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

**Le plus simple sous Windows : double-clique `GO.bat`** (dans `tools/pilot/`).
Menu numéroté : lancer Chrome A/B, lancer chaque mission, `git pull` — aucune commande
à retaper. À la fin d'une mission, **le dossier des résultats s'ouvre tout seul** dans
l'Explorateur, avec le fichier `A-MENVOYER.md` sélectionné.

En ligne de commande, dans `tools/pilot/`, fenêtre du bon compte déjà ouverte et connectée :

- Windows : `py pilot.py missions\exemple-verif-connexion.json`
- macOS/Linux : `python3 pilot.py missions/exemple-verif-connexion.json`

À chaque étape, le script affiche ce qu'il va faire : **Entrée** = exécuter, **`q`** = arrêter.
(`--yes` enchaîne les étapes en lecture seule sans demander ; les clics restent toujours confirmés.)

Résultats dans `resultats/<date>-<mission>/` (dossier ignoré par Git) :

- **`A-MENVOYER.md` : le fichier unique à me renvoyer** (déroulé + textes sanitisés +
  journal réseau filtré). Une copie est aussi écrite à chemin fixe :
  `resultats/DERNIER-A-MENVOYER.md` — toujours au même endroit, rien à chercher ;
- `resultat.md`, `texte-*.txt`, `reseau.txt` : les pièces séparées (secours/détail).
  Le réseau est **filtré** (API métier + erreurs, sans paramètres d'URL) : fini le bruit CDN ;
- `*.png` : captures — ⚠️ **non modifiées** : regarde-les, masque email/avatar si visibles, puis envoie.

## Première mission réelle : T-01 (zéro copier-coller d'URL)

L'URL de la conversation de A transite toute seule vers la mission B, via un fichier
local `cibles-locales/conversation-A.txt` (ignoré par Git, ne quitte jamais ton PC).

1. `GO.bat` → **1** (Chrome A) : connecte-toi compte A si besoin.
2. `GO.bat` → **4** (T-01 partie A) : à la pause, crée la conversation
   `MARQUEUR-A-001` à la main (20 s, message indiqué par la mission), **sans la partager**,
   laisse-la affichée, Entrée. Le script vérifie le marqueur, sauvegarde l'URL, capture.
3. `GO.bat` → **2** (Chrome B) : connecte-toi compte B.
4. `GO.bat` → **5** (T-01 partie B) : le script ouvre l'URL sauvegardée et vérifie.
5. Envoie-moi les deux `A-MENVOYER.md` (celui de A, puis celui de B) + les captures relues.
   ✅ Sain attendu chez B : `MARQUEUR-A-001 : ABSENT`. 🚩 `TROUVE` = on arrête tout et on en parle.
