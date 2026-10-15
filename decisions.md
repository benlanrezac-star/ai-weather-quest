# decisions.md

Statuts : ADOPTÉE · PROPOSÉE (en attente de Benjamin) · REMPLACÉE.
Toute décision qui touche le modèle soumis ou le calendrier reste PROPOSÉE tant que Benjamin ne l'a pas validée.

---

## D-001 · Approche : post-traitement de l'IFS, pas d'émulateur global — ADOPTÉE
- Date : 14/10/2026 (reprise des instructions du projet).
- Pourquoi : coût de calcul nul côté GPU ; c'est l'approche qui a gagné les périodes précédentes.
- Conséquence : la v1 dépend de la disponibilité des données IFS en temps réel (voir D-003).

## D-002 · Variable unique pour la v1 : tas — ADOPTÉE
- Date : 14/10/2026.
- Les deux échéances (p1 et p2) sont soumises chaque semaine.
- MJO et TS : hors périmètre v1.

## D-003 · Source IFS : ECMWF S2S sur ECDS (délai 48 h) — PROPOSÉE
- Date : 14/10/2026.
- Données : temps réel 100+1 membres ; reprévisions à la volée, 20 ans, 10+1 membres, jours impairs.
- Écart prévision / reprévision à traiter : 101 membres en temps réel, 11 en reprévision. La calibration doit être entraînée sur 11 membres, puis appliquée sur 11 membres tirés du temps réel, ou sur une statistique robuste à la taille d'ensemble.
- Date de reprévision : le jeudi tombe une fois sur deux un jour pair → prendre la reprévision du jour impair le plus proche, en n'utilisant que des dates ≤ jeudi.
- À valider par Benjamin : accès ECDS + acceptation de la licence S2S.

## D-004 · Tâche automatique le samedi, pas le jeudi — PROPOSÉE (change le calendrier)
- Date : 14/10/2026.
- Pourquoi : la prévision du jeudi 00 UTC n'est publiée qu'au samedi 00 UTC (délai 48 h). Une tâche le jeudi n'aurait pas les données.
- Proposition :
  - cron samedi 06:00 UTC ;
  - relance automatique le dimanche 06:00 UTC si aucune soumission n'est détectée ;
  - alerte e-mail en cas d'échec ;
  - procédure manuelle de secours le dimanche avant 20:00 UTC.
- Remplace « GitHub Actions planifié le jeudi » dans les jalons.

## D-005 · Noms d'équipe et de modèle — ADOPTÉE
- Date : 15/10/2026.
- Équipe : `SoleWQ`. Modèle : `MetoceanML`.
- Ces noms doivent être utilisés à l'identique (casse comprise) dans AI_WQ_create_empty_dataarray et AI_WQ_forecast_submission.
- Le nom du modèle est figé sur toute la période DJF.
- Type de modèle à l'inscription : Post-processing.

## D-006 · Modèle d'essai séparé pendant le Bridge — PROPOSÉE
- Inscrire un 2e nom de modèle (ex. `chaintest`) pour tester la chaîne pendant le Bridge, avec une prévision climatologique.
- Le modèle v1 n'apparaît qu'à partir de son premier essai réel.
- Permet de tester ECBox dès le 22 ou le 29 oct. sans attendre la v1.
- À confirmer :
  - qu'un modèle « climatologie » est acceptable en essai Bridge (question au forum ou à aiweatherquest@ecmwf.int) ;
  - si l'inscription d'un 2e modèle se fait après coup, depuis le tableau de bord.

## D-007 · Outillage : Python 3.12, uv, layout src/, CI 3.11 + 3.12 — ADOPTÉE
- Date : 15/10/2026.
- `.python-version` = 3.12 (version installée en local) ; `requires-python >=3.11,<3.13`.
- Backend de build `uv_build`, package `aiwq` sous `src/`, dépendances figées dans `uv.lock`.
- CI : GitHub Actions `tests.yml`, ubuntu-latest, uv 0.11.14 figé, matrice 3.11 / 3.12, `uv sync --locked` puis `uv run pytest`.
- Pourquoi 3.11 aussi : compatibilité de sites-toolkit non vérifiée ; on garde la porte ouverte sans coût.

## D-008 · Convention de score alignée sur AI-WQ-package 3.32 — ADOPTÉE
- Date : 15/10/2026. Source : `forecast_evaluation.py` et `check_fc_submission.py` (roue PyPI 3.32), comportement vérifié en exécutant `calculate_RPS` sur un cas jouet.
- RPS = somme sur les 5 quintiles des écarts cumulés au carré, sans division par K-1.
- Masque terre : points à fraction ≥ 0,5 ; pondération cos(lat).
- RPSS de période = 1 − Σ w·RPS_fc / Σ w·RPS_clim, sur tous les points et toutes les semaines.
- Une prévision NaN est comptée comme une probabilité nulle (RPS = 5 au pire), comme dans le code officiel. Les points d'observation tout-NaN sont exclus.
- Le contrôle de format `aiwq.grid.check_submission_array` est plus strict que l'officiel :
  - aucun NaN accepté (l'officiel rejette de toute façon un point tout-NaN, car sa somme vaut 0) ;
  - somme des quintiles à 1 ± 1e-6 (l'officiel tolère ± 0,2).

## D-009 · Téléchargement S2S : cdsapi sur ECDS, réduction immédiate en moyennes hebdo — PROPOSÉE
- Date : 15/10/2026. Détail : `docs/plan-telechargement-s2s.md`.
- Bibliothèque `cdsapi>=0.7.7`, client construit avec `ECDS_KEY`.
- Jeux `s2s-forecasts` et `s2s-reforecasts`, variable `2_m_temperature`, échéances `432_456` … `744_768`.
- Question liée (A/B/C) : tranchée par D-010.

## D-010 · Modèle soumis : calibration à la volée (option A) — ADOPTÉE
- Date : 15/10/2026. Validée par Benjamin.
- Chaque semaine, le modèle est ajusté sur la reprévision ECMWF de la date de version associée au jeudi (jour impair ≤ jeudi, cf. D-003) : même cycle et même saison que la prévision du jour.
- Pourquoi : aucune reprévision d'hiver du cycle actuel n'existe avant cet hiver (reprévisions à la volée + changement de cycle en mai 2026). B (ancien cycle) et C (hors saison) introduisent un biais.
- Conséquences :
  - la tâche du samedi télécharge le temps réel ET la reprévision, soit ~0,2 à 0,4 Go par semaine ;
  - l'ajustement se fait dans la tâche hebdomadaire : il doit être rapide et sans réglage manuel ;
  - l'échantillon d'entraînement est petit (20 ans × 11 membres par date), d'où un modèle peu paramétré pour la v1.
- Encore PROPOSÉ : utiliser l'hiver 2025/26 (option B) uniquement pour la validation hors ligne, jamais pour la soumission.
- À vérifier au test minimal : que la reprévision de la date de version est publiée au plus tard le samedi 00 UTC. Sinon, prendre la date de version impaire précédente.
