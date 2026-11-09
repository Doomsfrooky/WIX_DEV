"""Audiso (/audiso), stage 2 in direction C2.

Order (round 2's): the logo hero on Audiso's apricot tint (the logo instead of a visible title; the h1 stays as
screen-reader text) with the two website links > about Audiso + the KOLAS panel > strengths > Mission & Vision >
organisation (Audiso marked as this page) > products (six plates, two columns at 320; the two website links again
in the heading column, so the next step is at the end of the page too, not only about 3,000 px up). Every section
carries the audiso tone (its deep tone is the site's umber, the logo's gold).
Copy from round 2 (tools/pages_v2/audiso.py, which took it from tools/build_v1.py audiso()). External links
(audiso.co.kr, xr.audiso.co.kr) open in a new tab.
"""
import kit
from kit import t, sec

SITE_A = 'https://audiso.co.kr/'
SITE_XR = 'https://xr.audiso.co.kr/'
LOGO = ('https://i.imgur.com/lQwB2st.jpeg', 1858, 542)      # white ground, multiplied into the tint
KOLAS = ('https://i.imgur.com/Ycn67aA.png', 886, 529)        # RGB (no transparency), so imgur's 320 px copy is safe

INTRO = [
    ('(주)오디에스오는 국내 유일 국가인정 청력계 교정기관으로서, 보다 정확한 난청 진단 및 치료의 발전에 기여하고자 설립되었습니다.',
     'Audiso is Korea’s only nationally accredited audiometer calibration body, founded to advance more accurate diagnosis and treatment of hearing loss.'),
    ('대한민국 참조표준데이터센터인 한국인 청각 데이터센터에서 시작하여, 2018년부터 한국인의 정상 청력을 측정하기 위한 기기 교정, 표준검사 지침, 환경 교정 등의 표준절차를 바탕으로 국내 어디서나 인증된 청력검사를 받을 수 있도록 힘쓰고 있습니다.',
     'Starting from the Korean hearing reference data center, since 2018 we have built standard procedures for device calibration, standard test guidelines and environment calibration so that certified hearing tests are available anywhere in Korea.'),
    ('검사자와 환경에 대한 교육으로 교정 이후에도 지속적인 관리를 지원하며, VR 시뮬레이션과 AI 기술 등 청각 관련 사업과의 협력을 통해 교정받는 기관과 함께 성장하는 파트너가 되겠습니다.',
     'We support examiners and test environments after calibration through training, and work with VR simulation and AI partners to grow together with the institutions we serve.'),
]

STRENGTHS = [
    ('현직 이비인후과 전문의', 'Practising ENT specialist',
     '원주세브란스기독병원 이비인후과 교수로 활동하며, 진료와 수술에서 얻은 청각 관련 최신 데이터를 활용해 최적의 서비스를 제공합니다.',
     'Led by an ENT professor at Wonju Severance Christian Hospital, using the latest hearing data from clinical practice and surgery.'),
    ('KOLAS 국제공인교정기관', 'KOLAS-accredited',
     '청각 관련 국내 최초 청력계 기골도 분야 KOLAS 국제공인교정기관으로 인정받았습니다.',
     'Korea’s first KOLAS-accredited calibration body for audiometer air and bone conduction.'),
    ('청각 분야 전문가', 'Hearing specialists',
     '소속 직원 모두 청각학 전공자로, 청각에 대한 전문 지식을 활용해 높은 수준의 서비스를 제공합니다.',
     'All staff majored in audiology.'),
    ('출장 교정 서비스', 'On-site calibration',
     '전국 모두 직접 방문이 가능하며, 어디에서나 편리하게 출장 교정 서비스를 받을 수 있습니다.',
     'We visit sites anywhere in Korea.'),
    ('일정 맞춤 서비스', 'Flexible scheduling',
     '고객 일정에 맞추어 원하는 날짜로 진행할 수 있도록 예약신청 시스템을 제공합니다.',
     'Book the date that suits you through our reservation system.'),
    ('교육 서비스 제공', 'Training',
     '교정 외에 환경, 검사자 등 청각 검사기기를 제외한 요소에 대한 교육 서비스를 제공합니다.',
     'Training on test environments and examiners, beyond the devices themselves.'),
]

MISSION = [
    (('미션', 'Mission'),
     '국내 유일 국가인정 청력계 교정기관으로서, 표준화된 청력검사 환경 구축과 청각 솔루션 상용화를 통해 국민 청각 건강 증진에 기여합니다.',
     'As Korea’s only accredited audiometer calibration body, improve national hearing health through standardised test environments and commercial hearing solutions.'),
    (('비전', 'Vision'),
     'KOLAS 국제공인교정 기반의 정확한 청각 서비스와 혁신적 디지털 헬스케어 솔루션으로, 청각 분야의 글로벌 파트너로 성장합니다.',
     'Grow into a global partner in hearing with accurate KOLAS-based services and digital healthcare solutions.'),
]

# (imgur id, title ko, title en, text ko, text en); every file is 640 x 400 (the originals, no imgur resize needed)
PRODUCTS = [
    ('uTtErq7', 'WithHear, 난청 선별진단기기', 'WithHear hearing screening device',
     '난청의 조기 진단을 위한 청각검사, AI 고막 검사 기능을 탑재한 선별 진단 기기 개발 및 보급',
     'A screening device with hearing tests and AI eardrum examination for early diagnosis of hearing loss.'),
    ('6Hgxcfl', '의료 가상현실 시뮬레이터', 'Medical VR simulators',
     '청력검사, 이석증 진단치료, 측두골 임플란트 삽입 수술 등 임상실습 주제를 디지털트윈 및 리얼타임 렌더링 VR 시뮬레이션으로 개발',
     'Digital-twin, real-time VR simulations for clinical training: hearing tests, BPPV diagnosis and treatment, temporal-bone implant surgery.'),
    ('KsgzHqL', '어지럼증 디지털 치료제', 'Digital therapeutic for dizziness',
     '어지럼증을 치료하고 자세 균형을 회복할 수 있도록 재활운동을 제공하는 가상현실 기반의 맞춤 전정재활 훈련용 소프트웨어 개발',
     'VR-based, personalised vestibular rehabilitation software for treating dizziness and restoring balance.'),
    ('lcbkdkk', '모두의 보청기', 'Hearing aids for everyone (app)',
     '보청기 정보, 전문 병원 및 보청기 센터 위치기반 서비스, 난청 챗봇 상담 기능을 탑재한 애플리케이션 개발',
     'An app with hearing-aid information, location-based clinic and centre search, and a hearing-loss chatbot.'),
    ('Ltm00mT', '의사가 알려주는 디지털 치료제', 'Digital Therapeutics (book)',
     '디지털 치료기기의 개념부터 활용 사례, 의료법과 개인정보 보호까지 다룬 DTx 전문 서적 발간',
     'A book on digital therapeutics, from concepts and cases to medical law and privacy.'),
    ('dYhZ1vM', '피스탑 트리플케어', 'Peace Stop Triple Care',
     '소리에 민감한 귀 및 감각기관의 균형 관리를 위한 영양소를 공급해 주는 건강 기능 식품 개발',
     'A health functional food supplying nutrients for ears sensitive to sound and the balance of the sensory organs.'),
]


def about():
    # nw_paren keeps the accreditation number '(KC24-437)' from breaking at its hyphen in the narrow 320 column; box()
    # sets the h3 in the display face and puts its glyphs in the font subset
    kolas = kit.box(
        t(kit.nw_paren('KOLAS 국제공인교정기관 인정 (KC24-437)'), kit.nw_paren('KOLAS accredited calibration body (KC24-437)'), 'h3')
        + t('ISO 국제 표준에 기반한 정확한 청력계 교정 서비스를 제공합니다.', 'Accurate audiometer calibration based on ISO international standards.', 'p'),
        kit.img(kit.imgur(KOLAS[0], 'm'), ('KOLAS 교정 인정 마크, 인정번호 KC24-437', 'KOLAS calibration mark, No. KC24-437'), KOLAS[1], KOLAS[2]),
        tone='audiso')
    return kit.prose(INTRO) + kolas


def products():
    items = []
    for iid, tk, te, dk, de in PRODUCTS:
        fg = kit.plate(f'https://i.imgur.com/{iid}.jpeg', (tk, te), 640, 400, sizes='(max-width: 760px) 50vw, 300px')
        items.append((fg, (tk, te), t(dk, de, 'p')))
    return kit.fig_cols(items, 3, m2=True)       # two columns at 320


def render():
    links = '<p class="k-btns">' + kit.btn(SITE_A, 'audiso.co.kr') + kit.btn(SITE_XR, 'xr.audiso.co.kr') + '</p>'
    hero = kit.page_hero(
        'Audiso',
        alt=('오디에스오(주) · 청각재활연구소 교원창업 기업', 'Audiso Co., Ltd. · faculty ' + kit.nw('start-up of RIHE')),
        lead=('청력계 KOLAS 인정 교정기관 · 청각 솔루션 전문기업', 'KOLAS-accredited audiometer calibration · hearing solutions'),
        logo=(kit.imgur(LOGO[0], 'l'), LOGO[1], LOGO[2]), tone='audiso', inst='Audiology with ISO', extra=links)
    mv = kit.ruled([(h, t(ko, en, 'p')) for h, ko, en in MISSION], 2)
    strengths = kit.ruled([((a, b), t(c, d, 'p')) for a, b, c, d in STRENGTHS], 3)
    body = (
        hero
        + '<main>'
        + sec(('Audiso 소개', 'About Audiso'), about(), 'about', tone='audiso')
        + sec(('오디에스오의 강점', 'Why Audiso'), strengths, 'strengths', tone='audiso')
        + sec(('미션 · 비전', 'Mission &amp; Vision'), mv, 'mission', tone='audiso')
        + sec(('조직', 'Organization'), kit.org_chart(current='audiso'), 'organization', tone='audiso')
        + sec(('제품', 'Products'), products(), 'products', tone='audiso', aside=links)
        + '</main>'
    )
    return kit.page('Audiso', body, tone='audiso',
                    comment='제품 사진과 로고는 Imgur 주소를 그대로 씁니다. 두 누리집 링크는 새 창으로 열립니다.')
