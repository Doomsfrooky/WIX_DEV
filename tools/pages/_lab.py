"""Shared lab-page template for /about-1 (Basic Lab), /hearing-lab and /head-lab.

Each lab page module (basic-lab.py, hearing-lab.py, head-lab.py) holds only its copy (ported as is from
tools/build_v1.py) and calls render_lab(). Order:

  hero (lab-colour hairline + coil; HeAD Lab shows its logo as the title)
  > About (prose) > data center box (Hearing Lab, HeAD Lab: the center's logo is the heading)
  > Mission / Vision (/ Core Values) as ruled columns > Research subjects (2-column ruled grid)
  > Organization (org chart, this lab highlighted) > Director & Manager (+ link to People with the team count)
  > Publication (team list from data/publications.json, year filter, + link to the Research page for reports)
  > Alumni (small portrait grid; initial tile when there is no photo; the section is left out when there are none)
"""
import kit
from kit import t, tt, sec, more


def _members_link(key):
    n = len(kit.TEAMS.get(key, {}).get('members', []))
    if not n:
        return ''
    name = kit.LAB[key]['name']
    return f'<p class="h-more">{more("people", f"{name} 구성원 {n}명", f"{name}: {n} members")}</p>'


def render_lab(key, *, tagline, intro, mission, subjects, manager, alt=None, logo=None, dc=None, alumni=(),
               comment=''):
    """key: 'basic' | 'hearing' | 'head'.
    tagline, intro: (ko, en). alt: (ko, en) line under the title (default: the team name).
    mission: [(h3 (ko, en), ko, en)]. subjects: [(title_ko, title_en, ko, en)].
    manager: dict(photo, name=(ko, en), lines=(ko_list, en_list)).
    logo: (src, w, h) image shown as the hero title. dc: kit.dc_box() html.
    alumni: [(name, photo, role_ko, role_en)], newest first."""
    lb = kit.LAB[key]
    name = lb['name']

    hero = kit.page_hero(
        name, alt=alt or (lb['team_ko'], lb['team_en']), lead=tagline,
        logo=kit.img(logo[0], '', logo[1], logo[2], lazy=False) if logo else '',   # alt '': the h1 already holds the name as .sr text
        cls='hero-lablogo' if logo else '')

    body = hero + '<main>'
    body += sec(t('연구실 소개', 'About the lab'), kit.prose([intro]), 'about')   # the H1 already names the lab
    if dc:
        body += sec(t('데이터센터', 'Data center'), dc, 'data-center')

    body += sec(t('미션 · 비전', 'Mission &amp; Vision'),
                kit.ruled([(tt(h), t(ko, en, 'p')) for h, ko, en in mission], len(mission)), 'mission')
    body += sec(t('연구 주제', 'Research subjects'),
                kit.ruled([(t(a, b) if a != b else a, t(c, d, 'p')) for a, b, c, d in subjects], 2), 'subjects')
    body += sec(t('조직', 'Organization'), kit.org_chart(current=key), 'organization')

    people = (kit.director(short_en=False, quote=False)
              + kit.feature(kit.imgur(manager['photo'], 'l'), manager['name'], ('매니저', 'Manager'), manager['lines'],
                            alt=(f'{manager["name"][0]} 사진', f'Portrait of {manager["name"][1]}')))
    body += sec(t('연구소장 · 매니저', 'Director &amp; Manager'), people, 'people', aside=_members_link(key))

    pubs = [p for p in kit.PUBS if p['team'] == key]
    if pubs:
        lst = kit.listing('pub', pubs, filters=('year',))
        lst += kit.rv(more('/project#report', '학회 발표 목록은 연구 페이지에서 보기', 'Conference reports: Research page'))
        body += ('<!-- 논문 목록: data/publications.json에서 team 값이 이 연구실인 논문만 보여 줍니다. -->'
                 + sec(t('논문', 'Publication'), lst, 'publication',
                       note=t(f'{name}의 논문 {len(pubs)}편입니다. 눈금 하나가 논문 한 편입니다.',
                              f'{len(pubs)} articles from {name}. One tick is one article.')))

    if alumni:
        # KO role '학과 석사 · 2025년 2월 졸업': the date goes on its own line, so no '·' is left at a line end in the narrow cards
        grid = kit.people_grid([{'name': n, 'photo': ph, 'role_ko': '<br>'.join(rk.rsplit(' · ', 1)), 'role_en': re_}
                                for n, ph, rk, re_ in alumni], small=True)
        body += sec(t('졸업생', 'Alumni'), grid, 'alumni')
    body += '</main>'
    return kit.page(name, key, body, comment=comment)
