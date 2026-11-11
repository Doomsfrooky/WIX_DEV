# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

방문자 집단 세 가지를 모두 주 방문자로 둔다(우선순위 없음, 2026-11-06 사용자 답변).

- 연구원·의료진: 공동연구, 논문·데이터 확인, 학회 등에서 연구소를 알게 된 사람.
- 학생·지원자: 대학원 진학이나 연구원 채용에 관심 있는 사람.
- 기업·기관: 기술이전, 의료기기, 데이터센터 협력 상대, 정부·평가 기관.

환자·보호자·일반인은 주 방문자로 지정하지 않았다(사용자가 고른 목록에 없음).

## Product Purpose

연세대학교 원주세브란스기독병원 청각재활연구소(RIHE, Research Institute of Hearing Enhancement)의 홈페이지 www.smilesnail.org.
사이트가 방문자에게 가장 먼저 해내야 하는 일은 **연구 역량에 대한 신뢰**다: 논문·특허·데이터센터·연구실 규모로 실제로 연구하는 연구소임을 보여 준다(2026-11-06 사용자 답변).

연구소 소개 문구(tools/kit.py `MISSION`): "난청의 기전에 대한 기초 연구를 바탕으로 치료제 개발, 임상 연구, 의료기기 개발까지 청각에 대한 전주기적 연구를 하는 연구소입니다."

## Positioning

저장소에 있는 사실만 적는다.

- 기초 연구에서 치료제, 임상시험, 의료기기까지 청각을 전주기로 연구한다(`MISSION`, `AREAS`: 기초 연구, 빅데이터·인공지능, 의료기기, 임상시험).
- 국내 유일 기관 두 곳을 운영한다(`DATA_CENTERS`): 한국인 청각 참조표준데이터센터(2019년 1월부터), 청각 빅데이터센터(10만 건 이상의 데이터).
- 연구실과 회사: Basic Lab(기초팀), Hearing Lab, HeAD Lab(Hearing AI & Data Lab), Audiso(연구소 기반 회사).

## Operating Context

- 사이트는 Wix 클래식 에디터이고 본문은 Wix HTML 요소(iframe)에 들어간다. 3차부터 각 요소는 GitHub Pages 주소(`site/<페이지>.html`)를 띄운다. 데스크톱과 모바일(320px 폭)이 같은 파일을 쓴다.
- 한국어와 영어. 영어는 `?lang=en` 또는 Wix 페이지 코드의 postMessage로 바뀐다. Wix Multilingual은 아직 꺼져 있다.
- 콘텐츠 원본은 `data/*.json` 과 `tools/build_v1.py` 의 1차 문구이고, `tools/build.py` 로 페이지를 만든다.

## Capabilities and Constraints

- 페이지 10개: Home, About, Research(/project), People, Basic Lab(/about-1), Hearing Lab, HeAD Lab, Audiso, Contact(/연락처), Gallery(/gallery).
- iframe 제약(CLAUDE.md "Wix iframe에서 모션이 동작하는 조건"): 높이 고정, 100vh·sticky·fixed·스크롤 가로채기 금지, 클릭으로 높이가 늘어나는 내용 금지, 스크롤 연동 효과는 IntersectionObserver 근사로만.
- 영상은 Wix 미디어 주소를 참조한다. 이미 Wix·Imgur에 있는 사진도 주소 그대로 쓰고, 새 구성원·갤러리 사진과 도표는 저장소 `site/media/` 에 웹용 사본만 둔다(`tools/media.py`, 2026-11-09 결정).
- Gallery 페이지는 Wix CMS 목록을 postMessage로 받을 수 있다(`tools/pages/gallery.md`).

## Brand Commitments

- 따로 지켜야 할 기관 디자인 규정은 없다(2026-11-06 사용자 답변). 지금 쓰는 기관명 표기와 로고를 그대로 쓴다: "연세대학교 원주세브란스기독병원" / "Yonsei University · Wonju Severance Christian Hospital", "청각재활연구소" / "Research Institute of Hearing Enhancement", HeAD Lab·Audiso 로고, 데이터센터 로고.
- 연구실 이름(Basic Lab, Hearing Lab, HeAD Lab, Audiso)은 두 언어 모두 라틴 문자로 쓴다.
- 도메인 smilesnail.org.

## Evidence on Hand

- 학술지 논문 121편(`data/publications.json`), 학회 발표 110건(`data/reports.json`), 특허 80건(`data/patents.json`), 기술이전 12건(1차 문구, 데이터 아님). (2026-11-10 기준)
- 구성원 36명, 팀 6개(`data/people.json`: 교수진 3, Basic 5, Hearing 5, HeAD 6, 행정 4, Audiso 13). 36명 모두 사진이 있다(Imgur 27, 저장소 9).
- 갤러리 사진 59장(`data/gallery.json`: 저장소 사본 53, Wix 미디어 6), 영상 3편(`data/videos.json`, Wix 영상: 연구소 소개, 청각빅데이터센터 홍보, G1 뉴스).
- 연구소장 인사말과 약력(`tools/kit.py` `DIRECTOR`), 협력 기관 로고(About).
- 없는 것: 추천사·후기, 수상 목록 데이터, 환자 대상 안내 자료, 영문 보도자료. 만들어 넣지 않는다.

## Product Principles

1. 신뢰는 실제 숫자와 실제 사람에서 나온다. 논문·특허·데이터센터·구성원은 데이터에서 그대로 가져오고, 지어내지 않는다.
2. 세 방문자 집단이 각자 필요한 것(연구 성과, 사람과 연구실, 협력 창구)에 두 번 안에 닿게 한다.
3. 읽는 구간(논문 목록, 구성원)은 차분하게 둔다. 움직임은 의미 있는 곳에만 쓴다.
4. 한국어와 영어가 같은 품질이어야 한다. 한국어를 영어에서 번역하지 않는다.
5. Wix iframe 안에서 실제로 동작하는 것만 내놓는다. wix-sim과 실측으로 확인한 뒤 보여 준다.

## Accessibility & Inclusion

- `prefers-reduced-motion` 이면 처음부터 정지 상태로 보여 준다.
- 스크립트가 실패해도 내용이 숨은 채로 남지 않는다(2차 kit의 안전장치).
- 이미지 alt와 aria-label은 KO/EN 쌍. 지금은 모든 Wix HTML 요소가 스크린리더에 영어 기본값 'Embedded Content'로 읽히므로, 3단계에서 요소마다 한국어 설명을 넣는다(`docs/wix-platform-facts.md`).
