"""Gallery (/gallery, new page): photos from data/gallery.json, then the videos from data/videos.json.

Order: hero (title, the hairline with the small coil, lead) > Photos (year toggles, justified rows on desktop,
2 columns at 320, 12 per page, in-place viewer) > Videos (the shared player).

The photo list is baked into the HTML (so the page works with no message at all), and it can be replaced live:
the page posts {type: 'ready'} to window.parent, and Wix page code answers with {type: 'gallery', items: [...]}
read from a CMS collection (see tools/pages/gallery.md for the Velo code).
"""
import kit
from kit import t


def render():
    hero = kit.page_hero(t('갤러리', 'Gallery'),
                         lead=('학회와 수상, 그리고 연구소 사람들의 사진을 모았습니다.',
                               'Conferences, awards and the people of the institute.'))
    photos = kit.sec_wide(t('사진', 'Photos'), kit.gallery_grid(live=True), 'photos')
    videos = kit.videos_sec(t('영상', 'Videos'))
    body = hero + '<main>' + photos + videos + '</main>'
    return kit.page('Gallery', 'navy', body,
                    comment='사진은 data/gallery.json, 영상은 data/videos.json에서 만들어집니다. '
                            'Wix CMS의 Gallery 컬렉션을 쓰려면 tools/pages/gallery.md의 페이지 코드를 붙이세요.')
