"""27SS 鞋款：原本是整張 CAD 頁(3 隻鞋)或只剩鞋跟局部 → 從 CAD 頁裁出該顏色的完整鞋。
用法：python3 tools/shoe_crops.py   (在 repo 根目錄；重產資料後 post_1112_fix → fill_images → 這支)
SLOT: A=左上 B=右上 C=左下。來源頁以「某個款色目前的 doll」找出，所以要在 fill_images 之前或之後都可跑一次。"""
import re,json,hashlib,io,base64
from PIL import Image,ImageChops
s=open('data.js',encoding='utf-8').read()
d={a:json.loads(b) for a,b in re.findall(r'window\.(\w+)=(.*?);\n(?=window\.|$)',s,re.S)}; it={i['id']:i for i in d['SDR_ITEMS']}
box={'A':(0,75,600,362),'B':(600,75,1200,362),'C':(0,495,600,785)}
# 款色 -> (來源頁款色, 欄位)   來源頁取自該款色現有 doll（須為原 CAD 整頁，所以先記下）
SRC={'S833':'ABYSHXW501-BU','S841':'ABYSHXW504-CR','S811':'ABYSHXW503-YE','S807':'ABYSHXW918-RE','SKY':'ABYSHXW913-RE'}
MAP={'ABYSHXW907-BK':('S833','A'),'ABYSHXW001-KH':('S833','B'),'ABYSHXW501-BU':('S833','C'),
     'ABYSHXW922-BK':('S841','A'),'ABYSHXW504-CR':('S841','C'),
     'ABYSHXW920-WH':('S811','A'),'ABYSHXW921-RE':('S811','B'),'ABYSHXW503-YE':('S811','C'),
     'ABYSHXW916-BK':('S807','A'),'ABYSHXW918-RE':('S807','C'),
     'ABYSHXW913-RE':('SKY','A'),'ABYSHXW912-TU':('SKY','B')}
import sys
page={k:it[v]['doll'] for k,v in SRC.items()}
if '--pages' in sys.argv: json.dump(page,open('/tmp/shoe_pages.json','w'))
else: page=json.load(open('/tmp/shoe_pages.json'))
IMG=json.loads(re.search(r'window\.SDR_IMG=(.*);\n',open('imgs.js').read(),re.S).group(1))
for iid,(sk,sl) in MAP.items():
    im=Image.open(f'big/{page[sk]}.jpg').convert('RGB')
    if sk=='SKY':
        w,h=im.size; b=(0,0,w//2,h) if sl=='A' else (w//2,0,w,h); b=(b[0],int(h*.2),b[2],int(h*.78))
    else: b=box[sl]
    c=im.crop(b); bg=Image.new('RGB',c.size,'white'); bb=ImageChops.difference(c,bg).convert('L').point(lambda v:255 if v>25 else 0).getbbox()
    if bb: p=12; c=c.crop((max(0,bb[0]-p),max(0,bb[1]-p),min(c.width,bb[2]+p),min(c.height,bb[3]+p)))
    buf=io.BytesIO(); c.save(buf,'JPEG',quality=88); raw=buf.getvalue(); h=hashlib.md5(raw).hexdigest()[:12]
    c.save(f'big/{h}.jpg',quality=88); t=c.copy(); t.thumbnail((360,360)); tb=io.BytesIO(); t.save(tb,'JPEG',quality=72)
    IMG[h]='data:image/jpeg;base64,'+base64.b64encode(tb.getvalue()).decode()
    it[iid]['doll']=h; it[iid].pop('ref',None); print(iid,sk,sl,c.size)
open('imgs.js','w').write('window.SDR_IMG='+json.dumps(IMG)+';\n')
open('data.js','w',encoding='utf-8').write(''.join(f'window.{a}={json.dumps(v,ensure_ascii=False)};\n' for a,v in d.items()))
