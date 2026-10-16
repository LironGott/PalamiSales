#!/usr/bin/env python3
"""Build the PALAMI pricing page draft (not part of site/ until prices are approved).

  python3 sales/pricing-page/build.py [--preview PATH]

PRICING comes from sales/quote/quote.src.html. Images are inlined from site/img.
Writes sales/pricing-page/index.html (full HTML doc).
"""
import base64, pathlib, re, sys
HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent.parent
quote = (ROOT / "sales/quote/quote.src.html").read_text(encoding="utf-8")
cfg = re.search(r"^var PRICING = \{.*?^\};", quote, re.S | re.M).group(0)
b64 = lambda p: "data:image/webp;base64," + base64.b64encode((ROOT / p).read_bytes()).decode()
svg = (ROOT / "site/img/wordmark-tagline.svg").read_text(encoding="utf-8").strip()
svg = re.sub(r"<\?xml[^>]*>\s*", "", svg)
page = ((HERE / "page.src.html").read_text(encoding="utf-8")
        .replace("/*CONFIG*/", cfg)
        .replace("<!--MASCOT_HEAD-->", b64("site/img/mascot-head.webp"))
        .replace("<!--LOGO_FULL-->", b64("site/img/logo-full.webp"))
        .replace("<!--MASCOT-->", b64("site/img/mascot.webp"))
        .replace("<!--WORDMARK-->", svg))
head_end = page.index("</style>") + len("</style>")
doc = ('<!doctype html>\n<html lang="he" dir="rtl">\n<head>\n<meta charset="utf-8">\n'
       '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
       + page[:head_end] + "\n</head>\n<body>\n" + page[head_end:] + "\n</body>\n</html>\n")
(HERE / "index.html").write_text(doc, encoding="utf-8")
print("wrote sales/pricing-page/index.html", len(doc)//1024, "KB")
if "--preview" in sys.argv:
    p = pathlib.Path(sys.argv[sys.argv.index("--preview") + 1]); p.write_text(page, encoding="utf-8"); print("wrote", p)
