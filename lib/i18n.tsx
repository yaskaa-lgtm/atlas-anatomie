import {createContext,useContext,useEffect,useMemo,useState,type ReactNode} from 'react';
import en from '@/locales/en.json';
import fr from '@/locales/fr.json';

/** Langues disponibles. `bcp47` sert à formater les nombres (1 234 en français, 1,234 en anglais). */
export const LOCALES={fr:{label:'Français',bcp47:'fr-FR'},en:{label:'English',bcp47:'en-US'}} as const;
export type Locale=keyof typeof LOCALES;
/** Ordre d'affichage dans le sélecteur de langue. */
export const LOCALE_ORDER=['fr','en'] as const satisfies readonly Locale[];
/** Langue affichée par défaut à la première visite. */
export const DEFAULT_LOCALE:Locale='fr';
/** Langue de référence : elle comble les traductions manquantes. */
export const REFERENCE_LOCALE:Locale='en';
const STORAGE_KEY='human-atlas.locale';
const MESSAGES:Record<Locale,unknown>={fr,en};

type PluralForms={one:string;other:string};
/** Construit la liste des clés valides à partir de en.json, pour que TypeScript signale les fautes de frappe. */
type Keys<T,P extends string=''>={
 [K in keyof T&string]:T[K] extends string?`${P}${K}`:T[K] extends PluralForms?`${P}${K}`:Keys<T[K],`${P}${K}.`>
}[keyof T&string];
export type MessageKey=Keys<typeof en>;
export type Vars=Record<string,string|number>;

export function formatNumber(value:number,locale:Locale){return value.toLocaleString(LOCALES[locale].bcp47);}

/** Suit un chemin pointé ("systems.presets.all") dans un fichier de langue. */
function lookup(source:unknown,key:string):unknown{
 return key.split('.').reduce<unknown>((node,part)=>node&&typeof node==='object'?(node as Record<string,unknown>)[part]:undefined,source);
}

/** Remplace les {variables} du texte. Les nombres sont formatés selon la langue active. */
function fill(template:string,locale:Locale,vars?:Vars){
 if(!vars)return template;
 return template.replace(/\{(\w+)\}/g,(match,name:string)=>{
  const value=vars[name];
  if(value===undefined)return match;
  return typeof value==='number'?formatNumber(value,locale):value;
 });
}

/** En français 0 et 1 prennent le singulier ("0 pièce"), en anglais seul 1 le prend. */
function isSingular(count:number,locale:Locale){return locale==='fr'?Math.abs(count)<2:Math.abs(count)===1;}

function translate(locale:Locale,key:string,vars?:Vars):string{
 const chain=locale===REFERENCE_LOCALE?[locale]:[locale,REFERENCE_LOCALE];
 for(const candidate of chain){
  const entry=lookup(MESSAGES[candidate],key);
  if(typeof entry==='string')return fill(entry,locale,vars);
  if(entry&&typeof entry==='object'&&'one' in entry&&'other' in entry){
   const forms=entry as PluralForms;
   const count=typeof vars?.count==='number'?vars.count:0;
   return fill(isSingular(count,locale)?forms.one:forms.other,locale,vars);
  }
 }
 const dev=(import.meta as {env?:{DEV?:boolean}}).env?.DEV;
 if(dev)console.warn(`[i18n] clé absente de en.json et de ${locale}.json : ${key}`);
 return key;
}

interface I18nValue{locale:Locale;setLocale:(next:Locale)=>void;t:(key:MessageKey,vars?:Vars)=>string;n:(value:number)=>string}
const I18nContext=createContext<I18nValue|null>(null);

/** Relit le choix de langue de la visite précédente, sinon applique la langue par défaut. */
function storedLocale():Locale{
 try{const saved=localStorage.getItem(STORAGE_KEY);if(saved&&saved in LOCALES)return saved as Locale;}catch{/* stockage refusé (navigation privée) */}
 return DEFAULT_LOCALE;
}

export function I18nProvider({children}:{children:ReactNode}){
 const [locale,setLocale]=useState<Locale>(storedLocale);
 useEffect(()=>{
  document.documentElement.lang=locale;
  document.title=translate(locale,'app.title');
  document.querySelector('meta[name="description"]')?.setAttribute('content',translate(locale,'app.metaDescription'));
  try{localStorage.setItem(STORAGE_KEY,locale);}catch{/* la langue reste valable pour cette visite */}
 },[locale]);
 const value=useMemo<I18nValue>(()=>({locale,setLocale,t:(key,vars)=>translate(locale,key,vars),n:count=>formatNumber(count,locale)}),[locale]);
 return <I18nContext.Provider value={value}>{children}</I18nContext.Provider>;
}

export function useI18n(){
 const value=useContext(I18nContext);
 if(!value)throw new Error('useI18n doit être appelé à l’intérieur de <I18nProvider>.');
 return value;
}
