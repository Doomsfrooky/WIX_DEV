#!/usr/bin/env python3
"""Download every HTML embed currently published on www.smilesnail.org.

Wix stores the code of each "HTML iframe" element as a separate file and only
serves the published version. This script reads the site's page list, finds
every HtmlComponent on the menu pages, saves its code under embeds/<page>/ and
regenerates docs/site-map.md.

Run it after anyone edits an embed directly in the Wix editor and publishes,
then `git diff` shows exactly what changed on the live site.

    python3 tools/fetch_live.py

Standard library only.
"""
import json
import os
import re
import sys
import urllib.parse
import urllib.request

SITE = "https://www.smilesnail.org"
EMBED_HOST = "https://www-smilesnail-org.filesusr.com/"
PAGE_JSON = "https://static.wixstatic.com/sites/{}.z?v=3"

# Menu order as shown in the site header. Keys are Wix URL slugs.
PAGES = [
    ("", "home", "Home"),
    ("about", "about", "About"),
    ("project", "research", "Research"),
    ("people", "people", "People"),
    ("about-1", "basic-lab", "Basic Lab"),
    ("hearing-lab", "hearing-lab", "Hearing Lab"),
    ("head-lab", "head-lab", "HeAD Lab"),
    ("audiso", "audiso", "Audiso"),
    ("연락처", "contact", "Contact"),
]

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "wix-dev-sync/1.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode("utf-8", errors="replace")


def slugify(title):
    s = re.sub(r"\s*[—-]\s*RIHE.*$", "", title or "").strip().lower()
    s = re.sub(r"[^0-9a-z가-힣]+", "-", s).strip("-")
    return s or "embed"


def main():
    home = get(SITE)
    routes = json.loads(re.search(r'"routes":(\{.*?\}),"pageIdToPrefix"', home).group(1))
    files = json.loads(re.search(r'"pageJsonFileNames":(\{[^}]*\})', home).group(1))

    rows = []
    for slug, folder, label in PAGES:
        route = routes.get("./" + slug)
        if not route:
            print(f"! route not found: /{slug}", file=sys.stderr)
            continue
        page_id = route["pageId"]
        page = json.loads(get(PAGE_JSON.format(files[page_id])))
        data = page.get("data", {})
        docs = data.get("document_data", {})
        conns = data.get("connections_data", {})

        comps = {}

        def walk(node):
            if isinstance(node, dict):
                dq = node.get("dataQuery")
                if isinstance(dq, str):
                    comps[dq.lstrip("#")] = node
                for v in node.values():
                    walk(v)
            elif isinstance(node, list):
                for v in node:
                    walk(v)

        walk(page.get("structure", page))

        out_dir = os.path.join(ROOT, "embeds", folder)
        os.makedirs(out_dir, exist_ok=True)
        for item_id, item in docs.items():
            if item.get("type") != "HtmlComponent":
                continue
            comp = comps.get(item_id, {})
            nick = comp.get("id", item_id)
            cq = comp.get("connectionQuery")
            if cq:
                for c in conns.get(cq.lstrip("#"), {}).get("items", []):
                    nick = c.get("role") or nick
            layout = comp.get("layout", {})
            if item.get("sourceType") == "htmlEmbedded":
                code = get(EMBED_HOST + item["url"])
                m = re.search(r"<title>(.*?)</title>", code, re.S)
                title = m.group(1).strip() if m else ""
                name = f"{nick}.{slugify(title)}.html"
                with open(os.path.join(out_dir, name), "w", encoding="utf-8") as f:
                    f.write(code)
                source = "HTML 코드"
            else:
                title, name, source = "", "", "웹사이트 주소: " + item.get("url", "")
            rows.append({
                "label": label, "slug": slug, "folder": folder, "id": nick,
                "view": "모바일" if nick.startswith("mobile") else "데스크톱",
                "height": layout.get("height"), "title": title,
                "file": f"embeds/{folder}/{name}" if name else "", "source": source,
            })
            print(f"{label:12s} #{nick:12s} {rows[-1]['file'] or rows[-1]['source']}")

    write_site_map(rows)


def write_site_map(rows):
    lines = [
        "# 사이트 구성표",
        "",
        "`python3 tools/fetch_live.py`가 자동으로 만드는 파일입니다. 직접 고치지 마세요.",
        "",
        "Wix의 HTML iframe 요소는 높이가 자동으로 늘어나지 않습니다. 아래 '에디터 높이'보다 코드 내용이 길면 잘리거나 iframe 안에 스크롤이 생깁니다.",
        "",
        "| 페이지 | 주소 | 요소 ID | 보기 | 에디터 높이(px) | 파일 |",
        "|---|---|---|---|---|---|",
    ]
    for r in rows:
        url = SITE + "/" + urllib.parse.quote(r["slug"]) if r["slug"] else SITE + "/"
        target = f"[{os.path.basename(r['file'])}](../{r['file']})" if r["file"] else r["source"]
        lines.append(f"| {r['label']} | {url} | `#{r['id']}` | {r['view']} | {r['height']} | {target} |")
    os.makedirs(os.path.join(ROOT, "docs"), exist_ok=True)
    with open(os.path.join(ROOT, "docs", "site-map.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
