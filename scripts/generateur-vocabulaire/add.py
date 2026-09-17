#!/usr/bin/env python3
"""Ajoute un lot a locales/anatomy-fr.json et committe.
Usage : python3 add.py "message de commit" < lot.json
lot.json : {"concepts": {"FMA…": "…"}, "parts": {"nom anglais": "…"}}   (parts optionnel)
Les pieces dont le nom anglais coincide avec un concept traduit sont deduites automatiquement.
"""
import json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
P=ROOT/'locales/anatomy-fr.json'
msg=sys.argv[1]
lot=json.load(sys.stdin)
atlas=json.loads((ROOT/'public/models/atlas.json').read_text())
cname={c['id']:c['name'].lower() for c in atlas['concepts']}
partnames={pp['name'].lower() for pp in atlas['parts']}
d=json.loads(P.read_text())
concepts=lot.get('concepts',{}); explicit=lot.get('parts',{})
for k in concepts: assert k in cname, f"id inconnu {k}"; assert k not in d['concepts'], f"deja traduit {k}"
for k in explicit: assert k in partnames, f"piece inconnue {k}"; assert k not in d['parts'], f"deja traduite {k}"
derived={cname[k]:v for k,v in concepts.items() if cname[k] in partnames and cname[k] not in d['parts'] and cname[k] not in explicit}
d['concepts'].update(concepts); d['parts'].update(derived); d['parts'].update(explicit)
P.write_text(json.dumps(d,ensure_ascii=False,indent=2)+"\n")
subprocess.run(['git','-C',str(ROOT),'add','-A'],check=True)
subprocess.run(['git','-C',str(ROOT),'commit','-q','-m',msg+"\n\nCo-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>"],check=True)
todo=sum(1 for v in list(concepts.values())+list(explicit.values()) if v=='TODO')
print(f"OK : {len(concepts)} concepts + {len(derived)+len(explicit)} pieces ({len(derived)} deduites), {todo} TODO — {msg[:60]}")
