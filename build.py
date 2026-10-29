"""Erzeugt en/index.html und tr/index.html aus index.html (Deutsch) und i18n.py.

Aufruf:  python3 build.py
"""
import os, re, sys
from i18n import T

ROOT = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()

# Längste Texte zuerst, damit Teilstrings nicht vorzeitig ersetzt werden
pairs = sorted(T, key=lambda t: -len(t[0]))
missing = [de for de, *_ in pairs if de not in src]
if missing:
    sys.exit('Nicht in index.html gefunden:\n  ' + '\n  '.join(missing))

LANGS = {'en': 1, 'tr': 2}
for lang, idx in LANGS.items():
    s = src
    for row in pairs:
        if row[0] != row[idx]:
            s = s.replace(row[0], row[idx])
    s = s.replace('<html lang="de">', f'<html lang="{lang}">', 1)
    s = s.replace('<link rel="canonical" href="https://ermantemiz.ch/">',
                  f'<link rel="canonical" href="https://ermantemiz.ch/{lang}/">', 1)
    # aktive Sprache im Umschalter
    s = s.replace(' aria-current="page">DE</a>', '>DE</a>', 1)
    s = s.replace(f'hreflang="{lang}">{lang.upper()}</a>', f'hreflang="{lang}" aria-current="page">{lang.upper()}</a>', 1)
    # Bildpfade eine Ebene höher
    s = s.replace('src="img/', 'src="../img/').replace('url(img/', 'url(../img/').replace('href="fonts/', 'href="../fonts/')
    out = os.path.join(ROOT, lang, 'index.html')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, 'w', encoding='utf-8').write(s)
    print('geschrieben:', os.path.relpath(out, ROOT))
