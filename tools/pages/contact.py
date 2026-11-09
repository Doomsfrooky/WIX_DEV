"""Contact (/연락처), stage 2 in direction C2.

Order (round 2's): the photo hero (the hospital campus, data/gallery.json '21.png'; DESIGN.md 6 recommends it, the
client confirms) > visit us (address, the director's email, affiliation, then the Google map) > team contacts (mailto
rows on the lab-row pattern, in each lab's tone; the contact person's photo comes from data/people.json).
Copy from round 2 (tools/pages_v2/contact.py, which took it from tools/build_v1.py contact()). Every address is real
and written out in full (no shortening): the emails are plain mailto links in the source.
"""
import sys
import urllib.parse

import kit
from kit import t, sec

HERO_PHOTO = '21.png'      # data/gallery.json key of the hero photograph (Wonju Severance Christian Hospital campus)
# 21.png is a banner, not a bare photograph: the campus rendering sits on a transparent strip at the left (x < 95) and
# above a transparent band carrying the Yonsei logo and the institute's name (y > 528). In the hero those margins show
# as a dark edge and the baked-in caption collides with the knockout title, so the hero takes only the opaque
# rendering: kit.gallery_photo(crop=...) cuts it through Wix's crop transform (x, y, w, h in the original's pixels).
HERO_CROP = (96, 2, 1295, 524)

MAP_Q = '원주세브란스기독병원'
MAP_SRC = f'https://www.google.com/maps?q={urllib.parse.quote(MAP_Q)}&amp;z=15&amp;output=embed'
MAP_LINK = f'https://www.google.com/maps/search/?api=1&amp;query={urllib.parse.quote(MAP_Q)}'

# (lab key, contact name, email): round-1 copy
TEAMS = [('basic', '이은수', 'es1121@yonsei.ac.kr'),
         ('hearing', '변유선', 'uuuseon@yonsei.ac.kr'),
         ('head', '윤철영', 'fezro@yonsei.ac.kr')]


def hero_image():
    """The campus rendering of 21.png (HERO_CROP); a clear KeyError if the photo leaves data/gallery.json."""
    return kit.gallery_photo(HERO_PHOTO, '50% 62%', '42% 50%', crop=HERO_CROP)


def _photo(key, name):
    """The contact's photo from data/people.json. TEAMS is round-1 copy, so a People update that removes the contact
    person does not change this page by itself: the build says so instead of quietly dropping the face."""
    m = next((m for m in kit.TEAMS.get(key, {}).get('members', []) if m['name'] == name), None)
    if m is None:
        print(f'contact: 담당자 {name} ({key}) is not in data/people.json; check TEAMS in tools/pages/contact.py', file=sys.stderr)
    return (m or {}).get('photo', '')


def visit():
    D = kit.DIRECTOR
    rows = [
        (('주소', 'Address'),
         t('강원특별자치도 원주시 일산로 20<br>연세대학교 원주세브란스기독병원 <span class="nw">의학관 318호 (26426)</span>',
           'Room 318, Medical Science Building<br>Wonju Severance Christian Hospital, Yonsei University<br>20 Ilsan-ro, Wonju, Gangwon-do 26426, Korea')),
        (('이메일', 'Email'),
         kit.mail(D['email']) + t(f'{D["name_ko"]} {D["role_ko"]}', f'{D["role_en"]} {D["name_en"]}', 'p', 'k-d')),
        (('소속', 'Affiliation'),
         t('연세대학교 원주의과대학 · 원주세브란스기독병원 이비인후과 · 청각재활연구소',
           'Yonsei University Wonju College of Medicine · Department of Otorhinolaryngology, Wonju Severance Christian Hospital · RIHE')),
    ]
    return (kit.kv(rows)
            + kit.map_embed(MAP_SRC, ('원주세브란스기독병원 위치 지도', 'Map: Wonju Severance Christian Hospital'), MAP_LINK))


def teams():
    items = []
    for key, name, email in TEAMS:
        lb = kit.LAB[key]
        en = kit.NAME_EN.get(name, name)
        items.append(dict(key=key, name=lb['name'], team=(lb['team_ko'], lb['team_en']),
                          person=(f'담당자 {name}', 'Contact: ' + (en if en != name else f'<span lang="ko">{name}</span>')),
                          email=email, photo=_photo(key, name)))
    return kit.contact_rows(items)


def render():
    hero = kit.page_hero(('연락처', 'Contact'), alt=('청각재활연구소에 문의하기', 'Get in touch'),
                         image=hero_image())
    body = (
        hero
        + '<main>'
        + sec(('연구소 안내', 'Visit us'), visit(), 'visit')
        + sec(('팀별 연락처', 'Team contacts'), teams(), 'teams')
        + '</main>'
    )
    return kit.page('Contact', body,
                    comment='주소와 이메일은 실제 연락처입니다(줄이거나 바꾸지 않습니다). 담당자 사진은 data/people.json에서 가져옵니다.')
