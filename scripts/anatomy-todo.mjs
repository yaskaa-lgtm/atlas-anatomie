// Liste les termes anatomiques pas encore traduits, pour preparer le prochain lot.
// Usage : node scripts/anatomy-todo.mjs <appareil> [nombre]
//   appareil : cardiac | respiratory | digestive | urinary | lymphatic | endocrine | reproductive
//              skeletal | muscular | arterial | venous | nervous | sensory | connective | integumentary
//   nombre   : taille du lot (40 par defaut)
// Les noms les plus courts sortent en premier : ce sont les structures les plus generales.
import {readFileSync} from 'node:fs';
import {fileURLToPath} from 'node:url';

const read=relative=>JSON.parse(readFileSync(fileURLToPath(new URL(relative,import.meta.url)),'utf8'));
const [system,limitArg]=process.argv.slice(2);
const limit=Number(limitArg??40);
if(!system){console.error('Indiquer un appareil, ex. : node scripts/anatomy-todo.mjs cardiac 40');process.exit(1);}

const atlas=read('../public/models/atlas.json');
const names=read('../locales/anatomy-fr.json');
const partById=new Map(atlas.parts.map(p=>[p.id,p]));
const systemOf=concept=>{
 const tally={};
 for(const id of concept.elements){const s=partById.get(id)?.system;if(s)tally[s]=(tally[s]??0)+1;}
 return Object.entries(tally).sort((a,b)=>b[1]-a[1])[0]?.[0]??'?';
};
const untranslated=v=>!v||v==='TODO';

const concepts=atlas.concepts.filter(c=>systemOf(c)===system&&untranslated(names.concepts[c.id])).sort((a,b)=>a.name.length-b.name.length);
const parts=[...new Set(atlas.parts.filter(p=>p.system===system).map(p=>p.name))].filter(n=>untranslated(names.parts[n.toLowerCase()])).sort((a,b)=>a.length-b.length);

console.log(`${system} : ${concepts.length} concept(s) et ${parts.length} nom(s) de piece a traduire.\n`);
console.log(`--- Prochain lot : ${Math.min(limit,concepts.length)} concept(s) ---`);
for(const c of concepts.slice(0,limit))console.log(`  "${c.id}": "${c.name}"   (${c.elements.length} piece${c.elements.length>1?'s':''})`);
console.log(`\n--- Noms de piece (${parts.length}) ---`);
for(const n of parts)console.log(`  "${n.toLowerCase()}": "${n}"`);
