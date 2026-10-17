"""Mark the Word section as right-to-left (<w:bidi/> in sectPr), which docx-js does not expose.
Usage: python3 rtl_section.py file.docx"""
import re, shutil, sys, zipfile

path = sys.argv[1]
tmp = path + '.tmp'
with zipfile.ZipFile(path) as zin, zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as zout:
    for item in zin.infolist():
        data = zin.read(item.filename)
        if item.filename == 'word/document.xml':
            xml = data.decode('utf-8')
            xml = re.sub(r'(?<!<w:bidi/>)(<w:docGrid )', r'<w:bidi/>\1', xml)  # schema order: bidi goes right before docGrid
            data = xml.encode('utf-8')
        zout.writestr(item, data)
shutil.move(tmp, path)
