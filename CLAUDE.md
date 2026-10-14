# CLAUDE.md — AI Weather Quest (Benjamin Lanrezac)

## Ordre de lecture en début de session
memory.md → tasks.md → decisions.md → claude-progress.md

## Objectif
13 soumissions consécutives sur la période DJF (jeudis 12/11/2026 → 04/02/2027), même modèle, même nom.
Chaîne automatique, dépôt public, note de méthode.
Un RPSS proche de 0 est acceptable ; une semaine manquée ne l'est pas, car elle exclut du classement de la période.

## Approche
- Post-traitement des prévisions ECMWF S2S : calibration des probabilités de quintiles de tas.
- Entraînement sur les reprévisions, avec un découpage temporel sans fuite.
- La baseline « IFS brut » sert à la validation uniquement, jamais à la soumission (T&C art. 4).

## Jalons
Les jalons ci-dessous intègrent D-004, qui est encore PROPOSÉE.

| Semaine | Contenu |
|---|---|
| 19 oct. | Inscription, squelette du dépôt, échantillons IFS + ERA5, 1er essai de chaîne (22 oct.) |
| 26 oct. | Jeu d'entraînement, baselines, RPSS en validation |
| 2 nov. | Modèle v1, MLflow, essai réel jeudi 5 nov. (dernière semaine Bridge) |
| 9 nov. | Gel, Docker, GitHub Actions le samedi + relance dimanche, répétition, go / no-go mer. 11 nov. |
| 12 nov. → 4 févr. | Soumissions automatiques (exécution le samedi), scores dans DuckDB |
| 8 févr. | Bilan + note de méthode |

## Risques connus
1. Délai de 48 h sur l'IFS : la fenêtre utile va du samedi 00 UTC au dimanche 23:59 UTC.
2. Panne ECDS déjà vue en juillet 2026 : prévoir un repli sur la climatologie avec le même nom de modèle, et suivre le forum.
3. Semaines du 24 et du 31 déc., et examens Cnam du 25 janv. au 5 févr. : aucune intervention manuelle ne doit être nécessaire.
4. Windows : sites-toolkit et cartopy ne sont documentés que pour Linux.
5. Une seule semaine d'essai réel du v1 (5 nov.) si la chaîne n'est pas testée avant.
6. GitHub désactive les workflows planifiés d'un dépôt public après 60 jours sans activité : la tâche hebdo doit commiter ses scores.

## Conventions
- Python 3, xarray, scikit-learn, uv, pytest.
- Commits en anglais, courts.
- Commandes PowerShell pour le local.
- Aucune donnée Akkodis, Fugro ou ABPmer.
- Secrets (mot de passe AI-WQ, clé ECDS) : uniquement dans les GitHub Secrets et un .env local ignoré par git. Jamais dans le dépôt.
