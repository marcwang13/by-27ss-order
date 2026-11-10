# 2026/11/10：拿掉價格與韓國入倉日、拿掉 Sample 選款敘述，改成台灣主打＋台灣市場分析。直接改寫 data.js。
import json,re,sys
p=sys.argv[1]+'/data.js'; s=open(p).read()
m=re.search(r'window.SDR_ITEMS=(\[.*?\]);\n',s,re.S); L=json.loads(m.group(1))
HERO={
 '1BYRTMW904':'涼感短袖T恤，台灣夏天又熱又濕，單價低、五色，量販主力','1BYRTMW506':'涼感短袖T恤，台灣夏天又熱又濕，單價低，量販主力',
 '1BYKTMW003':'彈性 POLO 衫，上班、打球、出遊都能穿，熟齡客群基本款','1BYKTMW502':'彈性 POLO 衫，上班、打球、出遊都能穿，熟齡客群基本款',
 '1BYKTMW007':'泡泡紗不貼身，悶熱天氣穿著舒服，五色好陳列','1BYKTMW505':'泡泡紗不貼身，悶熱天氣穿著舒服',
 '1BYJKMW005':'薄風衣兼防曬，春季到初夏、冷氣房都用得到，六色','1BYJKMW504':'薄風衣兼防曬，春季到初夏、冷氣房都用得到',
 '1BYVSMW001':'輕量背心，早晚溫差與冷氣房好搭，熟齡客群回購高','1BYVSMW501':'輕量背心，早晚溫差與冷氣房好搭，熟齡客群回購高',
 '1BYJKMW003':'SPEED HIKER 輕量外套，郊山健行的防風防曬層','1BYJKMW503':'SPEED HIKER 輕量外套，郊山健行的防風防曬層',
 '1BYGJSW002':'GORE-TEX 外套，5–6 月梅雨和 7 月起的颱風季必備','1BYGJSW502':'GORE-TEX 外套，5–6 月梅雨和 7 月起的颱風季必備',
 '1BYJKSW003':'基本款雨衣外套，價格比 GORE-TEX 好入手，梅雨季走量','1BYJKSW502':'基本款雨衣外套，價格比 GORE-TEX 好入手，梅雨季走量',
 '1BYPNMW004':'TL-3000 輕量 CORDURA 登山褲，耐磨又不悶，台灣登山客全年穿長褲','1BYPNMW502':'TL-3000 輕量 CORDURA 登山褲，耐磨又不悶，台灣登山客全年穿長褲',
 '1BYPNMW008':'涼感長褲，夏天也穿得住的長褲，防曬防蚊','1BYPNMW009':'涼感卡其長褲，日常與郊山通用',
 '1BYHPMW008':'SPEED HIKER 短褲，五色，夏季健行與日常都好賣','1BYHPMW505':'SPEED HIKER 短褲，五色，夏季健行與日常都好賣',
 '1BYRTMW901':'攀岩 HOLD MASTER 圖案T恤，五色，年輕客層與街頭穿搭','1BYHPMW901':'攀岩 HOLD MASTER 短褲，單價低，年輕客層入門',
 '1BYRTMW908':'健行圖案T恤，生活穿搭款，好帶','1BYJKMW901':'攀岩 RIDGE MASTER 外套，五色，bcc 生活線的形象款',
 '1BYRTMW003':'越野跑提花短袖，台灣越野跑賽季的主力上衣','1BYJKMW001':'越野跑防風外套，輕、可收納，跑山必備','1BYJKMW501':'越野跑防風外套，輕、可收納，跑山必備',
 'ABYSHXW001':'GORE-TEX 中筒健行鞋，台灣多雨濕滑，郊山到百岳都能穿','ABYSHXW501':'GORE-TEX 中筒健行鞋，台灣多雨濕滑，郊山到百岳都能穿',
 'ABYSHXW502':'GORE-TEX 低筒健行鞋，郊山與日常兩用','ABYSHXW908':'GORE-TEX 低筒健行鞋，郊山與日常兩用',
 'ABYSHXW504':'旋鈕 GORE-TEX 健行鞋，好穿脫，熟齡登山客接受度高','ABYSHXW922':'旋鈕 GORE-TEX 健行鞋，好穿脫，熟齡登山客接受度高',
 'ABYSHXW912':'品牌越野跑代表鞋款，VIBRAM 大底','ABYSHXW916':'旋鈕越野跑鞋，跑山與日常都能穿',
 '2BYHTXW913':'可拆式遮陽帽，台灣夏天紫外線強，登山健行必備','2BYHTXW903':'基本款棒球帽，四色，低單價加購',
 '2BYXXMW905':'涼感袖套，防曬剛需，櫃檯加購品','2BYSCXW903':'健行中筒襪，搭鞋款做組合',
 '2BYKSXW913':'18L 輕量背包，郊山單日行程最常用的容量','2BYKSXW920':'10L 小背包，日常與輕健行',
 '2BYABXW907':'單肩包，日常通勤與旅遊','2BYHTXW914':'BCC 棒球帽，生活線入門配件',
 '1BYETMW004':'涼感高領排汗衣，防曬內搭，登山與戶外工作都用得到','1BYETMW503':'涼感高領排汗衣，防曬內搭，登山與戶外工作都用得到',
}
def fallback(i):
    c=i['cat']
    if i['sheet']=='鞋款': return '台灣山區多雨、路面濕滑，防水與抓地是選鞋重點' if 'GORE' in i['zh'].upper() else '越野跑鞋在台灣跑山客群需求穩定，建議中等量'
    return {'帽子':'台灣夏季紫外線強，帽子是最好帶的低單價配件，遮陽帽可多備','背包':'20–30L 是台灣單日行程最常用的容量；45L 以上以高山、長程客為主，建議少量','配件包':'腰包、斜背包單價低，適合放櫃檯帶加購','襪子':'襪子四季都賣，適合搭鞋款做組合','手套':'薄手套用於登山防曬與握杖，建議基本量','登山杖':'登山杖是台灣中高齡登山客的常備品，折疊款好收納，建議中等量','太陽眼鏡':'太陽眼鏡屬加購品，建議少量試賣','燈具':'露營燈屬露營周邊，建議少量','其他配件':'防曬與登山小物單價低，適合帶加購，建議基本量'}.get(c,'台灣春夏偏熱，建議依店內客層少量試單')
for i in L:
    mm=re.match(r'(\d{4})/(\d\d)',i.get('launch') or '')
    tag=''
    if mm and (mm.group(1),mm.group(2)) in (('2026','12'),('2027','01'),('2027','02'),('2027','03')):
        mth=int(mm.group(2))%12+1; tag=f'台灣預計 {mth} 月上市'
    i['monTag']=tag; i['launch']=''; i['eta']=''; i['krw']=None; i['price']=None
    h=HERO.get(i['style']); i['whl']=bool(h); i['whlr']=h or ''
    if not i.get('tw'): i['tw']=fallback(i)
s=s[:m.start(1)]+json.dumps(L,ensure_ascii=False)+s[m.end(1):]
open(p,'w').write(s)
from collections import Counter
print(len(L),'hero',sum(1 for i in L if i['whl']),len({i['style'] for i in L if i['whl']}),'missing',[k for k in HERO if not any(i['style']==k for i in L)],'tw',sum(1 for i in L if i['tw']),Counter(i['monTag'] for i in L))
