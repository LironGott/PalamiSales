// Print the agreement HTML files to A4 PDF with a running footer (page X of Y + initials).
// Usage: node print.cjs out/agency.html [out/independent.html ...]
const { chromium } = require('playwright');
const { readFileSync } = require('node:fs');
const { pathToFileURL } = require('node:url');
const path = require('node:path');

const here = __dirname;
const root = path.resolve(here, '../../..');
const font = readFileSync(path.join(root, 'site/fonts/assistant-hebrew-27533b.woff2')).toString('base64');
const fontLatin = readFileSync(path.join(root, 'site/fonts/assistant-latin-6cb82b.woff2')).toString('base64');

const footer = (label) => `
<style>
@font-face{font-family:A;src:url(data:font/woff2;base64,${font}) format('woff2');unicode-range:U+0590-05FF,U+200C-2010,U+20AA,U+FB1D-FB4F;}
@font-face{font-family:A;src:url(data:font/woff2;base64,${fontLatin}) format('woff2');unicode-range:U+0000-00FF,U+2000-206F;}
.f{font-family:A,sans-serif;font-size:7.6pt;color:#545D58;width:100%;margin:0 18mm;display:flex;justify-content:space-between;align-items:center;direction:rtl;
   border-top:0.6pt solid #DEE3DF;padding-top:5px;-webkit-print-color-adjust:exact}
.i{display:inline-block;width:22mm;border-bottom:0.6pt solid #9AA39E;height:9px;margin-inline-start:4px}
.n{direction:rtl;unicode-bidi:isolate}
</style>
<div class="f"><span>${label}</span><span>ראשי תיבות<span class="i"></span></span>
<span class="n">עמוד <span class="pageNumber"></span> מתוך <span class="totalPages"></span></span></div>`;

(async () => {
const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' }).catch(() => chromium.launch());
for (const file of process.argv.slice(2)) {
  const page = await browser.newPage();
  await page.goto(pathToFileURL(path.resolve(file)).href, { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);
  const label = await page.title();
  const out = file.replace(/\.html$/, '.pdf');
  await page.pdf({
    path: out, format: 'A4', printBackground: true, preferCSSPageSize: true,
    displayHeaderFooter: true, headerTemplate: '<span></span>', footerTemplate: footer(label),
  });
  console.log('wrote', path.relative(root, path.resolve(out)));
  await page.close();
}
await browser.close();
})();
