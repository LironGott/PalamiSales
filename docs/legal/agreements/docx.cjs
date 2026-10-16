// Build the editable Word versions of the agreements for legal review.
// Usage (from this folder): python3 export_json.py && node docx.cjs
// Output: out/<file>-legal-review.docx, with track changes switched on and a first page of open questions for the lawyer.
const fs = require('node:fs');
const path = require('node:path');
const {
  Document, Packer, Paragraph, TextRun, ImageRun, Table, TableRow, TableCell, Header, Footer,
  AlignmentType, WidthType, BorderStyle, ShadingType, PageNumber, PageBreak, TabStopType, TableLayoutType,
} = require('docx');

const here = __dirname;
const root = path.resolve(here, '../../..');
const OUT = path.join(here, 'out');

const FONT = 'Arial';               // Hebrew-safe on every Word install
const GREEN = '08402A', COPPER = 'C37237', MUTED = '545D58', LINE = 'DEE3DF', CREAM = 'FCF4EC', SOFT = 'EEF6F1';
const PAGE_W = 11906, MARGIN = 1134; // A4, 2 cm margins
const CONTENT_W = PAGE_W - 2 * MARGIN;
const logo = fs.readFileSync(path.join(root, 'brand/logo/png/wordmark-tagline.png'));

const run = (text, o = {}) => new TextRun({
  text, rightToLeft: true, font: { ascii: FONT, hAnsi: FONT, cs: FONT },
  size: o.size || 21, sizeComplexScript: o.size || 21, bold: o.bold, boldComplexScript: o.bold,
  color: o.color, ...(o.extra || {}),
});
const para = (children, o = {}) => new Paragraph({
  bidirectional: true, alignment: o.align || AlignmentType.BOTH,
  spacing: { before: o.before ?? 0, after: o.after ?? 100, line: o.line || 300 },
  children: Array.isArray(children) ? children : [children], ...(o.extra || {}),
});
const p = (text, o = {}) => para(run(text, o), o);

const noBorder = { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' };
const thin = { style: BorderStyle.SINGLE, size: 4, color: LINE };
const cell = (children, w, o = {}) => new TableCell({
  width: { size: w, type: WidthType.DXA },
  shading: o.fill ? { type: ShadingType.CLEAR, color: 'auto', fill: o.fill } : undefined,
  margins: { top: 90, bottom: 90, left: 140, right: 140 },
  borders: o.borders || { top: noBorder, bottom: thin, left: noBorder, right: noBorder },
  children,
});
const table = (rows, widths, o = {}) => new Table({
  width: { size: widths.reduce((a, b) => a + b, 0), type: WidthType.DXA },
  columnWidths: widths, visuallyRightToLeft: true, layout: TableLayoutType.FIXED, rows, ...(o.extra || {}),
});

const sectionHeading = (n, title) => para([run(`${n}.  `, { bold: true, color: COPPER, size: 24 }), run(title, { bold: true, color: GREEN, size: 24 })],
  { before: 220, after: 80, align: AlignmentType.START, extra: { keepNext: true } });
const clauseItem = (n, text) => para([run(n, { color: MUTED, size: 19 }), run('\t'), run(text)], {
  extra: { indent: { start: 680, hanging: 680 }, tabStops: [{ type: TabStopType.START, position: 680 }] },
});

function memo(d) {
  const out = [
    p('לבדיקה משפטית: נקודות פתוחות', { bold: true, color: GREEN, size: 30, after: 60, align: AlignmentType.START }),
    p(`${d.doc_title} · נוסח ${d.version} · ${d.date}`, { color: MUTED, after: 200, align: AlignmentType.START }),
    p('שלום, זה נוסח ראשון שהכנו על בסיס מחקר, ולא חוות דעת משפטית. מעקב השינויים פעיל, כך שכל תיקון יסומן. אלה הנקודות שנשמח שתבדקו במיוחד:', { after: 160 }),
  ];
  d.review_notes.forEach((t, i) => out.push(clauseItem(`${i + 1}.`, t)));
  out.push(p('יש למחוק את העמוד הזה לפני שליחת ההסכם ללקוח.', { color: COPPER, bold: true, before: 200 }));
  out.push(new Paragraph({ children: [new PageBreak()] }));
  return out;
}

function parties(d) {
  const w = CONTENT_W / 2;
  const box = (pt) => cell([
    p(pt.role, { color: COPPER, bold: true, size: 18, after: 40, align: AlignmentType.START }),
    p(pt.name, { color: GREEN, bold: true, size: 24, after: 80, align: AlignmentType.START }),
    ...pt.rows.map(([k, v]) => para([run(k + ': ', { color: MUTED }), run(v)], { after: 60, align: AlignmentType.START })),
    p(pt.as, { color: MUTED, size: 18, before: 60, after: 0, align: AlignmentType.START }),
  ], w, { borders: { top: thin, bottom: thin, left: thin, right: thin } });
  return table([new TableRow({ children: d.parties.map(box) })], [w, w]);
}

function summary(d) {
  return table([new TableRow({ children: [cell([
    p('בקצרה, לפני הסעיפים', { bold: true, color: GREEN, size: 24, after: 100, align: AlignmentType.START }),
    ...d.summary.map((t) => para([run('✓  ', { color: '5E9677', bold: true }), run(t)], { after: 60, align: AlignmentType.START })),
    p(d.summary_note, { color: MUTED, size: 18, before: 80, after: 0, align: AlignmentType.START }),
  ], CONTENT_W, { fill: CREAM, borders: { top: thin, bottom: thin, left: thin, right: thin } })] })], [CONTENT_W]);
}

function annexBlock(b) {
  if (b.type === 'h3') return [p(b.text, { bold: true, color: GREEN, size: 22, before: 160, after: 60, align: AlignmentType.START, extra: { keepNext: true } })];
  if (b.type === 'p') return [p(b.text, { align: AlignmentType.START })];
  const cols = b.rows[0].length;
  const widths = cols === 2 ? [Math.round(CONTENT_W * 0.26), CONTENT_W - Math.round(CONTENT_W * 0.26)] : Array(cols).fill(Math.floor(CONTENT_W / cols));
  widths[widths.length - 1] += CONTENT_W - widths.reduce((a, c) => a + c, 0);
  const firstColBold = cols === 2;
  return [table(b.rows.map((r) => new TableRow({
    tableHeader: r[0].th, cantSplit: true,
    children: r.map((c, i) => cell([p(c.text, {
      bold: c.th || (firstColBold && i === 0), color: c.th ? GREEN : undefined, size: c.th ? 19 : 20, after: 0, align: AlignmentType.START, line: 276,
    })], widths[i], { fill: c.th ? SOFT : undefined })),
  })), widths), p('', { after: 60 })];
}

function annex(a) {
  return [
    new Paragraph({ children: [new PageBreak()] }),
    p(a.kicker, { color: COPPER, bold: true, size: 19, after: 20, align: AlignmentType.START }),
    para(run(a.title, { bold: true, color: GREEN, size: 32 }), {
      after: 200, align: AlignmentType.START,
      extra: { border: { bottom: { style: BorderStyle.SINGLE, size: 12, color: GREEN, space: 6 } } },
    }),
    ...a.blocks.flatMap(annexBlock),
  ];
}

function signatures(s) {
  const w = CONTENT_W / 2;
  const card = ([role, fields, cap]) => cell([
    p(role, { color: COPPER, bold: true, size: 19, after: 120, align: AlignmentType.START }),
    ...fields.map((f) => para([run(f + ':  '), run('_______________________', { color: MUTED })], { after: 160, align: AlignmentType.START })),
    p('', { after: 300 }),
    p('_______________________________', { color: '16211C', after: 20, align: AlignmentType.START }),
    p(cap, { color: MUTED, size: 18, after: 0, align: AlignmentType.START }),
  ], w, { borders: { top: thin, bottom: thin, left: thin, right: thin } });
  return [
    para(run('ולראיה באו הצדדים על החתום', { bold: true, color: GREEN, size: 26 }), {
      before: 360, after: 60, align: AlignmentType.START,
      extra: { keepNext: true, border: { top: { style: BorderStyle.SINGLE, size: 12, color: GREEN, space: 10 } } },
    }),
    p(s.note, { color: MUTED, size: 19, after: 160, align: AlignmentType.START, extra: { keepNext: true } }),
    table([new TableRow({ cantSplit: true, children: [card(s.palami), card(s.other)] })], [w, w]),
  ];
}

function build(v) {
  const d = JSON.parse(fs.readFileSync(path.join(OUT, `agreement-${v}.json`), 'utf8'));
  const header = new Header({ children: [
    new Paragraph({ bidirectional: true, alignment: AlignmentType.START, children: [
      new ImageRun({ type: 'png', data: logo, transformation: { width: 120, height: 40 } }),
    ] }),
  ] });
  const footer = new Footer({ children: [para([
    run(`${d.doc_title} · נוסח ${d.version}`, { color: MUTED, size: 16 }),
    run('\tראשי תיבות: ____________', { color: MUTED, size: 16 }),
    run('\tעמוד ', { color: MUTED, size: 16 }),
    new TextRun({ children: [PageNumber.CURRENT], size: 16, color: MUTED, font: FONT, rightToLeft: true }),
    run(' מתוך ', { color: MUTED, size: 16 }),
    new TextRun({ children: [PageNumber.TOTAL_PAGES], size: 16, color: MUTED, font: FONT, rightToLeft: true }),
  ], { align: AlignmentType.START, after: 0, extra: {
    tabStops: [{ type: TabStopType.CENTER, position: CONTENT_W / 2 }, { type: TabStopType.END, position: CONTENT_W }],
    border: { top: { style: BorderStyle.SINGLE, size: 4, color: LINE, space: 4 } },
  } })] });

  const body = [
    ...memo(d),
    para(run(`מספר הסכם: ________   ·   נוסח ${d.version} · ${d.date}`, { color: MUTED, size: 18 }), { align: AlignmentType.END, after: 120 }),
    p(d.title, { bold: true, color: GREEN, size: 44, after: 40, align: AlignmentType.START }),
    p(d.subtitle, { color: MUTED, size: 24, after: 240, align: AlignmentType.START }),
    parties(d), p('', { after: 120 }),
    summary(d), p('', { after: 120 }),
    p('לכן הוסכם בין הצדדים כך:', { bold: true, color: GREEN, size: 22, after: 60, align: AlignmentType.START }),
    ...d.clauses.flatMap((c) => [sectionHeading(c.n, c.title), ...c.items.map((it) => clauseItem(it.n, it.text))]),
    ...d.annexes.flatMap(annex),
    ...signatures(d.signatures),
  ];

  const doc = new Document({
    creator: 'PALAMI', title: d.doc_title, description: 'נוסח לבדיקה משפטית',
    features: { trackRevisions: true },
    styles: { default: { document: { run: { font: FONT, size: 21, rightToLeft: true }, paragraph: { bidirectional: true } } } },
    sections: [{
      properties: { page: { size: { width: PAGE_W, height: 16838 }, margin: { top: 1300, bottom: 1100, left: MARGIN, right: MARGIN, header: 500, footer: 500 } } },
      headers: { default: header }, footers: { default: footer }, children: body,
    }],
  });
  const file = path.join(OUT, JSON.parse(JSON.stringify(d)).doc_title && `${v === 'agency' ? 'palami-agreement-agency' : 'palami-agreement-independent'}-legal-review.docx`);
  return Packer.toBuffer(doc).then((buf) => { fs.writeFileSync(file, buf); console.log('wrote', path.relative(root, file)); });
}

Promise.all(['agency', 'independent'].map(build)).catch((e) => { console.error(e); process.exit(1); });
