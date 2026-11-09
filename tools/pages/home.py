"""Home (/), stage 2 in direction C2 (the reference page for tools/KIT.md).

Order (round 2's, adapted to C2): the hero, whose record is the outcomes (core.OUTCOMES on counter wheels, counted
from data/*.json at build time, with the link to the lists) > research areas > labs (with faces) > data centers >
videos > director > gallery teaser. The confirmed C2 hero already carries the record under its frame, so the outcomes
are not repeated in a second band (DESIGN.md, "Home").
"""
import kit
from kit import sec


def render():
    body = (
        kit.home_hero()
        + '<main>'
        + sec(('연구 분야', 'Research areas'), kit.areas(), 'research')
        + sec(('연구실', 'Labs'), kit.lab_rows(), 'labs')
        + sec(('데이터센터', 'Data centers'), kit.data_centers(), 'data-centers')
        + kit.videos_sec()
        + sec(('연구소장', 'Director'), kit.director(short_en=True), 'director')
        + kit.gallery_teaser()
        + '</main>'
    )
    return kit.page('청각재활연구소', body,
                    comment='기록 숫자는 data/*.json에서 셉니다. 영상은 data/videos.json, 사진은 data/gallery.json(앞 다섯 장)에서 만들어집니다.')
