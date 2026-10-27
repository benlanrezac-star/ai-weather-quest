# memory.md — AI Weather Quest (faits vérifiés)

Dernière vérification : 14/10/2026. Revérifier toute ligne avant de s'appuyer dessus.

## Calendrier (source : aiweatherquest.ecmwf.int/competition-structure, page màj 14/07/2026 ; T&C màj 10/08/2026)
- Bridge SON 2026 : initialisations du 13/08 au 05/11/2026. Le jeudi 5 nov. est la DERNIÈRE semaine d'essai.
- DJF 2026 : initialisations du 12/11/2026 au 04/02/2027 (13 jeudis).
- MAM 2027 : 11/02 → 06/05/2027.
- Classement période : soumettre CHAQUE semaine des 13 semaines, même modèle (page Evaluation System).
- Chaque modèle doit avoir une « model methodology summary », publique (T&C art. 4).

## Calendrier hebdomadaire (source : /submitting-forecasts, màj 15/07/2026)
- J1 jeudi 00 UTC = initialisation. Seules les données horodatées ≤ jeudi 00 UTC sont autorisées.
- Fenêtre de soumission : jusqu'au dimanche 23:59 UTC (J4).
- Semaine 3 = jours 19-25 (lun → dim), semaine 4 = jours 26-32.
- Publication des scores : J37 (vendredi).

## Format (source : doc AI-WQ-package, submit_forecast.html)
- Variable 'tas', fc_period '1' ou '2', fc_start_date 'YYYYMMDD' (jeudi).
- Tableau (5, 121, 240) : quintile [0.2..1.0] × lat 90 → -90 pas -1.5 × lon 0 → 358.5.
- Somme sur l'axe quintile = 1 (contrôle officiel : atol 0,2) ; valeurs dans [0, 1] (tol 1e-5).
- NaN : le message du package les dit « permis », mais la somme avec skipna fait échouer un point tout-NaN, et le score officiel le compte RPS = 5 (pire cas). → Ne jamais soumettre de NaN (vérifié le 15/10/2026 sur AI-WQ-package 3.32).
- Dims attendues : quintile, latitude, longitude. Obs officielles : quintile étiqueté 0..4.
- teamname et modelname doivent être ceux de l'inscription.
- Nom de fichier : tas_YYYYMMDD_p1_<team>_<model>.nc. Vérification : AI_WQ_check_submission.

## Outils (doc installation + forum, fil 15249)
- AI-WQ-package ≥ 3.32 (3.32 ne tente plus le FTP, 22/09/2026 ; FTP fermé le 04/09/2026).
- sites-toolkit ≥ 20261005.1, depuis https://get.ecmwf.int/repository/pypi-all/simple (ECBox).
- Installation documentée « on Linux » → GitHub Actions (Linux) OK ; Windows local NON vérifié.
- Mot de passe de soumission envoyé par e-mail à l'inscription. Des équipes signalent des e-mails non reçus (08/10/2026).
- Le package sert aussi : données d'entraînement ERA5 hebdo 1,5° (retrieve_annual_training_data, ≥ 1979, latence 3 mois), évaluation (retrieve_evaluation_data, forecast_evaluation).
- GitHub : sur un dépôt public, les workflows planifiés sont désactivés après 60 jours sans activité → la tâche hebdo doit commiter (scores) chaque semaine.

## Score (source : /evaluation-system)
- RPSS vs climatologie, pondéré par l'aire.
- tas évalué sur les points à ≥ 50 % de terre seulement.
- Vérité : ERA5T. Bornes de quintiles : ERA5, 20 ans, échantillon élargi à 100 (± 4 jours, pas de 2 jours).
- RPSS période = ratio des RPS sommés sur tous les points et toutes les semaines (pas une moyenne des RPSS hebdo).

## Données IFS (sources : confluence S2S/Models màj 07/07/2026 ; licence S2S rev. 4 ; ECDS)
- ECMWF dans S2S via ECDS : délai 48 h, CC BY 4.0, 100+1 membres, quotidien, 1,5°, jours 0-46.
- Reprévisions ECMWF : à la volée, 20 dernières années, 10+1 membres, les jours impairs du mois (1, 3, …, 31, hors 29 févr.).
- Conséquence : prévision du jeudi 00 UTC disponible au plus tôt le samedi 00 UTC → ~48 h utiles avant la clôture.
- Incident documenté : données ECDS absentes du 22 au 27/07/2026 ; soumission par e-mail acceptée dans ce cas (forum, fil 15190).
- Accès ECDS (vérifié le 15/10/2026) : WEB-API fermée le 27/05/2026 ; API https://ecds.ecmwf.int/api ; client cdsapi ≥ 0.7.7 ; jeux `s2s-forecasts` / `s2s-reforecasts` ; variable `2_m_temperature` ; échéances moyennes journalières `a_b` (ex. `432_456`) ; pas de clé `number` ; reprévision = year/month/day (version du modèle) + hyear/hmonth/hday.
- Mesures du 27/10/2026 (clé et licences OK) :
  - temps réel, contrôle, 1 champ : 58 Ko, 266 s ;
  - reprévision, perturbed, 1 année × 1 échéance (10 membres) : 569 Ko, **4 725 s (79 min)** de file d'attente.
  - La taille ne pose aucun problème ; c'est la latence de la file qui est le risque.
- Semaines AI-WQ : observations du lundi au dimanche → depuis l'initialisation du jeudi 00 UTC, p1 = 432-600 h, p2 = 600-768 h.
- Tableau S2S indique CY49R1 ; un cycle CY50r1 est opérationnel depuis mai 2026 (Tech Memo 938) → à clarifier.

## Règles sensibles (T&C art. 4)
- Reprise directe d'une prévision ECMWF ou tierce « sans transformation significative » = risque de disqualification.
  → La baseline « IFS brut en quintiles » ne doit JAMAIS être soumise.
- Jusqu'à 3 modèles par équipe → un 2e modèle en parallèle est autorisé.
- Pas d'obligation de publier le code.

## Inscription (formulaire /ecmwf-ai-weather-quest-registration)
- Champs modèle : nom, type (Data-driven / Hybrid / Post-processing / Statistical / Unknown), nb de personnes, CPU, GPU, type d'infra, lien de doc (optionnel).
- Choix public / anonyme.
- Questionnaire de résumé du modèle : PDF lié depuis la page d'inscription.
