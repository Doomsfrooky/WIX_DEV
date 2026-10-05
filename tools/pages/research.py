"""Research (/project): small-coil hero > projects (four areas with their images) > Publication > Report > Patents.

Copy from tools/build_v1.py (research()); the KO area titles come from kit.AREAS (awaiting client confirmation).
Lists are generated from data/publications.json, reports.json and patents.json: 10 per page, filters, tick ruler.
"""
import kit
from kit import t, sec

# project images (round-1 research page), keyed by kit.AREAS key: (imgur id, width, height, alt ko, alt en)
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


def projects():
    items = []
    for a in kit.AREAS:
        iid, w, h, ak, ae = IMGS[a['key']]
        src = f'https://i.imgur.com/{iid}.jpeg'
        fg = kit.plate(kit.imgur(src, 'l'), (ak, ae), w, h, href=src,
                       srcset=f'{kit.imgur(src, "l")} 640w, {kit.imgur(src, "h")} 1024w')
        items.append((fg, t(a['ko'], a['en']), t(a['d_ko'], a['d_en'], 'p')))
    return kit.fig_cols(items, 2)


def render():
    hero = kit.page_hero(
        t('연구', 'Research'),
        alt=('청각재활연구소의 연구 성과', 'Research output of the Institute'),
        lead=('기초 연구, 빅데이터·인공지능, 의료기기, 임상시험을 아우르는 연구를 합니다. 연구소와의 협력을 언제나 환영합니다.',
              'Our hearing research covers basic science, big data &amp; AI, medical devices and clinical trials. '
              'We always welcome collaborations with our laboratory.'))
    body = (
        hero
        + '<main>'
        + sec(t('연구 분야', 'Projects'), projects(), 'projects',
              note=t('그림을 누르면 원본 크기로 열립니다.', 'Select a figure to open it full size.'))
        + '<!-- 논문·학회 발표·특허 목록: data/publications.json, reports.json, patents.json에서 만들어집니다. -->'
        + sec(t('논문', 'Publication'), kit.listing('pub', kit.PUBS), 'publication',
              note=t('눈금 하나가 논문 한 편입니다. 고른 조건에 맞는 눈금은 남색으로 표시됩니다.',
                     'One tick is one article. Ticks that match the filter stay navy.'))
        + sec(t('학회 발표', 'Report'), kit.listing('report', kit.REPORTS), 'report',
              note=t('눈금 하나가 발표 한 건입니다.', 'One tick is one presentation.'))
        + sec(t('특허', 'Patents'), kit.listing('patent', kit.PATENTS, ('status', 'country')), 'patents',
              note=t('출원·등록 건을 모두 포함합니다.', 'Includes filed and granted patents. Titles are listed in Korean.'))
        + '</main>'
    )
    return kit.page('Research', 'navy', body,
                    comment='논문·학회 발표·특허 목록은 data/*.json을 고친 뒤 build.py를 다시 실행하면 바뀝니다.')
