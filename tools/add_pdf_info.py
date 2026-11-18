#!/usr/bin/env python3
"""把原廠 27SS 整合策略簡報（Visual Strategy ZH）裡能對上款名的內容寫進 data.js 的 info 欄（商品資訊）。
只對「款名明確對得上」的款式寫；對不上的內容放在 story.js 的季節策略面板與各系列商品資訊。
重跑安全：每次先清掉 info 再寫。用法：python3 tools/add_pdf_info.py"""
import json, os, re
os.chdir(os.path.dirname(os.path.abspath(__file__)) + '/..')
s = open('data.js', encoding='utf-8').read()
i = s.find('window.SDR_ITEMS='); j = s.find('];', i) + 1
head, tail = s[:i], s[j:]
items = json.loads(s[i + len('window.SDR_ITEMS='):j])

def has(it, *keys):
    t = ' '.join([it['zh'], it['en'], it['style']]).upper()
    return any(k.upper() in t for k in keys)

RULES = [
    # (條件, 文字行)
    (lambda it: has(it, 'TOUGH SHIELD'), [
        'Tough Shield 是原廠春季 2 的防護耐用系列：外套加長褲的系統，賣點是耐磨、立體剪裁、防風雨。',
        '帽款跟著服裝走，春季搭 GORE-TEX＋Tough Shield，陳列和對應的服裝主打款放一起。']),
    (lambda it: it['sheet'] == '配件' and has(it, 'GORE-TEX') and it['cat'] == '帽子', [
        '原廠春季帽款搭配：GORE-TEX＋Tough Shield，走防護與耐用結構。',
        '帽款和對應的服裝主打款、活動組合放在一起陳列。']),
    (lambda it: (it['drop'] == 'DNS' or has(it, 'DNS')) and it['sheet'] in ('上身', '下身'), [
        'DNS 頂規線：把已驗證的高山技術下放到健行，耐用度做到 Spectra／Dyneema 等級。',
        '外殼、保暖層、機能褲成套，是洋蔥式穿搭的完整系統；原廠建議用 DNS 建立專業形象，再挑部分健行款放量。']),
    (lambda it: (it['drop'] == 'DNS' or has(it, 'DNS')) and it['sheet'] == '配件' and not has(it, 'UL30', 'UL 30'), [
        'DNS 頂規線配件：和 DNS 服裝一起，撐起專業登山的形象；原廠建議用 DNS 建立專業形象，再挑部分健行款放量。']),
    (lambda it: has(it, 'UL30', 'UL 30'), [
        'DNS UL 30：登山用，輕量結構、保留高山必要機能。',
        '原廠春季登山組合的背包：搭 Tough Shield 服裝與 YAK LOAD 登山鞋。']),
    (lambda it: has(it, 'DYNEEMA') and it['drop'] != 'DNS', [
        '原廠把 Dyneema 等級的耐用度從 DNS 帶進健行款，轉成容易跟客人說明的主打商品。']),
    (lambda it: has(it, 'COLLINE'), [
        'COLLINE 是原廠郊山健行的量款核心，做大已驗證的一日健行系列（背包 20L／26L）。',
        '累計售出率 78.4%，賣得好的就加深。']),
    (lambda it: has(it, 'DASH') and it['cat'] == '背包', [
        'DASH 越野背心包：依跑步距離規劃款式，先顧合身與取物方便，容量依活動選。',
        '靠跑者試用與依距離選款換回購；和越野鞋、越野防風雨外套一起陳列。']),
    (lambda it: it['sheet'] == '鞋款' and has(it, 'TRAIL-X 02'), [
        'TRAIL-X 02：Vibram 大底加 T.C.S. 穩定系統，原廠列為全球擴展款，吸引更廣的越野健行客群。',
        '實證路徑：選手驗證 → 消費者試穿 → 門市說明 → 回購。']),
    (lambda it: it['sheet'] == '鞋款' and has(it, 'EXUM'), [
        '快速健行款：健行的防護力，加上越野鞋的緩震與靈活，原廠列為全球策略款。',
        '通路分工：專業登山通路賣主打款加全球款；一般通路賣已驗證的核心款。']),
    (lambda it: it['sheet'] == '鞋款' and has(it, 'YAKLOAD', 'YAK LOAD'), [
        'YAK LOAD Re-master：高階登山代表款，更新楦型，採用 LOOP GRIP Y7+。',
        '原廠春季登山組合的鞋款主角，專業登山通路主推。']),
]

n = 0
for it in items:
    lines = []
    for cond, txt in RULES:
        if cond(it):
            lines += [x for x in txt if x not in lines]
    if lines:
        it['info'] = '\n'.join(lines); n += 1
    else:
        it.pop('info', None)
open('data.js', 'w', encoding='utf-8').write(head + 'window.SDR_ITEMS=' + json.dumps(items, ensure_ascii=False) + tail)
styles = len({it['style'] for it in items if it.get('info')})
print('款色', n, '款', styles)
