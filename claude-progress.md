# claude-progress.md

## Session 1 — 14/10/2026 — Cadrage avant code
Statut : terminée côté Claude ; actions de Benjamin en attente.

### Fait
- Règles revérifiées en ligne : site officiel, T&C du 10/08/2026, doc du package, forum, confluence S2S.
- Écarts trouvés par rapport aux instructions du projet :
  - La dernière semaine du Bridge est le jeudi 5 nov. (et non le 11 nov., qui est la fin administrative du Bridge).
  - Soumission via ECBox : AI-WQ-package ≥ 3.32 + sites-toolkit. Le FTP est fermé.
  - 2e modèle autorisé : jusqu'à 3 modèles par équipe.
  - L'IFS temps réel n'est disponible qu'avec 48 h de délai → la tâche automatique ne peut pas tourner le jeudi.
  - Soumettre l'IFS brut = risque de disqualification.
- Dossier de suivi créé : CLAUDE.md, memory.md, tasks.md, decisions.md, claude-progress.md, feature_list.json, .project-config.
- Git configuré sur le poste Windows ; dossier local C:\Users\Benjamin\dev\ai-weather-quest initialisé avec .gitignore.

### Comparaison aux jalons
- En avance d'une demi-semaine : la préparation du jalon du 19 oct. est faite.
- Rien n'est encore dans le dépôt GitHub. Ce travail ne laisse pas de trace publique tant que les fichiers ne sont pas commités.

### Prochaine session
1. Benjamin tranche D-003 à D-006.
2. Inscription faite, mot de passe reçu.
3. Squelette du dépôt et premier téléchargement S2S.

## Session 1 (suite) — 15/10/2026 — Dépôt GitHub en place
Statut : terminée.

### Fait
- Dépôt public créé : https://github.com/benlanrezac-star/ai-weather-quest
- Premier commit `23dec3a` (fichiers de suivi + .gitignore) poussé sur main.
- Dossier local : C:\Users\Benjamin\dev\ai-weather-quest (Windows, PowerShell).
- Compte GitHub : benlanrezac-star ; e-mail git = adresse noreply.

### Toujours en attente (Benjamin)
- Trancher D-003 à D-006 (decisions.md), surtout D-005 (noms) qui bloque l'inscription.
- Inscription AI Weather Quest + réception du mot de passe de soumission.
- Accès ECDS (licence S2S, clé API).

### Prochaine session
- Squelette du dépôt : uv, src/, tests/, pytest, CI GitHub Actions sur push.
- Choix de l'environnement local (Windows natif / WSL2 / Docker) pour sites-toolkit et cartopy.
