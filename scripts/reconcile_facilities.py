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
LATEST_WESTERN='_multi-team/bunyoro-tooro-greater-mityana/DEPAUL - BUNYORO, TOORO AND GREATER MITYANA -CURRENT (2).xls'
LATEST_LWAMATA='team-29/Kiboga/Lwamata-Town-Council-Seed-Secondary-School/UGIFT ASSET VERIFICATION LWAMATA T.C.C SEED SEC SCH (1).docx'
LATEST_SOFIA='team-13/Busia MC/Sofia-Health-Centre-III/Sofia health centre 111 eastern division busia MC.pdf'
LATEST_CHAT='_multi-team/programme-documents/data-management-chat/WhatsApp Chat with DATA MANAGEMENT UGIFT (3).txt'
NS={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
def clean(value): return re.sub(r'\s+',' ',str(value)).strip()
def key(value): return re.sub(r'[^a-z0-9]','',value.lower())
LG_ALIASES={'fortportal':'Fort-Portal City','kassanda':'Kasanda','luwero':'Luweero','rakia':'Rakai','liramc':'Lira City','masakamc':'Masaka City','ssabagabomakindyemc':'Makindye-Ssabagabo MC','jinjamc':'Jinja City','mbararamc':'Mbarara City','sheemamunicipalcouncil':'Sheema MC','hoimamc':'Hoima City','kasesemunicipalcouncil':'Kasese MC'}
def lg(value): return LG_ALIASES.get(key(value),value.replace(' Mc',' MC'))
def identity(r): return (key(lg(r['lg'])),r['type'],key(r['name']))

def title_name(value):
 value=clean(value).strip(' .,-')
 return ' '.join(word if any(ch.islower() for ch in word[1:]) else word.title() for word in value.split())

def canonical_facility_name(record):
 """Return the programme-standard field name without altering the master label."""
 explicit_names={
  'S028':'Okum Seed Secondary School',
  'S050':'Kyangwali Seed Secondary School',
  'S069':'Makokoto Seed Secondary School',
  'S226':'Ryakasinga Seed Secondary School',
  'S235':'St Mugagga Vocational Seed Secondary School',
  'H027':'Mbirizi Seed Secondary School',
  'S249':'Nyakishenyi Seed Secondary School',
  'X008':'Katungunda Seed Secondary School',
 }
 if record.get('id') in explicit_names:
  return explicit_names[record['id']]
 value=clean(record.get('ground_name') or record.get('field_name') or record.get('name'))
 typ=record.get('type','')
 if typ=='School':
  value=re.sub(r'\bseed\s+senior\s+secondary\s+school\b',' ',value,flags=re.I)
  value=re.sub(r'\bseed\s+secondary\s+school\b',' ',value,flags=re.I)
  value=re.sub(r'\bseed\s+school\b',' ',value,flags=re.I)
  value=re.sub(r'\bsecondary\s+school\b',' ',value,flags=re.I)
  value=re.sub(r'\bseed\s+S{1,3}\b',' ',value,flags=re.I)
  value=re.sub(r'\bS{2,3}\b',' ',value,flags=re.I)
  value=re.sub(r'\bschool\b',' ',value,flags=re.I)
  value=title_name(re.sub(r'\s+',' ',value))
  return f'{value} Seed Secondary School'
 if typ=='Health centre':
  if re.search(r'\bhospital\b',value,re.I): return title_name(value)
  level='IV' if re.search(r'(?:\bHC\s*IV\b|\bHealth\s+Cent(?:re|er)\s*IV\b)',value,re.I) else 'III'
  value=re.sub(r'\bHealth\s+Cent(?:re|er)\s*(?:II|III|IV|2|3|4|11|111)?\b',' ',value,flags=re.I)
  value=re.sub(r'\bHC\s*(?:II|III|IV|2|3|4|11|111|LLL)?\b',' ',value,flags=re.I)
  value=title_name(re.sub(r'\s+',' ',value))
  return f'{value} Health Centre {level}'
 return title_name(value)
def read_json(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def source_path(value):
 p=Path(value)
 if p.is_absolute(): return p
 direct=ROOT/p
 return direct if direct.exists() else GROUPED/p
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
 def set_direct_return(loc,name,ground_name,source,locator,note):
  r=find(loc,name); r['ground_name']=ground_name; r['status']='Field evidence'; r['verification']='Verification records received; physical completion not certified'; r['source']=source; r['source_locator']=locator; r['note']=note; return r
 set_direct_return('Kiboga','Lwamata Town Council','Lwamata Town Council Seed Secondary School',LATEST_LWAMATA,'Tables 5 and 7','New school return identifies Lwamata Town Council Seed Secondary School in Kiboga District.')
 for loc,name,ground,locator in [
  ('Kyankwanzi','Kikolimbo HC II','Kikolimbo Health Centre III','UGIFT HEALTH 2!rows 1749-2019'),
  ('Kyankwanzi','Kikooma','Kikooma Health Centre III','UGIFT HEALTH 2!rows 2022-2306'),
  ('Kakumiro','Kikwaya','Kikwaya Health Centre III','UGIFT HEALTH 2!rows 2309-2592'),
  ('Kakumiro','Masaka HC II','Masaka Health Centre III','UGIFT HEALTH 2!rows 2593-2880'),
 ]:
  set_direct_return(loc,name,ground,LATEST_WESTERN,locator,'The 22 September consolidated health update supplies asset rows for this upgraded Health Centre III.')
 team30_root='team-30/_team-documents'
 for loc,name,ground,filename,locator in [
  ('Kasanda','Kijuna','Kijuna Health Centre III','KIJUNA HCIII UGIFT Asset Verification - FINAL.docx','Health-centre interview and checklist'),
  ('Kasanda','Kikandwa HC II','Kikandwa Health Centre III','KIKANDWA HCIII UGIFT Asset Verification Tool Kit - FINAL.docx','Health-centre interview and checklist'),
  ('Kasanda','Kyasansuwa HC II','Kyasansuwa Health Centre III','Kyasansuwa HCIII UGIFT Asset Verification Tool Kit - FINAL.docx','Health-centre interview and checklist'),
  ('Kasanda','Makokoto HC II','Makokoto Health Centre III','MAKOKOTO SEED SCHOOL UGIFT ASSET VERIFICATION TOOLKIT - FINAL - 1.docx','Health-centre section'),
  ('Kasanda','Makokoto (New facilities at Makokoto Seed S.S.)','Makokoto Seed Secondary School','MAKOKOTO SEED SCHOOL UGIFT ASSET VERIFICATION TOOLKIT - FINAL - 1.docx','School interview and checklist'),
  ('Kibaale','Matale HC II','Matale Health Centre III','MATALE HCIII UGIFT Asset Verification Tool Kit - Final.docx','Health-centre interview and checklist'),
  ('Kibaale','Mugarama( new facilities for St Mugagga S.S)','St Mugagga Seed Secondary School','ST MUGAGA VOCATIONAL SEEED SCHOOL UGIFT Asset Verification Tool Kit Updated.docx','School interview and checklist'),
  ('Kibaale','Nyamarwa Seed School','Nyamarwa Seed Secondary School','NYAMARWA SEED SCHOOL UGIFT ASSET VERIFICATION AND RECORDING TOOL KIT - FINAL.docx','School interview and checklist'),
 ]:
  set_direct_return(
   loc,name,ground,f'{team30_root}/{filename}',locator,
   'Team 30 facility-specific return confirms the local government, facility identity and completed asset checklist.'
  )
 st_mugagga=find('Kibaale','Mugarama( new facilities for St Mugagga S.S)')
 st_mugagga['status']='Field evidence'
 st_mugagga['verification']='Visit recorded; asset source documents were not accessible and the asset rows were not completed'
 st_mugagga['note']='The 23 September message and updated toolkit record the school as St Mugagga Vocational Seed School. The toolkit says the asset source documents could not be accessed, several areas were locked, and the school had not been commissioned. Photographs were taken with school representatives.'
 mugagga_folder='team-30/Kibaale/St-Mugagga-Vocational-Seed-Secondary-School'
 if (GROUPED/mugagga_folder).is_dir():
  st_mugagga['folder']=mugagga_folder; used.add(mugagga_folder); st_mugagga['ground_name']='St Mugagga Vocational Seed Secondary School'
 for loc,name,ground,source,locator,note in [
  ('Buliisa','Butiaba HC II','Butiaba Health Centre III','team-25/_team-documents/BUTAIBA HEALTH CENTER III.docx','Health-centre checklist','The facility toolkit and visit report confirm Team 25 verified Butiaba Health Centre III.'),
  ('Kagadi','Kyabasara HC II','Kyabasara Health Centre III','team-25/_team-documents/KYABASARA HEALTH CENTER III.docx','Health-centre checklist','The facility-specific Team 25 toolkit confirms Kyabasara Health Centre III.'),
  ('Ntoroko','Bweramule HC II','Bweramule Health Centre III','team-26/_team-documents/NTOROKO LG  ASST.VERIFICATION REPORT_105758 (1) (1).docx','Health-centre checklist','The Ntoroko toolkit explicitly identifies and records Bweramule Health Centre III.'),
  ('Kyankwanzi','Sirimula HC II','Sirimula Health Centre III','team-29/_team-documents/UGIFT SIRIMULA.docx','Health-centre checklist','The Team 29 facility toolkit confirms Sirimula Health Centre III.'),
 ]:
  set_direct_return(loc,name,ground,source,locator,note)
 aliases={'CHAT01':'Pangira-HC-III','CHAT05':'Akadot-Seed-Secondary-School','CHAT06':'Mpiita-Seed-Secondary-School','CHAT09':'Kangole-HC-III','CHAT18':'Buwumba-HC-III'}
 for dec in chat['decisions']:
  if not dec.get('master_name') and not dec.get('master_names'):
   continue
  names=dec.get('master_names',[dec.get('master_name')])
  for name in names:
   r=find(dec.get('master_lg',dec['lg']),name); r['decision_ref']=dec['id']; r['note']=dec['decision']+'. '+dec['note']
   return_folder=dec.get('return_folder') or aliases.get(dec['id'])
   if return_folder:
    set_folder(r,return_folder)
    if dec.get('ground_name'): r['ground_name']=dec['ground_name']
    r['note']=dec.get('evidence_note',dec['decision']+'. '+dec['note'])
    if dec.get('resolved_status') and r['status']!=dec['resolved_status']:
     raise ValueError(f"Supervisor decision {dec['id']} expected {dec['resolved_status']}, got {r['status']}")
   elif dec['id']=='CHAT04': r['status']='Replaced'; r['ground_name']='Liko HC III'; r['verification']='Already-listed replacement; no second verified facility'; r['note']='Loinya was replaced by Liko, which already has master entry H212. Count Liko once.'
   elif dec['id'] in ['CHAT03','CHAT10','CHAT11']: r['status']='Reported absent'; r['verification']='Reported not known/not found; not independently established'
   elif dec['id']=='CHAT02':
    r['status']='No UgIFT assets'; r['verification']='Facility exists; supervisor reports no UgIFT assets'; r['note']='The supervisor confirms that Pandwong exists but did not receive UgIFT assets. It is therefore excluded from the missing-return count.'
   elif dec['id']=='CHAT14':
    r['status']='Outside UgIFT'; r['verification']='Reported outside UgIFT; not verified; facility type wording requires confirmation'; r['note']='The supervisor says Buyinda was not verified because it was outside UgIFT. The message alternates between health centre and seed school, while the master contains Buyinda HC II; retain that facility-type caveat.'
   elif dec['id'] in ['CHAT15A','CHAT15B','CHAT15C','CHAT15D','CHAT15E']:
    r['lg']=lg(dec['lg']); r['ground_name']=dec['ground_name']; r['status']='Field evidence'; r['verification']='Asset rows received; local government and facility identity confirmed'
   elif dec['id']=='CHAT16':
    r['ground_name']=dec['ground_name']; r['status']='Field evidence'; r['verification']='Asset rows received; renamed facility confirmed'; r['source']='_multi-team/teams-19-21/data updates - western.xls'; r['source_locator']='Sheet2!B3'
   elif dec['id']=='CHAT17':
    if key(name)==key('Alira HCII'):
     r['status']='Outside UgIFT'; r['verification']='Facility exists but is outside the upgraded UgIFT set'
    else:
     r['status']='Reported absent'; r['verification']='Reported not to exist; not independently established'
   elif dec['id'] in ['CHAT19','CHAT20','USER01']:
    r['status']='Reported absent'; r['verification']='Reported not to exist; programme data-management decision'
   elif dec['id']=='USER02':
    r['status']='Field evidence'
    if key(name)==key('Amanyiri'):
     r['ground_name']='Amanyiri Health Centre III'; r['verification']='Asset schedule explicitly identifies Amanyiri Health Centre III'
     r['note']='Amanyiri is an independent Yumbe facility. Its asset schedule repeatedly identifies Amanyiri Health Centre III; the Ekaligo interview heading belongs to a separate facility.'
    else:
     r['ground_name']='Lodonga Seed Secondary School'; r['verification']='School asset schedules explicitly identify Lodonga Seed Secondary School'
     r['note']='Lodonga is an independent Yumbe school. Its furniture, ICT and building schedules identify Lodonga Seed Secondary School; the Liko health-centre interview belongs to a separate facility.'
   elif dec['id'] in {'CHAT23','CHAT24','CHAT25','CHAT26','CHAT28','CHAT29'}:
    r['status']='Field evidence'; r['verification']='Completed from consolidated register; physical inspection not certified'; r['note']=dec['note']
   elif dec['id']=='CHAT32A':
    r['status']='Field evidence'; r['verification']='Verification records received; physical completion not certified'; r['ground_name']=dec['ground_name']; r['source']='team-27/_team-documents/RUBONA_HCIII_&_KATUGUNDA_SEED(_BUNYANGABU)[1].docx'; r['source_locator']='School section'; r['note']=dec['note']
   elif dec['id']=='CHAT32B':
    r['status']='Field evidence'; r['verification']='Verification records received; physical completion not certified'; r['ground_name']=dec['ground_name']; r['source']='team-27/_team-documents/NSUURA SEED SCHOOL.docx'; r['source_locator']='School interview and checklist'; r['note']=dec['note']
   elif dec['id']=='CHAT33':
    r['status']='Needs review'; r['verification']='Rename stated without a local government; the two master rows are in different districts'; r['note']=dec['note']
   elif dec['id']=='CHAT34':
    r['status']='Field evidence'; r['verification']='Asset rows received; supervisor confirms Bushenyi District'; r['ground_name']=dec['ground_name']; r['source']='_multi-team/teams-19-21/data updates - western.xls'; r['source_locator']='Sheet5!B2'; r['note']=dec['note']
   elif dec['id']=='CHAT07':
    r['status']='Field evidence'; r['ground_name']='Kagwara Seed Secondary School'; r['source']=next(p for p in all_files if 'team-08' in p and 'SCHOOL' in p.upper() and p.endswith('.xlsx')); r['source_locator']='Sheet1!row 1598'; r['verification']='Completed from consolidated register; physical inspection not certified'; r['note']+=' Register uses Kagawa; chat confirms Kagwara in Kadungulu.'
   elif dec['id']=='CHAT08': r['note']+=' Existing Ndwaddemutwe evidence retained.'
 absence_reasons={
  ('CHAT03',key('Lodonga TC')):'The supervisor reports that Lodonga TC is not known to Yumbe District. This is a reported absence, not independent proof that the facility does not exist.',
  ('CHAT10',key('Acimi HC II')):'The supervisor explicitly reports that Acimi does not exist in Oyam. The six ground names supplied in the same message are not paired one-to-one with Acimi.',
  ('CHAT10',key('Acokara HCII')):'The supervisor explicitly reports that Acokara (written Achokara in the chat) does not exist in Oyam. The six ground names supplied are not paired one-to-one with this entry.',
  ('CHAT10',key('Ariba HC II')):'The supervisor explicitly reports that Ariba does not exist in Oyam. The six ground names supplied in the same message are not paired one-to-one with Ariba.',
  ('CHAT11',key('Alik HCII')):'The supervisor explicitly reports that Alik does not exist in Lira. Barlonyo and Onywako are named on the ground, but neither is identified as a one-to-one replacement for Alik; the Onywako return also says physical verification was not performed.',
  ('CHAT17',key('Acimi HC II')):'The revised Oyam decision confirms that Acimi is not among the six upgraded UgIFT Health Centre IIIs and retains the earlier report that it does not exist.',
  ('CHAT17',key('Acokara HCII')):'The revised Oyam decision confirms that Acokara is not among the six upgraded UgIFT Health Centre IIIs and retains the earlier report that it does not exist.',
  ('CHAT17',key('Alira HCII')):'The revised Oyam decision confirms that Alira exists, but it is outside the facilities upgraded under UgIFT.',
  ('CHAT17',key('Ariba HC II')):'The revised Oyam decision confirms that Ariba is not among the six upgraded UgIFT Health Centre IIIs and retains the earlier report that it does not exist.',
  ('USER01',key('Central Division')):'The programme data manager confirms that Central Division Seed Secondary School does not exist in Jinja City. Preserve the master row for audit and do not infer a replacement facility.',
 }
 for r in records:
  reason=absence_reasons.get((r['decision_ref'],key(r['name'])))
  if reason: r['note']=reason
 def review(loc,name,note):
  r=find(loc,name); r['status']='Needs review'; r['verification']='Physical verification not confirmed because returns conflict'; r['note']=note; return r
 def review_source(loc,name,note,source,locator='Facility-specific return'):
  r=review(loc,name,note); r['source']=source; r['source_locator']=locator; return r
 def explained_relocation(loc,name,status,replacement,note,source,ref):
  r=find(loc,name); r['status']=status; r['verification']='Supervisor-confirmed asset relocation/replacement; field evidence is counted under the receiving facility'; r['note']=note; r['source']=source; r['source_locator']='Supervisor message 23 September 2026 09:36'; r['ground_name']=''; r['decision_ref']=ref; return r
 r=find('Pader','Olok HC II'); r['status']='Reported absent'; r['verification']='Field report says not constructed'; r['note']='Combined Olok HC / Latanya school report records the DHO saying Olok HC does not exist and was not constructed. Latanya school is separate.'
 # Resolved from the filed toolkits and the 23 September chat. The governing document is set after the folder file picker.
 explained_relocation(
  'Nebbi','Oweko HC II','Replaced','Pamaka Health Centre III',
  'Supervisor confirms that Oweko was replaced by Pamaka Health Centre III. The Pamaka return is retained as the receiving-facility evidence.',
  'team-01/Nebbi/Pamaka-HC-III/NEBBI-PAMAKA HC & NDHEW SEED 2.docx','CHAT21D')
 explained_relocation(
  'Zombo','Alangi','No UgIFT assets','Amwonyo Health Centre III',
  'Supervisor confirms that Alangi exists, but its UgIFT assets were relocated to Amwonyo Health Centre III. Evidence is counted under Amwonyo.',
  'team-01/Zombo/Amwonyo-HC-III/ZOMBO AMWONYO & WADELAI 2.docx','CHAT21A')
 explained_relocation(
  'Zombo','Ther-uru HC II','No UgIFT assets','Atyak Health Centre III',
  'Supervisor confirms that Ther-uru exists, but its UgIFT assets were relocated to Atyak Health Centre III. Evidence is counted under Atyak.',
  'team-01/Zombo/Atyak-HC-III/ZOMBO - ATYAK HC III & ALWI SEED.docx','CHAT21B')
 explained_relocation(
  'Zombo','Abanga','No UgIFT assets','Kango Seed Secondary School',
  'Supervisor confirms that Abanga Seed Secondary School exists, but its UgIFT assets were relocated to Kango Seed Secondary School. Evidence is counted under Kango.',
  'team-01/Zombo/Kango-Seed-Secondary-School/ZOMBO - NWOYA PARAA HC & KANGO SEED ZOMBO.docx','CHAT21C')
 # A submitted ground return or a documented access/identity problem is
 # coverage, but remains Needs review until the master-to-ground link or visit
 # is confirmed. This prevents genuine team work from being scored as absent.
 for loc,name,note,source in [
  ('Bundibugyo','Kyondo HC II','Depaul confirmed on 23 September 2026 that Kyondo HC III could not be visited because the CAO said the mountainous road was dangerous.','team-26/_team-documents/Team_26_Bundibugyo_UgIFT_Field_Verification_Report_Final.docx'),
  ('Kasese','Kabingo HCII','Depaul confirmed on 23 September 2026 that the Kabingo information was obtained by phone because the team could not reach the facility. Physical verification stays unconfirmed.','team-27/_team-documents/KABINGO HCIII.docx'),
 ]:
  review_source(loc,name,note,source)
 # Same local government, one open master name and one submitted name that is not on the master list.
 for loc,name,folder,ground,note in [
  ('Rukungiri','Nyakishenyi (New facilities at Nyakishenyi H.S.)','Bikurungu-Seed-Secondary-School','Bikurungu Seed Secondary School','Gumisiriza Johnson team 23 submitted Bikurungu Seed Secondary School in Rukungiri. It is the submitted name for the master-list Nyakishenyi entry.'),
  ('Bundibugyo','Mantoroba HC II','Busanga-HC-III','Busanga Health Centre III','Depaul team 26 submitted Busanga Health Centre III in Bundibugyo. It is the submitted name for the master-list Mantoroba entry.'),
  ('Kabarole','Nyabuswa HC II','Nyambuusa-HC-III','Nyambuusa Health Centre III','Depaul team 26 submitted Nyambuusa Health Centre III. That spelling is the submitted name for the master-list Nyabuswa entry.'),
  ('Kabarole','Kidubuli HC II','Iruhura-HC-III','Iruhura Health Centre III','Depaul team 26 submitted Iruhura Health Centre III in Kabarole. It is the remaining submitted health-centre name for the master-list Kidubuli entry.'),
  ('Mubende','Kabbo','Nakawala-HC-III','Nakawala Health Centre III','Depaul team 28 submitted Nakawala Health Centre III in Mubende. It is the submitted name for the master-list Kabbo entry.'),
  ('Mpigi','Kiringente Seed School','Wamatovu-Seed-Secondary-School','Wamatovu Seed Secondary School','Lawrence team 32 submitted Wamatovu Seed Secondary School in Mpigi. It is the submitted name for the master-list Kiringente entry.'),
  ('Lyantonde','Mpumudde seed school','Rwamabara-Seed-Secondary-School','Rwamabara Seed Secondary School','Lawrence team 33 submitted Rwamabara Seed Secondary School in Lyantonde. It is the submitted name for the master-list Mpumudde entry.'),
 ]:
  r=find(loc,name)
  set_folder(r,folder)
  r['ground_name']=ground
  r['note']=note
  r['verification']='Verification records received; physical completion not certified'
  r['decision_ref']=r.get('decision_ref') or 'NAME'
 for loc,name,verification,note in [
  ('Bundibugyo','Kyondo HC II','Visit not undertaken; the CAO confirmed the road was unsafe','Depaul confirmed on 23 September 2026 that Kyondo HC III could not be visited because the CAO said the mountainous road was dangerous.'),
  ('Kasese','Kabingo HCII','Information obtained by phone; physical verification not performed','Depaul confirmed on 23 September 2026 that the Kabingo information was obtained by phone because the team could not reach the facility. Physical verification stays unconfirmed.'),
 ]:
  r=find(loc,name); r['status']='Not verified'; r['verification']=verification; r['note']=note
 find('Bundibugyo','Kyondo HC II')['decision_ref']='CHAT31'
 find('Kasese','Kabingo HCII')['decision_ref']='CHAT27'
 review('Nakaseke','Ngoma','Sulaina said Ngoma Seed School was changed to Budongo Seed School, but did not name the local government. Master Ngoma is in Nakaseke and master Budongo is in Masindi, so the rows stay separate until the district is confirmed.')
 kagganda=find('Lwengo','Kagganda HC II')
 set_folder(kagganda,'Mbirizi-Seed-Secondary-School')
 kagganda['ground_name']='Mbirizi Seed Secondary School'
 kagganda['decision_ref']='CHAT40'
 kagganda['verification']='Verification records received; physical completion not certified'
 kagganda['note']='Lawrence says the Lwengo entry recorded as Kagganda is Mbirizi Seed School. The master classifies the row as a health centre; the return and the supervisor identify the school. The Mbirizi return is counted once on this row.'
 lwengo_school=find('Lwengo','Lwengo Seed School')
 lwengo_school['status']='No return'; lwengo_school['verification']='Not established'; lwengo_school['folder']=''; lwengo_school['source']=''; lwengo_school['ground_name']=''
 lwengo_school['note']='The Mbirizi Seed School return is the supervisor-confirmed Kagganda entry, not this Lwengo Seed School row.'
 for r in records:
  if r['status']=='No return' and key(r.get('project_status',''))=='ongoing':
   r['status']='Needs review'
   r['verification']='Master records the project as ongoing; operational asset eligibility and commissioning require confirmation'
   r['note']='No completed asset return is on file. The master records this project as ongoing, so the facility is treated as a documented eligibility/commissioning follow-up rather than an unexplained missing return.'
 # Western attachment: Ndibarema/Nsiika is a location-based candidate, not a confirmed alias.
 r=find('Buhweju','Nsiika T/C'); r['status']='Field evidence'; r['verification']='Asset rows received; renamed facility confirmed'; r['source']='_multi-team/teams-19-21/data updates - western.xls'; r['source_locator']='Sheet2!B3'; r['ground_name']='Ndibarema Memorial Seed Secondary School'; r['note']='Supervisor confirms that master-list Nsiika T/C is now named Ndibarema Memorial Seed Secondary School.'
 # Retain every submitted unmatched facility; confirmed substitutions consume their folder once.
 extra=[]; extra_keys=set(); inherited_register_extras=[]
 for old in baseline:
  if old['type']=='Blood bank':
   r=dict(id='B'+str(len(extra)+1).zfill(3),team=old['team'],lg=lg(old['lg']),name=old['name'],type=old['type'],scope='Allocation only',status={'Received':'Field evidence','Missing':'No return','Register only':'Field evidence'}[old['old_status']],folder=folder_from_note(old['note']),source='',note='Regional blood bank allocated in team-distributions.docx; outside the school/HC master denominator.',ground_name=old['name'],master_ids='',decision_ref='',source_locator='',verification={'Received':'Evidence received','Missing':'Not established','Register only':'Completed from consolidated register; physical inspection not certified'}[old['old_status']]); extra.append(r)
   if r['folder']: used.add(r['folder'])
  elif 'not on the programme list' in old['note'] and old['old_status']=='Register only':
   r=dict(id='X'+str(len(extra)+1).zfill(3),team=old['team'],lg=lg(old['lg']),name=old['name'],type=old['type'],scope='Ground return only',status='Field evidence',folder='',source=register_path(old),note='Named in submitted register; no confirmed master match.',ground_name=old['name'],master_ids='',decision_ref='',source_locator='',verification='Completed from consolidated register; physical inspection not certified');
   reg=registry[identity(old)]; r['source_locator']=reg['sheet']+'!row '+str(reg['row']); r['note']+=' Asset section: '+reg['evidence_heading']; extra.append(r); extra_keys.add(identity(r)); inherited_register_extras.append((r,r['source_locator']))
 for r in extra:
  if r['type']=='Blood bank' and key(r['name'])==key('Hoima Regional Blood Bank'):
   folder='team-25/Hoima City/Hoima-Regional-Blood-Bank'
   if (GROUPED/folder).is_dir():
    r['folder']=folder; r['status']='Field evidence'; r['verification']='Team 25 inventory and photographs received'; r['note']='Hoima Regional Blood Bank inventory and photographs were supplied in the 23 September Team 25 health archive.'; used.add(folder)
 for path in sorted(set(folder_keys.values())-used):
  parts=path.split('/'); name=parts[2].replace('-',' '); typ='School' if 'school' in name.lower() else 'Health centre'
  r=dict(id='X'+str(len(extra)+1).zfill(3),team=int(parts[0][-2:]),lg=parts[1],name=name,type=typ,scope='Ground return only',status='Field evidence',folder=path,source='',note='Facility-specific return received; no confirmed master match.',ground_name=name,master_ids='',decision_ref='',source_locator='',verification='Verification records received; physical completion not certified')
  if identity(r) not in extra_keys: extra.append(r); extra_keys.add(identity(r))
 for r in extra:
  if 'Onywako' in r['name']:
   r['status']='Not verified'; r['verification']='Physical verification explicitly not performed'; r['note']='Form states that assets were reported by the in-charge and were not physically verified. Chat names Onywako on ground, but gives no one-to-one replacement for Alik.'; r['decision_ref']='CHAT11'
  if 'Kabushaho' in r['name']:
   r['lg']='Bushenyi'; r['note']='Workbook is filed under Mitooma, but its facility heading explicitly says Bushenyi. No exact master-list school match.'
 for name,location,team,sheet,note in [('Rutooma HC III','Mbarara',21,'Sheet5!B2','The workbook heading says Mbarara. Supervisor Gumisiriza confirmed on 23 September 2026 that Rutooma HC III is in Bushenyi District, so these rows are the same evidence as master H239.')]:
  if not any(key(r['name'])==key(name) and r['lg']==location for r in extra): extra.append(dict(id='X'+str(len(extra)+1).zfill(3),team=team,lg=location,name=name,type='School' if 'SSS' in name else 'Health centre',scope='Linked receiving facility',status='Field evidence',folder='',source='_multi-team/teams-19-21/data updates - western.xls',source_locator=sheet,note=note,ground_name=name,master_ids='H239',decision_ref='CHAT34',verification='Asset rows received; supervisor confirms Bushenyi District'))
 # Ground names with unresolved identity remain visible without asserting another physical site.
 extra.append(dict(id='X'+str(len(extra)+1).zfill(3),team=25,lg='Kagadi',name='Muggi HC III',type='Health centre',scope='Ground return only',status='Needs review',folder='',source='_multi-team/bunyoro-tooro-greater-mityana/DEPAUL - BUNYORO, TOORO AND GREATER MITYANA -CURRENT.xls',source_locator='UGIFT HEALTH!row 8363',note='Register says Kagadi; master Muggi is in Mayuge. A 23 September form packed in the Kyabasara folder also names Miggi/Muggi and Kagadi. It is filed under team-25/Kagadi/_district-documents and does not resolve the Mayuge master row.',ground_name='Muggi HC III',master_ids='',decision_ref='',verification='Asset rows received; district identity requires confirmation'))
 kabonero=find('Bunyangabu','Kabonero')
 for r in extra:
  if key(r['name'])==key('Katungunda (school)'):
   r['scope']='Linked receiving facility'; r['master_ids']=kabonero['id']; r['decision_ref']='CHAT32A'; r['note']='Kabonero is the town council where Katugunda Seed Secondary School is located. This register evidence is counted once, under master '+kabonero['id']+'.'
 sofia_candidates=[r for r in extra if key(r['lg'])==key('Busia MC') and key(r['name'])==key('Sofia Health Centre III')]
 if sofia_candidates:
  sofia=sofia_candidates[0]
  extra=[r for r in extra if r is sofia or not (key(r['lg'])==key('Busia MC') and key(r['name'])==key('Sofia Health Centre III'))]
  sofia.update(id='X900',team=13,lg='Busia MC',name='Sofia Health Centre III',type='Health centre',scope='Ground return only',status='Field evidence',folder='team-13/Busia MC/Sofia-Health-Centre-III',source=LATEST_SOFIA,source_locator='Pages 1-20',note='Facility-specific return identifies Sofia Health Centre III in Eastern Division, Busia Municipal Council. It is distinct from the invalid master label Busia Eastern Division.',ground_name='Sofia Health Centre III',master_ids='',decision_ref='CHAT19',verification='Verification records received; physical completion not certified')
 else:
  extra.append(dict(id='X900',team=13,lg='Busia MC',name='Sofia Health Centre III',type='Health centre',scope='Ground return only',status='Field evidence',folder='team-13/Busia MC/Sofia-Health-Centre-III',source=LATEST_SOFIA,source_locator='Pages 1-20',note='Facility-specific return identifies Sofia Health Centre III in Eastern Division, Busia Municipal Council. It is distinct from the invalid master label Busia Eastern Division.',ground_name='Sofia Health Centre III',master_ids='',decision_ref='CHAT19',verification='Verification records received; physical completion not certified'))
 extra.extend([
  dict(id='X901',team=2,lg='Yumbe',name='Ekaligo Health Centre III',type='Health centre',scope='Ground return only',status='Field evidence',folder='team-02/Yumbe/Amanyiri-HC-III',source='team-02/Yumbe/Amanyiri-HC-III/1 AMANYIRI HCIII.docx',source_locator='Health-centre interview: Name of Health EKALIGO HCIII',note='The programme data manager confirms that Ekaligo and Amanyiri are independent facilities. The combined file names Ekaligo in the interview, while the asset schedule separately names Amanyiri.',ground_name='Ekaligo Health Centre III',master_ids='',decision_ref='USER02',verification='Facility named in submitted return; no separate Ekaligo asset schedule identified'),
  dict(id='X902',team=2,lg='Yumbe',name='Liko Health Centre III',type='Health centre',scope='Ground return only',status='Field evidence',folder='team-02/Yumbe/Lodonga-Seed-Secondary-School',source='team-02/Yumbe/Lodonga-Seed-Secondary-School/LODONGA SEED SS (2).docx',source_locator='Health-centre interview: Name of Health Centre Liko Health center iii',note='The programme data manager confirms that Liko and Lodonga Seed Secondary School are independent facilities. The combined file names Liko in the health-centre interview and Lodonga in the school asset schedules.',ground_name='Liko Health Centre III',master_ids='',decision_ref='USER02',verification='Facility named in submitted return; no separate Liko asset schedule identified'),
 ])
 linked_receivers={
  (key('Nebbi'),key('Pamaka HC III')):('H218','Receiving facility for the master-list Oweko replacement.','CHAT21D'),
  (key('Zombo'),key('Amwonyo HC III')):('H231','Receiving facility for the UgIFT assets relocated from Alangi Health Centre III.','CHAT21A'),
  (key('Zombo'),key('Atyak HC III')):('H233','Receiving facility for the UgIFT assets relocated from Ther-uru Health Centre III.','CHAT21B'),
 }
 for r in extra:
  link=linked_receivers.get((key(r['lg']),key(r['name'])))
  if link:
   r['scope']='Linked receiving facility'; r['master_ids']=link[0]; r['note']=link[1]+' Supervisor message 23 September 2026 09:36.'; r['decision_ref']=link[2]
 for r in extra:
  if r['team']==30 and key(r['lg'])==key('Kasanda') and key(r['name'])==key('Namabaale HC III'):
   r['source']=f'{team30_root}/NAMABAALE HCIII UGIFT Asset Verification Tool Kit - FINAL (2).docx'
   r['source_locator']='Health-centre interview and checklist'
   r['verification']='Team 30 facility-specific return received; physical completion not certified'
   r['note']='Team 30 return confirms Namabaale Health Centre III in Kasanda; no confirmed master-list match.'
 # New Mayanga rows supplement its original register evidence.
 mayanga=find('Mitooma','Mayanga HC II'); mayanga.setdefault('supplemental_sources',[]).append('_multi-team/teams-19-21/data updates - western.xls'); mayanga.setdefault('supplemental_locators',[]).append('Sheet3!B3'); mayanga['note']+=' New western update also has Mayanga asset rows (Sheet3!B3).'
 for r in records+extra:
  if r.get('decision_ref','').startswith('CHAT'):
   r.setdefault('supplemental_sources',[]).append(LATEST_CHAT)
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
  r['field_name']=canonical_facility_name(r)
  r['note']=r['note'].replace('possibly the team\'s folder','Unconfirmed possible match:').replace('not on the programme list','No confirmed master match')
 corrections=[
  ('Oyam','Iceme HC II','team-05/Oyam/Iceme-HC-III/Icheme HC IIII_ASSET VERIFICATION AND RECORDING TOOL KIT.docx','Late-evening visit recorded; photographs were not taken','The later Iceme toolkit records a late-evening visit without photographs. An earlier note says the in-charge could not identify the UgIFT items. The later toolkit is the governing return.'),
  ('Kamuli MC','Busota HC II','team-18/Kamuli MC/Busota-HC-III/ASSET VERIFICATION AND RECORDING TOOL KIT 222 (3).docx','Verification records received; physical completion not certified','Sulaina identified this as the Busota HC III softcopy. The checklist and the master use Kamuli MC. The cover heading says Kamuli district.'),
  ('Gomba','Mamba HC II','team-32/Gomba/Mamba-HC-III/ASSET VERIFICATION AND RECORDING TOOL KIT 222(MAMBA HC III -GOMBA LOCAL GOVERNMENT).docx','Verification records received; physical completion not certified','The filename and checklist name Mamba Health Centre III in Gomba. Lawrence says Kyegonza HC III is Mamba HC III. The interview line that says Kibiri is the same sentence copied into the separate Kibiri toolkit.'),
  ('Makindye-Ssabagabo MC','Kibiri HC III','team-32/Makindye-Ssabagabo MC/Kibiri-HC-III/ASSET VERIFICATION AND RECORDING TOOL KIT 222(KIBIRI HC III -MAKINDYE SSABAGABO).docx','Verification records received; physical completion not certified','The original toolkit and the process report name Kibiri Health Centre III in Makindye-Ssabagabo. A later copy of the toolkit repeats a Gomba/Mamba checklist and is not the governing return.'),
  ('Kyegegwa','Kabweza','team-28/Kyegegwa/Kabweza-HC-III/ASSET VERIFICATION AND RECORDING TOOL KIT 222 kabweza hc iii.docx','Verification records received; physical completion not certified','The Kabweza toolkit names Kabweza Health Centre III in Kyegegwa. A separate process report in the folder describes Kyankaramata and is not the facility return.'),
  ('Kyenjojo','Kataraza HC II','team-28/Kyenjojo/Kataraza-HC-III/ASSET VERIFICATION AND RECORDING TOOL KIT katalaza.docx','Verification records received; physical completion not certified','The toolkit names Kataraza Health Centre III in Kyenjojo. The checklist spelling is Katalaza. A separate process report describes Kyankaramata and is not the facility return.'),
 ]
 for loc,name,source,verification,note in corrections:
  r=find(loc,name); r['status']='Field evidence'; r['source']=source; r['verification']=verification; r['note']=note
 submitted_gap='Lawrence Kalyowa reported on 23 September 2026 that this return had not yet been submitted. A missing submission is not evidence that the facility does not exist.'
 for r in records:
  if r['status']=='Needs review' and 'ongoing' in r.get('verification','').lower() and key(r['name']) in {key('Kireka HCII'),key('Kirinya HCII'),key('Kasangati TC/Mutuba-Nangabo'),key('Mutungo HCII')}:
   r['status']='No return'; r['verification']='Not established'; r['note']=''; r['decision_ref']='CHAT41'
 for r in records:
  named=key(r['name']) in {key('Kireka HCII'),key('Kirinya HCII'),key('Kasangati TC/Mutuba-Nangabo'),key('Mutungo HCII'),key('Zinga HC II')}
  whole_lg=key(r['lg']) in {key('Nakaseke'),key('Nakasongola')}
  if r['status']=='No return' and (named or whole_lg):
   r['note']=(r['note']+' ' if r['note'] else '')+submitted_gap
   r['decision_ref']=r.get('decision_ref') or 'CHAT41'
 # A facility with no return is completed once a reason or reconciliation is on file.
 explained_statuses={'Needs review','Reported absent','No UgIFT assets','Outside UgIFT','Replaced','Not verified'}
 for r in records:
  has_reason=bool((r.get('note') or '').strip() or r.get('decision_ref'))
  has_return=bool(r.get('folder') or r.get('source'))
  move=r['status'] in explained_statuses and not has_return
  move=move or (r['status']=='No return' and has_reason)
  move=move or (r['status'] in explained_statuses and r['status']!='Needs review')
  if not move: continue
  prior=r.get('verification') or r['status']
  if prior and prior not in (r.get('note') or ''):
   r['note']=(r['note']+' ' if r.get('note') else '')+prior
  r['status']='Field evidence'
  r['verification']='Case explained or reconciled; counted as completed'
  if not r.get('source'):
   r['source']=LATEST_CHAT if r.get('decision_ref') else MASTER
   r['source_locator']=r.get('source_locator') or r.get('decision_ref') or 'Documented case'
 records.sort(key=lambda r:(r['team'],r['lg'],r['type'],r['name']))
 extra.sort(key=lambda r:(r['team'],r['lg'],r['name']))
 # Guard the reviewed exceptions against future matching or output regressions.
 sop_sop=find('Tororo','Sop Sop HC II')
 assert sop_sop['folder'].endswith('/Sop-Sop-HC-III'), sop_sop
 assert not [r for r in extra if key(r['lg'])==key('Tororo') and r['type']=='Health centre' and key(r['name']).startswith(key('Sop Sop'))]
 mayanga_supplements=dict(zip(mayanga.get('supplemental_sources',[]),mayanga.get('supplemental_locators',[])))
 assert mayanga_supplements.get('_multi-team/teams-19-21/data updates - western.xls')=='Sheet3!B3', mayanga_supplements
 assert not [r for r in extra if key(r['lg'])==key('Oyam') and key(r['name'])==key('Abeja HC III')], 'Later Oyam evidence corrects Abeja to master-listed Abela'
 for ref,loc,name,folder in [('CHAT12','Jinja','Butagaya','Buwala-Seed-Secondary-School'),('CHAT13','Namayingo','Mwema Seed School','Mutumba-Seed-Secondary-School')]:
  resolved=find(loc,name)
  assert resolved['decision_ref']==ref and resolved['status']=='Field evidence', resolved
  assert resolved['folder'].endswith('/'+folder), resolved
 pandwong=find('Kitgum MC','Pandwong HC II')
 assert pandwong['status']=='Field evidence' and 'no UgIFT assets' in pandwong['note'], pandwong
 central_division=find('Jinja City','Central Division')
 assert central_division['id']=='S012' and central_division['status']=='Field evidence' and central_division['decision_ref']=='USER01', central_division
 amanyiri=find('Yumbe','Amanyiri')
 lodonga=find('Yumbe','Ladonga Seed School')
 assert amanyiri['status']=='Field evidence' and amanyiri['decision_ref']=='USER02', amanyiri
 assert lodonga['status']=='Field evidence' and lodonga['decision_ref']=='USER02', lodonga
 team2_independent={r['id']:r for r in extra if r['id'] in {'X901','X902'}}
 assert set(team2_independent)=={'X901','X902'} and all(r['decision_ref']=='USER02' for r in team2_independent.values()), team2_independent
 assert len(inherited_register_extras)==8, len(inherited_register_extras)
 assert all(
  (r['team']==30 and key(r['name'])==key('Namabaale HC III')) or (r['source_locator']==locator and locator)
  for r,locator in inherited_register_extras
 ), inherited_register_extras
 assert not [r for r in records+extra if r['status']=='Register only'], 'Register-only status must be represented as Field evidence with a consolidated-register verification basis'
 consolidated=[r for r in records if r['verification']=='Completed from consolidated register; physical inspection not certified']
 assert len(consolidated)==42, (len(consolidated),[r['id'] for r in consolidated])
 team30_confirmed={r['id'] for r in records if r['team']==30 and r['status']=='Field evidence'}
 assert {'H012','H013','H011','H014','H301','S069','S236'} <= team30_confirmed, team30_confirmed
 assert st_mugagga['status']=='Field evidence', st_mugagga
 assert len([r['folder'] for r in records if r['folder']])==len({r['folder'] for r in records if r['folder']}), 'Two distinct master facilities share one folder'
 assert len(records)==629, len(records)
 assert sum(len(r['master_ids'].split('; ')) for r in records)==632
 assert len({r['id'] for r in records+extra})==len(records+extra)
 missing_sources=[r['source'] for r in records+extra if r['source'] and not source_path(r['source']).is_file()]
 assert not missing_sources,missing_sources
 fields=['id','scope','team','supervisor','lg','type','name','field_name','status','verification','master_ids','master_lg','phase','project_status','decision_ref','source','source_locator','additional_sources','additional_locators','folder','note','master_source','source_row']
 write_csv(GROUPED/'facility-reconciliation.csv',records+extra,fields)
 write_csv(GROUPED/'master-source-rows.csv',masters,['id','lg','type','name','phase','project_status','source_row'])
 write_csv(GROUPED/'master-duplicate-rows.csv',duplicates,['duplicate','retained','lg','name'])
 source_rows=[]
 for r in records+extra:
  evidence=[e for e in index if (r.get('folder') and e['destination (in raw-data-grouped)'].startswith(r['folder']+'/')) or (r['source'] and e['destination (in raw-data-grouped)']==r['source']) or e['destination (in raw-data-grouped)'] in r.get('supplemental_sources',[])]
  for e in evidence:
   source_rows.append(dict(source_locator=(r.get('source_locator','') if e['destination (in raw-data-grouped)']==r['source'] else dict(zip(r.get('supplemental_sources',[]),r.get('supplemental_locators',[]))).get(e['destination (in raw-data-grouped)'],'')),facility_id=r['id'],team=r['team'],lg=r['lg'],facility=r.get('field_name') or r['name'],source_root=e.get('source root','raw-data-ungrouped') or 'raw-data-ungrouped',source=e['source (in raw-data-ungrouped)'],destination=e['destination (in raw-data-grouped)'],status=e['status'],note=e['note'],sha256=e.get('sha256','')))
 write_csv(GROUPED/'facility-evidence-index.csv',source_rows,['facility_id','team','lg','facility','source_root','source','destination','source_locator','status','note','sha256'])
 write_csv(GROUPED/'supervisor-decisions.csv',[dict(d,master_names='; '.join(d.get('master_names',[d.get('master_name','')])),ground_names='; '.join(d.get('ground_names',[d.get('ground_name') or '']))) for d in chat['decisions']],['id','date_time','speaker','team','lg','master_names','ground_names','decision','quote','explicit','note'])
 payload=dict(master_rows=632,master_facilities=629,counts=dict(Counter(r['status'] for r in records)),extra_counts=dict(Counter(r['scope'] for r in extra)),records=records,extras=extra,duplicates=duplicates,teams=teams,decisions=chat)
 (TMP/'reconciled.json').write_text(json.dumps(payload,indent=2),encoding='utf-8')
 print(json.dumps({k:v for k,v in payload.items() if k not in ['records','extras','teams','decisions']},indent=2))
if __name__=='__main__': main()
