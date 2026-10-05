"""Contact (/연락처): small-coil hero > visit us (address, director's email, affiliation, Google map) > team contacts.

Copy from tools/build_v1.py (contact()). Team contacts are mailto rows on the lab-row pattern; the contact person's
photo comes from data/people.json.
"""
import urllib.parse

import kit
from kit import t, sec, rv

MAP_Q = '원주세브란스기독병원'
MAP_SRC = f'https://www.google.com/maps?q={urllib.parse.quote(MAP_Q)}&amp;z=15&amp;output=embed'
MAP_LINK = f'https://www.google.com/maps/search/?api=1&amp;query={urllib.parse.quote(MAP_Q)}'

# (lab key, contact name, email): round-1 copy
TEAMS = [('basic', '이은수', 'es1121@yonsei.ac.kr'),
         ('hearing', '변유선', 'uuuseon@yonsei.ac.kr'),
         ('head', '윤철영', 'fezro@yonsei.ac.kr')]


def _photo(key, name):
    return next((m.get('photo', '') for m in kit.TEAMS.get(key, {}).get('members', []) if m['name'] == name), '')


def visit():
    D = kit.DIRECTOR
    rows = [
        (t('주소', 'Address'),
         t('강원특별자치도 원주시 일산로 20<br>연세대학교 원주세브란스기독병원 <span class="nw">의학관 318호 (26426)</span>',
           'Room 318, Medical Science Building<br>Wonju Severance Christian Hospital, Yonsei University<br>20 Ilsan-ro, Wonju, Gangwon-do 26426, Korea')),
        (t('이메일', 'Email'),
         f'<a class="mail" href="mailto:{D["email"]}">{D["email"]}</a>'
         + t(f'{D["name_ko"]} {D["role_ko"]}', f'{D["role_en"]} {D["name_en"]}', 'p', 'd')),
        (t('소속', 'Affiliation'),
         t('연세대학교 원주의과대학 · 원주세브란스기독병원 이비인후과 · 청각재활연구소',
           'Yonsei University Wonju College of Medicine · Department of Otorhinolaryngology, Wonju Severance Christian Hospital · RIHE')),
    ]
    return (rv(kit.kv(rows))
            + kit.map_embed(MAP_SRC, ('원주세브란스기독병원 위치 지도', 'Map: Wonju Severance Christian Hospital'), MAP_LINK))


def render():
    hero = kit.page_hero(t('연락처', 'Contact'), alt=('청각재활연구소에 문의하기', 'Get in touch'))
    teams = []
    for key, name, email in TEAMS:
        lb = kit.LAB[key]
        en = kit.NAME_EN.get(name, name)
        teams.append(dict(key=key, name=lb['name'], team=(lb['team_ko'], lb['team_en']),
                          person=(f'담당자 {name}', 'Contact: ' + (en if en != name else f'<span lang="ko">{name}</span>')),
                          email=email, photo=_photo(key, name)))
    body = (
        hero
        + '<main>'
        + sec(t('연구소 안내', 'Visit us'), visit(), 'visit')
        + sec(t('팀별 연락처', 'Team contacts'), kit.contact_rows(teams), 'teams')
        + '</main>'
    )
    return kit.page('Contact', 'navy', body)
