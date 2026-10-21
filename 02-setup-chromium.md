# 02 — Setup Chromium (Mission 0, ~30 min)

## 1. Comptes

- [ ] Compte **Bugcrowd** chercheur créé (c'est lui qui sera payé). Récupère ton adresse
      `@bugcrowdninja.com` dans ton profil Bugcrowd : OpenAI **préfère** que les comptes
      de test OpenAI soient créés avec. Note-la hors de ce dépôt.
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
