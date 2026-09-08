import re, json, html, sys
src = open(sys.argv[1], encoding='utf-8').read()
src = re.sub(r'data:image/[a-z]+;base64,[A-Za-z0-9+/=]+', 'IMG', src)

def txt(s):
    s = re.sub(r'<br\s*/?>', ' ', s)
    s = re.sub(r'<[^>]+>', ' ', s)
    return re.sub(r'\s+', ' ', html.unescape(s)).strip()

# Walk the doc, remembering the most recent deck / cue-card context.
tokens = []
pat = re.compile(
    r'<div class="deck-head".*?<h[12][^>]*>(?P<deck>.*?)</h[12]>'
    r'|<span class="pg"[^>]*>(?P<pg>.*?)</span>'
    r'|<h2[^>]*>(?P<h2>.*?)</h2>'
    r'|<h3[^>]*>(?P<h3>.*?)</h3>'
    r'|<span class="kind (?P<kind>[a-z]+)"'
    r'|<li class="step">(?P<step>.*?)</li>'
    r'|<pre class="out(?P<bad>[^"]*)"[^>]*>(?P<out>.*?)</pre>', re.S)

cur = {'deck':'', 'pg':'', 'h2':'', 'h3':'', 'kind':''}
cards, card = [], None
def newcard():
    global card
    card = {'deck':cur['deck'], 'pg':cur['pg'], 'h2':cur['h2'],
            'title':cur['h3'] or cur['h2'], 'kind':cur['kind'],
            'steps':[], 'out':[]}
    cards.append(card)

for m in pat.finditer(src):
    g = m.groupdict()
    if g['deck']:  cur['deck'] = txt(g['deck']); cur['pg']=''; card=None
    elif g['pg'] is not None and m.group('pg') is not None:
        cur['pg'] = txt(g['pg']); card = None
    elif g['h2'] is not None and m.group('h2') is not None:
        cur['h2'] = txt(g['h2']); cur['h3']=''; card=None
    elif g['h3'] is not None and m.group('h3') is not None:
        cur['h3'] = txt(g['h3']); card=None
    elif g['kind']: cur['kind'] = g['kind']
    elif g['step'] is not None and m.group('step') is not None:
        s = g['step']
        c = re.search(r'class="cmd"[^>]*>(.*?)</code>', s, re.S)
        d = re.search(r'class="does"[^>]*>(.*?)</p>', s, re.S)
        w = re.search(r'class="where"[^>]*>(.*?)</span>', s, re.S)
        if c:
            if card is None: newcard()
            card['steps'].append({
                'cmd': html.unescape(re.sub(r'<[^>]+>','',c.group(1))).strip(),
                'does': txt(d.group(1)) if d else '',
                'where': txt(w.group(1)) if w else ''})
    elif g['out'] is not None and m.group('out') is not None:
        if card is not None:
            card['out'].append({'bad':'bad' in (g['bad'] or ''),
                                'text': html.unescape(re.sub(r'<[^>]+>','',g['out']))})

cards = [c for c in cards if c['steps']]
json.dump(cards, open(sys.argv[2],'w'), indent=1)
print(f"cards={len(cards)} steps={sum(len(c['steps']) for c in cards)}")
for c in cards:
    print(f"--- [{c['deck'][:22]} | {c['pg']}] {c['title'][:58]} ({c['kind']})")
    for s in c['steps']:
        print(f"     {s['where']:>3} $ {s['cmd'][:150]}")
