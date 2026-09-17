# Prochaines étapes

Feuille de route détaillée pour reprendre le projet. **Lire `CLAUDE.md` d'abord** : il contient
les règles de travail de l'utilisateur, l'architecture i18n et l'état du dépôt.

**Rappel des trois règles les plus importantes :**
- Attendre la validation de l'utilisateur avant chaque grosse modification.
- **S'arrêter à la fin de chaque étape** (budget de crédits limité, il reprend en plusieurs sessions).
- Lots de 30 à 50 termes maximum, avec un tableau `anglais | français` à relire après chaque lot.

---

## ÉTAPE 4b — Traduire le vocabulaire anatomique ← PROCHAINE

**C'est le gros chantier restant.** L'interface est traduite à 100 %, mais les **noms de structures**
affichés (titre du panneau de détail, résultats de recherche, liste des pièces incluses) viennent
du fichier de données et sont encore en anglais. L'utilisateur l'a déjà signalé comme gênant.

### 4b.1 — Faire choisir le périmètre à l'utilisateur (À FAIRE EN PREMIER)

5 090 termes uniques à 40 par lot = **~127 lots à relire**. Ne pas se lancer sans son accord.
Lui présenter ces trois options :

| Option | Volume | Commentaire |
|---|---|---|
| **(a) Périmètre ciblé** | ~300 à 500 termes, ~10 lots | Les structures réellement rencontrées en imagerie médicale : os, gros vaisseaux, organes, structures thoraciques et abdominales. Le reste reste en anglais par repli. **Recommandé** : immédiatement utile pour son DTS IMRT. |
| **(b) Tout traduire** | 5 090 termes, ~127 lots | Exhaustif, mais très long et coûteux en crédits. |
| **(c) Par appareil** | variable | Un système complet à la fois (squelette, puis cœur, puis appareil digestif…). Bon compromis si il veut réviser un appareil précis. |

### 4b.2 — Mettre en place le mécanisme (une seule fois)

**Ne jamais modifier `public/models/atlas.json`.** C'est la donnée source sous licence CC BY 4.0,
et la règle de l'utilisateur est que l'anglais reste disponible comme référence.

Créer **`locales/anatomy-fr.json`**, une table de correspondance appliquée à l'affichage :

```json
{
  "concepts": {
    "FMA7197": "foie",
    "FMA3734": "arc de l'aorte"
  },
  "parts": {
    "gingiva of upper jaw": "gencive du maxillaire"
  }
}
```

Deux tables sont nécessaires, car les données ont deux types de noms :

| Source | Clé à utiliser | Volume | Exemple |
|---|---|---|---|
| `concepts[].name` | l'**identifiant FMA** (`concepts[].id`) | 3 432 | `FMA3734` → `arch of aorta` |
| `parts[].name` | le **nom anglais en minuscules** | 1 674 uniques | `gingiva of upper jaw` |

Les `parts` n'ont pas d'identifiant FMA propre (leur `id` est de la forme `FJ1252`), et 2 234 pièces
se partagent 1 674 noms. Utiliser le nom anglais comme clé évite donc les doublons.

Créer ensuite **`lib/anatomy-names.ts`** :

```ts
import {useI18n} from '@/lib/i18n';
import names from '@/locales/anatomy-fr.json';
import type {Concept,Part} from '@/app/anatomy';

/** Renvoie le nom affichable d'une structure : le français s'il existe, sinon l'anglais d'origine. */
export function useAnatomyName(){
 const {locale}=useI18n();
 return {
  concept:(c:Pick<Concept,'id'|'name'>)=>locale==='fr'?(names.concepts[c.id as keyof typeof names.concepts]??c.name):c.name,
  part:(p:Pick<Part,'name'>)=>locale==='fr'?(names.parts[p.name.toLowerCase() as keyof typeof names.parts]??p.name):p.name,
 };
}
```

Le repli terme par terme est automatique : un terme non traduit reste en anglais, rien ne casse.

### 4b.3 — ⚠️ PIÈGE PRINCIPAL : traduire à l'affichage uniquement

`chosen.name` (l'état React) **doit rester le nom anglais**, parce qu'il sert de clé de recherche
dans deux fonctions de `app/anatomy.ts` :

```tsx
explanationKey(chosen.name, selected.system)      // cherche 'heart', 'liver'… dans ORGAN_KEYS
hasOrganExplanation(chosen.name.toLowerCase())    // idem
```

Si on traduit `chosen.name` à la source, les 9 explications d'organes cessent de s'afficher.
**Ne traduire qu'au moment du rendu JSX.**

### 4b.4 — Points à câbler dans `app/page.tsx`

| Emplacement | Code actuel | Action |
|---|---|---|
| Titre du panneau de détail | `<SheetTitle …>{chosen?.name}</SheetTitle>` | traduire à l'affichage |
| Légende sous le corps (mode isolé) | `chosen?.name??t('caption.isolated')` | traduire à l'affichage |
| Liste des pièces incluses | `<span>{p.name}</span>` dans `member-list` | traduire à l'affichage |
| Résultats de recherche | `<span className="search-result-name">{c.name}</span>` | traduire à l'affichage |
| Libellé d'accessibilité du champ | `itemToStringLabel={c=>c.name}` | traduire à l'affichage |
| **Filtre de recherche** | `c.name.toLowerCase().includes(term)||c.id.toLowerCase().includes(term)` | **voir 4b.5** |
| Suggestions par défaut | `['heart','brain','liver',…]` | **ne pas toucher** : ce sont des clés de correspondance avec les données anglaises |

### 4b.5 — Rendre la recherche bilingue

La recherche doit trouver une structure tapée **en français comme en anglais** — l'utilisateur
connaît les deux, et les termes anglais restent affichés pour ce qui n'est pas encore traduit.
Étendre le filtre pour comparer aussi le nom français :

```tsx
atlas.concepts.filter(c=>{
 const french=conceptName(c).toLowerCase();
 return c.name.toLowerCase().includes(term)||french.includes(term)||c.id.toLowerCase().includes(term);
})
```

**Penser aux accents** : « artere » doit trouver « artère ». Normaliser les deux côtés avec
`.normalize('NFD').replace(/\p{Diacritic}/gu,'')` avant la comparaison.

Le tri actuel est `a.name.length-b.name.length` (les noms courts d'abord). Le conserver, mais
trier sur le nom affiché pour que l'ordre reste cohérent en français.

### 4b.6 — Choisir les termes de chaque lot

Créer un script d'aide, par exemple `scripts/anatomy-todo.mjs`, qui liste les termes non encore
traduits **par ordre de priorité**. Bonne heuristique : **les noms les plus courts d'abord**
(`arch of aorta` avant `first anterior ventricular branch of right coronary artery`), car ce sont
les structures les plus générales et les plus utiles. Filtrer aussi par système (`parts[].system`)
pour l'option (c).

### 4b.7 — Étendre le contrôle de couverture

`scripts/translation-coverage.mjs` ne vérifie aujourd'hui que l'interface (123/123).
Y ajouter une section pour le vocabulaire :

```
Interface  : 123/123 clés traduites.
Vocabulaire : 312/5090 termes traduits (6 %).
```

### 4b.8 — Boucle de travail pour chaque lot

1. Prendre 30 à 50 termes non traduits.
2. **Vérifier chaque terme dans la Terminologia Anatomica. Ne jamais inventer.**
   En cas de doute : écrire `"TODO"` comme valeur et le signaler explicitement à l'utilisateur.
3. Ajouter les entrées dans `locales/anatomy-fr.json`.
4. Lancer `npm run check` et `node scripts/validate-atlas.mjs`.
5. **Présenter le tableau `anglais | français`** et signaler :
   - les termes à plusieurs traductions valides selon le contexte ;
   - les `TODO` restants ;
   - les abréviations conservées telles quelles (IRM, TDM, TEP…).
6. **Attendre la relecture de l'utilisateur.**
7. Commit avec un message en français mentionnant le numéro du lot.

### Définition du « terminé » pour l'étape 4b

- `locales/anatomy-fr.json` couvre le périmètre choisi par l'utilisateur.
- Cliquer une structure affiche son nom en français.
- La recherche fonctionne en français **et** en anglais, accents compris.
- `npm run check`, `validate-atlas.mjs`, `validate-interactions.mjs` et `npm run build` passent.
- Aucun `TODO` non signalé à l'utilisateur.

---

## ÉTAPE 5 — Vérification visuelle et liste des TODO

À faire **après** la validation de l'étape 4b.

### 5.1 — Chercher les débordements de texte

Le français est en moyenne **15 à 20 % plus long que l'anglais**. C'est le principal risque
d'affichage. Lancer `npm run dev` et inspecter ces endroits précis :

| Zone | Textes à risque |
|---|---|
| Panneau de gauche | « Appareil respiratoire », « Système lymphatique », « Système endocrinien », « Tissu conjonctif » — la largeur est fixée à 254 px (222 px sous 1000 px de large) dans `app/globals.css` |
| Barre du bas | « Éclater l'anatomie », « Assembler et réinitialiser », « Toutes les pièces » — dock de 460 px de large |
| Panneau de détail | « Afficher l'anatomie environnante » dans le bouton principal ; largeur 310 px (280 px sous 1000 px) |
| Légende sous le corps | « STRUCTURE SÉLECTIONNÉE » — `white-space:nowrap`, donc risque de dépassement |
| Noms anatomiques longs | Les noms français peuvent être très longs (« branche ventriculaire antérieure de l'artère coronaire droite ») dans un titre en 28 px |

### 5.2 — Tester les mises en page mobiles

Le projet cible explicitement trois formats (voir `scripts/validate-interactions.mjs`) :
**390×844**, **320×568** et **844×390** (paysage). Utiliser le mode responsive du navigateur.
Le 320×568 est le plus contraint : c'est là que les textes longs casseront en premier.

### 5.3 — Corriger

Privilégier les ajustements CSS dans `app/globals.css` (taille de police, `text-wrap`, largeur de
panneau) **plutôt que de raccourcir les traductions**. Si un terme anatomique doit absolument être
raccourci, le signaler à l'utilisateur : la justesse du terme prime sur l'esthétique.

### 5.4 — Lister tous les TODO restants

```sh
node scripts/translation-coverage.mjs
grep -rn '"TODO"' locales/
```

Présenter la liste complète à l'utilisateur, groupée par catégorie, en indiquant pour chaque
terme **pourquoi** il est en TODO (terme ambigu, structure rare, absente de la TA…).

---

## ÉTAPE 6 — Documentation (optionnelle)

`README.md` et `public/ATTRIBUTION.md` sont encore en anglais. Ce n'est **pas** de l'interface :
ce sont des fichiers lus sur GitHub par des développeurs. À demander à l'utilisateur :

- Les laisser en anglais (convention sur GitHub, lisibles par tous).
- Les traduire en français (cohérent avec un projet francophone).
- **Les deux** : `README.md` en anglais + `README.fr.md` en français. Le plus courant.

⚠️ **`public/ATTRIBUTION.md` contient l'attribution CC BY 4.0 obligatoire.** Si on le traduit,
conserver les noms de licence et le crédit « The Database Center for Life Science » à l'identique.

---

## ÉTAPE 7 — Publication en ligne

**C'est une action visible de l'extérieur : demander confirmation explicite avant de l'exécuter.**

L'utilisateur a déjà choisi de créer **un dépôt neuf à son nom** (pas un fork). Le remote `origin`
est libre, `upstream` pointe vers le dépôt de l'auteur original. `gh` est connecté au compte
**`yaskaa-lgtm`**.

### 7.1 — Créer le dépôt et envoyer le code

```sh
gh repo create <nom-du-depot> --public --source=. --remote=origin --push
```

Lui faire choisir le nom et si le dépôt doit être public ou privé.

### 7.2 — Déployer

Le projet est **entièrement statique**, donc simple à héberger. `vercel.json` est déjà configuré
(`npm ci`, `npm run build`, dossier de sortie `dist`). Importer le dépôt sur Vercel comme projet
Vite : aucune variable d'environnement, aucune clé d'API nécessaire.

### 7.3 — Avant la mise en ligne, vérifier

- `LICENSE` intact, avec `Copyright (c) 2026 ashemag`.
- Attribution BodyParts3D / CC BY 4.0 visible dans l'app (panneau « À propos ») et dans
  `public/ATTRIBUTION.md`.
- `web/index.html` annonce bien `lang="fr"` et la description française.
- Les ~33 Mo de géométrie 3D se chargent correctement depuis l'hébergeur.
- Éventuellement, regarder les 11 vulnérabilités `npm audit` — toutes dans des outils de
  développement, donc non exposées aux visiteurs. **Ne pas lancer `npm audit fix --force`.**
