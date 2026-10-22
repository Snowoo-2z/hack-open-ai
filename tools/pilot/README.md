# 🕹️ Pilot — « tu pilotes tout », version légale et réaliste

## Le partage des rôles (ce qui est automatisé, ce qui ne le sera pas)

| Qui | Quoi |
|---|---|
| **Moi** | J'écris les **missions** (fichiers JSON tout prêts dans `missions/`) : navigation, attentes, vérifications, captures, journal réseau. Tu n'écris aucun code. |
| **Le script** (sur ton PC) | Il se connecte à **ton** Chrome via le port de debug local, exécute les étapes **une par une**, génère un dossier `resultats/…/` prêt à me renvoyer. |
| **Toi** (le minimum vital) | Installer Python + 1 bibliothèque (une fois), lancer Chrome avec une commande copiée-collée, **te connecter à tes comptes** (mots de passe/codes = jamais dans un script), résoudre un éventuel CAPTCHA **à la main**, valider chaque action avec **Entrée**, me renvoyer les résultats. |

Ce qui restera **toujours manuel**, et pourquoi :

- **Connexions et création de comptes** : automatiser l'authentification = mots de passe en
  clair dans des fichiers + comportement de bot détectable. Non.
- **CAPTCHA** : leur contournement est explicitement hors-scope du programme OpenAI.
- **Scans/fuzzing/brute-force automatisés** : hors-scope aussi, et le brief prévient que
  les scanners automatisés peuvent entraîner rate-limit ou bannissement du compte/IP.
  Ici : rythme humain, une action validée à la fois, uniquement nos deux comptes.
- Je n'ai **aucun accès à distance** à ta machine : le script tourne chez toi, tu peux
  le couper à tout moment (`q` à une étape, ou ferme le terminal / Chrome).

## Installation (une seule fois, ~10 min)

1. **Récupère ce dépôt sur ton PC** : sur GitHub, repo `hack-open-ai` → choisis la branche
   `arena/ee9571b2-hack-open-ai` dans le menu des branches → bouton **Code** → **Download ZIP**
   → dézippe (ou `git clone` si tu as Git). Tu travailleras dans `tools/pilot/`.
2. **Python** :
   - Windows : https://www.python.org/downloads/ → installeur → ⚠️ coche
     **« Add python.exe to PATH »** sur le premier écran. Vérifie dans PowerShell : `py --version`
   - macOS : installeur python.org, ou `brew install python` si tu as Homebrew. Vérifie : `python3 --version`
   - Linux : `sudo apt install python3 python3-pip` (ou équivalent de ta distro).
3. **Playwright** (la bibliothèque qui parle à Chrome — aucun navigateur supplémentaire
   à télécharger, on pilote *ton* Chrome) — dans le dossier `tools/pilot/` :
   - Windows PowerShell : `py -m pip install -r requirements.txt`
   - macOS/Linux : `python3 -m pip install -r requirements.txt`
4. **Test sans navigateur** (vérifie que tout est en place) :
   - Windows : `py pilot.py missions\exemple-verif-connexion.json --validate-only`
   - macOS/Linux : `python3 pilot.py missions/exemple-verif-connexion.json --validate-only`
   → doit répondre « Mission valide … ».

## Lancer Chrome « pilotable » (à chaque session de test)

Profils **dédiés et jetables** — jamais ton profil Chrome perso. Deux fenêtres possibles en
même temps : **A = port 9222**, **B = port 9223**.

**Windows (PowerShell)** — compte A :
```powershell
& "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --remote-debugging-address=127.0.0.1 --user-data-dir="$env:USERPROFILE\oai-pilot\A" https://chatgpt.com
```
Compte B : même commande avec `9223` et `\oai-pilot\B`.

**macOS (Terminal)** — compte A :
```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --remote-debugging-port=9222 --remote-debugging-address=127.0.0.1 --user-data-dir="$HOME/oai-pilot/A" https://chatgpt.com
```
Compte B : port `9223`, dossier `B`.

**Linux (terminal)** — compte A (`google-chrome`, ou `chromium` selon ton install) :
```bash
google-chrome --remote-debugging-port=9222 --remote-debugging-address=127.0.0.1 --user-data-dir="$HOME/oai-pilot/A" https://chatgpt.com
```

> 🔐 **Sécurité du port de debug** : tant que ce Chrome est ouvert, tout programme *local*
> peut le piloter. C'est pour ça : adresse `127.0.0.1` uniquement, profil de test dédié
> (dossier `oai-pilot`), aucun compte perso dedans, et on **ferme** ces fenêtres à la fin
> de la session. Ne lance jamais une commande venue d'ailleurs que ce dépôt sans me la montrer.

Ensuite, dans chaque fenêtre : connecte-toi **manuellement** (A : `snwdc@bugcrowdninja.com`,
B : `snwdc+b@bugcrowdninja.com`). Au premier lancement, crée les comptes OpenAI comme
décrit dans `../../02-setup-chromium.md` — le profil piloté remplace les profils colorés.

## Exécuter une mission

Dans `tools/pilot/`, fenêtre du bon compte déjà ouverte et connectée :

- Windows : `py pilot.py missions\exemple-verif-connexion.json`
- macOS/Linux : `python3 pilot.py missions/exemple-verif-connexion.json`

À chaque étape, le script affiche ce qu'il va faire : **Entrée** = exécuter, **`q`** = arrêter.
(`--yes` enchaîne les étapes en lecture seule sans demander ; les clics restent toujours confirmés.)

Résultats dans `resultats/<date>-<mission>/` (dossier ignoré par Git) :

- `resultat.md` : le déroulé horodaté — **c'est ce que tu me renvoies en premier** ;
- `texte-*.txt` : texte visible des pages, **déjà sanitisé** (emails/jetons masqués) ;
- `reseau.txt` : méthode + code HTTP + chemin, **sans paramètres d'URL** ;
- `*.png` : captures — ⚠️ **non modifiées** : regarde-les, masque email/avatar si visibles, puis envoie.

## Première mission réelle : T-01

1. Compte A (à la main, 1 fois) : crée la conversation contenant `MARQUEUR-A-001`
   (message exact dans `../../03-plan-tests-phase1.md`), **sans la partager**,
   copie son URL dans tes notes locales.
2. Ouvre `missions/t01-partie-B.json` dans un éditeur de texte et remplace
   `__REMPLACE_PAR_L_ID_DE_TA_CONVERSATION_A__` par l'ID de ton URL.
   ⚠️ Ce fichier modifié reste **chez toi**, ne le commite jamais.
3. Chrome **B** lancé (port 9223) et connecté, puis :
   `python3 pilot.py missions/t01-partie-B.json` (ou `py pilot.py missions\t01-partie-B.json`)
4. Renvoie-moi `resultat.md` + `texte-page-B.txt` + la capture relue.
   ✅ Sain attendu : `MARQUEUR-A-001 : ABSENT`. 🚩 `TROUVE` = on arrête tout et on en parle.
