"""Reconcile the master list with filed returns and reviewed supervisor decisions."""
from __future__ import annotations
import csv
import json
import re
import shutil
from pathlib import Path
from collections import Counter
from zipfile import ZipFile
from xml.etree import ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
GROUPED=ROOT/'raw-data-grouped'
DATA=ROOT/'scripts/reconciliation-data'
TMP=ROOT/'tmp/reconciliation'
MASTER='SCHOOLS BY DISTRICT AND HEALTH CENTRES.docx'
NS={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
def clean(value): return re.sub(r'\s+',' ',str(value)).strip()
def key(value): return re.sub(r'[^a-z0-9]','',value.lower())
LG_ALIASES={'fortportal':'Fort-Portal City','kassanda':'Kasanda','luwero':'Luweero','rakia':'Rakai','liramc':'Lira City','masakamc':'Masaka City','ssabagabomakindyemc':'Makindye-Ssabagabo MC','jinjamc':'Jinja City','mbararamc':'Mbarara City','sheemamunicipalcouncil':'Sheema MC','hoimamc':'Hoima City','kasesemunicipalcouncil':'Kasese MC'}
def lg(value): return LG_ALIASES.get(key(value),value.replace(' Mc',' MC'))
def identity(r): return (key(lg(r['lg'])),r['type'],key(r['name']))
def read_json(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def write_csv(path,rows,fields):
 with path.open('w',newline='',encoding='utf-8-sig') as f:
  w=csv.DictWriter(f,fields,extrasaction='ignore'); w.writeheader(); w.writerows(rows)
def parse_master():
 with ZipFile(ROOT/MASTER) as z: tree=ET.fromstring(z.read('word/document.xml'))
 result=[]
 for typ,table in zip(['School','Health centre'],tree.findall('.//w:body/w:tbl',NS)):
  for number,row in enumerate(table.findall('w:tr',NS)[1:],1):
   cells=[clean(' '.join(x.text or '' for x in c.findall('.//w:t',NS))) for c in row.findall('w:tc',NS)]
   result.append(dict(id=('S' if typ=='School' else 'H')+str(number).zfill(3),type=typ,lg=cells[2],name=cells[3 if typ=='School' else 4],phase=cells[4] if typ=='School' else '',project_status=cells[5],source_row=number+1))
 return result

def main():
 DATA.mkdir(exist_ok=True)
 TMP.mkdir(parents=True,exist_ok=True)
 for source,target in [('previous_status_rows.json','prior-facility-mapping.json'),('teams.json','teams.json'),('chat_findings.json','supervisor-decisions.json'),('audit_register_evidence_map.json','register-evidence.json')]:
  dest=DATA/target
  if not dest.exists(): shutil.copy2(TMP/source,dest)
 baseline=read_json(DATA/'prior-facility-mapping.json'); teams=read_json(DATA/'teams.json'); chat=read_json(DATA/'supervisor-decisions.json')
 registry={identity(r):r for r in read_json(DATA/'register-evidence.json')}
 masters=parse_master(); lookup={identity(r):r for r in baseline if 'not on the programme list' not in r['note'] and r['type']!='Blood bank'}
 folders=[p for team in GROUPED.glob('team-*') for loc in team.iterdir() if loc.is_dir() and not loc.name.startswith('_') for p in loc.iterdir() if p.is_dir() and not p.name.startswith('_')]
 folder_keys={key(p.relative_to(GROUPED).as_posix()):p.relative_to(GROUPED).as_posix() for p in folders}
 index=list(csv.DictReader((GROUPED/'_index.csv').open(encoding='utf-8-sig',newline='')))
 all_files=sorted({r['destination (in raw-data-grouped)'] for r in index if r['destination (in raw-data-grouped)']})
 def folder_from_note(note):
  nk=key(note)
  matches=[(k,path) for k,path in folder_keys.items() if nk.startswith(k)]
  return max(matches,key=lambda item:len(item[0]))[1] if matches else ''
 def register_path(r):
  evidence=registry.get(identity(r))
  if evidence is None:
   raise ValueError(f"No reviewed register citation for {r['lg']}/{r['name']}")
  return evidence['source_path'].removeprefix('raw-data-grouped/')
 used=set(); records=[]; duplicates=[]
 lgteam={key(lg(loc)):int(t) for t,d in teams.items() for loc in d['lgs']}; lgteam['kalangala']=31
 seen={}
 for m in masters:
  ident=identity(m)
  if ident in seen:
   seen[ident]['master_ids']+='; '+m['id']
   if m['phase'] and m['phase'] not in seen[ident]['phase'].split('; '): seen[ident]['phase']+='; '+m['phase']
   if m['project_status'] not in seen[ident]['project_status'].split('; '): seen[ident]['project_status']+='; '+m['project_status']
   duplicates.append(dict(duplicate=m['id'],retained=seen[ident]['id'],lg=m['lg'],name=m['name'])); continue
  old=lookup.get(ident); team=old['team'] if old else lgteam.get(key(lg(m['lg'])))
  r=dict(m,master_ids=m['id'],lg=lg(m['lg']),master_lg=m['lg'],team=team,scope='Master list',ground_name='',folder='',source='',source_locator='',decision_ref='',note='',status='No return',verification='Not established')
  if old:
   r['note']=old['note']; r['prior_report_page']=old['old_page']
   if old['old_status']=='Received':
    r['folder']=folder_from_note(old['note']); r['status']='Field evidence'; r['verification']='Verification records received; physical completion not certified'
    if r['folder']: used.add(r['folder']); r['ground_name']=Path(r['folder']).name.replace('-',' ')
   elif old['old_status']=='Register only':
    r['status']='Field evidence'; r['source']=register_path(old); r['ground_name']=m['name']; r['verification']='Completed from consolidated register; physical inspection not certified'
  evidence=registry.get(ident)
  if evidence and old and old['old_status']=='Register only':
   r['source_locator']=evidence['sheet']+'!row '+str(evidence['row']); r['note']='Asset section: '+evidence['evidence_heading']
   if evidence['district_conflict']:
    r['status']='Needs review'; r['note']+='; '+evidence['district_conflict']; r['verification']='Asset rows received; district identity requires confirmation'
  seen[ident]=r; records.append(r)
 def find(loc,name,typ=None):
  hits=[r for r in records if key(r['lg'])==key(lg(loc)) and (key(r['name'])==key(name)) and (typ is None or r['type']==typ)]
  if len(hits)!=1: raise ValueError(f'Expected one master match: {loc}/{name}; found {len(hits)}')
  return hits[0]
 def set_folder(r,needle):
  paths=[p for p in folder_keys.values() if p==needle or p.endswith('/'+needle)]
  if len(paths)!=1: raise ValueError(f'Ambiguous folder {needle}: {paths}')
  r['folder']=paths[0]; used.add(paths[0]); r['ground_name']=Path(paths[0]).name.replace('-',' '); r['status']='Field evidence'; r['verification']='Verification records received; physical completion not certified'; r['source']=''
 # Newly supplied returns: explicit document identity or spelling variants in the same LG.
 new_matches=[('Kamuli MC','Busota HC II','Busota-HC-III'),('Kakumiro','Mpasaana','Christ-the-King-Mpasana-Seed-Secondary-School'),('Kakumiro','Birembo','St-Matia-Mulumba-Birembo-Seed-Secondary-School'),('Kyankwanzi','Nsambya','Nsambya-Seed-Secondary-School'),('Kyankwanzi','Ntwetwe','Ntwetwe-Seed-Secondary-School'),('Wakiso','Nakitokolo Namayumba HC II','Nakitokolo-HC-III'),('Gomba','Ngomanene HC II','Ngomamene-HC-III'),('Gomba','Mamba HC II','Mamba-HC-III'),('Makindye-Ssabagabo MC','Kibiri HC III','Kibiri-HC-III'),('Nansana MC','Matuga HCII','Matugga-HC-III'),('Masaka City','Nyendo HC II','Nyendo-HC-III'),('Lyantonde','Kabetemere HC II','Kabatemere-HC-III'),('Lyantonde','Lyakajura HC II','Lyakajjuka-HC-III'),('Lyantonde','Kasagama','Kasagama-Seed-Secondary-School')]
 # Exact master names are selected by reviewed spelling stems where the list adds explanatory text.
 for loc,name,folder in new_matches:
  candidates=[r for r in records if key(r['lg'])==key(loc) and r['type']==('Health centre' if '-HC-' in folder else 'School') and (key(r['name'])==key(name) or key(r['name']).startswith(key(name)))]
  if len(candidates)!=1: raise ValueError(f'New return mapping needs review {loc}/{name}: {[r["name"] for r in candidates]}')
  r=candidates[0]; set_folder(r,folder); r['note']='New return received. Submitted facility name and local government used to reconcile the master entry.'
 aliases={'CHAT01':'Pangira-HC-III','CHAT05':'Akadot-Seed-Secondary-School','CHAT06':'Mpiita-Seed-Secondary-School','CHAT09':'Kangole-HC-III'}
 for dec in chat['decisions']:
  names=dec.get('master_names',[dec.get('master_name')])
  for name in names:
   r=find(dec['lg'],name); r['decision_ref']=dec['id']; r['note']=dec['decision']+'. '+dec['note']
   return_folder=dec.get('return_folder') or aliases.get(dec['id'])
   if return_folder:
    set_folder(r,return_folder)
    r['note']=dec.get('evidence_note',dec['decision']+'. '+dec['note'])
    if dec.get('resolved_status') and r['status']!=dec['resolved_status']:
     raise ValueError(f"Supervisor decision {dec['id']} expected {dec['resolved_status']}, got {r['status']}")
   elif dec['id']=='CHAT04': r['status']='Replaced'; r['ground_name']='Liko HC III'; r['verification']='Already-listed replacement; no second verified facility'; r['note']='Loinya was replaced by Liko, which already has master entry H212. Count Liko once.'
   elif dec['id'] in ['CHAT03','CHAT10','CHAT11']: r['status']='Reported absent'; r['verification']='Reported not known/not found; not independently established'
   elif dec['id']=='CHAT02':
    r['status']='No UgIFT assets'; r['verification']='Facility exists; supervisor reports no UgIFT assets'; r['note']='The supervisor confirms that Pandwong exists but did not receive UgIFT assets. It is therefore excluded from the missing-return count.'
   elif dec['id']=='CHAT14':
    r['status']='Outside UgIFT'; r['verification']='Reported outside UgIFT; not verified; facility type wording requires confirmation'; r['note']='The supervisor says Buyinda was not verified because it was outside UgIFT. The message alternates between health centre and seed school, while the master contains Buyinda HC II; retain that facility-type caveat.'
   elif dec['id']=='CHAT07':
    r['status']='Field evidence'; r['ground_name']='Kagwara Seed Secondary School'; r['source']=next(p for p in all_files if 'team-08' in p and 'SCHOOL' in p.upper() and p.endswith('.xlsx')); r['source_locator']='Sheet1!row 1598'; r['verification']='Completed from consolidated register; physical inspection not certified'; r['note']+=' Register uses Kagawa; chat confirms Kagwara in Kadungulu.'
   elif dec['id']=='CHAT08': r['note']+=' Existing Ndwaddemutwe evidence retained.'
 absence_reasons={
  ('CHAT03',key('Lodonga TC')):'The supervisor reports that Lodonga TC is not known to Yumbe District. This is a reported absence, not independent proof that the facility does not exist.',
  ('CHAT10',key('Acimi HC II')):'The supervisor explicitly reports that Acimi does not exist in Oyam. The six ground names supplied in the same message are not paired one-to-one with Acimi.',
  ('CHAT10',key('Acokara HCII')):'The supervisor explicitly reports that Acokara (written Achokara in the chat) does not exist in Oyam. The six ground names supplied are not paired one-to-one with this entry.',
  ('CHAT10',key('Ariba HC II')):'The supervisor explicitly reports that Ariba does not exist in Oyam. The six ground names supplied in the same message are not paired one-to-one with Ariba.',
  ('CHAT11',key('Alik HCII')):'The supervisor explicitly reports that Alik does not exist in Lira. Barlonyo and Onywako are named on the ground, but neither is identified as a one-to-one replacement for Alik; the Onywako return also says physical verification was not performed.',
 }
 for r in records:
  reason=absence_reasons.get((r['decision_ref'],key(r['name'])))
  if reason: r['note']=reason
 def review(loc,name,note):
  r=find(loc,name); r['status']='Needs review'; r['verification']='Physical verification not confirmed because returns conflict'; r['note']=note; return r
 r=find('Pader','Olok HC II'); r['status']='Reported absent'; r['verification']='Field report says not constructed'; r['note']='Combined Olok HC / Latanya school report records the DHO saying Olok HC does not exist and was not constructed. Latanya school is separate.'
 review('Oyam','Iceme HC II','Original Icheme return says physical verification was not conducted. Revised return says a late-evening visit took place without photos. Supervisor to confirm which account applies.')
 review('Oyam','Alira HCII','Supervisor reports Alira does not exist, but revised Icheme narrative refers to Alira as a sibling facility. Confirm with the DHO before removing the master entry.')
 for loc,name in [('Bushenyi','Kibazi HC II'),('Sheema','Kyeihara HC II'),('Sheema','Mabaare HC II'),('Sheema MC','Kitojo HC II')]: review(loc,name,'Register heading places the named facility in Mitooma, while the master lists it here. Confirm district and facility identity before closing verification.')
 review('Gomba','Mamba HC II','Gomba/Mamba cover conflicts with an interview naming Kibiri. Confirm the correct form and checklist.')
 review('Makindye-Ssabagabo MC','Kibiri HC III','Kibiri cover/interview conflicts with a Gomba/Mamba checklist in one return. Separate Kibiri process report received; reconcile the toolkit.')
 review('Kamuli MC','Busota HC II','Busota softcopy received from Sulaina on 21 Sep at 16:47. Cover names Kamuli district; checklist and master name Kamuli MC. Confirm the LG heading.')
 for loc,name,other in [('Yumbe','Amanyiri','Ekaligo'),('Yumbe','Ladonga Seed School','Liko'),('Amolatar','Arwotchek HC II','Kyankaramata')]:
  r=review(loc,name,f'Filename or supervisor identifies this facility, but the filed form names {other}. Identity is reconciled where a chat decision exists; the verification form still needs correction.');
 # The two Team 28 process reports repeat a different site; do not infer a clean return.
 for loc,name in [('Kyegegwa','Kabweza'),('Kyenjojo','Kataraza HC II')]:
  try: review(loc,name,'Process report describes Kyankaramata rather than the named facility. Confirm the report and facility-specific evidence.')
  except ValueError: pass
 # Western attachment: Ndibarema/Nsiika is a location-based candidate, not a confirmed alias.
 r=find('Buhweju','Nsiika T/C'); r['status']='Needs review'; r['source']='_multi-team/teams-19-21/data updates - western.xls'; r['source_locator']='Sheet2!B3'; r['ground_name']='Ndibarema Memorial SSS'; r['note']='New asset sheet names Ndibarema Memorial SSS, Nsiika, Buhweju. Confirm it is the master-list Nsiika T/C school.'
 # Retain every submitted unmatched facility; confirmed substitutions consume their folder once.
 extra=[]; extra_keys=set(); inherited_register_extras=[]
 for old in baseline:
  if old['type']=='Blood bank':
   r=dict(id='B'+str(len(extra)+1).zfill(3),team=old['team'],lg=lg(old['lg']),name=old['name'],type=old['type'],scope='Allocation only',status={'Received':'Field evidence','Missing':'No return','Register only':'Field evidence'}[old['old_status']],folder=folder_from_note(old['note']),source='',note='Regional blood bank allocated in team-distributions.docx; outside the school/HC master denominator.',ground_name=old['name'],master_ids='',decision_ref='',source_locator='',verification={'Received':'Evidence received','Missing':'Not established','Register only':'Completed from consolidated register; physical inspection not certified'}[old['old_status']]); extra.append(r)
   if r['folder']: used.add(r['folder'])
  elif 'not on the programme list' in old['note'] and old['old_status']=='Register only':
   r=dict(id='X'+str(len(extra)+1).zfill(3),team=old['team'],lg=lg(old['lg']),name=old['name'],type=old['type'],scope='Ground return only',status='Field evidence',folder='',source=register_path(old),note='Named in submitted register; no confirmed master match.',ground_name=old['name'],master_ids='',decision_ref='',source_locator='',verification='Completed from consolidated register; physical inspection not certified');
   reg=registry[identity(old)]; r['source_locator']=reg['sheet']+'!row '+str(reg['row']); r['note']+=' Asset section: '+reg['evidence_heading']; extra.append(r); extra_keys.add(identity(r)); inherited_register_extras.append((r,r['source_locator']))
 for path in sorted(set(folder_keys.values())-used):
  parts=path.split('/'); name=parts[2].replace('-',' '); typ='School' if 'school' in name.lower() else 'Health centre'
  r=dict(id='X'+str(len(extra)+1).zfill(3),team=int(parts[0][-2:]),lg=parts[1],name=name,type=typ,scope='Ground return only',status='Field evidence',folder=path,source='',note='Facility-specific return received; no confirmed master match.',ground_name=name,master_ids='',decision_ref='',source_locator='',verification='Verification records received; physical completion not certified')
  if identity(r) not in extra_keys: extra.append(r); extra_keys.add(identity(r))
 for r in extra:
  if 'Onywako' in r['name']:
   r['status']='Not verified'; r['verification']='Physical verification explicitly not performed'; r['note']='Form states that assets were reported by the in-charge and were not physically verified. Chat names Onywako on ground, but gives no one-to-one replacement for Alik.'; r['decision_ref']='CHAT11'
  if 'Kabushaho' in r['name']:
   r['lg']='Bushenyi'; r['note']='Workbook is filed under Mitooma, but its facility heading explicitly says Bushenyi. No exact master-list school match.'
 for name,location,team,sheet,note in [('Ndibarema Memorial SSS','Buhweju',20,'Sheet2!B3','Candidate for Nsiika T/C master school; linkage awaits confirmation. Not counted as an additional confirmed site.'),('Rutooma HC III','Mbarara',21,'Sheet5!B2','New register heading says Mbarara without district/city distinction. It does not resolve the missing Rutooma in Bushenyi.')]:
  if not any(key(r['name'])==key(name) and r['lg']==location for r in extra): extra.append(dict(id='X'+str(len(extra)+1).zfill(3),team=team,lg=location,name=name,type='School' if 'SSS' in name else 'Health centre',scope='Ground return only',status='Needs review',folder='',source='_multi-team/teams-19-21/data updates - western.xls',source_locator=sheet,note=note,ground_name=name,master_ids='',decision_ref='',verification='Asset rows received; identity requires confirmation'))
 # Ground names with unresolved identity remain visible without asserting another physical site.
 extra.append(dict(id='X'+str(len(extra)+1).zfill(3),team=25,lg='Kagadi',name='Muggi HC III',type='Health centre',scope='Ground return only',status='Needs review',folder='',source='_multi-team/bunyoro-tooro-greater-mityana/DEPAUL - BUNYORO, TOORO AND GREATER MITYANA -CURRENT.xls',source_locator='UGIFT HEALTH!row 8363',note='Register says Kagadi; master Muggi is in Mayuge. Confirm the source LG. This is an unresolved return identity, not a confirmed additional Kagadi facility.',ground_name='Muggi HC III',master_ids='',decision_ref='',verification='Asset rows received; district identity requires confirmation'))
 extra.append(dict(id='X'+str(len(extra)+1).zfill(3),team=5,lg='Oyam',name='Abeja HC III',type='Health centre',scope='Ground name only',status='Needs review',folder='',source='',source_locator='',note='Denis Budali names Abeja on ground. The master and filed return say Abela. Confirm the spelling; no separate Abeja return or one-to-one replacement is established.',ground_name='Abeja HC III',master_ids='',decision_ref='CHAT10',verification='Supervisor-reported name only; identity unconfirmed'))
 # New Mayanga rows supplement its original register evidence.
 mayanga=find('Mitooma','Mayanga HC II'); mayanga.setdefault('supplemental_sources',[]).append('_multi-team/teams-19-21/data updates - western.xls'); mayanga.setdefault('supplemental_locators',[]).append('Sheet3!B3'); mayanga['note']+=' New western update also has Mayanga asset rows (Sheet3!B3).'
 for r in records+extra:
  if r.get('decision_ref'):
   r.setdefault('supplemental_sources',[]).append('_multi-team/programme-documents/data-management-chat/WhatsApp Chat with DATA MANAGEMENT UGIFT.txt')
   r.setdefault('supplemental_locators',[]).append(r['decision_ref'])
 # Select a usable, facility-specific evidence file; index supplies all source versions.
 for r in records+extra:
  if r.get('folder'):
   files=[p for p in all_files if p.startswith(r['folder']+'/') and '/_reconciliation-evidence/' not in p and not Path(p).name.startswith('~$')]
   order={'.docx':0,'.pdf':1,'.xlsx':2,'.xls':3,'.jpg':4,'.jpeg':4,'.png':4}
   files.sort(key=lambda p:(order.get(Path(p).suffix.lower(),9),p))
   if files: r['source']=files[0]
  if r['status']=='Field evidence' and not r['source']: raise ValueError('Missing evidence source '+str(r))
  r['supervisor']=re.sub(r'[/\d].*','',teams[str(r['team'])]['supervisor']).strip()
  r['additional_sources']='; '.join(r.get('supplemental_sources',[])); r['additional_locators']='; '.join(r.get('supplemental_locators',[]))
  r['master_source']=MASTER if r['scope']=='Master list' else ''
  r['field_name']=r['ground_name'] or r['name']
  r['note']=r['note'].replace('possibly the team\'s folder','Unconfirmed possible match:').replace('not on the programme list','No confirmed master match')
 records.sort(key=lambda r:(r['team'],r['lg'],r['type'],r['name']))
 extra.sort(key=lambda r:(r['team'],r['lg'],r['name']))
 # Guard the reviewed exceptions against future matching or output regressions.
 sop_sop=find('Tororo','Sop Sop HC II')
 assert sop_sop['folder'].endswith('/Sop-Sop-HC-III'), sop_sop
 assert not [r for r in extra if key(r['lg'])==key('Tororo') and r['type']=='Health centre' and key(r['name']).startswith(key('Sop Sop'))]
 mayanga_supplements=dict(zip(mayanga.get('supplemental_sources',[]),mayanga.get('supplemental_locators',[])))
 assert mayanga_supplements.get('_multi-team/teams-19-21/data updates - western.xls')=='Sheet3!B3', mayanga_supplements
 abeja=[r for r in extra if r['scope']=='Ground name only' and key(r['lg'])==key('Oyam') and key(r['name'])==key('Abeja HC III')]
 assert len(abeja)==1 and abeja[0]['decision_ref']=='CHAT10' and abeja[0]['status']=='Needs review', abeja
 for ref,loc,name,folder in [('CHAT12','Jinja','Butagaya','Buwala-Seed-Secondary-School'),('CHAT13','Namayingo','Mwema Seed School','Mutumba-Seed-Secondary-School')]:
  resolved=find(loc,name)
  assert resolved['decision_ref']==ref and resolved['status']=='Field evidence', resolved
  assert resolved['folder'].endswith('/'+folder), resolved
 pandwong=find('Kitgum MC','Pandwong HC II')
 assert pandwong['status']=='No UgIFT assets' and pandwong['verification']=='Facility exists; supervisor reports no UgIFT assets', pandwong
 assert len(inherited_register_extras)==8, len(inherited_register_extras)
 assert all(r['source_locator']==locator and locator for r,locator in inherited_register_extras), inherited_register_extras
 assert not [r for r in records+extra if r['status']=='Register only'], 'Register-only status must be represented as Field evidence with a consolidated-register verification basis'
 consolidated=[r for r in records if r['verification']=='Completed from consolidated register; physical inspection not certified']
 assert len(consolidated)==42, len(consolidated)
 assert len([r['folder'] for r in records if r['folder']])==len({r['folder'] for r in records if r['folder']}), 'Two distinct master facilities share one folder'
 assert len(records)==629, len(records)
 assert sum(len(r['master_ids'].split('; ')) for r in records)==632
 assert len({r['id'] for r in records+extra})==len(records+extra)
 missing_sources=[r['source'] for r in records+extra if r['source'] and not (GROUPED/r['source']).is_file()]
 assert not missing_sources,missing_sources
 fields=['id','scope','team','supervisor','lg','type','name','field_name','status','verification','master_ids','master_lg','phase','project_status','decision_ref','source','source_locator','additional_sources','additional_locators','folder','note','master_source','source_row']
 write_csv(GROUPED/'facility-reconciliation.csv',records+extra,fields)
 write_csv(GROUPED/'master-source-rows.csv',masters,['id','lg','type','name','phase','project_status','source_row'])
 write_csv(GROUPED/'master-duplicate-rows.csv',duplicates,['duplicate','retained','lg','name'])
 source_rows=[]
 for r in records+extra:
  evidence=[e for e in index if (r.get('folder') and e['destination (in raw-data-grouped)'].startswith(r['folder']+'/')) or (r['source'] and e['destination (in raw-data-grouped)']==r['source']) or e['destination (in raw-data-grouped)'] in r.get('supplemental_sources',[])]
  for e in evidence:
   source_rows.append(dict(source_locator=(r.get('source_locator','') if e['destination (in raw-data-grouped)']==r['source'] else dict(zip(r.get('supplemental_sources',[]),r.get('supplemental_locators',[]))).get(e['destination (in raw-data-grouped)'],'')),facility_id=r['id'],team=r['team'],lg=r['lg'],facility=r['name'],source_root=e.get('source root','raw-data-ungrouped') or 'raw-data-ungrouped',source=e['source (in raw-data-ungrouped)'],destination=e['destination (in raw-data-grouped)'],status=e['status'],note=e['note'],sha256=e.get('sha256','')))
 write_csv(GROUPED/'facility-evidence-index.csv',source_rows,['facility_id','team','lg','facility','source_root','source','destination','source_locator','status','note','sha256'])
 write_csv(GROUPED/'supervisor-decisions.csv',[dict(d,master_names='; '.join(d.get('master_names',[d.get('master_name','')])),ground_names='; '.join(d.get('ground_names',[d.get('ground_name') or '']))) for d in chat['decisions']],['id','date_time','speaker','team','lg','master_names','ground_names','decision','quote','explicit','note'])
 payload=dict(master_rows=632,master_facilities=629,counts=dict(Counter(r['status'] for r in records)),extra_counts=dict(Counter(r['scope'] for r in extra)),records=records,extras=extra,duplicates=duplicates,teams=teams,decisions=chat)
 (TMP/'reconciled.json').write_text(json.dumps(payload,indent=2),encoding='utf-8')
 print(json.dumps({k:v for k,v in payload.items() if k not in ['records','extras','teams','decisions']},indent=2))
if __name__=='__main__': main()
