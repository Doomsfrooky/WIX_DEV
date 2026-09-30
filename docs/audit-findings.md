# 점검 결과 전체 목록

[audit.md](audit.md)의 부록입니다. 2026-09-30에 게시된 사이트 기준이며, 항목마다 다른 에이전트가 파일을 다시 열어 반박을 시도했고 확인된 것만 남겼습니다(반박된 2건 제외). 위치의 줄 번호는 `embeds/` 파일 기준입니다.

## Home

### [중간] 홈 Outcomes의 'Journals 118'이 Research 페이지 논문 목록(총 120건)과 맞지 않음
- 분류: 내용·데이터 · 위치: `embeds/home/html2.outcomes.html:103`, `embeds/home/mobileHtml1.home.html:56`, `embeds/research/html1.research.html:497`, `embeds/research/html1.research.html:506`, `embeds/research/html1.research.html:3123`
- 영향: 데스크톱과 모바일의 모든 방문자가 홈 첫 성과 카드에서 118편을 보는데, Research 페이지에서는 '총 120건'이 보여 두 숫자가 어긋나고 성과 수치의 신뢰도가 떨어짐.
- 고치는 법: html2.outcomes.html:103과 mobileHtml1.home.html:56의 118을 120으로 바꾸고, Wix에서 #html2와 #mobileHtml1 두 요소를 모두 업데이트한 뒤 게시하세요. README의 수정 순서에 'Research에 논문을 추가하면 홈 Outcomes 두 파일도 수정'을 체크 항목으로 넣으세요.
- 검증 메모: 심각도 medium. 497·506행은 pub-item 시작 줄이고 제목은 498·507행 pub-title에 있음.

### [중간] 홈 페이지 제목(탭·검색결과·공유 미리보기)이 템플릿에 있던 '건강 | 청각재활연구소'로 남아 있음
- 분류: 내용·데이터 · 위치: `(게시된 페이지 HTML):189`, `(게시된 페이지 HTML):192`, `(게시된 페이지 HTML):208`, `(게시된 페이지 HTML):202`, `(Wix 페이지 데이터):1`
- 영향: 브라우저 탭과 북마크, 구글·네이버 검색결과 제목, 카카오톡·페이스북 공유 미리보기에 연구소와 관계없는 '건강'이 사이트 대표 제목으로 나옴.
- 고치는 법: Wix 에디터에서 홈 페이지 설정 > SEO 기본 > 페이지 제목을 '청각재활연구소 | Research Institute of Hearing Enhancement' 등으로 바꾸세요(og/twitter 제목도 같이 바뀜). 고급 SEO의 keywords는 '청각재활연구소, 난청, ...'처럼 쉼표로 나누세요.
- 검증 메모: 제목: '홈 페이지 SEO 제목이 연구소를 나타내지 않는 "건강 | 청각재활연구소"로 설정돼 있음'. '템플릿에 있던'이라는 말은 근거가 없으니 빼세요. keywords 쉼표 누락은 검색 순위에 거의 영향이 없는 low 수준 부수 사항임.

### [중간] 모바일 홈에 소개 영상, 연구소 소개 인포그래픽 3장, 책 'Article' 링크가 전혀 없음
- 분류: 데스크톱·모바일 불일치 · 위치: `(Wix 기본 요소 목록):3`, `(Wix 기본 요소 목록):5`, `(Wix 기본 요소 목록):6`, `(Wix 기본 요소 목록):7`, `(Wix 기본 요소 목록):10`, `(Wix 기본 요소 목록):17`, `(게시된 페이지 HTML):324`, `embeds/home/mobileHtml1.home.html:61`
- 영향: 모바일 방문자에게는 2분 29초 소개 영상, 연구소 설립 배경·성과·발전계획 인포그래픽 3장, 책 후기 링크가 보이지 않음. 모바일 DTx 블록에서는 책 소개를 눌러도 이동할 곳이 없음.
- 고치는 법: mobileHtml1.home.html의 DTx 블록(61–70행)에 `<a href="https://blog.naver.com/barunbooks7/223201924941" target="_blank" rel="noopener">Article</a>`를 추가하세요. 영상은 모바일 에디터에서 VideoPlayer의 숨기기를 해제하거나 mobileHtml1 위·아래에 따로 배치하세요. 인포그래픽은 모바일 폭(320px)에서 읽을 수 있는 텍스트 요약으로 넣으세요. 내용을 더한 뒤에는 #mobileHtml1 높이(현재 1493)를 다시 맞추세요.

### [중간] 모바일 연구소장·히어로 텍스트가 데스크톱과 다름(소속 누락·소속명 다름, 이메일 없음, 인사말·영문 소개 잘림)
- 분류: 데스크톱·모바일 불일치 · 위치: `embeds/home/html3.director.html:166`, `embeds/home/html3.director.html:171`, `embeds/home/html3.director.html:172`, `embeds/home/html3.director.html:174`, `embeds/home/html3.director.html:178`, `embeds/home/html3.director.html:181`, `embeds/home/html3.director.html:184`, `embeds/home/mobileHtml1.home.html:79` 외
- 영향: 모바일 방문자에게 연구소장 소속 하나(의학통계학과 겸임교수)가 빠지고 소속명도 다르게 보임. 연락처 이메일이 없고, 인사말과 영문 소개는 중간에서 잘린 채 표시됨.
- 고치는 법: mobileHtml1.home.html 80–84행 목록을 데스크톱 170–173행 4개 항목과 똑같이 맞추고, `<a href="mailto:okas2000@yonsei.ac.kr">okas2000@yonsei.ac.kr</a>`를 넣으세요. 79행 인사말에는 데스크톱 178행의 전체 문장을, 51행에는 데스크톱 62행의 전체 영문을 넣으세요. 고친 뒤 높이를 다시 재서 #mobileHtml1 높이를 조정하세요.
- 검증 메모: 영향: '인사말과 영문 소개가 중간에서 잘린 채 표시됨'을 '인사말과 영문 소개가 데스크톱보다 짧은 요약본으로만 제공됨'으로 고치세요. 실제 결함은 소속 1개 누락, 소속명 불일치, 이메일 누락임.

### [중간] 작은 보조 텍스트 색 #718096이 흰 배경에서 대비 4.02:1로 WCAG AA(4.5:1) 미달
- 분류: 접근성 · 위치: `embeds/home/html1.home-hero.html:45`, `embeds/home/html3.director.html:79`, `embeds/home/html3.director.html:85`, `embeds/home/html3.director.html:115`, `embeds/home/mobileHtml1.home.html:21`, `embeds/home/mobileHtml1.home.html:41`
- 영향: 저시력 사용자나 햇빛 아래 휴대폰 사용자는 영문 소개, 영문 인사말, 모바일 소속 목록(12px)을 읽기 어려움.
- 고치는 법: #718096을 #64748b(4.76:1)이나 #5f6b7a(5.43:1)처럼 4.5:1 이상인 색으로 바꾸세요. 모바일 41행 소속 목록은 본문 색 #4a5568(7.53:1)을 쓰고 글자 크기를 0.8rem 이상으로 키우세요.

### [중간] 홈 이미지 대체텍스트가 파일명('3.png' 등)이거나 뜻이 없는 값('DTx')임
- 분류: 접근성 · 위치: `(게시된 페이지 HTML):323`, `(게시된 페이지 HTML):329`, `(게시된 페이지 HTML):331`, `embeds/home/mobileHtml1.home.html:64`
- 영향: 스크린리더 사용자는 인포그래픽 3장의 내용(설립 배경, 성과, 발전계획)을 전혀 알 수 없고 '3 점 png' 같은 파일명만 듣게 됨. 검색엔진 이미지 색인에도 불리함.
- 고치는 법: Wix 에디터에서 각 이미지 설정 > '이미지에 대한 설명(대체 텍스트)'을 입력하세요. 인포그래픽은 핵심 내용을 요약한 문장(예: '청각재활연구소 소개: 국내 유일 전주기적 청각분야 특화 연구소, 기초·임상·기기·교육·커뮤니티 연구'), 그림1은 '《의사가 알려주는 디지털 치료제》 책 표지', 그림2는 '서영준 연구소장 캐리커처'로 넣으세요. 모바일 64행은 `alt="《의사가 알려주는 디지털 치료제》 책 표지"`로 바꾸세요.
- 검증 메모: 같은 323행의 헤더 로고 alt="청각재활연구소_최종로고(1).png"와 alt="image.png"도 파일명임(masterPage라 모든 페이지에 해당). 함께 적으면 좋음.

### [중간] 한글 전체 글자가 든 Pretendard 폰트(굵기당 약 770KB)를 받아 홈 한 페이지에 폰트만 1.5~2.3MB
- 분류: 성능 · 위치: `embeds/home/html1.home-hero.html:8`, `embeds/home/html2.outcomes.html:8`, `embeds/home/html3.director.html:8`, `embeds/home/mobileHtml1.home.html:7`, `embeds/home/html3.director.html:73`, `embeds/home/html3.director.html:162`
- 영향: 모바일 데이터로 홈에 들어온 방문자는 1.5MB 넘는 폰트를 받아야 하고, 그동안 글자가 대체 폰트로 보였다가 바뀜(font-display: swap). 느린 회선에서는 첫 화면이 늦게 완성됨.
- 고치는 법: 4개 파일의 링크를 `https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard-dynamic-subset.min.css`로 바꾸세요. html3 73행은 600 대신 700(이미 받는 Bold)을 써서 굵기 하나를 줄이세요. 사이트의 다른 페이지 임베드도 같은 링크를 쓰므로 한꺼번에 바꾸면 효과가 큼.

### [낮음] 데스크톱 홈 인포그래픽(3.png)이 2019년 시점 성과 수치와 날짜를 보여 주어 바로 위 Outcomes 및 About 페이지와 어긋남
- 분류: 내용·데이터 · 위치: `(Wix 기본 요소 목록):6`, `(게시된 페이지 HTML):323`, `embeds/home/html2.outcomes.html:103`, `embeds/home/html2.outcomes.html:109`, `embeds/home/html2.outcomes.html:115`, `embeds/about/html2.참조표준데이터센터.html:102`
- 영향: 데스크톱 방문자는 Outcomes 카드 바로 아래에서 기준 시점도 집계 기준도 다른 성과 숫자(논문 243 vs 118, 기술이전 13 vs 12)를 보게 되어 어느 값이 맞는지 알 수 없음. 센터 유치 시점도 About과 두 달 차이가 남.
- 고치는 법: 인포그래픽 3장을 최신 수치로 다시 만들거나, 이미지 아래에 '2019년 기준 자료' 캡션을 다세요. 필요 없으면 이미지를 삭제하세요. 참조표준데이터센터 시작 시점은 한 가지(2019년 1월 또는 3월)로 통일하세요.
- 검증 메모: 근거: 243건·9건(430백만원)은 '사전 준비'(기도점액연구소·iBMW연구원) 칸의 값이므로 9+1+3=13과 12, 243과 118의 비교를 삭제하세요. 제목: '데스크톱 홈 인포그래픽(3.png)이 2019년 기준 연혁·성과 자료인데 기준 시점 표시 없이 현재 Outcomes 바로 아래 노출됨'. 참조표준데이터센터 날짜(1월 운영 vs 3월 유치)는 불일치 가능성만 있으니 '담당자 확인 필요'로 낮추세요. 심각도 low.

### [낮음] 영문 제목·문단에 lang="en"이 없어 스크린리더가 한국어 음성으로 읽음
- 분류: 접근성 · 위치: `embeds/home/html1.home-hero.html:2`, `embeds/home/html1.home-hero.html:59`, `embeds/home/html1.home-hero.html:62`, `embeds/home/html2.outcomes.html:98`, `embeds/home/html3.director.html:166`, `embeds/home/html3.director.html:181`, `embeds/home/mobileHtml1.home.html:2`, `embeds/home/mobileHtml1.home.html:48` 외
- 영향: 스크린리더(VoiceOver, 센스리더, NVDA)는 한국어 음성으로 영문 문단을 읽어 발음이 틀리거나 알아듣기 어려움(WCAG 3.1.2 부분 언어).
- 고치는 법: 영문 요소에 `lang="en"`을 붙이세요. 예: `<p class="hero-sub-en" lang="en">`, `<p class="message-en" lang="en">`, `<h1 class="hero-title" lang="en">`, `<section class="section" id="outcomes" lang="en">`.

### [낮음] 홈 문구 오탈자('청각재활연구소 에', '기전 대한', '게을리 하지', 'patho-physiology' 등)
- 분류: 내용·데이터 · 위치: `embeds/home/html1.home-hero.html:60`, `embeds/home/html1.home-hero.html:61`, `embeds/home/mobileHtml1.home.html:49`, `embeds/home/mobileHtml1.home.html:50`, `embeds/home/html3.director.html:181`, `embeds/home/html3.director.html:184`
- 영향: 홈 첫 화면 환영 문구와 소개 문장에 오탈자가 있어 데스크톱·모바일 모든 방문자에게 공식 연구소 사이트가 덜 다듬어진 인상을 줌.
- 고치는 법: '청각재활연구소에 오신 것을 환영합니다.', '난청의 기전에 대한', '청각재활연구소만의', '게을리하지', 'pathophysiology'로 고치세요. 데스크톱(html1, html3)과 모바일(mobileHtml1)을 같이 고쳐야 함. about/html1.about-intro.html:132와 about/mobileHtml1.about.html:50의 '청각 재활연구소만의'도 같은 문장임.
- 검증 메모: about의 두 줄은 '청각 재활연구소만의' 띄어쓰기만 해당하고 '게을리 하지'는 없음.

### [낮음] 데스크톱 영문 이탤릭이 진짜 이탤릭이 아니라 기울이기만 한 가짜 이탤릭으로 나오고, 모바일과 글꼴 처리도 다름
- 분류: 버그 · 위치: `embeds/home/html1.home-hero.html:12-16`, `embeds/home/html1.home-hero.html:48`, `embeds/home/html3.director.html:9`, `embeds/home/html3.director.html:80`, `embeds/home/html3.director.html:116`, `embeds/home/mobileHtml1.home.html:10-15`, `embeds/home/mobileHtml1.home.html:17`
- 영향: Windows·Mac 데스크톱에서 영문 소개와 영문 인사말이 글자 모양이 어색한 가짜 이탤릭으로 보이고, 같은 문장이 모바일과 다르게 렌더링됨.
- 고치는 법: 이탤릭용 face를 하나 더 선언하세요: `@font-face { font-family:'EngSerif'; src: local('Times New Roman Italic'), local('TimesNewRomanPS-ItalicMT'); font-style: italic; unicode-range: U+0020-007F, U+00A0-00FF, U+0100-024F, U+2000-206F; }`. Playfair 링크는 `family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400`로 바꾸세요. 모바일 17행은 'EngSerif'를 쓰도록 통일하세요.
- 검증 메모: 근거·영향: '모바일은 시스템 폰트를 바로 써서 진짜 이탤릭이 나온다'를 'iOS에서는 진짜 Times 이탤릭이 나오지만 Android에서는 TNR이 없어 Pretendard를 기울여 흉내 낸다'로 고치세요. 모바일 62행 'Digital Therapeutics'(Playfair, font-style:italic)도 같은 가짜 이탤릭임.

### [낮음] 데스크톱 연구소장 소속 목록만 가운데 정렬이라 왼쪽 정렬인 같은 칸의 다른 줄과 어긋남
- 분류: 버그 · 위치: `embeds/home/html3.director.html:95-100`, `embeds/home/html3.director.html:144-146`
- 영향: 데스크톱 방문자에게 이름·직함은 왼쪽, 소속·이메일은 가운데, 인사말은 다시 왼쪽으로 보여 한 칸 안에서 정렬이 오락가락함.
- 고치는 법: 99행 `text-align: center;`를 지우세요(모바일은 144–146행 규칙으로 계속 가운데 정렬됨).
- 검증 메모: '모바일 규칙이 데스크톱으로 새어 나온 것으로 보임'은 추정이므로 빼고, 같은 칸 안의 정렬 불일치라는 사실만 남기세요.

### [낮음] 데스크톱 연구소장 이메일이 클릭되지 않는 일반 텍스트임(Contact 페이지는 mailto 링크)
- 분류: 링크 · 위치: `embeds/home/html3.director.html:174`, `embeds/contact/html1.contact-info.html:162`
- 영향: 홈에서 연구소장에게 연락하려는 방문자는 주소를 직접 복사해야 하고, iframe 안 텍스트라 휴대폰·태블릿에서는 선택하기도 불편함.
- 고치는 법: `<p class="email"><a href="mailto:okas2000@yonsei.ac.kr" style="color:inherit">okas2000@yonsei.ac.kr</a></p>`로 바꾸세요(Contact 페이지와 같은 방식).
- 검증 메모: html3는 데스크톱 전용이라 휴대폰에서는 보이지 않음. 영향 문장에서 '휴대폰'은 빼세요(태블릿은 데스크톱 레이아웃이라 해당됨).

### [낮음] 데스크톱 홈 소개 영상이 자동재생되며 파일 하나가 11.7MB(480p 단일 화질)
- 분류: 성능 · 위치: `(Wix 기본 요소 목록):3`, `(Wix 페이지 데이터):1`
- 영향: 데스크톱 방문자는 홈을 열면 영상이 자동으로 재생되고 끝까지 보면 최대 11.7MB를 받음. 480p 한 가지 화질만 있어 1040px 영역에서는 해상도가 낮음.
- 고치는 법: 자동재생을 끄거나(Wix 영상 설정 > 재생 옵션), 필요하면 음소거 자동재생으로 유지하세요. 원본을 720p 이상으로 다시 올려 Wix가 여러 화질을 만들게 하세요.

#### 검증 단계에서 추가로 발견된 항목 (Home)

검증 에이전트가 따로 보고한 것으로, 2차 검증은 거치지 않았습니다.

- [medium] 모든 페이지에 나오는 헤더 로고 두 개(masterPage)의 대체텍스트가 파일명이고 홈 링크도 없음. 근거: live/home.html:323 `alt="청각재활연구소_최종로고(1).png"`, `alt="image.png"`. masterPage.json dataItem-mmvcntfd `"alt": "청각재활연구소_최종로고(1).png"`, dataItem-mmvctyuh `"alt": "image.png"`이고 두 항목 모두 link 필드가 없음. SSR에서는 `<div id="comp-mmvcntf5" ...><div data-testid="linkElement" class="apPOZK"><img ...`로 <a href> 없이 렌더링됨. 스크린리더는 로고를 파일명으로 읽고, 로고를 눌러도 홈으로 가지 않음.
- [medium] 홈 본문 전체가 클라이언트에서 넣는 교차 출처 iframe(filesusr.com) 안에만 있어 검색엔진이 보는 홈 페이지에 본문과 H1이 거의 없음. 근거: live/home.html에서 `<h1` 0건. <body>에서 script/style를 뺀 텍스트는 288자(메뉴, 'Digital Therapeutics Article ​디지털 치료제에 대한 차세대 한림원 회원의 전문 서적 출판', 저작권)뿐임. 모바일 SSR(live-home-mobile.html)은 메뉴와 저작권 177자뿐이라 구글 모바일 우선 색인 기준으로 홈에 연구소 소개 문장이 하나도 없음. SEO 제목 문제(home-seo-title-template-leftover)와 합쳐 검색 노출에 직접 영향을 줌.
- [low] 데스크톱 DTx 섹션 오른쪽 칸 배경이 Wix 무료 스톡 사진 'VR Goggles'(VR 헤드셋을 쓴 인물)이고, 책 표지(그림1, x=186 w=406) 왼쪽으로 보임. 근거: live/home.html:331 `alt="VR Goggles"`, jemzh.json dataItem-lo5cadwq1 `"title": "VR Goggles", "uri": "11062b_943b58c87b634b808d4e21c87d169803~mv2.jpg", "description": "search/public/vr/..."`(Wix 스톡 검색에서 가져온 이미지). 연구소와 관계없는 인물 사진이 책 소개 옆에 보이므로 의도했는지 확인이 필요함.
- [low] 한글 제목 '연구소장'에 한글 글리프가 없는 Playfair Display를 지정해, 운영체제마다 다른 기본 serif(Windows 바탕, Mac AppleMyungjo 등)로 렌더링됨. 나머지 한글은 Pretendard라 섞여 보임. 근거: html3.director.html:30 `font-family: 'Playfair Display', serif;`(153행 `<h2 class="section-title">연구소장</h2>`), mobileHtml1.home.html:24 `.sec-title{font-family:'Playfair Display',serif;...}`(73행 '연구소장').
- [low] html3.director.html:197–202는 IntersectionObserver로 `.fade`를 관찰하는데 이 파일에는 class="fade" 요소가 없어 쓰이지 않는 코드임(html2의 코드를 복사해 온 흔적).

## About

### [높음] html1(소개)과 html4(Partners)의 내용 높이가 Wix 에디터 높이보다 커서 iframe 안에 스크롤바가 생김
- 분류: Wix iframe · 위치: `embeds/about/html1.about-intro.html:54`, `embeds/about/html1.about-intro.html:86`, `embeds/about/html4.partners.html:25`, `embeds/about/html4.partners.html:65`, `embeds/about/html4.partners.html:69`, `docs/site-map.md:13`, `docs/site-map.md:16`, `(측정 결과):8` 외
- 영향: 데스크톱 방문자 전원에게 해당. 페이지 맨 위 소개 영역(11px 초과)과 Partners 영역(16px 초과)의 iframe에 세로 스크롤바가 생기거나 하단이 잘립니다. Windows처럼 스크롤바가 항상 보이는 환경에서는 첫 화면부터 스크롤바가 눈에 띄고, 마우스 휠이 iframe 안에서 먼저 소모됩니다. 잘리는 부분은 하단 여백이라 글자가 사라지지는 않습니다.
- 고치는 법: 코드에서 하단 여백을 줄여 에디터 높이 안에 맞추는 방법이 가장 간단합니다. html1은 `.section { padding: 60px 24px 44px; }`에 `.intro-text p:last-child { margin-bottom: 0; }`를 더하면 약 742px로 761px 안에 들어갑니다. html4는 `.section { padding: 48px 24px 28px; }`로 바꾸면 약 454px로 458px 안에 들어갑니다. 코드를 그대로 두려면 에디터에서 html1을 773px 이상, html4를 475px 이상으로 늘리고 그 아래 요소들을 같은 만큼 내리세요. 이때 html2의 y를 761로 옮겨 1px 겹침도 없애세요.

### [중간] ILIAS Biologics 로고의 글자가 투명한 흰색 계열 PNG라서 흰 카드 위에서는 글자가 거의 보이지 않음
- 분류: 내용·데이터 · 위치: `embeds/about/html4.partners.html:62`, `embeds/about/html4.partners.html:123`, `embeds/about/mobileHtml1.about.html:33`, `embeds/about/mobileHtml1.about.html:77`
- 영향: 데스크톱과 모바일 방문자 모두 Partners 8개 중 하나를 빨간 점으로만 보게 되어 어느 협력사인지 알아볼 수 없습니다.
- 고치는 법: ILIAS Biologics의 컬러 또는 검정 글자 버전 로고로 교체하세요. 흰 글자 로고를 계속 써야 한다면 해당 카드에만 어두운 배경(예: `style="background:#1a202c"`)을 주세요. 데스크톱 html4:123과 모바일 77행을 모두 바꿔야 합니다.
- 검증 메모: 제목: ILIAS Biologics 로고 PNG에서 글자 채움이 지워져 얇은 회색 윤곽선만 남아 있어 로고가 흐리게 보임. 증거 보정: 글자 내부는 흰색이 아니라 완전 투명(alpha 0)이고, 남은 불투명 픽셀은 빨간 점과 (32~160) 회색 윤곽선뿐임. 배경 제거 과정에서 글자 채움까지 지워진 것으로 보임. 1280px 렌더링에서는 'ILIAS'가 속 빈 윤곽선 글자로 겨우 읽히고 'Biologics'는 흐림. 320px 모바일(117x48)에서는 더 알아보기 어려움. 영향: 데스크톱과 모바일 모두 협력사 로고 하나가 다른 7개와 달리 흐리고 깨진 것처럼 보임. 수정: 글자 채움이 있는 ILIAS Biologics 원본 로고(컬러 또는 검정 글자, 가로 420px 이하)를 받아 html4:123과 mobileHtml1:77의 src를 함께 교체하세요. 카드에 어두운 배경을 주는 방법은 쓰지 마세요. 윤곽선이 어두운 회색이라 오히려 글자가 완전히 사라집니다.

### [중간] 모바일 데이터센터 카드에서 운영 시작일, 데이터 규모, 영문 명칭이 빠지고 alt 텍스트가 축약됨
- 분류: 데스크톱·모바일 불일치 · 위치: `embeds/about/html2.참조표준데이터센터.html:99`, `embeds/about/html2.참조표준데이터센터.html:101`, `embeds/about/html2.참조표준데이터센터.html:102`, `embeds/about/html3.청각빅데이터센터.html:76`, `embeds/about/html3.청각빅데이터센터.html:78`, `embeds/about/html3.청각빅데이터센터.html:79`, `embeds/about/html4.partners.html:113`, `embeds/about/html4.partners.html:123` 외
- 영향: 모바일 방문자는 참조표준데이터센터의 운영 시작 시점(2019년 1월)과 빅데이터센터의 데이터 규모(10만건 이상)를 볼 수 없습니다. 모바일 스크린리더 사용자는 '참조표준 디씨', '빅데이터 디씨'처럼 뜻을 알기 어려운 대체 텍스트를 듣게 됩니다.
- 고치는 법: mobileHtml1 59행 끝에 ' 2019년 1월부터 운영.'을, 65행 끝에 ' 10만건 이상 데이터.'를 추가하세요. 필요하면 각 h3 아래에 영문명 `<p>`도 추가합니다. alt는 데스크톱과 같게 '청각참조표준데이터센터 로고', '청각빅데이터센터 로고', 'NCSRD 국가참조표준센터', 'ILIAS Biologics'로 맞추세요.

### [중간] 데스크톱에 있는 영상 스트립 2개(청각빅데이터센터 홍보영상 포함)가 모바일에서는 전혀 나오지 않음
- 분류: 데스크톱·모바일 불일치 · 위치: `(Wix 페이지 데이터):1`, `embeds/about/html2.참조표준데이터센터.html:107`, `embeds/about/html3.청각빅데이터센터.html:84`, `embeds/about/mobileHtml1.about.html:54`
- 영향: 모바일 방문자는 데스크톱에서 보이는 뉴스 영상과 청각빅데이터센터 홍보영상(3분 35초)을 전혀 볼 수 없습니다.
- 고치는 법: Wix 모바일 에디터에서 영상을 보여 줄 요소를 추가하세요. 예를 들어 모바일 전용 비디오 플레이어를 mobileHtml1과 갤러리 사이에 넣습니다. 또는 영상을 YouTube 등에 올리고 데스크톱과 모바일 임베드 양쪽에 같은 플레이어 iframe을 넣어 한 곳에서 관리하세요.

### [중간] 음성이 있는 3분 35초 홍보영상이 음소거·자동재생·무한반복 배경으로만 들어가 있어 소리, 일시정지, 설명을 제공할 수 없음
- 분류: 접근성 · 위치: `(Wix 페이지 데이터):1`, `embeds/about/html3.청각빅데이터센터.html:84`
- 영향: 데스크톱 방문자는 홍보영상의 음성을 켤 수 없고 재생을 멈출 수도 없습니다. 5초 넘게 자동으로 움직이는 콘텐츠에 정지 수단이 없어 WCAG 2.2.2(일시정지·정지·숨기기)에 위배되고, 스크린리더 사용자에게는 영상이 있다는 사실도 내용도 전달되지 않습니다. 480p 원본이 전체 폭으로 늘어나 흐릿하게 보이고, preload auto 설정으로 방문하자마자 영상 데이터를 받습니다.
- 고치는 법: Column 배경 영상을 컨트롤이 보이는 Wix 비디오 플레이어(또는 YouTube 임베드)로 바꾸세요. 자동재생을 끄거나 최소한 음소거 해제와 일시정지를 할 수 있게 하고, 영상 위나 아래에 제목과 한 줄 설명을 넣으세요. 가능하면 1080p 원본을 다시 올리세요. 24초짜리 배경 영상을 유지한다면 장식용임을 분명히 하고 정지 버튼을 제공하세요.
- 검증 메모: 증거 보정: '전체 폭 docked(2083)'를 '전체 폭 스트립(propItem-mnd00dfs "fullWidth": true)'으로 바꾸세요. 영향에서 'preload auto 설정으로 방문하자마자 영상 데이터를 받습니다'는 확인되지 않았으므로 빼거나 'preload="auto"로 설정되어 있어 재생 시 미리 받을 수 있습니다' 정도로 낮추세요. 나머지(음성이 있는 3분 35초 홍보영상이 음소거·반복 배경으로만 쓰이고, 소리를 켜거나 멈출 수 없으며, 480p라 전체 폭에서 흐림)는 그대로 유효합니다.

### [중간] 상단 소개 문구의 회색 글자(#718096)가 흰 배경에서 명암비 4.02:1로 WCAG AA(4.5:1) 미달
- 분류: 접근성 · 위치: `embeds/about/html1.about-intro.html:33`, `embeds/about/html1.about-intro.html:34`, `embeds/about/html1.about-intro.html:46`, `embeds/about/html1.about-intro.html:47`, `embeds/about/mobileHtml1.about.html:20`, `embeds/about/mobileHtml1.about.html:40`
- 영향: 시력이 약한 방문자나 밝은 야외에서 휴대폰으로 보는 방문자에게 연구소 한 줄 소개('난청에 대한 기초 연구 뿐만 아니라 ... 연세대학교 공식 연구소입니다.')가 흐리게 보입니다. 데스크톱과 모바일 모두 해당합니다.
- 고치는 법: 같은 파일에서 이미 쓰는 #4a5568(7.53:1)로 바꾸세요. 회색 톤을 유지하려면 4.5:1 이상인 더 진한 회색을 쓰면 됩니다. 모바일 40행의 인라인 style은 .hero p 규칙과 중복이므로 지우고 CSS 한 곳에서만 색을 지정하세요.

### [중간] 로고 이미지 10개가 원본 해상도 그대로 쓰여 약 200px 크기로 표시하는 데 1.2MB를 받음
- 분류: 성능 · 위치: `embeds/about/html2.참조표준데이터센터.html:99`, `embeds/about/html3.청각빅데이터센터.html:76`, `embeds/about/html4.partners.html:103`, `embeds/about/html4.partners.html:108`, `embeds/about/html4.partners.html:113`, `embeds/about/html4.partners.html:118`, `embeds/about/html4.partners.html:123`, `embeds/about/html4.partners.html:128` 외
- 영향: About 페이지를 여는 방문자는 작은 로고를 보려고 약 1.2MB의 이미지를 받습니다. 모바일 데이터 환경에서는 Partners 영역이 늦게 뜨고 데이터 사용량이 늘어납니다.
- 고치는 법: 파트너 로고는 가로 420px 이하(2배 화면 기준 205px×2), 데이터센터 로고는 가로 720px 이하로 줄여서 다시 올리세요. 투명이 필요 없는 로고는 JPEG/WebP로 저장하세요. 로고마다 20~40KB 수준이면 전체 200KB 안쪽으로 줄어듭니다. img에 width/height 속성을 넣으면 로딩 중 레이아웃이 흔들리는 것도 막을 수 있습니다.

### [중간] Pretendard 전체 글꼴(굵기당 약 770KB)을 불러와 짧은 소개 페이지에서 글꼴만 약 1.56MB를 받음
- 분류: 성능 · 위치: `embeds/about/html1.about-intro.html:7`, `embeds/about/html1.about-intro.html:8`, `embeds/about/html2.참조표준데이터센터.html:8`, `embeds/about/html3.청각빅데이터센터.html:8`, `embeds/about/html4.partners.html:8`, `embeds/about/mobileHtml1.about.html:7`
- 영향: About 페이지로 처음 들어온 방문자, 특히 모바일 방문자는 한글 몇백 자를 표시하려고 글꼴 1.5MB 이상을 받습니다. font-display:swap이어서 글자는 먼저 대체 글꼴로 보이다가 나중에 바뀌어 화면이 한 번 흔들립니다.
- 고치는 법: 5개 파일의 Pretendard 링크를 `https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard-dynamic-subset.min.css`로 바꾸거나, 최소한 `pretendard-subset.min.css`로 바꾸세요. Google Fonts를 쓰는 파일에는 `<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>`를 추가하세요.
- 검증 메모: 증거 보정: 로드된 글꼴은 html1 'Pretendard 400', html2 'Pretendard 700/400'+'Playfair Display 600', html3 'Pretendard 700/400', 모바일 'Pretendard 700/400'+'Playfair Display 600/700'이고, html4는 Pretendard 파일을 받지 않습니다. 합계 약 1.56MB(Regular+Bold)는 그대로입니다.

### [낮음] 한글 제목 '청각재활연구소'의 글꼴 목록에 Pretendard가 없어 방문자 OS 기본 명조체로 표시됨
- 분류: 버그 · 위치: `embeds/about/html1.about-intro.html:11`, `embeds/about/html1.about-intro.html:59`, `embeds/about/html1.about-intro.html:125`, `embeds/about/mobileHtml1.about.html:23`, `embeds/about/mobileHtml1.about.html:46`
- 영향: 같은 제목이 Windows에서는 바탕, macOS에서는 AppleMyungjo, Android에서는 Noto Serif CJK처럼 기기마다 다른 글꼴로 보여 페이지의 나머지 Pretendard 글꼴과 어긋납니다.
- 고치는 법: html1:59와 모바일 23행을 `font-family: 'Playfair Display', Pretendard, serif;`로 바꾸세요. 그러면 영문은 Playfair, 한글은 Pretendard로 표시되어 주석의 의도와 같아집니다.

### [낮음] word-break: keep-all이 없어 한글 단어가 중간에서 줄바꿈됨 ('연 / 세대학교', '운 / 영.')
- 분류: 접근성 · 위치: `embeds/about/html1.about-intro.html:18`, `embeds/about/html1.about-intro.html:119`, `embeds/about/html2.참조표준데이터센터.html:102`, `embeds/about/mobileHtml1.about.html:17`, `embeds/about/mobileHtml1.about.html:42`, `embeds/about/mobileHtml1.about.html:65`
- 영향: 대부분의 방문자에게 기관명 '연세대학교'가 '연 / 세대학교'로 갈라지는 등 단어가 쪼개져 읽기 어렵습니다. 특히 폭이 좁은 모바일에서 여러 곳에 발생합니다.
- 고치는 법: 각 파일의 body 규칙에 `word-break: keep-all; overflow-wrap: break-word;`를 추가하세요.

### [낮음] 소개 문구의 띄어쓰기 오류와 기관명 표기 불일치('청각 재활연구소', '연구 뿐만', '수집 생산')
- 분류: 내용·데이터 · 위치: `embeds/about/html1.about-intro.html:119`, `embeds/about/html1.about-intro.html:131`, `embeds/about/html1.about-intro.html:132`, `embeds/about/html2.참조표준데이터센터.html:102`, `embeds/about/mobileHtml1.about.html:42`, `embeds/about/mobileHtml1.about.html:49`, `embeds/about/mobileHtml1.about.html:50`, `embeds/about/mobileHtml1.about.html:59`
- 영향: About 페이지를 읽는 모든 방문자에게 기관 소개 첫 문장부터 맞춤법 오류가 보이고, 연구소 공식 명칭이 한 페이지 안에서 두 가지로 표기됩니다.
- 고치는 법: 데스크톱과 모바일 모두에서 '기초 연구뿐만 아니라', '청각재활연구소만의', '수집·생산하고'로 고치세요. 원하면 '어깨를 나란히 할 수 있는' 또는 '견줄 수 있는'으로 다듬으세요. home/html3.director.html:184의 같은 문장도 함께 고치세요.
- 검증 메모: 수정 범위 보완: '수집·생산'으로 통일하려면 about 두 파일 외에 hearing-lab/html1.hearing-lab.html:586과 hearing-lab/mobileHtml1.hearing-lab-mobile.html:90도 함께 고치세요. '어깨를 나란히 견줄'을 다듬는다면 home/html3.director.html:178도 같이 고쳐야 합니다(184행 '청각 재활연구소만의'는 이미 fix에 있음).

### [낮음] 1인칭 인용문에 화자 표시가 없고, 소개 문단이 홈 인사말을 그대로 복사한 4벌로 관리됨
- 분류: 내용·데이터 · 위치: `embeds/about/html1.about-intro.html:127`, `embeds/about/html1.about-intro.html:128`, `embeds/about/html1.about-intro.html:129`, `embeds/about/html1.about-intro.html:131`, `embeds/about/html1.about-intro.html:132`, `embeds/about/mobileHtml1.about.html:48`, `embeds/about/mobileHtml1.about.html:49`, `embeds/about/mobileHtml1.about.html:50` 외
- 영향: About 페이지만 보는 방문자는 '임상의이자 연구자로서 걸어왔습니다'라는 1인칭 문장을 누가 말했는지 알 수 없습니다. 같은 문장이 홈 데스크톱, About 데스크톱, About 모바일에 따로 들어 있어(홈 모바일 포함 시 더 많음) 한 곳만 고치면 페이지마다 문구가 달라집니다.
- 고치는 법: 인용문 아래에 `<cite>— 서영준 연구소장</cite>`처럼 화자를 표시하세요(모바일도 동일). 문장을 고칠 때 home/html3.director.html과 about 두 파일을 함께 고쳐야 한다는 점을 README에 적어 두거나, 인용문 대신 연구소 관점의 3인칭 문장으로 바꾸세요.

### [낮음] 모바일의 쓰이지 않는 @font-face, html3의 불필요한 Playfair 로드, 실제 구조와 맞지 않는 편집 안내 주석
- 분류: 유지보수 · 위치: `embeds/about/mobileHtml1.about.html:11`, `embeds/about/mobileHtml1.about.html:17`, `embeds/about/html3.청각빅데이터센터.html:9`, `embeds/about/html2.참조표준데이터센터.html:107`, `embeds/about/html3.청각빅데이터센터.html:84`
- 영향: 방문자에게 보이는 문제는 아닙니다. 하지만 데스크톱과 모바일의 글꼴 지정 방식이 달라 나중에 한쪽만 고치기 쉽고, html3는 쓰지 않는 CSS를 매번 요청하며, 주석이 편집자에게 잘못된 작업 위치를 알려 줍니다.
- 고치는 법: 모바일 17행을 `font-family:'EngSerif',Pretendard,sans-serif`로 바꿔 데스크톱과 맞추세요(또는 11-15행 삭제). html3:7-9의 Google Fonts 링크를 지우세요. html2:107과 html3:84 주석은 '영상은 이 iframe 아래의 별도 스트립(Column 배경)에 있음'으로 고치거나 삭제하세요.
- 검증 메모: 주석 부분은 빼세요. html2:107과 html3:84 주석은 'Wix 에디터에서 이 요소 아래에 영상을 넣으라'는 뜻이고, 실제로 바로 아래에 영상 스트립(comp-mmvc6jbi, comp-mnd00cz7)이 있어 구조와 맞습니다. 수정 보정: html3에서는 9행의 Playfair Display 링크(쓸 곳이 없으면 7행 preconnect도)만 지우고, 8행 Pretendard 링크는 반드시 남기세요. 모바일 17행은 `font-family:'EngSerif',Pretendard,sans-serif`로 바꿔 데스크톱과 맞추세요.

## Research

### [높음] 데스크톱 특허 아코디언이 max-height 5000px에 잘려 80건 중 22건이 보이지 않음 (모바일은 80건 모두 표시)
- 분류: 버그 · 위치: `embeds/research/html1.research.html:182`, `embeds/research/html1.research.html:2404`, `embeds/research/html1.research.html:2865-3048`, `embeds/research/mobileHtml1.research.html:57`
- 영향: 데스크톱 방문자는 헤더에 '80건'이라고 적힌 특허 목록을 열어도 마지막 22건(등록 특허 다수 포함, 유럽·미국 등록 특허 포함)을 볼 방법이 없습니다. 스크롤바나 '더 있음' 표시도 없이 항목 중간이 잘려 보입니다. 같은 목록이 모바일에서는 전부 보여 기기별로 내용이 다릅니다.
- 고치는 법: L182를 `max-height` 고정값 대신 JS로 열 때 `body.style.maxHeight = body.scrollHeight + 'px'`(닫을 때 0)로 설정하거나, 애니메이션이 필요 없으면 `.collapse-body{display:none}` / `.collapse-body.open{display:block}`로 바꾸세요. 모바일(L57, 8000px, 현재 여유 1,834px)도 특허가 약 23건 더 늘면 같은 문제가 생기므로 같은 방식으로 함께 고치세요.

### [높음] 고정 높이 iframe 안에서 더보기·특허 목록을 펼치면 내용이 iframe 바닥 아래로 사라짐 (특허 아코디언은 iframe의 맨 아래 경계에서 열림)
- 분류: Wix iframe · 위치: `docs/site-map.md:18`, `docs/site-map.md:19`, `embeds/research/html1.research.html:1583`, `embeds/research/html1.research.html:2380`, `embeds/research/html1.research.html:2403`, `embeds/research/mobileHtml1.research.html:1173`, `embeds/research/mobileHtml1.research.html:1935`, `embeds/research/mobileHtml1.research.html:1941`
- 영향: 방문자가 '특허 목록 (80건)'을 클릭하면 화살표만 뒤집히고 목록은 iframe 바닥 아래에서 열려 아무것도 바뀌지 않은 것처럼 보입니다. 'Publication 더보기'(115건)나 'Report 더보기'(89건)를 누르면 1만 px 이상의 내용이 3843px(모바일 3651px) 창 안에 갇혀, 페이지 스크롤과 iframe 내부 스크롤이 겹칩니다. 특히 모바일 터치에서는 스크롤이 매우 헷갈리고, Report·Patents 섹션까지 가기 어렵습니다.
- 고치는 법: (1) 목록을 iframe 안에 두려면 목록 자체를 스크롤 박스로 만드세요(예: `#pub-list,#report-list,.collapse-inner{max-height:600px;overflow-y:auto}`). 그러면 iframe 높이가 변하지 않습니다. 또는 '더보기'를 한 번에 전부가 아닌 10~20건씩 늘리고, 그 상태에서도 높이가 맞도록 에디터 높이를 조정하세요. (2) 특허처럼 맨 아래에 있는 아코디언은 연 직후 `document.getElementById('patent-body').scrollIntoView()`를 호출하거나, 특허 섹션을 별도 페이지나 Wix 네이티브 요소로 옮기세요. (3) 데스크톱 에디터 높이를 실제 초기 높이(약 3900px)에 맞게 약간 늘리세요.

### [중간] 모바일에는 Publication·Report 연도 필터가 없음 (데스크톱에는 연도 버튼 7개씩 있음)
- 분류: 데스크톱·모바일 불일치 · 위치: `embeds/research/html1.research.html:478-489`, `embeds/research/html1.research.html:1606-1618`, `embeds/research/mobileHtml1.research.html:81-88`, `embeds/research/mobileHtml1.research.html:1177-1180`, `embeds/research/mobileHtml1.research.html:2593-2606`
- 영향: 모바일 방문자는 94건의 학회 발표나 120건의 논문에서 특정 연도(예: 2025년)를 찾으려면 '더보기'로 전부 펼친 뒤 1만 px 넘게 스크롤해야 합니다. 같은 페이지인데 데스크톱에서 되는 기능이 모바일에서는 되지 않습니다.
- 고치는 법: 모바일에도 연도 필터 행을 추가하세요(가로 스크롤 한 줄 또는 `<select>`). 데스크톱 applyFilter처럼 팀+연도를 함께 적용하도록 모바일 스크립트를 고치세요. Report에는 연도 필터만 넣으면 됩니다.

### [중간] 특허 아코디언이 클릭 핸들러만 있는 div여서 키보드로 열 수 없고 펼침 상태도 알려지지 않음
- 분류: 접근성 · 위치: `embeds/research/html1.research.html:2403-2407`, `embeds/research/html1.research.html:177-182`, `embeds/research/html1.research.html:470-487`, `embeds/research/mobileHtml1.research.html:1941-1945`, `embeds/research/mobileHtml1.research.html:56-57`, `embeds/research/mobileHtml1.research.html:83-87`
- 영향: 키보드만 쓰는 방문자는 Tab으로 특허 헤더에 갈 수 없어 목록을 열지 못합니다. 스크린리더 사용자는 열림/닫힘 상태를 알 수 없고, 어떤 팀·연도 필터가 켜져 있는지도 들을 수 없습니다.
- 고치는 법: 헤더를 `<button type="button" class="collapse-header" aria-expanded="false" aria-controls="patent-body">`로 바꾸고, 토글할 때 aria-expanded를 갱신하세요. 닫힌 body에는 `hidden` 속성이나 `visibility:hidden`을 함께 주세요. 필터 버튼에는 `aria-pressed="true/false"`를 설정하세요.

### [중간] 저자·팀 태그·학회 태그·선택된 필터 버튼의 작은 글씨가 WCAG AA 대비 4.5:1에 미달
- 분류: 접근성 · 위치: `embeds/research/html1.research.html:34`, `embeds/research/html1.research.html:277-281`, `embeds/research/html1.research.html:288-291`, `embeds/research/html1.research.html:302-327`, `embeds/research/html1.research.html:232-247`, `embeds/research/mobileHtml1.research.html:32-37`, `embeds/research/mobileHtml1.research.html:41`, `embeds/research/mobileHtml1.research.html:43` 외
- 영향: 저시력 사용자나 햇빛 아래 모바일 사용자는 모든 논문·발표의 저자 줄과 팀 태그(특히 Hearing Lab 2.78:1)를 읽기 어렵습니다. 모바일은 10.4px 글씨라 더 심합니다.
- 고치는 법: --text-light를 #5a6578 이하(대비 5.9:1 이상)로 어둡게 하세요. 팀 태그 글자색은 배경 대비 4.5:1이 되도록 어둡게 조정하세요(예: hearing #4A6F8E, head #2F6E9E, collab #6E4E9A, basic #23704A). 선택된 버튼 배경도 같은 어두운 색을 쓰세요. 모바일 태그는 최소 12px 이상을 권장합니다.

### [중간] 저자 목록 36건과 학회명 11건이 원본에서 '...'로 잘린 채 게시됨 (일부는 날짜까지 잘림)
- 분류: 내용·데이터 · 위치: `embeds/research/html1.research.html:518`, `embeds/research/html1.research.html:1773`, `embeds/research/html1.research.html:1805`, `embeds/research/html1.research.html:1821`, `embeds/research/html1.research.html:2061`, `embeds/research/html1.research.html:2093`, `embeds/research/html1.research.html:2189`, `embeds/research/html1.research.html:2197` 외
- 영향: 방문자는 공동저자 전체, 학회 정식 명칭, 발표 날짜(L2189 '201...', L2197 날짜 없음)를 알 수 없습니다. 연구 실적 페이지에서 정보가 빠지고 작성이 덜 된 것처럼 보입니다.
- 고치는 법: 원본 데이터(연구자 DB 내보내기)에서 전체 저자와 학회명을 다시 가져와 '...' 부분을 채우세요. 저자가 너무 많으면 'et al.'로 명시적으로 줄이세요. 데스크톱과 모바일 파일을 모두 고쳐야 합니다.

### [중간] 논문·발표 제목과 학회명에 오타가 여러 개 있음 (예: '서비스 모텔', 'Technolohy', '2023재75차')
- 분류: 내용·데이터 · 위치: `embeds/research/html1.research.html:1525`, `embeds/research/html1.research.html:1689`, `embeds/research/html1.research.html:1693`, `embeds/research/html1.research.html:1773`, `embeds/research/html1.research.html:1930`, `embeds/research/html1.research.html:1969`, `embeds/research/html1.research.html:1985`, `embeds/research/html1.research.html:2029` 외
- 영향: 연구소의 공식 실적 목록에 오타가 보여 신뢰도가 떨어집니다. 특히 '서비스 모텔'은 뜻이 완전히 달라집니다. 제목으로 검색하는 방문자는 해당 발표를 찾지 못할 수 있습니다.
- 고치는 법: 위 오타를 데스크톱과 모바일 두 파일에서 모두 고치세요. 데이터를 옮길 때 맞춤법 검사를 한 번 거치세요.
- 검증 메모: The mobile line for the 'Implant’s' typo (L1773) is M1330, which is missing from the location list.

### [낮음] 특허 목록에 완전히 같은 항목 7쌍이 있고, 번호나 날짜가 없어 구별할 수 없음. '80건' 숫자도 하드코딩됨
- 분류: 내용·데이터 · 위치: `embeds/research/html1.research.html:2404`, `embeds/research/html1.research.html:2457`, `embeds/research/html1.research.html:2537`, `embeds/research/html1.research.html:2465`, `embeds/research/html1.research.html:2529`, `embeds/research/html1.research.html:2513`, `embeds/research/html1.research.html:2609`, `embeds/research/html1.research.html:2617` 외
- 영향: 방문자에게는 같은 특허가 두 번씩 나열된 것처럼 보입니다. 실제로 서로 다른 출원(분할·PCT 등)이라도 번호나 날짜가 없어 확인할 수 없고, '80건'이라는 실적이 부풀려졌다는 인상을 줄 수 있습니다. 항목을 추가하거나 삭제해도 헤더 숫자는 자동으로 바뀌지 않습니다.
- 고치는 법: 특허마다 출원/등록 번호와 연도를 템플릿대로 넣으세요(`10-XXXXXXX`, `등록 2024`). 정말 중복인 항목은 지우세요. 헤더 숫자는 `document.querySelectorAll('#patent-body .pub-item').length`로 계산해 채우세요(데스크톱·모바일 모두).
- 검증 메모: Exact-match counts are 74 distinct items by title+tags and 53 distinct titles. The auditor's 73/52 only holds after removing whitespace ('제조방법' vs '제조 방법'). The header '80건' matches the actual 80 items today; the risk is only that it will drift when items are added or removed.

### [낮음] 서브셋이 없는 Pretendard 정적 폰트를 굵기별로 통째로 받아 페이지당 약 2.3~3.1MB 폰트 다운로드
- 분류: 성능 · 위치: `embeds/research/html1.research.html:10`, `embeds/research/mobileHtml1.research.html:7`
- 영향: 모바일 데이터 환경에서 이미지 4장(약 0.64MB)보다 훨씬 큰 폰트 3MB 안팎을 받느라 첫 로딩이 느리고 데이터를 많이 씁니다. font-display:swap이라 글꼴이 바뀌는 순간 줄바꿈이 달라져 높이도 흔들립니다.
- 고치는 법: `pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css`(또는 static/pretendard-dynamic-subset.min.css)로 바꾸면, 쓰인 글자 범위의 조각 파일만 받습니다. 사이트 전체 embed에 같은 링크가 있다면 한 번에 바꾸세요.
- 검증 메모: '페이지당 약 2.3~3.1MB' is inaccurate. Because of the browser cache, the download happens once on the first visit to the site (about 2.33MB with Times New Roman installed, 3.12MB without it, e.g. on Android); later pages reuse the cache. Text shows immediately in a fallback font because of font-display:swap, so the cost is data usage plus a reflow when the font swaps.

### [낮음] 저자 표기에 데이터 변환 흔적이 남음 (끝에 붙은 쉼표 71건, 빈 저자 칸, 붙어버린 이름, 소속 첨자 문자)
- 분류: 내용·데이터 · 위치: `embeds/research/html1.research.html:1175`, `embeds/research/html1.research.html:1355`, `embeds/research/html1.research.html:968`, `embeds/research/html1.research.html:1004`, `embeds/research/html1.research.html:1022`, `embeds/research/html1.research.html:1283`, `embeds/research/html1.research.html:1634`, `embeds/research/html1.research.html:1738` 외
- 영향: 저자 이름이 깨져 보이고(예: 'Sagonga'), 공저자 검색·인용할 때 혼란을 줍니다.
- 고치는 법: 끝의 쉼표와 빈 칸을 지우고, 붙은 이름은 'SUNMOK HA', 'JINSIL CHOI', 'YOON AH PARK', 'JAEHYUN HAN'처럼 띄어 쓰세요. 첨자 '1/a'를 지우고 한 사람의 영문 표기를 하나로 통일하세요(두 파일 모두).

### [낮음] Report 9건은 발표 제목 자리에 학회 이름이 들어가 무엇을 발표했는지 알 수 없음
- 분류: 내용·데이터 · 위치: `embeds/research/html1.research.html:1689`, `embeds/research/html1.research.html:1761`, `embeds/research/html1.research.html:1777`, `embeds/research/html1.research.html:1817`, `embeds/research/html1.research.html:1825`, `embeds/research/html1.research.html:1833`, `embeds/research/html1.research.html:1841`, `embeds/research/html1.research.html:1865` 외
- 영향: 방문자에게 같은 학회명이 두 번 보이고, 발표 주제는 전혀 보이지 않습니다.
- 고치는 법: 각 항목의 실제 발표(강연) 제목을 넣거나, 제목을 알 수 없으면 '초청 강연' 같은 표시로 바꾸세요.

### [낮음] 날짜·저널명 표기가 섞여 있고, Report의 같은 해 안에서 순서가 뒤섞임
- 분류: 내용·데이터 · 위치: `embeds/research/html1.research.html:1629`, `embeds/research/html1.research.html:1637`, `embeds/research/html1.research.html:2077`, `embeds/research/html1.research.html:642`, `embeds/research/html1.research.html:651`, `embeds/research/html1.research.html:660`, `embeds/research/html1.research.html:849`, `embeds/research/html1.research.html:497` 외
- 영향: 목록이 정리되지 않은 것처럼 보이고, 기본으로 보이는 5건이 그 해의 최신 발표가 아닐 수 있습니다.
- 고치는 법: 날짜는 `YYYY.MM(.DD)`로, 저널명은 공식 표기 하나로 통일하세요. Report 목록은 같은 해 안에서도 날짜 내림차순으로 정렬하세요. L2077의 개최지를 확인해 고치세요(온라인 발표였다면 '온라인'으로).
- 검증 메모: The journal-variant line numbers point to the pub-item opening tags, not the journal tags. The actual tag lines are L503 'Hearing Research', L549 'HEARING RESEARCH', L648/L711/L720 'Journal of Audiology and Otology', L657 'PloS one', L666 'PLoS ONE', and L855/L918/L1296 'PLOS ONE'. There are 9 English variant groups plus a Korean one ('대한이비인후-두경부외과학회지' ×2 vs '대한이비인후과학회지 두경부외과학' ×5), 10 in total.

### [낮음] 특허 10건에 빈 국가 태그가 회색 알약 모양으로 표시되고, 상태 태그의 클래스가 제각각임
- 분류: 버그 · 위치: `embeds/research/html1.research.html:2485`, `embeds/research/html1.research.html:2509`, `embeds/research/html1.research.html:2525`, `embeds/research/html1.research.html:2685`, `embeds/research/html1.research.html:2693`, `embeds/research/html1.research.html:2701`, `embeds/research/html1.research.html:2789`, `embeds/research/html1.research.html:2877` 외
- 영향: 방문자에게는 10개 특허 옆에 의미 없는 빈 회색 박스가 보이고, 해당 특허의 국가 정보가 빠져 있습니다. 출원과 등록이 서로 다른 스타일(저널용·연도용)을 빌려 써서 유지보수 때 혼동을 줍니다.
- 고치는 법: 빈 국가 태그는 실제 국가를 채우거나 span을 지우세요. CSS에 `.pub-tag:empty{display:none}`를 추가해 두면 안전합니다. 상태/국가 태그 전용 클래스(`.pub-tag.status-filed`, `.status-granted`, `.country`)를 만들고, 모든 항목에 있는 '특허' 태그는 빼세요.

### [낮음] 데스크톱 필터 함수가 비표준 전역 변수 window.event에 의존함
- 분류: 유지보수 · 위치: `embeds/research/html1.research.html:470-487`, `embeds/research/html1.research.html:1610-1616`, `embeds/research/html1.research.html:3073-3086`
- 영향: 현재 주요 브라우저에서는 동작합니다(테스트한 팀×연도 35개 조합 모두 건수와 표시가 정상). 다만 window.event는 폐지 예정(legacy) API라, 함수를 다른 곳에서 호출하거나 addEventListener로 바꾸면 곧바로 ReferenceError나 잘못된 버튼이 선택됩니다.
- 고치는 법: `onclick="filterPub(this)"`처럼 버튼을 인자로 넘기고, 함수에서 `btn.closest('.filter-btns').id`로 팀/연도를 구분하세요.
- 검증 메모: The impact is overstated. Switching to addEventListener would not break it: browsers still set window.event during listener dispatch. It breaks only when the function is called programmatically outside a click, e.g. from DOMContentLoaded. There, event.target is document, which has no closest(), or event is undefined, so the error is a TypeError, not a ReferenceError.

### [낮음] 모바일에서 소개 문구와 협업 제안 문장이 빠지고 프로젝트 설명 내용이 달라짐
- 분류: 데스크톱·모바일 불일치 · 위치: `embeds/research/html1.research.html:385`, `embeds/research/html1.research.html:396`, `embeds/research/html1.research.html:408`, `embeds/research/html1.research.html:419`, `embeds/research/html1.research.html:430`, `embeds/research/html1.research.html:441`, `embeds/research/mobileHtml1.research.html:63-66`, `embeds/research/mobileHtml1.research.html:71-75`
- 영향: 모바일 방문자는 연구소의 협업 제안 문장과 대표 성과(환기관, 골전도 보청기 임상시험, '대한민국 유일' 지정)를 보지 못합니다.
- 고치는 법: 모바일 설명을 줄이더라도 핵심 사실(대표 기기, 임상시험 대상, 협업 제안)은 남기세요. 데스크톱 문구를 고칠 때 모바일도 함께 고치도록 체크리스트를 만드세요.

### [낮음] 프로젝트 이미지 4장이 표시 크기보다 2~5배 큰 원본 그대로 로드됨
- 분류: 성능 · 위치: `embeds/research/html1.research.html:404`, `embeds/research/html1.research.html:415`, `embeds/research/html1.research.html:426`, `embeds/research/html1.research.html:437`, `embeds/research/mobileHtml1.research.html:72-75`
- 영향: 모바일에서 286px로 보이는 이미지에 가로 1,000~1,389px 원본(약 0.64MB)을 받습니다. 2배 밀도 화면 기준으로도 필요한 크기의 약 2~2.4배입니다. 크기 속성이 없어 로딩 중에 레이아웃이 밀립니다.
- 고치는 법: 이미지를 가로 약 900px(데스크톱 2x)/600px(모바일 2x)로 줄이고 WebP로 다시 올리세요(Imgur 썸네일 접미사 'l' 사용, 예: JbUTgTel.jpeg 등). `<img loading="lazy" width="..." height="...">`를 추가하세요.
- 검증 메모: The Imgur 'l' suffix gives a 640px-wide thumbnail. That suits mobile 2x (about 572px) but is below desktop 2x (about 904px); desktop needs 'h' (1024px). These images are near the top of the page, so loading="lazy" gains little; width/height are the more important fix.

### [낮음] 논문 120·발표 94·특허 80건 데이터가 데스크톱과 모바일 파일에 따로 복사돼 있어 수정할 때마다 두 번 고쳐야 함
- 분류: 유지보수 · 위치: `embeds/research/html1.research.html:495-1580`, `embeds/research/mobileHtml1.research.html:90-1172`, `embeds/research/html1.research.html:182`, `embeds/research/mobileHtml1.research.html:57`
- 영향: 새 논문을 한쪽 파일에만 넣으면 데스크톱과 모바일 방문자가 서로 다른 실적을 보게 됩니다. 이미 CSS 차이 때문에 기기별 표시 내용이 달라져 있습니다.
- 고치는 법: 항목 데이터를 JSON 배열 하나로 옮기고, 두 embed가 같은 데이터에서 목록을 그리게 하세요(Wix CMS 컬렉션 + 네이티브 리피터로 옮기는 것도 방법). 당장은 수정할 때마다 두 파일을 비교하는 스크립트(parse→diff)를 돌리세요.

#### 검증 단계에서 추가로 발견된 항목 (Research)

검증 에이전트가 따로 보고한 것으로, 2차 검증은 거치지 않았습니다.

- [medium, accessibility] 페이지 언어가 한국어로만 지정되어 영문 제목이 한국어 음성으로 읽힘. embeds/research/html1.research.html:2 and embeds/research/mobileHtml1.research.html:2 both declare `<html lang="ko">`. 169 of the 294 list titles are English-only (e.g. html1 L1525 'Neutrophil-to-Lymphocyte Ratio and Platelet-to-Lymphocyte Ratio: ...', L2329 'Comparison of clinical features and prognosis ...'), and no element anywhere in either file has lang="en". This fails WCAG 3.1.2 (Language of Parts, AA). Screen readers such as VoiceOver or NVDA read the English titles, authors and journal names with Korean pronunciation rules. Fix: add lang="en" to #pub-list/#report-list, or to each English .pub-title/.pub-authors, in both files.

## People

### [높음] 구성원 사진 31장을 원본 크기(최대 1610×2000px, 1MB)로 불러와 90~110px(모바일 65~75px) 원형 사진 하나 보여주려고 7.3MB를 다운로드함
- 분류: 성능 · 위치: `embeds/people/html1.people.html:80`, `embeds/people/html1.people.html:81`, `embeds/people/html1.people.html:125-324`, `embeds/people/mobileHtml1.people.html:30`, `embeds/people/mobileHtml1.people.html:36`, `embeds/people/mobileHtml1.people.html:63-138`
- 영향: 모든 방문자가 People 페이지를 열 때마다 사진 7.3MB를 한꺼번에 받는다. 특히 모바일(데이터 요금·느린 망) 방문자는 65px짜리 동그라미 사진 때문에 로딩이 매우 느리고 사진이 늦게 하나씩 뜬다. 실제 필요한 용량의 약 17배다.
- 고치는 법: 각 img URL을 imgur 축소본으로 바꾼다: `https://i.imgur.com/F9YowOS.jpeg` → `https://i.imgur.com/F9YowOSm.jpeg`(최대 320px, 레티나 110px×2 대응 충분). 31장 모두 적용하면 7.3MB → 약 0.45MB(−94%). 추가로 모든 `<img>`에 `loading="lazy" decoding="async" width="90" height="90"`을 넣는다. 데스크톱·모바일 두 파일 모두 수정.
- 검증 메모: 제목의 '최대 1610×2000px'는 '최대 1621×2000px(2Q56Mj7), 최대 1,040,340 B(F9YowOS)'로 바로잡아야 함. impact의 '열 때마다'도 틀림. imgur가 `cache-control: public, max-age=31536000`을 보내므로 '처음 방문할 때(캐시가 비어 있을 때) 사진 7.3MB를 한꺼번에 받는다'로 고쳐야 함. fix의 `alt`/크기 관련 제안은 그대로 유효함. `width="90" height="90"` 속성은 CSS가 덮어쓰므로 교수·모바일 사진 크기에는 영향이 없음.

### [중간] iframe 에디터 높이와 실제 내용 높이 불일치: 데스크톱은 17px 넘쳐 내부 스크롤바 발생, 모바일은 하단 68px 빈 공간
- 분류: Wix iframe · 위치: `docs/site-map.md:20`, `docs/site-map.md:21`, `embeds/people/html1.people.html:66`, `embeds/people/mobileHtml1.people.html:23`
- 영향: 데스크톱: 내용이 iframe보다 17px 길어서 iframe 안에 3454px 높이의 세로 스크롤바가 생기고(Windows 브라우저에서 항상 보임), 마우스 휠이 iframe 안쪽 17px을 먼저 스크롤한다. 모바일: 마지막 Audiso 카드 아래와 푸터 사이에 약 68px의 빈 흰 공간이 생긴다.
- 고치는 법: Wix 에디터에서 데스크톱 #html1 높이를 3454 → 3475 이상(여유를 두어 3480)으로 늘리거나, html1:66의 마지막 섹션 하단 padding을 40px → 20px로 줄인다. 모바일 #mobileHtml1은 3668 → 약 3605로 줄인다. 단, 아래 '데스크톱/모바일 내용 차이' 항목을 반영해 모바일에 내용을 추가하면 높이가 늘어나므로 수정 후 다시 측정해 맞춘다.
- 검증 메모: fix 중 'html1:66의 마지막 섹션 하단 padding을 40px → 20px로 줄인다'는 틀림. html1:66 `.team-section { padding: 56px 24px 40px; ...}`은 섹션 6개 모두에 적용되므로 이 줄을 고치면 전체 높이가 약 120px 줄어들고, 이번에는 아래에 약 100px 빈 공간이 생김. `#audiso { padding-bottom: 20px; }`처럼 마지막 섹션에만 규칙을 따로 추가해야 함. 참고로 잘리는 것은 하단 여백뿐이고 내용은 잘리지 않음.

### [중간] 모바일 버전에 교수진 소속 학과·연구원 전체 이름·소개 문구가 빠져 데스크톱과 내용이 다름
- 분류: 데스크톱·모바일 불일치 · 위치: `embeds/people/html1.people.html:106`, `embeds/people/html1.people.html:128`, `embeds/people/html1.people.html:134`, `embeds/people/html1.people.html:140`, `embeds/people/html1.people.html:157-158`, `embeds/people/mobileHtml1.people.html:43-46`, `embeds/people/mobileHtml1.people.html:63-65`, `embeds/people/mobileHtml1.people.html:76`
- 영향: 모바일 방문자에게는 교수 3명의 소속 학과(이비인후과/생체공학과)가 보이지 않고, Post-doc 연구원의 이름이 성 없이 'Temuulen'으로만 표시된다. 연구소 소개 문구도 모바일에는 없다. 구성원 변동 시 두 파일을 따로 고쳐야 해 이런 불일치가 계속 생길 수 있다.
- 고치는 법: mobileHtml1의 교수 카드 3개에 `<p class="role">이비인후과</p>` / `생체공학과` / `이비인후과` 줄을 추가하고, 76행을 `<h4>Temuulen Batsaikhan</h4>`(alt도 동일)로 바꾸고, hero에 소개 문구 `<p>연세대학교 원주세브란스기독병원 청각재활연구소(RIHE) 구성원을 소개합니다.</p>`를 추가한다. 추가 후 모바일 높이가 늘어나므로(현재 여유 68px) 다시 측정해 #mobileHtml1 높이를 맞춘다. 장기적으로는 구성원 목록을 한 곳(JS 배열 등)에 두고 두 파일이 같은 데이터로 카드를 그리게 한다.

### [중간] 작은 글씨의 색 대비가 WCAG AA 기준(4.5:1) 미달: 회색 보조 텍스트 4.02:1, 부서 배지 3.04:1, 탭 hover 2.38~4.31:1
- 분류: 접근성 · 위치: `embeds/people/html1.people.html:29`, `embeds/people/html1.people.html:45`, `embeds/people/html1.people.html:47`, `embeds/people/html1.people.html:69`, `embeds/people/html1.people.html:84-87`, `embeds/people/html1.people.html:128`, `embeds/people/html1.people.html:134`, `embeds/people/html1.people.html:140` 외
- 영향: 저시력·고령 방문자나 햇빛 아래 모바일 화면에서 교수 소속 학과, 팀 영문명, 모바일의 직위(박사과정/연구원 등), Audiso 부서 배지(개발/영업/인증…)를 읽기 어렵다. 모두 12px 안팎의 작은 글씨라 AA 기준 4.5:1이 필요하다.
- 고치는 법: `--text-light`와 모바일 `#718096`을 `#5a6578`(약 5.9:1) 이상 진하게 바꾼다. 부서 배지 글자색 `#B8880E` → `#8a6508`(#FFF9E6 대비 약 5:1 이상)로 바꾼다. 탭 hover는 흰 글자 대신 진한 글자(#1a202c)를 쓰거나, 배경색을 더 진한 톤(예: audiso #8a6a0a, hearing #4a6f8f, head #2f6f9f)으로 바꿔 4.5:1 이상을 맞춘다. 두 파일 모두 적용.
- 검증 메모: fix의 '탭 hover는 흰 글자 대신 진한 글자(#1a202c)를 쓰거나'는 모든 탭에 통하지 않음. #1a202c를 쓰면 audiso #D4A017 6.87, hearing #7096B5 5.22, head #4A90C4 4.72로 통과하지만, basic #2E8B57 3.84와 admin #8B6BB5 3.78은 여전히 미달임. 기초팀·행정팀 hover는 배경을 더 진하게 바꿔야 함(예: basic #1f6b43 → 흰 글자 6.48:1, admin #6f4f9a → 흰 글자 6.44:1).

### [중간] Pretendard 전체 글꼴 파일을 굵기별로 통째로 받아 페이지당 글꼴만 1.5~2.3MB 다운로드
- 분류: 성능 · 위치: `embeds/people/html1.people.html:10`, `embeds/people/html1.people.html:55`, `embeds/people/mobileHtml1.people.html:7`
- 영향: 사진과 별도로 글꼴만 1.5MB(모바일)~2.3MB(데스크톱)를 받아야 텍스트가 최종 글꼴로 표시된다. 느린 모바일 망에서 첫 표시가 늦어지고 글꼴이 바뀌며 깜빡인다.
- 고치는 법: 두 파일의 Pretendard 링크를 `https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard-dynamic-subset.min.css`로 교체한다(페이지에 쓰인 글자 묶음만 받음). 추가로 `.tab-btn`의 `font-weight: 500`을 400 또는 700으로 맞추면 굵기 파일 하나를 덜 받는다.
- 검증 메모: impact 보충: 이 비용은 People 페이지 고유가 아니라 embeds 23개 파일이 모두 같은 `pretendard.min.css`를 쓰는 사이트 전체 문제임. jsDelivr가 `max-age=31536000, immutable`로 보내므로 사이트를 처음 방문할 때 한 번만 받음. 따라서 fix도 23개 파일 전체의 Pretendard 링크를 `pretendard-dynamic-subset.min.css`로 바꾸는 것으로 넓혀야 함.

### [낮음] 팀 탭 메뉴의 position:sticky가 iframe 안이라 동작하지 않아, 스크롤하면 탭 바가 사라짐(고정 탭 바용 scroll-margin도 무의미)
- 분류: Wix iframe · 위치: `embeds/people/html1.people.html:48-52`, `embeds/people/html1.people.html:66`, `embeds/people/html1.people.html:332-338`, `embeds/people/mobileHtml1.people.html:21`, `embeds/people/mobileHtml1.people.html:23`, `embeds/people/mobileHtml1.people.html:143-148`
- 영향: 3,400~3,600px 길이의 페이지에서 첫 화면을 지나면 탭 바가 화면 밖으로 사라진다. 방문자가 아래쪽(예: 행정팀)에서 다른 팀으로 이동하려면 맨 위까지 다시 스크롤해야 한다. 코드상 의도(상단 고정 탭)가 실제 사이트에서 구현되지 않는다.
- 고치는 법: iframe 안의 sticky는 동작하지 않으므로 둘 중 하나를 택한다. (1) 탭 바를 Wix 네이티브 요소(메뉴/앵커 버튼)로 만들어 섹션에 고정(Pin/‘스크롤 시 고정’)하고 iframe의 각 섹션 위치에 Wix 앵커를 둔다. (2) 탭 바를 iframe 안에 둔다면 `position: sticky`와 `scroll-margin-top` 규칙을 지워 ‘상단 고정’이라는 잘못된 기대를 없애고, 각 섹션 끝에 '맨 위로' 링크를 추가한다.
- 검증 메모: 심각도를 low로 낮춤. impact에 한 줄 보충: 탭 바가 고정되지 않을 뿐 탭을 누르면 해당 섹션으로 이동하는 기능은 그대로 동작함(보이는 오류가 아니라 의도한 고정 기능이 빠진 것).

### [낮음] 글꼴 지정이 의도대로 적용되지 않음: 한글 팀 제목은 OS 기본 명조체로, 영문 굵은 글씨는 가짜 굵기로, Android는 Times 대신 Pretendard로 표시
- 분류: 버그 · 위치: `embeds/people/html1.people.html:15-19`, `embeds/people/html1.people.html:46`, `embeds/people/html1.people.html:68`, `embeds/people/html1.people.html:158`, `embeds/people/mobileHtml1.people.html:11-15`, `embeds/people/mobileHtml1.people.html:25`, `embeds/people/mobileHtml1.people.html:76`
- 영향: 팀 제목 6개 중 한글 4개가 Windows(바탕체)·Mac(애플명조) 등 OS마다 다른 기본 명조체로 보여, 같은 줄의 영문 제목(Playfair)·본문(Pretendard)과 서체가 제각각이다. 영문 이름 굵은 글씨는 번진 듯한 가짜 볼드로 보이고, Android 방문자는 코드 주석('영어만 Times New Roman')과 다른 서체를 보게 된다.
- 고치는 법: `.team-title`의 font-family를 `'Playfair Display', Pretendard, serif`로 바꿔 한글은 Pretendard로 표시되게 한다. EngSerif에 굵은 면을 추가한다: `@font-face { font-family:'EngSerif'; src: local('Times New Roman Bold'), local('TimesNewRomanPS-BoldMT'); font-weight:700; unicode-range: 같은 범위 }`. Android까지 같은 영문 서체가 필요하면 local() 대신 웹폰트(예: Google Fonts의 Tinos 또는 Libre Caslon)를 지정한다. 두 파일 모두 적용.
- 검증 메모: impact 범위를 좁혀야 함. 가짜 굵기가 적용되는 영문 굵은 글씨는 html1:158 `<h4>Temuulen Batsaikhan</h4>`와 mobile:76 `<h4>Temuulen</h4>` 두 곳(한 사람)뿐임. Android 관련 서술은 오프라인에서 재현하지 못한 부분임.

### [낮음] 제목 단계가 h2에서 h4로 건너뜀(h3 없음)
- 분류: 접근성 · 위치: `embeds/people/html1.people.html:105`, `embeds/people/html1.people.html:120`, `embeds/people/html1.people.html:126`, `embeds/people/mobileHtml1.people.html:45`, `embeds/people/mobileHtml1.people.html:59`, `embeds/people/mobileHtml1.people.html:63`
- 영향: 스크린리더 사용자가 제목 목록으로 페이지 구조를 탐색할 때 팀(h2) 아래 단계가 빠져 있어 구조가 누락된 것처럼 안내된다.
- 고치는 법: 구성원 이름 `<h4>`를 `<h3>`으로 바꾸고 CSS 선택자 `.member-card h4`(html1:82), `.card h4`(mobile:31), `.fac-card h4`(mobile:37)를 `h3`으로 함께 수정한다.

### [낮음] 사진 alt가 바로 아래 이름과 똑같아 스크린리더가 이름을 두 번 읽고, Temuulen 사진 alt는 이름 일부만 있음
- 분류: 접근성 · 위치: `embeds/people/html1.people.html:125-324`, `embeds/people/html1.people.html:157`, `embeds/people/mobileHtml1.people.html:63-138`, `embeds/people/mobileHtml1.people.html:76`
- 영향: 스크린리더 사용자는 카드마다 '서영준, 이미지 / 서영준'처럼 같은 이름을 두 번 듣는다(31회). 사진이라는 정보도 전달되지 않는다.
- 고치는 법: 이름이 바로 옆에 있으므로 `alt=""`로 비워 장식 이미지로 처리하거나, `alt="서영준 교수 사진"`처럼 이름과 구별되는 설명으로 바꾼다. Temuulen은 `alt="Temuulen Batsaikhan 사진"`으로 전체 이름을 쓴다. 두 파일 모두 적용.
- 검증 메모: impact에서 '사진이라는 정보도 전달되지 않는다'를 삭제해야 함(스크린리더가 이미지 역할을 알려 줌). fix는 `alt=""`(장식 이미지로 처리)를 우선 권장함. `alt="서영준 교수 사진"`은 '서영준 교수 사진, 이미지'처럼 또 중복으로 읽힐 수 있음.

#### 검증 단계에서 추가로 발견된 항목 (People)

검증 에이전트가 따로 보고한 것으로, 2차 검증은 거치지 않았습니다.

- [medium, 외부 사실 기반, 파일 증거는 확실함] People 사진 31장이 전부 imgur 무료 호스팅에 핫링크로 걸려 있음. 예: html1:125 `<img src="https://i.imgur.com/vIAp69Y.jpeg" alt="서영준" class="member-photo">`, mobile:63의 같은 URL, html1:125-324와 mobile:63-138의 31개 전부. Imgur는 2025-09-30부터 영국 접속을 차단했고, 계정에 연결되지 않은 오래된 비활성 업로드를 지우는 정책(2023)도 발표함. 그래서 해외(영국) 방문자이거나 imgur가 파일을 지우면 구성원 사진 31장이 한꺼번에 깨짐. 이 환경에서 curl로는 200이 오므로 현재 한국 접속은 정상임. 사진을 Wix 미디어(static.wixstatic.com)로 옮기면 크기 최적화(people-img-oversized)도 함께 해결됨.
- [low] html1:9 `<link rel="preconnect" href="https://fonts.googleapis.com">`은 CSS 호스트에만 preconnect 하고, 실제 글꼴 파일을 주는 fonts.gstatic.com(`crossorigin` 필요)에는 하지 않아 효과가 거의 없음. mobile 파일에는 preconnect가 아예 없음(mobile:7-8).

## Basic Lab

### [높음] 데스크톱 Publication 아코디언의 max-height 3000px 때문에 기본 '전체' 보기에서 논문 14편(2016~2020년)이 잘려 보이지 않음
- 분류: Wix iframe · 위치: `embeds/basic-lab/html1.basic-lab.html:317-324`, `embeds/basic-lab/html1.basic-lab.html:654-1037`, `embeds/basic-lab/html1.basic-lab.html:909-1034`
- 영향: 데스크톱 방문자가 Publication을 펼치면 기본 '전체' 목록이 2020년 논문 중간에서 스크롤바나 안내 없이 끊깁니다. 2020·2019·2018·2017·2016년 논문 14편이 아예 없는 것처럼 보입니다.
- 고치는 법: `.collapse-body.open`의 max-height 고정값을 없애야 합니다. 방법은 둘 중 하나입니다. (1) JS에서 `el.style.maxHeight = el.scrollHeight + 'px'`로 실제 높이를 넣고, 필터를 바꿀 때마다 다시 계산합니다. (2) 열린 상태를 `max-height:none`으로 바꿉니다. 모바일(8000px)과 같은 방식으로 맞추는 것이 좋습니다. 이렇게 고쳐도 아래 'iframe 높이' 문제는 따로 해결해야 합니다.
- 검증 메모: 개수 표현만 바로잡습니다. '14편이 안 보이고 그 위 1편도 잘림'이 아니라, 2016~2020년 논문 14편 가운데 13편은 완전히 가려지고 1편(909행 'Improvement of stem cell-derived exosome…')은 중간이 잘립니다. 완전히 가려지는 첫 항목은 918행 'In vitro time-lapse live-cell imaging…'입니다. 수정안의 '모바일(8000px)과 같은 방식'은 따르면 안 됩니다. 모바일 56행 `.collapse-body.open{max-height:8000px}`도 고정 상한이라, 현재 pub-body 6177px(한 편당 약 150px) 기준으로 약 12편만 더 추가되면 모바일도 똑같이 잘립니다. 양쪽 모두 max-height:none 또는 scrollHeight 방식으로 바꾸는 것이 맞습니다.

### [높음] 아코디언을 펼치면 콘텐츠가 고정된 iframe 높이(데스크톱 3212px, 모바일 1979px)를 크게 넘어 iframe 안에 스크롤이 생김
- 분류: Wix iframe · 위치: `docs/site-map.md:22-23`, `embeds/basic-lab/html1.basic-lab.html:650-654`, `embeds/basic-lab/html1.basic-lab.html:1042-1046`, `embeds/basic-lab/mobileHtml1.basic-lab-mobile.html:55-56`, `embeds/basic-lab/mobileHtml1.basic-lab-mobile.html:144-145`
- 영향: 데스크톱에서 Publication을 펼치면 약 2800~2930px, 모바일에서는 약 6200px가 iframe 내부 스크롤 영역으로 들어갑니다. 방문자는 페이지 스크롤과 iframe 스크롤이 겹친 이중 스크롤을 겪습니다. 휴대폰에서는 1979px짜리 iframe 안에서 다시 6000px 넘게 스크롤해야 해서 목록 아래쪽을 사실상 보기 어렵습니다. 접힌 상태의 데스크톱에서는 페이지 하단에 186px 흰 여백이 생깁니다.
- 고치는 법: Wix HTML iframe은 높이가 자동으로 늘어나지 않습니다. 다음 중 하나를 권장합니다. (1) 논문 목록을 iframe 안에 펼치지 말고 페이지당 5~10편씩 보여 주는 페이지네이션을 넣습니다. (2) '전체 목록은 Research 페이지에서' 형태로 링크만 둡니다(`target="_top"`). (3) Velo의 `$w('#html1')`와 postMessage로 높이를 조절합니다. 적어도 접힌 상태 기준으로 데스크톱 에디터 높이를 3026px에 맞춰 빈 여백은 없애야 합니다.
- 검증 메모: 수정안 (3)은 쓸 수 없습니다. Velo HtmlComponent API에는 높이를 바꾸는 속성이나 메서드가 없습니다(문서 목록: allow, scrolling, src, collapsed, hidden … postMessage/onMessage). postMessage로 높이를 알려 줘도 iframe 크기를 바꿀 방법이 없으니 (3)은 빼야 합니다. 에디터 높이를 3026px에 딱 맞추는 것도 권하지 않습니다. 측정값은 Times New Roman 없이 잰 것이라 ±3% 오차가 있고, Windows/Mac에서 글꼴 때문에 조금만 길어져도 접힌 상태에서 스크롤바가 생깁니다. 약간 여유를 두거나 Windows에서 실제로 확인한 뒤 정해야 합니다.

### [중간] 데스크톱에 .pub-authors와 .pub-tag.team-basic 스타일이 없어 저자 줄이 논문 제목보다 크게 보이고 'Basic Lab' 태그에 배경이 없음
- 분류: 버그 · 위치: `embeds/basic-lab/html1.basic-lab.html:362-394`, `embeds/basic-lab/html1.basic-lab.html:668`, `embeds/basic-lab/html1.basic-lab.html:671`
- 영향: 데스크톱에서 Publication을 펼친 방문자에게는 41편 모두 저자 목록(16px, 진한 글자)이 논문 제목(14.7px)보다 크고 진하게 보여 제목과 저자가 구분되지 않습니다. 'Basic Lab' 태그도 옆의 연도·저널 알약형 태그와 달리 배경 없는 맨 글자로 나옵니다.
- 고치는 법: 데스크톱 CSS에 모바일과 같은 규칙을 추가합니다. `.pub-authors{font-size:0.8rem;color:var(--text-mid);margin-bottom:5px}`, `.pub-tag.team-basic{background:var(--accent-light);color:var(--accent-dark)}`. 이 페이지의 모든 논문이 Basic Lab이므로 team-basic 태그를 아예 빼는 방법도 있습니다.

### [중간] Report 아코디언은 '연동 예정' 안내문만 있는 빈 섹션이고, 데스크톱의 연도 필터 버튼 5개는 눌러도 아무 변화가 없음
- 분류: 내용·데이터 · 위치: `embeds/basic-lab/html1.basic-lab.html:1040-1064`, `embeds/basic-lab/html1.basic-lab.html:1103-1121`, `embeds/basic-lab/mobileHtml1.basic-lab-mobile.html:516-519`, `embeds/research/html1.research.html:1605`
- 영향: 방문자가 Report를 펼치면 개발 중 메모 같은 '연동 예정' 문구와 작동하지 않는 필터 버튼만 봅니다. 데스크톱은 '연동 예정', 모바일은 'Research 페이지에서 확인'으로 안내가 서로 다르고, 모바일에는 이동할 링크도 없습니다.
- 고치는 법: Report 아코디언과 필터 버튼을 없애고 `<a href="https://www.smilesnail.org/project" target="_top">학회 발표는 Research 페이지에서 보기 →</a>` 한 줄로 바꿉니다. 데스크톱과 모바일에 같은 문구를 씁니다. 실제 데이터를 넣을 경우에는 pub-item을 채우고 버튼 구성(~2021 포함)을 Publication과 맞춥니다.

### [중간] 데스크톱과 모바일의 문구가 서로 다름(Mission/Vision 전체 문장, 히어로, 조직도 명칭·순서, 소장 소속, 연구주제 제목)
- 분류: 데스크톱·모바일 불일치 · 위치: `embeds/basic-lab/html1.basic-lab.html:485-487`, `embeds/basic-lab/mobileHtml1.basic-lab-mobile.html:85`, `embeds/basic-lab/html1.basic-lab.html:516`, `embeds/basic-lab/html1.basic-lab.html:520`, `embeds/basic-lab/mobileHtml1.basic-lab-mobile.html:100-101`, `embeds/basic-lab/html1.basic-lab.html:536-560`, `embeds/basic-lab/mobileHtml1.basic-lab-mobile.html:107-113`, `embeds/basic-lab/html1.basic-lab.html:582` 외
- 영향: 같은 페이지인데 PC와 휴대폰에서 연구실의 Mission·Vision 문장이 완전히 다르게 나와, 어느 쪽이 공식 문구인지 알 수 없습니다. 조직도의 상위 기관 이름과 하위 조직 순서, 소장 소속 표기도 기기마다 다릅니다.
- 고치는 법: 공식 문구를 하나로 정하고 두 파일에 똑같이 반영합니다. Mission/Vision, 히어로 문구, 조직도(명칭 'Audiso Co., Ltd.' 여부, 순서), 소속 표기('연세대학교' 포함 여부), 연구주제 제목을 통일합니다. 앞으로는 수정할 때마다 데스크톱과 모바일을 함께 고치는 체크리스트를 두는 것을 권장합니다.

### [중간] 모바일에는 논문 연도 필터와 Alumni 섹션이 없고, 논문 수 '(41편)'은 모바일에만 표시됨
- 분류: 데스크톱·모바일 불일치 · 위치: `embeds/basic-lab/html1.basic-lab.html:656-664`, `embeds/basic-lab/mobileHtml1.basic-lab-mobile.html:144-145`, `embeds/basic-lab/html1.basic-lab.html:1081-1086`, `embeds/basic-lab/mobileHtml1.basic-lab-mobile.html:69-74`, `embeds/basic-lab/mobileHtml1.basic-lab-mobile.html:520-522`
- 영향: 휴대폰 방문자는 연도별로 걸러 볼 수 없어 약 6000px 길이의 목록을 전부 스크롤해야 합니다. 데스크톱에만 있는 Alumni 섹션은 모바일 사용자에게 보이지 않습니다.
- 고치는 법: 모바일에도 데스크톱과 같은 연도 필터 버튼을 추가합니다(가로 스크롤 칩이면 320px에서도 들어갑니다). Alumni 섹션을 모바일에도 넣거나, 졸업생이 없는 동안에는 두 쪽 모두에서 빼서 구성을 맞춥니다. 논문 수 표시도 양쪽에 똑같이 두거나 둘 다 뺍니다.

### [중간] 저자 목록 14건이 이름 중간에서 '...'로 잘렸고, 붙어 쓴 이름과 빈 저자(', ,')가 방문자에게 그대로 보임
- 분류: 내용·데이터 · 위치: `embeds/basic-lab/html1.basic-lab.html:713`, `embeds/basic-lab/html1.basic-lab.html:776`, `embeds/basic-lab/html1.basic-lab.html:794`, `embeds/basic-lab/html1.basic-lab.html:803`, `embeds/basic-lab/html1.basic-lab.html:812`, `embeds/basic-lab/html1.basic-lab.html:839`, `embeds/basic-lab/html1.basic-lab.html:857`, `embeds/basic-lab/html1.basic-lab.html:866` 외
- 영향: PC와 모바일 모두에서 저자 이름이 'Tae Hoo...', 'Brown Da...'처럼 단어 중간에서 끊겨 공동저자 정보가 틀리거나 빠져 보입니다. 'SUNMOKHA', 'JINSILCHOI' 같은 표기는 실제 이름으로 알아보기 어렵습니다.
- 고치는 법: 원본 DB(WoS/Scopus 등)에서 저자 목록을 다시 받아, 잘린 14건은 전체 저자를 넣거나 'Kong TH, et al.'처럼 et al. 형식으로 통일합니다. 'Ha SM', 'Choi JS', 'Park YA', 'Bae MR'처럼 표기 형식을 하나로 맞추고 1001행의 빈 저자(', ,')는 지웁니다. 같은 데이터를 쓰는 Research 페이지(html1/mobileHtml1)도 함께 고칩니다.
- 검증 메모: 위치 목록에 992행(`HYUNMI JU, SUNHEE LEE, JINSILCHOI , YOUNG JOON SEO`)과 모바일 대응 줄이 빠져 있습니다. 증거에는 적혀 있으니 위치 목록에도 넣으면 됩니다.

### [중간] 아코디언 헤더가 onclick만 있는 div라 키보드로 열 수 없고, 접힌 상태에서도 숨은 필터 버튼에 Tab 포커스가 들어감
- 분류: 접근성 · 위치: `embeds/basic-lab/html1.basic-lab.html:650`, `embeds/basic-lab/html1.basic-lab.html:1042`, `embeds/basic-lab/html1.basic-lab.html:317-321`, `embeds/basic-lab/mobileHtml1.basic-lab-mobile.html:144`, `embeds/basic-lab/mobileHtml1.basic-lab-mobile.html:516`
- 영향: 키보드와 스크린리더 사용자는 Publication/Report를 펼칠 수 없어 논문 목록에 접근하지 못합니다. 데스크톱에서는 보이지 않는 필터 버튼 14개(7개씩 2세트)에 포커스가 머물러 화면에서 포커스 위치를 놓칩니다.
- 고치는 법: 헤더를 `<button type="button" class="collapse-header" aria-expanded="false" aria-controls="pub">`로 바꾸고, 토글할 때 aria-expanded 값을 바꿉니다. 접힌 본문에는 `hidden` 속성(또는 visibility:hidden)을 함께 줘서 포커스와 읽기 대상에서 빠지게 합니다. ▼ 화살표에는 aria-hidden="true"를 붙입니다.
- 검증 메모: 두 가지를 바로잡습니다. (1) 숨은 필터 버튼은 14개(7+7)가 아니라 13개입니다. Publication 7개(657-663행), Report 6개(1049-1054행)입니다. (2) '스크린리더 사용자는 논문 목록에 접근하지 못합니다'는 틀렸습니다. 접힘을 max-height:0과 overflow:hidden만으로 처리해서, 접힌 상태에서도 41편이 접근성 트리에 그대로 노출됩니다(CDP getFullAXTree에서 마지막 논문 'Head position…'이 StaticText로 나옴). 스크린리더 사용자의 실제 문제는 열림/닫힘 상태(aria-expanded)를 알 수 없는 것과, 화면에서는 잘린 항목도 읽혀 보이는 화면과 읽히는 내용이 다르다는 점입니다. 펼칠 수 없는 사람은 마우스 없이 키보드만 쓰는 시각 사용자입니다(데스크톱 기준).

### [중간] 작은 글자의 명도 대비가 WCAG AA 기준 4.5:1에 못 미침(#999 2.85:1, #718096 4.02:1, 초록 배경 흰 글자 4.25:1, 초록 태그 3.90:1)
- 분류: 접근성 · 위치: `embeds/basic-lab/html1.basic-lab.html:31`, `embeds/basic-lab/html1.basic-lab.html:59-62`, `embeds/basic-lab/html1.basic-lab.html:73-75`, `embeds/basic-lab/html1.basic-lab.html:348-353`, `embeds/basic-lab/html1.basic-lab.html:1058`, `embeds/basic-lab/html1.basic-lab.html:1083`, `embeds/basic-lab/mobileHtml1.basic-lab-mobile.html:19`, `embeds/basic-lab/mobileHtml1.basic-lab-mobile.html:61` 외
- 영향: 저시력 사용자나 밝은 야외에서 휴대폰을 보는 사용자는 모바일 저자 목록(11px 회색), 9.9px 'Basic Lab' 태그, 선택된 연도 필터 글자, Report 안내문을 읽기 어렵습니다.
- 고치는 법: #718096은 #4a5568(7.53:1) 정도로, #999는 #666 이하로 어둡게 합니다. 초록 배경 흰 글자는 이미 정의된 `--accent-dark` #1F6B42(6.48:1)를 쓰고, 연한 초록 배경 위 글자색도 #2E8B57 대신 #1F6B42(5.96:1)로 바꿉니다. 모바일 태그 글자는 최소 11px(0.7rem) 이상으로 키웁니다.

### [낮음] Publication '2026' 필터를 누르면 해당 논문이 0편이라 안내 문구 없이 빈 상자만 보임
- 분류: 버그 · 위치: `embeds/basic-lab/html1.basic-lab.html:658`, `embeds/basic-lab/html1.basic-lab.html:1103-1121`, `embeds/basic-lab/html1.basic-lab.html:630`
- 영향: '2026'을 누른 방문자에게는 필터 버튼 줄 아래가 비어 있어 목록이 고장 난 것처럼 보입니다.
- 고치는 법: 항목이 없는 연도 버튼(2026)은 숨기거나, filterYear 끝에서 보이는 항목 수를 세어 0이면 '해당 연도 논문이 없습니다.' 문구를 표시합니다. 버튼 목록을 data-year 값에서 자동으로 만들면 앞으로도 맞게 유지됩니다.

### [낮음] 데스크톱에서 소개 두 번째 문단과 Mission 카드가 글자 하나 다르지 않은 같은 문장임
- 분류: 내용·데이터 · 위치: `embeds/basic-lab/html1.basic-lab.html:501`, `embeds/basic-lab/html1.basic-lab.html:516`, `embeds/basic-lab/mobileHtml1.basic-lab-mobile.html:93`
- 영향: 데스크톱 방문자는 스크롤 약 300px 안에서 같은 문장을 두 번 읽게 됩니다.
- 고치는 법: 소개 두 번째 문단을 다른 내용(주요 연구 성과, 장비 등)으로 바꾸거나 Mission 문장을 새로 씁니다. 모바일 Mission 문구와도 함께 통일합니다(drift 항목 참고).

### [낮음] 같은 저널을 다른 이름·대소문자로 표기함(4개 저널)
- 분류: 내용·데이터 · 위치: `embeds/basic-lab/html1.basic-lab.html:681`, `embeds/basic-lab/html1.basic-lab.html:726`, `embeds/basic-lab/html1.basic-lab.html:699`, `embeds/basic-lab/html1.basic-lab.html:798`, `embeds/basic-lab/html1.basic-lab.html:717`, `embeds/basic-lab/html1.basic-lab.html:996`, `embeds/basic-lab/html1.basic-lab.html:951`, `embeds/basic-lab/html1.basic-lab.html:969`
- 영향: 같은 저널이 서로 다른 저널처럼 보이고, 대문자와 일반 표기가 섞여 목록이 정리되지 않은 인상을 줍니다.
- 고치는 법: 저널명을 공식 표기(예: 'Journal of Audiology & Otology', 'Laryngoscope Investigative Otolaryngology', 'BioMed Research International', 'International Journal of Molecular Sciences')로 통일합니다. 데스크톱, 모바일, Research 페이지를 함께 고칩니다.

### [낮음] Research Subjects 카드의 hover 떠오름 효과가 .fade.show 규칙에 덮여 작동하지 않음
- 분류: 버그 · 위치: `embeds/basic-lab/html1.basic-lab.html:275-278`, `embeds/basic-lab/html1.basic-lab.html:440-443`, `embeds/basic-lab/html1.basic-lab.html:607`
- 영향: 코드에 의도된 카드 hover 이동 효과가 데스크톱 방문자에게 보이지 않습니다. 기능상 영향은 작습니다.
- 고치는 법: `.rs-card.fade.show:hover { transform: translateY(-2px); }`처럼 명시도를 높이거나, 페이드 애니메이션을 transform 대신 opacity만으로 처리합니다. 효과가 필요 없으면 275-278행을 지웁니다.

### [낮음] 제목 단계가 h2에서 h4로 건너뜀(데스크톱 연구주제, 모바일 Director·연구주제)
- 분류: 접근성 · 위치: `embeds/basic-lab/html1.basic-lab.html:605-608`, `embeds/basic-lab/mobileHtml1.basic-lab-mobile.html:119-122`, `embeds/basic-lab/mobileHtml1.basic-lab-mobile.html:132-134`
- 영향: 스크린리더 사용자가 제목 목록으로 이동할 때 h3가 빠져 있어 문서 구조를 잘못 이해할 수 있습니다.
- 고치는 법: 연구주제 카드 제목과 모바일 인물 이름을 h3로 바꾸고, 글자 크기는 CSS로 유지합니다.

### [낮음] 110px(데스크톱)·70px(모바일)로 표시하는 인물 사진 2장을 원본(870×864 116KB, 931×1396 267KB) 그대로 받음
- 분류: 성능 · 위치: `embeds/basic-lab/html1.basic-lab.html:578`, `embeds/basic-lab/html1.basic-lab.html:589`, `embeds/basic-lab/html1.basic-lab.html:219-221`, `embeds/basic-lab/mobileHtml1.basic-lab-mobile.html:121`, `embeds/basic-lab/mobileHtml1.basic-lab-mobile.html:125`, `embeds/basic-lab/mobileHtml1.basic-lab-mobile.html:41`
- 영향: 두 사진에 383KB를 받지만 표시 크기에는 약 27KB면 충분합니다. 모바일 데이터 사용자에게는 불필요하게 로딩이 늦어집니다.
- 고치는 법: src를 imgur 중간 크기 썸네일(`https://i.imgur.com/vIAp69Ym.jpeg`, `https://i.imgur.com/SkXdr8pm.jpeg`, 최대 320px)로 바꾸고 `width="110" height="110" loading="lazy"`를 추가합니다. 같은 이미지를 쓰는 home, people, hearing-lab, head-lab 페이지에도 똑같이 적용할 수 있습니다.
- 검증 메모: SkXdr8pm은 가로가 214px라 110px 정사각형을 2x 화면에 보여 줄 때 필요한 220px에 조금 못 미칩니다. 레티나에서도 선명해야 하면 'l' 썸네일(SkXdr8pl 427x640 35,223B, vIAp69Yl 640x636 44,783B)을 써도 원본보다 약 80% 가볍습니다. SkXdr8p는 basic-lab과 people에서만 쓰고, home·hearing-lab·head-lab이 쓰는 것은 vIAp69Y뿐입니다.

### [낮음] 낡은 TODO와 주석, 실제 항목과 다른 논문 추가 템플릿, 쓰지 않는 CSS, 4곳에 복제된 논문 데이터가 유지보수 실수를 부름
- 분류: 유지보수 · 위치: `embeds/basic-lab/html1.basic-lab.html:8`, `embeds/basic-lab/html1.basic-lab.html:494`, `embeds/basic-lab/html1.basic-lab.html:528`, `embeds/basic-lab/html1.basic-lab.html:588`, `embeds/basic-lab/html1.basic-lab.html:630-643`, `embeds/basic-lab/mobileHtml1.basic-lab-mobile.html:9-16`, `embeds/basic-lab/mobileHtml1.basic-lab-mobile.html:26-29`, `embeds/basic-lab/mobileHtml1.basic-lab-mobile.html:67-68` 외
- 영향: 템플릿대로 새 논문을 추가하면 저자 줄과 팀 태그가 빠진 항목이 생깁니다. 논문 하나를 추가할 때 네 파일과 '(41편)' 숫자를 모두 고치지 않으면 PC·모바일·Research 페이지의 목록이 서로 어긋납니다. 이미 끝난 TODO가 남아 있어 무엇이 남은 작업인지 헷갈립니다.
- 고치는 법: 끝난 TODO와 틀린 주석을 지웁니다. 템플릿을 실제 항목 구조(pub-title/pub-authors/pub-tags)로 바꿉니다. 쓰지 않는 CSS를 정리합니다. 장기적으로는 논문 데이터를 JS 배열이나 JSON 하나로 두고 목록과 개수('41편')를 스크립트로 만들어, 네 곳을 따로 고칠 필요를 없앱니다.

#### 검증 단계에서 추가로 발견된 항목 (Basic Lab)

검증 에이전트가 따로 보고한 것으로, 2차 검증은 거치지 않았습니다.

- [low, a11y] 데스크톱 연도 필터 버튼이 선택 상태를 색(.active 클래스)으로만 나타냄. aria-pressed가 없어 스크린리더 사용자는 어떤 필터가 켜져 있는지 알 수 없음(WCAG 4.1.2). embeds/basic-lab/html1.basic-lab.html:657 `<button class="year-btn active" onclick="filterYear(this,'pub')">전체</button>`, 1105-1108행 `b.classList.remove('active'); ... btn.classList.add('active');`에서 클래스만 바꾸고 상태 속성은 건드리지 않음. 게다가 348-349행 `.year-btn.active, .year-btn:hover`가 hover와 active를 같은 모양으로 그려서, 마우스를 올리면 어느 버튼이 선택됐는지 눈으로도 구분이 안 됨.
- [low, maintainability/latent clipping] 모바일 Publication도 높이 상한이 고정돼 있음. embeds/basic-lab/mobileHtml1.basic-lab-mobile.html:56 `.collapse-body.open{max-height:8000px}`. 현재 pub-body scrollHeight는 6177px(렌더링 측정)이고 한 편당 약 150px라, 논문이 약 12편 더 늘면 데스크톱 3000px 문제와 똑같이 끝부분이 스크롤바 없이 잘림. 데스크톱 수정 때 모바일 상한도 같이 없애야 함.

## Hearing Lab

### [높음] Publication 아코디언을 펼치면 내용이 iframe 고정 높이를 크게 넘어 Alumni와 논문 목록 하단이 잘림 (데스크톱·모바일 모두)
- 분류: Wix iframe · 위치: `embeds/hearing-lab/html1.hearing-lab.html:378-385`, `embeds/hearing-lab/html1.hearing-lab.html:743-747`, `embeds/hearing-lab/mobileHtml1.hearing-lab-mobile.html:50-51`, `embeds/hearing-lab/mobileHtml1.hearing-lab-mobile.html:141-142`, `docs/site-map.md:24-25`
- 영향: 논문 목록을 보려고 Publication을 여는 모든 방문자는 목록 중간 이후(데스크톱 약 1,870px, 모바일 약 2,870px)와 Alumni 섹션을 iframe 안의 별도 스크롤로만 볼 수 있거나 잘린 채로 보게 됩니다. 모바일에서는 페이지 스크롤과 iframe 내부 스크롤이 겹쳐 특히 불편합니다. 접힌 상태의 데스크톱에서는 페이지 하단에 약 200px 빈 공간이 생깁니다.
- 고치는 법: iframe 전체 높이가 변하지 않도록 목록 상자 자체를 고정 높이 스크롤 영역으로 바꾸세요. 예: `.collapse-body.open{max-height:none}` 대신 `.collapse-inner #pub-list{max-height:560px; overflow-y:auto}`(모바일도 동일)로 두고, Wix 에디터 높이를 '접힌 높이 + 펼친 목록 상자 높이'(데스크톱 약 3806+650, 모바일 약 2364+650)로 맞춥니다. 또는 페이지 내 목록은 최근 5편만 보여주고 '전체 보기'를 Research 페이지 링크(target="_top")로 연결하세요. 데스크톱 에디터 높이는 접힘 상태 기준으로 약 3810px로 줄여 하단 여백을 없애세요.
- 검증 메모: 영향 수정: 잘리는 범위가 '목록 중간 이후'보다 큽니다. 에디터 높이 안에 완전히 들어오는 논문은 데스크톱에서 19편 중 첫 5편, 모바일에서는 첫 1편뿐입니다(#pub 시작 y=3357/2078). 따라서 모바일에서는 목록 거의 전부와 Alumni를 iframe 내부 스크롤로만 볼 수 있습니다. 수정안 보완: 제안한 '접힌 높이 + 650px'로 에디터 높이를 늘리면 아코디언이 접혀 있는 동안(기본 상태) 하단에 약 650px 빈 공간이 생겨 같은 문제가 반대로 나타납니다. 목록 상자를 아코디언 밖에 항상 펼친 고정 높이 스크롤 상자로 두거나(높이 불변), 최근 5편만 보여주고 Research 페이지 링크(target="_top")를 다는 방식이 맞습니다.

### [높음] Research 페이지에 있는 Hearing Lab 2026년 논문 2편이 Hearing Lab 페이지에 없고, '2026' 필터를 누르면 빈 목록이 나옴
- 분류: 내용·데이터 · 위치: `embeds/hearing-lab/html1.hearing-lab.html:751`, `embeds/hearing-lab/html1.hearing-lab.html:758-759`, `embeds/hearing-lab/html1.hearing-lab.html:1008`, `embeds/hearing-lab/mobileHtml1.hearing-lab-mobile.html:141-143`, `embeds/research/html1.research.html:496-513`, `embeds/research/mobileHtml1.research.html:92`, `embeds/research/mobileHtml1.research.html:101`
- 영향: Hearing Lab 페이지 방문자는 연구팀의 가장 최근 성과(특히 참조표준의 핵심 결과인 한국인 성인 정상 청력역치 논문)를 볼 수 없고, 데스크톱에서 '2026' 버튼을 누르면 아무것도 없는 빈 목록을 보게 됩니다. 같은 사이트의 Research 페이지와 내용이 서로 다릅니다.
- 고치는 법: 두 논문 항목을 research/html1.research.html 496-513행에서 복사해 hearing-lab 데스크톱 `#pub-list` 맨 위(758행 다음)와 모바일 142행 다음에 추가하고, 모바일 제목을 `Publication (21편)`으로 고치세요. filterYear()에 표시 항목이 0개일 때 '해당 연도 논문이 없습니다' 문구를 보여주는 처리를 추가하세요.
- 검증 메모: research/html1.research.html의 해당 항목은 497-513행입니다(496행은 빈 줄). 그 외 내용은 그대로 맞습니다.

### [중간] Report 아코디언이 미완성 안내 문구만 있고, 연도 필터 버튼 6개는 눌러도 아무 변화가 없음 (데스크톱·모바일 문구도 서로 모순)
- 분류: 버그 · 위치: `embeds/hearing-lab/html1.hearing-lab.html:937-958`, `embeds/hearing-lab/html1.hearing-lab.html:1001-1002`, `embeds/hearing-lab/mobileHtml1.hearing-lab-mobile.html:315-318`
- 영향: Report를 연 방문자는 '연동 예정'이라는 공사 중 문구와 눌러도 반응 없는 필터 버튼만 보게 됩니다. 데스크톱은 '연동 예정', 모바일은 'Research 페이지에서 확인하세요'라고 서로 다르게 안내하고, 둘 다 해당 페이지로 가는 링크가 없습니다.
- 고치는 법: 당장은 Report의 연도 필터 버튼(943-950행)을 삭제하고, 안내 문구를 양쪽 모두 `<a href="https://www.smilesnail.org/project" target="_top">Research 페이지에서 학회 발표 보기 →</a>`로 통일하세요. 이후 Research 페이지의 학회 발표 중 Hearing Lab 항목에 data-team="hearing"을 붙여 이 목록을 채우면 필터가 동작합니다.
- 검증 메모: 심각도 high → medium. Report는 클릭해야 열리고, 잘못된 정보 없이 '연동 예정' 안내만 보이는 미완성 영역입니다.

### [중간] 데스크톱 논문 목록에서 저자(.pub-authors)와 'Hearing Lab' 태그(.team-hearing)에 CSS가 없어 저자가 제목보다 크게, 태그는 맨글자로 표시됨
- 분류: 버그 · 위치: `embeds/hearing-lab/html1.hearing-lab.html:421-453`, `embeds/hearing-lab/html1.hearing-lab.html:761`, `embeds/hearing-lab/html1.hearing-lab.html:764`, `embeds/hearing-lab/mobileHtml1.hearing-lab-mobile.html:55`, `embeds/hearing-lab/mobileHtml1.hearing-lab-mobile.html:61`
- 영향: 데스크톱 방문자에게 저자 목록이 논문 제목보다 큰 글씨로 보여 제목과 저자가 구분되지 않고, 'Hearing Lab' 태그만 배지 모양 없이 떠 있는 글자로 보여 깨진 화면처럼 보입니다.
- 고치는 법: 데스크톱 <style>의 `.pub-tag.conf` 다음에 `.pub-authors{font-size:0.8rem;color:var(--text-mid);margin-bottom:5px}`와 `.pub-tag.team-hearing{background:var(--accent-light);color:var(--accent-dark)}`를 추가하세요.

### [중간] 데스크톱과 모바일의 Mission·Vision 문장이 완전히 다르고, 모바일에는 데이터센터 상세·소개 이미지·연도 필터가 빠져 있는 등 내용 불일치
- 분류: 데스크톱·모바일 불일치 · 위치: `embeds/hearing-lab/html1.hearing-lab.html:545-547`, `embeds/hearing-lab/html1.hearing-lab.html:565-567`, `embeds/hearing-lab/html1.hearing-lab.html:581-600`, `embeds/hearing-lab/html1.hearing-lab.html:612-619`, `embeds/hearing-lab/html1.hearing-lab.html:634-658`, `embeds/hearing-lab/html1.hearing-lab.html:679`, `embeds/hearing-lab/html1.hearing-lab.html:711`, `embeds/hearing-lab/html1.hearing-lab.html:749-757` 외
- 영향: 모바일(Wix 모바일 레이아웃) 방문자는 데스크톱과 다른 연구실 미션·비전 문장을 보게 되어 공식 문구가 무엇인지 혼란스럽고, 데이터센터의 역할 8개 항목·설명·소개 이미지를 전혀 볼 수 없습니다. 조직도 순서도 기기마다 다릅니다.
- 고치는 법: Mission·Vision 공식 문구를 하나로 정해 두 파일에 같은 문장을 넣으세요. 모바일 dc-box에 영문 명칭, 설명 문단(최소 1-2개)과 8개 항목 `<ul>`을 추가하고, 조직도 순서·명칭(상위 박스 전체 이름, 'Audiso Co., Ltd.')과 소속 표기(연세대학교 포함)를 데스크톱과 맞추세요. 앞으로 수정 시 README 안내대로 두 파일을 함께 고치세요.

### [중간] 논문 저자 목록이 이름 중간에서 잘리거나 빈 저자가 있고, 같은 저널명이 두 가지로 표기되는 등 서지정보 오류
- 분류: 내용·데이터 · 위치: `embeds/hearing-lab/html1.hearing-lab.html:761`, `embeds/hearing-lab/html1.hearing-lab.html:779`, `embeds/hearing-lab/html1.hearing-lab.html:788`, `embeds/hearing-lab/html1.hearing-lab.html:797`, `embeds/hearing-lab/html1.hearing-lab.html:855`, `embeds/hearing-lab/html1.hearing-lab.html:869`, `embeds/hearing-lab/html1.hearing-lab.html:887`, `embeds/hearing-lab/html1.hearing-lab.html:896` 외
- 영향: 방문자에게 공동저자 이름이 'Cho Wan-...', 'Ji Hy...'처럼 중간에서 잘려 보이고, 쉼표만 있는 빈 저자 칸이 보여 자료가 부정확하다는 인상을 줍니다. 저자 본인 이름이 잘린 경우 연구 실적 확인에도 지장이 있습니다.
- 고치는 법: 원 논문(DOI)에서 전체 저자 목록을 받아 6건의 '...' 부분을 완성하고(또는 'Kim D-Y, et al.'처럼 et al.로 명시), 896행의 `, ,`와 869행 `HANJAEHYUN ,`를 `Jaehyun Han,`으로 고치세요. 저널명은 'Journal of Audiology and Otology'로 통일하고, ICA 발표집은 conf 태그로 바꾸거나 Report로 옮기세요. 데스크톱·모바일·Research 페이지 4개 파일 모두 같이 수정해야 합니다.
- 검증 메모: 이름 중간에서 잘린 것은 4건(761 `Kim,...`, 779 `Cho Wan-...`, 887 `YOUNG JOO...`, 905 `Ji Hy...`)입니다. 788과 797은 완전한 이름 뒤에 '...'만 붙은 경우라 'et al.'로 바꾸면 됩니다. 896행의 빈 저자는 Crossref 기준 'Tae Hoon Kong'이고, 869행은 'Jaehyun Han, Tae Hui Kim'입니다. 저널명: Crossref 저널 레코드(ISSN 2384-1621)의 공식 표기는 'Journal of Audiology & Otology'이므로, 'and'가 공식명이라는 근거는 틀렸습니다. 한 가지로 통일하되 저널 자체 표기인 '&'를 권장합니다.

### [중간] Publication/Report 아코디언 제목이 클릭만 되는 div라 키보드로 열 수 없고, 접힌 상태에서도 안의 필터 버튼에 Tab 포커스가 들어감
- 분류: 접근성 · 위치: `embeds/hearing-lab/html1.hearing-lab.html:743`, `embeds/hearing-lab/html1.hearing-lab.html:937`, `embeds/hearing-lab/html1.hearing-lab.html:378-382`, `embeds/hearing-lab/html1.hearing-lab.html:750-756`, `embeds/hearing-lab/html1.hearing-lab.html:944-949`, `embeds/hearing-lab/mobileHtml1.hearing-lab-mobile.html:141`, `embeds/hearing-lab/mobileHtml1.hearing-lab-mobile.html:315`
- 영향: 키보드·스크린리더 사용자는 논문 목록(이 페이지의 핵심 자료)을 열 방법이 없고, 데스크톱에서는 Tab을 누를 때 보이지 않는 버튼 13개에 포커스가 들어가 현재 위치를 잃습니다. 스크린리더에는 펼침/접힘 상태도 전달되지 않습니다.
- 고치는 법: collapse-header를 `<button type="button" class="collapse-header" aria-expanded="false" aria-controls="pub">`로 바꾸고 toggle 함수에서 aria-expanded를 갱신하세요. 접힌 본문에는 `hidden` 속성(또는 `visibility:hidden`을 transition 후 적용)을 주어 내부 버튼이 포커스되지 않게 하세요.

### [중간] 작은 글씨 다수가 WCAG AA 명암비(4.5:1)에 미달 — 특히 모바일 배지·팀 태그 2.78:1
- 분류: 접근성 · 위치: `embeds/hearing-lab/html1.hearing-lab.html:26-32`, `embeds/hearing-lab/html1.hearing-lab.html:60-65`, `embeds/hearing-lab/html1.hearing-lab.html:73-78`, `embeds/hearing-lab/html1.hearing-lab.html:185-189`, `embeds/hearing-lab/html1.hearing-lab.html:313-321`, `embeds/hearing-lab/html1.hearing-lab.html:408-413`, `embeds/hearing-lab/html1.hearing-lab.html:444-448`, `embeds/hearing-lab/html1.hearing-lab.html:953` 외
- 영향: 저시력 사용자나 햇빛 아래 휴대폰으로 보는 방문자는 모바일의 Director/Manager 배지, 논문별 'Hearing Lab' 태그, 저자 목록, 졸업 연도, 데스크톱의 Report 안내문·선택된 필터 버튼 글자를 읽기 어렵습니다.
- 고치는 법: 작은 글자용 색을 진하게 바꾸세요: 모바일 `.badge`, `.pub-tag.team-hearing`의 글자색 #7096B5 → #4E7595 이하(가능하면 #3F6380, 5.6:1 이상), `#718096` → `#5A6678`(약 5.9:1), 데스크톱 `#999` → `#666`, 흰 글자 배경 `#7096B5` → `#4E7595`(4.9:1), `--accent-dark`를 #466B8A 정도로 한 단계 진하게.
- 검증 메모: 수정안 정정: 모바일 `.badge`와 `.pub-tag.team-hearing`(배경 #EDF2F8)에 #4E7595를 쓰면 4.34:1로 여전히 AA 미달입니다. #3F6380(5.64:1) 이상으로 진하게 바꿔야 합니다. #5A6678/#fff는 5.82:1입니다.

### [낮음] 이미지 대체텍스트가 실제 이미지 내용과 다르거나 약어라 스크린리더 사용자에게 의미가 전달되지 않음
- 분류: 접근성 · 위치: `embeds/hearing-lab/html1.hearing-lab.html:566`, `embeds/hearing-lab/mobileHtml1.hearing-lab-mobile.html:88`
- 영향: 스크린리더 사용자는 소개 이미지를 'Hearing Lab'으로 잘못 듣고, 모바일에서는 'DC'라는 약어만 듣게 됩니다.
- 고치는 법: 566행 alt를 `한국인 청각 참조표준데이터센터 심볼(STANDARD 귀 모양 로고)`로, 모바일 88행 alt를 `청각참조표준데이터센터 로고`로 바꾸세요.

### [낮음] 제목 레벨이 h2에서 h4로 건너뛰어 스크린리더 목차 구조가 어긋남
- 분류: 접근성 · 위치: `embeds/hearing-lab/html1.hearing-lab.html:700-703`, `embeds/hearing-lab/html1.hearing-lab.html:968-971`, `embeds/hearing-lab/mobileHtml1.hearing-lab-mobile.html:116-123`, `embeds/hearing-lab/mobileHtml1.hearing-lab-mobile.html:129-131`, `embeds/hearing-lab/mobileHtml1.hearing-lab-mobile.html:323-325`
- 영향: 스크린리더로 제목 목록을 탐색하는 사용자에게 중간 단계가 빠진 구조로 들리고, 같은 항목이 데스크톱/모바일에서 다른 레벨로 들립니다.
- 고치는 법: Research Subjects 카드와 Alumni 카드의 h4, 모바일 dm-info의 h4를 h3로 바꾸고, 기존 h4 글자 크기는 CSS 클래스 선택자로 유지하세요.

### [낮음] 110px·70px로 표시되는 인물 사진에 1621×2000(277KB) 원본을 쓰는 등 이미지가 표시 크기보다 과도하게 큼
- 분류: 성능 · 위치: `embeds/hearing-lab/html1.hearing-lab.html:686`, `embeds/hearing-lab/html1.hearing-lab.html:675`, `embeds/hearing-lab/html1.hearing-lab.html:576-578`, `embeds/hearing-lab/html1.hearing-lab.html:566`, `embeds/hearing-lab/html1.hearing-lab.html:284-286`, `embeds/hearing-lab/mobileHtml1.hearing-lab-mobile.html:38`, `embeds/hearing-lab/mobileHtml1.hearing-lab-mobile.html:88`, `embeds/hearing-lab/mobileHtml1.hearing-lab-mobile.html:118` 외
- 영향: 모바일 데이터로 접속한 방문자가 70px 썸네일 2개를 위해 약 390KB를 내려받는 등 페이지 로딩이 불필요하게 느려집니다.
- 고치는 법: 인물 사진은 정사각형 240×240px(2배 해상도) JPEG 품질 80으로, 로고 PNG는 가로 840px로 줄여 imgur에 다시 올리고 src를 교체하세요(예상 합계 100KB 이하). 두 파일 모두 같은 URL을 쓰므로 한 번 교체하면 됩니다.

### [낮음] 데이터센터 영문 명칭이 로고·About 페이지와 다르고, 같은 상자 안에서도 국문 명칭이 두 가지로 쓰임
- 분류: 내용·데이터 · 위치: `embeds/hearing-lab/html1.hearing-lab.html:581-582`, `embeds/hearing-lab/html1.hearing-lab.html:586`, `embeds/about/html2.참조표준데이터센터.html:101`
- 영향: 방문자가 같은 기관의 공식 영문 명칭을 두 가지로 보게 되어 혼란스럽고, 검색·인용 시 명칭이 일관되지 않습니다.
- 고치는 법: 581행을 로고·About 페이지와 같은 `Korea Hearing Standard-data Center`로 바꾸고, 586행 `한국인 청각 데이터센터는`을 `한국인 청각 참조표준데이터센터는`으로 통일하세요.

### [낮음] 이미 끝난 TODO, 사실과 다른 주석, 쓰이지 않는 CSS(KOLAS 등)가 남아 있어 다음 수정자가 오해할 수 있음
- 분류: 유지보수 · 위치: `embeds/hearing-lab/html1.hearing-lab.html:159`, `embeds/hearing-lab/html1.hearing-lab.html:168`, `embeds/hearing-lab/html1.hearing-lab.html:204-226`, `embeds/hearing-lab/html1.hearing-lab.html:532-535`, `embeds/hearing-lab/html1.hearing-lab.html:554`, `embeds/hearing-lab/html1.hearing-lab.html:575`, `embeds/hearing-lab/html1.hearing-lab.html:626`, `embeds/hearing-lab/html1.hearing-lab.html:685` 외
- 영향: 방문자에게 보이지는 않지만, 다음에 코드를 고치는 사람이 '사진/조직도가 아직 미완성', 'KOLAS 박스가 빠졌다'고 오해해 불필요한 작업을 하거나 Audiso의 KOLAS 인증을 Hearing Lab에 잘못 추가할 위험이 있습니다.
- 고치는 법: 완료된 TODO(626, 685)와 KOLAS 관련 주석·CSS(159, 204-226, 532-535, 554)를 삭제하고 575행 주석을 '투명 배경'으로 고치세요. 미사용 CSS 블록(79-84, 143-154, 292-304, 474-481, 모바일 39·60·62)도 정리하세요.

### [낮음] 같은 논문 목록이 4개 파일에 손으로 복사되어 있고 모바일 개수(19편)와 데스크톱 max-height(3000px)가 하드코딩되어 추가 시 누락·잘림 위험
- 분류: 유지보수 · 위치: `embeds/hearing-lab/html1.hearing-lab.html:758-929`, `embeds/hearing-lab/mobileHtml1.hearing-lab-mobile.html:141-313`, `embeds/hearing-lab/html1.hearing-lab.html:383-385`, `embeds/research/html1.research.html:494-513`
- 영향: 논문을 추가할 때 4개 파일과 개수 문구를 모두 고치지 않으면 페이지마다 목록이 달라지고(이미 발생), 몇 편 더 추가되면 데스크톱 목록 하단이 max-height에 걸려 보이지 않게 됩니다.
- 고치는 법: 개수는 스크립트로 계산해 표시하세요(`document.querySelectorAll('#pub-list .pub-item').length`). max-height는 `max-height: none`(펼침 시 scrollHeight로 설정) 방식으로 바꾸세요. 장기적으로는 논문 데이터를 한 곳(예: Research 페이지 기준 JSON)에서 관리하고 data-team="hearing" 항목만 뽑아 쓰는 방식을 검토하세요.

#### 검증 단계에서 추가로 발견된 항목 (Hearing Lab)

검증 에이전트가 따로 보고한 것으로, 2차 검증은 거치지 않았습니다.

- [low] html1.hearing-lab.html:725-736: the '✏️ 논문 추가 방법' template comment tells maintainers to paste `<div class="pub-item" data-year="2025">` ... `<span class="pub-tag year">2025</span>` / `<span class="pub-tag journal">저널명</span>`. The template has no `data-team="hearing"`, no `<div class="pub-authors">` and no `pub-tag team-hearing` span. All 19 real entries (e.g. 759-766) have all three. Entries added by following the instructions will look different from the rest (no authors, no Hearing Lab tag), and will be missing if the data is later filtered by data-team as proposed in the Report and duplicated-data findings.
- [low, supports the bibliographic finding] Crossref author lists give the fix values: html1.hearing-lab.html:896 `Dong Su Jang, Dong Hyo Shin, Woojae Han, , YOUNG JOON SEO` should be 'Dong Su Jang, Dong Hyo Shin, Woojae Han, Tae Hoon Kong, Young Joon Seo'. Line 869 `HANJAEHYUN , TAEHUI KIM` should be 'Jaehyun Han, Tae Hui Kim'. Line 779's truncated list is really 15 authors ('... Wan-Ho Cho, Tae Hoon Kong, Soo Hee Oh, In-Ki Jin, Michelle J. Suh, Hyo-Jeong Lee, Seong Jun Choi, Dongchul Cha, Kyung-Ho Park, Young Joon Seo'). The same strings are at mobileHtml1.hearing-lab-mobile.html:280, 253 and 163.

## HeAD Lab

### [높음] Publication 아코디언을 펼치면 콘텐츠가 고정 iframe 높이를 크게 넘어서 목록 하단·Report·Alumni가 iframe 밖으로 밀려남 (데스크톱·모바일)
- 분류: Wix iframe · 위치: `embeds/head-lab/html1.head-lab.html:365-367`, `embeds/head-lab/html1.head-lab.html:735-739`, `embeds/head-lab/html1.head-lab.html:750-903`, `embeds/head-lab/mobileHtml1.head-lab-mobile.html:56`, `embeds/head-lab/mobileHtml1.head-lab-mobile.html:152-307`, `docs/site-map.md:26-27`
- 영향: 논문 목록을 연 방문자는 iframe 안에 별도 스크롤바가 생기거나(이중 스크롤) 목록 뒷부분·Report·Alumni가 잘려 보이지 않습니다. 데스크톱은 17편 중 앞 4~5편만 보이고, 모바일은 목록이 2,555px로 iframe(2,852px) 대부분을 넘어서 터치 스크롤이 iframe 안에 갇힙니다.
- 고치는 법: Wix iframe은 높이가 자동으로 늘지 않으므로 펼침 구조를 없애는 것이 안전합니다. (1) 최근 5편만 항상 보이게 하고 '전체 논문 보기' 링크를 `<a href="https://www.smilesnail.org/project" target="_top">`로 Research 페이지에 연결하거나, (2) 목록을 고정 높이 내부 스크롤 상자로 바꾸고(`#pub-list{max-height:480px;overflow-y:auto}` / 모바일 `#pub-body .collapse-inner{max-height:560px;overflow-y:auto}`) 아코디언을 기본 펼침으로 둔 뒤 에디터 높이를 그만큼(데스크톱 약 +560px, 모바일 약 +640px) 늘리세요. 어느 쪽이든 수정 후 펼친 상태 높이를 다시 측정해 에디터 높이와 맞추세요.
- 검증 메모: 세부 수치 정정: #pub-list 자체 높이는 1804px입니다(1877px은 연도 버튼을 포함한 #pub 본문 높이). Alumni top 5631은 Publication과 Report를 모두 펼쳤을 때 값이고, Publication만 펼치면 5514입니다. 모바일 문장은 '목록이 2,555px로 iframe(2,852px) 대부분을 넘어서'가 아니라 '펼치면 문서 높이가 2,784→5,338px로 늘어 iframe보다 약 2,486px 길어지고, 17편 중 2편만 완전히 보임'으로 고쳐야 합니다. 추가로, Report 아코디언 하나만 열어도 넘칩니다. Report는 데스크톱에서 +117px(6077−5960)라 4083+117≈4200>4097, 모바일에서 +97px(5435−5338)라 2784+97≈2881>2852입니다. 따라서 어느 아코디언이든 열기만 하면 스크롤바가 생기거나 하단(Alumni)이 잘립니다.

### [중간] 데스크톱 논문 목록에서 .pub-authors와 .pub-tag.team-head CSS가 없어 저자명이 제목보다 크게, 'HeAD Lab' 태그가 배경 없는 맨 글자로 표시됨
- 분류: 버그 · 위치: `embeds/head-lab/html1.head-lab.html:396-435`, `embeds/head-lab/html1.head-lab.html:753`, `embeds/head-lab/html1.head-lab.html:756`, `embeds/head-lab/mobileHtml1.head-lab-mobile.html:61`, `embeds/head-lab/mobileHtml1.head-lab-mobile.html:68`
- 영향: 데스크톱에서 Publication을 여는 모든 방문자에게 저자 줄(16px, 본문색)이 논문 제목(14.7px)보다 크게 보여 제목과 저자가 뒤바뀐 것처럼 읽히고, 'HeAD Lab' 태그만 테두리·배경 없이 떠 있는 글자로 보입니다.
- 고치는 법: 데스크톱 <style>에 추가: `.pub-authors{font-size:0.8rem;color:var(--text-mid);margin-bottom:5px}` 와 `.pub-tag.team-head{background:var(--accent-light);color:var(--accent-dark);border:1px solid var(--accent-border)}`.

### [중간] Report 섹션이 '연동 예정' 안내문뿐인 빈 자리이고, 데스크톱 연도 버튼 5개는 눌러도 아무 변화가 없음; 모바일 안내문은 내용이 다르고 링크도 없음
- 분류: 내용·데이터 · 위치: `embeds/head-lab/html1.head-lab.html:909-932`, `embeds/head-lab/html1.head-lab.html:980-990`, `embeds/head-lab/mobileHtml1.head-lab-mobile.html:308-311`
- 영향: Report를 연 방문자는 작동하지 않는 연도 버튼 6개와 '연동 예정'이라는 미완성 안내만 보게 됩니다. 데스크톱은 '예정', 모바일은 'Research 페이지에서 확인하세요'로 서로 모순되며, 모바일 안내에는 이동할 링크가 없습니다.
- 고치는 법: 데이터가 준비될 때까지 Report 아코디언과 연도 버튼을 삭제하거나, Research 페이지의 학회 발표(conf) 항목 중 HeAD Lab 항목을 `<div class="pub-item" data-year="…">` 형식으로 #report-list에 넣으세요. 안내문을 유지한다면 데스크톱·모바일 문구를 통일하고 `<a href="https://www.smilesnail.org/project" target="_top">Research 페이지</a>` 링크를 넣으세요(target="_top" 없으면 iframe 안에서 열림).
- 검증 메모: 제목은 '5개', 영향 설명은 '6개'로 서로 다릅니다. 내용이 바뀌지 않는 버튼은 '전체'를 포함해 6개입니다(누르면 강조 표시만 바뀜). 수정안도 고쳐야 합니다. Research 페이지의 Report 항목에는 data-team 속성이 없고(embeds/research/html1.research.html:1605 `<!-- Report은 팀별 필터 없음 (팀장님 지시) -->`, 1622 이후 항목은 `<div class="pub-item" data-year="2026">` 형식), 팀 필터도 없습니다. 그래서 'HeAD Lab 항목을 골라 옮긴다'는 수작업으로 팀을 지정해야 가능하고, 모바일 안내대로 Research 페이지에 가도 HeAD Lab 발표만 따로 볼 수 없습니다. 링크를 넣는다면 '전체 학회 발표 목록'으로 안내하는 것이 정확합니다.

### [중간] Publication 연도 필터의 '2026'과 '~2021' 버튼은 해당 논문이 0편이라 누르면 목록이 완전히 비고 안내 문구도 없음
- 분류: 버그 · 위치: `embeds/head-lab/html1.head-lab.html:743`, `embeds/head-lab/html1.head-lab.html:748`, `embeds/head-lab/html1.head-lab.html:973-991`
- 영향: 방문자가 2026 또는 ~2021을 누르면 빈 흰 상자만 남아 오류가 난 것처럼 보입니다.
- 고치는 법: 버튼을 실제 데이터 연도에서 자동 생성하거나(예: 스크립트로 `new Set([...items].map(i=>i.dataset.year))`로 버튼 생성), 0편인 2026/~2021 버튼을 삭제하세요. 필터 결과가 0이면 '해당 연도 논문이 없습니다' 문구를 표시하도록 filterYear에 처리 추가.

### [중간] 아코디언 헤더가 onclick만 있는 div라 키보드로 열 수 없고, 접힌 상태에서도 안쪽 연도 버튼 13개에 Tab 포커스가 들어감
- 분류: 접근성 · 위치: `embeds/head-lab/html1.head-lab.html:735`, `embeds/head-lab/html1.head-lab.html:911`, `embeds/head-lab/html1.head-lab.html:360-364`, `embeds/head-lab/html1.head-lab.html:742-748`, `embeds/head-lab/html1.head-lab.html:918-923`, `embeds/head-lab/mobileHtml1.head-lab-mobile.html:152`, `embeds/head-lab/mobileHtml1.head-lab-mobile.html:308`
- 영향: 키보드·스크린리더 사용자는 Publication/Report 목록을 열 수 없고, 반대로 보이지 않는 버튼 13개에 포커스가 들어가 현재 위치를 잃습니다. 스크린리더는 펼침 여부도 알 수 없습니다.
- 고치는 법: 헤더를 `<button type="button" class="collapse-header" aria-expanded="false" aria-controls="pub">`로 바꾸고 토글 함수에서 aria-expanded를 갱신하세요. 접힌 본문에는 `hidden` 속성 또는 `.collapse-body:not(.open){visibility:hidden}`을 적용해 안쪽 버튼이 포커스되지 않게 하세요. 화살표 span에는 aria-hidden="true".
- 검증 메모: 접힌 상태에서 포커스되는 버튼 13개는 데스크톱에만 해당합니다. 모바일에서는 헤더를 키보드로 열 수 없는 문제만 있습니다.

### [중간] 작은 글자 다수가 WCAG AA 대비 4.5:1 미달 (회색 #718096·#999, 하늘색 #4A90C4 조합)
- 분류: 접근성 · 위치: `embeds/head-lab/html1.head-lab.html:60-64`, `embeds/head-lab/html1.head-lab.html:73-76`, `embeds/head-lab/html1.head-lab.html:387-394`, `embeds/head-lab/html1.head-lab.html:926`, `embeds/head-lab/mobileHtml1.head-lab-mobile.html:19`, `embeds/head-lab/mobileHtml1.head-lab-mobile.html:61`, `embeds/head-lab/mobileHtml1.head-lab-mobile.html:63`, `embeds/head-lab/mobileHtml1.head-lab-mobile.html:68` 외
- 영향: 저시력·고령 방문자와 햇빛 아래 휴대폰 사용자는 히어로 부제, 모바일 저자명·졸업 정보·Director/Manager 배지·조직도의 HeAD Lab 상자, 선택된 연도 버튼 글자를 읽기 어렵습니다(모바일은 10~11px로 더 작음).
- 고치는 법: 보조 글자색을 #718096 → #4a5568(흰 배경 7.53:1)로, 연한 하늘 배경 위 글자 #4A90C4 → #2E6E9E(#EBF5FF 위 4.96:1)로, 하늘색 배경 위 흰 글자는 배경을 #2E6E9E(5.47:1)로, 안내문 #999 → #666(5.74:1)으로 바꾸세요. :root의 --text-light, --accent 값을 조정하면 데스크톱은 한 번에 반영됩니다.

### [중간] 모바일에서 히어로 문구·로고, HBDC 심볼 이미지, 빅데이터센터 설명 2문단과 5개 업무 목록, 논문 연도 필터가 빠져 있음
- 분류: 데스크톱·모바일 불일치 · 위치: `embeds/head-lab/html1.head-lab.html:520-527`, `embeds/head-lab/html1.head-lab.html:544-546`, `embeds/head-lab/html1.head-lab.html:559-569`, `embeds/head-lab/html1.head-lab.html:741-749`, `embeds/head-lab/mobileHtml1.head-lab-mobile.html:83-86`, `embeds/head-lab/mobileHtml1.head-lab-mobile.html:95-99`, `embeds/head-lab/mobileHtml1.head-lab-mobile.html:152-153`
- 영향: 모바일 방문자(대다수)는 빅데이터센터가 무엇을 하는지(PTA/ABR 표준화, 건보공단 데이터 연동, 데이터 제공·컨설팅 등)를 알 수 없고, 히어로 슬로건도 데스크톱과 다릅니다. 논문 17편을 연도로 좁힐 방법도 없습니다.
- 고치는 법: 모바일 DC 박스에 데스크톱의 두 문단(요약 가능)과 5개 `<ul>` 항목을 추가하고, 히어로에 동일 슬로건 '데이터로 소리를 이해하고, AI로 미래를 예측하다'와 로고 이미지를 넣으세요. 논문 목록은 연도 필터를 이식하거나 상단 finding의 '최근 5편 + 전체 보기 링크' 방식으로 통일하세요.
- 검증 메모: '모바일 방문자(대다수)'는 근거가 없는 추정이니 '대다수'를 빼세요. 로고 이미지는 모바일 h1 텍스트 'HeAD Lab'이 대신하므로 빠진 것은 이름이 아니라 부제 'RIHE Hearing AI & Data Lab'(이미지 속 글자), 슬로건, 환영 문구입니다.

### [중간] 90~110px(모바일 55~70px) 썸네일에 원본 크기 인물 사진을 그대로 써서 약 1.3MB를 내려받음, lazy 로딩도 없음
- 분류: 성능 · 위치: `embeds/head-lab/html1.head-lab.html:673`, `embeds/head-lab/html1.head-lab.html:683`, `embeds/head-lab/html1.head-lab.html:944`, `embeds/head-lab/html1.head-lab.html:949`, `embeds/head-lab/html1.head-lab.html:266-268`, `embeds/head-lab/html1.head-lab.html:456-458`, `embeds/head-lab/mobileHtml1.head-lab-mobile.html:41`, `embeds/head-lab/mobileHtml1.head-lab-mobile.html:72` 외
- 영향: 모바일 방문자는 55~70px 크기 사진 몇 장을 위해 1.3MB 이상을 받아 느린 망에서 페이지 표시가 늦어지고 데이터가 소모됩니다. 특히 이준헌 사진 1장이 683KB로 필요한 크기(2배 해상도 기준 180×180)의 약 8배입니다.
- 고치는 법: 인물 사진을 정사각형 240×240(약 15~25KB) JPEG/WebP로 잘라 다시 올리고 src를 교체하세요(imgur는 URL 끝에 's'/'m' 썸네일 접미사도 가능하나 원본을 줄여 올리는 편이 확실). 화면 아래쪽 Alumni·Director 사진에는 `loading="lazy" width="90" height="90"`을 추가하세요. 9cFssq8.png(2788×771, 표시 최대 380px)도 800px 폭으로 줄이면 됩니다.
- 검증 메모: '필요한 크기의 약 8배'는 가로 픽셀 기준(1570/180≈8.7배)입니다. 픽셀 수로는 약 100배, 바이트로는 적정 썸네일(약 8~25KB)의 27~80배이니 기준을 명시하세요. 수정안 보완: imgur 접미사를 실제로 확인했습니다. https://i.imgur.com/gQo7vUzb.jpeg 는 160×160 정사각형 8,267B, 'm'은 241×320 25,906B, 's'는 90×90 3,712B입니다. 90~110px 표시(2배 해상도)에는 'b'(160×160)가 가장 간단한 즉시 해결책이고, 's'는 2배 해상도에서 흐립니다.

### [낮음] 데스크톱과 모바일의 조직도 순서·명칭, 소장 소속, 섹션 제목, 논문 편수 표기가 서로 다름
- 분류: 데스크톱·모바일 불일치 · 위치: `embeds/head-lab/html1.head-lab.html:536`, `embeds/head-lab/html1.head-lab.html:632-656`, `embeds/head-lab/html1.head-lab.html:677`, `embeds/head-lab/html1.head-lab.html:736`, `embeds/head-lab/html1.head-lab.html:946-956`, `embeds/head-lab/mobileHtml1.head-lab-mobile.html:90`, `embeds/head-lab/mobileHtml1.head-lab-mobile.html:113-120`, `embeds/head-lab/mobileHtml1.head-lab-mobile.html:128` 외
- 영향: 같은 페이지를 기기에 따라 다른 조직 구조 순서(Audiso 위치), 다른 소속 표기(연세대학교 누락)로 보게 되어 공식 정보처럼 보이는 내용이 일관되지 않습니다.
- 고치는 법: 조직도 하위 상자 순서와 명칭(Audiso Co., Ltd. / 상위 기관 전체 명칭)을 한쪽 기준으로 통일하고, 모바일 소장 소속에 '연세대학교'를 추가하세요. 논문 편수는 양쪽 모두 표시하거나 모두 빼고, 날짜 표기 형식도 하나로 맞추세요.
- 검증 메모: 영향 설명 중 '공식 정보처럼 보이는 내용이 일관되지 않습니다'는 과장입니다. 약칭·순서 차이일 뿐 사실 오류는 없습니다.

### [낮음] 저자 목록 5건이 이름 중간에서 '...'로 잘려 있고, 여러 건은 이름 형식이 뒤섞여 있음
- 분류: 내용·데이터 · 위치: `embeds/head-lab/html1.head-lab.html:780`, `embeds/head-lab/html1.head-lab.html:789`, `embeds/head-lab/html1.head-lab.html:798`, `embeds/head-lab/html1.head-lab.html:807`, `embeds/head-lab/html1.head-lab.html:852`, `embeds/head-lab/html1.head-lab.html:870`, `embeds/head-lab/html1.head-lab.html:888`, `embeds/head-lab/html1.head-lab.html:897` 외
- 영향: 방문자에게 'S...', 'P...', 'Ko...'처럼 잘린 이름이 그대로 보여 데이터 추출 과정의 흔적이 노출되고, 일부 저자가 누락되거나 다른 사람처럼 읽힙니다.
- 고치는 법: 각 논문의 전체 저자 목록을 원문(DOI/학술DB)에서 다시 복사하거나, 길면 '제1저자 외 N명' 형식으로 명시적으로 줄이세요. 이름 표기를 'Yoon CY'나 'Chul Young Yoon' 등 한 형식으로 통일하고 한글 이름은 영문으로 바꾸세요. 데스크톱·모바일 두 파일 모두 수정 필요.

### [낮음] 같은 학술지가 서로 다른 이름으로 표기되고, 연작 논문 Part 2가 Part 1보다 먼저 나옴
- 분류: 내용·데이터 · 위치: `embeds/head-lab/html1.head-lab.html:788`, `embeds/head-lab/html1.head-lab.html:793`, `embeds/head-lab/html1.head-lab.html:806`, `embeds/head-lab/html1.head-lab.html:811`, `embeds/head-lab/html1.head-lab.html:829`, `embeds/head-lab/html1.head-lab.html:838`, `embeds/head-lab/html1.head-lab.html:892`, `embeds/head-lab/mobileHtml1.head-lab-mobile.html:196` 외
- 영향: 목록이 정리되지 않은 인상을 주고, 같은 학술지를 다른 곳으로 오인할 수 있습니다.
- 고치는 법: 학술지명을 공식 표기(PLOS ONE, Hearing Research, European Archives of Oto-Rhino-Laryngology, Nutrients, Korean Journal of Otorhinolaryngology-Head and Neck Surgery)로 통일하고, Part 1을 Part 2 위로 옮기세요. 두 파일 모두 수정.

### [낮음] Alumni 학과명 표기 불일치('의료정보통계학' vs '의료정보통계학과')와 졸업연도 순서 뒤섞임
- 분류: 내용·데이터 · 위치: `embeds/head-lab/html1.head-lab.html:943-957`, `embeds/head-lab/mobileHtml1.head-lab-mobile.html:318-320`
- 영향: 한 명만 학과명이 다르게 보이고, 졸업 순서가 최신순도 오래된순도 아니어서 오타·정리 누락으로 보입니다.
- 고치는 법: 이주형 항목을 '의료정보통계학과 석사'로 고치고, 카드 순서를 졸업 최신순(이준헌 2026 → 김지원 2025 → 이주형 2023)으로 두 파일 모두 정렬하세요.

### [낮음] 데스크톱에 h1이 없고(제목이 이미지 안에만 있음) h2 다음 바로 h4로 건너뛰며, 일부 이미지 대체텍스트가 부실함
- 분류: 접근성 · 위치: `embeds/head-lab/html1.head-lab.html:520-527`, `embeds/head-lab/html1.head-lab.html:545`, `embeds/head-lab/html1.head-lab.html:697-721`, `embeds/head-lab/html1.head-lab.html:941-955`, `embeds/head-lab/mobileHtml1.head-lab-mobile.html:96`, `embeds/head-lab/mobileHtml1.head-lab-mobile.html:125-132`, `embeds/head-lab/mobileHtml1.head-lab-mobile.html:138-145`, `embeds/head-lab/mobileHtml1.head-lab-mobile.html:316-320`
- 영향: 스크린리더 사용자는 데스크톱에서 페이지 대제목을 찾을 수 없고 제목 탐색 시 단계가 끊겨 구조 파악이 어렵습니다. 'HBDC Symbol', '빅데이터DC'는 의미를 전달하지 못합니다.
- 고치는 법: 데스크톱 로고 이미지를 `<h1><img … alt="HeAD Lab – RIHE Hearing AI & Data Lab"></h1>`로 감싸세요. rs-card·alumni·dm-info의 h4를 h3로 바꾸고(스타일은 클래스 기준이라 영향 적음), alt를 '청각빅데이터센터 심볼'(장식이면 alt=""), 모바일 '청각빅데이터센터 로고'로 통일하세요.

### [낮음] 논문 17편 목록이 데스크톱·모바일(및 Research 페이지)에 수작업 복제되어 있고, 모바일에만 편수 '(17편)'이 하드코딩됨
- 분류: 유지보수 · 위치: `embeds/head-lab/html1.head-lab.html:736`, `embeds/head-lab/html1.head-lab.html:750-903`, `embeds/head-lab/mobileHtml1.head-lab-mobile.html:152-306`
- 영향: 새 논문을 추가할 때 최소 4곳(head-lab 2개, research 2개)을 고치고 모바일 편수 숫자도 손으로 바꿔야 해서, 한 곳이라도 빠지면 기기·페이지별 목록과 편수가 어긋납니다.
- 고치는 법: 편수는 스크립트로 계산해 표시하세요: `document.querySelector('#pub-arrow').previousElementSibling.textContent = '📄 Publication (' + document.querySelectorAll('#pub-body .pub-item').length + '편)'`. 목록 자체는 docs/에 단일 원본(JSON 등)을 두고 4개 임베드를 생성하는 스크립트로 관리하는 것을 권장.

### [낮음] 사용되지 않는 CSS·주석 처리된 영상 자리표시자·미사용 폰트 정의가 남아 있음
- 분류: 유지보수 · 위치: `embeds/head-lab/html1.head-lab.html:137-148`, `embeds/head-lab/html1.head-lab.html:192-208`, `embeds/head-lab/html1.head-lab.html:274-286`, `embeds/head-lab/html1.head-lab.html:408-411`, `embeds/head-lab/html1.head-lab.html:431-435`, `embeds/head-lab/html1.head-lab.html:589-594`, `embeds/head-lab/mobileHtml1.head-lab-mobile.html:10-16`, `embeds/head-lab/mobileHtml1.head-lab-mobile.html:42` 외
- 영향: 방문자에게 직접 보이진 않지만, 다른 랩 페이지에서 복사하면서 남은 코드가 섞여 있어 실제로 필요한 스타일이 빠진 것(데스크톱 저자·태그)을 알아채기 어렵게 만들었습니다.
- 고치는 법: 미사용 규칙과 영상 주석 블록을 삭제하거나, 영상 계획이 있으면 실제 영상 ID로 활성화하세요. 모바일 body 글꼴을 데스크톱과 같이 `'EngSerif', Pretendard, sans-serif`로 바꾸거나 @font-face를 삭제하세요.

#### 검증 단계에서 추가로 발견된 항목 (HeAD Lab)

검증 에이전트가 따로 보고한 것으로, 2차 검증은 거치지 않았습니다.

- [low] 데스크톱 연구주제·졸업생 카드의 마우스 오버 효과가 작동하지 않음. 원인: embeds/head-lab/html1.head-lab.html:320-323 `.rs-card:hover { transform: translateY(-2px);`와 453-455 `.alumni-card:hover { transform: translateY(-2px); }`는 481-484 `.fade.show { opacity: 1; transform: translateY(0); }`와 명시도가 같고(0,2,0) 더 앞에 있어서 덮어써집니다. 또 476-480 `.fade`의 `transition: opacity 0.6s ease, transform 0.6s ease;`가 318 `.rs-card`의 transition을 대체합니다. 700·944줄 카드는 모두 `class="rs-card fade"` / `class="alumni-card fade"`입니다. 1280px 렌더링에서 hover 뒤 computed transform은 rs-card와 alumni-card 모두 matrix(1,0,0,1,0,0)였습니다. 해결: `.fade.show.rs-card:hover, .fade.show.alumni-card:hover{transform:translateY(-2px)}`처럼 명시도를 올리거나, 둘 중 한쪽 효과를 삭제하세요.
- [high, 첫 finding에 포함할 내용] Publication뿐 아니라 Report 아코디언만 열어도 iframe을 넘칩니다. 데스크톱 Report 본문은 +117px(measure-summary contentHeightAllExpanded 6077 − 직접 측정한 Publication만 펼친 높이 5960)라 4083+117≈4200 > 에디터 높이 4097이고, 모바일은 +97px(5435−5338)라 2784+97≈2881 > 2852입니다. 원인 코드: html1.head-lab.html:911 `<div class="collapse-header" onclick="toggleCollapse('report')">`, mobileHtml1.head-lab-mobile.html:308 `<div class="collapse-header" onclick="toggle('report')">`. 즉 '연동 예정' 안내문만 보려고 열어도 Alumni 하단이 잘리거나 iframe 스크롤바가 생깁니다.

## Audiso

### [중간] 모바일에는 소개 문장 일부, 강점 및 제품 설명이 빠졌고 책 제목과 제품 효능 표현이 데스크톱과 다름
- 분류: 데스크톱·모바일 불일치 · 위치: `embeds/audiso/html1.audiso.html:401`, `embeds/audiso/mobileHtml1.audiso-mobile.html:114`, `embeds/audiso/html1.audiso.html:417-446`, `embeds/audiso/mobileHtml1.audiso-mobile.html:122-127`, `embeds/audiso/html1.audiso.html:519-582`, `embeds/audiso/mobileHtml1.audiso-mobile.html:152-157`, `embeds/audiso/html1.audiso.html:573`, `embeds/audiso/html1.audiso.html:492` 외
- 영향: 모바일 방문자는 데스크톱과 다른 정보를 봅니다. 책 제목이 '디지털 치료제'로 잘려 실제 서명(『의사가 알려주는 디지털 치료제』)과 달라지고, 건강기능식품 '피스탑 트리플케어'는 모바일에서만 '이명 관리'라는 효능 표현이 붙어 두 버전의 표시 내용이 서로 어긋납니다.
- 고치는 법: 모바일 제품 카드에 정식 책 제목 '의사가 알려주는 디지털 치료제'를 쓰세요. 피스탑 설명은 허용된 기능성 표현 하나로 정해 두 파일에 똑같이 넣으세요('이명 관리'를 쓸 수 있는 표현인지 먼저 확인 필요). 소개 문단 마지막 문장과 강점 카드의 '원주세브란스기독병원 이비인후과 교수' 정보는 모바일에도 넣으세요. 넣은 뒤 모바일 높이(현재 2722, 여유 5px)를 다시 재고 #mobileHtml1 높이를 조정하세요.
- 검증 메모: 근거 보강: 사이트의 다른 곳(embeds/home/mobileHtml1.home.html:66 "<h3>의사가 알려주는 디지털 치료제</h3>")은 정식 서명을 쓰므로, audiso 모바일 156행만 서명이 다릅니다.

### [중간] 대표 버튼, 슬로건, 히어로 부제 글자의 명암 대비가 WCAG AA 기준(4.5:1)에 못 미침
- 분류: 접근성 · 위치: `embeds/audiso/html1.audiso.html:25`, `embeds/audiso/html1.audiso.html:78-92`, `embeds/audiso/html1.audiso.html:143-148`, `embeds/audiso/html1.audiso.html:31`, `embeds/audiso/html1.audiso.html:59-76`, `embeds/audiso/html1.audiso.html:483-486`, `embeds/audiso/mobileHtml1.audiso-mobile.html:20`, `embeds/audiso/mobileHtml1.audiso-mobile.html:22` 외
- 영향: 저시력 방문자나 밝은 곳에서 휴대폰을 보는 방문자는 노란 대표 버튼의 흰 글자와 'Audiology with ISO!' 슬로건을 읽기 어렵습니다. 모두 일반 크기 글자라 AA 기준 4.5:1을 넘어야 하는데 2.38:1밖에 되지 않습니다.
- 고치는 법: 히어로 버튼은 하단 xr 버튼처럼 배경 #1a1a1a에 글자 #D4A017(7.33:1)로 바꾸거나, 흰 글자를 유지하려면 배경을 #8A6508 정도로 어둡게 하세요. 슬로건 글자색은 #8A6508 이상으로 어둡게 하고, #718096은 #4a5568(7.53:1)로 바꾸세요. 조직도 화살표는 #767676 이상으로 하세요.
- 검증 메모: 사소한 보정: 조직도 화살표(↓, 22.4px, 일반 굵기)는 글자이므로 엄밀히는 비텍스트 3:1이 아니라 텍스트 4.5:1 기준이 적용되며, 어느 기준으로도 미달입니다.

### [낮음] 데스크톱 iframe 여유 높이가 4px뿐이고, 폭 1024px 전후에서는 내용이 에디터 높이보다 20px 길어짐
- 분류: Wix iframe · 위치: `docs/site-map.md:28`, `embeds/audiso/html1.audiso.html:536`
- 영향: 브라우저 폭이 약 980~1029px인 방문자(1024px 모니터나 창, 1280px 화면을 125%로 확대한 노트북, iPad 가로 모드처럼 데스크톱 레이아웃이 뜨는 태블릿)는 iframe 안에 세로 스크롤바가 생기거나 하단 20px이 잘립니다. 다른 폭에서도 여유가 4px뿐이라 문구를 한 줄만 늘려도 바로 잘립니다.
- 고치는 법: Wix 에디터에서 #html1 높이를 3077에서 3130px 안팎으로 늘려 줄바꿈 한 두 줄 분량의 여유를 두세요. 또는 536행의 설명을 줄여 3줄에 맞추세요. 문구나 word-break 설정을 바꾼 뒤에는 폭 980, 1024, 1280에서 높이를 다시 재세요.
- 검증 메모: 영향 수정: 넘치는 20px은 마지막 섹션의 하단 여백(padding 60px)뿐입니다. 1024px에서 마지막 버튼(588행 xr 바로가기)의 하단은 y=3037로 에디터 높이 3077 안에 있으므로 잘리는 글자나 버튼은 없습니다. 실제 증상은 Windows 등 일반 스크롤바를 쓰는 환경에서 폭 약 980~1029px(창 폭 약 1000~1046px)일 때 iframe 안에 불필요한 세로 스크롤바가 생기고 마우스 휠이 잠깐 iframe에 걸리는 정도입니다. iPad는 오버레이 스크롤바라 보이지 않습니다. 수정 방법(#html1 높이를 약 3130px로 늘리기)은 그대로 유효합니다.

### [낮음] 서브셋 없는 Pretendard 전체 폰트를 불러와 첫 방문 시 폰트만 데스크톱 약 3.1MB, 모바일 약 2.3MB를 받음
- 분류: 성능 · 위치: `embeds/audiso/html1.audiso.html:10`, `embeds/audiso/html1.audiso.html:11`, `embeds/audiso/mobileHtml1.audiso-mobile.html:6`, `embeds/audiso/mobileHtml1.audiso-mobile.html:7`, `embeds/audiso/mobileHtml1.audiso-mobile.html:19`
- 영향: 휴대폰 데이터로 처음 들어온 방문자는 폰트 2.3MB를 다 받을 때까지 글꼴이 바뀌거나 늦게 표시됩니다. 사이트의 다른 iframe도 같은 파일을 쓰므로 한 번 받으면 캐시되지만, 첫 페이지는 눈에 띄게 느립니다.
- 고치는 법: 두 파일의 Pretendard 링크를 https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css 로 바꾸고 font-family를 'Pretendard Variable'로 바꾸세요. 그러면 실제 쓰는 글자 묶음만 내려받습니다. 모바일 7행의 Playfair Display 링크와 19행의 .hero h1 규칙은 지우세요.
- 검증 메모: 수치 보정: Times New Roman이 설치된 Windows/macOS 데스크톱에서는 SemiBold가 필요 없어(600 굵기 글자는 영문뿐이라 TNR로 표시됨) Regular, Medium, Bold 3개 약 2.34MB를 받습니다. 3.1MB는 TNR이 없는 환경(리눅스 등)에서만 해당합니다. 모바일 2.34MB는 맞습니다. font-display:swap이라 글자는 대체 글꼴로 바로 보이고 나중에 바뀝니다(깜빡임).

### [낮음] KOLAS 마크 PNG가 886×529px, 384KB인데 화면에는 80×48px(모바일 50×30px)로만 표시됨
- 분류: 성능 · 위치: `embeds/audiso/html1.audiso.html:407`, `embeds/audiso/html1.audiso.html:190-194`, `embeds/audiso/mobileHtml1.audiso-mobile.html:117`, `embeds/audiso/mobileHtml1.audiso-mobile.html:80`, `embeds/audiso/html1.audiso.html:381`
- 영향: 작은 아이콘 하나 때문에 모바일 방문자도 384KB를 내려받습니다. 표시 크기의 10배가 넘는 해상도입니다.
- 고치는 법: KOLAS 마크를 가로 160px(2배 해상도)로 줄이고 WebP나 압축 PNG로 다시 올려 약 10KB 수준으로 만든 뒤 src를 바꾸세요. 로고도 가로 720px로 줄이면 됩니다.

### [낮음] 제품 카드의 마우스 오버 떠오름 효과가 .fade.show 규칙에 덮여 작동하지 않음
- 분류: 버그 · 위치: `embeds/audiso/html1.audiso.html:287-292`, `embeds/audiso/html1.audiso.html:333-341`, `embeds/audiso/html1.audiso.html:519`
- 영향: 제품 카드 6개에 마우스를 올려도 의도한 3px 떠오름이 없고 그림자만 갑자기 나타납니다. 강점 카드와 반응이 달라 보입니다.
- 고치는 법: '.product-card.fade.show:hover { transform: translateY(-3px); }'를 추가하고 '.product-card.fade { transition: opacity .6s ease, transform .2s, box-shadow .2s; }'로 transition을 합치세요. 또는 fade 클래스를 카드를 감싸는 요소로 옮기세요.
- 검증 메모: 수정안 보정: '.product-card.fade { transition: ... transform .2s ...}'로 바꾸면 페이드인 슬라이드도 0.2s로 빨라집니다. fade 클래스를 카드를 감싸는 별도 div로 옮기는 두 번째 방법을 권장하세요. 강점 카드도 그림자 전환이 없으므로 두 카드의 차이는 떠오름 효과 유무뿐입니다.

### [낮음] word-break: keep-all이 없어 한글 단어가 줄 끝에서 음절 단위로 끊김 ('전문|의', '시스|템' 등)
- 분류: 접근성 · 위치: `embeds/audiso/html1.audiso.html:43-48`, `embeds/audiso/mobileHtml1.audiso-mobile.html:17`, `embeds/audiso/mobileHtml1.audiso-mobile.html:122-127`, `embeds/audiso/html1.audiso.html:420`, `embeds/audiso/html1.audiso.html:435`
- 영향: '현직 이비인후과 전문' 다음 줄에 '의'만 남는 식으로 단어가 쪼개져 읽기 불편하고, 모바일의 좁은 카드에서 특히 자주 보입니다.
- 고치는 법: 두 파일의 body에 'word-break: keep-all; overflow-wrap: anywhere;'를 추가하세요. 줄바꿈이 달라져 높이가 늘 수 있으니 적용한 뒤 데스크톱(980, 1024, 1280)과 모바일(320) 높이를 다시 재고 Wix 에디터 높이를 맞추세요. 현재 여유는 4~5px뿐입니다.
- 검증 메모: 개수는 글꼴에 따라 달라집니다(TNR 대체 글꼴 기준 모바일 15곳, 데스크톱 12곳). 예시는 재현됩니다.

### [낮음] 두 embed 모두 h1이 없어 문서 제목 구조가 h2부터 시작함
- 분류: 접근성 · 위치: `embeds/audiso/html1.audiso.html:379-384`, `embeds/audiso/mobileHtml1.audiso-mobile.html:19`, `embeds/audiso/mobileHtml1.audiso-mobile.html:101-106`
- 영향: 스크린리더 사용자가 제목(heading) 단위로 이동하면 페이지 제목 없이 'Audiso 소개'(h2)부터 시작해 이 페이지가 무엇에 관한 것인지 바로 알기 어렵습니다.
- 고치는 법: 히어로에 시각적으로 숨긴 <h1>Audiso (주)오디에스오</h1>을 넣거나 로고 이미지를 <h1>로 감싸세요. 모바일은 이미 정의된 .hero h1 스타일을 활용하면 됩니다.

### [낮음] 모바일 이미지 alt가 영문 약어로 되어 있고, 장식용 이모지 아이콘이 스크린리더에 읽힘
- 분류: 접근성 · 위치: `embeds/audiso/mobileHtml1.audiso-mobile.html:103`, `embeds/audiso/mobileHtml1.audiso-mobile.html:117`, `embeds/audiso/mobileHtml1.audiso-mobile.html:153-157`, `embeds/audiso/html1.audiso.html:418`, `embeds/audiso/html1.audiso.html:423`, `embeds/audiso/html1.audiso.html:428`, `embeds/audiso/html1.audiso.html:433`, `embeds/audiso/html1.audiso.html:438` 외
- 영향: 모바일 스크린리더 사용자는 'VR Sim', 'VR DTx' 같은 뜻이 불분명한 약어를 듣고, 강점 카드마다 '청진기', '자동차' 같은 이모지 이름을 먼저 듣게 됩니다.
- 고치는 법: 모바일 alt를 데스크톱과 같은 한국어로 맞추세요. 제품명이 바로 아래 h3에 있으므로 제품 이미지는 alt=""로 두는 방법도 있습니다. 이모지 div에는 aria-hidden="true"를 추가하세요.
- 검증 메모: 로고의 alt="Audiso"는 회사명이라 큰 문제는 아닙니다. 핵심은 'VR Sim', 'VR DTx' 같은 약어와 이모지 읽힘입니다.

### [낮음] KOLAS 관련 표현에 '인증'과 '인정'이 섞여 있음
- 분류: 내용·데이터 · 위치: `embeds/audiso/html1.audiso.html:380`, `embeds/audiso/html1.audiso.html:407`, `embeds/audiso/html1.audiso.html:409-410`, `embeds/audiso/mobileHtml1.audiso-mobile.html:102`, `embeds/audiso/mobileHtml1.audiso-mobile.html:118`
- 영향: 같은 박스 안에서 '인증'과 '인정'이 번갈아 나와 혼란스럽습니다. 교정기관 입장에서는 KOLAS '인정(accreditation)'을 제품 '인증(certification)'과 구분하는 것이 공식 표현입니다.
- 고치는 법: KOLAS에 관한 표현은 '인정'으로 통일하세요. 예: '청력계 KOLAS 인정 교정기관', 'KOLAS 국제공인교정기관 인정 (KC24-437)', alt 'KOLAS 인정마크 KC24-437'. 모바일도 똑같이 고치세요.

### [낮음] 맞춤법과 띄어쓰기 오류 및 병원명 표기 불일치
- 분류: 내용·데이터 · 위치: `embeds/audiso/html1.audiso.html:401`, `embeds/audiso/html1.audiso.html:410`, `embeds/audiso/html1.audiso.html:425`, `embeds/audiso/html1.audiso.html:420`, `embeds/audiso/mobileHtml1.audiso-mobile.html:118`
- 영향: 방문자가 보는 공식 소개 문구에 맞춤법 오류와 병원명 표기 차이가 있습니다.
- 고치는 법: '해 나가겠습니다', '청각 관련', '인정받았습니다'로 고치고, 병원명은 '원주세브란스기독병원'으로 통일하세요.
- 검증 메모: 추가: 같은 401행의 '교정 받는'도 '교정받는'으로 붙여 쓰세요.

### [낮음] 제품 목록이 '근거'로 적힌 xr.audiso.co.kr의 현재 주요 제품과 다름 (마인드톤 없음, 모두의 보청기 설명 불일치)
- 분류: 내용·데이터 · 위치: `embeds/audiso/html1.audiso.html:509-513`, `embeds/audiso/html1.audiso.html:551-560`, `embeds/audiso/mobileHtml1.audiso-mobile.html:152-157`
- 영향: 방문자가 하단의 'xr.audiso.co.kr 바로가기'를 누르면 이 페이지와 다른 제품 구성과 설명을 보게 됩니다.
- 고치는 법: 오디에스오에 현재 공식 제품 목록을 확인해 마인드톤을 넣을지와 모두의 보청기 설명을 정한 뒤, 데스크톱과 모바일 두 파일에 똑같이 반영하세요.

### [낮음] 모바일 파일에 다른 페이지에서 복사해 온 미사용 CSS 23개와 효과 없는 @font-face가 남아 있고, 주석이 실제 코드와 다름
- 분류: 유지보수 · 위치: `embeds/audiso/mobileHtml1.audiso-mobile.html:11-17`, `embeds/audiso/mobileHtml1.audiso-mobile.html:21`, `embeds/audiso/mobileHtml1.audiso-mobile.html:77`, `embeds/audiso/mobileHtml1.audiso-mobile.html:29-74`, `embeds/audiso/html1.audiso.html:130-175`, `embeds/audiso/html1.audiso.html:376-377`, `embeds/audiso/html1.audiso.html:389`, `embeds/audiso/html1.audiso.html:512`
- 영향: 방문자에게 바로 보이지는 않지만, 수정할 때 어떤 규칙이 실제로 적용되는지 헷갈립니다. 예를 들어 모바일의 EngSerif나 21행 .hero-logo를 고쳐도 화면이 바뀌지 않습니다. 주석을 믿고 링크를 점검하면 잘못된 주소를 놓칠 수 있습니다.
- 고치는 법: 모바일 29~74행의 미사용 규칙과 21행 .hero-logo를 지우고, body 글꼴을 "'EngSerif', Pretendard, sans-serif"로 바꿔 데스크톱과 맞추세요. 데스크톱 130~175행의 미사용 규칙을 정리하고 주석을 실제 링크에 맞게 고치세요.
- 검증 메모: 수정안 보정: 모바일 21행은 지우지 말고 77행의 max-width:240px;width:70%를 21행에 합친 뒤 77행을 지우세요(21행의 margin:8px auto;display:block은 실제로 적용 중입니다). 지워도 되는 범위는 모바일 29~40행과 50~74행, 데스크톱 130~134행과 150~175행입니다. 모바일 41~49행(.mv-card, .org-*)과 데스크톱 135~149행(.about-text, .slogan)은 사용 중이므로 남겨야 합니다.

#### 검증 단계에서 추가로 발견된 항목 (Audiso)

검증 에이전트가 따로 보고한 것으로, 2차 검증은 거치지 않았습니다.

- [medium] 이미지 8개가 모두 i.imgur.com에 올라가 있는데, imgur는 영국 접속을 막고 있어 영국 방문자에게는 로고, KOLAS 마크, 제품 사진이 모두 표시되지 않습니다. 증거: check-host.net에서 https://i.imgur.com/Ycn67aA.png 를 확인한 결과 uk1 노드는 "Content not available in your country", de2/jp1/us1 노드는 "OK"였습니다. 위치: embeds/audiso/html1.audiso.html:381 <img src="https://i.imgur.com/lQwB2st.jpeg" ...>, 407 "https://i.imgur.com/Ycn67aA.png", 521, 532, 543, 554, 565, 576; embeds/audiso/mobileHtml1.audiso-mobile.html:103, 117, 152-157. 수정: 이미지를 Wix 미디어(static.wixstatic.com)로 옮겨 src를 바꾸세요. 사이트 전체의 imgur 이미지에 같은 문제가 있습니다.
- [low] 데스크톱 전용 iframe의 반응형 규칙은 적용될 일이 없는 죽은 코드입니다. 증거: html1.audiso.html:346 "@media (max-width: 768px) {"와 365 "@media (max-width: 480px) {". 데스크톱 요소는 docked 전체 폭이고 Wix 클래식 사이트 최소 폭은 980px이므로 이 조건은 절대 참이 되지 않습니다. 모바일은 별도 파일(mobileHtml1)을 씁니다. 결과: 이 규칙을 고쳐도 모바일 화면은 바뀌지 않습니다.

## Contact

### [높음] 연락처 페이지의 브라우저 탭·검색결과·공유 제목이 Wix 템플릿 문구 '문의 | BUSINESS NAME'으로 게시되어 있음
- 분류: 내용·데이터 · 위치: `(측정 결과):187`, `(측정 결과):189`, `(측정 결과):200`, `(Wix 페이지 데이터):1`
- 영향: 모든 방문자의 브라우저 탭, 구글·네이버 검색결과 제목, 카카오톡·페이스북 공유 미리보기에 'BUSINESS NAME'이라는 템플릿 자리표시 문구가 그대로 보입니다. SEO 설명도 비어 있고 본문 연락처는 iframe 안에만 있어서, 검색결과 요약에 주소나 이메일이 나오지 않습니다.
- 고치는 법: Wix 에디터 → 페이지 메뉴 → Contact 페이지 ⋯ → SEO 기본에서 '검색 결과 제목'을 예: '연락처 | 청각재활연구소'로 바꾸고, '검색 결과 설명'에 '연세대학교 원주세브란스기독병원 의학관 318호, (26426) 강원특별자치도 원주시 일산로 20, okas2000@yonsei.ac.kr' 같은 문구를 넣은 뒤 게시하세요. 다른 페이지 SEO 제목에도 'BUSINESS NAME'이 남아 있는지 함께 확인하세요.
- 검증 메모: Two corrections to the evidence. (1) '의학관' does appear once in the published HTML: the Wix business info JSON has `"businesLocationsDescription":"의학관 4층 기능연구실"`. So '의학관 0건' is wrong; it is still true that none of the contact content shown to visitors is in the HTML. (2) 'BUSINESS NAME' is not only on this page. masterPage.json has page u1adb with `"pageTitleSEO":"Data center for Korean reference hearing | BUSINESS NAME","pageUriSEO":"datacenter","hidePage":true,..."indexable":true`. curl https://www.smilesnail.org/datacenter returns 200 with `<title>Data center for Korean reference hearing | BUSINESS NAME</title>`, and pages-sitemap.xml lists `<loc>https://www.smilesnail.org/datacenter</loc>`. The fix should name that page too, not just say 'check other pages'.

### [중간] Wix 비즈니스 정보와 구조화 데이터의 주소(4층 기능연구실, 우편번호 220-050, 강원도)가 연락처 페이지(318호, 26426, 강원특별자치도)와 다름
- 분류: 내용·데이터 · 위치: `(측정 결과):445`, `(게시된 페이지 HTML):200`, `embeds/contact/html1.contact-info.html:155-157`, `embeds/contact/mobileHtml1.contact.html:54-55`
- 영향: 검색엔진이 받는 공식 주소 데이터에는 2015년에 폐지된 6자리 우편번호 220-050과 옛 이름 '강원도'가 들어 있고 도로명(streetAddress)은 빠져 있습니다. 상세 위치도 '의학관 4층 기능연구실'과 '의학관 318호'(3층)로 달라서, 방문자나 검색엔진은 어느 쪽이 맞는지 알 수 없습니다.
- 고치는 법: 먼저 실제 연구소 위치(318호인지 4층 기능연구실인지)를 확인하세요. 그다음 Wix 대시보드 → 설정 → 비즈니스 정보에서 주소를 '강원특별자치도 원주시 일산로 20', 우편번호 '26426', 상세 위치를 실제 호실로 바꾸고, 연락처 임베드 두 파일(html1, mobileHtml1)도 같은 값으로 맞추세요.
- 검증 메모: '318호 = 3층' is an inference from the room number, not verified. It does not change the finding.

### [중간] 우편번호·주소, 연구소장 표기 등 작은 회색 글자(#718096)의 명도 대비가 4.02:1로 WCAG AA(4.5:1) 미달
- 분류: 접근성 · 위치: `embeds/contact/html1.contact-info.html:29`, `embeds/contact/html1.contact-info.html:34`, `embeds/contact/html1.contact-info.html:123`, `embeds/contact/html1.contact-info.html:156`, `embeds/contact/html1.contact-info.html:163`, `embeds/contact/mobileHtml1.contact.html:20`, `embeds/contact/mobileHtml1.contact.html:37`, `embeds/contact/mobileHtml1.contact.html:55` 외
- 영향: 저시력 사용자나 햇빛 아래 휴대폰으로 보는 사용자는 이 페이지에서 가장 중요한 정보인 도로명 주소·우편번호와 이메일 담당자 표기를 읽기 어렵습니다. 특히 모바일에서는 12~12.8px로 더 작습니다.
- 고치는 법: #718096을 #4a5568(7.53:1, 본문에 이미 쓰는 색)이나 #5a6577(5.89:1)로 바꾸세요. 두 파일의 인라인 style 4곳과 CSS 규칙 5곳을 모두 고쳐야 합니다.

### [중간] Google 지도 iframe에 title 속성이 없어 스크린리더가 이름 없는 프레임으로 읽음
- 분류: 접근성 · 위치: `embeds/contact/html1.contact-info.html:183`, `embeds/contact/mobileHtml1.contact.html:69`
- 영향: 스크린리더 사용자는 '프레임'이라는 안내만 듣고 무슨 내용인지 알 수 없습니다(WCAG 4.1.2 이름·역할·값 위반). 이 프레임은 Wix iframe 안에 들어 있는 중첩 프레임이라 탐색하기가 더 헷갈립니다.
- 고치는 법: 두 파일의 지도 iframe에 `title="원주세브란스기독병원 위치 (Google 지도)"`를 추가하세요.

### [중간] 텍스트 몇 줄짜리 페이지가 부분 집합이 아닌 전체 Pretendard 폰트 2종(약 1.56MB)을 내려받음
- 분류: 성능 · 위치: `embeds/contact/html1.contact-info.html:8`, `embeds/contact/mobileHtml1.contact.html:7`
- 영향: 처음 방문한 모바일 사용자는 연락처 몇 줄을 보려고 약 1.5MB 폰트를 받습니다. font-display:swap이 설정되어 있어 폰트가 도착하면 글꼴이 바뀌면서 화면이 한 번 흔들립니다.
- 고치는 법: 두 파일의 링크를 `https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard-dynamic-subset.min.css`로 바꾸세요. 다른 페이지 임베드도 같은 링크를 쓰고 있다면 사이트 전체에서 한 번에 바꾸는 편이 좋습니다.
- 검증 메모: This is not specific to the contact page. All 23 embed files use the same URL (`pretendard@v1.3.9/dist/web/static/pretendard.min.css`). The woff2 files are served with `cache-control: public, max-age=31536000, immutable`, and every embed iframe sits under the same top-level site, so a visitor downloads the fonts once for the whole site. The 1.5MB cost applies only when a visitor's first page is this one (or any page, on a first visit). Report it once as a site-wide finding. Also, the woff2 paths quoted in the evidence are only valid under /packages/pretendard/dist/web/static/. Under /dist/web/static/ they return 404.

### [낮음] 지도에 비공식 구형 주소(maps.google.com/maps?...&output=embed)를 쓰고 있어 매번 301 리다이렉트가 생기며 지연 로딩도 없음
- 분류: 유지보수 · 위치: `embeds/contact/html1.contact-info.html:176-183`, `embeds/contact/mobileHtml1.contact.html:68-70`
- 영향: 지도를 불러올 때마다 리다이렉트가 한 번 더 생깁니다. 공식 퍼가기 형식이 아니라서 Google이 이 리다이렉트를 없애면 연락처 페이지 지도가 예고 없이 빈 칸이 됩니다. 모바일에서는 화면 아래에 있는 지도도 페이지를 열자마자 Google Maps 스크립트를 모두 불러옵니다.
- 고치는 법: Google 지도 → 공유 → 지도 퍼가기에서 받은 `https://www.google.com/maps/embed?pb=...` 주소로 두 파일의 src를 바꾸고, `loading="lazy"`와 title 속성을 함께 넣으세요.
- 검증 메모: A HEAD request to the same URL returns 404. Only GET redirects. Anyone checking the link with HEAD would wrongly conclude it is broken.

### [낮음] '팀별 연락처'(h2) 다음에 h3를 건너뛰고 h4를 쓰며, 제목 안의 이모지가 스크린리더에 그대로 읽힘
- 분류: 접근성 · 위치: `embeds/contact/html1.contact-info.html:197`, `embeds/contact/html1.contact-info.html:202-203`, `embeds/contact/html1.contact-info.html:213-214`, `embeds/contact/html1.contact-info.html:224-225`, `embeds/contact/html1.contact-info.html:153`, `embeds/contact/html1.contact-info.html:161`, `embeds/contact/html1.contact-info.html:166`, `embeds/contact/mobileHtml1.contact.html:74-95`
- 영향: 스크린리더 사용자가 제목 목록으로 이동할 때 한 단계가 빠져 있어 구조를 헷갈릴 수 있습니다. 또 '둥근 압정 주소', 'DNA 기초팀', '로봇 얼굴 데이터팀'처럼 뜻 없는 이모지 이름이 먼저 읽힙니다.
- 고치는 법: 두 파일에서 팀 카드 제목 h4를 h3로 바꾸고(CSS 선택자 `.team-card h4`도 함께 수정), 이모지는 `<span aria-hidden="true">📍</span>`처럼 감싸고 `.team-icon` div에도 aria-hidden="true"를 넣으세요.
- 검증 메모: The exact spoken emoji names (such as '로봇 얼굴') depend on the screen reader and OS. Also, on desktop the team emoji are outside the heading (in a separate div). Only on mobile are they inside the h4 text.

### [낮음] 모바일에서 기관 전체 이름 줄이 빠져 있고, 본문 글꼴 지정 방식이 데스크톱과 달라 모바일의 EngSerif 선언은 쓰이지 않는 코드임
- 분류: 데스크톱·모바일 불일치 · 위치: `embeds/contact/html1.contact-info.html:142`, `embeds/contact/mobileHtml1.contact.html:44-47`, `embeds/contact/html1.contact-info.html:19`, `embeds/contact/mobileHtml1.contact.html:11-17`
- 영향: 모바일 방문자는 첫 화면에서 연구소가 어느 병원 소속인지 보지 못합니다. 두 파일의 글꼴 구성이 달라서 나중에 한쪽만 고치면 데스크톱과 모바일 표시가 더 어긋날 수 있습니다.
- 고치는 법: 모바일 히어로의 h1 아래에 `<p>연세대학교 원주세브란스기독병원 청각재활연구소 (RIHE)</p>`를 추가하세요. 모바일 body의 font-family도 `'EngSerif', Pretendard, sans-serif`로 바꿔 데스크톱과 맞추세요.
- 검증 메모: The impact is overstated. On mobile, the first info card at 241px (line 53) shows `<strong>연세대학교 원주세브란스기독병원</strong>`, and the 소속 card (lines 64-66) lists the hospital and department. The visitor does see the affiliation on the first screen. The font difference has no visible effect either: Times New Roman has no Hangul, so it falls back to Pretendard, the same result as EngSerif. The unused EngSerif block is just dead code.

### [낮음] 한글 섹션 제목('연구소 안내', '팀별 연락처')의 글꼴 목록에 한글 글꼴이 없어 OS 기본 명조체로 표시됨
- 분류: 버그 · 위치: `embeds/contact/html1.contact-info.html:41-43`, `embeds/contact/html1.contact-info.html:146`, `embeds/contact/html1.contact-info.html:197`, `embeds/contact/mobileHtml1.contact.html:23`
- 영향: 페이지의 다른 한글은 모두 Pretendard인데 섹션 제목 한글만 운영체제의 기본 serif 글꼴(Windows는 바탕, macOS는 AppleMyungjo 등)로 나와, 기기마다 제목 모양이 다릅니다. 이번 오프라인 렌더(Linux)에서는 고딕으로 보였기 때문에 테스트로도 찾기 어렵습니다.
- 고치는 법: 두 파일의 해당 규칙을 `font-family: 'Playfair Display', Pretendard, serif;`로 바꾸세요. 그러면 영문은 Playfair, 한글은 Pretendard로 표시됩니다.
- 검증 메모: This is site-wide, not contact-only. A Playfair stack without Pretendard appears in 20 embed files across all pages (about, audiso, basic-lab, head-lab, hearing-lab, home, people, research, contact). Report it once as a site-wide issue.

## 페이지 간 데이터 일치

### [높음] Hearing Lab 페이지(데스크톱+모바일)에 Research의 2026년 Hearing 논문 2편이 빠져 있음
- 분류: 내용·데이터 · 위치: `embeds/research/html1.research.html:497`, `embeds/research/html1.research.html:506`, `embeds/research/mobileHtml1.research.html:91`, `embeds/research/mobileHtml1.research.html:100`, `embeds/hearing-lab/html1.hearing-lab.html:758`, `embeds/hearing-lab/html1.hearing-lab.html:751`, `embeds/hearing-lab/mobileHtml1.hearing-lab-mobile.html:142`
- 영향: Hearing Lab 페이지를 보는 방문자(데스크톱·모바일 모두)는 연구실의 최신 2026년 논문 2편을 볼 수 없고, 데스크톱에서 '2026' 연도 필터를 누르면 아무 항목도 없는 빈 목록이 나옵니다. Research 페이지와 연구실 페이지가 서로 다른 논문 수를 보여줍니다.
- 고치는 법: research/html1.research.html:497-514의 pub-item 2개를 hearing-lab/html1.hearing-lab.html의 `<div id="pub-list">` 바로 아래(:758 다음)와 hearing-lab/mobileHtml1.hearing-lab-mobile.html의 pub-body 첫 항목 앞(:143 앞)에 그대로 복사하세요. 앞으로 논문을 추가할 때는 Research 데스크톱·모바일 + 해당 연구실 데스크톱·모바일, 총 4곳을 함께 수정해야 합니다(체크리스트 권장).
- 검증 메모: 수정 방법에 한 가지를 더해야 합니다. hearing-lab/mobileHtml1.hearing-lab-mobile.html:141 헤더에 `<span>📄 Publication (19편)</span>`처럼 개수가 고정되어 있으므로, 2편을 추가하면 이 숫자도 '(21편)'으로 바꿔야 합니다. 2026 필터가 빈 목록이 되는 문제는 데스크톱(:751)에만 해당합니다.

### [중간] Home Outcomes의 논문 수 '118 Journals'가 Research 페이지의 논문 목록 120건과 맞지 않음
- 분류: 내용·데이터 · 위치: `embeds/home/html2.outcomes.html:103`, `embeds/home/mobileHtml1.home.html:56`, `embeds/research/html1.research.html:495`, `embeds/research/html1.research.html:3123`, `embeds/research/mobileHtml1.research.html:2639`
- 영향: 첫 화면에서 '118 Journals'를 본 방문자가 Research 페이지에서 '총 120건'을 보게 되어, 두 숫자가 서로 다릅니다(데스크톱·모바일 모두).
- 고치는 법: html2.outcomes.html:103과 mobileHtml1.home.html:56의 118을 실제 논문 수(현재 120)로 바꾸세요. 논문을 추가할 때마다 Home 숫자 2곳도 함께 고치도록 체크리스트에 넣으세요.

### [중간] 3개 연구실 페이지의 Report(학회 발표) 아코디언이 모두 비어 있음 (Research에는 94건)
- 분류: 내용·데이터 · 위치: `embeds/basic-lab/html1.basic-lab.html:1059`, `embeds/hearing-lab/html1.hearing-lab.html:954`, `embeds/hearing-lab/html1.hearing-lab.html:944`, `embeds/head-lab/html1.head-lab.html:927`, `embeds/basic-lab/mobileHtml1.basic-lab-mobile.html:518`, `embeds/hearing-lab/mobileHtml1.hearing-lab-mobile.html:317`, `embeds/head-lab/mobileHtml1.head-lab-mobile.html:310`, `embeds/research/html1.research.html:1622`
- 영향: 연구실 페이지에서 '📋 Report'를 펼친 방문자는 발표 목록 대신 '연동 예정' 안내만 봅니다. 데스크톱에서는 아무것도 걸러지지 않는 연도 버튼이 보이고, 모바일 안내문에는 Research로 가는 링크가 없습니다.
- 고치는 법: (A) Research의 Report 94건에 data-team(basic/hearing/head)을 붙이고 해당 항목을 각 연구실 데스크톱·모바일의 report-list에 복사하거나, (B) 당장은 Report 아코디언과 연도 버튼을 없애고 `<a href="https://www.smilesnail.org/project#report" target="_top">Research 페이지에서 학회 발표 보기 →</a>` 링크 하나로 바꾸세요. 데스크톱·모바일 문구도 하나로 맞추세요.
- 검증 메모: 수정 방법 (B)의 링크 `https://www.smilesnail.org/project#report`는 원하는 위치로 가지 않습니다. #report는 Research 페이지의 iframe(다른 출처) 안에 있는 요소라, 상위 Wix 페이지는 이 해시로 스크롤하지 못하고 Research 페이지 맨 위만 엽니다. 해시 없이 `https://www.smilesnail.org/project` + target="_top"으로 링크하세요. 방법 (A)는 Research의 주석 `<!-- Report은 팀별 필터 없음 (팀장님 지시) -->`(html1.research.html:1605)와 충돌하므로, 팀 분류를 먼저 결정해야 합니다.

### [중간] People 모바일에서 Temuulen의 성이 빠지고, 교수 3명의 소속 학과가 표시되지 않음
- 분류: 데스크톱·모바일 불일치 · 위치: `embeds/people/html1.people.html:158`, `embeds/people/mobileHtml1.people.html:76`, `embeds/people/html1.people.html:128`, `embeds/people/html1.people.html:134`, `embeds/people/html1.people.html:140`, `embeds/people/mobileHtml1.people.html:23`, `embeds/people/mobileHtml1.people.html:24`, `embeds/people/mobileHtml1.people.html:25`
- 영향: 모바일 방문자는 Post-doc 연구원의 전체 이름과 기재홍(생체공학과) 등 교수진의 소속 학과를 볼 수 없어서, 같은 페이지인데 데스크톱과 정보가 다릅니다.
- 고치는 법: mobileHtml1.people.html:76의 `<h4>Temuulen</h4>`를 `<h4>Temuulen Batsaikhan</h4>`로 바꾸고, :23-25 각 fac-card에 `<p class="role" style="font-size:0.7rem;color:#718096">이비인후과</p>`(기재홍은 생체공학과)를 추가하세요.
- 검증 메모: '나머지 31명'이 아니라 '나머지 27명'입니다. 두 파일 모두 전체 카드가 31장이고, 이 중 4장이 다릅니다.

### [중간] Home 연구소장 경력이 모바일에서 1개 빠지고 1개는 다르게 적혀 있음
- 분류: 데스크톱·모바일 불일치 · 위치: `embeds/home/html3.director.html:166`, `embeds/home/html3.director.html:170`, `embeds/home/html3.director.html:171`, `embeds/home/html3.director.html:172`, `embeds/home/html3.director.html:174`, `embeds/home/mobileHtml1.home.html:81`, `embeds/home/mobileHtml1.home.html:82`, `embeds/home/mobileHtml1.home.html:83`
- 영향: 모바일로 Home을 보는 방문자는 연구소장의 겸임 경력 1개를 볼 수 없고, 학과명도 데스크톱과 다르게 봅니다.
- 고치는 법: mobileHtml1.home.html:82를 `<li>연세대학교 미래캠퍼스 디지털헬스케어학과 겸임교수</li>`로 고치고, 그 아래에 `<li>연세대학교 원주의과대학원 의학통계학과 겸임교수</li>`를 추가하세요. 필요하면 이메일 줄도 넣으세요.

### [낮음] 특허 목록 '80건' 중 7쌍이 똑같은 중복 항목이라 서로 다른 특허는 73건뿐
- 분류: 내용·데이터 · 위치: `embeds/research/html1.research.html:2404`, `embeds/research/html1.research.html:2457`, `embeds/research/html1.research.html:2537`, `embeds/research/html1.research.html:2465`, `embeds/research/html1.research.html:2529`, `embeds/research/html1.research.html:2513`, `embeds/research/html1.research.html:2609`, `embeds/research/html1.research.html:2617` 외
- 영향: 특허 목록을 펼친 방문자는 똑같은 줄을 7번 두 번씩 보게 되고, '80건'이라는 숫자(목록 헤더와 Home)가 중복을 포함해 부풀려져 보입니다.
- 고치는 법: 실제로 번호가 다른 별개 출원이면 각 항목에 출원/등록번호를 넣어 구별되게 하세요(주석 템플릿의 `10-XXXXXXX (대한민국)` 형식). 진짜 중복이면 데스크톱·모바일에서 각 7개씩 지우고, '(80건)' 헤더 2곳과 Home Patents 숫자 2곳을 실제 건수로 고치세요.
- 검증 메모: 제목을 '특허 7쌍이 번호 없이 똑같이 표시되어 구별할 수 없음(실제 중복인지는 확인 필요)'으로 바꿔야 합니다. '서로 다른 특허는 73건뿐'은 삭제하세요. 또 데스크톱에서는 특허 아코디언이 max-height 5000px에서 잘려(:182) 뒤쪽 22건이 보이지 않습니다. 그래서 :2777과 :2985의 두 번째 사본은 데스크톱에서 보이지 않고, 데스크톱 방문자가 보는 중복은 5쌍입니다. 모바일에서는 7쌍이 모두 보입니다.

### [낮음] 연구실 데스크톱 페이지에는 팀 태그(.pub-tag.team-*) CSS가 없어 팀 색상이 빠진 채 글자만 표시됨
- 분류: 데스크톱·모바일 불일치 · 위치: `embeds/basic-lab/html1.basic-lab.html:376`, `embeds/hearing-lab/html1.hearing-lab.html:435`, `embeds/head-lab/html1.head-lab.html:417`, `embeds/basic-lab/mobileHtml1.basic-lab-mobile.html:59`, `embeds/hearing-lab/mobileHtml1.hearing-lab-mobile.html:52`, `embeds/head-lab/mobileHtml1.head-lab-mobile.html:59`, `embeds/research/html1.research.html:308`
- 영향: 데스크톱 연구실 페이지에서는 'Basic Lab/Hearing Lab/HeAD Lab' 태그가 배경·테두리 없이 글자만 나오지만, 같은 논문이 Research 페이지와 모바일 연구실 페이지에서는 팀 색상 칩으로 나옵니다. 팀 색상 표시가 페이지마다 다릅니다.
- 고치는 법: Research 데스크톱의 `.pub-tag.team-basic/hearing/head` 규칙(background·color·border)을 연구실 데스크톱 3개 파일의 `.pub-tag.conf` 규칙 다음에 복사하세요. `var(--basic)` 같은 변수는 연구실 파일에 정의되어 있지 않으니 #2E8B57/#7096B5/#4A90C4처럼 색상값을 직접 넣어야 합니다.
- 검증 메모: 모바일 CSS 줄 번호가 틀렸습니다. 실제 위치는 basic 모바일 :66-68, hearing 모바일 :60-62, head 모바일 :66-68입니다(finding의 :59-61, :52, :59가 아님).

### [낮음] 특허 10건은 국가 태그가 비어 있고, 상태/국가 태그에 연도·저널용 클래스를 섞어 씀
- 분류: 내용·데이터 · 위치: `embeds/research/html1.research.html:2485`, `embeds/research/html1.research.html:2509`, `embeds/research/html1.research.html:2525`, `embeds/research/html1.research.html:2685`, `embeds/research/html1.research.html:2693`, `embeds/research/html1.research.html:2701`, `embeds/research/html1.research.html:2789`, `embeds/research/html1.research.html:2877` 외
- 영향: 10건은 어느 나라 특허인지 알 수 없고, 빈 회색 칩이 작게 남습니다. 등록(회색)과 출원(파란색)이 연도·저널 스타일을 빌려 쓰고 있어서, 나중에 year/journal 스타일을 바꾸면 특허 표시도 함께 바뀝니다.
- 고치는 법: 빈 국가 태그 10곳에 실제 국가(PCT라면 'PCT')를 넣거나 span을 지우세요. `.pub-tag.status-reg`, `.pub-tag.status-app`, `.pub-tag.country` 같은 특허 전용 클래스를 만들어 쓰고, 값이 늘 같은 '특허' 태그는 없애거나 출원/등록번호로 바꾸세요.
- 검증 메모: 데스크톱에서는 빈 태그 10건 중 :2973과 :3005 두 건이 잘린 영역(특허 아코디언 5000px 제한)에 있어 실제로 보이는 것은 8건입니다. 모바일에서는 10건이 모두 보입니다.

### [낮음] 논문 저자 35건과 학회명 12건이 '...'로 잘려 있고, 같은 저널 이름이 여러 표기로 섞여 있음
- 분류: 내용·데이터 · 위치: `embeds/research/html1.research.html:518`, `embeds/research/html1.research.html:833`, `embeds/research/html1.research.html:2189`, `embeds/research/html1.research.html:497`, `embeds/research/html1.research.html:543`, `embeds/research/html1.research.html:642`, `embeds/research/html1.research.html:651`, `embeds/research/html1.research.html:660` 외
- 영향: 방문자는 저자 목록과 학회명·날짜가 중간에 끊긴 채로 봅니다. 같은 저널이 여러 이름으로 나와서 목록이 정리되지 않은 인상을 줍니다.
- 고치는 법: 잘린 47건은 원본 DB(RISS/WoS 등)에서 전체 저자와 학회명을 다시 가져와 Research 데스크톱·모바일과 연구실 페이지를 함께 고치세요. 저널명은 공식 표기 하나(예: 'Journal of Audiology and Otology', 'PLOS ONE')로 통일하세요.
- 검증 메모: '학회명 12건'은 '학회명 11건 + 발표자 목록 1건(:1922)'으로 고쳐야 합니다. 잘린 항목은 합계 47건으로 맞습니다.

### [낮음] Home 첫 문장에 띄어쓰기 오류와 조사 누락이 있음 (데스크톱·모바일 모두)
- 분류: 내용·데이터 · 위치: `embeds/home/html1.home-hero.html:60`, `embeds/home/html1.home-hero.html:61`, `embeds/home/mobileHtml1.home.html:49`, `embeds/home/mobileHtml1.home.html:50`
- 영향: 사이트에 들어온 모든 방문자가 가장 먼저 보는 문장에 '연구소 에'(띄어쓰기 오류)와 '기전 대한'(조사 '에' 누락)이 있습니다.
- 고치는 법: 4곳 모두 '청각재활연구소에 오신 것을 환영합니다.'와 '난청의 기전에 대한 기초 연구를…'로 고치세요.

### [낮음] Alumni: Basic Lab 모바일에는 섹션이 없고, 졸업일·학과명 표기가 복사본마다 다름
- 분류: 데스크톱·모바일 불일치 · 위치: `embeds/basic-lab/html1.basic-lab.html:1084`, `embeds/basic-lab/mobileHtml1.basic-lab-mobile.html:516`, `embeds/head-lab/html1.head-lab.html:946`, `embeds/head-lab/html1.head-lab.html:956`, `embeds/head-lab/mobileHtml1.head-lab-mobile.html:318`, `embeds/head-lab/mobileHtml1.head-lab-mobile.html:320`, `embeds/hearing-lab/html1.hearing-lab.html:972`, `embeds/hearing-lab/mobileHtml1.hearing-lab-mobile.html:325`
- 영향: 작은 차이지만, 졸업생 정보를 고칠 때 복사본마다 형식이 달라 빠뜨리기 쉽습니다. Basic Lab 모바일에는 졸업생을 추가할 자리가 없습니다.
- 고치는 법: 날짜 형식을 하나로 정하고(예: 2025.02), 이주형의 학과명을 '의료정보통계학과'로 통일하세요. Basic Lab 모바일에도 hearing/head 모바일과 같은 Alumni 섹션을 추가하세요.

### [낮음] 한국인 청각 참조표준데이터센터의 영문 이름이 About과 Hearing Lab에서 다름
- 분류: 내용·데이터 · 위치: `embeds/about/html2.참조표준데이터센터.html:101`, `embeds/hearing-lab/html1.hearing-lab.html:581`
- 영향: 같은 기관이 두 페이지에서 서로 다른 영문 이름으로 소개됩니다.
- 고치는 법: 공식 영문 이름 하나를 정해 두 파일에 똑같이 쓰세요(About처럼 한글 제목 아래에 영문을 두거나, Hearing Lab 제목을 한글로 두고 영문을 부제로).

#### 검증 단계에서 추가로 발견된 항목 (페이지 간 데이터 일치)

검증 에이전트가 따로 보고한 것으로, 2차 검증은 거치지 않았습니다.

- [high] Research 데스크톱 특허 아코디언이 잘려 80건 중 22건이 보이지 않습니다. embeds/research/html1.research.html:182 `.collapse-body.open { max-height: 5000px; }`와 :179 `overflow: hidden;` 때문입니다. 1280px에서 #patent-body 내용 높이는 6941px로 측정되었고, 58번째 항목은 반쯤 잘리며, 59~80번째(:2873 '가상현실 기반의 휴대용 안진 검사장치 및 이를 이용한 검진 방법'부터 끝까지)는 볼 방법이 없습니다. 모바일(mobileHtml1.research.html:57, max-height 8000px)은 잘리지 않습니다.
- [high] Basic Lab 데스크톱 Publication 아코디언이 잘려 41편 중 13편이 보이지 않습니다. embeds/basic-lab/html1.basic-lab.html:322-323 `.collapse-body.open { max-height: 3000px; }` 때문입니다. 1280px에서 #pub 내용은 4430px이고, 28번째는 반쯤 잘리며, 29~41번째(:918-919 'In vitro time-lapse live-cell imaging to explore cell migration toward the organ of corti'부터)는 보이지 않습니다. 모바일(mobileHtml1.basic-lab-mobile.html:56, 8000px)은 잘리지 않습니다.
- [low] 연구실 데스크톱 연도 필터에 해당 연도 항목이 0건인 버튼이 있습니다. basic-lab/html1.basic-lab.html:658과 head-lab/html1.head-lab.html:743의 `<button class="year-btn" onclick="filterYear(this,'pub')">2026</button>`, 그리고 세 연구실 Report의 연도 버튼(:1050-1054 등)입니다. filterYear(예: head-lab :975~)에는 '결과 없음' 표시가 없어 누르면 목록이 빈 채로 남습니다. Research에는 `id="pub-no-results"`(:1579)가 있지만 연구실 페이지에는 없습니다.
- [low] Home 모바일의 영문 소개 문장이 데스크톱보다 짧게 잘려 있습니다. embeds/home/mobileHtml1.home.html:51은 `…conducts full-cycle research on hearing.`로 끝나고, embeds/home/html1.home-hero.html:62에는 `…full-cycle research on hearing from the development of drugs, clinical research, and medical devices, and strives to become the world's best research institute in hearing research.`가 있습니다.
- [low] Hearing Lab 모바일 논문 헤더에 개수가 고정되어 있습니다. embeds/hearing-lab/mobileHtml1.hearing-lab-mobile.html:141 `<span>📄 Publication (19편)</span>`(basic 모바일 :144 '(41편)', head 모바일 :152 '(17편)'도 같은 방식)이라, 논문을 추가할 때 이 숫자를 따로 고쳐야 합니다. hearing-lab-missing-2026-pubs 수정 방법에 이 내용이 빠져 있습니다.

## 중복·유지보수

### [높음] 논문 데이터 복제본끼리 이미 어긋남: Hearing Lab 페이지에 2026년 논문 2편이 빠져 있고 건수 표기가 서로 다름
- 분류: 내용·데이터 · 위치: `embeds/research/html1.research.html:497`, `embeds/research/html1.research.html:506`, `embeds/research/mobileHtml1.research.html:91`, `embeds/research/mobileHtml1.research.html:100`, `embeds/hearing-lab/html1.hearing-lab.html:751`, `embeds/hearing-lab/html1.hearing-lab.html:759`, `embeds/hearing-lab/mobileHtml1.hearing-lab-mobile.html:141`, `embeds/home/html2.outcomes.html:103` 외
- 영향: Hearing Lab 페이지 방문자는 데스크톱과 모바일 모두에서 최신 2026년 논문 2편을 볼 수 없습니다. '2026' 버튼을 누르면 안내 문구 없이 빈 목록이 나옵니다. 같은 팀 논문 수가 Research 필터에서는 21건, Hearing Lab 모바일 제목에서는 19편, 홈에서는 118 대 120으로 페이지마다 다르게 보입니다.
- 고치는 법: 당장은 두 논문을 hearing-lab/html1과 mobileHtml1의 pub-list 맨 앞에 추가하세요. 모바일 제목 '(19편)'은 '(21편)'으로 바꾸거나 JS로 자동 계산되게 합니다. 홈의 118은 기준(학술지만 셀지, 전체를 셀지)을 정해 맞춥니다. 근본적으로는 논문 목록을 하나의 원본(JSON 또는 스프레드시트)으로 두고, 스크립트로 8개 임베드를 생성하거나 Wix CMS 컬렉션과 반복 레이아웃으로 옮겨야 다시 어긋나지 않습니다.

### [높음] 같은 아코디언의 max-height가 파일마다 3000/5000/8000px로 고정됨: 지금도 Basic Lab 논문 14편과 특허 23건이 잘리고, Hearing/HeAD Lab은 약 8–10편 더 추가하면 잘림
- 분류: 버그 · 위치: `embeds/basic-lab/html1.basic-lab.html:322`, `embeds/hearing-lab/html1.hearing-lab.html:383`, `embeds/head-lab/html1.head-lab.html:365`, `embeds/research/html1.research.html:182`, `embeds/research/mobileHtml1.research.html:57`, `embeds/basic-lab/mobileHtml1.basic-lab-mobile.html:56`, `embeds/hearing-lab/mobileHtml1.hearing-lab-mobile.html:51`, `embeds/head-lab/mobileHtml1.head-lab-mobile.html:56` 외
- 영향: 데스크톱 방문자는 Basic Lab의 2016–2020년 논문 대부분과 특허 목록 뒤쪽 23건을 볼 수 없으며, 잘렸다는 표시도 없습니다. 앞으로 논문이 추가되면 Hearing Lab과 HeAD Lab에서도 같은 일이 조용히 반복됩니다.
- 고치는 법: 고정 max-height 대신 열 때 JS로 실제 높이를 넣으세요(`body.style.maxHeight = open ? body.scrollHeight + 'px' : '0'`). 또는 `<details>/<summary>`를 쓰면 높이 제한 자체가 없어집니다. 이 토글 코드는 7개 파일에 복사돼 있으므로 공통 스니펫 1개로 정리하고 모든 파일에 같은 방식을 적용합니다.
- 검증 메모: 기본 '전체' 보기에서 가려지는 14편은 basic-lab의 2016–2020년 논문 전부입니다(2016 2, 2017 3, 2018 3, 2019 1, 2020 5). 다만 '~2021' 필터를 누르면 26편·2856px로 3000px 안에 들어와 모두 보입니다. 특허 23건은 필터가 없어 볼 방법이 없습니다. 항목 높이 105–112px는 랩 논문 기준(103–106px)이고, 특허 항목은 약 86px입니다. audiso/mobileHtml1 L55의 규칙은 파일에 .collapse-body 요소가 없어 쓰이지 않으므로 영향 위치에서 빼야 합니다. 토글 코드는 7개가 아니라 8개 파일에 있습니다(랩 데스크톱 3 toggleCollapse, 랩 모바일 3 toggle, research html1 togglePatent, research mobile toggleCollapse).

### [중간] 고유 논문·발표·특허 294건이 .pub-item 742개로 복제됨: 논문 1편 추가에 파일 6개(페이지 3곳의 Wix 요소 6개)를 손으로 고쳐야 함
- 분류: 유지보수 · 위치: `embeds/research/html1.research.html:495`, `embeds/research/html1.research.html:1622`, `embeds/research/html1.research.html:2407`, `embeds/research/mobileHtml1.research.html:89`, `embeds/basic-lab/html1.basic-lab.html:665`, `embeds/basic-lab/mobileHtml1.basic-lab-mobile.html:144`, `embeds/hearing-lab/html1.hearing-lab.html:759`, `embeds/hearing-lab/mobileHtml1.hearing-lab-mobile.html:141` 외
- 영향: 논문 한 편을 올릴 때마다 서로 다른 3개 페이지에서 Wix 요소 6개를 열어 코드 전체를 바꿔 붙여야 합니다. 하나라도 빠뜨리면 위 Hearing Lab 사례처럼 페이지마다 내용과 개수가 달라지는데, 이를 알려주는 장치가 없습니다.
- 고치는 법: data/publications.json(title, authors, year, team, venue, type) 하나를 원본으로 두세요. 그리고 tools/에 생성 스크립트를 추가해 research·lab 데스크톱/모바일 8개 파일의 목록 부분과 개수 숫자를 자동으로 채웁니다. 생성 결과를 커밋하고 바뀐 요소만 Wix에 붙여넣습니다. 더 나아가 Wix CMS 컬렉션 하나에 데이터를 두고 페이지별로 필터링된 반복 레이아웃을 쓰면 수정 지점이 1곳으로 줄어듭니다.
- 검증 메모: '고유 레코드 294건'은 research 한 벌에 들어 있는 행 수입니다. 특허 80행에는 태그까지 같은 중복 행 7쌍이 있어서, 실제로 서로 다른 레코드는 294건보다 적습니다.

### [중간] 랩 데스크톱 3개 페이지에 .pub-authors와 .pub-tag.team-* 스타일이 없음: 논문 77건에서 저자명이 제목보다 크게, 팀 뱃지는 배경 없는 글자로 표시됨
- 분류: 버그 · 위치: `embeds/basic-lab/html1.basic-lab.html:376`, `embeds/basic-lab/html1.basic-lab.html:668`, `embeds/basic-lab/html1.basic-lab.html:671`, `embeds/hearing-lab/html1.hearing-lab.html:435`, `embeds/hearing-lab/html1.hearing-lab.html:761`, `embeds/hearing-lab/html1.hearing-lab.html:764`, `embeds/head-lab/html1.head-lab.html:417`, `embeds/head-lab/html1.head-lab.html:753` 외
- 영향: Basic, Hearing, HeAD Lab 데스크톱에서 Publication을 펼치면 모든 논문의 저자 줄이 제목보다 크고 진하게 보입니다. 'Basic Lab' 같은 팀 태그만 뱃지 모양이 없어 연도·저널 뱃지와 어긋나 보입니다.
- 고치는 법: 세 파일 CSS에 research/html1 L277–327의 `.pub-authors`와 `.pub-tag.team-*` 규칙을 그대로 추가하세요. 장기적으로는 공통 CSS를 한 곳(생성 스크립트의 공통 템플릿)에서 관리해 복사본끼리 규칙이 빠지지 않게 합니다.
- 검증 메모: 수정안의 'research L277–327 규칙을 그대로 추가'는 그대로는 동작하지 않습니다. research의 .pub-tag.team-*는 color: var(--basic)/var(--hearing)/var(--head)/var(--collab)를 쓰는데, 랩 :root(basic L24–33 등)에는 --accent 계열과 --text* 변수만 정의돼 있습니다. 복사할 때 hex 값(#2E8B57, #7096B5, #4A90C4)이나 var(--accent)로 바꿔야 합니다.

### [중간] 연도 필터 버튼이 파일 4개의 8개 그룹에 하드코딩됨: 2027 없음, '~2021' 유무 제각각, 눌러도 0건인 버튼이 많음
- 분류: 유지보수 · 위치: `embeds/basic-lab/html1.basic-lab.html:657`, `embeds/basic-lab/html1.basic-lab.html:1049`, `embeds/basic-lab/html1.basic-lab.html:1115`, `embeds/basic-lab/html1.basic-lab.html:630`, `embeds/hearing-lab/html1.hearing-lab.html:750`, `embeds/hearing-lab/html1.hearing-lab.html:944`, `embeds/hearing-lab/html1.hearing-lab.html:1005`, `embeds/head-lab/html1.head-lab.html:742` 외
- 영향: 2027년 논문을 넣어도 연도 버튼이 없으면 '전체'에서만 보입니다. 2027을 추가하려면 4개 파일의 8개 버튼 그룹을 고쳐야 합니다. '최근 5년 + 이전' 구성을 유지하려면 여기에 JS 4곳과 '~2021' 라벨 5곳까지 바꿔야 하고, 랩 3곳은 라벨 문자열을 JS가 그대로 비교하므로 한 곳만 바꾸면 필터가 고장 납니다. 지금도 방문자가 누르면 빈 화면만 나오는 버튼이 있습니다.
- 고치는 법: 버튼을 JS로 생성하세요. 목록 항목의 data-year 고유값을 내림차순으로 정렬해 최근 N개 연도 버튼을 만들고, 나머지는 '~(최근연도-N)'로 묶습니다. 기준 연도는 계산으로 구하고 0건인 연도 버튼은 만들지 않습니다. 이 필터 스크립트 하나를 4개 파일이 공유하도록 생성 스크립트에 넣습니다. 비어 있는 랩 Report 필터는 제거합니다.

### [중간] 손으로 쓴 개수와 기간이 6개 파일에 흩어져 있음: '80건' 특허 목록의 고유 제목은 52개, 홈 118은 목록 120건과 불일치
- 분류: 내용·데이터 · 위치: `embeds/home/html2.outcomes.html:103`, `embeds/home/html2.outcomes.html:109`, `embeds/home/mobileHtml1.home.html:56`, `embeds/home/mobileHtml1.home.html:57`, `embeds/research/html1.research.html:2404`, `embeds/research/mobileHtml1.research.html:1942`, `embeds/research/html1.research.html:2457`, `embeds/research/html1.research.html:2537` 외
- 영향: 방문자는 '특허 80건' 목록에서 같은 제목이 번호 없이 반복되는 것을 보게 되어 숫자를 신뢰하기 어렵습니다. 논문이나 특허를 추가할 때 이 숫자 8곳을 함께 고쳐야 하는데, 이미 118과 120, 19편과 21건처럼 어긋나 있습니다.
- 고치는 법: 목록 개수는 research처럼 JS로 `.pub-item` 수를 세어 표시하세요(모바일 '(N편)', '(80건)'). 홈 Outcomes 숫자도 데이터 원본에서 생성하거나, 최소한 기준(학술지만/전체)을 주석에 적습니다. 특허 행에는 출원·등록번호를 넣어 구분하고, 진짜 중복은 정리하고, 빈 국가 태그는 채웁니다. '(2022.1~)' 같은 기간 표기는 한 곳(생성 데이터)에서만 관리합니다.
- 검증 메모: 함께 고쳐야 하는 숫자는 8곳이 아니라 9곳입니다(118×2, 80×4, 랩 모바일 (N편)×3). '(2022.1~)'는 두 곳에 복제돼 있지만 값이 같아 현재 결함은 아닙니다. 유지보수 참고 사항 정도입니다.

### [중간] 'EngSerif'(local('Times New Roman')) 방식 때문에 기기마다 영문 글꼴이 다르고, 모바일 6개 파일은 다른 방식이라 같은 기기에서도 페이지마다 영문 글꼴이 달라짐
- 분류: 데스크톱·모바일 불일치 · 위치: `embeds/home/html1.home-hero.html:12`, `embeds/home/html1.home-hero.html:48`, `embeds/research/html1.research.html:15`, `embeds/home/mobileHtml1.home.html:17`, `embeds/home/mobileHtml1.home.html:21`, `embeds/about/mobileHtml1.about.html:17`, `embeds/audiso/mobileHtml1.audiso-mobile.html:17`, `embeds/basic-lab/mobileHtml1.basic-lab-mobile.html:16` 외
- 영향: Times New Roman은 Windows, macOS, iOS에만 기본 설치되고 Android에는 없습니다. 따라서 Android 방문자에게는 17개 임베드의 영문이 Pretendard(고딕)로, Windows/Mac/iPhone 방문자에게는 명조(TNR)로 보입니다. TNR이 없는 기기에서는 모바일 6개 페이지만 명조로 나와 페이지마다 영문 글꼴이 바뀝니다. TNR이 있는 기기에서는 굵은 영문 제목과 기울임 문장이 가짜 굵게·가짜 기울임으로 그려집니다(예: 홈 데스크톱 L48 italic 문장은 가짜 기울임, 같은 문장의 모바일 L21은 진짜 TNR Italic). iframe 높이가 고정이라 OS마다 흰 여백이나 잘림 정도도 달라집니다.
- 고치는 법: 한 가지 방식으로 통일하세요. TNR과 글자 폭이 같은 웹폰트 Tinos를 Google Fonts에서 400/700/400italic으로 불러오고(`family=Tinos:ital,wght@0,400;0,700;1,400`), `font-family: 'Tinos', Pretendard, sans-serif`로 바꾸면 모든 기기에서 같은 영문 명조가 나옵니다. Tinos에는 한글이 없어 한글은 자동으로 Pretendard가 됩니다. 23개 파일의 local() @font-face와 6개 파일의 'Times New Roman' 직접 지정은 모두 제거합니다. 영문 명조가 꼭 필요하지 않다면 Pretendard 하나로 통일하는 방법도 있습니다.
- 검증 메모: TNR이 있는 기기에서 가짜 굵게·가짜 기울임이 생긴다는 부분은 Chromium 계열(local()이 Regular face의 전체 이름과 일치)에서만 근거가 있습니다. Safari/WebKit은 local()을 가족명으로 찾을 수 있어 iOS에서도 같은지는 확인하지 못했습니다.

### [중간] 23개 임베드가 서브셋이 아닌 Pretendard 전체 글꼴을 불러와 임베드 하나에 최대 3.0MB 글꼴을 받음
- 분류: 성능 · 위치: `embeds/basic-lab/html1.basic-lab.html:10`, `embeds/research/html1.research.html:10`, `embeds/research/mobileHtml1.research.html:7`, `embeds/hearing-lab/mobileHtml1.hearing-lab-mobile.html:1`, `embeds/basic-lab/html1.basic-lab.html:302`
- 영향: 휴대폰으로 Research나 랩 페이지를 처음 열면 글꼴만 약 2–3MB를 받습니다. 느린 모바일 회선에서는 한글이 늦게 뜨거나 대체 글꼴에서 바뀌며 깜빡이고, 데이터 요금 부담도 생깁니다.
- 고치는 법: 23개 파일의 링크를 같은 버전의 `.../dist/web/static/pretendard-dynamic-subset.min.css`로 바꾸세요. 이 CSS는 unicode-range로 쪼갠 조각 중 실제로 쓰인 글자 조각만 받습니다. 쓰는 굵기도 400/700 정도로 줄이면(500·600을 400/700으로 대체) 추가로 절감됩니다.
- 검증 메모: '3.01MB'는 4개 굵기 합계 3,121,336B에 Playfair를 더한 값이고, MiB 기준으로 약 3.0입니다. 모든 iframe의 최상위 사이트가 같아 HTTP 캐시가 공유되므로, 이 비용은 사이트 첫 방문(또는 캐시 만료 후) 한 번만 듭니다. 페이지를 옮길 때마다 다시 받지는 않습니다.

### [중간] 인물·연락처·조직도가 최대 12개 파일에 복제됨: 이메일은 파일마다 표기 방식이 달라 검색·치환으로 다 찾을 수 없고, 이미 내용이 어긋남
- 분류: 데스크톱·모바일 불일치 · 위치: `embeds/contact/html1.contact-info.html:162`, `embeds/contact/mobileHtml1.contact.html:59`, `embeds/home/html3.director.html:174`, `embeds/contact/mobileHtml1.contact.html:81`, `embeds/home/html3.director.html:171`, `embeds/home/mobileHtml1.home.html:82`, `embeds/people/html1.people.html:158`, `embeds/people/mobileHtml1.people.html:76` 외
- 영향: 구성원 1명 추가는 2개 파일, 팀장 교체는 6개 파일, 연구소장 사진 교체는 10개 파일을 고쳐야 합니다. 이메일 변경은 서로 다른 표기 2가지를 모두 찾아야 해서 모바일 연락처만 옛 주소로 남기 쉽습니다. 실제로 데스크톱과 모바일 방문자는 이미 서로 다른 직함과 이름을 보고 있습니다.
- 고치는 법: people.json(이름, 역할, 팀, 사진, 이메일)을 원본으로 두고 People·Contact·Lab·Home 임베드의 해당 부분을 생성하세요. 이메일 표기는 한 방식으로 통일합니다. 당장은 모바일 연구소장 직함, Temuulen 이름, 교수 소속을 데스크톱과 맞추고, 조직도 순서와 명칭을 한 가지로 정합니다.

### [낮음] CSS와 JS가 23개 파일에 통째로 복사됨: CSS 규칙 920개 중 462개가 중복이고 같은 선택자에 파일마다 다른 값이 들어 있음
- 분류: 유지보수 · 위치: `embeds/basic-lab/html1.basic-lab.html:25`, `embeds/hearing-lab/html1.hearing-lab.html:26`, `embeds/basic-lab/html1.basic-lab.html:339`, `embeds/research/html1.research.html:221`, `embeds/audiso/mobileHtml1.audiso-mobile.html:30`, `embeds/audiso/mobileHtml1.audiso-mobile.html:58`, `embeds/hearing-lab/html1.hearing-lab.html:205`, `embeds/home/html3.director.html:198`
- 영향: 스타일 하나를 고치려면(예: 팀 색, 섹션 제목 밑줄, 아코디언 동작) 최대 23개 Wix 요소를 다시 붙여넣어야 합니다. 이미 복사본마다 값이 달라서 위의 저자명 크기, 필터 버튼 글꼴, 아코디언 높이 같은 문제가 파일별로 생겼습니다.
- 고치는 법: 공통 CSS/JS(리셋, 글꼴, 섹션 제목, 아코디언, 필터, 페이드)를 한 파일로 모으고, 생성 스크립트가 각 임베드에 넣게 하세요. Wix iframe은 서로 다른 출처라 외부 CSS 하나를 공유하기 어렵고, 저장소 안에서 템플릿으로 합치는 편이 현실적입니다. 팀 색은 CSS 변수 한 벌로 정의합니다. 미사용 규칙과 불필요한 observer는 삭제합니다.
- 검증 메모: 아코디언 토글은 7벌이 아니라 8개 파일에 있습니다(research html1 togglePatent, research mobile toggleCollapse 포함). 규칙 수 920/458은 파서에 따라 909/465 정도로 달라지는 근사값입니다.

### [낮음] 오래된 TODO와 내부 메모, 실제와 다른 입력 예시가 방문자 브라우저로 전송되고, 화면에는 '연동 예정' 문구가 계속 보임
- 분류: 유지보수 · 위치: `embeds/basic-lab/html1.basic-lab.html:528`, `embeds/basic-lab/html1.basic-lab.html:588`, `embeds/hearing-lab/html1.hearing-lab.html:626`, `embeds/hearing-lab/html1.hearing-lab.html:685`, `embeds/home/html3.director.html:190`, `embeds/contact/html1.contact-info.html:194`, `embeds/audiso/html1.audiso.html:512`, `embeds/research/html1.research.html:1605` 외
- 영향: 방문자가 iframe 소스를 보면 내부 결정 이력('팀장님 지시', 'v6 확정')이 보입니다. 다음 담당자가 예시 코드를 그대로 따라 논문이나 특허를 추가하면 기존 항목과 다른 모양(저자·팀 태그 없음)이 됩니다. 랩 Report 칸은 실제로 연동되지 않은 채 '연동 예정'이라고 계속 안내합니다.
- 고치는 법: 끝난 TODO와 내부 메모는 삭제하고, 결정 이력은 저장소 docs나 커밋 메시지로 옮기세요. 입력 예시는 실제 항목 한 개를 복사한 형태로 고치거나, 데이터 원본으로 전환한 뒤 삭제합니다. 랩 Report 칸은 모바일처럼 'Research 페이지에서 확인하세요' 링크(target="_top")로 바꾸거나 해당 팀 발표를 실제로 넣습니다.
- 검증 메모: home/html3 L190 '<!-- TODO: 교수님 사진 교체 시 src만 변경 -->'은 끝난 작업이 아니라 사용 안내입니다. 따라서 끝난 TODO는 5개가 아니라 4개입니다. 수정안의 '모바일처럼 … 링크(target="_top")'도 틀렸습니다. 랩 모바일(예: basic-lab mobile L518 '학회 발표 데이터는 Research 페이지에서 확인하세요.')은 링크 없는 일반 텍스트이므로, 모바일에도 링크를 새로 넣어야 합니다.

#### 검증 단계에서 추가로 발견된 항목 (중복·유지보수)

검증 에이전트가 따로 보고한 것으로, 2차 검증은 거치지 않았습니다.

- research/html1.research.html 기본(접힌) 상태에서 이미 내용이 iframe보다 깁니다. docs/site-map.md L18의 에디터 높이는 3843px이고, measure-summary의 contentHeight는 3900px(TNR 시뮬레이션 3856px)입니다. 따라서 페이지를 열자마자 iframe 안에 스크롤이 생기거나 아래쪽이 잘립니다(측정 오차 ±3%). 아코디언이나 더보기를 열면 32664px까지 늘어나지만 iframe은 고정 높이입니다. 같은 현상이 basic-lab html1(에디터 3212px, docs/site-map.md L22 대 전부 펼침 6143px)과 hearing/head 랩(4017/4097 대 약 6060px)에도 있어, 방문자는 페이지 스크롤 안에 또 스크롤을 써야 합니다. 다른 감사에서 다루지 않았다면 high입니다.
- 저자 목록이 성 뒤에서 잘린 채 '...'로 끝나는 항목이 여러 파일에 그대로 표시됩니다. 예: research/html1.research.html:518과 hearing-lab/html1.hearing-lab.html:761 `Cho, Wan-Ho, Lee, Jihyun, Kwak, Chanbeom, You, Sunghwa, Sagong, Junghee, Kim,...`, research L590 `…Suh, Michelle J., Cho,...`. 집계 결과 research 214건 중 36건, basic 41건 중 14건, hearing 19건 중 6건, head 17건 중 5건이고 데스크톱과 모바일이 같습니다. 이름 없이 'Kim,' 'Cho,'에서 끊겨 있어 원본을 내보낼 때 잘린 것으로 보입니다(low–medium).
- 랩 모바일 Report 칸은 링크 없이 안내만 합니다. basic-lab/mobileHtml1.basic-lab-mobile.html:518 `<p class="placeholder">학회 발표 데이터는 Research 페이지에서 확인하세요.</p>`이고, hearing과 head 모바일도 같습니다. Research로 가는 링크(target="_top")가 없어 방문자가 직접 메뉴에서 찾아가야 합니다(low).

