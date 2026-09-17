# Human Atlas — traduction française

> **Feuille de route détaillée : [`PROCHAINES-ETAPES.md`](PROCHAINES-ETAPES.md)**
> Ce fichier-ci décrit l'**état** du projet et les règles de travail.
> `PROCHAINES-ETAPES.md` décrit **ce qu'il reste à faire**, étape par étape, avec le mécanisme
> à mettre en place, les pièges et les points à câbler. Lire les deux avant de commencer.

## Contexte du projet

Application web d'anatomie 3D **clonée depuis `github.com/ashemag/human-atlas`** (licence MIT),
en cours de traduction intégrale en français. L'objectif final est une publication en ligne.

**L'utilisateur** : Yani, étudiant en imagerie médicale (DTS IMRT), **débutant en développement**,
sur Mac. Il n'est pas l'auteur du code original.

### Règles de travail imposées par l'utilisateur — à respecter strictement

1. **Expliquer chaque étape dans un langage accessible à un débutant.** Pas de jargon non défini.
2. **Attendre sa validation avant toute grosse modification.** Ne jamais enchaîner deux étapes sans accord.
3. **S'arrêter à la fin de chaque étape.** Il a un budget de crédits limité et reprend en plusieurs sessions.
4. **Traduire par lots de 30 à 50 termes maximum**, puis présenter un tableau
   `terme anglais | traduction française` qu'il relit avant le lot suivant.
5. **Nomenclature anatomique française officielle (Terminologia Anatomica).**
   **Ne jamais inventer un terme** : en cas de doute, marquer `TODO` et le signaler, pas deviner.
6. **Signaler les termes à plusieurs traductions valides** selon le contexte.
7. **Garder les abréviations médicales internationales** telles quelles (IRM, TDM, TEP…)
   et signaler celles dont on n'est pas sûr.
8. **Commit Git après chaque étape validée**, message clair **en français**.
9. En cas d'hésitation entre deux approches : **demander**, ne pas choisir seul.
10. Répondre **en français**.

## Techno

React 19 + TypeScript, Three.js (rendu 3D), Vite 8, Tailwind CSS 4, composants shadcn/ui.
Site **entièrement statique**, aucun backend. Node.js v24 installé (le projet exige ≥ 22.13).

```sh
npm ci      # une seule fois : installer les dépendances
npm run dev # lancer l'app -> http://localhost:3016  (Ctrl+C pour arrêter)
```

### Vérifications à relancer après chaque lot de traduction

```sh
npm run check                            # TypeScript
node scripts/translation-coverage.mjs    # clés d'interface non traduites (les TODO)
node scripts/validate-atlas.mjs          # intégrité des 2 234 maillages / 3 432 concepts
node scripts/validate-interactions.mjs   # recherche, sélection, tactile, mises en page
npm run build                            # build de production
```

## Licences — ne pas les casser

- **Code** : MIT, `Copyright (c) 2026 ashemag`. Modification et republication autorisées.
  **Conserver le fichier `LICENSE` tel quel**, nom de l'auteur inclus.
- **Données anatomiques** : **BodyParts3D 4.0, CC BY 4.0** (Database Center for Life Science).
  **L'attribution doit rester visible** : voir `public/ATTRIBUTION.md` et la clé `about.attribution`
  dans les fichiers de langue. Elle peut être traduite, pas supprimée.

## Git

- `upstream` → `https://github.com/ashemag/human-atlas` (le dépôt de l'auteur original, lecture seule).
- **`origin` est libre.** L'utilisateur a choisi de créer **un dépôt neuf à lui** (pas un fork)
  le jour de la publication.
- `gh` CLI installé et connecté au compte **`yaskaa-lgtm`**. Demander confirmation avant de créer
  un dépôt public : c'est une action visible de l'extérieur.
- Commits locaux signés `yaskaa`.

## Architecture i18n — comment ça marche

Solution **maison, sans dépendance externe** (choix explicite de l'utilisateur, pour garder un code
lisible et ne pas ajouter de paquets à maintenir).

| Fichier | Rôle |
|---|---|
| `locales/en.json` | **Référence anglaise.** Le texte original y est conservé intact. Ne jamais le supprimer. |
| `locales/fr.json` | Traductions françaises. |
| `lib/i18n.tsx` | Moteur : contexte React, repli, formatage des nombres, pluriels. |
| `components/language-switch.tsx` | Sélecteur `FR / EN` (barre du haut). |
| `scripts/translation-coverage.mjs` | Compare en/fr et liste les clés manquantes. |

**Règle fondamentale : ne jamais écrire de texte en dur dans le code.** Toujours extraire vers
`locales/en.json` (anglais d'origine) **et** `locales/fr.json` (traduction).

### Utilisation

```tsx
const {t,n}=useI18n();
t('systems.title')                          // texte simple
t('systems.visible',{count:visibleCount})   // avec variable + pluriel + nombre formaté
n(1234)                                     // nombre seul -> "1 234" en fr, "1,234" en en
t(`systems.names.${s.id}`)                  // clé dynamique (typée)
```

### Quatre comportements à connaître

1. **Repli automatique** : clé absente de `fr.json` → l'anglais de `en.json` s'affiche.
   Jamais de blanc. C'est ce qui rend la traduction par lots sans risque.
2. **Clés typées** : `MessageKey` est dérivé de `en.json`. Une faute de frappe = erreur TypeScript.
   Donc **toute nouvelle clé doit d'abord exister dans `en.json`**.
3. **Pluriels** : entrée objet `{"one":"…","other":"…"}`, choisie via `{count}`.
   En français 0 et 1 prennent le singulier ; en anglais seul 1.
4. **Erreurs stockées en clé**, pas en texte (`useState<MessageKey|null>`), pour qu'elles suivent
   la langue active. `scene.tsx` reçoit donc des clés via `onError`.

### Pièges dans `app/scene.tsx`

- Accède aux traductions via **`translate.current(...)` (une `useRef`)** et non `t(...)`, pour que
  changer de langue **ne reconstruise pas la scène 3D** (le `useEffect` dépend de `[atlas]`).
  Le libellé d'accessibilité du canevas est mis à jour par un `useEffect` séparé sur `[t]`.
- Le fichier utilise déjà des variables locales nommées `t` pour ses calculs 3D. Ne pas les confondre.

### Piège dans `app/anatomy.ts`

`SYSTEMS` ne contient plus que `id` et `color`. **L'ordre du tableau est significatif** :
`scene.tsx` s'en sert (`findIndex`) pour calculer les angles d'éclatement des pièces.
Ne jamais le réordonner. Les noms/descriptions sont dans `systems.names.*` / `systems.descriptions.*`.

`ORGAN_KEYS` contient les noms **anglais** de 9 organes. Ce sont des clés de correspondance avec
les données de `atlas.json` : **ne pas les traduire**. Même chose pour la liste des suggestions de
recherche par défaut dans `page.tsx` (`['heart','brain','liver',…]`).

## Avancement

| Étape | État |
|---|---|
| 1 — Analyse du projet | ✅ terminée |
| 2 — Lancement en local | ✅ terminée, app fonctionnelle |
| 3 — Structure i18n + sélecteur de langue | ✅ terminée et validée (commit `031db5b`) |
| 4a — Traduction de l'interface | ✅ **terminée, 123/123 clés** (commit `1ce7106`) |
| 4b — Traduction du vocabulaire anatomique | ⬜ **PROCHAINE ÉTAPE — non commencée** |
| 5 — Vérification visuelle et liste des TODO | ⬜ à faire |

## PROCHAINE ÉTAPE : le vocabulaire anatomique

> **Le plan d'exécution complet est dans [`PROCHAINES-ETAPES.md`](PROCHAINES-ETAPES.md), section
> « ÉTAPE 4b »** : mécanisme à créer, pièges, points à câbler dans `page.tsx`, recherche bilingue,
> boucle de travail par lot. Ce qui suit n'en est que le résumé.

C'est le gros chantier restant, et le point de friction principal pour l'utilisateur : il a déjà
signalé que cliquer sur une structure ou la chercher affichait encore de l'anglais.
**L'interface est maintenant traduite, mais les noms anatomiques eux-mêmes ne le sont pas.**

### Où se trouve le vocabulaire

`public/models/atlas.json` (1,3 Mo) — **ne pas modifier ce fichier** : c'est la donnée source
sous CC BY 4.0, et l'anglais doit rester disponible comme référence.

- **3 432 noms de concepts** (`concepts[].name`) — ce que la recherche affiche.
  Ex. `arch of aorta`, `anterior ventricular branch of right coronary artery`
- **1 674 noms de maillages uniques** (`parts[].name`) — les pièces individuelles.
  Ex. `Gingiva of upper jaw`
- **5 090 termes uniques au total**, ~13 259 mots.

Chaque concept porte un **identifiant FMA** (`FMA3710`…), de la *Foundational Model of Anatomy*.
Précieux : il identifie chaque structure sans ambiguïté, ce qui évite de confondre deux termes
voisins et permet de retrouver la traduction officielle.

### Mécanisme recommandé (à valider avec l'utilisateur avant de coder)

Créer `locales/anatomy-fr.json` : une correspondance **identifiant FMA → nom français**, appliquée
au chargement des données. Avantages : `atlas.json` reste intact (respect de la licence et de la
règle « l'anglais reste la référence »), le repli vers l'anglais fonctionne terme par terme, et on
peut s'arrêter à n'importe quel lot.

```json
{ "FMA3734": "arc de l'aorte", "FMA7197": "foie" }
```

Points à câbler : le titre du panneau de détail (`chosen?.name`), la liste `member-list`
(`p.name`), les résultats de recherche (`c.name`), et **la recherche elle-même** — il faudra
qu'elle trouve une structure tapée en français *et* en anglais.

### Décision à prendre avec l'utilisateur

5 090 termes à 40 par lot = **~127 lots à relire**. Lui proposer explicitement le choix :

- **(a) Périmètre ciblé d'abord** : les ~300 à 500 structures réellement rencontrées en imagerie
  médicale (os, gros vaisseaux, organes, structures thoraciques et abdominales). Le reste reste en
  anglais par repli. ~10 lots. **Recommandé** : utile immédiatement pour ses études.
- **(b) Tout traduire** : exhaustif mais très long.
- **(c) Par appareil/système** : un système complet à la fois (squelette, puis cœur, etc.).

## Terminologie — décisions déjà prises

Ces choix ont été présentés à l'utilisateur avec le lot des 15 systèmes, qu'il a validé
(« c'est bien »). Il n'a toutefois **pas répondu terme par terme** aux points signalés
ci-dessous : les reconfirmer s'ils reviennent dans un lot.

| Anglais | Retenu | Alternative valable |
|---|---|---|
| Respiratory / Digestive / Urinary | **Appareil** respiratoire / digestif / urinaire | « Système … » (calque de l'anglais, très répandu) |
| Reproductive | **Appareil génital** (TA : *systema genitale*) | « Appareil reproducteur » (plus scolaire) |
| Body surface | **Surface du corps** (traduction littérale voulue par l'auteur original) | « Téguments », « Système tégumentaire » (plus exacts anatomiquement) |
| brain | **encéphale** (TA : *encephalon*) | « cerveau » (courant, mais désigne stricto sensu une partie) |
| spinal cord | **moelle spinale** (TA) | « moelle épinière » (usage courant) |
| lymph nodes | **nœuds lymphatiques** (TA) | « ganglions lymphatiques » (usage clinique) |
| upper left abdomen | **hypochondre gauche** | |
| ADULT HUMAN · MALE | **HOMME ADULTE** | « ADULTE DE SEXE MASCULIN » (plus littéral, mais long) |

**« Human Atlas » reste en anglais** : c'est le nom du produit, et l'utilisateur l'avait
volontairement restauré (commit `1c38bf3`).

## À vérifier visuellement (étape 5)

Le français est en moyenne 15 à 20 % plus long que l'anglais. Surveiller les débordements :
noms de systèmes dans le panneau de gauche (« Appareil respiratoire » vs « Respiratory »),
boutons de la barre du bas, et les mises en page mobiles (le projet cible 390×844, 320×568
et 844×390 — voir `validate-interactions.mjs`).

## Dette technique connue, non bloquante

- `npm audit` signale 11 vulnérabilités (8 hautes), toutes dans des outils de **développement**.
  L'app ne traite aucune donnée utilisateur. **Ne pas lancer `npm audit fix --force`** :
  cela installerait des versions majeures différentes et casserait très probablement l'app.
- Le build avertit que le bundle JS dépasse 500 ko (930 ko / 269 ko gzip). Sans conséquence
  fonctionnelle ; à traiter éventuellement avant la mise en ligne.
- `README.md` et `public/ATTRIBUTION.md` sont encore en anglais (documentation, pas interface).
