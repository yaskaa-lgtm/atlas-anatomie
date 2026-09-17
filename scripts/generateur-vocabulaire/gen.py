#!/usr/bin/env python3
"""Generateur a regles pour vaisseaux et muscles. Usage : python3 gen.py <system>  -> JSON sur stdout, relecture sur stderr."""
import json,re,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
from skel import BASE as SKEL,ORD,side,tooth
from skel import art as _art
def art(text,g):return 'des '+text if g in ('fp','mp') else _art(text,g)   # reutilise le squelette
ROOT=Path(__file__).resolve().parents[2]
atlas=json.loads((ROOT/'public/models/atlas.json').read_text())
done=json.loads((ROOT/'locales/anatomy-fr.json').read_text())['concepts']
frnames={c['id']:v for c,v in [(c,done.get(c['id'])) for c in atlas['concepts']] if v and v!='TODO'}
byname={c['name'].lower():c['id'] for c in atlas['concepts']}

def A(m,f=None):return (m,f or m)
ADJ={
 'renal':A('rénal','rénale'),'ileal':A('iléal','iléale'),'ulnar':A('ulnaire'),'azygos':A('azygos'),'lumbar':A('lombaire'),'radial':A('radial','radiale'),
 'portal':A('porte'),'cardiac':A('cardiaque'),'splenic':A('splénique'),'hepatic':A('hépatique'),'sigmoid':A('sigmoïdien','sigmoïdienne'),'femoral':A('fémoral','fémorale'),
 'basilic':A('basilique'),'fibular':A('fibulaire'),'cephalic':A('céphalique'),'axillary':A('axillaire'),'brachial':A('brachial','brachiale'),'systemic':A('systémique'),
 'lingular':A('lingulaire'),'subcostal':A('subcostal','subcostale'),'ileocolic':A('iléo-colique'),'obturator':A('obturateur','obturatrice'),'popliteal':A('poplité','poplitée'),
 'genicular':A('géniculaire'),'pulmonary':A('pulmonaire'),'subclavian':A('subclavier','subclavière'),'hemiazygos':A('hémi-azygos'),'testicular':A('testiculaire'),
 'suprarenal':A('surrénal','surrénale'),'colic':A('colique'),'iliolumbar':A('ilio-lombaire'),'subscapular':A('subscapulaire'),'common':A('commun','commune'),'iliac':A('iliaque'),
 'gastric':A('gastrique'),'middle':A('moyen','moyenne'),'deep':A('profond','profonde'),'lobar':A('lobaire'),'marginal':A('marginal','marginale'),'suprascapular':A('suprascapulaire'),
 'thoracodorsal':A('thoraco-dorsal','thoraco-dorsale'),'median':A('médian','médiane'),'sacral':A('sacral','sacrale'),'musculophrenic':A('musculo-phrénique'),'external':A('externe'),
 'internal':A('interne'),'lateral':A('latéral','latérale'),'medial':A('médial','médiale'),'brachiocephalic':A('brachio-céphalique'),'superior':A('supérieur','supérieure'),
 'inferior':A('inférieur','inférieure'),'rectal':A('rectal','rectale'),'saphenous':A('saphène'),'anterior':A('antérieur','antérieure'),'posterior':A('postérieur','postérieure'),
 'tibial':A('tibial','tibiale'),'jugular':A('jugulaire'),'ascending':A('ascendant','ascendante'),'descending':A('descendant','descendante'),'apical':A('apical','apicale'),'segmental':A('segmentaire'),
 'gluteal':A('glutéal','glutéale'),'phrenic':A('phrénique'),'thoracic':A('thoracique'),'upper':A('supérieur','supérieure'),'lower':A('inférieur','inférieure'),'pudendal':A('pudendal','pudendale'),
 'palmar':A('palmaire'),'metacarpal':A('métacarpien','métacarpienne'),'dorsal':A('dorsal','dorsale'),'basal':A('basal','basale'),'plantar':A('plantaire'),'metatarsal':A('métatarsien','métatarsienne'),
 'pre-hepatic':A('pré-hépatique'),'epigastric':A('épigastrique'),'mesenteric':A('mésentérique'),'gastroepiploic':A('gastro-omental','gastro-omentale'),'pancreaticoduodenal':A('pancréatico-duodénal','pancréatico-duodénale'),
 'antebrachial':A('antébrachial','antébrachiale'),'circumflex':A('circonflexe'),'scapular':A('scapulaire'),'accessory':A('accessoire'),'digital':A('digital','digitale'),'proper':A('propre'),
 'intercostal':A('intercostal','intercostale'),'humeral':A('huméral','humérale'),'interventricular':A('interventriculaire'),'apicoposterior':A('apico-postérieur','apico-postérieure'),
 'superficial':A('superficiel','superficielle'),'intrapulmonary':A('intrapulmonaire'),'subsegmental':A('subsegmentaire'),'perforating':A('perforant','perforante'),'coronary':A('coronaire'),
 'caval':A('cave'),'intrahepatic':A('intra-hépatique'),'extrahepatic':A('extra-hépatique'),'caudate':A('caudé','caudée'),'great':A('grand','grande'),'small':A('petit','petite'),
 'left':A('gauche'),'right':A('droit','droite'),'bronchopulmonary':A('broncho-pulmonaire'),'hepatovenous':A('hépato-veineux','hépato-veineuse'),'cardiac':A('cardiaque'),
 'venous':A('veineux','veineuse'),'arterial':A('artériel','artérielle'),'vascular':A('vasculaire'),'hollow':A('creux','creuse'),'terminal':A('terminal','terminale'),
 'ventricular':A('ventriculaire'),'atrial':A('atrial','atriale'),'sinuatrial':A('sino-atrial','sino-atriale'),'atrioventricular':A('atrio-ventriculaire'),'conus':A('du cône'),
 'first':A('premier','première'),'second':A('deuxième'),'third':A('troisième'),'fourth':A('quatrième'),'fifth':A('cinquième'),'sixth':A('sixième'),'seventh':A('septième'),'eighth':A('huitième'),'ninth':A('neuvième'),'tenth':A('dixième'),'eleventh':A('onzième'),'twelfth':A('douzième'),
}
# unites composees, traduites d'un bloc (forme feminine ; le masculin est derive par ADJ quand possible)
UNIT={
 'circumflex humeral':'circonflexe humérale','circumflex femoral':'circonflexe fémorale','circumflex scapular':'circonflexe scapulaire','circumflex iliac':'circonflexe iliaque',
 'palmar digital':'digitale palmaire','dorsal digital':'digitale dorsale','plantar digital':'digitale plantaire','palmar metacarpal':'métacarpienne palmaire','dorsal metacarpal':'métacarpienne dorsale',
 'plantar metatarsal':'métatarsienne plantaire','dorsal metatarsal':'métatarsienne dorsale','basal segmental':'segmentaire basale',
 'medial superior':'médiale supérieure','medial inferior':'médiale inférieure','lateral superior':'latérale supérieure','lateral inferior':'latérale inférieure',
 'anterior superior':'antérieure supérieure','anterior inferior':'antérieure inférieure','posterior superior':'postérieure supérieure','posterior inferior':'postérieure inférieure',
 'medial basal':'basale médiale','lateral basal':'basale latérale','anterior basal':'basale antérieure','posterior basal':'basale postérieure',
 'superior lingular':'lingulaire supérieure','inferior lingular':'lingulaire inférieure','vena cava':'cave','superior vena cava':'cave supérieure','inferior vena cava':'cave inférieure',
}
UNIT_M={'basal segmental':'segmentaire basal','medial basal':'basal médial','lateral basal':'basal latéral','anterior basal':'basal antérieur','posterior basal':'basal postérieur',
 'medial superior':'médial supérieur','medial inferior':'médial inférieur','lateral superior':'latéral supérieur','lateral inferior':'latéral inférieur',
 'anterior superior':'antérieur supérieur','anterior inferior':'antérieur inférieur','posterior superior':'postérieur supérieur','posterior inferior':'postérieur inférieur',
 'superior lingular':'lingulaire supérieur','inferior lingular':'lingulaire inférieur'}
PRE={'great','small','first','second','third','fourth','fifth','sixth','seventh','eighth','ninth','tenth','eleventh','twelfth'}  # adjectifs places avant le nom
NOUN={
 'vein':('veine','f'),'vena cava':('veine cave','f'),'caudate lobe branch':('branche du lobe caudé','f'),'venous arch':('arcade veineuse','f'),'venous network':('réseau veineux','m'),'venous tree':('arbre veineux','m'),'venous tree organ':('organe arborescent veineux','m'),
 'venous trunk':('tronc veineux','m'),'venous system':('système veineux','m'),'venous anastomosis':('anastomose veineuse','f'),'venous plexus':('plexus veineux','m'),
 'artery':('artère','f'),'arterial tree':('arbre artériel','m'),'arterial tree organ':('organe arborescent artériel','m'),'arterial trunk':('tronc artériel','m'),'arterial system':('système artériel','m'),'arterial anastomosis':('anastomose artérielle','f'),'arterial arch':('arcade artérielle','f'),
 'part':('partie','f'),'branch':('branche','f'),'tributary':('affluent','m'),'sector':('secteur','m'),'segment':('segment','m'),'trunk':('tronc','m'),'subdivision':('subdivision','f'),
 'region':('région','f'),'set':('ensemble','m'),'tree':('arbre','m'),'subsector':('sous-secteur','m'),'sinus':('sinus','m'),'plexus':('plexus','m'),'arch':('arcade','f'),'network':('réseau','m'),
 'hemiliver':('hémifoie','m'),'liver':('foie','m'),'penis':('pénis','m'),'ring finger':('annulaire','m'),'index finger':('index','m'),'middle finger':('majeur','m'),'little finger':('auriculaire','m'),
 'foot':('pied','m'),'hand':('main','f'),'ventricle':('ventricule','m'),'atrium':('atrium','m'),'heart':('cœur','m'),'lung':('poumon','m'),'thumb':('pouce','m'),'kidney':('rein','m'),
 'vascular tree':('arbre vasculaire','m'),'hollow tree organ':('organe arborescent creux','m'),'tree organ':('organe arborescent','m'),'vascular tree organ':('organe arborescent vasculaire','m'),
 'bronchopulmonary segment':('segment broncho-pulmonaire','m'),'hepatovenous segment':('segment hépato-veineux','m'),'hepatovenous subsector':('sous-secteur hépato-veineux','m'),
 'coronary sinus':('sinus coronaire','m'),'coronary sinus tree':('arbre du sinus coronaire','m'),'segmental vein':('veine segmentaire','f'),'pulmonary vein':('veine pulmonaire','f'),
 'aorta':('aorte','f'),'arch of aorta':('arc de l\'aorte','m'),'coronary artery':('artère coronaire','f'),'anastomosis':('anastomose','f'),'veins':('veines','fp'),'arteries':('artères','fp'),
 'perforating veins':('veines perforantes','fp'),'dorsal digital veins':('veines digitales dorsales','fp'),'plantar digital veins':('veines digitales plantaires','fp'),'anterior intercostal veins':('veines intercostales antérieures','fp'),
}
NOUN.update({k:v for k,v in SKEL.items() if k not in NOUN})
ROMAN={'i':'I','ii':'II','iii':'III','iv':'IV','v':'V','vi':'VI','vii':'VII','viii':'VIII','ix':'IX','x':'X'}
SPECIAL={
 'median cubital vein':('veine médiane du coude','f'),'median antebrachial vein':('veine médiane de l\'avant-bras','f'),'great saphenous vein':('grande veine saphène','f'),'small saphenous vein':('petite veine saphène','f'),
 'great cardiac vein':('grande veine cardiaque','f'),'small cardiac vein':('petite veine cardiaque','f'),'middle cardiac vein':('veine cardiaque moyenne','f'),'vascular tree':('arbre vasculaire','m'),
 'set of veins':('ensemble de veines','m'),'set of perforating veins':('ensemble des veines perforantes','m'),'set of dorsal digital veins':('ensemble des veines digitales dorsales','m'),'set of plantar digital veins':('ensemble des veines digitales plantaires','m'),
 'set of anterior intercostal veins':('ensemble des veines intercostales antérieures','m'),'portal venous tree':('arbre veineux porte','m'),'portal venous system':('système veineux porte','m'),
 'anterior cardiac venous tree':('arbre veineux cardiaque antérieur','m'),'superior vena caval tree':('arbre de la veine cave supérieure','m'),'inferior vena caval tree':('arbre de la veine cave inférieure','m'),
 'segment of venous tree organ':('segment d\'organe arborescent veineux','m'),'hollow tree organ':('organe arborescent creux','m'),
}

ADJ.update({
 'cerebral':A('cérébral','cérébrale'),'temporal':A('temporal','temporale'),'cerebellar':A('cérébelleux','cérébelleuse'),'recurrent':A('récurrent','récurrente'),
 'thoraco-acromial':A('thoraco-acromial','thoraco-acromiale'),'occipital':A('occipital','occipitale'),'choroidal':A('choroïdien','choroïdienne'),'callosomarginal':A('calloso-marginal','calloso-marginale'),
 'collateral':A('collatéral','collatérale'),'interosseous':A('interosseux','interosseuse'),'cervical':A('cervical','cervicale'),'carotid':A('carotidien','carotide'),'pontine':A('du pont'),
 'communicating':A('communicant','communicante'),'pericallosal':A('péricalleux','péricalleuse'),'central':A('central','centrale'),'thyrocervical':A('thyro-cervical','thyro-cervicale'),
 'posteromedial':A('postéro-médial','postéro-médiale'),'parietal':A('pariétal','pariétale'),'frontobasal':A('fronto-basal','fronto-basale'),'costocervical':A('costo-cervical','costo-cervicale'),
 'carpal':A('carpien','carpienne'),'vertebral':A('vertébral','vertébrale'),'pancreatic':A('pancréatique'),'transverse':A('transverse'),'sphenoid':A('sphénoïdal','sphénoïdale'),'septal':A('septal','septale'),
 'postcommunicating':A('post-communicant','post-communicante'),'precommunicating':A('pré-communicant','pré-communicante'),'vermian':A('vermien','vermienne'),'variant':A('variant','variante'),
 'ureteric':A('urétérique'),'thyroid':A('thyroïdien','thyroïdienne'),'thalamoperforating':A('thalamo-perforant','thalamo-perforante'),'thalamogeniculate':A('thalamo-géniculé','thalamo-géniculée'),
 'temporo-occipital':A('temporo-occipital','temporo-occipitale'),'tarsal':A('tarsien','tarsienne'),'splenial':A('splénial','spléniale'),'spinal':A('spinal','spinale'),'prefrontal':A('préfrontal','préfrontale'),
 'precuneal':A('précunéal','précunéale'),'precentral':A('précentral','précentrale'),'postcentral':A('postcentral','postcentrale'),'polar':A('polaire'),'pectoral':A('pectoral','pectorale'),
 'paracentral':A('paracentral','paracentrale'),'ophthalmic':A('ophtalmique'),'intermediomedial':A('intermédio-médial','intermédio-médiale'),'insular':A('insulaire'),'hypothalamic':A('hypothalamique'),
 'gastroduodenal':A('gastro-duodénal','gastro-duodénale'),'deltoid':A('deltoïdien','deltoïdienne'),'celiac':A('cœliaque'),'coeliac':A('cœliaque'),'bronchial':A('bronchique'),'arcuate':A('arqué','arquée'),
 'anterolateral':A('antéro-latéral','antéro-latérale'),'acromial':A('acromial','acromiale'),'subsuperior':A('sub-supérieur','sub-supérieure'),'mediobasal':A('médio-basal','médio-basale'),
 'laterobasal':A('latéro-basal','latéro-basale'),'gastro-epiploic':A('gastro-omental','gastro-omentale'),'cecal':A('cæcal','cæcale'),'basilar':A('basilaire'),'supreme':A('suprême'),
 'oesophageal':A('œsophagien','œsophagienne'),'esophageal':A('œsophagien','œsophagienne'),'intracranial':A('intracrânien','intracrânienne'),'inferomedial':A('inféro-médial','inféro-médiale'),
 'diagonal':A('diagonal','diagonale'),'distal':A('distal','distale'),'proximal':A('proximal','proximale'),'abdominal':A('abdominal','abdominale'),'lobar':A('lobaire'),'ovarian':A('ovarique'),
 'uterine':A('utérin','utérine'),'vesical':A('vésical','vésicale'),'lingual':A('lingual','linguale'),'facial':A('facial','faciale'),'maxillary':A('maxillaire'),'mandibular':A('mandibulaire'),
 'buccal':A('buccal','buccale'),'labial':A('labial','labiale'),'nasal':A('nasal','nasale'),'palatine':A('palatin','palatine'),'lacrimal':A('lacrymal','lacrymale'),'supraorbital':A('supra-orbitaire'),
 'infraorbital':A('infra-orbitaire'),'meningeal':A('méningé','méningée'),'auricular':A('auriculaire'),'pharyngeal':A('pharyngien','pharyngienne'),'laryngeal':A('laryngé','laryngée'),
 'gonadal':A('gonadique'),'sigmoid':A('sigmoïdien','sigmoïdienne'),'ileal':A('iléal','iléale'),'jejunal':A('jéjunal','jéjunale'),'cystic':A('cystique'),'gastroepiploic':A('gastro-omental','gastro-omentale'),
 'suprarenal':A('surrénale'),'intermediate':A('intermédiaire'),'peroneal':A('fibulaire'),'sural':A('surale'),'genicular':A('géniculaire'),'descending':A('descendant','descendante'),
 'ascending':A('ascendant','ascendante'),'nutrient':A('nourricier','nourricière'),'perforating':A('perforant','perforante'),'muscular':A('musculaire'),'cutaneous':A('cutané','cutanée'),
 'articular':A('articulaire'),'calcaneal':A('calcanéen','calcanéenne'),'malleolar':A('malléolaire'),'suprascapular':A('suprascapulaire'),'subscapular':A('subscapulaire'),'thoracodorsal':A('thoraco-dorsal','thoraco-dorsale'),
 'sinuatrial':A('sino-atrial','sino-atriale'),'conus':A('du cône artériel'),'atrioventricular':A('atrio-ventriculaire'),'obtuse':A('obtus','obtuse'),'acute':A('aigu','aiguë'),'interlobar':A('interlobaire'),
 'segmental':A('segmentaire'),'cortical':A('cortical','corticale'),'capsular':A('capsulaire'),'adrenal':A('surrénal','surrénale'),'ovarian':A('ovarique'),'testicular':A('testiculaire'),'pubic':A('pubien','pubienne'),
 'obturator':A('obturateur','obturatrice'),'iliolumbar':A('ilio-lombaire'),'lumbar':A('lombaire'),'sacral':A('sacral','sacrale'),'gluteal':A('glutéal','glutéale'),'pudendal':A('pudendal','pudendale'),
})
UNIT.update({'anterior descending':'descendante antérieure','posterior descending':'descendante postérieure','anterior interventricular':'interventriculaire antérieure','posterior interventricular':'interventriculaire postérieure',
 'ulnar collateral':'collatérale ulnaire','radial collateral':'collatérale radiale','middle collateral':'collatérale moyenne','medial collateral':'collatérale médiale',
 'ulnar recurrent':'récurrente ulnaire','radial recurrent':'récurrente radiale','tibial recurrent':'récurrente tibiale','dorsal carpal':'carpienne dorsale','palmar carpal':'carpienne palmaire',
 'posterior inferior cerebellar':'cérébelleuse postéro-inférieure','anterior inferior cerebellar':'cérébelleuse antéro-inférieure','superior cerebellar':'cérébelleuse supérieure',
 'medial frontobasal':'fronto-basale médiale','lateral frontobasal':'fronto-basale latérale','posterior communicating':'communicante postérieure','anterior communicating':'communicante antérieure',
 'anterior choroidal':'choroïdienne antérieure','posterior medial choroidal':'choroïdienne postéro-médiale','posterior lateral choroidal':'choroïdienne postéro-latérale',
 'lateral tarsal':'tarsienne latérale','medial tarsal':'tarsienne médiale','common carotid':'carotide commune','internal carotid':'carotide interne','external carotid':'carotide externe',
 'deep cervical':'cervicale profonde','transverse cervical':'cervicale transverse','superficial cervical':'cervicale superficielle','inferior thyroid':'thyroïdienne inférieure','superior thyroid':'thyroïdienne supérieure',
 'polar temporal':'temporale polaire','anterior temporal':'temporale antérieure','middle temporal':'temporale moyenne','posterior temporal':'temporale postérieure',
 'anterior parietal':'pariétale antérieure','posterior parietal':'pariétale postérieure','lateral occipital':'occipitale latérale','medial occipital':'occipitale médiale',
 'anterior cerebral':'cérébrale antérieure','middle cerebral':'cérébrale moyenne','posterior cerebral':'cérébrale postérieure','anterior spinal':'spinale antérieure','posterior spinal':'spinale postérieure',
 'anterolateral central':'centrale antéro-latérale','posteromedial central':'centrale postéro-médiale','anterior interosseous':'interosseuse antérieure','posterior interosseous':'interosseuse postérieure','common interosseous':'interosseuse commune',
 'dorsal pancreatic':'pancréatique dorsale','inferior pancreatic':'pancréatique inférieure','great pancreatic':'pancréatique magna','caudal pancreatic':'pancréatique caudale',
 'anterior cecal':'cæcale antérieure','posterior cecal':'cæcale postérieure','superior terminal':'terminale supérieure','inferior terminal':'terminale inférieure',
})
NOUN.update({'precentral sulcus':('sillon précentral','m'),'postcentral sulcus':('sillon postcentral','m'),'colon':('côlon','m'),'continuity':('continuité','f'),'lobe':('lobe','m'),
 'angular gyrus':('gyrus angulaire','m'),'branches':('branches','fp'),'division':('division','f'),'vasculature':('vascularisation','f'),'system':('système','m'),'content':('contenu','m'),'compartment':('compartiment','m'),
 'arterial circle':('cercle artériel','m'),'abdomen':('abdomen','m'),'stomach':('estomac','m'),'spleen':('rate','f'),'pancreas':('pancréas','m'),'duodenum':('duodénum','m'),'jejunum':('jéjunum','m'),'ileum':('iléum','m'),
 'cecum':('cæcum','m'),'appendix':('appendice vermiforme','m'),'rectum':('rectum','m'),'esophagus':('œsophage','m'),'trachea':('trachée','f'),'bronchus':('bronche','f'),'brain':('encéphale','m'),
 'cerebellum':('cervelet','m'),'pons':('pont','m'),'spinal cord':('moelle spinale','f'),'thalamus':('thalamus','m'),'internal capsule':('capsule interne','f'),'posterior limb':('bras postérieur','m'),
 'larynx':('larynx','m'),'pharynx':('pharynx','m'),'tongue':('langue','f'),'face':('face','f'),'neck':('cou','m'),'thigh':('cuisse','f'),'leg':('jambe','f'),'arm':('bras','m'),'forearm':('avant-bras','m'),
 'diaphragm':('diaphragme','m'),'bladder':('vessie','f'),'urinary bladder':('vessie','f'),'prostate':('prostate','f'),'testis':('testicule','m'),'uterus':('utérus','m'),'ovary':('ovaire','m'),
 'ureter':('uretère','m'),'adrenal gland':('glande surrénale','f'),'suprarenal gland':('glande surrénale','f'),'thyroid gland':('glande thyroïde','f'),'gallbladder':('vésicule biliaire','f'),
})
SPECIAL.update({'right lobe branch':('branche du lobe droit','f'),'left lobe branch':('branche du lobe gauche','f'),'organ segment':('segment d\'organe','m'),'cardiovascular system':('système cardio-vasculaire','m'),'vasculature of body':('vascularisation du corps','f'),'antero-medial basal segmental artery':('artère segmentaire basale antéro-médiale','f'),'central sulcus':('sillon central','m'),'arteria princeps pollicis':('artère principale du pouce','f'),'arteria radialis indicis':('artère radiale de l\'index','f'),'dorsalis pedis artery':('artère dorsale du pied','f'),
 'hepatic artery proper':('artère hépatique propre','f'),'celiac trunk':('tronc cœliaque','m'),'coeliac trunk':('tronc cœliaque','m'),'variant artery':('artère variante','f'),'variant bronchial artery':('artère bronchique variante','f'),
 'arch of aorta':('arc de l\'aorte','m'),'abdominal aorta':('aorte abdominale','f'),'thoracic aorta':('aorte thoracique','f'),'ascending aorta':('aorte ascendante','f'),'descending aorta':('aorte descendante','f'),
 'cerebral arterial circle':('cercle artériel du cerveau','m'),'appendicular artery':('artère appendiculaire','f'),'arcuate artery':('artère arquée','f'),'set of arteries':('ensemble d\'artères','m'),
 'marginal artery of colon':('artère marginale du côlon','f'),'segment of artery':('segment d\'artère','m'),'vascular tree':('arbre vasculaire','m'),'anastomosis':('anastomose','f'),'arterial anastomosis':('anastomose artérielle','f'),
})

def M(fr):return ('muscle '+fr,'m')
MUSCLE={
 'soleus':M('soléaire'),'iliacus':M('iliaque'),'vocalis':M('vocal'),'omohyoid':M('omo-hyoïdien'),'gemellus':M('jumeau'),'anconeus':M('anconé'),'gracilis':M('gracile'),
 'platysma':('platysma','m'),'spinalis':M('épineux'),'splenius':M('splénius'),'perineum':('périnée','m'),'diaphragm':('diaphragme','m'),'coccygeus':M('coccygien'),'sartorius':M('sartorius'),
 'pectineus':M('pectiné'),'plantaris':M('plantaire'),'popliteus':M('poplité'),'supinator':M('supinateur'),'mylohyoid':M('mylo-hyoïdien'),'stylohyoid':M('stylo-hyoïdien'),'thyrohyoid':M('thyro-hyoïdien'),
 'subclavius':M('subclavier'),'piriformis':M('piriforme'),'brachialis':M('brachial'),'geniohyoid':M('génio-hyoïdien'),'hyoglossus':M('hyoglosse'),'sternohyoid':M('sterno-hyoïdien'),
 'psoas major':M('grand psoas'),'psoas minor':M('petit psoas'),'teres major':M('grand rond'),'teres minor':M('petit rond'),'soft palate':('palais mou','m'),'muscle organ':('muscle','m'),'uvula':('luette','f'),
 'puborectalis':M('pubo-rectal'),'genioglossus':M('génioglosse'),'supraspinatus':M('supra-épineux'),'sternothyroid':M('sterno-thyroïdien'),'pubococcygeus':M('pubo-coccygien'),'iliococcygeus':M('ilio-coccygien'),
 'infraspinatus':M('infra-épineux'),'uvular muscle':M('uvulaire'),'medial rectus':M('droit médial'),'lateral rectus':M('droit latéral'),'superior rectus':M('droit supérieur'),'inferior rectus':M('droit inférieur'),
 'superior oblique':M('oblique supérieur'),'inferior oblique':M('oblique inférieur'),'rhomboid major':M('grand rhomboïde'),'rhomboid minor':M('petit rhomboïde'),
 'gluteus maximus':M('grand glutéal'),'gluteus medius':M('moyen glutéal'),'gluteus minimus':M('petit glutéal'),'semitendinosus':M('semi-tendineux'),'semimembranosus':M('semi-membraneux'),
 'rectus femoris':M('droit fémoral'),'vastus medialis':M('vaste médial'),'vastus lateralis':M('vaste latéral'),'vastus intermedius':M('vaste intermédiaire'),'quadriceps femoris':M('quadriceps fémoral'),
 'longus capitis':M('long de la tête'),'longus colli':M('long du cou'),'scalenus anterior':M('scalène antérieur'),'scalenus medius':M('scalène moyen'),'scalenus posterior':M('scalène postérieur'),
 'adductor longus':M('long adducteur'),'adductor brevis':M('court adducteur'),'adductor magnus':M('grand adducteur'),'adductor minimus':M('petit adducteur'),'adductor hallucis':M('adducteur de l\'hallux'),'adductor pollicis':M('adducteur du pouce'),
 'deltoid':M('deltoïde'),'palmaris longus':M('long palmaire'),'palmaris brevis':M('court palmaire'),'brachioradialis':M('brachio-radial'),'thyro-arytenoid':M('thyro-aryténoïdien'),'aryepiglotticus':M('ary-épiglottique'),
 'pectoralis minor':M('petit pectoral'),'pectoralis major':M('grand pectoral'),'external oblique':M('oblique externe'),'internal oblique':M('oblique interne'),'splenius capitis':M('splénius de la tête'),'splenius cervicis':M('splénius du cou'),
 'coracobrachialis':M('coraco-brachial'),'extensor indicis':M('extenseur de l\'index'),'serratus anterior':M('dentelé antérieur'),'serratus posterior':M('dentelé postérieur'),
 'serratus posterior superior':M('dentelé postérieur supérieur'),'serratus posterior inferior':M('dentelé postérieur inférieur'),'gemellus superior':M('jumeau supérieur'),'gemellus inferior':M('jumeau inférieur'),
 'quadratus femoris':M('carré fémoral'),'quadratus lumborum':M('carré des lombes'),'spinalis thoracis':M('épineux du thorax'),'trapezius':M('trapèze'),'opponens pollicis':M('opposant du pouce'),
 'abductor hallucis':M('abducteur de l\'hallux'),'oblique arytenoid':M('aryténoïdien oblique'),'transverse arytenoid':M('aryténoïdien transverse'),'obturator internus':M('obturateur interne'),'obturator externus':M('obturateur externe'),
 'flexor accessorius':M('carré plantaire'),'pronator quadratus':M('carré pronateur'),'pronator teres':M('rond pronateur'),'extensor digitorum':M('extenseur des doigts'),'levator ani':M('élévateur de l\'anus'),
 'longissimus capitis':M('longissimus de la tête'),'longissimus thoracis':M('longissimus du thorax'),'longissimus cervicis':M('longissimus du cou'),'transversus thoracis':M('transverse du thorax'),'transversus abdominis':M('transverse de l\'abdomen'),
 'semispinalis capitis':M('semi-épineux de la tête'),'semispinalis thoracis':M('semi-épineux du thorax'),'semispinalis cervicis':M('semi-épineux du cou'),'cricothyroid':M('crico-thyroïdien'),
 'tensor veli palatini':M('tenseur du voile du palais'),'levator veli palatini':M('élévateur du voile du palais'),'chest':('thorax','m'),'musculature':('musculature','f'),
 'iliocostalis lumborum':M('ilio-costal des lombes'),'iliocostalis thoracis':M('ilio-costal du thorax'),'iliocostalis cervicis':M('ilio-costal du cou'),'flexor carpi radialis':M('fléchisseur radial du carpe'),'flexor carpi ulnaris':M('fléchisseur ulnaire du carpe'),
 'gastrocnemius':M('gastrocnémien'),'interspinalis thoracis':M('interépineux du thorax'),'flexor hallucis longus':M('long fléchisseur de l\'hallux'),'flexor hallucis brevis':M('court fléchisseur de l\'hallux'),
 'flexor pollicis brevis':M('court fléchisseur du pouce'),'flexor pollicis longus':M('long fléchisseur du pouce'),'extensor digiti minimi':M('extenseur du petit doigt'),'extensor carpi ulnaris':M('extenseur ulnaire du carpe'),
 'biceps femoris':M('biceps fémoral'),'biceps brachii':M('biceps brachial'),'triceps brachii':M('triceps brachial'),'external anal sphincter':M('sphincter externe de l\'anus'),
 'flexor digitorum brevis':M('court fléchisseur des orteils'),'flexor digitorum longus':M('long fléchisseur des orteils'),'flexor digitorum profundus':M('fléchisseur profond des doigts'),'flexor digitorum superficialis':M('fléchisseur superficiel des doigts'),
 'lumbrical':M('lombrical'),'lumbricals':('muscles lombricaux','mp'),'rectus capitis anterior':M('droit antérieur de la tête'),'rectus capitis lateralis':M('droit latéral de la tête'),
 'rectus capitis posterior major':M('grand droit postérieur de la tête'),'rectus capitis posterior minor':M('petit droit postérieur de la tête'),'lateral crico-arytenoid':M('crico-aryténoïdien latéral'),'posterior crico-arytenoid':M('crico-aryténoïdien postérieur'),
 'extensor hallucis longus':M('long extenseur de l\'hallux'),'extensor hallucis brevis':M('court extenseur de l\'hallux'),'abductor pollicis brevis':M('court abducteur du pouce'),'abductor pollicis longus':M('long abducteur du pouce'),
 'extensor pollicis brevis':M('court extenseur du pouce'),'extensor pollicis longus':M('long extenseur du pouce'),'extensor digitorum longus':M('long extenseur des orteils'),'extensor digitorum brevis':M('court extenseur des orteils'),
 'obliquus capitis superior':M('oblique supérieur de la tête'),'obliquus capitis inferior':M('oblique inférieur de la tête'),'intertransversarius muscle':M('intertransversaire'),'lumbar intertransversarius':M('intertransversaire lombaire'),
 'papillary muscle':M('papillaire'),'external intercostal muscle':M('intercostal externe'),'internal intercostal muscle':M('intercostal interne'),'innermost intercostal muscle':M('intercostal intime'),'intercostal muscle':M('intercostal'),
 'levator palpebrae superioris':M('élévateur de la paupière supérieure'),'interspinales lumborum':('muscles interépineux des lombes','mp'),'interspinales cervicis':('muscles interépineux du cou','mp'),
 'abductor digiti minimi':M('abducteur du petit doigt'),'opponens digiti minimi':M('opposant du petit doigt'),'flexor digiti minimi brevis':M('court fléchisseur du petit doigt'),
 'extensor carpi radialis longus':M('long extenseur radial du carpe'),'extensor carpi radialis brevis':M('court extenseur radial du carpe'),'levatores costarum longi':('muscles longs élévateurs des côtes','mp'),'levatores costarum breves':('muscles courts élévateurs des côtes','mp'),
 'dorsal interossei':('muscles interosseux dorsaux','mp'),'palmar interossei':('muscles interosseux palmaires','mp'),'plantar interosseous':M('interosseux plantaire'),'dorsal interosseous':M('interosseux dorsal'),
 'anterior cervical intertransversarii':('muscles intertransversaires antérieurs du cou','mp'),'posterior cervical intertransversarii':('muscles intertransversaires postérieurs du cou','mp'),
 'medial lumbar intertransversarius':M('intertransversaire médial des lombes'),'lateral lumbar intertransversarius':M('intertransversaire latéral des lombes'),
 'myocardium':('myocarde','m'),'free wall':('paroi libre','f'),'compartment':('compartiment','m'),'dorsum':('dos','m'),'plantar part':('partie plantaire','f'),'subendocardial layer':('couche sous-endocardique','f'),
 'sternocleidomastoid':M('sterno-cléido-mastoïdien'),'head':('chef','m'),'head of organ':('chef d\'organe','m'),'head of muscle organ':('chef de muscle','m'),'faucial part':('partie faucale','f'),'anal part':('partie anale','f'),
 'inflow part':('chambre de remplissage','f'),'outflow part':('chambre de chasse','f'),'wall':('paroi','f'),'muscle':('muscle','m'),'zone':('zone','f'),'region':('région','f'),'mouth':('bouche','f'),
 'sphincter':M('sphincter'),'masseter':M('masséter'),'temporalis':M('temporal'),'buccinator':M('buccinateur'),'orbicularis oris':M('orbiculaire de la bouche'),'orbicularis oculi':M('orbiculaire de l\'œil'),
 'lateral pterygoid':M('ptérygoïdien latéral'),'medial pterygoid':M('ptérygoïdien médial'),'digastric':M('digastrique'),'tibialis anterior':M('tibial antérieur'),'tibialis posterior':M('tibial postérieur'),
 'fibularis longus':M('long fibulaire'),'fibularis brevis':M('court fibulaire'),'fibularis tertius':M('troisième fibulaire'),'rectus abdominis':M('droit de l\'abdomen'),'pyramidalis':M('pyramidal'),
 'latissimus dorsi':M('grand dorsal'),'subscapularis':M('subscapulaire'),'levator scapulae':M('élévateur de la scapula'),'tensor fasciae latae':M('tenseur du fascia lata'),'multifidus':M('multifide'),
 'erector spinae':M('érecteur du rachis'),'iliopsoas':M('ilio-psoas'),'bulbospongiosus':M('bulbo-spongieux'),'ischiocavernosus':M('ischio-caverneux'),'cremaster':M('crémaster'),
}
NOUN.update(MUSCLE);NOUN.update({'thorax':('thorax','m'),'infraspinatus muscle':('muscle infra-épineux','m'),'upper eyelid':('paupière supérieure','f'),'lower eyelid':('paupière inférieure','f'),'palate':('palais','m'),'rotator':('muscle rotateur','m'),'rotator muscle':('muscle rotateur','m')})
ADJ.update({'scalene':A('scalène'),'rotator':A('rotateur','rotatrice'),'prevertebral':A('prévertébral','prévertébrale'),'extra-ocular':A('extra-oculaire'),'intrinsic':A('intrinsèque'),'extrinsic':A('extrinsèque'),
 'postvertebral':A('postvertébral','postvertébrale'),'suboccipital':A('suboccipital','suboccipitale'),'papillary':A('papillaire'),'perineal':A('du périnée'),'thenar':A('thénar'),'hypothenar':A('hypothénar'),
 'uvular':A('uvulaire'),'interspinalis':A('interépineux','interépineuse'),'infrahyoid':A('infra-hyoïdien','infra-hyoïdienne'),'suprahyoid':A('supra-hyoïdien','supra-hyoïdienne'),'innermost':A('intime'),
 'long':A('long','longue'),'short':A('court','courte'),'oblique':A('oblique'),'straight':A('droit','droite'),'vertical':A('vertical','verticale'),'sternocostal':A('sterno-costal','sterno-costale'),
 'clavicular':A('claviculaire'),'anal':A('anal','anale'),'faucial':A('faucal','faucale'),'septal':A('septal','septale'),'lumbar':A('lombaire'),'cervical':A('cervical','cervicale'),'thoracic':A('thoracique'),
 'gluteal':A('glutéal','glutéale'),'pectoral':A('pectoral','pectorale'),'obturator':A('obturateur','obturatrice'),'myocardial':A('myocardique'),'humeral':A('huméral','humérale'),'ulnar':A('ulnaire'),
 'superficial':A('superficiel','superficielle'),'intermediate':A('intermédiaire'),'inflow':A('de remplissage'),'outflow':A('de chasse'),'subendocardial':A('sous-endocardique')})
UNIT.update({'anterolateral head':'chef antéro-latéral'})
SPECIAL.update({'muscle of head':('muscle de la tête','m'),'superficial perineal muscle':('muscle superficiel du périnée','m'),'myocardium of left ventricle proper':('myocarde du ventricule gauche proprement dit','m'),'myocardium of right ventricle proper':('myocarde du ventricule droit proprement dit','m'),'myocardial zone 11':('zone myocardique 11','m'),'myocardial zone 12':('zone myocardique 12','m'),'set of lumbricals of hand':('ensemble des muscles lombricaux de la main','m'),
 'set of lumbricals of left hand':('ensemble des muscles lombricaux de la main gauche','m'),'set of lumbricals of right hand':('ensemble des muscles lombricaux de la main droite','m'),
 'intrinsic muscle of dorsum of foot':('muscle intrinsèque du dos du pied','m'),'intrinsic muscle of plantar part of foot':('muscle intrinsèque de la plante du pied','m'),
 'faucial part of mouth':('partie faucale de la bouche','f'),'anal part of perineum':('partie anale du périnée','f'),'soft palate':('palais mou','m'),'musculature of chest':('musculature du thorax','f'),
 'wall of left side of heart':('paroi du cœur gauche','f'),'wall of right side of heart':('paroi du cœur droit','f')})

def adjf(w,g):
 if w in UNIT:return UNIT_M.get(w,UNIT[w]) if g=='m' else UNIT[w]
 if w in ADJ:return ADJ[w][0 if g=='m' else 1]
 return None
def tokenize(adjs):
 """decoupe une liste de mots en unites (bigrammes connus d'abord)."""
 out=[];i=0
 while i<len(adjs):
  if i+1<len(adjs) and ' '.join(adjs[i:i+2]) in UNIT:out.append(' '.join(adjs[i:i+2]));i+=2
  else:out.append(adjs[i]);i+=1
 return out
def noun_phrase(name):
 """'[left] adj adj NOUN' -> texte, genre"""
 words=name.split(' ')
 for n in range(min(4,len(words)),0,-1):
  head=' '.join(words[-n:])
  if head in NOUN:
   noun,g=NOUN[head];adjs=words[:-n]
   sd=None
   if adjs and adjs[0] in ('left','right'):sd=adjs[0];adjs=adjs[1:]
   units=tokenize(adjs)
   if 'segment' in head and units and units[-1] in ROMAN:noun=noun+' '+ROMAN[units[-1]];units=units[:-1]
   gg='m' if g in ('m','mp') else 'f'
   fr=[adjf(u,gg) for u in units]
   if any(f is None for f in fr):return None
   if g in ('fp','mp'):fr=[' '.join(w if w[-1] in 'sx' else w+'s' for w in f.split(' ')) for f in fr]
   pre=[f for u,f in zip(units,fr) if u in PRE];post=[f for u,f in zip(units,fr) if u not in PRE]
   text=' '.join(pre+[noun]+list(reversed(post)))
   if sd:text=side(text,gg,sd)
   return (text,g if g in ('fp','mp') else gg)
 return None
def tr(name):
 name=name.strip().lower().replace(' (in-vivo)','').replace(' (in vivo)','')
 if name in SPECIAL:return SPECIAL[name]
 m=re.fullmatch(r"(.+) (i|ii|iii|iv|v|vi|vii|viii|ix|x)",name)
 if m:
  r=tr(m.group(1))
  if r:return (r[0]+' '+ROMAN[m.group(2)],r[1])
 if name in NOUN:return NOUN[name]
 t=tooth(name)
 if t:return t
 m=re.fullmatch(r"(.+) proper",name)
 if m:
  r=tr(m.group(1))
  if r:return (r[0]+(' propres' if r[1]=='fp' else ' propre'),r[1])
 m=re.fullmatch(r"(.+?) to (.+)",name)
 if m and ' of ' in m.group(1):
  a=tr(m.group(1));b=tr(m.group(2))
  if a and b:return (a[0]+' pour '+('l\''+b[0] if re.match(r'^[aeiouyâàéèêëîïôûùœh]',b[0],re.I) else ('le ' if b[1]=='m' else 'la ')+b[0]),a[1])
 m=re.fullmatch(r"(.+?) of (.+)",name)
 if m:
  a=tr(m.group(1));b=tr(m.group(2))
  if a and b:return (a[0]+' '+art(b[0],b[1]),a[1])
 np_=noun_phrase(name)
 if np_:return np_
 m=re.fullmatch(r"(left|right) (.+)",name)
 if m:
  r=tr(m.group(2))
  if r:return (side(r[0],r[1],m.group(1)),r[1])
 m=re.fullmatch(r"(first|second|third|fourth|fifth|sixth|seventh|eighth|ninth|tenth|eleventh|twelfth) (.+)",name)
 if m:
  r=tr(m.group(2))
  if r:return (ORD[m.group(1)][0 if r[1]=='m' else 1]+' '+r[0],r[1])
 return None

pb={pp['id']:pp for pp in atlas['parts']}
def sysof(c):
 t={}
 for i in c['elements']:
  s=pb.get(i,{}).get('system')
  if s:t[s]=t.get(s,0)+1
 return max(t,key=t.get) if t else '?'
SYSTEM=sys.argv[1]
out={};miss=[]
for c in atlas['concepts']:
 if c['id'] in done or sysof(c)!=SYSTEM:continue
 r=tr(c['name'])
 if r:out[c['id']]=(c['name'],r[0])
 else:miss.append((c['id'],c['name']))
json.dump({k:v[1] for k,v in out.items()},sys.stdout,ensure_ascii=False,indent=0)
print('\n---',len(out),'traduits ;',len(miss),'non traduits',file=sys.stderr)
for k,v in out.items():print(f'{k:10} {v[0]:60} → {v[1]}',file=sys.stderr)
for k,v in miss:print(f'MANQUE {k:10} {v}',file=sys.stderr)
