"""Export the agreement content (content.py) as plain JSON blocks for the Word build (docx.cjs).

Run from the repo root:  python3 docs/legal/agreements/export_json.py  -> out/agreement-<version>.json
Fill-in blanks become underscores, checkboxes become ☐, and other HTML is reduced to text.
"""
import html, json, os, re, sys
from html.parser import HTMLParser

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'out')
sys.path.insert(0, HERE)
import content  # noqa: E402

FILLS = {'[[s]]': '________', '[[l]]': '______________________________', '[[]]': '________________'}


def text(s):
    for k, f in FILLS.items():
        s = s.replace(k, f)
    s = s.replace('<span class="cb"></span>', '☐')
    s = s.replace('&nbsp;', ' ')
    s = re.sub(r'<[^>]+>', '', s)
    return re.sub(r'\s+', ' ', html.unescape(s)).strip()


def pick(x, v):
    return x[v] if isinstance(x, dict) else x


class Blocks(HTMLParser):
    """Reduce an annex HTML fragment to p / h3 / table blocks."""

    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.blocks, self.buf, self.row, self.rows, self.in_cell, self.header = [], [], None, None, False, False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ('p', 'h3'):
            self.buf = []
        elif tag == 'table':
            self.rows, self.header = [], False
        elif tag == 'tr':
            self.row = []
        elif tag in ('td', 'th'):
            self.in_cell, self.buf = True, []
            self.header = self.header or tag == 'th'
        elif tag == 'span' and a.get('class', '').startswith('fill'):
            cls = a['class']
            self.buf.append('[[s]]' if 'w-s' in cls else '[[l]]' if 'w-l' in cls else '[[]]')
        elif tag == 'span' and a.get('class') == 'cb':
            self.buf.append('☐ ')

    def handle_endtag(self, tag):
        if tag in ('p', 'h3') and not self.in_cell:
            t = text(''.join(self.buf))
            if t:
                self.blocks.append({'type': tag, 'text': t})
            self.buf = []
        elif tag in ('td', 'th'):
            self.row.append({'text': text(''.join(self.buf)), 'th': tag == 'th'})
            self.in_cell, self.buf = False, []
        elif tag == 'tr':
            self.rows.append(self.row)
        elif tag == 'table':
            self.blocks.append({'type': 'table', 'rows': self.rows})
            self.rows = None

    def handle_data(self, d):
        self.buf.append(d)

    def handle_entityref(self, name):
        self.buf.append(f'&{name};')


def annex_blocks(h):
    p = Blocks()
    p.feed(h)
    return p.blocks


def export(v):
    c = content
    clauses = []
    for i, (title, items) in enumerate(c.CLAUSES, 1):
        out, j = [], 0
        for it in items:
            it = pick(it, v)
            if it is None:
                continue
            j += 1
            out.append({'n': f'{i}.{j}', 'text': text(it)})
        clauses.append({'n': str(i), 'title': text(pick(title, v)), 'items': out})
    sig = {
        'agency': {'note': 'החתימה נעשית פעם אחת, בידי מנהל או מנהלת הסוכנות, ומכסה את ההסכם ואת כל הנספחים. העובדים לא צריכים לחתום.',
                   'other': ['הסוכנות', ['שם החותם/ת', 'תפקיד', 'ח.פ. / ע.מ.', 'תאריך'], 'חתימה וחותמת']},
        'independent': {'note': 'החתימה נעשית פעם אחת ומכסה את ההסכם ואת כל הנספחים.',
                        'other': ['העסק', ['שם מלא', 'ת.ז. / מס׳ עוסק', 'תאריך'], 'חתימה']},
    }[v]
    return {
        'version': c.VERSION, 'date': c.VERSION_DATE,
        'title': c.META[v]['title'], 'subtitle': text(c.META[v]['subtitle'].replace('<span class="dot">•</span>', ' · ')),
        'doc_title': c.META[v]['doc_title'],
        'parties': [{'role': p['role'], 'name': p['name'], 'as': p['as'],
                     'rows': [[k, text(val)] for k, val in p['rows']]} for p in c.PARTIES[v]],
        'summary': [text(pick(s, v)) for s in c.SUMMARY], 'summary_note': c.SUMMARY_NOTE,
        'clauses': clauses,
        'annexes': [{'kicker': a['kicker'], 'title': a['title'], 'blocks': annex_blocks(pick(a['html'], v))} for a in c.annexes(v)],
        'signatures': {'note': sig['note'], 'palami': ['PALAMI', ['שם החותם/ת', 'תפקיד', 'תאריך'], 'חתימה'], 'other': sig['other']},
        'review_notes': c.REVIEW_NOTES[v],
    }


def main():
    os.makedirs(OUT, exist_ok=True)
    for v in ('agency', 'independent'):
        path = os.path.join(OUT, f'agreement-{v}.json')
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(export(v), f, ensure_ascii=False, indent=1)
        print('wrote', os.path.relpath(path))


if __name__ == '__main__':
    main()
