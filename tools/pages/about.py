"""About (/about): small-coil hero > the institute (director's opening line + two paragraphs) > director >
organisation > data centers > partners > gallery teaser.

Copy from tools/build_v1.py (about()) and kit.DIRECTOR. The gallery teaser replaces the old small Wix Pro Gallery
at the bottom of /about: it shows the first five photos of data/gallery.json and links to /gallery.
"""
import kit
from kit import t, sec, rv

# partner logos (round-1 About): (imgur file, alt ko, alt en, size and trim). w/h are the files' pixel sizes; crop trims
# whitespace built into a file (top, right, bottom, left); kit.logos() then gives every mark the same visual area.
# Files wider than 640 px are served as imgur's 640 px 'l' copy (same ratio, so w/h/crop still hold), except the two
# PNGs with transparency (NCSRD, ILIAS), which imgur's thumbnails would flatten onto black.
PARTNERS = [
    ('e73yTmH.jpeg', 'Cochlear', 'Cochlear', dict(w=640, h=540)),
    ('Gt2yITF.jpeg', 'KRISS 한국표준과학연구원', 'KRISS Korea Research Institute of Standards and Science', dict(w=3900, h=600)),
    ('uYE9HkB.png', 'NCSRD 국가참조표준센터', 'NCSRD National Center for Standard Reference Data', dict(w=2000, h=846)),
    ('GdiAYNJ.jpeg', '대한청각학회', 'Korean Audiological Society', dict(w=959, h=453, crop=(.28, .14, .35, .13), style='filter:brightness(1.08) contrast(1.1)')),
    ('7WGSBl9.png', 'ILIAS Biologics', 'ILIAS Biologics', dict(w=1497, h=608, style='filter:drop-shadow(0 0 .5px #2a2f38) drop-shadow(0 0 .5px #2a2f38)')),
    ('sH2hnnv.jpeg', 'M.I one', 'M.I one', dict(w=400, h=428, crop=(.09, .07, .05, .06))),
    ('bM7xqYi.png', 'Innoshuttle', 'Innoshuttle', dict(w=2000, h=437)),
    ('pkbfNok.jpeg', 'J&amp;KYM', 'J&amp;KYM', dict(w=672, h=676)),
]


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
    return q + rv(text, 2)


def render():
    hero = kit.page_hero(
        t('연구소 소개', 'About RIHE'),
        alt='<span data-l="ko" lang="en">Research Institute of Hearing <span class="nw">Enhancement · RIHE</span></span><span data-l="en">청각재활연구소 · RIHE</span>',
        lead=('난청에 대한 기초 연구뿐만 아니라 의료기기 개발, 임상시험에 이르기까지 전주기적인 연구를 진행하는 연세대학교 공식 연구소입니다.',
              'An official Yonsei University institute conducting full-cycle research, from basic research on hearing loss to '
              'medical device development and clinical trials.'))
    keep = ('uYE9HkB.png', '7WGSBl9.png')      # RGBA: keep the original file
    partners = kit.logos([(f'https://i.imgur.com/{f}' if (f in keep or o['w'] <= 700) else kit.imgur(f'https://i.imgur.com/{f}', 'l'),
                           (ak, ae), o) for f, ak, ae, o in PARTNERS])
    body = (
        hero
        + '<main>'
        + sec(t('청각재활연구소', 'The Institute'), institute(), 'institute')
        + sec(t('연구소장', 'Director'), kit.director(short_en=False, quote=False), 'director')
        + sec(t('조직', 'Organization'), kit.org_chart(), 'organization')
        + sec(t('데이터센터', 'Data centers'), kit.data_centers(), 'data-centers')
        + sec(t('협력 기관', 'Partners'), partners, 'partners')
        + kit.gallery_teaser()
        + '</main>'
    )
    return kit.page('About', 'navy', body,
                    comment='아래 갤러리는 data/gallery.json의 앞 다섯 장을 보여 주고 /gallery로 연결됩니다(예전 Pro Gallery 대신).')
