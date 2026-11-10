# 갤러리(/gallery) 페이지 코드: Wix CMS로 사진 관리하기

`site/gallery.html`에는 `data/gallery.json`의 사진(2026-11-10 기준 59장)이 기본 목록으로 들어 있습니다. 아래 페이지 코드를 붙이면 CMS 컬렉션 **Gallery**의 사진이 기본 목록을 대신합니다. 코드가 실패하거나 메시지가 오지 않으면 기본 목록이 그대로 보이므로 페이지가 비는 일은 없습니다.

3차(C2 디자인, `tools/pages/gallery.py`)에서도 주고받는 방식은 2차와 같습니다. 아래 페이지 코드는 그대로 쓰면 됩니다. 바뀐 것은 4절의 iframe 높이뿐입니다.

**2026-11-09부터 새 갤러리 사진은 저장소에 넣습니다**(`python3 tools/media.py gallery`, CLAUDE.md 결정 2, 의뢰인: "관리가 쉬운 쪽으로"). 이 문서의 CMS 방식은 그 대신 쓸 수 있는 방법입니다. CMS 목록이 오면 `data/gallery.json`의 사진(저장소 사진 포함) 전체를 대신하므로 두 방법을 섞어 쓰지 않습니다.

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
    console.error('Gallery CMS', err);   // 실패하면 HTML 안의 기본 사진(data/gallery.json)이 그대로 보입니다.
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

3차 디자인(C2)에서 잰 값입니다. '지금 기본 목록' 줄은 2026-11-10 최종 점검 때 폭 980~1920 px를 1 px씩 잰 값(`heights.js --fine`), '13장 이상' 줄은 2026-11-09(3차 2단계 마무리 빌드: 320의 '지금 영상' 줄을 뺐고 연도 버튼이 한 줄, 캡션 12px)에 20 px 간격으로 잰 값입니다. 데스크톱은 그 가운데 가장 큰 값, "980"은 요소 폭이 980 px 고정일 때, 모바일은 320 px입니다. 모두 한국어·영어 가운데 큰 값에 24 px를 더하고 10 단위로 올렸습니다(이번에는 모든 경우 KO = EN). 사진을 저장소(`tools/media.py`)로 늘리든 CMS로 늘리든 같은 표를 씁니다.

**12장을 넘으면 높이는 사진 장수보다 사진 모양이 정합니다.** 데스크톱의 사진 줄은 줄마다 높이를 목표값(폭에 따라 220~320 px)에 가깝게 맞추므로, 가로로 긴 사진은 한 줄에 두 장씩 크게 들어가 줄 수가 늘어납니다. 그래서 같은 장수라도 모양에 따라 1,400 px까지 차이 나고, 폭이 넓을수록 길어지는 것도 아닙니다(16:9는 1,460 px 폭에서 가장 깁니다). 아래 값은 한 쪽 가득(12장)에 페이지 넘김 줄까지 있는 13장 이상일 때입니다. 딱 12장이면 넘김 줄이 없어 약 80 px 짧습니다.

| 사진 | 데스크톱 | 980 | 모바일(320) |
|---|---|---|---|
| 지금 기본 목록(59장, 2026-11-10) | 3690 | 2750 | 2630 |
| 13장 이상, 가로·세로가 섞임(2026-11-09 사진의 비율) | 3420 | 2400 | 2480 |
| 13장 이상, 대부분 4:3 (휴대폰·카메라 기본) | 3510 | 2400 | 2480 |
| 13장 이상, 대부분 3:2 (DSLR) | 3400 | 2300 | 2480 |
| 13장 이상, 대부분 1:1 | 3010 | 2170 | 2480 |
| 13장 이상, 대부분 세로 3:4 | 2980 | 2290 | 2480 |
| 13장 이상, 대부분 16:9 | 4210 | 3120 | 2480 |
| 13장 이상, 대부분 2:1 (파노라마·배너) | 4360 | 2980 | 2480 |

- 한 페이지는 12장까지이고 넘치는 사진은 다음 페이지로 갑니다. 갤러리는 가장 긴 쪽(모든 연도·모든 쪽, 두 언어)의 높이를 미리 잡아 두므로, 연도 버튼과 페이지 넘김을 눌러도 높이가 바뀌지 않습니다.
- 모바일은 4:3 두 칸이라 사진 모양과 상관없고, 캡션 줄 수와 연도 버튼 줄 수(연도가 많으면 두 줄)가 높이를 정합니다. 위 2480은 2026-11-09 캡션에 연도가 2~4개일 때입니다. 지금 목록(연도 8개, '전체'까지 단추 9개, 가장 긴 캡션은 영어 'Military Deafness and Tinnitus Prevention Association booth at the Changwon defence industry expo', 한국어 '대한민국 2023 지방시대 엑스포, 가상현실 어지럼증 디지털치료기기 체험 부스')은 2630입니다. 캡션이 모두 한 줄이면 2320, 모두 그 가장 긴 캡션만큼 길면 연도 2~4개에서 2770, 8개에서 2820입니다(2026-11-10 최종 점검, `{type:'gallery'}` 메시지로 잼).
- 사진 모양을 미리 알 수 없으면 처음부터 **데스크톱 4360(요소 폭이 980 고정이면 3120), 모바일 2820**으로 두면 위 표의 어떤 경우에도 잘리지 않습니다(사진이 적거나 세로 사진이 많으면 페이지 아래가 비어 보입니다). 휴대폰·카메라 사진(4:3, 3:2)이 대부분이면 데스크톱 3510 / 980 2400으로 충분하고, 모바일은 캡션에 따라 2480~2820입니다.
- 마무리 전 이 표(같은 날)의 값은 대부분 이 표보다 크거나 같았지만, **세로 3:4의 980 값(2260)은 이제 30 px 모자랍니다**. 그 값으로 두었다면 이 표로 바꿉니다. 그보다 이전 표(13장 이상 3400 / 2400 / 2580)는 지금 사진 비율을 1920 폭에서만 잰 값이라 4:3이나 16:9 사진에서 잘립니다.
- 13장 이상 값은 목록을 실제로 보내서 쟀습니다(모양마다 같은 비율 13장, 지금 캡션들을 돌려 씀, `{type:'gallery', items}` 메시지). 다시 재는 법: 저장소 목록은 `python3 tools/build.py --only gallery` 뒤 `node tools/verify/heights.js site/gallery.html --fine --md` 를 돌리고 `docs/wix-heights.md` 의 gallery 줄을 고칩니다(`--fine` 은 980~1920을 1 px씩 잽니다. 20 px 간격(`--sweep 20`)은 1,476 px의 꼭대기를 놓쳐 30 px 모자랐습니다).
- 높이가 사진 모양에 따라 크게 달라지는 이유와 고칠 방법(쪽을 '12장'이 아니라 '높이 예산'으로 나누기)은 `DESIGN.md` "2단계 마무리"에 적었습니다. 의뢰인이 정하기 전까지는 위 표를 씁니다.
