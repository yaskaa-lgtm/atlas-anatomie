# Générateur de vocabulaire anatomique

Outils Python (sans dépendance) qui ont produit la majorité de `locales/anatomy-fr.json`
à partir des noms anglais de `public/models/atlas.json`, par règles : dictionnaire de base
(Terminologia Anatomica), accords de genre et de nombre, ordinaux, « de la / du / de l' »,
côté gauche/droit, unités composées (« circonflexe humérale », « segmentaire basale »).

| Fichier | Rôle |
|---|---|
| `skel.py` | Dictionnaire et règles du squelette (os, dents, phalanges, disques…). |
| `gen.py` | Étend `skel.py` : adjectifs accordés, vaisseaux, nerfs, muscles. |
| `add.py` | Ajoute un lot à `anatomy-fr.json`, déduit les noms de pièces homonymes, committe. |

```sh
# Voir ce que les règles produiraient pour un appareil (rien n'est écrit) :
python3 scripts/generateur-vocabulaire/gen.py arterial > /tmp/out.json 2> /tmp/relecture.txt

# Intégrer un lot (JSON {"concepts": {"FMA…": "…"}, "parts": {...}}) :
python3 scripts/generateur-vocabulaire/add.py "Vocabulaire lot N : …" < lot.json
```

Les deux scripts ne traduisent que les concepts **pas encore présents** dans `anatomy-fr.json`.
Pour corriger un choix global (ex. « atrium » → « oreillette »), il est plus simple de faire un
remplacement dans le JSON puis `node scripts/anatomy-review.mjs`.
