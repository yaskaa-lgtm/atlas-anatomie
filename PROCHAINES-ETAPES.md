# Prochaines étapes

Feuille de route détaillée pour reprendre le projet. **Lire `CLAUDE.md` d'abord** : il contient
les règles de travail de l'utilisateur, l'architecture i18n et l'état du dépôt.

**Rappel des trois règles les plus importantes :**
- Attendre la validation de l'utilisateur avant chaque grosse modification.
- **S'arrêter à la fin de chaque étape** (budget de crédits limité, il reprend en plusieurs sessions).
- Lots de 30 à 50 termes maximum, avec un tableau `anglais | français` à relire après chaque lot.

---

## ÉTAPE 4b — Traduire le vocabulaire anatomique ← ✅ TERMINÉE

5 088 / 5 091 termes traduits (100 %), 76 lots, 15 appareils. L'utilisateur a finalement demandé
de **tout traduire** (« tu peux tout continuer y compris squelette »). Détails dans `CLAUDE.md`,
tableau complet dans `TRADUCTIONS-VOCABULAIRE.md`, outils dans `scripts/generateur-vocabulaire/`.

**3 TODO restants** (affichés en anglais) : `FMA9348` subaortic curtain of left ventricle,
`FMA9551` / `FMA9550` outflow part of left / right atrium. À trancher avec l'utilisateur ou un enseignant.

---

## ÉTAPE 5 — Vérification visuelle et liste des TODO ← PROCHAINE

L'étape 4b est terminée : celle-ci peut commencer.

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
