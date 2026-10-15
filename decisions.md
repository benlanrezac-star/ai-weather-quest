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
