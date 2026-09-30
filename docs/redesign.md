# 사이트 개편 (시안 2단계)

새 디자인은 `site/` 폴더에 있습니다. 1단계 수정(`embeds/`, [paste-list.md](paste-list.md))과는 별개이며, 아직 사이트에 적용하지 않은 시안입니다.

## 무엇이 달라졌나

- **파일 하나로 데스크톱과 모바일을 모두 처리합니다.** 같은 파일을 데스크톱 요소와 모바일 요소에 붙이면 되므로, 모바일 사본이 따로 어긋나는 일이 없습니다.
- **한국어와 영어가 한 파일에 들어 있습니다.** 어느 언어를 보여 줄지는 Wix 페이지가 알려 줍니다(아래 영어 페이지 설정).
- **데이터는 한 곳에서 관리합니다.** 논문·학회 발표·특허·구성원은 `data/*.json`에 있습니다. 논문 1편을 추가하면 Research, 해당 연구실 페이지, 홈의 논문 수가 함께 바뀝니다.
- **긴 목록은 10개씩 넘겨 봅니다.** 펼치는 방식이 아니라서 iframe 높이가 거의 일정하고, 잘리거나 스크롤바가 생기지 않습니다. 팀·연도 필터 버튼은 데이터에서 자동으로 만들어집니다(최근 5개 연도 + 그 이전).
- **글꼴은 IBM Plex Sans KR / IBM Plex Mono(Google Fonts)로 통일했습니다.** 필요한 글자만 받아 가벼우며, 기기마다 영문 글꼴이 달라지던 문제가 없습니다.

## 고치고 다시 만드는 법

1. 목록을 바꿀 때는 `data/publications.json`, `reports.json`, `patents.json`, `people.json`을 고칩니다. 소개 문구는 `tools/build.py` 안에 한국어·영어가 나란히 있습니다.
2. `python3 tools/build.py`를 실행하면 `site/*.html`이 다시 만들어집니다. `--preview`를 붙이면 오른쪽 아래에 KO/EN 전환 버튼이 있는 미리보기(`site-preview/`)가 만들어집니다.
3. 바뀐 파일을 Wix 요소에 붙여넣고 게시합니다.

## Wix에 적용하는 순서 (결정 후)

1. 페이지마다 데스크톱 요소 하나(`#html1`)에 `site/<페이지>.html`을 붙이고 높이를 아래 표대로 맞춥니다. 홈과 About처럼 요소가 여러 개인 페이지는 나머지 HTML 요소(`#html2` 등)를 지웁니다.
2. 모바일 에디터에서 모바일 요소(`#mobileHtml1`)에 같은 파일을 붙이고 모바일 높이를 맞춥니다.
3. 게시합니다.

높이는 한국어·영어, 목록의 모든 페이지·필터 중 가장 긴 경우에 20px를 더한 값입니다.

| 페이지 | 파일 | 데스크톱 높이(px) | 모바일 높이(px) |
|---|---|---|---|
| Home | `site/home.html` | 2,700 | 4,250 |
| About | `site/about.html` | 1,820 | 2,260 |
| Research | `site/research.html` | 4,630 | 7,880 |
| People | `site/people.html` | 3,100 | 5,490 |
| Basic Lab | `site/basic-lab.html` | 3,740 | 5,330 |
| Hearing Lab | `site/hearing-lab.html` | 4,350 | 6,420 |
| HeAD Lab | `site/head-lab.html` | 4,590 | 6,930 |
| Audiso | `site/audiso.html` | 3,000 | 5,310 |
| Contact | `site/contact.html` | 1,290 | 1,470 |

## 영어 페이지 설정

1. Wix 대시보드에서 **Wix Multilingual**을 추가하고 영어를 두 번째 언어로 켭니다. 영어 페이지 주소는 `/en/...` 형식을 가정했습니다(다르면 `tools/build.py`의 링크 규칙만 바꾸면 됩니다).
2. 각 페이지의 Velo 페이지 코드(에디터 아래 코드 패널)에 아래를 넣어, iframe에 현재 언어를 알려 줍니다. 요소 ID는 페이지에 맞게 바꿉니다.

```js
import wixWindow from 'wix-window';

$w.onReady(function () {
  const lang = wixWindow.multilingual.currentLanguage; // 'ko' 또는 'en'
  ['#html1', '#mobileHtml1'].forEach(id => {
    const el = $w(id);
    if (el && el.postMessage) el.postMessage({ lang });
  });
});
```

3. 메뉴, 헤더 로고 옆 글자, SEO 제목 같은 Wix 기본 요소는 Multilingual의 번역 관리자에서 영어로 입력합니다.

이 방식은 공식 API(`postMessage`, `wixWindow.multilingual`) 범위이지만 이 사이트에서 실제로 동작하는지는 적용할 때 한 페이지로 먼저 확인해야 합니다.

## 확인이 필요한 것

- **영어 문구:** 연구 분야, 연구실 소개, Mission·Vision, 직함 등 영어는 제가 쓴 초안입니다. 특히 교수님 직함과 학과명 영문 표기는 공식 표기를 확인해 주세요.
- **구성원 영문 이름:** 논문 저자 목록에서 확인되는 9명만 영문으로 넣었습니다(서영준, 공태훈, 기재홍, 변유선, 이동혁, 윤철영, 이현수, 전진희, 강철영). 나머지는 영어 페이지에서도 한글로 표시됩니다. 영문 표기를 알려 주시면 `tools/build.py`의 `NAME_EN`에 넣겠습니다.
- **사진:** 새 구성원 7명은 사진 대신 성을 표시합니다. 사진은 여전히 imgur에 있어 무겁고(원본 그대로), 영국에서는 보이지 않습니다.
- **홈의 Wix 기본 요소:** 소개 영상, 2019년 기준 인포그래픽 3장, 디지털 치료제 책 소개를 새 홈에서 어떻게 할지 정해야 합니다.
- **Research 학회 발표 제목**은 원본 데이터 그대로입니다(일부 학회명이 원본에서 '...'로 잘려 있음).
