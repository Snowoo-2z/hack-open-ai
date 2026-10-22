# Journal de bord — une ligne par test, toujours datée (UTC)

> Ne jamais y écrire : tokens, cookies, clés, données personnelles, détails exploitables
> d'une faille non rapportée. Si 🚩 : écrire seulement « candidat T-xx, voir Bugcrowd ».

| Date (UTC) | Test | Compte | Résultat (✅ RAS / 🔎 / 🚩) | Note courte |
|---|---|---|---|---|
| 2026-10-21 | — | — | — | Lecture du brief Bugcrowd, kit initial créé. |
| 2026-10-22 | Mission 0 | — | 🔄 | Alias @bugcrowdninja.com validé (mails de test reçus, alias simple et variante `+`). Création des comptes A/B en cours. |
| 2026-10-22 | Mission 0 | — | 🔄 | Navigateur pas encore installé côté chercheur : instructions officielles ajoutées (§0 du setup) + clarification : aucun contrôle à distance, tests manuels. En attente OS + navigateur choisi. |
| 2026-10-22 | Mission 0 | — | 🔄 | OS chercheur confirmé : **Windows**, Git + PowerShell disponibles, Chrome installé. |
| 2026-10-22 | Exemple pilot | A | ✅ | 1ʳᵉ mission pilotée OK (connexion CDP, page_info, extraction). Compte A Free, UI FR ; surfaces confirmées : Images, Planifié, Bibliothèque, Plugins, Codex, Explorer, Projets. 2 bugs du harnais corrigés (capture en timeout → repli CDP ; réseau lettre-par-lettre → format + filtre API). Ajouts confort : ouverture auto du dossier résultats, fichier unique `A-MENVOYER.md`, lanceur `GO.bat`, transfert d'URL A→B sans copier-coller. |
| 2026-10-22 | T-01 (partie A) | A | ✅ | Conversation privée marqueur créée (09:05 UTC) : `MARQUEUR-A-001` TROUVÉ chez A (attendu), URL sauvegardée en local pour la partie B, capture OK. Bouton **Partager** confirmé sur la conversation (→ T-05 faisable). Endpoints observés : `POST /backend-api/f/conversation`, `POST /backend-api/conversation/init`, `GET /backend-api/conversations/{id}` (200 chez le propriétaire — c'est LE code à surveiller chez B), `GET /backend-api/wham/tasks/list`, `GET /backend-api/bazaar/conversation/{id}/ads`. En attente partie B. |
