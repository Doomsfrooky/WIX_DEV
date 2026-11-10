# 갤러리(/gallery) 페이지 코드: Wix CMS로 사진 관리하기

`site/gallery.html`에는 지금 사진 6장(`data/gallery.json`)이 기본 목록으로 들어 있습니다. 아래 페이지 코드를 붙이면 CMS 컬렉션 **Gallery**의 사진이 기본 목록을 대신합니다. 코드가 실패하거나 메시지가 오지 않으면 기본 목록이 그대로 보이므로 페이지가 비는 일은 없습니다.

## 1. CMS 컬렉션 만들기 (한 번만)

대시보드 > CMS > 컬렉션 만들기 > 이름 `Gallery`. 권한은 **누구나 읽기**로 둡니다.

| 필드 이름 | 형식 | 내용 |
|---|---|---|
| photo | 이미지 | 사진 |
| caption_ko | 텍스트 | 한국어 캡션 |
| caption_en | 텍스트 | 영어 캡션 (비우면 영어 화면에도 한국어 캡션이 나옵니다) |
| year | 텍스트 또는 숫자 | 연도 4자리 (예: 2021). 연도 버튼이 이 값으로 만들어집니다 |
| order | 숫자 | 작은 수가 먼저 나옵니다. 비워 두면 번호가 있는 사진보다 앞에 올 수 있으니 숫자를 넣어 주세요 |
| visible | 예/아니오 | '아니오'로 두면 숨겨집니다. 비워 두면 보입니다 |

Wix가 필드 키를 다르게 만들 수 있습니다(예: `captionKo`). 필드 설정에서 키를 확인하고 아래 코드의 `F`를 맞춰 주세요.

**사진 추가:** 대시보드 > CMS > Gallery > '+ 항목 추가'에서 사진을 올리고 캡션과 연도를 적은 뒤 저장합니다. 에디터를 열거나 게시할 필요가 없습니다.

## 2. 페이지 코드 (에디터 > /gallery 페이지 > 코드 패널에 붙여 넣기)

HTML iframe 요소의 ID는 데스크톱 `#html1`, 모바일 `#mobileHtml1`로 가정했습니다. 다르면 `FRAMES`를 고칩니다.

```js
import wixData from 'wix-data';

const COLLECTION = 'Gallery';
const F = { photo: 'photo', ko: 'caption_ko', en: 'caption_en', year: 'year', order: 'order', visible: 'visible' };
const FRAMES = ['#html1', '#mobileHtml1'];

// wix:image://v1/<미디어ID>/<파일명>#originWidth=W&originHeight=H
//   → https://static.wixstatic.com/media/<미디어ID> + 원본 가로·세로 (iframe이 비율을 미리 잡는 데 씁니다)
function toPhoto(uri) {
  const s = String(uri || '');
  const m = /^wix:image:\/\/v1\/([^/#]+)\/([^#]*)/.exec(s);
  if (m) {
    const w = /originWidth=(\d+)/.exec(s), h = /originHeight=(\d+)/.exec(s);
    let file = m[2];
    try { file = decodeURIComponent(file); } catch (e) {}
    return { src: `https://static.wixstatic.com/media/${m[1]}`, file, width: w ? +w[1] : 0, height: h ? +h[1] : 0 };
  }
  if (/^https:\/\//.test(s)) return { src: s, width: 0, height: 0 };   // 외부 주소: 비율은 4:3으로 잡힙니다
  return null;
}

function yearOf(v) {
  if (v instanceof Date) return String(v.getFullYear());
  const m = /\d{4}/.exec(String(v ?? ''));
  return m ? m[0] : '';
}

async function loadItems() {
  const res = await wixData.query(COLLECTION)
    .ne(F.visible, false)            // 비워 둔 항목은 보이고, '아니오'만 숨깁니다
    .ascending(F.order)
    .descending('_createdDate')
    .limit(100)
    .find();
  return res.items.map((row) => {
    const p = toPhoto(row[F.photo]);
    if (!p) return null;
    return { ...p, caption_ko: row[F.ko] || '', caption_en: row[F.en] || '', year: yearOf(row[F.year]) };
  }).filter(Boolean);
}

$w.onReady(async function () {
  let items = [];
  // 모바일 요소가 없는 페이지에서도 오류가 나지 않게 확인합니다.
  const frames = FRAMES.map((id) => { try { return $w(id); } catch (e) { return null; } })
    .filter((el) => el && typeof el.postMessage === 'function');
  const send = (el) => { if (items.length) el.postMessage({ type: 'gallery', items }); };

  // 순서 맞추기: iframe이 준비되면 {type:'ready'}를 보내고, 그때 목록을 보냅니다.
  frames.forEach((el) => el.onMessage((e) => { if (e.data && e.data.type === 'ready') send(el); }));

  try {
    items = await loadItems();
  } catch (err) {
    console.error('Gallery CMS', err);   // 실패하면 HTML 안의 기본 사진 6장이 그대로 보입니다.
    return;
  }
  frames.forEach(send);                  // iframe이 먼저 준비된 경우를 위해 한 번 더 보냅니다(중복은 무시됩니다).

  // 영어판(Wix Multilingual을 켠 뒤): import wixWindowFrontend from 'wix-window-frontend'; 를 맨 위에 넣고
  // frames.forEach((el) => el.postMessage({ lang: wixWindowFrontend.multilingual.currentLanguage }));
});
```

## 3. 동작 방식 (참고)

- iframe은 열리자마자 `window.parent`로 `{type:'ready'}`를 보냅니다. 목록이 오지 않으면 1.5초, 4초 뒤에 한 번씩 더 보냅니다.
- 페이지 코드는 `{type:'gallery', items:[...]}`로 답합니다. 각 항목은 `src`(wix:image://, static.wixstatic.com/media/..., 또는 https 주소) 또는 `media`(미디어 ID), `width`, `height`, `caption_ko`, `caption_en`, `year`, 선택으로 `file`을 가집니다.
- iframe은 받은 목록으로 사진, 연도 버튼, 페이지 넘김을 다시 만듭니다. 캡션은 글자로만 넣기 때문에 HTML이 섞여 있어도 실행되지 않습니다. 쓸 수 있는 항목이 하나도 없으면 기본 목록을 유지합니다.
- 사진 주소에는 크기 조절(fit 600/1200/1600 px)과 `enc_auto`(AVIF/WebP 자동 변환)가 붙습니다.

## 4. iframe 높이

| 사진 수 | 데스크톱 | 모바일(320) |
|---|---|---|
| 지금 기본 6장 | 1980 | 1760 |
| 한 페이지 가득(12장) | 2750 | 2350 |
| 13장 이상(페이지 넘김 버튼 줄 추가) | 2820 | 2420 |

한 페이지는 12장까지이고 넘치는 사진은 다음 페이지로 갑니다. CMS로 사진을 늘릴 계획이면 처음부터 **데스크톱 2820, 모바일 2420**으로 두면 다시 에디터를 열 필요가 없습니다(사진이 적을 때는 페이지 아래가 비어 보입니다). 측정 범위는 폭 980~1920 px와 320 px, 한국어·영어 중 큰 값입니다. 세로로 긴 사진은 줄이 낮아 이보다 짧습니다.
