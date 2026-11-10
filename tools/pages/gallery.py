"""Gallery (/gallery), stage 2 in direction C2.

Order (round 2's): the photo hero (the ORL-HNS 2018 congress, data/gallery.json 'IMG_6300'; DESIGN.md 6 recommends
it, the client confirms) > Photos (year filters with counts, justified rows on desktop, two 4:3 columns at 320, 12 per
page, the pager, a viewer that opens in place over the grid: absolute, centred in the visible band of the tall Wix
iframe, never position: fixed) > Videos (the shared player, data/videos.json; plays only on click).

The photo list is baked into the HTML from data/gallery.json (so the page works with no message at all), and it can be
replaced live: the page posts {type: 'ready'} to window.parent, and Wix page code answers with
{type: 'gallery', items: [...]} read from a CMS collection (tools/pages/gallery.md has the Velo code and the heights).
Copy from round 2 (tools/pages_v2/gallery.py).
"""
import kit

HERO_PHOTO = 'IMG_6300'    # data/gallery.json key of the hero photograph (International Congress of ORL-HNS 2018)
LEAD = ('학회와 수상, 그리고 연구소 사람들의 사진을 모았습니다.', 'Conferences, awards and the people of the institute.')


def render():
    hero = kit.page_hero(('갤러리', 'Gallery'), lead=LEAD, image=kit.gallery_photo(HERO_PHOTO, '50% 40%'))
    body = (
        hero
        + '<main>'
        + kit.sec_wide(('사진', 'Photos'), kit.gallery_grid(live=True), 'photos')
        + kit.videos_sec(('영상', 'Videos'))
        + '</main>'
    )
    return kit.page('Gallery', body,
                    comment='사진은 data/gallery.json, 영상은 data/videos.json에서 만들어집니다. '
                            'Wix CMS의 Gallery 컬렉션을 쓰려면 tools/pages/gallery.md의 페이지 코드를 붙이세요.')
