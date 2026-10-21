# 01 — Stratégie : où un duo « Chromium + temps » a une vraie chance

Réalité du terrain : ~2 164 chercheurs sur le programme, moyenne payée ≈ 438 $,
seul le **premier** rapport unique est payé. Les XSS évidentes et les IDOR triviaux sur les
endpoints historiques sont déjà passés au peigne fin depuis 2023. Notre avantage n'est pas
la puissance de feu (interdite de toute façon : pas de scanners/fuzzing), c'est la
**méthode sur les surfaces neuves et les transitions d'état**.

## Priorités (rapport probabilité × payout × faisabilité navigateur seul)

### 🥇 P1 — Contrôle d'accès entre NOS deux comptes (ChatGPT + Platform)
Le classique qui continue de payer quand une **nouvelle fonctionnalité** oublie un contrôle :
conversations, projets, fichiers uploadés, GPTs personnalisés, artefacts/contenus générés,
partages, espaces d'équipe. Méthode : A crée un objet, B tente lecture/écriture/suppression
par l'UI puis par la requête rejouée (compte B, identifiant de l'objet de A).
**Zooms à forte valeur : les transitions** — privé → partagé → partage révoqué → supprimé →
restauré ; renommage ; déplacement entre projets ; changement de propriétaire d'org.
Chaque transition est un endroit où un cache ou un contrôle saute.

### 🥈 P2 — Liens de partage & révocation
Un lien partagé continue-t-il de fonctionner après révocation/suppression/changement de
visibilité ? Le contenu « dé-partagé » reste-t-il accessible via un ancien identifiant,
une miniature, un export, une API annexe ? Tests 100 % navigateur, entre A et B.

### 🥉 P3 — XSS stockée via contenu partagé A → B
Surfaces où du texte contrôlé par A s'affiche chez B : titres, noms/descriptions de GPT,
noms de fichiers, contenus rendus (Markdown, tableaux, blocs de code, aperçus de liens).
On commence par des **marqueurs inertes** (texte unique, caractères spéciaux) pour voir
l'encodage ; on n'escalade qu'entre nos comptes, preuve minimale, jamais d'exfiltration.

### P4 — Autorisations fins Platform/API (si tu as accès API)
Rôles d'organisation/projet : un rôle restreint peut-il lire/créer au-delà de son périmètre ?
Clés de service vs clés utilisateur, projets archivés, membres retirés dont l'accès persisterait.
⚠️ Quantités minuscules, aucun brute-force, aucun contournement de quota à botter en touche.

### P5 — Codex / navigateur intégré / extension Chrome (surface récente)
Barème plus bas (P1 500–1 500 $) mais surface **neuve** donc moins ratissée : restrictions
d'origine du navigateur intégré, transferts de fichiers navigateur↔local, approbations
(one-time rejouée ? appliquée au mauvais site/acteur ?), frontières extension↔app.
Pré-requis : installer l'app desktop ChatGPT et/ou l'extension officielle. À ouvrir en Phase 2
si tu es partant.

### P6 — Recon passive `*.openai.org` / `*.openai.com` (en tâche de fond)
Logs de transparence de certificats (crt.sh) + DNS publics, depuis le navigateur, pour repérer
des sous-domaines **inutilisés** pointant vers des services tiers déprovisionnés
(subdomain takeover explicitement in-scope). Zéro scan agressif : lecture seule, et on ne
« prend » rien sans en parler d'abord ici.

### ❌ Ce qu'on ne fera jamais (hors-scope ou suicidaire pour le compte)
Jailbreaks et « le modèle m'a dit… », évasions du Code Interpreter *interne* à la sandbox,
fuzzing/brute-force/scraping massif, contournement Cloudflare/CAPTCHA, tests sur les GPTs
d'autrui, phishing, DoS, chasse aux en-têtes manquants. Voir `00-scope-et-regles.md`.

## Boucle de travail (une itération = un aller-retour)

1. Je te donne **un** test numéroté (objectif, prérequis, clics exacts, résultat attendu sain).
2. Tu l'exécutes, tu notes dans `journal.md`, tu me renvoies : date/heure UTC, compte utilisé,
   URL (sans token), code HTTP, extrait requis/réponse **sanitisé**, captures masquées.
3. Je qualifie : `RAS` / `à creuser` / `bug candidat`. Si candidat : on gèle, on reproduit
   une 2ᵉ fois proprement, je rédige le rapport (template EN), tu relis et tu soumets sur Bugcrowd.
4. On ne passe au test suivant qu'après qualification. Lent = propre = défendable devant le triage.

## Ce qui fait payer (critères du triage Bugcrowd/OpenAI)

- **Impact démontré, pas théorique** : « B lit le fichier privé de A » > « l'ID semble prévisible ».
- Attaquant **moins privilégié** franchissant une restriction **réellement appliquée**.
- Reproduction pas à pas sur version courante, comptes de test, preuves datées.
- Rapport le premier, unique, clair. D'où : dès qu'un candidat tient debout, on soumet vite,
  on peaufinera en commentaire si le triage demande.
