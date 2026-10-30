import sys
NEW = r"""const SZ_TOP_M={85:'XS',90:'S',95:'M',100:'L',105:'XL',110:'2XL',115:'3XL',120:'4XL',125:'5XL',130:'6XL'};
const SZ_TOP_W={85:'S',90:'M',95:'L',100:'XL',105:'2XL'};
const SZ_WAIST={66:'26"',69:'27"',71:'28"',74:'29"',76:'30"',79:'31"',81:'32"',84:'33"',86:'34"',91:'36"',96:'38"',101:'40"',106:'42"'};
const SZ_SHOE_M={250:'US7',255:'US7.5',260:'US8',265:'US8.5',270:'US9',275:'US9.5',280:'US10',285:'US10.5',290:'US11',295:'US11.5',300:'US12'};
const SZ_SHOE_W={230:'US6',235:'US6.5',240:'US7',245:'US7.5',250:'US8',255:'US8.5',260:'US9'};
function szConv(z,it){ const n=Number(z); if(!isFinite(n)||String(z)!==String(n)) return '';
  const w=it&&it.gen==='女', shoe=it&&it.sheet==='鞋款', low=it&&it.sheet==='下身';
  if(shoe) return (w?SZ_SHOE_W:SZ_SHOE_M)[n]||'';
  if(n in SZ_WAIST && (low || !(n in SZ_TOP_M))) return SZ_WAIST[n];
  if(n>=85&&n<=130) return (w?SZ_TOP_W:SZ_TOP_M)[n]||'';
  if(n>=54&&n<=62) return '頭圍';
  if(n>=20&&n<=30) return 'cm';
  return ''; }
function SZL(z,it){ const l=SZ_LBL[z]; if(l&&l!==z&&z!=='ASSORTED') return esc(l)+`<small class="szn">${esc(z)}</small>`; const c=szConv(z,it); return esc(l||z)+(c?`<small class="szn">${esc(c)}</small>`:''); }"""
p=sys.argv[1]; h=open(p,encoding='utf8').read()
a=h.index('function SZL(z,it){'); b=h.index('\n',a)
h=h[:a]+NEW+h[b:]
if len(sys.argv)>2:
    i=h.index('<p class="sznote"><b>尺寸</b>'); j=h.index('</p>',i)
    h=h[:i]+'<p class="sznote"><b>尺寸</b>照原廠開的尺寸段，數字下方小字是對照：上衣為韓國標準（男 95＝M、100＝L；女 85＝S、90＝M），褲子為腰圍 cm 換算英吋，鞋款為 mm 換算 US 碼，帽子為頭圍 cm。字母尺寸 XS～3XL，F＝單一尺寸。實際以各款原廠尺寸表為準。斜線灰格＝這個顏色沒開的尺寸。</p>'+h[j+4:]
open(p,'w',encoding='utf8').write(h)
