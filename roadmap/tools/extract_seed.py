#!/usr/bin/env python3
"""Build seed/seed.json from the original roadmap file (source/palami-roadmap-drag.html).

The source file is read as data only and is never modified. Every text is copied
verbatim; new fields (status, progress, assignee) start empty or as "proposal" so
no progress is invented.

Usage: python3 roadmap/tools/extract_seed.py
"""
import hashlib, html, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'source' / 'palami-roadmap-drag.html'
OUT = ROOT / 'seed' / 'seed.json'
SOURCE_SHA256 = '93d8f87239b95c345e8873d9b83c7a7287b4e72d26dffa679955973266116ff1'


def text_of(fragment):
    return html.unescape(re.sub(r'<[^>]+>', '', fragment)).strip()


def one(pattern, src):
    found = re.findall(pattern, src, re.S)
    if len(found) != 1:
        sys.exit(f'expected exactly one match for {pattern!r}, got {len(found)}')
    return found[0]


def main():
    raw = SRC.read_bytes()
    if hashlib.sha256(raw).hexdigest() != SOURCE_SHA256:
        sys.exit('source file changed; check it before re-extracting')
    src = raw.decode('utf-8')
    seed = json.loads(one(r'<script type="application/json" id="seed">(.*?)</script>', src))

    tasks = []
    for i, t in enumerate(seed['tasks']):
        tasks.append({**t, 'order': (i + 1) * 10, 'status': 'proposal', 'progress': None, 'assignee': ''})
    agencies = [{'id': f'a{i + 1}', 'order': (i + 1) * 10, **a} for i, a in enumerate(seed['agencies'])]

    panel = one(r'<section class="panel"><h2>למי פונים, ובאיזה שלב</h2>(.*?)</section>', src)
    muted = re.findall(r'<p class="muted">(.*?)</p>', panel, re.S)
    sales = one(r'<summary>תוכנית העבודה למכירות</summary>(.*?)</details>', panel)
    sales_paras = [text_of(p) for p in re.findall(r'<p>(.*?)</p>', sales, re.S)]
    footer = text_of(one(r'<footer>(.*?)</footer>', src))
    footer_plan = footer[footer.index('שנה 1:'):]

    texts = {
        'title': text_of(one(r'<h1>(.*?)</h1>', src)),
        'subtitle': text_of(one(r'<div class="sub">(.*?)</div>', src)),
        'audienceIntro': text_of(muted[0]),
        'agencyNote': text_of(muted[1]),
        'salesPlan': '\n\n'.join(sales_paras),
        'planNote': footer_plan,
    }
    out = {
        'format': 'palami-roadmap-seed',
        'source': {'file': 'source/palami-roadmap-drag.html', 'sha256': SOURCE_SHA256, 'instance': seed['instance']},
        'tasks': tasks,
        'agencies': agencies,
        'texts': texts,
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'wrote {OUT.relative_to(ROOT)}: {len(tasks)} tasks, {len(agencies)} agencies, {len(texts)} texts')


if __name__ == '__main__':
    main()
