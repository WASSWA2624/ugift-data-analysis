from pathlib import Path
from zipfile import ZipFile
from PIL import Image,ImageOps,ImageDraw
import json
P=Path(r'D:/coding/ugift-data-analysis/outputs/narrative-report/reconciliation-06102026')
z=ZipFile(P.parent/'ugift-working-report-06102026-0000.docx')
items=[]
for num in [98,99]:
 p=P/f'structure_deleted_photo{num}.png';p.write_bytes(z.read(f'word/media/image{num}.png'))
 im=Image.open(p);print(num,str(p),im.size)
 items.append((str(num),im))
sheet=Image.new('RGB',(1200,800),'white');draw=ImageDraw.Draw(sheet)
for i,(num,im) in enumerate(items):
 thumb=ImageOps.contain(im,(590,760));sheet.paste(thumb,(600*i+(590-thumb.width)//2,30));draw.text((600*i+10,10),num,fill='black')
sheet.save(P/'structure_deleted_photo_contact.png')
