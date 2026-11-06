#!/usr/bin/env python3
"""Round-3 design directions: build site/_directions/<key>.html from tools/kits/<key>.py.

    python3 tools/directions.py            # every kit in tools/kits/ (a, b, c)
    python3 tools/directions.py a c        # only these
    python3 tools/directions.py --hero DIR # assemble DIR/index.html from DIR/hero.html, hero.css, hero.js, fonts.txt
                                           # (used by the /67 hero exploration; DIR is under site/_directions/_67/)

Each kit module exposes render() -> full HTML document (it calls core.page_shell with prefix='../').
Every output goes through the same checks as tools/build.py (em-dash, lang="en", vendor-only scripts, robots, no vh).
"""
import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.dont_write_bytecode = True
sys.path.insert(0, HERE)
import core  # noqa: E402
from build import check  # noqa: E402

KITS = ['a', 'b', 'c']
OUT = os.path.join(ROOT, 'site', '_directions')


def load_kit(key):
    path = os.path.join(HERE, 'kits', key + '.py')
    if not os.path.exists(path):
        return None
    spec = importlib.util.spec_from_file_location('kit_' + key, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def write(path, doc, name):
    errs = check(name, doc)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(doc)
    print(f'  {"FAIL" if errs else "ok":5s} {name:12s} {len(doc.encode("utf-8")) / 1024:6.1f} KB  {os.path.relpath(path, ROOT)}')
    for er in errs:
        print('        ' + er)
    return not errs


def hero(d):
    """Assemble a standalone hero attempt: DIR/hero.html (body fragment), hero.css, hero.js (runs after GSAP loads),
    fonts.txt (one stylesheet URL per line, optional). All GSAP files in site/vendor are loaded."""
    d = os.path.abspath(d)
    rd = lambda n: open(os.path.join(d, n), encoding='utf-8').read() if os.path.exists(os.path.join(d, n)) else ''
    fonts = [x.strip() for x in rd('fonts.txt').splitlines() if x.strip() and not x.startswith('#')]
    prefix = os.path.relpath(os.path.join(ROOT, 'site'), d).replace(os.sep, '/') + '/'
    doc = core.page_shell(f'hero {os.path.basename(d)} · RIHE', rd('hero.html'), css=rd('hero.css'), js=rd('hero.js'),
                          fonts=fonts, vendor=('gsap', 'split', 'ease', 'draw'), prefix=prefix, robots='noindex', lang_toggle=True)
    return write(os.path.join(d, 'index.html'), doc, os.path.basename(d))


def main():
    args = sys.argv[1:]
    if args[:1] == ['--hero']:
        ok = all(hero(x) for x in args[1:])
        sys.exit(0 if ok else 1)
    os.makedirs(OUT, exist_ok=True)
    ok = True
    for key in args or KITS:
        mod = load_kit(key)
        if mod is None:
            print(f'  skip  {key:12s} (tools/kits/{key}.py not written yet)')
            continue
        ok = write(os.path.join(OUT, key + '.html'), mod.render(), key) and ok
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
