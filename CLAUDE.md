# CLAUDE.md · RIHE 홈페이지 (smilesnail.org) 작업 안내

청각재활연구소(RIHE) 홈페이지 www.smilesnail.org 의 본문을 만드는 저장소다. 사이트는 Wix 클래식 에디터이고, 본문은 Wix HTML 요소(iframe)에 들어간다.
**공개 저장소다. 키, 토큰, Imgur Client-ID 같은 비밀값은 어디에도 넣지 않는다.**

## 구조 (README·tools/KIT.md 요약)

```
data/*.json                  논문·발표·특허·구성원·사진·영상 데이터 (문구와 사실의 원본, 지어내지 않는다)
tools/kit.py                 공통 디자인(토큰, 부품, CSS, JS). 3차에서 방향별 tools/kits/a.py, b.py, c.py 로 나눈다
tools/pages/<name>.py        페이지 내용. render() -> HTML
tools/build.py               python3 tools/build.py [--preview] [--only home,research] -> site/<name>.html
tools/build_v1.py            1차 KO/EN 문구 전체. 페이지 문구는 여기서 그대로 옮긴다
site/<name>.html             실제로 Wix에 들어가는 페이지(페이지당 1개, 데스크톱·모바일 공용, KO/EN)
site/_directions/            디자인 방향 시안 (확정 전)
site/vendor/                 npm에서 받아 버전을 고정한 라이브러리(GSAP 등). 페이지는 필요한 파일만 상대 경로로 부른다
site/index.html              시안·페이지 목록(작업용, noindex)
site/_probe.html             Wix 주소 방식 실측 페이지
tools/wix-sim.html           Wix 흉내(헤더 + 고정 높이 교차 출처 iframe)
tools/verify/                검증 스크립트(아래)
docs/wix-platform-facts.md   Wix 플랫폼 조사 결과(근거 포함)
embeds/                      1차(현재 게시된) Wix 코드 사본. fetch_live.py로 다시 받는다
```

페이지 10개: home(/), about(/about), research(/project), people(/people), basic-lab(/about-1), hearing-lab, head-lab, audiso, contact(/연락처), gallery(/gallery).

## 결정한 것

1. Wix 요소는 **"웹사이트 주소"** 방식. 각 요소에 `https://doomsfrooky.github.io/WIX_DEV/site/<페이지>.html` 을 넣는다. 그 뒤 수정은 저장소에서만, Wix는 높이를 바꿀 때만 연다.
   - 주소 방식으로 바뀐 뒤에는 **main = 실제 사이트**다. 확정 전 작업은 브랜치에서만, 승인받은 것만 main에 머지한다. 머지 후 반영까지 최대 10분(Pages 배포 + max-age=600).
2. 사진·영상은 저장소에 넣지 않는다. Wix 미디어(static.wixstatic.com, video.wixstatic.com)와 Imgur 주소를 그대로 참조한다(Pages 1GB, 월 100GB).
3. 디자인 판단은 사용자가 한다. 방향 시안을 보여 주고 고르게 한다.
4. **스킬 규칙보다 이 프로젝트의 지시가 우선이다.** 부딪히면 지시를 따르고, 건너뛴 규칙을 보고에 적는다.
   - design-taste-frontend 의 업종별 셰이더·루프 영상·장면 효과 금지 규칙은 적용하지 않는다. 첫 화면은 "모션 목표"대로 만든다.
   - design-taste-frontend 의 주소·전화·이메일을 줄이거나 `.example` 로 바꾸는 규칙도 적용하지 않는다. 실제 연구소 정보를 쓴다.
   - 어떤 스킬이 100vh, sticky, 스크롤 연동 효과를 권해도 아래 "Wix iframe에서 모션이 동작하는 조건"을 따른다.

## 작업 규칙

- Wix HTML 요소는 높이가 자동으로 바뀌지 않는다. 내용 길이를 바꾸면 높이 표(`docs/wix-heights.md`)도 같이 고친다.
- 모바일은 같은 파일을 320px 폭에서 보이게 만든다(Wix 모바일 viewport가 width=320).
- Imgur 주소의 대소문자는 절대 바꾸지 않는다.
- 이메일이 Cloudflare 이메일 보호로 깨지지 않는지 확인한다. 미리보기 주소에서 가려져 보이면 저장소 원본부터 확인하고, 원본이 맞으면 고치지 않는다.
- 제안을 늘어놓지 말고 사용자가 고른 것을 정확히 구현한다. 지정하지 않은 부분은 건드리지 않는다.
- 수정은 브랜치와 PR로 한다. 데이터와 문구는 그대로 둔다. 저자 목록은 게시된 원문을 유지한다.

### 문구·언어·링크 (2차 규칙을 이어받음)
- 화면의 모든 문구는 `t(ko, en)` 쌍. `t(ko, en, 'p')` 처럼 태그 지정, `tt(pair)`, 언어 중립은 `t(text)`.
- 언어는 `?lang=en|ko` 를 head 스크립트가 **첫 화면을 그리기 전에** 적용한다. Wix 페이지 코드의 `postMessage({lang})` 도 받는다. 영어 화면에서 한국어가 먼저 보였다 바뀌는 깜빡임이 없어야 한다.
- 이미지 alt는 쌍(`data-alt-en`), aria-label은 `data-aria-en`.
- 페이지 사이 링크는 `link()`·`more()` 로 만들고 `kit.PATHS` 경로를 쓴다. 모두 `target="_top"`. Wix Multilingual은 꺼져 있어서 `/en/...` 이 404다(그동안 `EN_PREFIX` 처리 주의).
- `build.py` 검사(실패하면 빌드 중단): 화면 문구의 em-dash(—) 금지, `data-l="en"` 에는 `lang="en"`, `<script src>` 는 `vendor/` 상대 경로만, robots meta 필수, vh·svh·dvh·innerHeight 금지.
- 검색 노출: 본문 페이지 `<meta name="robots" content="noindex, indexifembedded">`(kit.ROBOTS), 시안·목록·도구는 `noindex`.
- 한글 글꼴은 필요한 글자만 받는다(Google Fonts `text=` 서브셋).

## Wix iframe에서 모션이 동작하는 조건 (중요)

Wix HTML 요소는 내용 높이만큼 큰 iframe이고, 스크롤은 바깥 Wix 페이지가 한다. iframe 안 window는 스크롤되지 않는다. Wix(smilesnail.org)와 iframe(github.io)은 출처가 다르다.

- **되는 것**
  - IntersectionObserver 등장 애니메이션. 교차 출처에서도 최상위 화면 기준으로 동작한다. 단 **`rootMargin` 은 무시되고 `rootBounds` 는 null**. 등장 시점은 `threshold` 로만 조절한다.
  - 시간 기반 애니메이션, 호버, 캔버스·WebGL, 자동재생 루프 영상(muted, playsinline, loop, autoplay, poster).
- **그대로는 안 되는 것**
  - GSAP ScrollTrigger scrub, 스크롤 진행률 기반 parallax, CSS `animation-timeline: scroll()/view()`.
  - Lenis 같은 부드러운 스크롤, wheel·touchmove 의 `preventDefault` (바깥 페이지 스크롤까지 막는다).
  - position: sticky·fixed 고정 연출.
  - **화면 높이 기준 크기.** iframe 안 `100vh`·`svh`·`dvh`·`window.innerHeight` 는 Wix 요소 전체 높이(수천 px)다. 첫 화면 높이는 `aspect-ratio` 나 고정 px로 정한다.
  - 바깥 화면 한 장(실측 2026-11-06): 데스크톱은 창 높이(650~950px)에서 Wix 헤더 217px(스크롤되면 사라짐)을 뺀 만큼이 첫 화면. 모바일은 viewport 320×약 690, 헤더 140px이 **sticky** 라서 보이는 띠는 약 480~610px. IntersectionObserver는 sticky 헤더에 가려진 부분도 "보임"으로 센다.
- **대안** (위에서부터)
  1. 센티널: 문서 전체에 100px 안팎의 투명 요소를 빈틈없이 깔고 threshold를 1% 단위로 준다. 걸친 요소의 `intersectionRect` 로 보이는 구간을 1px 단위로 추정해 parallax·scrub을 근사한다(`site/_probe.html` 에 동작 예시). 페이지가 `window.RIHE.band = {top, bottom}`(문서 px)을 내놓으면 `wixsim.js` 가 실제 값과의 오차를 잰다. 모바일 성능은 실측한다.
  2. 요소마다 threshold 0~1을 50단계 이상 주고 보이는 비율로 진행률 계산.
  3. Wix 설정 > 사용자 지정 코드(Body 끝)에서 부모 스크롤 값을 postMessage로 보내는 브리지(비공식). 실측해서 될 때만, **쓰기 전에 사용자에게 먼저 알린다.**
- 사진·영상을 WebGL·캔버스에 넣을 때: static.wixstatic.com, video.wixstatic.com, i.imgur.com 모두 `access-control-allow-origin: *` 이고 캔버스가 오염되지 않음을 확인했다(2026-11-06). `crossorigin="anonymous"` 를 붙인다.
- 성능·접근성: 화면 밖 애니메이션은 멈춘다. WebGL은 모바일에서 단순화하거나 정지 이미지로. 60fps, 첫 화면 2.5초 안. `prefers-reduced-motion` 이면 처음부터 정지 상태.
- 콘텐츠가 숨은 채로 남으면 안 된다: 숨김 상태는 `html.js` 아래에서만, IO 콜백이 1.5초 안에 없으면 전부 표시, 스크립트 실패 시 CSS 타이머로 표시(2차 kit의 안전장치를 이어받는다).

## 라이브러리

GSAP(SplitText 포함) 또는 Motion. CDN으로 부르지 않는다. `npm` 으로 받아 버전을 고정하고 필요한 파일만 `site/vendor/<패키지>@<버전>/` 에 복사해서 상대 경로로 부른다. 클라우드 기본 네트워크에는 jsDelivr·unpkg가 없을 수 있다.

## 검증 (`tools/verify/`)

Node와 미리 설치된 Playwright로 돈다(`npm install` 불필요). 저장소 루트에서 실행한다. 페이지는 로컬 서버 두 개로 띄운다: 바깥 `http://localhost:8001`, 안쪽 `http://127.0.0.1:8002`(교차 출처).

```
node tools/verify/render.js   site/home.html <out> [--widths 1280,320] [--langs ko,en] [--frames]   # 전체 스크린샷 + 점검(stillInvisible·brokenImages·errors 모두 0)
node tools/verify/wixsim.js   site/home.html <out> [--w 1280|320] [--lang en]                       # Wix처럼 교차 출처 iframe에서 바깥을 스크롤. 시간순(t*)·스크롤순(s*) 스크린샷
node tools/verify/interact.js site/research.html [--width 320]                                      # 모든 버튼·필터·페이저를 눌러도 높이가 그대로인지
node tools/verify/heights.js  site/home.html site/about.html --md                                   # 폭·언어별 문서 높이 → docs/wix-heights.md (+24px, 10 단위 올림)
node tools/verify/fallback.js site/home.html [--width 320] [--out dir]                              # JS 끔 / 주 스크립트 실패 / 동작 줄이기 에서 숨은 내용 0
node tools/verify/shoot.js    site/home.html out.png [--width 320] [--sel ".hero"] [--lang en] [--scale 2] [--full]
node tools/verify/probe.js    site/home.html "document.fonts.size" [--width 320]
```

- 값 없는 플래그(`--frames`, `--full`, `--md`)는 맨 끝에 둔다.
- 헤드리스 Chrome은 i.imgur.com에서 403을 받는다(일반 브라우저와 curl은 200). 그래서 `lib.js` 가 imgur 파일만 curl로 받아 `tools/verify/.mirror/`(gitignore)에서 내준다. 실제 사이트와는 무관하다.
- 다른 외부 주소가 Chrome에서만 막히면 `python3 tools/verify/mirror.py site/home.html` 로 받아 두고 `MIRROR=1 node tools/verify/render.js ...` 로 띄운다. 빠진 주소는 결과의 `notInMirror` 에 나온다.
- 움직임은 스크린샷으로 판단하기 어렵다. 핵심 장면은 시간순 4~6장(`--frames`, `wixsim.js` 의 t*)으로 보고, 미리보기 링크를 같이 준다.

## 미리보기 링크

확정 전 시안은 main에 머지하지 않고 커밋 해시 주소로 보여 준다(브랜치 이름의 슬래시가 주소를 깨므로 해시를 쓴다).

```
페이지:        https://raw.githack.com/Doomsfrooky/WIX_DEV/<해시>/site/_directions/a.html
wix-sim:       https://raw.githack.com/Doomsfrooky/WIX_DEV/<해시>/tools/wix-sim.html?src=https://rawcdn.githack.com/Doomsfrooky/WIX_DEV/<해시>/site/_directions/a.html
wix-sim 320:   위 주소에 &w=320
목록:          https://raw.githack.com/Doomsfrooky/WIX_DEV/<해시>/site/index.html  (wix-sim 링크를 자동으로 만든다)
```

## 스킬 (`.claude/skills/`)

design-taste-frontend(Leonxlnx/taste-skill), impeccable(pbakaus/impeccable, Apache 2.0, LICENSE·NOTICE.md 동봉), 67·aura-farming(Jakeschincariol/claude-illegal-codes, MIT). impeccable 엔진은 처음 실행할 때 `~/.impeccable` 로 내려받는다(저장소에 넣지 않음). 위 "결정한 것 4"가 스킬 규칙보다 우선한다.
