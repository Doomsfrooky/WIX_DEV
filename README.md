# WIX_DEV

청각재활연구소(RIHE) 홈페이지 [www.smilesnail.org](https://www.smilesnail.org)의 본문 저장소입니다(3차 개편, 2026-11, 디자인 C2).

사이트는 Wix 클래식 에디터입니다. 쪽마다 본문은 Wix **HTML 요소** 하나(데스크톱 `#html1`, 모바일 `#mobileHtml1`)이고, [docs/wix-connect.md](docs/wix-connect.md) 대로 전환하면 이 요소가 **웹사이트 주소** 방식으로 이 저장소의 GitHub Pages 파일 `https://doomsfrooky.github.io/WIX_DEV/site/<쪽>.html` 을 불러 보여 줍니다. 그 뒤로는 내용은 이 저장소에서만 고치고, Wix는 요소 높이를 바꿀 때만 엽니다. main에 머지하면 10분 안에 사이트에 반영됩니다(전환 뒤 main = 실제 사이트).

**2026-11-11 전환해서 게시했습니다**(한국어 `https://www.smilesnail.org/`, 영어 `https://www.smilesnail.org/en/`, 영어 요소는 주소 끝에 `?lang=en`). 이제 main에 머지하면 실제 사이트에 반영됩니다. 게시된 상태는 `python3 tools/fetch_live.py` 가 `docs/site-map.md` 로 받아 둡니다.

- Wix 쪽 연결(쪽별 요소·주소·높이·설명, 지울 요소, 갤러리 쪽 만들기, 메뉴 글꼴·색, 영어판): [docs/wix-connect.md](docs/wix-connect.md)
- 요소 높이 표: [docs/wix-heights.md](docs/wix-heights.md)
- 작업 규칙: [CLAUDE.md](CLAUDE.md), 디자인 기록: [DESIGN.md](DESIGN.md), 공통 부품 설명: [tools/KIT.md](tools/KIT.md)

## 구조

```
data/*.json                 논문·학회 발표·특허·구성원·사진·영상 (내용의 원본)
tools/kit.py, kit_assets/   공통 디자인(부품, CSS, JS)과 Home 첫 화면
tools/pages/<쪽>.py         쪽별 내용
tools/build.py              site/<쪽>.html 을 만들고 검사(--preview: site-preview/, 언어 전환 버튼 포함)
tools/media.py              사진 넣기(구성원 사진, 갤러리, 도표). 메타데이터를 지운 웹용 사본만 site/media/ 에
tools/verify/               검증(렌더, Wix 흉내, 버튼, 높이, JS 끔)
site/<쪽>.html              Wix가 (전환 뒤) 불러 가는 쪽 10개(데스크톱·모바일 공용, 한국어·영어)
site/media/, site/vendor/   사진 사본, 버전을 고정한 라이브러리(GSAP)
tools/fetch_live.py         게시된 Wix 쪽의 HTML 요소 상태를 받아 docs/site-map.md 로
embeds/, docs/paste-list.md, docs/redesign.md   1·2차 기록(옛 HTML 코드 붙여넣기 방식, 2차 시안). 지금은 쓰지 않습니다
```

쪽 10개: home(/), about(/about), research(/project), people(/people), basic-lab(/about-1), hearing-lab, head-lab, audiso, contact(/연락처), gallery(/gallery).

## 고쳐서 반영하는 순서

1. 내용은 `data/*.json`, 문구와 배치는 `tools/pages/<쪽>.py`·`tools/kit.py` 에서 고칩니다. 사진은 `python3 tools/media.py` 로만 넣습니다.
2. `python3 tools/build.py` 로 `site/*.html` 을 만듭니다(검사에 걸리면 멈춥니다).
3. `tools/verify/` 로 확인합니다(CLAUDE.md "검증").
4. 내용 길이가 바뀌었으면 `node tools/verify/heights.js site/<쪽>.html --fine --md` 로 높이를 재고 `docs/wix-heights.md`·`docs/wix-connect.md` 를 고칩니다.
5. 브랜치에서 커밋하고 PR로 main에 머지합니다. 높이가 바뀐 쪽만 Wix 에디터에서 요소 높이를 고치고 **게시**를 누릅니다.

전환 뒤에는 본문 코드를 Wix 코드 칸에 붙여 넣지 않습니다(1차 방식). 그러면 주소 방식 요소가 옛 코드로 돌아갑니다.
