#!/usr/bin/env python3
"""Build the RIHE site pages from tools/pages/<name>.py (each exposes render() -> HTML) using tools/kit.py.

    python3 tools/build.py                      # site/<name>.html (paste into Wix; no language toggle)
    python3 tools/build.py --preview            # site-preview/<name>.html (small KO/EN toggle bottom right)
    python3 tools/build.py --only home,research # only these pages

Page names: home, about, research, people, basic-lab, hearing-lab, head-lab, audiso, contact, gallery.
A page whose module does not exist yet is skipped with a note.

Checks on every page (the build fails on an error):
- no em-dash characters in visible copy;
- every data-l="en" element carries lang="en";
- the file stays one self-contained document (no external scripts).
"""
import importlib.util
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.dont_write_bytecode = True
sys.path.insert(0, HERE)
import kit  # noqa: E402

PAGES = ['home', 'about', 'research', 'people', 'basic-lab', 'hearing-lab', 'head-lab', 'audiso', 'contact', 'gallery']


def load_page(name):
    path = os.path.join(HERE, 'pages', name + '.py')
    if not os.path.exists(path):
        return None
    spec = importlib.util.spec_from_file_location('page_' + name.replace('-', '_'), path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def visible_text(doc):
    s = re.sub(r'<!--.*?-->', ' ', doc, flags=re.S)
    s = re.sub(r'<(script|style)\b.*?</\1>', ' ', s, flags=re.S)
    alts = ' '.join(re.findall(r'(?:alt|aria-label|data-alt-en|data-aria-en|title)="([^"]*)"', s))
    return re.sub(r'<[^>]+>', ' ', s) + ' ' + alts


def check(name, doc):
    errs = []
    vis = visible_text(doc)
    for m in re.finditer('—', vis):
        errs.append(f'em-dash in visible copy: ...{vis[max(0, m.start() - 40):m.start() + 20].strip()}...')
    for m in re.finditer(r'<[a-z0-9]+\b[^>]*\bdata-l="en"[^>]*>', doc):
        tag = m.group(0)
        if 'lang="en"' not in tag and not tag.startswith('<span data-l="en">'):
            errs.append(f'data-l="en" without lang="en": {tag[:80]}')
    if re.search(r'<script[^>]+src=', doc):
        errs.append('external <script src> is not allowed')
    return errs


def main():
    args = sys.argv[1:]
    kit.PREVIEW = '--preview' in args
    only = None
    if '--only' in args:
        only = [x.strip() for x in args[args.index('--only') + 1].split(',') if x.strip()]
        bad = [x for x in only if x not in PAGES]
        if bad:
            sys.exit(f'unknown page(s): {", ".join(bad)}; pages: {", ".join(PAGES)}')
    out_dir = os.path.join(ROOT, 'site-preview' if kit.PREVIEW else 'site')
    os.makedirs(out_dir, exist_ok=True)
    failed = False
    for name in only or PAGES:
        mod = load_page(name)
        if mod is None:
            print(f'  skip  {name:12s} (tools/pages/{name}.py not written yet)')
            continue
        doc = mod.render()
        errs = check(name, doc)
        out = os.path.join(out_dir, name + '.html')
        with open(out, 'w', encoding='utf-8') as f:
            f.write(doc)
        print(f'  {"FAIL" if errs else "ok":5s} {name:12s} {len(doc.encode("utf-8")) / 1024:6.1f} KB  {os.path.relpath(out, ROOT)}')
        for er in errs:
            print('        ' + er)
        failed = failed or bool(errs)
    if failed:
        sys.exit(1)


if __name__ == '__main__':
    main()
