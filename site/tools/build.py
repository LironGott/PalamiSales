"""Build the deployable static site into site/dist/.

The page sources in site/ are written as page fragments (head tags + body) so they can be previewed
as a claude.ai artifact. This script turns them into complete HTML documents for hosting:
  - adds <!doctype>, <html lang dir>, charset, viewport, canonical, hreflang, Open Graph and icons
  - swaps Google Fonts for the self-hosted copies in site/fonts/
  - turns explicit index.html links into directory links (en/, ../)
  - copies only the assets the pages use, plus robots.txt, sitemap.xml, 404.html and favicon.ico
  - sets the demo form endpoint when FORM_ENDPOINT is given

Run from the repository root:  python3 site/tools/build.py
Optional: FORM_ENDPOINT=https://... python3 site/tools/build.py
Preview copy for the artifact: python3 site/tools/build.py --preview  (writes site/.preview/)
"""
import os, re, shutil, json, sys

SITE_URL = 'https://palami.io'
FORM_ENDPOINT = os.environ.get('FORM_ENDPOINT', '').strip()
PREVIEW = '--preview' in sys.argv  # keep explicit index.html links, for the claude.ai artifact preview

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.dirname(HERE)
DIST = os.path.join(SRC, '.preview' if '--preview' in sys.argv else 'dist')
BRAND = os.path.join(os.path.dirname(SRC), 'brand')

# (source path, url path, lang, alternate source path)
PAGES = [
    ('index.html', '/', 'he', 'en/index.html'),
    ('en/index.html', '/en/', 'en', 'index.html'),
    ('privacy.html', '/privacy.html', 'he', 'en/privacy.html'),
    ('en/privacy.html', '/en/privacy.html', 'en', 'privacy.html'),
    ('accessibility.html', '/accessibility.html', 'he', 'en/accessibility.html'),
    ('en/accessibility.html', '/en/accessibility.html', 'en', 'accessibility.html'),
]
URL = {p[0]: p[1] for p in PAGES}
GOOGLE_FONTS = re.compile(r'<link rel="preconnect" href="https://fonts\.googleapis\.com">\n<link rel="preconnect" href="https://fonts\.gstatic\.com" crossorigin>\n<link rel="stylesheet" href="https://fonts\.googleapis\.com/[^"]+">\n')


def read(p):
    with open(os.path.join(SRC, p), encoding='utf-8') as f:
        return f.read()


def write(p, s):
    full = os.path.join(DIST, p)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, 'w', encoding='utf-8') as f:
        f.write(s)


def build_page(src, url, lang, alt):
    s = read(src)
    base = '../' if src.startswith('en/') else ''
    # split the fragment into head tags and body
    m = re.search(r'<svg width="0"|<div class="site[ "]', s)
    cut = m.start()
    head, body = s[:cut], s[cut:]
    head = head.replace('<meta name="claude:viewport-fit-sides" content="cover">\n', '')
    head = GOOGLE_FONTS.sub('<link rel="preload" href="%sfonts/fonts.css" as="style">\n<link rel="stylesheet" href="%sfonts/fonts.css">\n' % (base, base), head)
    title = re.search(r'<title>(.*?)</title>', head).group(1)
    desc = re.search(r'<meta name="description" content="([^"]*)">', head).group(1)
    he_url = URL[src] if lang == 'he' else URL[alt]
    en_url = URL[src] if lang == 'en' else URL[alt]
    meta = [
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">',
        '<meta name="theme-color" content="#08402A">',
        f'<link rel="canonical" href="{SITE_URL}{url}">',
        f'<link rel="alternate" hreflang="he" href="{SITE_URL}{he_url}">',
        f'<link rel="alternate" hreflang="en" href="{SITE_URL}{en_url}">',
        f'<link rel="alternate" hreflang="x-default" href="{SITE_URL}{he_url}">',
        f'<link rel="apple-touch-icon" href="{base}img/apple-touch-icon.png">',
        '<meta property="og:type" content="website">',
        '<meta property="og:site_name" content="PALAMI">',
        f'<meta property="og:title" content="{title}">',
        f'<meta property="og:description" content="{desc}">',
        f'<meta property="og:url" content="{SITE_URL}{url}">',
        f'<meta property="og:image" content="{SITE_URL}/img/og-{lang}.png">',
        '<meta property="og:image:width" content="1200">',
        '<meta property="og:image:height" content="630">',
        f'<meta property="og:locale" content="{"he_IL" if lang == "he" else "en_US"}">',
        '<meta name="twitter:card" content="summary_large_image">',
    ]
    # directory-style links on the live site
    if not PREVIEW:
        body = body.replace('href="en/index.html"', 'href="en/"').replace('href="../index.html"', 'href="../"')
        body = re.sub(r'href="index\.html"', 'href="./"', body)
    if FORM_ENDPOINT:
        body = body.replace('id="demo-form" action="#"', 'id="demo-form" action="%s"' % FORM_ENDPOINT)
    d = 'rtl' if lang == 'he' else 'ltr'
    html = f'<!doctype html>\n<html lang="{lang}" dir="{d}">\n<head>\n' + '\n'.join(meta) + '\n' + head.strip() + '\n</head>\n<body>\n' + body.strip() + '\n</body>\n</html>\n'
    write(src, html)
    return html


def main():
    if os.path.isdir(DIST):
        shutil.rmtree(DIST)
    os.makedirs(DIST)
    used = set()
    for src, url, lang, alt in PAGES:
        html = build_page(src, url, lang, alt)
        used.update(re.findall(r'img/([\w.-]+\.(?:webp|png|svg|jpg))', html))
    js = read('js/site.js')
    used.update(re.findall(r"'([\w.-]+\.webp)'", js))
    used.update(['mascot.webp', 'og-he.png', 'og-en.png', 'apple-touch-icon.png', 'favicon-32.png'])
    for d in ('css', 'js', 'fonts'):
        shutil.copytree(os.path.join(SRC, d), os.path.join(DIST, d))
    os.makedirs(os.path.join(DIST, 'img'))
    missing = []
    for name in sorted(used):
        p = os.path.join(SRC, 'img', name)
        if os.path.exists(p):
            shutil.copy(p, os.path.join(DIST, 'img', name))
        else:
            missing.append(name)
    # favicon.ico for browsers that ask for it at the root
    try:
        from PIL import Image
        imgs = [Image.open(os.path.join(BRAND, 'icons', f'favicon-{n}.png')).convert('RGBA') for n in (16, 32, 48)]
        imgs[2].save(os.path.join(DIST, 'favicon.ico'), sizes=[(16, 16), (32, 32), (48, 48)], append_images=imgs[:2])
    except Exception as e:  # PIL missing: the PNG favicon still works
        print('favicon.ico skipped:', e)
    write('robots.txt', f'User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n')
    urls = []
    for src, url, lang, alt in PAGES:
        alt_url = URL[alt]
        he, en = (url, alt_url) if lang == 'he' else (alt_url, url)
        urls.append(f'  <url><loc>{SITE_URL}{url}</loc>'
                    f'<xhtml:link rel="alternate" hreflang="he" href="{SITE_URL}{he}"/>'
                    f'<xhtml:link rel="alternate" hreflang="en" href="{SITE_URL}{en}"/></url>')
    write('sitemap.xml', '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + '\n'.join(urls) + '\n</urlset>\n')
    write('404.html', '''<!doctype html>
<html lang="he" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>העמוד לא נמצא · PALAMI</title>
<link rel="icon" href="/img/favicon-32.png">
<link rel="stylesheet" href="/fonts/fonts.css">
<link rel="stylesheet" href="/css/site.css">
</head>
<body>
<main class="site doc nf" dir="rtl" lang="he"><div class="in">
  <img src="/img/mascot.webp" alt="">
  <h1>העמוד לא נמצא</h1>
  <p>אולי הקישור השתנה. אפשר לחזור לעמוד הבית.</p>
  <a class="btn" href="/">לעמוד הבית</a>
  <p class="alt" lang="en" dir="ltr">Page not found. <a href="/en/">Go to the English home page</a></p>
</div></main>
</body>
</html>
''')
    size = sum(os.path.getsize(os.path.join(r, f)) for r, _, fs in os.walk(DIST) for f in fs)
    print(json.dumps({'pages': len(PAGES), 'images': len(used) - len(missing), 'missing': missing,
                      'form_endpoint': FORM_ENDPOINT or None, 'total_kb': size // 1024}, ensure_ascii=False))


if __name__ == '__main__':
    main()
