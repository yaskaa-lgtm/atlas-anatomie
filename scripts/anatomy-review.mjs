// Genere TRADUCTIONS-VOCABULAIRE.md : tous les noms anatomiques traduits, par appareil,
// en tableau « anglais | francais » pour relecture. Les TODO et les termes non traduits sont signales.
// Usage : node scripts/anatomy-review.mjs
import {readFileSync,writeFileSync} from 'node:fs';
import {fileURLToPath} from 'node:url';

const read=relative=>JSON.parse(readFileSync(fileURLToPath(new URL(relative,import.meta.url)),'utf8'));
const atlas=read('../public/models/atlas.json');
const names=read('../locales/anatomy-fr.json');
const fr=read('../locales/fr.json');
const partById=new Map(atlas.parts.map(p=>[p.id,p]));
const systemOf=concept=>{
 const tally={};
 for(const id of concept.elements){const s=partById.get(id)?.system;if(s)tally[s]=(tally[s]??0)+1;}
 return Object.entries(tally).sort((a,b)=>b[1]-a[1])[0]?.[0]??'?';
};
const ORDER=['cardiac','respiratory','digestive','urinary','lymphatic','endocrine','reproductive','sensory','connective','integumentary','nervous','skeletal','venous','arterial','muscular'];
const cell=v=>v===undefined?'*(non traduit)*':v==='TODO'?'**TODO**':v;

let out=`# Vocabulaire anatomique — relecture\n\nGénéré par \`node scripts/anatomy-review.mjs\` à partir de \`locales/anatomy-fr.json\`. Ne pas éditer à la main : corriger le JSON puis régénérer.\n\n`;
let totalDone=0,total=0,todos=0;
for(const system of ORDER){
 const concepts=atlas.concepts.filter(c=>systemOf(c)===system).sort((a,b)=>a.name.localeCompare(b.name));
 const conceptNames=new Set(concepts.map(c=>c.name.toLowerCase()));
 const parts=[...new Set(atlas.parts.filter(p=>p.system===system).map(p=>p.name))].filter(n=>!conceptNames.has(n.toLowerCase())).sort();
 const rows=[...concepts.map(c=>[c.name,names.concepts[c.id],c.id]),...parts.map(n=>[n,names.parts[n.toLowerCase()],'pièce'])];
 const done=rows.filter(r=>r[1]&&r[1]!=='TODO').length;
 totalDone+=done;total+=rows.length;todos+=rows.filter(r=>r[1]==='TODO').length;
 out+=`## ${fr.systems.names[system]} — ${done}/${rows.length}\n\n| Anglais | Français | Réf. |\n|---|---|---|\n`;
 for(const [en,frName,ref] of rows)out+=`| ${en} | ${cell(frName)} | ${ref} |\n`;
 out+='\n';
}
out=out.replace('# Vocabulaire anatomique — relecture\n',`# Vocabulaire anatomique — relecture\n\n**${totalDone} / ${total} termes traduits · ${todos} TODO**\n`);
writeFileSync(fileURLToPath(new URL('../TRADUCTIONS-VOCABULAIRE.md',import.meta.url)),out);
console.log(`TRADUCTIONS-VOCABULAIRE.md : ${totalDone}/${total} termes, ${todos} TODO.`);
