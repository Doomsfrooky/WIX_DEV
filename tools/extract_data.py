#!/usr/bin/env python3
"""현재 임베드(embeds/)에서 논문·발표·특허·구성원 데이터를 뽑아 data/*.json으로 저장.

한 번만 실행하는 이전용 스크립트입니다. 이후에는 data/*.json을 직접 고치고
tools/build.py로 페이지를 만듭니다.
"""
import html, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
E = lambda p: open(os.path.join(ROOT, 'embeds', p), encoding='utf-8').read()


def text(s):
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', s))).strip()


def items(block):
    return re.findall(r'<div class="pub-item"([^>]*)>(.*?)\n\s*</div>\s*</div>', block, re.S)


def main():
    r = E('research/html1.research.html')
    pub_block = r.split('id="pub-list"')[1].split('id="pub-no-results"')[0]
    rep_block = r.split('id="report-list"')[1].split('id="report-no-results"')[0]
    pat_block = r.split('id="patent-body"')[1].split('</section>')[0]

    pubs = []
    for attrs, body in items(pub_block):
        tags = re.findall(r'<span class="pub-tag ([^"]+)">(.*?)</span>', body)
        pubs.append({
            'year': int(re.search(r'data-year="(\d+)"', attrs).group(1)),
            'team': re.search(r'data-team="(\w+)"', attrs).group(1),
            'title': text(re.search(r'<div class="pub-title">(.*?)</div>', body, re.S).group(1)),
            'authors': text(re.search(r'<div class="pub-authors">(.*?)</div>', body, re.S).group(1)),
            'journal': next(text(v) for k, v in tags if k == 'journal'),
        })

    reports = []
    for attrs, body in items(rep_block):
        tags = re.findall(r'<span class="pub-tag ([^"]+)">(.*?)</span>', body)
        reports.append({
            'year': int(re.search(r'data-year="(\d+)"', attrs).group(1)),
            'title': text(re.search(r'<div class="pub-title">(.*?)</div>', body, re.S).group(1)),
            'authors': text(re.search(r'<div class="pub-authors">(.*?)</div>', body, re.S).group(1)),
            'event': next(text(v) for k, v in tags if k == 'conf'),
        })

    patents = []
    for attrs, body in items(pat_block):
        tags = [text(v) for k, v in re.findall(r'<span class="pub-tag ([^"]+)">(.*?)</span>', body)]
        patents.append({
            'title': text(re.search(r'<div class="pub-title">(.*?)</div>', body, re.S).group(1)),
            'status': tags[0],          # 출원 / 등록
            'country': tags[1],         # 비어 있으면 원본에 국가 정보 없음
        })

    # 구성원: People 데스크톱이 기준
    p = E('people/html1.people.html')
    teams = []
    for sec in re.findall(r'<section class="team-section" id="(\w+)">(.*?)</section>', p, re.S):
        key, body = sec
        title = text(re.search(r'<h2 class="team-title">(.*?)</h2>', body, re.S).group(1))
        sub = text(re.search(r'<p class="team-subtitle">(.*?)</p>', body, re.S).group(1))
        members = []
        for card in re.findall(r'<div class="member-card[^"]*">(.*?)\n      </div>', body, re.S):
            photo = re.search(r'<img src="([^"]+)"', card)
            roles = [text(x) for x in re.findall(r'<p class="member-role"[^>]*>(.*?)</p>', card, re.S)]
            dept = re.search(r'<span class="member-dept">(.*?)</span>', card)
            members.append({
                'name': text(re.search(r'<h4>(.*?)</h4>', card, re.S).group(1)),
                'role': roles[0] if roles else '',
                'dept': (roles[1] if len(roles) > 1 else '') or (text(dept.group(1)) if dept else ''),
                'photo': photo.group(1) if photo else '',
            })
        teams.append({'key': key, 'title': title, 'subtitle': sub, 'members': members})

    out = {'publications': pubs, 'reports': reports, 'patents': patents, 'people': teams}
    for k, v in out.items():
        with open(os.path.join(ROOT, 'data', k + '.json'), 'w', encoding='utf-8') as f:
            json.dump(v, f, ensure_ascii=False, indent=1)
        print(k, len(v))


if __name__ == '__main__':
    main()
