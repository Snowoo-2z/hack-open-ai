# 00 — Scope & règles (résumé FR du brief Bugcrowd OpenAI, lu le 2026-10-21)

Source faisant foi, toujours vérifier avant de tester : https://bugcrowd.com/engagements/openai
En cas de doute entre ce résumé et le brief : **le brief gagne**. En cas de doute tout court :
support@bugcrowd.com **avant** de tester.

Chiffres du programme (21 oct. 2026) : 663 vulnérabilités récompensées, ~2 164 chercheurs,
paiement moyen ≈ 438 $, 75 % des rapports acceptés/rejetés sous 13 jours. Max exceptionnel : 100 000 $.

## ✅ In-scope (payé) — par cible

| Cible | Exemples | Barème indicatif |
|---|---|---|
| **API OpenAI** — `api.openai.com` + infra cloud qui sert l'API | AuthN/Z, exposition de données, accès modèles privés/non publiés | P1 2 000–6 500 $, P2 1 000–2 000 $, P3 500–1 000 $, P4 200–500 $ |
| **ChatGPT** — chatgpt.com / chat.openai.com, Plus, login, abonnements, plugins OpenAI (Browsing, Code Interpreter), plugins/GPTs **créés par toi** | XSS stockée/réfléchie, CSRF, SQLi, auth, autorisation (IDOR), exposition de données, paiements, exécuter des requêtes sur des modèles privés/pre-release | P1 2 000–6 500 $ … P4 200–500 $ |
| **Codex** — CLI, web, desktop, navigateur intégré de l'app ChatGPT desktop, extension Chrome ChatGPT (`hehggadaopoacecdllhhajmbjkdcmajg`) | Évasion de sandbox (fichiers/réseau/processus au-delà de la politique active), franchissement d'origine du navigateur intégré, abus des canaux navigateur↔extension↔app, contournement d'approbations requises, accès cross-origin non autorisé | P1 500–1 500 $, P2 250–500 $, P3 100–250 $, P4 50–100 $ |
| **OpenAI Research** — `openai.org`, `*.openai.org` | Web/API testing classique | P1 1 250–3 500 $ … P3 200–600 $ |
| **Autres cibles OpenAI** — `openai.com`, `*.openai.com`, docs développeur, `platform.openai.com/playground`, autre infra publique OpenAI | Idem + **subdomain takeover sur sous-domaine inutilisé encore in-scope** | P1 1 250–2 500 $ … P3 200–600 $ |
| **Docs corporate chez des tiers** (Google Workspace, Notion, Jira, Stripe…) | Uniquement *retrouver* de l'info confidentielle OpenAI exposée. **Interdit de tester ces entreprises.** | Souvent P4/P5 = peu/pas payé |
| **Clés API OpenAI fuitées** (`sk-`, `sess-`) | ⚠️ **NE PAS soumettre via Bugcrowd** (pénalité de points). Formulaire dédié uniquement, bonus mensuel au meilleur lot : https://forms.gle/h8bQ5YKWzXb8FtrQ8 | Bonus mensuel |

Points précis du brief à connaître :

- **Accès à un modèle privé/non publié** (absent de la doc API et du sélecteur de modèles) =
  éligible, sévérité selon la sensibilité du modèle. ⚠️ Mais *brute-forcer* l'API pour deviner
  des noms de modèles = interdit (voir ci-dessous). Seule une découverte par une faille réelle compte.
- **Prompt injection au niveau applicatif** : les chaînes plausibles à faible interaction qui
  transfèrent des données utilisateur vers un tiers *dans les applications* intéressent OpenAI,
  à condition d'être ancrées dans la couche application (pas « le modèle a obéi »).
- Codex : un bypass doit violer une restriction **réellement appliquée** par la config supportée
  active. Persuader le modèle d'abuser d'un accès qu'il a déjà ≠ bug. Fonctions `/experimental`
  de Codex CLI = non éligibles. Vulnérabilités Chromium upstream reproduites à l'identique dans
  Chrome = à reporter chez Google, pas ici.
- In-app browser / UI Codex : spoofing visuel sans impact P1 = P5 informationnel, **non payé**.

## 🚫 Hors-scope (0 €, ne pas perdre de temps dessus)

- **Tout ce qui est « modèle »** : jailbreaks/DAN, faire dire/faire écrire des choses interdites
  au modèle, hallucinations, le faire « semblant » d'exécuter du code ou de révéler des secrets.
  → Formulaire séparé : https://openai.com/form/model-behavior-feedback
  (il existe aussi un programme **Safety** distinct : https://bugcrowd.com/engagements/openai-safety)
- Exécution de code **dans** les sandbox prévues (Code Interpreter Python, Agent Mode, outil
  `container` GPT-5 en `root` sous gVisor). C'est une fonctionnalité. Un prétendu RCE doit prouver
  la sortie de sandbox avec les indicateurs du brief (`uname -a`, `whoami`, `hostname -I` vs `/etc/hosts`…).
- DoS / dégradation, **brute force, password spraying, spam, fuzzing** (sauf autorisation explicite),
  scanners automatisés agressifs (ils peuvent aussi te faire bannir — le brief le dit noir sur blanc).
- Social engineering / phishing du personnel OpenAI, attaques physiques, email (SPF/DKIM/DMARC).
- Clickjacking, en-têtes HTTP manquants sans PoC, ciphers TLS sans PoC, version strings,
  messages d'erreur serveur sans exploit.
- Contournement Cloudflare sur `api.openai.com`, CAPTCHA, géoblocage/VPN, page « at capacity ».
- Domaines CNAME vers un tiers **actif** (ex. `pay.openai.com` → Stripe : reporter chez Stripe ;
  `community.openai.com`). Sites non-OpenAI : `ai.com`, `open.ai`, proxies/discord bots « gratuits ».
- Tester les **plugins/GPTs créés par d'autres** : interdit, pas d'autorisation.
- Constats déjà déclarés connus par le brief, ex. : changement de mot de passe n'invalidant pas
  tous les tokens ; suppression de compte sans mot de passe ; ajouter un membre à son org sans
  son accord ; clés API aux permissions larges ; dépasser le cap de clés ; ChatGPT affiche des
  images d'autres domaines (sauf si ça transmet des données sensibles à un tiers sans consentement) ;
  dépassements ponctuels de rate-limit/quota (seul un bypass durable à grande échelle, ordre de
  centaines de requêtes au-delà, peut être récompensé).
- Self-XSS via console, bugs exigeant une coopération invraisemblable de la victime, vieux navigateurs.

## 📜 Règles d'engagement (Safe Harbor = protection légale si on les suit toutes)

1. Tester uniquement les systèmes in-scope, uniquement **ses propres comptes**
   (compte `@bugcrowdninja.com` préféré par OpenAI, non obligatoire).
2. Ne pas violer la vie privée, ne pas perturber les systèmes, ne pas détruire de données.
3. Ne jamais accéder/modifier/utiliser les données d'autrui. Si une faille les expose :
   **stop**, rapport immédiat, suppression de toute copie. Preuve = strict minimum.
4. Tout échange sur une vulnérabilité passe par **Bugcrowd** ; confidentialité jusqu'à
   autorisation écrite d'OpenAI (visée sous 90 jours). Divulgation inconditionnelle : jamais de chantage.
5. Rapporter vite, avec : autorité de départ de l'attaquant, restriction violée, ressource
   protégée, résultat non autorisé concret, produit/version/OS/config, étapes de reproduction,
   et pour ChatGPT l'**ID/URL de conversation** si le bug s'y démontre.
6. Aucun remboursement des achats/upgrades faits pour tester. Rate-limit/blocage IP/compte possible :
   attendre l'expiration ; bannissement → support@bugcrowd.com (nombre limité de déblocages).
7. Safe Harbor ne couvre que les systèmes OpenAI. Les tiers interconnectés restent sous leur propre droit.

## Traduction pratique pour nous

- **Manuels, lents, ciblés** : Chromium + DevTools, un test à la fois, journalisés. Pas de scanner, pas de fuzzing.
- **Deux comptes à nous** (A = « victime », B = « attaquant ») : 95 % de nos tests sont A↔B.
- Toute anomalie → on fige les preuves (heure UTC, URLs, codes HTTP, captures), on arrête ce fil,
  on m'en parle **ici** avec des données sanitisées, je qualifie, puis **tu** soumets sur Bugcrowd.
