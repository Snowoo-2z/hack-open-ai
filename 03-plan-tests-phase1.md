# 03 — Plan de tests Phase 1 (ChatGPT web, comptes A/B, navigateur seul)

Règles de la phase : manuels uniquement, rythme humain, **que nos objets**.
On exécute dans l'ordre, un test par aller-retour. Si un résultat te semble anormal :
**stop**, note tout, renvoie-moi — ne « pousse » pas plus loin pour voir.

Légende statut : ☐ à faire · 🔄 en cours · ✅ RAS (comportement sain) · 🔎 à creuser · 🚩 candidat

---

## Mission 0 — Setup + inventaire (prérequis à tout)

☐ Setup complet de `02-setup-chromium.md` (profils OAI-A / OAI-B connectés).
🔄 **Inventaire des surfaces** — 1ᵉʳ passage fait le 2026-10-22 via la mission d'exemple
(compte A **Free**, interface FR). Confirmé visible : Nouveau chat, **Images**, **Planifié**,
**Bibliothèque**, **Plugins**, **Codex**, **Explorer**, **Projets** (aucun), Récents,
bouton `+` (pièces jointes), « Rejoindre l'espace de travail », mode Work = « Forfait
supérieur requis ». Réseau observé (filtré) : `GET /backend-api/wham/usage` (200).
Reste à confirmer au fil des missions : bouton Partager sur une conversation, écran de
création de GPT (Explorer), Paramètres (mémoire, connecteurs, export), platform.openai.com.

## Famille 1 — Objets privés de A, tentatives d'accès de B (cœur de la chasse)

Pour chaque type d'objet que l'inventaire aura confirmé (je détaillerai les clics au cas par cas) :

- ☐ **T-01 Conversation non partagée** : A crée une conversation contenant un marqueur unique
  (ex. `MARQUEUR-A-2026-001` — texte inventé par nous, zéro donnée réelle). A note l'URL/ID.
  Dans le profil B : ouvrir l'URL directement. **Sain attendu** : 404 / « introuvable » / redirection.
  Renvoie : code HTTP de la requête principale (Network), message affiché, capture B.
- ☐ **T-02 Fichier joint privé** : A joint un fichier texte inoffensif créé par nous à sa
  conversation ; B tente d'ouvrir l'URL du fichier récupérée côté A (Network, sans les cookies).
  **Sain** : refus ou URL signée à expiration courte non rejouable hors contexte.
- ☐ **T-03 Projet privé** : même schéma si les Projets existent sur ton compte (URL du projet
  ouvert avec B ; conversation du projet ouverte avec B).
- ☐ **T-04 GPT personnalisé privé** (si la création est dispo en gratuit chez toi) : GPT de A en
  visibilité « moi uniquement » ; B ouvre son URL. **Sain** : refus net, aucune fuite du nom,
  de la description ni des instructions dans la réponse réseau.

> Pour T-01→T-04, je te demanderai aussi la **réponse JSON** de la requête XHR principale côté B
> (Network → la requête → Response) : un refus « propre » en UI qui laisserait fuiter des métadonnées
> dans le JSON serait déjà un début de piste. Texte brut, après sanitisation.

## Famille 2 — Partage & révocation (transitions d'état)

- ☐ **T-05 Partage puis révocation** : A partage sa conversation marqueur via lien, B l'ouvre
  (OK attendu), A **révoque** le partage, B recharge le lien. **Sain** : accès coupé partout
  (page, XHR, éventuel export). Note le délai de coupure observé.
- ☐ **T-06 Suppression après partage** : A partage, B ouvre, A **supprime** la conversation,
  B recharge. **Sain** : contenu inaccessible aussi par le lien précédemment valide.
- ☐ **T-07 Renommage/modification après partage** : A modifie le contenu/titre après émission
  du lien ; qu'est-ce que B voit : instantané figé ou version live ? L'un ou l'autre peut être
  légitime — on documente, on compare à ce que l'UI promet à A (« copie » vs « lien vivant »).
  Écart promesse/réalité = piste.

## Famille 3 — Écriture croisée (B ne doit rien pouvoir modifier chez A)

On ne teste l'écriture que via l'interface d'abord ; le rejeu de requête modifiée (ID de A,
session de B) ne se fera que sur **une** ressource précise, à ma demande explicite, après
revue de la requête légitime équivalente de B sur **son propre** objet.

- ☐ **T-08 Inventaire des actions d'écriture** : avec B sur **son** objet clone (même marqueur,
  préfixe B), lister les requêtes XHR de : renommer, supprimer, partager, déplacer.
  Renvoie-moi la liste `méthode + chemin` (sans domaine complet ni token) : c'est la matière
  qui me sert à écrire d'éventuels tests d'autorisation ciblés, un par un.

## Famille 4 — Rendu de contenu A chez B (pré-XSS, marqueurs inertes uniquement)

- ☐ **T-09 Caractères spéciaux en aller-retour** : A met dans un titre/nom partagé vers B une
  chaîne inerte du type `TEST <b>gras</b> "guillemets" & entités` ; on observe chez B :
  affiché en texte brut (encodé = sain) ou interprété (gras réel = 🔎, on s'arrête là et on parle).
  Aucun payload d'exécution à ce stade, sous aucun prétexte.

## Famille 5 — Recon passive sous-domaines (tâche de fond, lecture seule)

- ☐ **T-10 Énumération par certificats** : navigateur → `crt.sh` → recherches `%.openai.org`
  puis `%.openai.com`. Export/liste des noms distincts. On trie ensemble, on ne visite
  individuellement **que** des noms qui semblent abandonnés (je fournis les critères),
  et on ne revendique aucun service tiers sans revue ici d'abord.

## Hors Phase 1 (on décidera après tes réponses au setup)

- Platform/API : rôles org/projet, clés, membres retirés (nécessite accès API).
- Codex desktop + extension Chrome officielle : origine/approbations/fichiers (nécessite installs).
- GPT Actions / connecteurs OAuth créés par toi vers un serveur à toi (SSRF, redirect_uri, state).
