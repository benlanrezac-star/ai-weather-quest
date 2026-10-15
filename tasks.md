# tasks.md

Légende : [ ] à faire · [~] en cours · [x] fait · (B) = Benjamin seul · (C) = avec Claude

## Avant de coder — cette semaine (14 → 18 oct.)

### Décisions
- [ ] (B) Valider ou modifier D-003 à D-006 dans decisions.md.

### Inscription
- [ ] (B) S'inscrire sur aiweatherquest.ecmwf.int, une fois les noms de D-005 choisis.
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
- [ ] (B) Lire le questionnaire de résumé de modèle (PDF), à remplir avant DJF.

## Semaine du 19 oct. (jalon 1)
- [ ] Squelette du dépôt : uv, src/, tests/, pytest, CI.
- [ ] Téléchargement d'un échantillon : IFS S2S (prévision + reprévision) et ERA5 via le package.
- [ ] Climatologie de référence via retrieve_evaluation_data.
- [ ] Premier essai de soumission ECBox avec le modèle d'essai, jeudi 22 oct. (si D-006 est validée).

## Plus tard (voir jalons dans CLAUDE.md)
