#!/usr/bin/env python3
"""Every component of tools/kit.py on three demo pages (working examples for tools/KIT.md; not part of the site).

    python3 tools/kit_demo.py        # site-preview/_kit.html, _kit-lists.html, _kit-lab.html (with the KO/EN toggle)

_kit.html        a photo hero (jump links in its extra) and every section component
_kit-lists.html  a tint hero with the record, a chapter, the three lists (Research's filters), a stacked list, the gallery
_kit-lab.html    kit.lab_page() for HeAD Lab (logo hero), with the round-2 copy read from tools/pages_v2/head-lab.py
All copy is the site's own (core, data/*.json, tools/pages_v2/*.py); nothing here is new content.
"""
import importlib.util
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.dont_write_bytecode = True
sys.path.insert(0, HERE)
import kit  # noqa: E402
from kit import t, sec  # noqa: E402
from build import check  # noqa: E402


def v2(name):
    """A round-2 page module (its copy constants), loaded from tools/pages_v2/."""
    sys.path.insert(0, os.path.join(HERE, 'pages_v2'))
    spec = importlib.util.spec_from_file_location('v2_' + name.replace('-', '_'), os.path.join(HERE, 'pages_v2', name + '.py'))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def demo_main():
    about, audiso, contact = v2('about'), v2('audiso'), v2('contact')
    nav = kit.jump_nav([('labs', ('연구실', 'Labs'), 'basic', 4), ('people', ('구성원', 'People'), 'head', 6),
                        ('lists', ('목록', 'Lists'), None, None)], ('이 페이지의 구성', 'On this page'))
    hero = kit.page_hero(('연구소 소개', 'About RIHE'), alt=('청각재활연구소', 'Research Institute of Hearing Enhancement'),
                         lead=('난청에 대한 기초 연구뿐만 아니라 의료기기 개발, 임상시험에 이르기까지 전주기적인 연구를 진행하는 연세대학교 공식 연구소입니다.',
                               'An official Yonsei University institute conducting full-cycle research, from basic research on hearing loss to '
                               'medical device development and clinical trials.'),
                         image=kit.gallery_photo(0, '50% 32%'), extra=nav)
    D = kit.DIRECTOR
    q = kit.quote(('“난청을 치료하는 임상의이자 난청을 연구하는 연구자로서, 청각재활연구소를 기반으로 융합 연구자의 길을 걸어왔습니다.”',
                   '“As a clinician who treats hearing loss and a researcher who studies it, I have walked the path of a '
                   'translational researcher based on this Institute.”'),
                  (f'{D["name_ko"]} {D["role_ko"]}', f'{D["role_en"]} {D["name_en"]}'), D['photo'])
    partners = kit.logos([(f'https://i.imgur.com/{f}' if (f in ('uYE9HkB.png', '7WGSBl9.png') or o['w'] <= 700) else kit.imgur(f'https://i.imgur.com/{f}', 'l'),
                           (ak, ae), o) for f, ak, ae, o in about.PARTNERS])
    kolas = kit.box(t('KOLAS 국제공인교정기관 인정 (KC24-437)', 'KOLAS accredited calibration body (KC24-437)', 'h3')
                    + t('ISO 국제 표준에 기반한 정확한 청력계 교정 서비스를 제공합니다.', 'Accurate audiometer calibration based on ISO international standards.', 'p'),
                    kit.img(kit.imgur('https://i.imgur.com/Ycn67aA.png', 'm'), ('KOLAS 교정 인정 마크, 인정번호 KC24-437', 'KOLAS calibration mark, No. KC24-437'), 886, 529),
                    tone='audiso')
    products = []
    for iid, tk, te, dk, de in audiso.PRODUCTS[:3]:
        products.append((kit.plate(f'https://i.imgur.com/{iid}.jpeg', (tk, te), 640, 400, sizes='(max-width: 760px) 50vw, 300px'), (tk, te), t(dk, de, 'p')))
    teams = []
    for key, name, email in contact.TEAMS:
        lb = kit.LAB[key]
        en = kit.NAME_EN.get(name, name)
        photo = next((m.get('photo', '') for m in kit.TEAMS[key]['members'] if m['name'] == name), '')
        teams.append(dict(key=key, name=lb['name'], team=(lb['team_ko'], lb['team_en']), person=(f'담당자 {name}', 'Contact: ' + en), email=email, photo=photo))
    visit = kit.kv([(('주소', 'Address'), t('강원특별자치도 원주시 일산로 20<br>연세대학교 원주세브란스기독병원 <span class="nw">의학관 318호 (26426)</span>',
                                             'Room 318, Medical Science Building<br>Wonju Severance Christian Hospital, Yonsei University<br>20 Ilsan-ro, Wonju, Gangwon-do 26426, Korea')),
                    (('이메일', 'Email'), kit.mail(D['email']) + t(f'{D["name_ko"]} {D["role_ko"]}', f'{D["role_en"]} {D["name_en"]}', 'p', 'k-d'))])
    body = (hero + '<main>'
            + sec(('청각재활연구소', 'The Institute'), q + kit.prose([kit.core.SINCE]), 'institute')
            + sec(('연구 분야', 'Research areas'), kit.areas(), 'areas')
            + sec(('연구실', 'Labs'), kit.lab_rows(current='head'), 'labs')
            + sec(('데이터센터', 'Data centers'), kit.data_centers(), 'data-centers')
            + sec(('조직', 'Organization'), kit.org_chart(current='hearing'), 'organization', tone='hearing')
            + sec(('데이터센터', 'Data center'), kit.dc_box('hearing', kit.prose([v2('hearing-lab').DC_TEXT]) + kit.bullets(v2('hearing-lab').DC_KO[:4], v2('hearing-lab').DC_EN[:4]),
                                                          since=('2019년 1월부터 운영', 'In operation since January 2019')), 'dcbox', tone='hearing')
            + kit.team_sec('faculty') + kit.team_sec('head') + kit.team_sec('hearing')
            + sec(('졸업생', 'Alumni'), kit.people_grid([{'name': '이준헌', 'photo': 'https://i.imgur.com/gQo7vUz.jpeg', 'role_ko': '의료정보통계학과 석사<br>2026년 2월 졸업', 'role_en': 'M.S. · Feb 2026'},
                                                       {'name': '류성화', 'photo': '', 'role_ko': '박사<br>2026년 졸업', 'role_en': 'Ph.D. · 2026'}], 's', 'head'), 'alumni', tone='head')
            + sec(('연구소장', 'Director'), kit.director(), 'people')
            + sec(('Audiso 소개', 'About Audiso'), kit.prose(audiso.INTRO[:1]) + kolas, 'audiso', tone='audiso')
            + sec(('제품', 'Products'), kit.fig_cols(products, 3, m2=True), 'products', tone='audiso')
            + sec(('협력 기관', 'Partners'), partners, 'partners')
            + sec(('연구소 안내', 'Visit us'), visit + kit.map_embed(contact.MAP_SRC, ('원주세브란스기독병원 위치 지도', 'Map: Wonju Severance Christian Hospital'), contact.MAP_LINK), 'visit')
            + sec(('팀별 연락처', 'Team contacts'), kit.contact_rows(teams), 'contacts', aside=kit.btn('https://audiso.co.kr/', 'audiso.co.kr'))
            + kit.videos_sec()
            + kit.gallery_teaser()
            + sec(('목록', 'Lists'), kit.listing('report', kit.REPORTS[:24]), 'lists', note=kit.REEL_NOTE['report'])
            + '</main>')
    return kit.page('Kit demo', body)


def demo_lists():
    rec = kit.record([(len(kit.PUBS), ('학술지 논문', 'Journal articles')), (len(kit.REPORTS), ('학회 발표', 'Conference presentations')),
                      (len(kit.PATENTS), ('특허 (출원·등록)', 'Patents (filed and granted)'))], ['#publication', '#report', '#patents'])
    hero = kit.page_hero(('연구', 'Research'), alt=kit.core.RESEARCH_TITLE, lead=kit.core.RESEARCH_LEAD, tone='inst', extra=rec)
    research = v2('research')
    figs = []
    for a in kit.AREAS[:2]:
        iid, w, h, ak, ae = research.IMGS[a['key']]
        src = f'https://i.imgur.com/{iid}.jpeg'
        figs.append((kit.plate(kit.imgur(src, 'l'), (ak, ae), w, h, href=src, srcset=f'{kit.imgur(src, "l")} 640w, {kit.imgur(src, "h")} 1024w'),
                     (a['ko'], a['en']), t(a['d_ko'], a['d_en'], 'p')))
    lines = ('청각재활연구소의', '연구 성과'), ('Research output', 'of the Institute')
    body = (hero + '<main>'
            + sec(('연구 분야', 'Projects'), kit.fig_cols(figs, 2), 'projects', note=('그림을 누르면 원본 크기로 열립니다.', 'Select a figure to open it full size.'))
            + kit.chapter(list(lines[0]), list(lines[1]), 'output', kit.core.RESEARCH_LEAD)
            + kit.list_sec(('논문', 'Publication'), 'pub', kit.PUBS, 'publication', note=kit.REEL_NOTE['pub'])
            + kit.list_sec(('학회 발표', 'Report'), 'report', kit.REPORTS, 'report', note=kit.REEL_NOTE['report'])
            + kit.list_sec(('특허', 'Patents'), 'patent', kit.PATENTS, 'patents', filters=('status', 'country'), note=kit.REEL_NOTE['patent'])
            + kit.sec_wide(('사진', 'Photos'), kit.gallery_grid(live=True), 'photos')
            + '</main>')
    return kit.page('Kit demo · lists', body)


def demo_lab():
    lab_mod = v2('_lab')
    seen = {}
    lab_mod.render_lab = lambda key, **kw: seen.update(key=key, **kw) or ''    # capture the round-2 copy, render nothing
    head = v2('head-lab')
    sys.modules['_lab'] = lab_mod
    head._lab = lab_mod
    head.render()
    kw = {k: v for k, v in seen.items() if k not in ('key', 'dc', 'comment')}
    dc = kit.dc_box('head', kit.prose([head.DC_TEXT]) + kit.bullets(head.DC_KO, head.DC_EN))
    return kit.lab_page('head', dc=dc, **kw)


def main():
    kit.PREVIEW = True
    out = os.path.join(ROOT, 'site-preview')
    os.makedirs(out, exist_ok=True)
    shutil.copytree(os.path.join(ROOT, 'site', 'vendor'), os.path.join(out, 'vendor'), dirs_exist_ok=True)   # GSAP next to the pages
    ok = True
    for name, fn in (('_kit', demo_main), ('_kit-lists', demo_lists), ('_kit-lab', demo_lab)):
        doc = fn()
        errs = check(name, doc)
        with open(os.path.join(out, name + '.html'), 'w', encoding='utf-8') as f:
            f.write(doc)
        print(f'  {"FAIL" if errs else "ok":5s} {name:12s} {len(doc.encode("utf-8")) / 1024:6.1f} KB  site-preview/{name}.html')
        for er in errs:
            print('        ' + er)
        ok = ok and not errs
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
