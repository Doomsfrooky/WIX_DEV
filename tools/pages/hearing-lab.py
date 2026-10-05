"""Hearing Lab (/hearing-lab): the shared lab template (_lab.py) with Hearing Lab's copy from tools/build_v1.py,
plus the box of the Korean reference hearing standard data center (logo as heading)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kit  # noqa: E402
import _lab  # noqa: E402

DC_KO = ['한국인 연령별/성별 청각 참조데이터 수집 및 생산 (국내 유일)', '한국인 청각 참조데이터 평가를 통한 참조데이터 자체 등급부여',
         '한국인 청각 참조데이터 등급부여 요청 및 참조표준 등록 요청', '국제공동연구를 통한 청각 데이터 생산 및 대규모 연구',
         '국제협력을 통한 국제 청각 데이터베이스 네트워크 구축', '이어폰/보청기 산업 및 의료기기 개발 데이터 제공',
         '난청 보건 사업 데이터 제공', '청각 관련 앱 개발 데이터 제공']
DC_EN = ['Collecting and producing Korean reference hearing data by age and sex (the only one in Korea)', 'Grading reference data through our own evaluation',
         'Requesting grading and registration as national reference standards', 'Producing hearing data and large-scale studies through international collaboration',
         'Building an international hearing database network', 'Data for the earphone, hearing-aid and medical-device industries',
         'Data for public hearing-health programmes', 'Data for hearing-related app development']
DC_TEXT = ('한국인의 특성을 충분히 반영하지 못하는 기존 외국 기준 대신 한국인 청각 참조표준을 적용하면 진단과 검사의 정확도가 높아져 한국인 환자에게 더 나은 의료서비스를 제공할 수 있습니다. '
           '한국인 청각 참조표준은 난청 보건 사업, 이어폰·보청기 등 의료기기, 청각 연구, skull simulator, 청각 치료 및 재활, 앱 개발 등에 적용될 예정입니다.',
           'Foreign standards do not fully reflect Korean characteristics. Applying Korean reference hearing standards makes diagnosis and testing more accurate '
           'and gives Korean patients better care. They will be applied to public hearing-health programmes, earphones, hearing aids and other devices, '
           'hearing research, skull simulators, treatment and rehabilitation, and app development.')


def render():
    dc = kit.dc_box('hearing', kit.prose([DC_TEXT]) + kit.bullets(DC_KO, DC_EN),
                    since=('2019년 1월부터 운영', 'In operation since January 2019'))
    return _lab.render_lab(
        'hearing',
        tagline=('한국인 청각의 표준을 만들어가는 연구', 'Setting the standard for Korean hearing'),
        intro=('Hearing Lab은 청각재활연구소 산하 참조표준팀으로, 한국인 청각 참조표준 데이터를 수집·생산하고 청각 연구를 수행합니다. '
               '한국인의 특성을 반영한 청각 참조표준을 확립하여 더 정확한 청력 진단과 더 나은 의료서비스 제공을 목표로 합니다.',
               'Hearing Lab is the reference standard team of RIHE. We collect and produce Korean reference hearing data and aim for more accurate '
               'diagnosis and better care through standards that reflect Korean characteristics.'),
        dc=dc,
        mission=[(('미션', 'Mission'),
                  '한국인 청각 참조데이터의 수집, 평가, 등급부여를 통해 국내 유일의 청각 참조표준 데이터센터를 운영하고 국제 네트워크를 구축합니다.',
                  'Run Korea’s only reference standard data center for hearing by collecting, evaluating and grading Korean hearing data, and build an international network.'),
                 (('비전', 'Vision'),
                  '한국인에게 최적화된 청각 참조표준을 확립하여 글로벌 청각 연구의 거점이 되고, 국민 청각 건강 증진에 기여합니다.',
                  'Establish hearing standards optimised for Koreans, become a hub of global hearing research and improve the nation’s hearing health.')],
        subjects=[('한국인 청각 참조표준 데이터 수집', 'Korean reference hearing data',
                   '연령별·성별 한국인 청각 데이터의 체계적 수집 및 품질 관리', 'Systematic collection and quality control of Korean hearing data by age and sex'),
                  ('청력검사 표준화 연구', 'Standardising hearing tests',
                   '국제 표준에 부합하는 청력검사 절차 및 기준 수립', 'Hearing-test procedures and criteria that meet international standards'),
                  ('보청기·이어폰 산업 데이터 제공', 'Data for industry',
                   '청각 산업 및 의료기기 개발을 위한 표준 데이터 제공', 'Standard data for the hearing industry and medical-device development'),
                  ('국제 청각 데이터베이스 네트워크', 'International hearing database network',
                   '글로벌 청각 연구 기관과의 데이터 공유 및 공동 연구', 'Data sharing and joint research with hearing institutes worldwide')],
        manager=dict(photo='https://i.imgur.com/2Q56Mj7.jpeg', name=('변유선', 'Yuseon Byun'),
                     lines=(['Hearing Lab · 박사과정'], ['Hearing Lab · Ph.D. Student'])),
        alumni=[('류성화', '', '박사 · 2026년 졸업', 'Ph.D. · 2026'), ('이지현', '', '박사 · 2022년 졸업', 'Ph.D. · 2022')],
        comment='논문 목록은 data/publications.json(team: hearing)에서 만들어집니다. 졸업생 사진이 생기면 tools/pages/hearing-lab.py의 alumni에 주소를 넣으세요.')
