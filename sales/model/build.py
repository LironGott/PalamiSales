#!/usr/bin/env python3
"""Build the PALAMI profitability model.

  python3 sales/model/build.py [--preview PATH]

Takes PRICING and COSTS from sales/quote/quote.src.html (one source of truth) and writes
sales/model/index.html (full HTML doc). --preview also writes the fragment for the artifact.
"""
import pathlib, re, sys
HERE = pathlib.Path(__file__).resolve().parent
quote = (HERE.parent / "quote" / "quote.src.html").read_text(encoding="utf-8")
cfg = "\n".join(re.search(r"^var %s = \{.*?^\};" % k, quote, re.S | re.M).group(0) for k in ("PRICING", "COSTS"))
base = (HERE / "model.src.html").read_text(encoding="utf-8").replace("/*CONFIG*/", cfg)
# two versions: free traveler counts per agency size (index.html) and fixed packages (packages.html)
for mode, name, title in (("flex", "index.html", None), ("packs", "packages.html", "מודל רווחיות PALAMI חבילות")):
    page = base.replace("/*MODE*/", "var MODE='%s';" % mode)
    if title: page = page.replace("<title>מודל רווחיות PALAMI</title>", "<title>%s</title>" % title, 1)
    head_end = page.index("</style>") + len("</style>")
    doc = ('<!doctype html>\n<html lang="he" dir="rtl" data-product="agent">\n<head>\n<meta charset="utf-8">\n'
           '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
           + page[:head_end] + "\n</head>\n<body>\n" + page[head_end:] + "\n</body>\n</html>\n")
    (HERE / name).write_text(doc, encoding="utf-8")
    print("wrote sales/model/" + name)
    if "--preview" in sys.argv:
        p = pathlib.Path(sys.argv[sys.argv.index("--preview") + 1])
        if mode == "packs": p = p.with_name(p.stem + "-packages" + p.suffix)
        p.write_text(page, encoding="utf-8"); print("wrote", p)
