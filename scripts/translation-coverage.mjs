// Compare locales/en.json (reference) et locales/fr.json.
// Affiche les cles pas encore traduites : elles s'affichent en anglais par repli automatique.
// Usage : node scripts/translation-coverage.mjs
import {readFileSync} from 'node:fs';
import {fileURLToPath} from 'node:url';

const read=name=>JSON.parse(readFileSync(fileURLToPath(new URL(`../locales/${name}.json`,import.meta.url)),'utf8'));
const isPlural=value=>value&&typeof value==='object'&&'one' in value&&'other' in value;
const flatten=(node,prefix='')=>Object.entries(node).flatMap(([key,value])=>{
 const path=prefix?`${prefix}.${key}`:key;
 return value&&typeof value==='object'&&!isPlural(value)?flatten(value,path):[path];
});

const reference=flatten(read('en'));
const translated=new Set(flatten(read('fr')));
const missing=reference.filter(key=>!translated.has(key));

console.log(`Interface : ${reference.length - missing.length}/${reference.length} cles traduites en francais.`);
if(!missing.length){console.log('Aucun TODO : toute l\'interface est traduite.');process.exit(0);}
console.log(`\n${missing.length} cle(s) encore en anglais :`);
for(const key of missing)console.log(`  TODO  ${key}`);
