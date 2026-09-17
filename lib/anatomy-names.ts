import {useMemo} from 'react';
import {useI18n,type Locale} from '@/lib/i18n';
import raw from '@/locales/anatomy-fr.json';

/** Table des noms français. Les concepts sont indexés par identifiant FMA, les pièces par nom anglais en minuscules. */
const NAMES=raw as {concepts:Record<string,string>;parts:Record<string,string>};

/** Normalise un texte pour la recherche : minuscules et sans accents, pour que « artere » trouve « artère ». */
export function fold(text:string){return text.toLowerCase().normalize('NFD').replace(/\p{Diacritic}/gu,'');}

/** Nom d'un concept (résultat de recherche) : français s'il existe, sinon l'anglais de l'atlas. */
export function conceptName(concept:{id:string;name:string},locale:Locale){
 return locale==='fr'?NAMES.concepts[concept.id]??concept.name:concept.name;
}

/** Nom d'une pièce (maillage individuel). */
export function partName(part:{name:string},locale:Locale){
 return locale==='fr'?NAMES.parts[part.name.toLowerCase()]??part.name:part.name;
}

/** Nom de la structure choisie : elle peut venir de la recherche (concept) ou d'un clic sur le corps (pièce),
 *  on essaie donc la table des pièces, puis celle des concepts, avant de garder l'anglais. */
export function chosenName(chosen:{id:string;name:string},locale:Locale){
 if(locale!=='fr')return chosen.name;
 return NAMES.parts[chosen.name.toLowerCase()]??NAMES.concepts[chosen.id]??chosen.name;
}

/** Fournit les trois résolveurs liés à la langue active. Mémorisé pour rester stable dans les dépendances de useMemo. */
export function useAnatomyName(){
 const {locale}=useI18n();
 return useMemo(()=>({
  concept:(concept:{id:string;name:string})=>conceptName(concept,locale),
  part:(part:{name:string})=>partName(part,locale),
  chosen:(chosen:{id:string;name:string})=>chosenName(chosen,locale),
 }),[locale]);
}
