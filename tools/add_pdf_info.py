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
    (lambda it: has(it, 'TOUGH SHIELD'), [
        'Tough Shield 系列：外套加長褲成套的防護系列，耐磨布料、立體剪裁、防風雨。',
        '帽款跟著服裝系列，可和 Tough Shield 外套、長褲成套搭配。']),
    (lambda it: it['sheet'] == '配件' and has(it, 'GORE-TEX') and it['cat'] == '帽子', [
        'GORE-TEX 帽款：防水、防護與耐用結構，搭春季防護服裝。']),
    (lambda it: (it['drop'] == 'DNS' or has(it, 'DNS')) and it['sheet'] in ('上身', '下身'), [
        'DNS 頂規線：高山驗證過的技術，耐用度做到 Spectra／Dyneema 等級。',
        '外殼、保暖層、機能褲成套，是完整的洋蔥式系統。']),
    (lambda it: (it['drop'] == 'DNS' or has(it, 'DNS')) and it['sheet'] == '配件' and not has(it, 'UL30', 'UL 30'), [
        'DNS 頂規線配件：和 DNS 服裝同一條高山專業線。']),
    (lambda it: has(it, 'UL30', 'UL 30'), [
        'DNS UL 30：登山用，輕量結構，保留高山必要機能。',
        '原廠春季登山搭配：Tough Shield 服裝＋YAK LOAD 登山鞋。']),
    (lambda it: has(it, 'DYNEEMA') and it['drop'] != 'DNS', [
        'Dyneema 等級的耐用度，從 DNS 頂規線帶到健行款。']),
    (lambda it: has(it, 'COLLINE'), [
        'COLLINE：郊山一日健行系列（背包 20L／26L），容量好用、好背。']),
    (lambda it: has(it, 'DASH') and it['cat'] == '背包', [
        'DASH 越野背心包：依跑步距離分款，重合身與取物方便，跑步中拿水、補給不用卸包。',
        '可搭越野鞋、越野防風雨外套成套。']),
    (lambda it: it['sheet'] == '鞋款' and has(it, 'TRAIL-X 02'), [
        'TRAIL-X 02：Vibram 大底加 T.C.S. 穩定系統，越野與健行都好穿。']),
    (lambda it: it['sheet'] == '鞋款' and has(it, 'EXUM'), [
        '快速健行款：健行鞋的防護力，加上越野鞋的緩震與靈活。']),
    (lambda it: it['sheet'] == '鞋款' and has(it, 'YAKLOAD', 'YAK LOAD'), [
        'YAK LOAD Re-master：高階登山鞋，更新楦型，採用 LOOP GRIP Y7+ 大底。',
        '原廠春季登山搭配的鞋款。']),
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
