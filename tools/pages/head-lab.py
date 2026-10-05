"""HeAD Lab (/head-lab): the shared lab template (_lab.py) with HeAD Lab's copy from tools/build_v1.py.
The hero title is the HeAD Lab logo; the box of the Korea Hearing Big-data Center has its logo as heading."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kit  # noqa: E402
import _lab  # noqa: E402

DC_KO = ['CDM, NHANES, UK Biobank 등 국내외 의료 빅데이터 활용 연구', '순음청력검사(PTA) 및 청성뇌간반응검사(ABR) 데이터 표준화',
         '건강보험공단 청력데이터 연동 추출', '청각 빅데이터 기반 AI 모델 개발 및 데이터 서비스', '산업체·연구자 대상 데이터 제공 및 기술 컨설팅']
DC_EN = ['Research using medical big data at home and abroad (CDM, NHANES, UK Biobank)',
         'Standardising pure-tone audiometry (PTA) and auditory brainstem response (ABR) data',
         'Linked extraction of hearing data from the National Health Insurance Service', 'AI models and data services built on hearing big data',
         'Data provision and technical consulting for industry and researchers']
DC_TEXT = ('산업계와 연구자에게 청각 분야의 빅데이터를 전문으로 제공하는 국내 유일 기관입니다. 10만 건 이상의 순음청력검사와 청성뇌간반응검사 데이터를 기반으로 '
           '라이프로그 데이터, 참조표준데이터, 보건의료빅데이터와 연계된 종합적인 청각빅데이터 제공을 목표로 합니다.',
           'Korea’s only provider of hearing big data for industry and researchers. Built on over 100,000 pure-tone audiometry and auditory brainstem '
           'response records, we aim to provide comprehensive hearing big data linked with lifelog, reference-standard and health big data.')


def render():
    dc = kit.dc_box('head', kit.prose([DC_TEXT]) + kit.bullets(DC_KO, DC_EN))
    return _lab.render_lab(
        'head',
        logo=('https://i.imgur.com/QV0SgF2.png', 981, 230),
        alt=('데이터팀', 'Data team'),
        tagline=('데이터로 소리를 이해하고, AI로 미래를 예측하다', 'Understanding sound with data, predicting the future with AI'),
        intro=('HeAD Lab은 청각 데이터와 인공지능 기술을 융합하여 난청 예측, 청력 건강 관리, 청각재활 분야의 솔루션을 개발합니다. '
               '데이터 과학과 AI 기술로 청력 손실의 조기 발견부터 개인 맞춤형 청각재활까지 청각 건강 관리의 전 주기를 아우르는 연구를 수행합니다.',
               'HeAD Lab combines hearing data and AI to build solutions for predicting hearing loss, managing hearing health and hearing rehabilitation, '
               'covering the full cycle from early detection to personalised rehabilitation.'),
        dc=dc,
        mission=[(('미션', 'Mission'),
                  '청각 건강 데이터의 표준화와 인공지능 기술 융합을 통해 난청 예방, 조기 진단 및 효과적인 재활을 위한 혁신적 솔루션을 개발하여 전 세계인의 청력 건강 증진에 기여합니다.',
                  'Standardise hearing-health data and combine it with AI to develop solutions for prevention, early diagnosis and effective rehabilitation of hearing loss worldwide.'),
                 (('비전', 'Vision'),
                  '빅데이터와 AI 기술을 활용한 청각 건강 관리의 글로벌 리더로서, 국제 표준을 선도하고 누구나 쉽게 접근할 수 있는 디지털 청각 건강 생태계를 구축합니다.',
                  'Lead hearing-health care with big data and AI, set international standards and build a digital hearing-health ecosystem open to everyone.'),
                 (('핵심 가치', 'Core Values'), '혁신성 · 정확성 · 협력', 'Innovation · Precision · Collaboration')],
        subjects=[('Future Hearing Prediction', 'Future Hearing Prediction',
                   '정상 청력자의 장기 데이터를 활용한 미래 청력 예측 AI 모델 개발', 'AI models that predict future hearing from long-term data of people with normal hearing'),
                  ('Ototoxicity &amp; Drugs', 'Ototoxicity &amp; Drugs',
                   '이독성 약물 데이터 분석 및 난청 발생 위험도 평가', 'Analysing ototoxic-drug data and the risk of hearing loss'),
                  ('Eardrum Imaging', 'Eardrum Imaging', '고막 내시경 영상 기반 AI 분류 및 온디바이스 적용', 'AI classification of eardrum endoscopy images, on device'),
                  ('Noise Map', 'Noise Map', '환경 소음과 건강 데이터를 융합한 소음지도 제작', 'Noise maps combining environmental noise and health data'),
                  ('International Cohorts', 'International Cohorts', 'UK Biobank 및 NHIS/KNHANES 연계 연구', 'Research linking UK Biobank and NHIS/KNHANES'),
                  ('Ear Age', 'Ear Age', '청력 기반 생물학적 나이 추정 및 청각 노화 연구', 'Estimating biological age from hearing, and ear ageing')],
        manager=dict(photo='https://i.imgur.com/RC37iFm.jpeg', name=('윤철영', 'Chul Young Yoon'),
                     lines=(['HeAD Lab 연구팀장', '연세대학교 의료정보통계학과'],
                            ['Team Leader, HeAD Lab', 'Department of Medical Informatics and Biostatistics, Yonsei University'])),
        alumni=[('이준헌', 'https://i.imgur.com/gQo7vUz.jpeg', '의료정보통계학과 석사 · 2026년 2월 졸업', 'M.S. · Feb 2026'),
                ('김지원', 'https://i.imgur.com/TWCotbS.jpeg', '의료정보통계학과 석사 · 2025년 2월 졸업', 'M.S. · Feb 2025'),
                ('이주형', 'https://i.imgur.com/jXCJxED.jpeg', '의료정보통계학 석사 · 2023년 2월 졸업', 'M.S. · Feb 2023')],
        comment='논문 목록은 data/publications.json(team: head)에서 만들어집니다. 졸업생은 tools/pages/head-lab.py의 alumni 목록에서 고칩니다.')
