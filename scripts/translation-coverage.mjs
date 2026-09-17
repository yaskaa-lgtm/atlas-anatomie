// Etat de la traduction francaise.
//   1. Interface : compare locales/en.json (reference) et locales/fr.json, liste les cles manquantes.
//   2. Vocabulaire : compare public/models/atlas.json et locales/anatomy-fr.json, par appareil.
// Usage : node scripts/translation-coverage.mjs
import {readFileSync} from 'node:fs';
import {fileURLToPath} from 'node:url';

const read=relative=>JSON.parse(readFileSync(fileURLToPath(new URL(relative,import.meta.url)),'utf8'));

// ---------- 1. Interface ----------
const isPlural=value=>value&&typeof value==='object'&&'one' in value&&'other' in value;
const flatten=(node,prefix='')=>Object.entries(node).flatMap(([key,value])=>{
 const path=prefix?`${prefix}.${key}`:key;
 return value&&typeof value==='object'&&!isPlural(value)?flatten(value,path):[path];
});
const reference=flatten(read('../locales/en.json'));
const translated=new Set(flatten(read('../locales/fr.json')));
const missing=reference.filter(key=>!translated.has(key));
console.log(`Interface : ${reference.length-missing.length}/${reference.length} cles traduites.`);
for(const key of missing)console.log(`  TODO  ${key}`);

// ---------- 2. Vocabulaire anatomique ----------
const atlas=read('../public/models/atlas.json');
const names=read('../locales/anatomy-fr.json');
const partById=new Map(atlas.parts.map(p=>[p.id,p]));
/** Appareil d'un concept = appareil majoritaire de ses pieces. */
export const systemOf=concept=>{
 const tally={};
 for(const id of concept.elements){const s=partById.get(id)?.system;if(s)tally[s]=(tally[s]??0)+1;}
 return Object.entries(tally).sort((a,b)=>b[1]-a[1])[0]?.[0]??'?';
};
const SYSTEM_ORDER=['cardiac','respiratory','digestive','urinary','lymphatic','endocrine','reproductive','skeletal','muscular','arterial','venous','nervous','sensory','connective','integumentary'];
const rows=SYSTEM_ORDER.map(system=>{
 const concepts=atlas.concepts.filter(c=>systemOf(c)===system);
 const parts=[...new Set(atlas.parts.filter(p=>p.system===system).map(p=>p.name.toLowerCase()))];
 const doneC=concepts.filter(c=>names.concepts[c.id]&&names.concepts[c.id]!=='TODO').length;
 const doneP=parts.filter(n=>names.parts[n]&&names.parts[n]!=='TODO').length;
 return {system,total:concepts.length+parts.length,done:doneC+doneP};
});
const total=rows.reduce((n,r)=>n+r.total,0),done=rows.reduce((n,r)=>n+r.done,0);
console.log(`\nVocabulaire : ${done}/${total} entrees traduites (${Math.round(done/total*100)} %).`);
for(const r of rows){
 const mark=r.done===r.total?'✓':r.done?'…':' ';
 console.log(`  ${mark} ${r.system.padEnd(14)} ${String(r.done).padStart(5)} / ${String(r.total).padEnd(5)}`);
}
const todos=[...Object.entries(names.concepts),...Object.entries(names.parts)].filter(([,v])=>v==='TODO').map(([k])=>k);
if(todos.length){console.log(`\n${todos.length} terme(s) marques TODO dans anatomy-fr.json :`);todos.forEach(k=>console.log(`  TODO  ${k}`));}
