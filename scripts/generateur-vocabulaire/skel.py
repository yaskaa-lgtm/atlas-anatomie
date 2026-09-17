#!/usr/bin/env python3
"""Generateur de traductions pour le squelette. Sortie : JSON {id: fr} sur stdout, non-traduits sur stderr."""
import json,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
atlas=json.loads((ROOT/'public/models/atlas.json').read_text())
done=json.loads((ROOT/'locales/anatomy-fr.json').read_text())['concepts']

ORD={'first':('premier','première'),'second':('deuxième','deuxième'),'third':('troisième','troisième'),'fourth':('quatrième','quatrième'),
 'fifth':('cinquième','cinquième'),'sixth':('sixième','sixième'),'seventh':('septième','septième'),'eighth':('huitième','huitième'),
 'ninth':('neuvième','neuvième'),'tenth':('dixième','dixième'),'eleventh':('onzième','onzième'),'twelfth':('douzième','douzième')}
# (francais, genre)
BASE={
 'rib':('côte','f'),'true rib':('vraie côte','f'),'false rib':('fausse côte','f'),'floating rib':('côte flottante','f'),'typical rib':('côte typique','f'),'atypical rib':('côte atypique','f'),
 'rib cage':('cage thoracique','f'),'costal cartilage':('cartilage costal','m'),'sternum':('sternum','m'),'manubrium':('manubrium','m'),'body of sternum':('corps du sternum','m'),'xiphoid process':('processus xiphoïde','m'),'zone of sternum':('zone du sternum','f'),
 'vertebra':('vertèbre','f'),'cervical vertebra':('vertèbre cervicale','f'),'thoracic vertebra':('vertèbre thoracique','f'),'lumbar vertebra':('vertèbre lombaire','f'),
 'atlas':('atlas','m'),'axis':('axis','m'),'sacrum':('sacrum','m'),'vertebral column':('colonne vertébrale','f'),'cervical vertebral column':('colonne vertébrale cervicale','f'),'thoracic vertebral column':('colonne vertébrale thoracique','f'),'lumbar vertebral column':('colonne vertébrale lombaire','f'),
 'set of cervical vertebrae':('ensemble des vertèbres cervicales','m'),'set of thoracic vertebrae':('ensemble des vertèbres thoraciques','m'),'set of lumbar vertebrae':('ensemble des vertèbres lombaires','m'),
 'intervertebral disk':('disque intervertébral','m'),'intervertebral symphysis':('symphyse intervertébrale','f'),'cervical intervertebral symphysis':('symphyse intervertébrale cervicale','f'),'thoracic intervertebral symphysis':('symphyse intervertébrale thoracique','f'),'lumbar intervertebral symphysis':('symphyse intervertébrale lombaire','f'),'articular disk':('disque articulaire','m'),'symphysis':('symphyse','f'),
 'skull':('crâne','m'),'neurocranium':('neurocrâne','m'),'basicranium':('base du crâne','f'),'frontal bone':('os frontal','m'),'parietal bone':('os pariétal','m'),'occipital bone':('os occipital','m'),'temporal bone':('os temporal','m'),'sphenoid bone':('os sphénoïde','m'),'ethmoid':('os ethmoïde','m'),
 'maxilla':('maxillaire','m'),'mandible':('mandibule','f'),'zygomatic bone':('os zygomatique','m'),'nasal bone':('os nasal','m'),'palatine bone':('os palatin','m'),'vomer':('vomer','m'),'hyoid bone':('os hyoïde','m'),
 'upper jaw':('mâchoire supérieure','f'),'lower jaw':('mâchoire inférieure','f'),'gingiva':('gencive','f'),'tooth':('dent','f'),'molar tooth':('molaire','f'),'premolar tooth':('prémolaire','f'),'canine tooth':('canine','f'),'incisor tooth':('incisive','f'),
 'skeleton of mouth':('squelette de la bouche','m'),'maxillary part of mouth':('partie maxillaire de la bouche','f'),'mandibular part of mouth':('partie mandibulaire de la bouche','f'),
 'nose':('nez','m'),'external nose':('nez externe','m'),'internal nose':('nez interne','m'),'root of nose':('racine du nez','f'),'nasal skeleton':('squelette nasal','m'),'osseous skeleton of nose':('squelette osseux du nez','m'),'osseous skeleton of external nose':('squelette osseux du nez externe','m'),'cartilaginous skeleton of external nose':('squelette cartilagineux du nez externe','m'),'bony part of nasal septum':('partie osseuse du septum nasal','f'),'septum':('septum','m'),'major alar cartilage':('grand cartilage alaire','m'),
 'cricoid cartilage':('cartilage cricoïde','m'),'thyroid cartilage':('cartilage thyroïde','m'),'arytenoid cartilage':('cartilage aryténoïde','m'),'corniculate cartilage':('cartilage corniculé','m'),'cuneiform cartilage':('cartilage cunéiforme','m'),'laryngeal cartilage':('cartilage du larynx','m'),
 'clavicle':('clavicule','f'),'scapula':('scapula','f'),'humerus':('humérus','m'),'radius':('radius','m'),'ulna':('ulna','f'),
 'scaphoid':('scaphoïde','m'),'lunate':('lunatum','m'),'triquetral':('triquetrum','m'),'pisiform':('pisiforme','m'),'trapezium':('trapèze','m'),'trapezoid':('trapézoïde','m'),'capitate':('capitatum','m'),'hamate':('hamatum','m'),
 'carpal bone':('os du carpe','m'),'proximal carpal bone':('os de la rangée proximale du carpe','m'),'distal carpal bone':('os de la rangée distale du carpe','m'),'metacarpal bone':('métacarpien','m'),
 'phalanx':('phalange','f'),'proximal phalanx':('phalange proximale','f'),'middle phalanx':('phalange moyenne','f'),'distal phalanx':('phalange distale','f'),
 'thumb':('pouce','m'),'index finger':('index','m'),'middle finger':('majeur','m'),'ring finger':('annulaire','m'),'little finger':('auriculaire','m'),'finger':('doigt','m'),
 'big toe':('hallux','m'),'second toe':('deuxième orteil','m'),'third toe':('troisième orteil','m'),'fourth toe':('quatrième orteil','m'),'little toe':('petit orteil','m'),'toe':('orteil','m'),
 'hip bone':('os coxal','m'),'bony pelvis':('pelvis osseux','m'),'pelvic girdle':('ceinture pelvienne','f'),'pelvic skeleton':('squelette pelvien','m'),'pelvis':('pelvis','m'),'posterior part of pelvis':('partie postérieure du pelvis','f'),
 'femur':('fémur','m'),'patella':('patella','f'),'tibia':('tibia','m'),'fibula':('fibula','f'),
 'talus':('talus','m'),'calcaneus':('calcanéus','m'),'navicular bone':('os naviculaire','m'),'cuboid bone':('os cuboïde','m'),'cuneiform bone':('os cunéiforme','m'),'medial cuneiform bone':('os cunéiforme médial','m'),'intermediate cuneiform bone':('os cunéiforme intermédiaire','m'),'lateral cuneiform bone':('os cunéiforme latéral','m'),
 'tarsal bone':('os du tarse','m'),'metatarsal bone':('métatarsien','m'),'sesamoid bone':('os sésamoïde','m'),
 'bone organ':('os','m'),'long bone':('os long','m'),'short bone':('os court','m'),'flat bone':('os plat','m'),'irregular bone':('os irrégulier','m'),'pneumatized bone':('os pneumatique','m'),'zone of bone organ':('zone d\'os','f'),'process of organ':('processus d\'organe','m'),'body of organ':('corps d\'organe','m'),
 'skeletal system':('système squelettique','m'),'axial skeleton':('squelette axial','m'),'axial skeletal system':('système squelettique axial','m'),'musculoskeletal system':('appareil locomoteur','m'),'skeleton (in vivo)':('squelette','m'),'skeletal system of trunk':('système squelettique du tronc','m'),'skeletal system of thorax':('système squelettique du thorax','m'),
 'cartilage organ':('cartilage','m'),'cartilage organ component':('composant de cartilage','m'),'cavitated organ':('organe cavitaire','m'),'organ with organ cavity':('organe à cavité','m'),'organ with cavitated organ parts':('organe à parties cavitaires','m'),
 'head':('tête','f'),'neck':('cou','m'),'back of neck':('nuque','f'),'occipital part of head':('partie occipitale de la tête','f'),'cheek':('joue','f'),
 'abdomen':('abdomen','m'),'abdomen proper':('abdomen proprement dit','m'),'back of abdomen':('région postérieure de l\'abdomen','f'),'wall of abdomen':('paroi de l\'abdomen','f'),'wall of abdomen proper':('paroi de l\'abdomen proprement dit','f'),'posterior abdominal wall':('paroi abdominale postérieure','f'),'abdominal segment of trunk':('segment abdominal du tronc','m'),
 'body wall':('paroi du corps','f'),'chest wall':('paroi thoracique','f'),'thoracic wall':('paroi thoracique','f'),'anterior chest wall':('paroi thoracique antérieure','f'),'anterior thoracic wall':('paroi thoracique antérieure','f'),'posterior thoracic wall':('paroi thoracique postérieure','f'),'back of thorax':('dos','m'),'posterior chest':('thorax postérieur','m'),'sternal part of chest':('région sternale','f'),'side':('côté','m'),
 'upper limb':('membre supérieur','m'),'lower limb':('membre inférieur','m'),'free upper limb':('partie libre du membre supérieur','f'),'free lower limb':('partie libre du membre inférieur','f'),
 'shoulder':('épaule','f'),'forearm':('avant-bras','m'),'wrist':('poignet','m'),'hand':('main','f'),'hand proper':('main proprement dite','f'),'hip':('hanche','f'),'thigh':('cuisse','f'),'knee':('genou','m'),'leg':('jambe','f'),'foot':('pied','m'),'foot proper':('pied proprement dit','m'),
 'anterior part':('partie antérieure','f'),'patellar part':('partie patellaire','f'),'bony pectoral girdle':('ceinture pectorale osseuse','f'),'pectoral girdle':('ceinture pectorale','f'),'skeleton':('squelette','m'),
 'subscapularis':('muscle subscapulaire','m'),'levator scapulae':('muscle élévateur de la scapula','m'),'tibialis anterior':('muscle tibial antérieur','m'),'tibialis posterior':('muscle tibial postérieur','m'),
 'fibularis longus':('muscle long fibulaire','m'),'fibularis brevis':('muscle court fibulaire','m'),'fibularis tertius':('muscle troisième fibulaire','m'),'muscle':('muscle','m'),'lateral compartment':('compartiment latéral','m'),
 'iliotibial tract':('tractus ilio-tibial','m'),'fascia lata':('fascia lata','m'),'zone of fascia lata':('zone du fascia lata','f'),'investing fascia':('fascia','m'),'zone':('zone','f'),'deep fascial system':('système des fascias profonds','m'),
}
VOWEL=re.compile(r"^[aeiouyâàéèêëîïôûùœh]",re.I)
def art(text,g):
 if VOWEL.match(text):return "de l'"+text
 return ("du " if g=='m' else "de la ")+text
def side(text,g,s):
 tail=re.findall(r" (du|de la|de l') ",text)
 if text.startswith(('muscle ','chef ')):g='m'
 elif tail and tail[-1]!="de l'":g='m' if tail[-1]=='du' else 'f'
 w='gauche' if s=='left' else ('droit' if g=='m' else 'droite')
 if ' proprement dit' in text:
  i=text.index(' proprement dit');return text[:i]+' '+w+text[i:]
 return text+' '+w
def tooth(name):
 m=re.fullmatch(r"(?:(left|right) )?(?:(upper|lower) )?(?:(first|second|central|lateral) )?(secondary )?(molar|premolar|canine|incisor) tooth",name)
 if not m:return None
 s,ul,mod,sec,kind=m.groups()
 base={'molar':'molaire','premolar':'prémolaire','canine':'canine','incisor':'incisive'}[kind]
 out=[]
 if mod in ('first','second'):out.append(ORD[mod][1])
 out.append(base)
 if mod=='central':out.append('centrale')
 if mod=='lateral':out.append('latérale')
 if sec:out.append('permanente')
 if ul:out.append('supérieure' if ul=='upper' else 'inférieure')
 if s:out.append('gauche' if s=='left' else 'droite')
 return (' '.join(out),'f')
def tr(name):
 name=name.strip()
 if name in BASE:return BASE[name]
 t=tooth(name)
 if t:return t
 m=re.fullmatch(r"(.+?) of (.+)",name)
 if m:
  a=tr(m.group(1));b=tr(m.group(2))
  if a and b:return (a[0]+' '+art(b[0],b[1]),a[1])
 m=re.fullmatch(r"(first|second|third|fourth|fifth|sixth|seventh|eighth|ninth|tenth|eleventh|twelfth) (.+)",name)
 if m:
  r=tr(m.group(2))
  if r:
   o=ORD[m.group(1)][0 if r[1]=='m' else 1];return (o+' '+r[0],r[1])
 m=re.fullmatch(r"(left|right) (.+)",name)
 if m:
  r=tr(m.group(2))
  if r:return (side(r[0],r[1],m.group(1)),r[1])
 return None

if __name__=='__main__':
 pb={pp['id']:pp for pp in atlas['parts']}
 def sysof(c):
  t={}
  for i in c['elements']:
   s=pb.get(i,{}).get('system')
   if s:t[s]=t.get(s,0)+1
  return max(t,key=t.get) if t else '?'
 SYSTEM=sys.argv[1] if len(sys.argv)>1 else 'skeletal'
 out={};miss=[]
 for c in atlas['concepts']:
  if c['id'] in done or sysof(c)!=SYSTEM:continue
  r=tr(c['name'].lower())
  if r:out[c['id']]=(c['name'],r[0])
  else:miss.append((c['id'],c['name']))
 json.dump({k:v[1] for k,v in out.items()},sys.stdout,ensure_ascii=False,indent=0)
 print('\n---',len(out),'traduits ;',len(miss),'non traduits',file=sys.stderr)
 for k,v in out.items():print(f'{k:10} {v[0]:55} → {v[1]}',file=sys.stderr)
 for k,v in miss:print(f'MANQUE {k:10} {v}',file=sys.stderr)
