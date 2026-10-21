# hack-open-ai — Bug Bounty OpenAI (Bugcrowd), légalement

Programme officiel : https://bugcrowd.com/engagements/openai
Brief lu et résumé le **2026-10-21** (dernière mise à jour affichée : 21 oct. 2026).

## Mode de fonctionnement de notre binôme

- **Toi** : les mains. Ton PC, ton Chromium, tes comptes de test. Tu exécutes les tests
  un par un, exactement comme décrits, et tu me renvoies les résultats.
- **Moi** : la tête. Je priorise les surfaces, je rédige les tests pas à pas,
  j'analyse ce que tu me renvoies (requêtes/réponses sanitisées, captures, codes HTTP),
  je distingue bug réel / comportement attendu / hors-scope, et je rédige le rapport Bugcrowd.
- Je ne teste **pas** OpenAI depuis mon sandbox (accès réseau restreint, et ce n'est pas
  le cadre du programme). Aucun test n'existe tant que tu ne l'as pas exécuté sur **tes** comptes.

## Règle d'or (à relire avant chaque session)

> On ne teste que les cibles in-scope, uniquement avec **nos propres comptes**,
> sans dégrader le service, sans toucher aux données d'autrui. Si un test expose
> des données qui ne sont pas les nôtres : **on s'arrête immédiatement**, on ne
> copie rien de plus que le strict minimum de preuve, on rapporte via Bugcrowd,
> on supprime les copies. Détails : [`00-scope-et-regles.md`](00-scope-et-regles.md).

## Fichiers

| Fichier | Contenu |
|---|---|
| [`00-scope-et-regles.md`](00-scope-et-regles.md) | Scope payé, hors-scope, règles d'engagement, paiements |
| [`01-strategie.md`](01-strategie.md) | Où chercher en priorité avec Chromium seul, et pourquoi |
| [`02-setup-chromium.md`](02-setup-chromium.md) | Comptes A/B, profils Chromium, DevTools, hygiène des secrets |
| [`03-plan-tests-phase1.md`](03-plan-tests-phase1.md) | Tests Phase 1, pas à pas, avec ce que tu dois me renvoyer |
| [`journal.md`](journal.md) | Journal de bord : un test = une ligne datée |
| [`templates/rapport-bugcrowd.md`](templates/rapport-bugcrowd.md) | Gabarit de rapport prêt à soumettre (EN) |
| [`tools/sanitize_har.py`](tools/sanitize_har.py) | Nettoie un export HAR (cookies, Authorization, tokens) avant partage |

## Confidentialité — CRITIQUE

- Ce dépôt peut être visible : **jamais** de cookies, tokens, clés API, HAR non sanitisés,
  ni de détails d'une vulnérabilité non corrigée. Le programme impose la confidentialité
  jusqu'à autorisation d'OpenAI (objectif : 90 jours après rapport).
- Le dossier `preuves-locales/` est dans `.gitignore` : mets-y tes captures brutes
  **en local seulement**. Tu me transmets des versions sanitisées dans le chat.
- Communication vulnérabilité = **Bugcrowd uniquement**. Pas de blog, pas de tweet, pas de GitHub issue.

## Démarrage rapide

1. Lis `00` et `02`, fais la **Mission 0** (setup + inventaire) dans `03`.
2. Renvoie-moi les réponses aux 4 questions à la fin de `02-setup-chromium.md`.
3. On enchaîne test par test, dans l'ordre de `03`.
