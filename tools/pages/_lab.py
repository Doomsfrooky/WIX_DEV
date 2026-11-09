"""Shared lab-page template for /about-1 (Basic Lab), /hearing-lab and /head-lab (stage 2, direction C2).

Each lab module (basic-lab.py, hearing-lab.py, head-lab.py) holds only its copy, ported as is from round 2
(tools/pages_v2/<lab>.py, which took it from tools/build_v1.py), and calls render_lab(). The composition is the kit's
lab template, kit.lab_page() (tools/KIT.md "Labs", DESIGN.md 9), so the three labs share one frame:

  hero (Basic Lab: the sage tint; Hearing Lab: the sky tint, see hearing-lab.py for the plaque photograph; HeAD Lab:
  its logo on the lilac tint)
  > 연구실 소개 > 데이터센터 (Hearing Lab, HeAD Lab: the center's logo is the heading)
  > 미션 · 비전 (· 핵심 가치) > 연구 주제 > 조직 (this lab marked) > 연구소장 · 매니저 (+ link to People with the count)
  > 논문 (the lab's publications, year filter, + link to the conference reports on /project)
  > 졸업생 (left out when there are none)

Read from data/*.json at build time, never hard-coded: the lab's member count and the manager's portrait
(data/people.json), the lab's publications and their count (data/publications.json, team key).
"""
import kit


def _manager(key, manager):
    """The manager's portrait from data/people.json (matched by the Korean name in the lab's team), so a new photo
    merged into the data reaches the lab page too; the copy's URL when the manager is not in the team list."""
    m = next((x for x in kit.TEAMS.get(key, {}).get('members', []) if x['name'] == manager['name'][0]), None)
    if m and m.get('photo'):
        return dict(manager, photo=m['photo'])
    return manager


def render_lab(key, *, tagline, intro, mission, subjects, manager, alt=None, logo=None, image=None, dc=None,
               alumni=(), comment=''):
    """key: 'basic' | 'hearing' | 'head'. Arguments are round 2's render_lab() arguments (tools/pages_v2/_lab.py):
    tagline, intro: (ko, en); alt: (ko, en) under the title (default the team name); mission: [((ko, en), ko, en)];
    subjects: [(title_ko, title_en, ko, en)]; manager: dict(photo, name=(ko, en), lines=(ko_list, en_list));
    logo: (src, w, h) in the hero instead of the title; dc: kit.dc_box() html; alumni: [(name, photo, role_ko, role_en)],
    newest first. Plus image: a hero photograph (kit.gallery_photo(key, pos, pos_m)); without it the hero is the
    lab's tint (or its logo on the tint)."""
    return kit.lab_page(key, tagline=tagline, intro=intro, mission=mission, subjects=subjects,
                        manager=_manager(key, manager), alt=alt, logo=logo, image=image, dc=dc, alumni=alumni,
                        comment=comment)
