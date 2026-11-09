"""About (/about), stage 2 in direction C2.

Order (round 2's): the hero (the members' group photograph, data/gallery.json 'IMG_0168'; DESIGN.md 6 recommends it,
the client confirms) > the institute (the director's opening line as a pull quote + two paragraphs) > director >
organisation > data centers > partners > gallery teaser (linking to /gallery; it replaces the old small Wix Pro Gallery
at the bottom of /about). The teaser leaves out the hero's photograph, which would otherwise come back as its biggest
picture, and shows the three newest other photos of data/gallery.json in one row.
Copy from round 2 (tools/pages_v2/about.py, which took it from tools/build_v1.py about()) and kit.DIRECTOR.
"""
import kit
from kit import sec

# partner logos (round-1 About; sizes and crops from round 2): (imgur file, alt ko, alt en, opts). w/h are the files'
# pixel sizes; crop trims whitespace built into a file (top, right, bottom, left); kit.logos() gives every mark the same
# visual area. Files wider than 700 px are served as imgur's 640 px 'l' copy (same ratio), except the two PNGs with
# transparency (NCSRD, ILIAS), which imgur's thumbnails would flatten onto black.
PARTNERS = [
    ('e73yTmH.jpeg', 'Cochlear', 'Cochlear', dict(w=640, h=540)),
    ('Gt2yITF.jpeg', 'KRISS 한국표준과학연구원', 'KRISS Korea Research Institute of Standards and Science', dict(w=3900, h=600)),
    ('uYE9HkB.png', 'NCSRD 국가참조표준센터', 'NCSRD National Center for Standard Reference Data', dict(w=2000, h=846)),
    ('GdiAYNJ.jpeg', '대한청각학회', 'Korean Audiological Society', dict(w=959, h=453, crop=(.28, .14, .35, .13), style='filter:brightness(1.08) contrast(1.1)')),
    ('7WGSBl9.png', 'ILIAS Biologics', 'ILIAS Biologics', dict(w=1497, h=608, style='filter:drop-shadow(0 0 .5px #2a2f38) drop-shadow(0 0 .5px #2a2f38)')),
    ('sH2hnnv.jpeg', 'M.I one', 'M.I one', dict(w=400, h=428, crop=(.09, .07, .05, .06))),
    ('bM7xqYi.png', 'Innoshuttle', 'Innoshuttle', dict(w=2000, h=437)),
    ('pkbfNok.jpeg', 'J&KYM', 'J&KYM', dict(w=672, h=676)),     # plain text: kit.img() escapes the alt itself
]
KEEP = ('uYE9HkB.png', '7WGSBl9.png')      # RGBA: keep the original file
HERO_PHOTO = 'IMG_0168'                     # data/gallery.json key of the hero photograph (the members)

# round 2's subtitle: the institute's name in the other language (KO page: the English name, EN page: the Korean name)
ALT = ('<span data-l="ko" lang="en">Research Institute of Hearing <span class="nw">Enhancement · RIHE</span></span>'
       '<span data-l="en">청각재활연구소 · RIHE</span>')
LEAD = ('난청에 대한 기초 연구뿐만 아니라 의료기기 개발, 임상시험에 이르기까지 전주기적인 연구를 진행하는 연세대학교 공식 연구소입니다.',
        'An official Yonsei University institute conducting full-cycle research, from basic research on hearing loss to '
        'medical device development and clinical trials.')


def institute():
    D = kit.DIRECTOR
    q = kit.quote(('“난청을 치료하는 임상의이자 난청을 연구하는 연구자로서, 청각재활연구소를 기반으로 융합 연구자의 길을 걸어왔습니다.”',
                   '“As a clinician who treats hearing loss and a researcher who studies it, I have walked the path of a '
                   'translational researcher based on this Institute.”'),
                  (f'{D["name_ko"]} {D["role_ko"]}', f'{D["role_en"]} {D["name_en"]}'))
    text = kit.prose([
        ('2015년부터 다양한 융합 연구를 선보인 연구소입니다. 세계 여러 나라 청각 특성화 연구소들과 어깨를 나란히 견줄 수 있는 연구소가 되겠습니다.',
         'Since 2015 the Institute has presented a wide range of translational research, and we aim to stand shoulder to shoulder '
         'with specialised hearing institutes around the world.'),
        ('청각 특성화 연구소만의 독특한 시각과 연구 방식으로 수년 동안 발전해 온 청각재활연구소의 우수한 연구들을 볼 수 있습니다.',
         'Here you can find the research the Institute has developed over the years with the perspective and methods of a '
         'hearing-specialised institute.'),
    ])
    return q + text


def partners():
    return kit.logos([(f'https://i.imgur.com/{f}' if (f in KEEP or o['w'] <= 700) else kit.imgur(f'https://i.imgur.com/{f}', 'l'),
                       (ak, ae), o) for f, ak, ae, o in PARTNERS])


def gallery():
    """The gallery teaser without the hero's photograph (it would come back as the teaser's biggest picture): the
    three newest other photos of data/gallery.json in one row (320: the first across, then a pair)."""
    photos = [p for p in kit.GALLERY if HERO_PHOTO not in (p.get('file', '') + p.get('media', '') + p.get('src', ''))][:3]
    return kit.gallery_teaser(photos, rows=(len(photos),))


def render():
    hero = kit.page_hero(('연구소 소개', 'About RIHE'), alt=ALT, lead=LEAD, image=kit.gallery_photo(HERO_PHOTO, '50% 32%'))
    body = (
        hero
        + '<main>'
        + sec(('청각재활연구소', 'The Institute'), institute(), 'institute')
        + sec(('연구소장', 'Director'), kit.director(short_en=False, quote=False), 'director')
        + sec(('조직', 'Organization'), kit.org_chart(), 'organization')
        + sec(('데이터센터', 'Data centers'), kit.data_centers(), 'data-centers')
        + sec(('협력 기관', 'Partners'), partners(), 'partners')
        + gallery()
        + '</main>'
    )
    return kit.page('About', body,
                    comment='맨 위 사진은 data/gallery.json의 구성원 단체 사진(IMG_0168)이고, 아래 갤러리는 그 사진을 뺀 가장 최근 세 장을 보여 주며 /gallery로 연결됩니다(예전 Pro Gallery 대신).')
