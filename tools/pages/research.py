"""Research (/project), stage 2 in direction C2.

Order (round 2's): the hero on the institute's tint (no photograph) with the record of the three lists (counted from
data/*.json at build time; each number jumps to its list) > research areas (the four project figures, full size on
click) > Publication > Report (학회 발표) > Patents (status and country filters).
Copy from round 2 (tools/pages_v2/research.py, which took it from tools/build_v1.py research()); the KO area titles
come from kit.AREAS (awaiting the client's confirmation, DESIGN.md 12.8). Lists: data/publications.json,
data/reports.json, data/patents.json; new entries appear after `python3 tools/build.py`, with no edit here.
"""
import kit
from kit import t, sec

# project figures (round-1 research page), keyed by kit.AREAS key: (imgur id, width, height, alt ko, alt en)
IMGS = {
    'basic': ('JbUTgTe', 1389, 879, '산화철 나노입자를 줄기세포에 내재화해 호밍 효과를 높이는 연구 개요도',
              'Diagram: iron oxide nanoparticles internalised in stem cells to improve homing'),
    'data': ('EgbUUiR', 1320, 754, '청각 데이터 참조표준센터의 데이터 생산·평가·보급 체계도',
             'Diagram: how the hearing reference standard data center produces, evaluates and distributes data'),
    'device': ('xqYPd2L', 1100, 640, '의료기기 개발 사례: 시술 기구의 3D 모형과 안진검사 고글',
               'Device examples: a 3D model of an instrument and nystagmography goggles'),
    'clinical': ('jNAHuk5', 998, 676, '골전도 보청기(BAHA) 임상시험의 두 시험군 구성',
                 'Bone conduction hearing aid (BAHA) trial: the two study groups'),
}

# the record's labels are core.OUTCOMES' (the Home hero's); the numbers are the lengths of the lists below
LISTS = (('publication', kit.PUBS, '학술지 논문'), ('report', kit.REPORTS, '학회 발표'), ('patents', kit.PATENTS, '특허 (출원·등록)'))


def record():
    label = {ko: (ko, en) for _, (ko, en) in kit.OUTCOMES}
    return kit.record([(len(items), label[ko]) for _, items, ko in LISTS], ['#' + sid for sid, _, _ in LISTS])


def projects():
    items = []
    for a in kit.AREAS:
        iid, w, h, ak, ae = IMGS[a['key']]
        src = f'https://i.imgur.com/{iid}.jpeg'
        fg = kit.plate(kit.imgur(src, 'l'), (ak, ae), w, h, href=src,
                       srcset=f'{kit.imgur(src, "l")} 640w, {kit.imgur(src, "h")} 1024w')
        items.append((fg, (a['ko'], a['en']), t(a['d_ko'], a['d_en'], 'p')))
    return kit.fig_cols(items, 2)


def render():
    hero = kit.page_hero(('연구', 'Research'), alt=kit.RESEARCH_TITLE, lead=kit.RESEARCH_LEAD, tone='inst', extra=record())
    body = (
        hero
        + '<main>'
        + sec(('연구 분야', 'Projects'), projects(), 'projects',
              note=('그림을 누르면 원본 크기로 열립니다.', 'Select a figure to open it full size.'))
        + '<!-- 논문·학회 발표·특허 목록: data/publications.json, reports.json, patents.json에서 만들어집니다. -->'
        + kit.list_sec(('논문', 'Publication'), 'pub', kit.PUBS, 'publication', note=kit.REEL_NOTE['pub'])
        + kit.list_sec(('학회 발표', 'Report'), 'report', kit.REPORTS, 'report', note=kit.REEL_NOTE['report'])
        + kit.list_sec(('특허', 'Patents'), 'patent', kit.PATENTS, 'patents', filters=('status', 'country'),
                       note=kit.REEL_NOTE['patent'])
        + '</main>'
    )
    return kit.page('Research', body,
                    comment='논문·학회 발표·특허 목록과 위의 숫자는 data/*.json을 고친 뒤 build.py를 다시 실행하면 바뀝니다.')
