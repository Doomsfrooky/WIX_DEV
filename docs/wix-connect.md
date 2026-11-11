# Wix 연결 안내 (3단계)

새 홈페이지 10쪽을 Wix에 붙이는 순서입니다. Wix에서 할 일은 **요소마다 주소와 높이를 넣는 것**뿐이고, 그 뒤의 수정은 저장소에서만 합니다(CLAUDE.md 결정 1).
확인한 날: 2026-11-10. 근거와 원자료는 `docs/wix-platform-facts.md`, 쪽 구조는 실제 사이트의 쪽 데이터(2026-11-10)에서 읽었습니다.

## 0. 먼저 할 일

1. **GitHub Pages 켜기**: 저장소 Settings → Pages → Build and deployment → Source: Deploy from a branch → Branch: `main`, `/ (root)` → Save.
   켜고 몇 분 뒤 `https://doomsfrooky.github.io/WIX_DEV/site/home.html` 이 열려야 합니다. 열리기 전에 Wix 주소를 바꾸면 그 칸에 GitHub 404가 보입니다.
2. **갤러리 쪽부터 만들기**(아래 3절): 새 홈과 연구소 소개에 갤러리로 가는 링크가 있어서, /gallery 가 없으면 그 링크가 404입니다.
3. 쪽마다 주소·높이·설명을 넣고(1절), 홈과 연구소 소개는 옛 요소를 지운 뒤(2절) **게시**합니다.

## 1. 쪽별 표

모든 쪽에 요소가 둘입니다. 데스크톱 `#html1`(화면 폭으로 늘어난 상태, 지금 그대로 둠)과 모바일 전용 `#mobileHtml1`(320px)입니다. **새로 만들지 말고 지금 있는 요소의 출처만 바꿉니다.** 그래야 요소 ID, 늘이기, 전체 화면 허용이 그대로 남습니다.

| 쪽 (Wix 주소) | 요소 ID | 넣을 주소 | 데스크톱 높이 | 모바일 높이 | 요소 설명 (삽입 요소 설명 칸) |
|---|---|---|---|---|---|
| Home (/) | #html1, #mobileHtml1 | https://doomsfrooky.github.io/WIX_DEV/site/home.html | 4810 | 5360 | 청각재활연구소 홈: 연구소 소개, 연구 성과, 연구 분야, 연구실, 최근 소식 |
| About (/about) | #html1, #mobileHtml1 | https://doomsfrooky.github.io/WIX_DEV/site/about.html | 3290 | 3970 | 연구소 소개: 소개 글, 연구소장 인사말, 조직, 데이터센터, 협력 기관 |
| Research (/project) | #html1, #mobileHtml1 | https://doomsfrooky.github.io/WIX_DEV/site/research.html | 6200 | 9230 | 연구: 연구 분야와 논문, 학회 발표, 특허 목록 |
| People (/people) | #html1, #mobileHtml1 | https://doomsfrooky.github.io/WIX_DEV/site/people.html | 3940 | 4870 | 구성원: 팀별 연구원 소개와 사진 |
| Basic Lab (/about-1) | #html1, #mobileHtml1 | https://doomsfrooky.github.io/WIX_DEV/site/basic-lab.html | 4120 | 5800 | Basic Lab(기초팀) 소개: 연구 주제, 팀장, 구성원, 논문 |
| Hearing Lab (/hearing-lab) | #html1, #mobileHtml1 | https://doomsfrooky.github.io/WIX_DEV/site/hearing-lab.html | 5310 | 7130 | Hearing Lab(참조표준팀) 소개: 한국인 청각 참조표준데이터센터, 구성원, 논문 |
| HeAD Lab (/head-lab) | #html1, #mobileHtml1 | https://doomsfrooky.github.io/WIX_DEV/site/head-lab.html | 5940 | 7810 | HeAD Lab(데이터팀) 소개: 청각 빅데이터센터, 구성원, 논문 |
| Audiso (/audiso) | #html1, #mobileHtml1 | https://doomsfrooky.github.io/WIX_DEV/site/audiso.html | 3380 | 4680 | 오디에스오 소개: 회사, KOLAS 공인교정, 제품 |
| Contact (/연락처) | #html1, #mobileHtml1 | https://doomsfrooky.github.io/WIX_DEV/site/contact.html | 2200 | 1910 | 연락처: 주소, 전화, 이메일, 팀별 담당자, 지도 |
| Gallery (/blank) | #html1 (+ #mobileHtml1) | https://doomsfrooky.github.io/WIX_DEV/site/gallery.html | 3690 (늘이기가 안 되면 2750) | 2630 | 갤러리: 학회와 행사 사진, 영상 |

- 데스크톱 높이는 `docs/wix-heights.md` 의 '데스크톱' 열입니다. 지금 데스크톱 요소가 모두 화면 폭으로 늘어나 있어서(실제 사이트 CSS `width:100%`) 이 값을 씁니다. 2560px 화면에서도 높이는 1920과 같습니다.
- 요소 설명은 지금 비어 있어서 스크린리더가 모든 칸을 영어 'Embedded Content'로 읽습니다. 데스크톱·모바일 요소에 같은 문구를 넣습니다.

- 영어 편집(5절)에서는 같은 칸에 영어 설명을 넣습니다: Home 'RIHE home: the institute, research outcomes, research areas, labs and latest news', About 'About RIHE: introduction, director's message, organization, data centers and partners', Research 'Research: research areas, publications, conference presentations and patents', People 'People: members of each team with photos', Basic Lab 'Basic Lab: research topics, team leader, members and publications', Hearing Lab 'Hearing Lab: Korean hearing reference standard data center, members and publications', HeAD Lab 'HeAD Lab: hearing big data center, members and publications', Audiso 'Audiso: company, KOLAS-accredited calibration and products', Contact 'Contact: address, phone, email, team contacts and map', Gallery 'Gallery: photos and videos of conferences and events'.

### 요소 하나를 바꾸는 법

1. 에디터에서 요소를 클릭하고 **웹사이트 주소 입력**(Enter Website Address)을 누릅니다. 지금은 'HTML 코드' 방식이라 코드가 보이면 '웹사이트 주소'를 고릅니다.
2. **웹사이트 주소** 칸에 위 표의 주소를 넣습니다.
3. 같은 창의 **삽입 요소 설명**(What's in the embed?) 칸에 위 표의 설명을 넣고 **적용**(Apply)을 누릅니다.
4. 높이를 표의 숫자로 맞춥니다(요소를 고른 뒤 도구 모음의 크기 칸, 또는 아래 모서리를 끌어서). 위치는 x 0, y 0 그대로 둡니다.
5. 모바일 에디터로 바꿔 `#mobileHtml1` 도 같은 주소·설명을 넣고 모바일 높이로 맞춥니다(폭 320, x 0).
6. 요소를 감싼 칸(섹션)의 아래끝이 요소 아래끝을 따라오는지 봅니다.

에디터의 한국어 표기는 Wix 도움말(2025-08) 기준이라 조금 다를 수 있습니다.

## 2. 지울 것 (홈과 연구소 소개만)

나머지 쪽(연구부터 연락처까지)은 지울 것이 없습니다. 홈·연구소 소개의 페이지 코드는 비어 있어서 지워도 깨지는 것이 없습니다.

### 홈 (/)
데스크톱 에디터에서 **첫 섹션(#html1이 있는 칸) 아래의 섹션 다섯 개를 통째로** 지웁니다. 모두 모바일에서는 이미 숨겨져 있어서 모바일 화면은 바뀌지 않습니다. #html1 높이를 늘리기 전에 지우는 편이 쉽습니다.

| 지울 섹션 | 안에 있는 것 | 새 홈에서는 |
|---|---|---|
| 둘째 (높이 660) | 연구소 소개 영상 플레이어 | 새 홈과 갤러리의 영상 칸에서 재생 |
| 셋째 (385) | #html2, 성과 숫자 | 새 홈 첫 화면의 숫자 |
| 넷째 (1680) | 연구소 소개 슬라이드 그림 3장 | **새 사이트에 없음** |
| 다섯째 (660) | 'Digital Therapeutics' 책 소개, 캐리커처, 네이버 블로그 'Article' 버튼 | 책은 Audiso 쪽에 있음. **네이버 링크와 캐리커처는 없음** |
| 여섯째 (863) | #html3, 연구소장 | 새 홈의 연구소장 칸 |

### 연구소 소개 (/about)
데스크톱 에디터에서 지웁니다: **#html2, #html3, #html4**, 배경 영상이 깔린 띠 두 개(청각 빅데이터센터 홍보영상 띠, 뉴스 영상 띠), 맨 아래 **Pro Gallery**(사진 10장).
- Pro Gallery는 데스크톱·모바일 공용이라 데스크톱에서 지우면 모바일에서도 없어집니다. 사진 6장은 이미 새 갤러리에 있고, **슬라이드 그림 4장(31.png, 32.png, 33.png, 27.png)은 새 사이트에 없습니다.**
- **맨 아래 섹션은 지우지 마세요.** 데스크톱에서는 비지만 모바일의 `#mobileHtml1` 이 그 안에 있습니다. 데스크톱에서 높이만 최소로 줄입니다.
- 지운 뒤 #html1 이 든 섹션 높이를 3290으로(지금 3568), 모바일 섹션 높이를 3970으로(지금 4207) 맞춰 아래 빈칸을 없앱니다.

지운 그림과 영상 파일은 Wix 미디어 관리자에 그대로 남습니다.

## 3. 갤러리 쪽 새로 만들기 (/gallery)

지금 사이트에는 /gallery 쪽이 없습니다(404).
1. 쪽 추가 → 빈 쪽, 이름 'Gallery'. 빈 쪽의 기본 URL(슬러그)은 `blank` 입니다. **2026-11-11 게시본은 `/blank` 그대로 두기로 해서 새 쪽 안의 갤러리 링크도 `/blank`(영어 `/en/blank`)로 맞췄습니다**(`tools/core.py` `PATHS['gallery']`). 나중에 슬러그를 `gallery` 로 바꾸면(쪽 목록에서 Gallery 옆 ⋯ → 설정 → SEO 기본 → URL 슬러그) `PATHS` 도 `/gallery` 로 되돌리고 빌드합니다. 둘이 다르면 갤러리 링크가 404입니다.
2. 다른 쪽의 `#html1` 을 복사해 붙여 넣는 방법을 먼저 써 봅니다(화면 폭 늘이기가 따라오는지 확인). 안 되면 추가 → 삽입(Embed) → HTML iframe을 넣습니다.
3. 주소 `https://doomsfrooky.github.io/WIX_DEV/site/gallery.html`, 설명 '갤러리: 학회와 행사 사진, 영상', x 0, y 0.
4. 높이: 화면 폭으로 늘어나면 **3690**, 980 폭 그대로면 **2750**. HTML 요소의 늘이기는 Wix가 공식으로 지원한다고 적어 둔 요소가 아니라서 새 요소에서는 안 될 수 있습니다.
5. 모바일: 다른 쪽처럼 데스크톱 요소를 모바일에서 숨기고 모바일 전용 HTML 요소(폭 320, 높이 **2630**, 같은 주소·설명)를 넣습니다.
6. 메뉴(메뉴 및 페이지)에 Gallery를 넣습니다. 지금 메뉴는 9개(Home부터 Contact)입니다.
7. 영상 전체 화면이 되는지 봅니다. 기존 요소에는 전체 화면 허용이 켜져 있습니다. 새 요소에 없으면 페이지 코드에 `$w('#html1').allowFullScreen();` 한 줄을 넣습니다.

## 4. 게시하고 확인

- Wix에서 **게시**합니다. 데스크톱과 휴대폰에서 10쪽을 열어 아래가 잘리거나 빈칸이 크게 남지 않는지 봅니다.
- 저장소를 고친 뒤 실제 사이트에 반영되기까지 최대 10분 걸립니다(Pages 배포 + 캐시 max-age=600).
- 내용 길이가 바뀌면(논문·발표·구성원·사진 추가) `docs/wix-heights.md` 를 다시 재고 **Wix에서는 그 요소의 높이만** 고칩니다. 사진 칸 크기가 같아서 구성원 사진만 넣을 때(예: 신중환 선생님)는 높이가 바뀌지 않습니다.
- githack 미리보기 주소는 Wix 안에 넣을 수 없습니다(CLAUDE.md "미리보기 링크"). Wix에는 위 표의 Pages 주소만 넣습니다.
- 다른 쪽에서 오는 링크 중 쪽 안의 위치를 가리키는 것(예: 연구실 쪽 '학회 발표 목록은 연구 페이지에서 보기')은 대상 쪽의 맨 위로 갑니다. 그 자리로 보내려면 Wix 페이지 코드가 따로 필요합니다(`docs/wix-platform-facts.md` 끝).

## 5. 영어판 (Wix Multilingual)

2026-11-11 켜고 공개했습니다(영어 `https://www.smilesnail.org/en/...`). 아래는 그때 한 순서이고, 다시 할 때나 다른 언어를 더할 때 씁니다.

### 켜는 순서 (Wix 도움말 'Wix 다국어 추가 및 설정하기', 2026-11-11 확인)
1. 앱 마켓 검색창에 **'Wix 다국어'** 를 그대로 넣고(도움말의 이름입니다. '다국어'만 치면 추천 목록에 다른 앱만 보일 수 있습니다) Wix가 만든 **Wix 다국어** 를 골라 **사이트에 추가**를 누릅니다. 사이트 대시보드의 앱 마켓에서 해도 같습니다. 에디터 위 **설정** 메뉴에 **다국어**가 보이면 거기서 바로 시작해도 됩니다.
2. 대시보드 → **다국어** → **지금 시작하기**. 기본 언어는 **한국어**로 확인합니다(정한 뒤에는 바꿀 수 없습니다). 국기를 고르고 **+ 언어 추가** → 언어 **English**, 국기 → **번역 시작 방법**: **수동 번역** → **English 사이트를 바로 공개할까요?**: **아니요, 지금은 숨깁니다** → **언어 추가**.
3. 언어 전환 → English에서 메뉴·머리글·바닥글 글자와 쪽마다 SEO 제목을 번역합니다. **영어 쪽 주소(slug)는 한국어와 똑같이 둡니다.** iframe 안 링크가 `/en/<한국어 쪽 주소>` 로 가기 때문입니다(`tools/core.py` 의 `EN_PREFIX = '/en'`, Wix 기본 방식인 하위 디렉터리 `/en/...` 와 같음).
4. 아래 '언어 전달'을 합니다.
5. 영어 미리보기를 확인한 뒤 대시보드 → 다국어 → 상태를 **공개**로 바꾸고 게시합니다. '언어 자동 전환'은 끕니다(Wix가 SEO에 나쁘다고 안내).
- 영어판을 공개하면 블로그·회원 같은 앱 쪽에도 영어 주소가 생깁니다. 공개 전에 살펴봅니다.

### 언어 전달
**2026-11-11 확인: 코드 없는 방법이 됩니다.** 영어 편집에서 요소 주소 끝에 `?lang=en` 을 붙이면 영어 쪽에만 들어가고, 한국어 쪽 주소는 그대로입니다(실제 사이트에서 한국어 20칸은 `?lang=en` 없음, 영어 20칸은 모두 `?lang=en`, 데스크톱·모바일 10쪽씩). 그래서 아래 페이지 코드는 쓰지 않았습니다.
1. 언어 전환 → English에서 `#html1` 을 고르고 '번역 편집' 또는 '웹사이트 주소 입력'으로 주소 칸이 열리는지 봅니다.
2. 열리면 주소 끝에 `?lang=en` 을 붙여 적용합니다(예: `.../site/home.html?lang=en`). 설명 칸도 영어로 바꿀 수 있으면 바꿉니다.
3. 한국어로 돌아와서 한국어 요소의 주소에 `?lang=en` 이 **없어야** 합니다. 한국어 쪽까지 바뀌었다면 되돌리고 아래 코드를 씁니다.

Wix 도움말에는 HTML 요소의 언어별 주소가 나오지 않습니다(번역 가능 목록에 없음). 안 되면 **페이지 코드**를 씁니다. 개발자 모드를 켜고 10쪽의 페이지 코드에 각각 붙여 넣습니다(쪽마다 `$w.onReady` 하나).

```js
import wixWindowFrontend from 'wix-window-frontend';

// 이 쪽의 HTML 요소 ID. 없는 ID는 건너뜁니다.
const FRAMES = ['#html1', '#mobileHtml1'];

$w.onReady(function () {
  const ml = wixWindowFrontend.multilingual;
  if (!ml.isEnabled) return;                                    // 다국어가 꺼져 있으면 아무것도 하지 않습니다(쪽은 한국어).
  const lang = ml.currentLanguage === 'en' ? 'en' : 'ko';
  FRAMES.forEach((id) => {
    let el = null;
    try { el = $w(id); } catch (e) { return; }
    if (!el) return;
    // 1) 영어면 주소에 ?lang=en 을 붙입니다. 처음부터 영어로 그려져 한국어가 먼저 보이지 않습니다.
    if (lang === 'en' && typeof el.src === 'string' && el.src) {
      const base = el.src.replace(/[?#].*$/, '');
      if (el.src !== base + '?lang=en') el.src = base + '?lang=en';
    }
    // 2) 주소가 늦게 바뀐 경우를 위해 메시지로도 알립니다(같은 언어면 iframe이 무시합니다).
    if (wixWindowFrontend.rendering.env !== 'browser' || typeof el.postMessage !== 'function') return;
    const send = () => { try { el.postMessage({ lang }); } catch (e) {} };
    send();                                                     // Wix가 iframe 로드가 끝날 때까지 들고 있다가 전달
    el.onMessage(() => send());                                 // 갤러리가 {type:'ready'} 를 보내오면 다시
    [1000, 3000, 6000].forEach((ms) => setTimeout(send, ms));
  });
});
```

- 언어를 바꾸면 Wix가 쪽 전체를 다시 불러오므로 이 코드도 다시 돌고, 따로 언어 변경을 기다릴 필요가 없습니다.
- 갤러리 쪽에서 CMS 연동 코드(`tools/pages/gallery.md`)도 쓴다면 같은 `$w.onReady` 안에 합칩니다. 지금처럼 사진을 저장소에서 관리하면 CMS 코드는 필요 없습니다.
- 이 코드는 Wix 렌더러의 메시지 처리를 흉내 낸 로컬 시험에서 확인했습니다(실제 Wix 에디터에서는 아직 안 돌려 봤습니다). 실제 사이트에서는 `https://www.smilesnail.org/en/project` 를 열어 영어로 보이면 됩니다.
- 쪽 높이는 언어마다 같아서(`docs/wix-heights.md` KO = EN) 영어용으로 따로 맞출 것이 없습니다. Wix도 언어별 크기 조정을 지원하지 않습니다.
- 요소 설명(삽입 요소 설명)의 언어별 번역은 Wix 도움말에 없습니다. 안 되면 영어 방문자의 스크린리더도 한국어 설명을 읽습니다.

## 6. 저장소를 연구소 계정으로 옮길 때

저장소를 다른 계정으로 옮기거나 이름을 바꾸면 Pages 주소가 바뀌고, **GitHub은 옛 Pages 주소를 새 주소로 넘겨주지 않습니다.** 옮긴 뒤 새 주소에서 Pages를 다시 켜고, Wix의 요소 주소를 모두 바꿔야 합니다. 쪽 파일 안에는 Pages 주소가 박혀 있지 않아서(모두 상대 경로) 저장소 쪽에서 고칠 것은 `CLAUDE.md` 결정 1의 주소뿐입니다.

새 주소 모양: `https://<새 계정>.github.io/<저장소 이름>/site/<쪽>.html`

| 쪽 | Wix 요소 | 지금 주소 | 새 주소 |
|---|---|---|---|
| Home | #html1, #mobileHtml1 | https://doomsfrooky.github.io/WIX_DEV/site/home.html | https://<새 계정>.github.io/<저장소>/site/home.html |
| About | #html1, #mobileHtml1 | https://doomsfrooky.github.io/WIX_DEV/site/about.html | https://<새 계정>.github.io/<저장소>/site/about.html |
| Research | #html1, #mobileHtml1 | https://doomsfrooky.github.io/WIX_DEV/site/research.html | https://<새 계정>.github.io/<저장소>/site/research.html |
| People | #html1, #mobileHtml1 | https://doomsfrooky.github.io/WIX_DEV/site/people.html | https://<새 계정>.github.io/<저장소>/site/people.html |
| Basic Lab | #html1, #mobileHtml1 | https://doomsfrooky.github.io/WIX_DEV/site/basic-lab.html | https://<새 계정>.github.io/<저장소>/site/basic-lab.html |
| Hearing Lab | #html1, #mobileHtml1 | https://doomsfrooky.github.io/WIX_DEV/site/hearing-lab.html | https://<새 계정>.github.io/<저장소>/site/hearing-lab.html |
| HeAD Lab | #html1, #mobileHtml1 | https://doomsfrooky.github.io/WIX_DEV/site/head-lab.html | https://<새 계정>.github.io/<저장소>/site/head-lab.html |
| Audiso | #html1, #mobileHtml1 | https://doomsfrooky.github.io/WIX_DEV/site/audiso.html | https://<새 계정>.github.io/<저장소>/site/audiso.html |
| Contact | #html1, #mobileHtml1 | https://doomsfrooky.github.io/WIX_DEV/site/contact.html | https://<새 계정>.github.io/<저장소>/site/contact.html |
| Gallery | #html1, #mobileHtml1 | https://doomsfrooky.github.io/WIX_DEV/site/gallery.html | https://<새 계정>.github.io/<저장소>/site/gallery.html |

영어판에서 언어별 주소(`?lang=en`)를 요소에 직접 넣었다면 그 영어 쪽 주소 10개도 같이 바꿉니다. 무료 계정이면 Pages를 쓰려면 저장소가 공개여야 합니다.

## 7. 머리글 메뉴 글꼴·색 (새 쪽과 맞추기)

머리글(로고와 메뉴)은 Wix가 모든 쪽에 붙이는 부분이라 저장소가 아니라 Wix에서 바꿉니다. 2026-11-10에 실제 사이트에서 잰 값과 바꿀 값입니다. 비교 그림은 대화에 보낸 `menu-before-after.png`.

| | 지금 | 바꿀 값 |
|---|---|---|
| 데스크톱 글꼴 | Avenir Light 14px | **Archivo Medium** 15px(굵게 끔) |
| 데스크톱 기본 글자색 | #000000 | **#696660** |
| 데스크톱 마우스오버 | #191919 | **#0f0e0c** |
| 데스크톱 클릭(현재 쪽) | #191919 | **#8a5a0e** |
| 모바일 메뉴 글꼴 | Futura Light 20px | **Archivo Medium** 18px |
| 모바일 기본 / 선택 | #000000 / #C58455 | **#0f0e0c / #8a5a0e** |
| 모바일 메뉴 아이콘 선 | #000000 | #0f0e0c |

1. **글꼴 올리기**: Archivo는 Wix 글꼴 목록에 없습니다. 아무 글자 상자 → 텍스트 편집 → 글꼴 목록 → **글꼴 업로드** → `Archivo-Medium.ttf`(SIL Open Font License, 무료로 써도 됨) → 이후 글꼴 목록의 **내 글꼴**에서 고릅니다. 올리기 싫으면 Wix 목록의 Helvetica가 가장 가깝습니다.
2. **데스크톱 메뉴**: 메뉴 클릭 → 디자인(붓) → **디자인 사용자 지정** → 기본 탭 > 텍스트(글꼴·크기·색) → 마우스오버 탭 > 텍스트 색 → 클릭 탭 > 텍스트 색. 다른 추천 디자인을 누르면 메뉴 모양이 바뀌니 누르지 않습니다.
3. **모바일 메뉴**: 모바일 에디터 → 메뉴 아이콘 → 메뉴 편집 → 모바일 메뉴 → 디자인 → 기본 탭 > 텍스트, 선택 탭 > 텍스트 색.

- 지금 메뉴는 이전 방식의 '추천 디자인' 메뉴라서 밑줄과 글자 간격을 줄 수 없습니다. 그래서 현재 쪽은 새 쪽의 갈색 표시선 대신 갈색 글자(#8a5a0e)로 나타냅니다.
- 새 쪽처럼 현재 쪽 아래에 2px 갈색 선까지 넣으려면 메뉴를 **새 가로 메뉴**로 바꿔야 합니다(요소 추가 > 메뉴 및 앵커 > 가로 메뉴, 머리글에 넣고 옛 메뉴 삭제 → 디자인 사용자 지정 > 메뉴 아이템 > 현재 페이지 > 테두리: 아래만 2px #8a5a0e, 글자색 #0f0e0c). 옛 메뉴는 새 메뉴로 바꿀 수 없어서 새로 만들어야 합니다.
- Gallery까지 10개가 Archivo 15px로 한 줄에 들어갑니다(약 762px / 메뉴 칸 940px). '더보기'는 생기지 않습니다.
