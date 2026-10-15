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

## Session 2 — 15/10/2026 — Squelette du dépôt et métriques
Statut : terminée côté Claude ; D-009 en attente de Benjamin.

### Fait
- Squelette : pyproject.toml (uv_build), uv.lock, .python-version 3.12, src/aiwq/, tests/, CI `.github/workflows/tests.yml` (D-007).
- `aiwq.grid` : grille 1,5° + `check_submission_array` (plus strict que l'officiel : pas de NaN, somme ± 1e-6).
- `aiwq.rps` : RPS / RPSS alignés sur AI-WQ-package 3.32 (D-008).
- `aiwq.climatology` : prévision 0,2 partout, baseline et repli.
- `uv run pytest` : 26 tests passent en local (Windows, Python 3.12.10).
- Plan de téléchargement S2S écrit, sans code : docs/plan-telechargement-s2s.md (D-009, PROPOSÉE).

### Constats
- Les NaN sont pénalisés au maximum par le score officiel (RPS = 5), et un point tout-NaN échoue au contrôle officiel. memory.md est corrigé.
- WEB-API S2S fermée depuis le 27/05/2026 : seul l'ECDS fonctionne.
- Reprévisions à la volée + changement de cycle en mai 2026 : pas de reprévisions d'hiver du cycle actuel avant cet hiver → question A/B/C dans le plan.

### Comparaison aux jalons (au 15/10)
- Jalon du 19 oct. : le squelette est fait, en avance.
- Sur le chemin critique, encore bloqués côté Benjamin :
  - inscription et mot de passe de soumission ;
  - clé ECDS + licence S2S ;
  - D-004 et D-006.
- L'essai ECBox du 22 oct. dépend de l'inscription et de D-006.
- Le téléchargement S2S réel dépend de la clé ECDS et de D-009.
- Pas de retard qui menace le 12 nov. à ce stade. Si l'inscription n'est pas faite d'ici le 20 oct., l'essai du 22 oct. glisse au 29 oct. et il ne reste qu'une semaine de marge avant le 5 nov.
