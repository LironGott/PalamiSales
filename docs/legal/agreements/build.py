"""Build the PALAMI service agreements (agency + independent agent) as self-contained HTML and PDF.

Run from the repo root:  python3 docs/legal/agreements/build.py
Output: docs/legal/agreements/out/*.html and *.pdf (PDF via Chromium, see print.cjs).

The clause texts live in content.py. A text may differ by version with V("agency", "independent").
"""
import base64, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
OUT = os.path.join(HERE, 'out')
sys.path.insert(0, HERE)
import content  # noqa: E402


def b64(path, mime):
    with open(os.path.join(ROOT, path), 'rb') as f:
        return f'data:{mime};base64,' + base64.b64encode(f.read()).decode()


def fonts_css():
    css = open(os.path.join(ROOT, 'site/fonts/fonts.css'), encoding='utf-8').read()
    # Keep only the families we use in print (Rubik + Assistant); inline the files.
    blocks = re.findall(r'@font-face\s*{[^}]*}', css)
    keep = [b for b in blocks if "'Rubik'" in b or "'Assistant'" in b]
    def inline(m):
        return 'url(' + b64('site/fonts/' + m.group(1), 'font/woff2') + ')'
    return '\n'.join(re.sub(r'url\(([^)]+\.woff2)\)', inline, b) for b in keep)


LOGO = b64('brand/logo/svg/wordmark-tagline.svg', 'image/svg+xml')
WORDMARK = b64('brand/logo/svg/wordmark.svg', 'image/svg+xml')
MASCOT = b64('brand/mascot/mascot-head.png', 'image/png')

CSS = r'''
@page { size: A4; margin: 22mm 18mm 20mm 18mm; }
:root {
  --green: #08402A; --green-soft: #EEF6F1; --copper: #C37237; --cream: #F9E2C5; --cream-soft: #FCF4EC;
  --ink: #16211C; --muted: #545D58; --line: #DEE3DF; --paper: #FFFFFF;
}
* { box-sizing: border-box; }
html { background: #E9ECE9; }
body { margin: 0; direction: rtl; color: var(--ink); background: #E9ECE9;
  font: 400 10.6pt/1.62 "Assistant", "Rubik", Arial, sans-serif; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
.sheet { max-width: 210mm; margin: 24px auto; padding: 18mm 18mm 16mm; background: var(--paper);
  box-shadow: 0 1px 2px rgb(21 26 23 / .06), 0 8px 28px rgb(21 26 23 / .10); }
@media print { html, body { background: #fff; } .sheet { margin: 0; padding: 0; box-shadow: none; max-width: none; } .screen-only { display: none !important; } }
@media screen and (max-width: 640px) { .sheet { margin: 0; padding: 22px 16px; box-shadow: none; } body { font-size: 15px; } }
.ltr { direction: ltr; unicode-bidi: isolate; }
h1, h2, h3, .display { font-family: "Rubik", "Assistant", Arial, sans-serif; color: var(--green); }

/* Cover */
.cover-top { display: flex; align-items: center; justify-content: space-between; gap: 16px;
  padding-bottom: 14px; border-bottom: 2px solid var(--green); }
.cover-top .logo { height: 54px; }
.cover-top .meta { font-size: 9pt; color: var(--muted); text-align: left; line-height: 1.5; }
.cover-top .meta b { color: var(--ink); font-weight: 600; }
.title { margin: 26px 0 4px; font-size: 25pt; line-height: 1.15; font-weight: 700; letter-spacing: -.01em; }
.subtitle { margin: 0 0 22px; font-size: 12.5pt; color: var(--muted); }
.subtitle .dot { color: var(--copper); padding: 0 6px; }

/* Parties */
.parties { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin: 0 0 18px; }
@media screen and (max-width: 640px) { .parties, .sign { grid-template-columns: 1fr !important; } }
.party { border: 1px solid var(--line); border-radius: 10px; padding: 12px 14px; break-inside: avoid; }
.party .role { font: 600 8.5pt/1 "Rubik", sans-serif; color: var(--copper); letter-spacing: .02em; margin-bottom: 6px; }
.party .name { font: 600 12pt/1.3 "Rubik", sans-serif; color: var(--green); margin-bottom: 4px; }
.row { display: flex; align-items: baseline; gap: 6px; margin-top: 5px; font-size: 9.8pt; }
.row .k { color: var(--muted); white-space: nowrap; }
.row .v { flex: 1; }
.fill { display: inline-block; min-width: 9em; border-bottom: 1px solid #9AA39E; height: 1.1em; vertical-align: baseline; }
.fill.w-s { min-width: 4.5em; } .fill.w-l { min-width: 16em; }
.row .v { display: flex; } .row .v .fill { flex: 1; min-width: 0; }
.sig .row > .fill { flex: 1; min-width: 0; }
.party .as { margin-top: 8px; font-size: 9pt; color: var(--muted); }

/* Summary box */
.summary { background: var(--cream-soft); border: 1px solid #F1D9BC; border-radius: 12px; padding: 14px 18px 12px;
  margin: 0 0 22px; break-inside: avoid; position: relative; }
.summary h2 { margin: 0 0 8px; font-size: 13pt; display: flex; align-items: center; gap: 8px; }
.summary h2 img { width: 30px; height: 30px; }
.summary ul { list-style: none; margin: 0; padding: 0; display: grid; grid-template-columns: 1fr 1fr; gap: 6px 22px; }
@media screen and (max-width: 640px) { .summary ul { grid-template-columns: 1fr; } }
.summary li { position: relative; padding-inline-start: 22px; font-size: 10pt; line-height: 1.5; }
.summary li::before { content: ""; position: absolute; inset-inline-start: 0; top: .3em; width: 13px; height: 13px; border-radius: 50%;
  background: #5E9677 url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E%3Cpath d='M4 8.4l2.6 2.5L12 5.4' fill='none' stroke='white' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E") center/11px no-repeat; }
.summary li b { color: var(--green); font-weight: 600; }
.summary .note { margin: 10px 0 0; font-size: 8.8pt; color: var(--muted); }

.agreed { font: 600 11pt/1.4 "Rubik", sans-serif; color: var(--green); margin: 4px 0 10px; }

/* Clauses */
.clause { margin: 0 0 12px; }
.clause h2 { font-size: 12.2pt; font-weight: 600; margin: 16px 0 6px; display: flex; gap: 8px; align-items: baseline;
  break-after: avoid; }
.clause h2 .n { display: inline-grid; place-items: center; min-width: 22px; height: 22px; padding: 0 4px; border-radius: 6px;
  background: var(--green-soft); color: var(--green); font-size: 10pt; }
.clause ol { list-style: none; margin: 0; padding: 0; counter-reset: sub; }
.clause li { position: relative; padding-inline-start: 34px; margin: 0 0 6px; text-align: justify; }
.clause li::before { content: attr(data-n); position: absolute; right: 0; top: 0; color: var(--muted);
  font-size: 9.2pt; font-variant-numeric: tabular-nums; direction: ltr; unicode-bidi: isolate; }
.clause li ul { margin: 4px 0 0; padding-inline-start: 18px; }
.clause li ul li { padding-inline-start: 0; margin-bottom: 2px; }
.clause li ul li::before { content: none; }
.clause li ul li::marker { color: var(--copper); }

/* Annex */
.annex { break-before: page; }
.annex-head { display: flex; align-items: center; justify-content: space-between; border-bottom: 2px solid var(--green);
  padding-bottom: 10px; margin-bottom: 14px; }
.annex-head h1 { margin: 0; font-size: 17pt; }
.annex-head h1 small { display: block; font: 600 9pt/1.2 "Rubik", sans-serif; color: var(--copper); margin-bottom: 4px; }
.annex-head img { height: 26px; }
.lead { color: var(--muted); margin: 0 0 12px; }
table { width: 100%; border-collapse: collapse; margin: 6px 0 12px; font-size: 9.6pt; }
tr { break-inside: avoid; } .box table { break-inside: avoid; }
th { background: var(--green-soft); color: var(--green); font: 600 9.2pt/1.3 "Rubik", sans-serif; text-align: start; padding: 7px 10px; }
td { border-bottom: 1px solid var(--line); padding: 6px 10px; vertical-align: top; }
td .fill { min-width: 6em; }
.box { border: 1px solid var(--line); border-radius: 10px; padding: 9px 14px 4px; margin: 0 0 9px; break-inside: avoid; }
.box p { margin: 4px 0 8px; } .box table { margin: 4px 0 8px; }
.box h3 { margin: 0 0 6px; font-size: 11pt; display: flex; gap: 8px; align-items: center; }
.cb { display: inline-block; width: 12px; height: 12px; border: 1.4px solid var(--green); border-radius: 3px; flex: none; }
.muted { color: var(--muted); }
.small { font-size: 9pt; }

/* Signatures */
.signing { break-inside: avoid; margin-top: 30px; padding-top: 18px; border-top: 2px solid var(--green); }
.signing h2 { font-size: 13pt; margin: 0 0 4px; }
.sign { display: grid; grid-template-columns: 1fr 1fr; gap: 18px; margin-top: 12px; }
.sig { border: 1px solid var(--line); border-radius: 12px; padding: 14px 16px 16px; }
.sig .role { font: 600 9pt/1 "Rubik", sans-serif; color: var(--copper); margin-bottom: 8px; }
.sig .row { margin-top: 10px; }
.sig .line { height: 46px; border-bottom: 1.4px solid var(--ink); margin-top: 14px; }
.sig .cap { font-size: 8.8pt; color: var(--muted); margin-top: 4px; display: flex; justify-content: space-between; }
.endmark { text-align: center; margin-top: 18px; color: var(--muted); font-size: 9pt; }
.endmark img { width: 34px; height: 34px; display: block; margin: 0 auto 4px; opacity: .9; }

.screen-bar { max-width: 210mm; margin: 16px auto 0; display: flex; gap: 10px; justify-content: space-between; align-items: center;
  font-size: 14px; color: var(--muted); padding: 0 4px; }
.screen-bar a { color: var(--green); font-weight: 600; }
'''


def esc_fill(text):
    """[[ ]] -> blank fill-in line; [[s]] short, [[l]] long."""
    text = text.replace('[[s]]', '<span class="fill w-s"></span>')
    text = text.replace('[[l]]', '<span class="fill w-l"></span>')
    return text.replace('[[]]', '<span class="fill"></span>')


def pick(x, v):
    return x[v] if isinstance(x, dict) else x


def render_clauses(clauses, v):
    out = []
    for i, (title, items) in enumerate(clauses, 1):
        lis = []
        j = 0
        for it in items:
            it = pick(it, v)
            if it is None:
                continue
            j += 1
            if isinstance(it, tuple):  # (text, [bullets])
                body = esc_fill(pick(it[0], v)) + '<ul>' + ''.join(f'<li>{esc_fill(pick(b, v))}</li>' for b in it[1]) + '</ul>'
            else:
                body = esc_fill(it)
            lis.append(f'<li data-n="{i}.{j}">{body}</li>')
        out.append(f'<section class="clause" id="s{i}"><h2><span class="n">{i}</span>{pick(title, v)}</h2><ol>{"".join(lis)}</ol></section>')
    return '\n'.join(out)


def render(v):
    c = content
    meta = c.META[v]
    parties = ''.join(
        f'''<div class="party"><div class="role">{p["role"]}</div><div class="name">{p["name"]}</div>
        {''.join(f'<div class="row"><span class="k">{k}</span><span class="v">{esc_fill(val)}</span></div>' for k, val in p["rows"])}
        <div class="as">{p["as"]}</div></div>''' for p in c.PARTIES[v])
    summary = ''.join(f'<li>{pick(s, v)}</li>' for s in c.SUMMARY)
    annexes = ''.join(
        f'''<section class="annex" id="annex-{a["id"]}"><div class="annex-head"><h1><small>{a["kicker"]}</small>{a["title"]}</h1>
        <img src="{WORDMARK}" alt="PALAMI"></div>{esc_fill(pick(a["html"], v))}</section>''' for a in c.annexes(v))
    sign = c.signatures(v)
    return f'''<!doctype html>
<html lang="he" dir="rtl" data-product="agent">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{meta["doc_title"]}</title>
<style>{fonts_css()}{CSS}</style>
</head>
<body>
<div class="screen-bar screen-only" dir="rtl" lang="he"><span>{meta["screen_note"]}</span><span><a href="{c.META[meta["other"]]["file"]}.html">{c.META[meta["other"]]["title"]}</a></span></div>
<main class="sheet" dir="rtl" lang="he">
  <header class="cover-top">
    <img class="logo" src="{LOGO}" alt="PALAMI · כל פרטי הנסיעה בכף ידך">
    <div class="meta">מספר הסכם: <span class="fill w-s"></span><br>נוסח <b class="ltr">{c.VERSION}</b> · {c.VERSION_DATE}</div>
  </header>
  <h1 class="title">{meta["title"]}</h1>
  <p class="subtitle">{meta["subtitle"]}</p>
  <div class="parties">{parties}</div>
  <aside class="summary" aria-label="בקצרה">
    <h2><img src="{MASCOT}" alt="">בקצרה, לפני הסעיפים</h2>
    <ul>{summary}</ul>
    <p class="note">{c.SUMMARY_NOTE}</p>
  </aside>
  <p class="agreed">לכן הוסכם בין הצדדים כך:</p>
  {render_clauses(c.CLAUSES, v)}
  {annexes}
  {sign}
</main>
</body>
</html>'''


def main():
    os.makedirs(OUT, exist_ok=True)
    built = []
    for v in ('agency', 'independent'):
        path = os.path.join(OUT, content.META[v]['file'] + '.html')
        with open(path, 'w', encoding='utf-8') as f:
            f.write(render(v))
        built.append(path)
        print('wrote', os.path.relpath(path, ROOT))
    # Artifact preview: the main page without the document skeleton (the publisher adds it).
    prev = os.path.join(OUT, 'preview.html')
    page = open(built[0], encoding='utf-8').read()
    page = re.sub(r'<!doctype html>\s*<html[^>]*>\s*<head>\s*', '', page)
    page = page.replace('</head>\n<body>\n', '').replace('</body>\n</html>', '')
    with open(prev, 'w', encoding='utf-8') as f:
        f.write(page)
    if '--no-pdf' not in sys.argv:
        subprocess.run(['node', os.path.join(HERE, 'print.cjs'), *built], check=True)


if __name__ == '__main__':
    main()
