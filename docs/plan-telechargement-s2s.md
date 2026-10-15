# Plan — téléchargement ECMWF S2S (2t) via ECDS

Statut : **à valider par Benjamin avant tout code** (D-009, PROPOSÉE).
Rédigé le 15/10/2026. Sources consultées le même jour, listées en bas.

## 1. Accès

- Depuis le 27/05/2026, le S2S n'est plus servi que par l'ECMWF Data Store (ECDS). L'ancienne WEB-API (`ecmwfapi`) est fermée.
- API : `https://ecds.ecmwf.int/api`, avec un jeton personnel. La licence S2S doit être acceptée sur le portail.
- Bibliothèque proposée : **`cdsapi>=0.7.7`**.
  - C'est le client recommandé sur la page ECDS « how-to-api ».
  - L'alternative `ecmwf-datastores-client` est marquée « Incubating », et l'ECMWF dit ne pas demander la migration pour l'instant.
- Secret : variable `ECDS_KEY`, dans `.env` en local et dans les GitHub Secrets en CI.
  - Le client est construit explicitement : `cdsapi.Client(url=..., key=os.environ["ECDS_KEY"])`.
  - Raison : ne pas dépendre de `~/.cdsapirc`, qui peut déjà pointer vers le CDS (ERA5). L'ECMWF demande un `.cdsapirc` distinct par data store.

## 2. Jeux de données et paramètres

Clés relevées dans le schéma de l'API (`/api/retrieve/v1/processes/<dataset>`) le 15/10/2026.

| Clé | Temps réel `s2s-forecasts` | Reprévision `s2s-reforecasts` |
|---|---|---|
| origin | `ecmwf` | `ecmwf` |
| level_type | `single_level` | `single_level` |
| variable | `2_m_temperature` | `2_m_temperature` |
| forecast_type | `control_forecast` puis `perturbed_forecast` (2 requêtes) | idem |
| year / month / day | date d'initialisation (jeudi) | **date de version du modèle** (jour impair ≤ jeudi, cf. D-003) |
| hyear / hmonth / hday | — | les 20 années de reprévision, même mois/jour |
| time | `00:00` | `00:00` |
| leadtime_hour | 14 intervalles journaliers `432_456` … `744_768` | idem |
| data_format | `grib` (seule option) | `grib` |
| area | omis (global) | omis |

Points à noter :
- Le nom de la variable est `2_m_temperature`. L'exemple de la page how-to-api écrit `2m_temperature`, qui n'existe pas dans le schéma.
- Les intervalles `a_b` désignent la moyenne journalière S2S de 2t (moyenne sur 24 h). C'est ce qu'il faut pour une moyenne hebdomadaire.
- Échéances : l'initialisation est le jeudi 00 UTC, et les semaines d'observation AI-WQ commencent le lundi (`retrieve_evaluation_data.py`).
  - Semaine 3 (p1) = jours 19-25 = échéances 432 → 600 h.
  - Semaine 4 (p2) = jours 26-32 = échéances 600 → 768 h.
- Il n'existe pas de clé `number` : `perturbed_forecast` renvoie tous les membres (100 en temps réel, 10 en reprévision). On ne peut pas sous-échantillonner côté serveur.
- La grille par défaut est en longitudes -180 → 180. Il faut la convertir en 0 → 358,5 et vérifier que les latitudes vont de 90 à -90 (`aiwq.grid`).

## 3. Volume estimé

Hypothèse : grille globale 1,5° = 121 × 240 = 29 040 points. En GRIB codé sur 12 à 24 bits, cela fait **≈ 45 à 90 Ko par champ**. Valeur à mesurer au premier téléchargement.

| Lot | Champs | GRIB brut | Après réduction en moyennes hebdo (float32) |
|---|---|---|---|
| 1 jeudi temps réel (101 membres × 14 j) | 1 414 | 65 – 130 Mo | 23 Mo |
| 1 date de reprévision (20 ans × 11 membres × 14 j) | 3 080 | 140 – 280 Mo | 51 Mo |
| Saison DJF temps réel (13 jeudis) | 18 382 | 0,8 – 1,7 Go | 0,3 Go |
| 26 dates de reprévision (entraînement) | 80 080 | 3,6 – 7,2 Go | 1,3 Go |

Conséquences :
- On convertit en moyennes hebdomadaires dès le téléchargement, et on ne garde pas le GRIB brut (dossier `data/`, ignoré par git).
- En CI, la tâche du samedi doit télécharger environ 0,2 à 0,4 Go (temps réel + la reprévision de la semaine). C'est compatible avec un runner GitHub (environ 14 Go de disque libre).

## 4. Découpage des requêtes

- Une requête = (jeu de données, date, forecast_type), avec les 14 échéances et, pour une reprévision, les 20 années.
- La limite de taille par requête et le temps d'attente dans la file ECDS ne sont **pas documentés** : il faut les mesurer au test minimal.
  - Si la requête de reprévision est refusée, on la découpe par `hyear`.
- Le téléchargement est idempotent : on ne relance pas une requête si le fichier cible existe et se lit.

## 5. Lecture GRIB

- Proposition : `cfgrib` + `eccodes` (roues binaires pip), puis conversion en xarray et NetCDF.
- Incertitude : roues `eccodes` sous Windows non vérifiées. À tester localement ; repli sur WSL2 ou sur la CI Linux (risque n° 4 de CLAUDE.md).

## 6. Fuites de données

- Temps réel : uniquement l'initialisation du jeudi 00 UTC (règle AI-WQ : données ≤ jeudi 00 UTC).
- Reprévision : date de version ≤ jeudi. Les années de reprévision s'arrêtent à l'année précédente.
- Les bornes de quintiles et la vérité viennent d'ERA5 via le package AI-WQ. Le découpage entraînement / validation se fait par année de reprévision (à fixer en D-0xx avec le jeu d'entraînement).

## 7. Question ouverte — à trancher par Benjamin (touche le modèle soumis)

Les reprévisions ECMWF sont produites à la volée avec le cycle en cours. Or un nouveau cycle est opérationnel depuis mai 2026 (CY50r1 selon le Tech Memo 938, encore à confirmer). Conséquence : **aucune reprévision du cycle actuel n'existe pour des dates d'hiver (nov. → févr.) avant qu'elles ne soient produites cet hiver**.

Options :
- **A. Calibration « à la volée »** : chaque semaine, on ajuste le modèle sur la reprévision de la même date de version, avec le même cycle et la même saison. C'est l'approche standard (anomalies ECMWF). En contrepartie, la tâche du samedi télécharge aussi la reprévision, soit environ 2 à 3 fois plus de volume.
- **B. Entraînement figé** sur les reprévisions de l'hiver 2025/26, produites avec l'ancien cycle : même saison, mais un biais de cycle possible.
- **C. Entraînement figé** sur les dates sept. → oct. 2026, produites avec le cycle actuel : même cycle, mais une saison décalée.

Recommandation : **A pour la v1**, et B uniquement pour la validation hors ligne (RPSS sur l'hiver 2025/26).

## 8. Test minimal proposé (après validation)

1. Récupérer le contrôle temps réel d'un jeudi récent (par ex. le 08/10/2026), avec une seule échéance. On mesure la taille, le temps de file et le format.
2. Récupérer une reprévision `perturbed_forecast` sur 1 an et 1 échéance.
3. Écrire une fonction de construction des requêtes, testée sans réseau : clés, dates, échéances. Le téléchargement réel reste hors pytest.

## Sources (consultées le 15/10/2026)

- ECDS, « CDSAPI setup » : https://ecds.ecmwf.int/how-to-api
- Schéma API ECDS : https://ecds.ecmwf.int/api/retrieve/v1/processes/s2s-forecasts et …/s2s-reforecasts
- Forum ECMWF, « S2S and TIGGE access method » (fil 15020) : https://forum.ecmwf.int/t/s2s-and-tigge-access-method/15020
- Guide de migration S2S/TIGGE vers ECDS : https://confluence.ecmwf.int/x/XzaXGw
- AI-WQ-package 3.32 (PyPI), `retrieve_evaluation_data.py` (semaines commençant le lundi)
