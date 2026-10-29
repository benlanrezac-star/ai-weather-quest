# tasks.md

Légende : [ ] à faire · [~] en cours · [x] fait · (B) = Benjamin seul · (C) = avec Claude

## Avant de coder — cette semaine (14 → 18 oct.)

### Décisions
- [ ] (B) Valider ou modifier D-003 à D-006 dans decisions.md.

### Inscription
- [x] (B) S'inscrire sur aiweatherquest.ecmwf.int, une fois les noms de D-005 choisis (fait le 19/10).
  - Type de modèle : Post-processing.
  - Résultats publics (le but est de les montrer en entretien).
- [ ] (B) Vérifier la réception de l'e-mail contenant le mot de passe de soumission.
  - Sans réponse sous 3 jours : écrire à aiweatherquest@ecmwf.int.
- [ ] (B) Créer un compte sur le forum ECMWF et suivre la catégorie AI Weather Quest (annonces, pannes).

### Accès aux données
- [ ] (B) Compte ECMWF : se connecter à ecds.ecmwf.int, accepter la licence S2S, récupérer la clé API ECDS.
- [ ] (B) Compte CDS : vérifier que la clé fonctionne (pour l'ERA5 brut, hors package).
- [ ] (C) Test minimal : télécharger 1 prévision S2S ECMWF (2t, 1 date) et 1 reprévision.

### Dépôt
- [x] (B) Configurer git (user.name, user.email noreply), git init, .gitignore.
- [x] (C) Copier les fichiers de suivi dans le dépôt local.
- [x] (B) Créer le dépôt GitHub public `ai-weather-quest` (github.com/benlanrezac-star/ai-weather-quest).
- [x] (B) Premier commit + push (15/10/2026).
- [ ] (C) Décider si l'environnement local est Windows natif, WSL2 ou Docker.
  - Raison : sites-toolkit et cartopy ne sont documentés que pour Linux.

### Lecture
- [ ] (B) Regarder le pas-à-pas du package (YouTube, webinaire « What's Next », 16/07/2026).
- [~] (C) Questionnaire de résumé de modèle : brouillon docs/model-summary.md (27/10). À remplir dans les 4 dernières semaines de DJF.

## Semaine du 19 oct. (jalon 1)
- [x] (C) Squelette du dépôt : uv, src/, tests/, pytest, CI (15/10, D-007).
- [x] (C) Modules grid, rps, climatology + 26 tests (15/10, D-008).
- [x] (B) Option A/B/C tranchée : A, calibration à la volée (D-010, 15/10).
- [x] (B) D-009 adoptée (28/10). Hiver 2025/26 en validation hors ligne : encore à confirmer.
- [ ] (C) Après D-009 : construction des requêtes ECDS (testée sans réseau) + test minimal réel (§ 8 du plan).
- [ ] (B) Ajouter le secret `ECDS_KEY` (GitHub Secrets + .env local) une fois la clé ECDS obtenue.
- [x] (C) 1er run CI GitHub Actions vert (3.11 + 3.12, 15/10).
- [ ] Téléchargement d'un échantillon : IFS S2S (prévision + reprévision) et ERA5 via le package.
- [ ] Climatologie de référence via retrieve_evaluation_data.
- [x] (C) Premier essai de soumission ECBox : climatologie sous SoloWQ / MetoceanML, init. 29/10, p1 + p2 soumis le 29/10 à 13:20 UTC, confirmés par AI_WQ_check_submission.

## Plus tard (voir jalons dans CLAUDE.md)
