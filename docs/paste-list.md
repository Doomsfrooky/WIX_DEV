# Wix 반영 목록 (1단계 수정)

2026-09-30 게시본 기준으로 고친 파일과, Wix에서 맞춰야 할 요소 높이입니다.

## 순서

1. Wix 에디터에서 페이지를 엽니다. 모바일 요소(`#mobileHtml1`)는 상단의 모바일 아이콘을 눌러 모바일 에디터에서 찾습니다.
2. **붙여넣기**가 적힌 요소를 클릭 → 설정 → **코드 입력** 칸을 전부 지우고 파일 내용을 통째로 붙여넣은 뒤 **업데이트**를 누릅니다.
3. 요소를 선택한 채 오른쪽 아래 크기 입력칸(또는 드래그)에서 높이를 **굵은 숫자**로 바꿉니다.
4. 모든 페이지를 마친 뒤 **게시하기**를 누릅니다.
5. 게시 후 `python3 tools/fetch_live.py`를 돌리면 저장소와 사이트가 일치하는지 확인할 수 있습니다(변경이 없으면 성공).

높이는 실제 사진과 글꼴로 렌더링해 잰 값에 여유 20px를 더한 것입니다. 측정 오차가 ±3% 정도 있으니, 게시 후 아래쪽이 잘리거나 스크롤바가 보이면 조금 더 늘려 주세요.

| 페이지 | 요소 | 보기 | 코드 | 높이(px) | 파일 |
|---|---|---|---|---|---|
| Home | `#html1` | 데스크톱 | 붙여넣기 | 450 (그대로) | `embeds/home/html1.home-hero.html` |
| Home | `#html2` | 데스크톱 | 붙여넣기 | 382 (그대로) | `embeds/home/html2.outcomes.html` |
| Home | `#html3` | 데스크톱 | 붙여넣기 | 855 → **880** | `embeds/home/html3.director.html` |
| Home | `#mobileHtml1` | 모바일 | 붙여넣기 | 1,493 → **2,020** | `embeds/home/mobileHtml1.home.html` |
| About | `#html1` | 데스크톱 | 붙여넣기 | 761 → **800** | `embeds/about/html1.about-intro.html` |
| About | `#html2` | 데스크톱 | 붙여넣기 | 512 → **530** | `embeds/about/html2.참조표준데이터센터.html` |
| About | `#html4` | 데스크톱 | - | 458 → **500** | `embeds/about/html4.partners.html` |
| About | `#mobileHtml1` | 모바일 | 붙여넣기 | 1,665 → **1,750** | `embeds/about/mobileHtml1.about.html` |
| Research | `#html1` | 데스크톱 | 붙여넣기 | 3,843 → **3,920** | `embeds/research/html1.research.html` |
| Research | `#mobileHtml1` | 모바일 | 붙여넣기 | 3,651 → **4,220** | `embeds/research/mobileHtml1.research.html` |
| People | `#html1` | 데스크톱 | - | 3,454 → **3,500** | `embeds/people/html1.people.html` |
| People | `#mobileHtml1` | 모바일 | 붙여넣기 | 3,668 → **3,710** | `embeds/people/mobileHtml1.people.html` |
| Basic Lab | `#html1` | 데스크톱 | 붙여넣기 | 3,212 → **3,050** | `embeds/basic-lab/html1.basic-lab.html` |
| Basic Lab | `#mobileHtml1` | 모바일 | 붙여넣기 | 1,979 → **2,320** | `embeds/basic-lab/mobileHtml1.basic-lab-mobile.html` |
| Hearing Lab | `#html1` | 데스크톱 | 붙여넣기 | 4,017 → **3,830** | `embeds/hearing-lab/html1.hearing-lab.html` |
| Hearing Lab | `#mobileHtml1` | 모바일 | 붙여넣기 | 2,372 → **3,270** | `embeds/hearing-lab/mobileHtml1.hearing-lab-mobile.html` |
| HeAD Lab | `#html1` | 데스크톱 | 붙여넣기 | 4,097 (그대로) | `embeds/head-lab/html1.head-lab.html` |
| HeAD Lab | `#mobileHtml1` | 모바일 | 붙여넣기 | 2,852 → **3,380** | `embeds/head-lab/mobileHtml1.head-lab-mobile.html` |
| Audiso | `#html1` | 데스크톱 | 붙여넣기 | 3,077 → **3,100** | `embeds/audiso/html1.audiso.html` |
| Audiso | `#mobileHtml1` | 모바일 | 붙여넣기 | 2,722 → **3,320** | `embeds/audiso/mobileHtml1.audiso-mobile.html` |
| Contact | `#html1` | 데스크톱 | - | 1,397 → **1,420** | `embeds/contact/html1.contact-info.html` |
| Contact | `#mobileHtml1` | 모바일 | 붙여넣기 | 1,493 → **1,550** | `embeds/contact/mobileHtml1.contact.html` |
`-`는 코드는 그대로 두고 높이만 바꾸면 되는 요소입니다. About `#html3`은 바꿀 것이 없습니다.

## 이번에 고친 내용

- 잘려서 보이지 않던 목록: Research 특허 22건, Basic Lab 논문 13편이 이제 끝까지 펼쳐집니다(아코디언 최대 높이 제한 제거, 모바일 포함).
- 연구실 데스크톱 3개: 저자 줄이 제목보다 크게 보이던 문제와 팀 태그 배경 수정. 논문이 없는 연도 버튼은 자동으로 숨깁니다.
- 연구실 Report: '연동 예정' 빈 칸 대신 Research 페이지로 가는 링크(데스크톱·모바일).
- Hearing Lab: 2026년 논문 2편 추가(데스크톱·모바일, 모바일 표기 21편). 홈 Journals 118 → 120.
- 모바일 9개 페이지: 빠지거나 다르게 적혀 있던 내용을 데스크톱과 같게 맞춤(연구소장 소속·이메일·인사말, 데이터센터 설명, Mission·Vision, 교수진 학과, 제품·강점 설명 등).
- 오타 수정(사이트 문구, 학회명). 저자 목록은 바꾸지 않았습니다. 검토용 자료는 [author-review.md](author-review.md)에 있습니다.

## 확인이 필요한 것

- 저자 목록이 원본에서 잘려 있는 논문(예: `Kim,...`)은 그대로 두었습니다. 논문 자체는 한 편도 삭제하지 않았습니다.
- Audiso 피스탑 트리플케어 설명의 효능 표현이 허용된 문구인지.
- Report의 학회명 11건은 원본에서 '...'로 잘려 있어 복원하지 못했습니다.

## Wix 설정 (코드 아님)

- 홈 SEO 제목: `건강 | 청각재활연구소` → 예: `청각재활연구소 | Research Institute of Hearing Enhancement`
- 연락처 SEO 제목: `문의 | BUSINESS NAME` → 예: `Contact | 청각재활연구소`
- 대시보드 설정 → 비즈니스 정보 주소: `의학관 318호`, 우편번호 `26426`, `강원특별자치도 원주시 일산로 20`으로 수정
- 헤더 로고 2개의 대체 텍스트(지금은 파일명)와 홈 링크
- HTML 요소마다 '삽입 요소 대체 텍스트' 입력(예: `연구소 소개`, `논문·특허 목록`)
