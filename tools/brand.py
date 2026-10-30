import sys, re, shutil, os
season, out = sys.argv[1], sys.argv[2]   # 27SS / 27FW
src='/home/claude/by/dst'
S = season; s = season.lower()           # 27ss
pre = 'BYS27' if S=='27SS' else 'BYF27'
key = 'bys' if S=='27SS' else 'byf'
h = open(src+'/index.html',encoding='utf8').read()
def rep(a,b,count=None,regex=False):
    global h
    n = len(re.findall(a,h)) if regex else h.count(a)
    assert n>0, ('missing',a[:60])
    h = re.sub(a,b,h) if regex else h.replace(a,b)
# brand / season strings
rep('DESCENTE_27FW', f'BLACKYAK_{S}')
rep('DESCENTE 27FW', f'BLACK YAK {S}')
rep('<title>BLACK YAK %s Early Buy 訂貨</title>'%S, f'<title>BLACK YAK {S} 經銷訂貨</title>')
rep('<b>DESCENTE</b><span>27FW Early Buy</span>', f'<b>BLACK YAK</b><span>{S}</span>')
rep('DESCENTE 業務', 'BLACK YAK 業務')
rep("'dst-admin'", f"'{key}-admin'"); rep("'dst-dev'", f"'{key}-dev'"); rep("'dst-auth'", f"'{key}-auth'")
rep("'dst-27fw-sent-v1'", f"'{key}-{s}-sent-v1'"); rep("'dst-27fw-draft-v1'", f"'{key}-{s}-draft-v1'")
rep('`DST27-', f'`{pre}-')
# colors: brand black + yellow accent
rep('--brand:#0a3f94; --brand-ink:#ffffff; --brand-2:#072d6c;', '--brand:#141414; --brand-ink:#ffffff; --brand-2:#333333;')
rep('--brand:#14408c; --brand-ink:#ffffff; --brand-2:#0c2b61;', '--brand:#1f1f1f; --brand-ink:#ffffff; --brand-2:#3a3a3a;')
rep('FF0A3F94','FF141414')
# config from data
rep("const SHEETS = ['上衣 TOUGH','羽絨','GORE-TEX'];", "const CFG = window.BY_CFG||{}; const SHEETS = CFG.sheets||[];")
rep("const MONTH_ORDER = ['5月','6月','7月','8月'];", "const MONTH_ORDER = CFG.months||[];")
rep("let S = {sheet:'上衣 TOUGH',", "let S = {sheet:(window.BY_CFG&&window.BY_CFG.sheets[0])||'',")
# sizes
a=h.index("const SZ_ORDER=["); b=h.index("function SZL(")
h=h[:a]+"""const SZ_ORDER=CFG.szOrder||[];
const RUNS=window.BY_RUNS||{};
const SZ_NUM={};
const SIZE_COLS={};
const SZ_LBL=CFG.szLabel||{};
"""+h[b:]
rep("function SZL(z,it){ const t=(SZ_NUM[it&&it.run]||{})[(it&&it.part)||'top']||{}; const n=t[z]; return esc(z)+(n!=null?`<small class=\"szn\">${n}</small>`:''); }",
    "function SZL(z,it){ const l=SZ_LBL[z]; return esc(l||z)+(l&&l!==z&&z!=='ASSORTED'?`<small class=\"szn\">${esc(z)}</small>`:''); }")
# card: month tag + price with KRW
rep("<span class=\"tag m\">${esc(it.mon)}到貨${it.eta?' · 交期 '+esc(it.eta):''}</span>",
    "${it.monTag?`<span class=\"tag m\">${esc(it.monTag)}${it.eta?' · '+esc(it.eta):''}</span>`:''}${it.drop==='DNS'?'<span class=\"tag\">DNS</span>':''}")
rep("<div class=\"price\">${it.price?`<small>建議售價</small>${fmt(it.price)}`:'<small>售價待確認</small>'}</div>",
    "<div class=\"price\">${it.krw?`<small>韓國 MSRP</small>₩${Number(it.krw).toLocaleString('en-US')}<br><small>台幣換算</small>${fmt(it.price)}`:'<small>售價待確認</small>'}</div>")
# notes
sz_ss='<b>尺寸</b>照原廠開的尺寸段：上衣 85～130、褲子為腰圍（cm），字母尺寸 XS～3XL，F＝單一尺寸，小字是原廠尺寸代碼。斜線灰格＝這個顏色沒開的尺寸。'
sz_fw='<b>數量</b>27FW 原廠目前只開到款號（顏色、尺寸都還是 ASSORTED），先填每款總件數，色別與尺寸確定後再分配。有標尺寸段的會寫在款名下方。'
i=h.index('<p class="sznote">'); j=h.index('</p>',i)
fxnote=f'<p class="sznote fxnote"><b>價格說明</b>台幣價＝韓國 MSRP × {0.0245} 直接換算（四捨五入到 10 元），<b>尚未加關稅、運費等成本</b>，僅供下單參考，正式售價另行公告。</p>'
h=h[:i]+fxnote+'<p class="sznote">'+(sz_ss if S=='27SS' else sz_fw)+h[j:]
assert 'DESCENTE' not in h, re.findall('.{30}DESCENTE.{30}',h)[:5]
# Excel: KRW column + FX note
rep("'備註','預計上市','台灣建議售價'];", "'備註','韓國入倉','韓國售價 MSRP(KRW)','台灣建議售價'];")
rep("it.note||'',it.launch||'',it.price||null];", "it.note||'',it.launch||'',it.krw||null,it.price||null];")
rep("'預計上市':10,'台灣建議售價':10};", "'韓國入倉':10,'韓國售價 MSRP(KRW)':12,'台灣建議售價':10};")
rep("row.getCell(cPrice).numFmt='#,##0';", "row.getCell(cPrice).numFmt='#,##0'; row.getCell(cPrice-1).numFmt='#,##0';")
rep("ws.getCell('B2').value='黃色格填訂購數量，灰色為無此尺寸。", "ws.getCell('B2').value='台灣建議售價＝韓國 MSRP × 0.0245 直接換算，尚未加關稅、運費等成本。黃色格填訂購數量，灰色為無此尺寸。")
# sheet titles in Excel limited 31 chars fine
os.makedirs(out,exist_ok=True)
for f in ['config.js','README.md']: shutil.copy(f'{src}/{f}', f'{out}/{f}')
os.makedirs(out+'/apps-script',exist_ok=True)
open(out+'/index.html','w',encoding='utf8').write(h)
g=open(src+'/apps-script/Code.gs',encoding='utf8').read()
g=g.replace('DESCENTE_27FW',f'BLACKYAK_{S}').replace('DESCENTE 27FW',f'BLACK YAK {S}').replace('DESCENTE 台灣','BLACK YAK 台灣').replace('DESCENTE 業務','BLACK YAK 業務').replace('#0a3f94','#141414')
assert 'DESCENTE' not in g, re.findall('.{30}DESCENTE.{30}',g)
open(out+'/apps-script/Code.gs','w',encoding='utf8').write(g)
c=open(out+'/config.js').read(); c=re.sub(r"SUBMIT_URL: '[^']*'","SUBMIT_URL: ''",c); open(out+'/config.js','w').write(c)
open(out+'/README.md','w').write(f'# BLACK YAK {S} 經銷線上訂貨\n\n照 SDR FW27／DESCENTE 27FW 範本。資料來源：原廠 Buyer Order Dashboard 匯出（{S}）。台幣價＝韓國 MSRP × 0.0245，未含關稅運費。\n\n- `index.html` 下單頁、`data.js` 商品資料（`BY_CFG` 分頁／尺寸設定）、`imgs.js`／`big/` 圖片、`config.js` 收單網址、`apps-script/Code.gs` 收單程式。\n- 重產資料：`tools/gen.py`\n')
print('ok', S)
# --- theme + dup name fix (applied to written file) ---
h=open(out+'/index.html',encoding='utf8').read()
for a,b in [('--bg:#f2f4f8; --surface:#ffffff; --sunk:#e6ebf2; --line:#d2dae6; --fg:#121a26; --muted:#5d6979;','--bg:#f4f4f2; --surface:#ffffff; --sunk:#ebebe8; --line:#d8d8d4; --fg:#161616; --muted:#66665f;'),
            ('--acc:#0b57c2; --acc-ink:#ffffff; --acc-soft:#e1ecfb;','--acc:#c2410c; --acc-ink:#ffffff; --acc-soft:#fdeee4;'),
            ('--bg:#0b1019; --surface:#131a26; --sunk:#1b2433; --line:#2b384d; --fg:#e8eef7; --muted:#97a5ba;','--bg:#111111; --surface:#1b1b1b; --sunk:#242424; --line:#363636; --fg:#efefec; --muted:#a3a39c;'),
            ('--acc:#6aa5f5; --acc-ink:#0b1019; --acc-soft:#16294a;','--acc:#fb923c; --acc-ink:#111111; --acc-soft:#3a2214;'),
            ('#0a3f94','#141414'),
            ('<div class="t1"><h3>${esc(it.zh||it.en)}</h3><span class="en">${esc(it.en)}</span></div>','<div class="t1"><h3>${esc(it.zh||it.en)}</h3>${it.zh?`<span class="en">${esc(it.en)}</span>`:\'\'}</div>')]:
    assert a in h, a[:50]; h=h.replace(a,b)
open(out+'/index.html','w',encoding='utf8').write(h)
# --- v2: WHL / 台灣建議 / 只看建議款 ---
h=open(out+'/index.html',encoding='utf8').read()
def R2(a,b):
    global h
    assert a in h, a[:60]; h=h.replace(a,b)
R2('.note{font-size:12px;color:var(--warn)}', '.note{font-size:12px;color:var(--warn)}\n.tw{font-size:12px;color:var(--fg);background:var(--sunk);border-radius:4px;padding:4px 8px;margin-top:4px}.tw b{color:var(--acc)}\n.whl{font-size:12px;color:var(--ok);margin-top:4px}.tag.w{background:var(--ok);color:#fff}')
R2("${it.note?`<div class=\"note\">${esc(it.note)}</div>`:''}",
   "${it.note?`<div class=\"note\">${esc(it.note)}</div>`:''}${it.whl&&it.whlr?`<div class=\"whl\">${esc(it.whlr)}</div>`:''}${it.tw?`<div class=\"tw\"><b>台灣市場</b>　${esc(it.tw)}</div>`:''}")
R2("${it.gen?`<span class=\"tag\">${esc(it.gen)}</span>`:''}", "${it.gen?`<span class=\"tag\">${esc(it.gen)}</span>`:''}")
R2('<label class="toggle"><input type="checkbox" id="only"> 只看已下單</label>',
   '<label class="toggle"><input type="checkbox" id="only"> 只看已下單</label>')
R2("if(S.months.size && !S.months.has(i.mon)) return false;", "if(S.months.size && !S.months.has(i.mon)) return false;\n    if(S.whl && !i.whl) return false;")
R2("$('#only').addEventListener('change',e=>{ S.only=e.target.checked; renderList(); });",
   "$('#only').addEventListener('change',e=>{ S.only=e.target.checked; renderList(); });\nif($('#whlonly')) $('#whlonly').addEventListener('change',e=>{ S.whl=e.target.checked; renderTabs(); renderList(); });")
R2("const hay=[i.zh,i.en,i.style,i.sku,i.color,i.cc,i.cat,i.theme].join(' ')", "const hay=[i.zh,i.en,i.style,i.sku,i.color,i.cc,i.cat,i.theme,i.icon,i.tw,i.whlr].join(' ')")
# Excel 備註帶入 WHL 與台灣建議
R2("it.note||'',it.launch||'',it.krw||null,it.price||null];", "[it.note,it.whl?(it.whlr||''):'',it.tw?'台灣市場：'+it.tw:''].filter(Boolean).join('\\n'),it.launch||'',it.krw||null,it.price||null];")
R2("'備註':18,", "'備註':30,")
# 尺寸說明
if S=='27SS':
    i=h.index('<p class="sznote"><b>尺寸</b>'); j=h.index('</p>',i)
    h=h[:i]+'<p class="sznote"><b>分類</b>上方分「上身／下身／配件／鞋款」，下一排可再依系列篩選（涼感透氣、登山健行、越野跑、攀岩、DNS 頂規…）。「台灣市場」是依台灣氣候給的下單建議。</p><p class="sznote"><b>尺寸</b>照原廠開的尺寸段：上衣 85～130、褲子為腰圍（cm）、鞋款為 mm，字母尺寸 XS～3XL，F＝單一尺寸，小字是原廠尺寸代碼。斜線灰格＝這個顏色沒開的尺寸。</p>'+h[j+4:]
else:
    i=h.index('<p class="sznote"><b>數量</b>'); j=h.index('</p>',i)
    h=h[:i]+'<p class="sznote"><b>分類</b>上方分「上身／下身／套裝」，下一排依系列篩選（ALPINE A、ALPINE B、TOUGH SHIELD、越野跑、攀岩、滑雪）。「台灣市場」是依台灣氣候給的下單建議。</p><p class="sznote"><b>數量</b>27FW 原廠目前只開到款號（顏色、尺寸還沒定），先填每款總件數，色別與尺寸確定後再分配。商品說明為原廠開發規格，多數款還在打樣階段。</p>'+h[j+4:]
open(out+'/index.html','w',encoding='utf8').write(h)
