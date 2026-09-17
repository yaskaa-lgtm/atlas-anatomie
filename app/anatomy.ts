import type {MessageKey} from '@/lib/i18n';
export type SystemId = 'skeletal'|'muscular'|'arterial'|'venous'|'nervous'|'digestive'|'respiratory'|'urinary'|'reproductive'|'lymphatic'|'endocrine'|'integumentary'|'connective'|'sensory'|'cardiac';
/** Les noms et descriptions sont dans locales/*.json sous systems.names.* et systems.descriptions.*.
 *  L'ordre de ce tableau détermine les angles d'éclatement dans scene.tsx : ne pas le modifier. */
export const SYSTEMS: {id:SystemId;color:string}[] = [
 {id:'skeletal',color:'#e2d9ba'},
 {id:'muscular',color:'#a85b50'},
 {id:'cardiac',color:'#b96760'},
 {id:'sensory',color:'#b0c8ce'},
 {id:'arterial',color:'#c05245'},
 {id:'venous',color:'#527c9f'},
 {id:'nervous',color:'#d8b565'},
 {id:'respiratory',color:'#b98991'},
 {id:'digestive',color:'#b8916b'},
 {id:'urinary',color:'#b47961'},
 {id:'lymphatic',color:'#879f7c'},
 {id:'endocrine',color:'#c5a09a'},
 {id:'reproductive',color:'#bda098'},
 {id:'integumentary',color:'#ba9b7d'},
 {id:'connective',color:'#aec3bb'},
];
export interface Part {id:string;name:string;conceptId:string;system:SystemId;chunk:number;positions:number;normals:number;indices:number;vertexCount:number;indexCount:number;bounds:[number[],number[]]}
export interface Concept {id:string;name:string;elements:string[]}
export interface Atlas {version:string;sex?:'male';source?:string;scope?:string;parts:Part[];concepts:Concept[];chunks:{url:string;bytes:number;gzip?:string;gzipBytes?:number}[];triangles:number}
export type View = 'three-quarter'|'front'|'back'|'side';
export interface SceneState {inspectorOpen?:boolean;explode:number;visible:SystemId[];selected:string[];isolate:boolean;view:View;rotate:boolean;reset:number;/** Zoom molette vers le point sous le curseur (et recentrage de l'orbite) plutôt que vers le centre. */zoomToCursor:boolean}
export const DEFAULT_VISIBLE:SystemId[] = ['cardiac','sensory','skeletal','muscular','arterial','venous','nervous','respiratory','digestive','urinary','lymphatic','endocrine','reproductive','connective'];
/** Organes ayant une explication propre. Ces clés correspondent aux noms anglais de l'atlas source
 *  (atlas.json), elles servent à retrouver la bonne entrée : ne pas les traduire. */
export const ORGAN_KEYS = ['heart','liver','brain','stomach','spleen','pancreas','urinary bladder','trachea','diaphragm'] as const;
export type OrganKey = typeof ORGAN_KEYS[number];
export function hasOrganExplanation(name:string):name is OrganKey{return (ORGAN_KEYS as readonly string[]).includes(name);}
/** Renvoie la clé de traduction à afficher : l'explication de l'organe si elle existe, sinon la description de son système. */
export function explanationKey(name:string,system:SystemId):MessageKey{
 const slug=name.toLowerCase();
 return hasOrganExplanation(slug)?`organs.${slug}`:`systems.descriptions.${system}`;
}
