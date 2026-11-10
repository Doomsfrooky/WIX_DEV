"""Basic Lab (/about-1): the shared lab template (_lab.py) with Basic Lab's copy from tools/build_v1.py.
No data center and no alumni yet (build_v1 lists none), so those sections are left out."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _lab  # noqa: E402


def render():
    return _lab.render_lab(
        'basic',
        tagline=('난청 치료의 근본을 탐구하는 기초연구', 'Basic research into the roots of hearing-loss treatment'),
        intro=('Basic Lab은 청각재활연구소 산하 기초팀으로, 줄기세포, 나노입자, 약물 전달 등 난청의 기전에 대한 기초 연구를 수행합니다.',
               'Basic Lab is the basic research team of RIHE, studying the mechanisms of hearing loss through stem cells, nanoparticles and drug delivery.'),
        mission=[(('미션', 'Mission'),
                  '난청 치료를 위한 혁신적인 기초 연구 기반을 구축하고, 줄기세포 및 나노공학 기술을 활용한 새로운 치료 접근법을 개발합니다.',
                  'Build an innovative basic research foundation for treating hearing loss and develop new therapies using stem cells and nano-engineering.'),
                 (('비전', 'Vision'),
                  '기초과학의 성과를 임상에 적용하여, 난청 환자의 삶의 질 향상에 기여하는 세계적 수준의 연구실을 목표로 합니다.',
                  'A world-class lab that brings basic science into the clinic and improves the quality of life of people with hearing loss.')],
        subjects=[('줄기세포 호밍 및 나노입자 전달', 'Stem-cell homing and nanoparticle delivery',
                   '자성 나노입자를 이용한 줄기세포의 내이 호밍 효율 향상 연구', 'Improving stem-cell homing to the inner ear with magnetic nanoparticles'),
                  ('Exosome 기반 치료제 연구', 'Exosome-based therapeutics',
                   '엑소좀을 활용한 내이 세포 보호 및 재생 치료제 개발', 'Exosome therapies that protect and regenerate inner-ear cells'),
                  ('약물 독성 및 보호 메커니즘 연구', 'Ototoxicity and protection',
                   '이독성 약물에 의한 내이 손상 기전 규명 및 보호 전략 연구', 'How ototoxic drugs damage the inner ear, and how to protect it'),
                  ('내이 세포 재생 연구', 'Inner-ear cell regeneration',
                   '유모세포 및 신경세포 재생을 위한 분자생물학적 접근', 'Molecular approaches to regenerating hair cells and neurons')],
        manager=dict(photo='https://i.imgur.com/SkXdr8p.jpeg', name=('이은수', '이은수'),
                     lines=(['Basic Lab 팀장 · 연구교수'], ['Team Leader, Basic Lab · Research Professor'])),
        comment='논문 목록은 data/publications.json(team: basic)에서 만들어집니다.')
