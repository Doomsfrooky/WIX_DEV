"""People (/people): every team from data/people.json in the hanging grid.

Order follows people.json: faculty > Basic Lab > Hearing Lab > HeAD Lab > administration > Audiso.
Hero: title, the hairline with the small coil, lead, then jump links to each team (with member counts).
Each team: lab mark, name, team name and member count in the heading column (plus a link to the lab page for
the four labs); 4:5 portraits in the content column, 4 columns on desktop and 2 at 320, revealed row by row.
Names in English come from kit.NAME_EN and roles from kit.ROLE_EN (both from build_v1.py); a member without a
photo gets an initial tile.
"""
import kit
from kit import t, sec, more


def _head(key):
    """(h2 html, note html, aside html) for a people.json team."""
    ck, ko, en = kit.TEAM_META[key]
    n = len(kit.TEAMS[key]['members'])
    cnt_ko, cnt_en = f'<span class="nw">{n}명</span>', f'<span class="nw">{n} members</span>'
    lb = kit.LAB.get(key)
    mark = kit.team_mark(ck)
    if lb:       # a lab: the lab name is the heading in both languages, the team name sits under it
        h = mark + lb['name']
        note = t(_tail(lb['team_ko'], f'{n}명'), _tail(lb['team_en'], f'{n} members'))
        aside = f'<p class="h-more">{more(lb["page"], lb["name"] + " 소개", "About " + lb["name"])}</p>'
    else:
        h = mark + t(ko, en)
        note = t(cnt_ko, cnt_en)
        aside = ''
    return h, note, aside


def _tail(team, cnt):
    """'team · count' that never ends a line on the '·': the last word of the team name, the dot and the count
    stay together ('Reference standard / team · 5 members' at the narrow heading column)."""
    head, _, last = team.rpartition(' ')
    return (head + ' ' if head else '') + f'<span class="nw">{last} · {cnt}</span>'


def _en_part(x):
    """English for one role part; short multi-word roles ('Team Leader') never split across lines."""
    en = kit.ROLE_EN.get(x.strip(), x.strip())
    return en.replace(' ', '&nbsp;') if len(en) <= 14 else en


def _card(m):
    """people.json member with its role line set: role parts joined by ' / ', the department on its own line
    (so a long English department never leaves a dangling '·' at a line end)."""
    role, dept = m.get('role', ''), m.get('dept', '')
    ko = ' / '.join(x.strip() for x in role.split('/')) if role else ''
    en = ' / '.join(_en_part(x) for x in role.split('/')) if role else ''
    if dept:
        ko = ko + '<br>' + dept if ko else dept
        en = en + '<br>' + kit.role_en(dept) if en else kit.role_en(dept)
    return dict(m, role_ko=ko, role_en=en)


def _nav_label(key):
    ck, ko, en = kit.TEAM_META[key]
    lb = kit.LAB.get(key)
    return (lb['name'] if lb else t(ko, en)), ck


def render():
    teams = [tm for tm in kit.PEOPLE if tm['members']]
    nav = kit.jump_nav([(tm['key'], *_nav_label(tm['key']), len(tm['members'])) for tm in teams],
                       ('팀 바로가기', 'Jump to a team'))
    hero = kit.page_hero(kit.t('구성원', 'People'), alt=('함께 연구하는 사람들', 'The people of RIHE'),
                         lead=('연세대학교 원주세브란스기독병원 청각재활연구소(RIHE) 구성원을 소개합니다.',
                               'Meet the members of the Research Institute of Hearing Enhancement.'),
                         extra=nav, cls='hero-people')
    body = hero + '<main>'
    for tm in teams:
        h, note, aside = _head(tm['key'])
        body += sec(h, kit.people_grid([_card(m) for m in tm['members']], rows=True), tm['key'], note=note, aside=aside, cls='team')
    body += '</main>'
    return kit.page('People', 'navy', body,
                    comment='구성원은 data/people.json에서 만들어집니다. 사진이 없는 구성원은 이름 첫 글자로 표시됩니다.')
