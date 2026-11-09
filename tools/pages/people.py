"""People (/people), stage 2 in direction C2.

Hero: the members' group photograph (data/gallery.json 'IMG_0168'; DESIGN.md 6 recommends it, the client confirms),
the title, round 2's subtitle and lead, and the jump links to every team with its member count.
Then one section per team in data/people.json order (faculty > Basic Lab > Hearing Lab > HeAD Lab > administration >
Audiso): the lab's Latin name or the team's KO/EN name, the team and the count, a link to the lab page for the four
labs, the tone tab, the portraits (faculty 3 columns, teams 6; 320: a list for the faculty, 3 columns for teams).
A member without a photograph gets an initial on the team's tint. Teams, members, counts and photos all come from
data/people.json at build time (a team with no members is left out).
"""
import kit


def _label(key):
    """Jump-link label: the lab's Latin name for the four labs, else the team's (ko, en) name (round 2)."""
    lb = kit.LAB.get(key)
    if lb:
        return lb['name']
    _, ko, en = kit.TEAM_META[key]
    return (ko, en)


def render():
    teams = [tm for tm in kit.PEOPLE if tm['members']]
    nav = kit.jump_nav([(tm['key'], _label(tm['key']), kit.TEAM_TONE.get(tm['key']), len(tm['members'])) for tm in teams],
                       ('팀 바로가기', 'Jump to a team'))
    hero = kit.page_hero(('구성원', 'People'), alt=kit.PEOPLE_TITLE, lead=kit.PEOPLE_LEAD,
                         image=kit.gallery_photo('IMG_0168', '50% 32%'), extra=nav)
    body = hero + '<main>' + ''.join(kit.team_sec(tm['key']) for tm in teams) + '</main>'
    return kit.page('People', body,
                    comment='구성원은 data/people.json에서 만들어집니다(팀 순서, 인원 수, 사진). 사진이 없는 구성원은 이름 첫 글자로 표시됩니다.')
