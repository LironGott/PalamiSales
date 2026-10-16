#!/usr/bin/env python3
"""Build the PALAMI quote page.

  python3 sales/quote/build.py            -> sales/quote/offer/index.html (full HTML doc, upload to www.palami.io/offer/)
  python3 sales/quote/build.py --preview  -> also writes a fragment for the claude.ai artifact preview (path printed)

Source: sales/quote/quote.src.html. Placeholders: <!--LOGO--> inline wordmark, <!--LOGO_FULL--> full logo with the beaver, <!--MASCOT--> (dark mode). Needs Pillow.
"""
import pathlib, re, sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent.parent
src = (HERE / "quote.src.html").read_text(encoding="utf-8")

logo = (ROOT / "brand/logo/svg/wordmark.svg").read_text(encoding="utf-8")
logo = re.sub(r'\swidth="[^"]*"\s+height="[^"]*"', "", logo, count=1)
logo = logo.replace('fill="#08402A"', 'style="fill:var(--logo-ink)"').replace('fill="#C37237"', 'style="fill:var(--logo-dot)"')
import base64, io
from PIL import Image
def data_uri(path, width):
    im = Image.open(ROOT / path)
    im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    buf = io.BytesIO(); im.save(buf, "WEBP", quality=88, method=6)
    return "data:image/webp;base64," + base64.b64encode(buf.getvalue()).decode()
page = (src.replace("<!--LOGO-->", logo.strip())
           .replace("<!--LOGO_FULL-->", data_uri("brand/logo/png/logo-full.png", 600))
           .replace("<!--MASCOT-->", data_uri("brand/mascot/mascot.png", 128)))

head_end = page.index("</style>") + len("</style>")
doc = ('<!doctype html>\n<html lang="he" dir="rtl" data-product="agent">\n<head>\n<meta charset="utf-8">\n'
       '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
       '<link rel="icon" href="/favicon.ico">\n'
       + page[:head_end] + "\n</head>\n<body>\n" + page[head_end:] + "\n</body>\n</html>\n")
out = HERE / "offer" / "index.html"
out.parent.mkdir(exist_ok=True)
out.write_text(doc, encoding="utf-8")
print("wrote", out.relative_to(ROOT))

if "--preview" in sys.argv:
    i = sys.argv.index("--preview")
    prev = pathlib.Path(sys.argv[i + 1]) if len(sys.argv) > i + 1 else HERE / ".preview.html"
    prev.write_text(page, encoding="utf-8")
    print("wrote", prev)
