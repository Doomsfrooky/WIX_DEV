#!/usr/bin/env python3
"""Offline copies of external files for the verification scripts (MIRROR=1 node tools/verify/render.js ...).

Only needed when the session's network blocks a host in Chrome but not in curl (proxy/certificate trouble).
Files go to tools/verify/.mirror/ (gitignored). Run from the repo root:

    python3 -c "import sys; sys.path.insert(0, 'tools/verify'); from mirror import dl, dl_css; dl('<url>')"
    python3 tools/verify/mirror.py site/home.html      # every https URL the page names, plus Google Fonts files

Names must match lib.js mirrorName(): host+path with unsafe characters replaced, a hash suffix for query strings,
and long names shortened with a hash. Use dl_css() for Google Fonts CSS: it also fetches every font file it lists.
"""
import hashlib
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DIR = os.path.join(HERE, '.mirror')


def name(url):
    clean = re.sub(r'[?#].*$', '', re.sub(r'^https?://', '', url))
    q = ('_' + hashlib.sha1(url.encode()).hexdigest()[:12]) if '?' in url else ''
    n = re.sub(r'[^A-Za-z0-9._-]+', '_', clean)
    if len(n) > 120:
        n = n[:60] + '_' + hashlib.sha1(clean.encode()).hexdigest()[:16]
    return n + q


def dl(url, ctype=None):
    os.makedirs(DIR, exist_ok=True)
    f = os.path.join(DIR, name(url))
    if not os.path.exists(f):
        r = subprocess.run(['curl', '-sSfL', '-o', f, '-w', '%{content_type}', url], capture_output=True, text=True)
        if r.returncode:
            print('FAIL', url, r.stderr.strip())
            return None
        ctype = ctype or r.stdout.strip()
        if ctype:
            open(f + '.type', 'w').write(ctype)
    return f


def dl_css(url):
    f = dl(url, 'text/css; charset=utf-8')
    if f:
        for u in re.findall(r'url\((https://[^)]+)\)', open(f, encoding='utf-8').read()):
            dl(u)
    return f


if __name__ == '__main__':
    for page in sys.argv[1:]:
        html = open(page, encoding='utf-8').read().replace('&amp;', '&')
        for u in sorted(set(re.findall(r'https://[^\s"\'<>)]+', html))):
            if 'fonts.googleapis.com/css' in u:
                dl_css(u)
            elif re.search(r'\.(jpe?g|png|webp|gif|svg|mp4|woff2?|ttf|css|js)(\?|$|/)', u) or 'wixstatic' in u or 'imgur' in u:
                dl(u)
        print('mirrored', page)
