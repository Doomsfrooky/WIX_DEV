"""Home (/): design A "Cochlea" with the judges' must-fixes.

Order: hero (cochlea) > research areas > outcomes > labs (with faces) > data centers > videos > director > gallery teaser.
"""
import kit
from kit import t, sec, more


def render():
    outcomes = kit.outcomes([
        (len(kit.PUBS), '학술지 논문', 'Journal articles'),
        (len(kit.PATENTS), '특허 (출원·등록)', 'Patents (filed and granted)'),
        (kit.TECH_TRANSFERS, '기술이전', 'Technology transfers'),
    ], more('research', '논문·학회 발표·특허 보기', 'Publications, reports and patents'))

    body = (
        kit.cochlea_hero()
        + '<main>'
        + sec(t('연구 분야', 'Research areas'), kit.areas(), 'research')
        + sec(t('성과', 'Outcomes'), outcomes, 'outcomes', note=t('눈금 하나가 한 건입니다.', 'One tick is one item.'))
        + sec(t('연구실', 'Labs'), kit.lab_rows(), 'labs')
        + sec(t('데이터센터', 'Data centers'), kit.data_centers(), 'data-centers')
        + kit.videos_sec()
        + sec(t('연구소장', 'Director'), kit.director(short_en=True), 'director')
        + kit.gallery_teaser()
        + '</main>'
    )
    return kit.page('청각재활연구소', 'navy', body,
                    comment='영상은 data/videos.json, 사진은 data/gallery.json(앞 다섯 장)에서 만들어집니다.')
