# 02 — Setup navigateur (Mission 0, ~30 min)

## 0. Installer le navigateur — et clarifier qui contrôle quoi

**Qui contrôle quoi (important)** : je n'ai **aucun** accès à ton PC et je ne peux ni voir
ton écran, ni piloter ton navigateur à distance. Mon environnement est séparé du tien.
Concrètement : je t'écris les clics/scripts ici, **tu** les exécutes chez toi, tu me renvoies
les résultats (texte/captures sanitisées). Tu restes aux commandes à 100 % — c'est aussi ce
qu'exige le programme (tests depuis tes comptes, ton IP).

**Oui, Chromium/Chrome sont scriptables** (protocole DevTools, Puppeteer/Playwright) — mais
sur la cible OpenAI, on restera **manuels** : le brief écarte fuzzing/scanners automatisés et
le contournement de CAPTCHA, et l'automatisation peut déclencher rate-limit/bannissement.
Les seuls scripts qu'on utilisera seront des utilitaires *locaux* que tu lances toi-même
(ex. `tools/sanitize_har.py`), lisibles dans ce dépôt avant exécution.

**Quel navigateur installer ?** N'importe quel navigateur à base Chromium **à jour** avec
profils + DevTools convient. Recommandation, du plus simple au plus « pur » :

1. **Google Chrome (recommandé pour débuter)** — https://www.google.com/chrome —
   installeur officiel, **mises à jour de sécurité automatiques**, profils et DevTools
   identiques à Chromium. La page officielle Chromium elle-même conseille les builds
   Chrome pour la plupart des usages, car ils s'auto-mettent à jour.
2. **Chromium officiel** — https://download-chromium.appspot.com (lien « point and click »
   de https://www.chromium.org/getting-involved/download-chromium/) : télécharge un ZIP,
   dézippe, lance l'exécutable (`chrome.exe` sous Windows, app Chromium sous macOS).
   ⚠️ Builds « best-effort », **aucune mise à jour automatique** : à re-télécharger soi-même
   régulièrement. Sous **Linux**, préfère ton gestionnaire de paquets
   (Debian/Ubuntu : `sudo apt install chromium` ; Fedora : `sudo dnf install chromium` ;
   Arch : `sudo pacman -S chromium`).
3. Déjà installé chez toi ? **Brave** ou **Edge** (base Chromium) font aussi l'affaire
   pour la Phase 1 — dis-moi simplement lequel tu as.

🚫 **Jamais** de sites de téléchargement tiers (« chromium gratuit », installeurs repackés) :
risque de malware. Uniquement les sources officielles ci-dessus ou les paquets de ton OS.

Vérification après install : ouvre le navigateur, tape `chrome://version` dans la barre
d'adresse (`chromium://version` sous Chromium pur) et note la première ligne pour ton retour.

## 1. Comptes

- [ ] Compte **Bugcrowd** chercheur créé (c'est lui qui sera payé).
      **Adresse `@bugcrowdninja.com` : rien à créer.** C'est un alias automatique
      `<ton_pseudo_bugcrowd>@bugcrowdninja.com` qui transfère vers l'email principal
      de ton compte Bugcrowd (généré à la 1ʳᵉ connexion, jusqu'à ~10 min d'attente).
      Ton pseudo se lit dans l'URL de ton profil : `bugcrowd.com/h/<pseudo>`.
      Astuce 2 comptes : `pseudo+a@bugcrowdninja.com` et `pseudo+b@bugcrowdninja.com`
      arrivent dans la même boîte. OpenAI *préfère* cet alias mais le brief dit
      explicitement qu'il n'est **pas obligatoire** — un compte perso convient aussi.
      Doc : https://docs.bugcrowd.com/researchers/participating-in-program/your-bugcrowdninja-email-address/
- [ ] Compte OpenAI **A** (« victime ») — idéalement l'adresse bugcrowdninja.
- [ ] Compte OpenAI **B** (« attaquant ») — une seconde adresse **à toi**
      (alias `+b` accepté par ton fournisseur, ou autre boîte que tu contrôles).
- [ ] N'achète **rien** pour l'instant (ni Plus, ni crédits API) : le programme ne rembourse pas.
      On décidera ensemble si une surface payante vaut le coup, preuves à l'appui.

## 2. Deux profils Chromium séparés (indispensable)

Chromium → avatar profil → « Ajouter » :

- Profil **`OAI-A`** : connecté au compte A sur chatgpt.com et platform.openai.com.
- Profil **`OAI-B`** : connecté au compte B, mêmes sites.
- Profil perso : **jamais** utilisé pour les tests (évite tout mélange de sessions/preuves).

Astuce : couleur de thème différente par profil (ex. A = bleu, B = rouge) pour ne jamais
confondre « qui suis-je » sur une capture d'écran.

## 3. DevTools — les 4 gestes que tu utiliseras partout

1. **F12 → onglet Network** : coche `Preserve log`, filtre `Fetch/XHR`.
2. Clic droit sur une requête → **Copy → Copy as fetch** (ou « Copy as cURL ») : c'est ce que
   tu me renverras, **après sanitisation** (voir §4).
3. Clic droit dans la liste Network → **Save all as HAR with content** : archive locale brute
   (dossier `preuves-locales/`, jamais commitée), puis version nettoyée via l'outil ci-dessous.
4. **Console** : uniquement pour *lire* des erreurs. On n'y colle aucun code trouvé sur internet
   (self-XSS = hors-scope et dangereux pour ton compte). Si un test exige du JS, je te le fournirai
   ici, ligne par ligne, en expliquant chaque ligne.

Optionnel plus tard (Phase 2, seulement si tu veux) : Burp Suite Community (gratuit) comme
proxy d'interception entre Chromium et les sites **in-scope**, en mode manuel, sans scanner.

## 4. Hygiène des secrets — NON négociable

- Ne me renvoie **jamais** en clair : cookies, en-têtes `Authorization`, tokens de session,
  clés API `sk-…`, mots de passe, codes 2FA. Remplace par `REDACTED` en gardant la structure.
- Pour un HAR : `python3 tools/sanitize_har.py brut.har propre.har` puis joins `propre.har`
  (l'outil supprime cookies/authorization et masque les motifs de clés/tokens évidents ;
  relis quand même avant envoi).
- Captures d'écran : masque email/avatar/identifiants personnels. Les **IDs d'objets de test**
  (conversation, fichier…) peuvent rester : ce sont des preuves, pas des secrets.
- Rien de tout ça sur GitHub : seuls les documents de méthode vivent dans le dépôt.

## 5. Ce que chaque retour de ta part doit contenir

```
Test : T-xx  |  Date/heure (UTC) : …  |  Compte : A ou B (profil Chromium)
URL de la page : …
Action faite : …
Résultat observé : … (code HTTP si requête, message affiché, capture masquée)
Attendu sain : … (je le donne dans la fiche de test)
Écart ? : oui/non — si oui, décris sans aller plus loin, on s'arrête là.
```

## 6. Les 4 questions auxquelles répondre avec ton premier retour

1. **Comptes** : Bugcrowd OK ? Adresse bugcrowdninja récupérée ? Comptes OpenAI A/B créés ?
   As-tu déjà un abonnement Plus et/ou un accès API Platform (organisation, crédits) ? (oui/non suffit)
2. **Machine** : OS (Windows/macOS/Linux + version) ? Chromium version (menu ⋮ → Aide → À propos) ?
   Python installé (pour `sanitize_har.py`) ? Burp Suite déjà installé/accepté ou DevTools uniquement ?
3. **Aisance** : DevTools Network, copier une requête, exporter un HAR — déjà fait / jamais fait ?
   (Aucune mauvaise réponse : ça règle le niveau de détail de mes fiches de test.)
4. **Piste de départ préférée** : (a) ChatGPT web A↔B [recommandé], (b) Platform/API si tu as
   l'accès, (c) Codex desktop + extension Chrome, (d) recon passive sous-domaines en parallèle.
