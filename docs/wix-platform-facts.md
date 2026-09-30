# Wix 플랫폼 확인 사항

[audit.md](audit.md) 2장의 근거입니다. 2026-09-30에 공식 문서(dev.wix.com, support.wix.com)와 게시된 사이트 코드로 확인했고, 다른 에이전트가 출처를 다시 열어 15개 모두 확인했습니다. 검증 단계에서 보완한 내용은 "검증 메모"에 적었습니다.

## Q1-a. Velo HtmlComponent API reference에 있는 속성/메서드 목록은? 높이(height)나 크기를 바꾸는 멤버가 있는가?

공식 API 레퍼런스(2026-02-22 갱신)의 HtmlComponent 멤버는 다음과 같습니다. 속성: allow, scrolling, src, collapsed, deleted, global, hidden, id, isVisible, parent, rendered, type. 메서드: allowFullScreen(), onMessage(), postMessage(), collapse(), delete(), expand(), hide(), onMouseIn(), onMouseOut(), onViewportEnter(), onViewportLeave(), restore(), scrollTo(), show(). 이벤트 타입은 HtmlComponentMessageEvent입니다. height, width, resize 같은 크기 관련 멤버는 없습니다. 크기와 관련된 것은 scrolling 하나뿐이고, 이것도 넘치는 내용을 스크롤바로 보여줄지만 정합니다.

출처:
- https://dev.wix.com/docs/velo/velo-only-apis/$w/html-component/introduction — 사이드바 목록: "allow / scrolling / src / collapsed / deleted / global / hidden / id / isVisible / parent / rendered / type / allowFullScreen() / onMessage() / postMessage() / collapse() / delete() / expand() / hide() / onMouseIn() / onMouseOut() / onViewportEnter() / onViewportLeave() / restore() / scrollTo() / show()"
- https://dev.wix.com/docs/velo/velo-only-apis/$w/html-component/introduction — "The HTML component creates a sandboxed environment (an iframe) that doesn't have direct access to the other elements on your page."
- https://dev.wix.com/docs/velo/velo-only-apis/$w/html-component/scrolling — "Setting the scrolling property sets what happens when the content in the HTML Component is larger than the size of the component."
- https://dev.wix.com/docs/velo/velo-only-apis/$w/html-component/src — "Setting the src property sets the website that's displayed in the HTML Component. The src value must be set to an HTTPS URL."

## Q1-b. Velo 페이지 코드로 HTML iframe 높이를 실행 중에 바꿀 수 있는가? postMessage + $w('#html1').onMessage로 높이를 자동으로 맞출 수 있는가?

둘 다 불가능합니다. postMessage()/onMessage()로 iframe과 페이지 코드가 데이터(예: 내용 높이 숫자)를 주고받을 수는 있습니다. 하지만 받은 값을 적용할 높이 API가 HtmlComponent에 없어서 자동 높이는 만들 수 없습니다. Wix 공식 포럼에서도 Wix 직원이 'iFrame은 크기 조절을 지원하지 않는다'고 답했고, 2024년 Community Manager는 대안으로 Custom Element를 안내했습니다. 라이브 사이트 CSS에도 높이가 고정값으로 박혀 있습니다(Home #html1 = height:450px). collapse()/expand()/hide()/show()로 접거나 숨길 수만 있습니다.

**검증 메모:** '둘 다 불가능'은 Velo 범위에서만 맞습니다. Velo가 아닌 경로가 있습니다. 대시보드의 Settings > Custom Code(Body - end)에 넣은 스크립트는 최상위 페이지 DOM에서 실행됩니다. 이 스크립트가 iframe의 postMessage를 받아 iframe과 상위 wrapper의 style.height를 직접 바꾸는 비공식 우회법이 있습니다. 근거는 forum.wixstudio.com/t/dynamic-height-for-embed-html-or-custom-element-to-resize-with-iframe-content/65727 #9(2026-07-27) "Add Wix Custom Code to the page, placed at Body - end. ... Update the iframe height and its Wix wrapper heights directly."이고, Community Manager가 #10(2026-07-28)에서 "Love this solution"이라고 답했습니다. 다만 공식 API가 아니라 DOM을 조작하는 방식이고, 같은 스레드 #3에는 "although I was able to enlarge the size, I couldn't make it push down the Wix elements below the HTML Component"라는 반대 경험도 있어 아래 요소가 밀리는지는 실측이 필요합니다.

출처:
- https://dev.wix.com/docs/velo/velo-only-apis/$w/html-component/messaging-between-a-site-page-and-an-html-element — "You can use code to send and receive messages between your page and your HTML iFrame element."
- https://forum.wixstudio.com/t/html-iframe-with-dynamic-height/9750 (#2, yisrael-wix, Wix Team, 2018-07-09) — "The HtmlComponent (iFrame) does not support resizing and it is not accessible using HTML properties (ID, CLASS or NAME) of from the DOM."
- https://forum.wixstudio.com/t/html-iframe-with-dynamic-height/9750 (#13, noahlovell, Community Manager, 2024-09-11) — "it's not possible to interact with the DOM when writing code within Wix Studio and Wix. That being said, there is the option of using Custom Elements which provide more functionality than iFrames"
- https://support.wix.com/en/article/wix-editor-embedding-a-site-or-a-widget — "The HTML and URL elements in our editor are iFrames. Therefore, the code or site you are embedding won't be responsive, even if it is originally."
- https://www.smilesnail.org (live HTML, curl 2026-09-30) — "#comp-mne5nuae{width:100%;left:0;margin-left:0;min-width:initial;height:450px;}"

## Q2-a. Custom Element를 라이브 사이트에 표시하려면 무엇이 필요한가(프리미엄 플랜, 연결 도메인, 광고 없음)? 이 사이트는 조건을 충족하는가?

세 가지가 모두 필요합니다: 프리미엄 플랜, 도메인 연결, Wix 광고 없음. 코드도 HTTPS로 제공되어야 합니다. 이 사이트는 라이브 HTML 기준으로 이미 모두 충족합니다(isPremium:true, isPremiumDomain:true, freemiumBanner:false, 도메인 smilesnail.org).

**검증 메모:** 보완: 프리미엄 플랜이 만료되거나 도메인 연결이 끊기면 Custom Element 자리에는 위의 빈 div만 렌더되어 내용이 통째로 사라집니다. 지금의 HtmlComponent 방식에는 이런 의존성이 없습니다.

출처:
- https://support.wix.com/en/article/wix-editor-adding-a-custom-element-to-your-site — "For security reasons, to use the custom element, you must upgrade your site with a Premium Plan, connect a domain and have no ads on it."
- https://dev.wix.com/docs/velo/velo-only-apis/$w/custom-element/introduction — "To use custom elements on your live site, you must have a Premium Plan, connect a custom domain, and remove ads."
- https://www.smilesnail.org (live HTML) — "\"isPremium\":true" / "\"isPremiumDomain\":true" / "\"freemiumBanner\":false" / "\"domain\":\"smilesnail.org\""

## Q2-b. Custom Element는 내용에 맞춰 높이가 바뀌는가, 아니면 에디터에서 정한 높이로 고정되는가?

게시된 사이트에서는 높이를 바꿀 수 있고, 그에 따라 페이지 레이아웃(아래 요소와 페이지 전체 높이)도 바뀝니다. Wix는 이것을 iframe 대비 장점으로 명시합니다. 에디터에서 정한 크기는 배치의 시작 크기일 뿐입니다. 요소가 커질 때 아래 요소가 어떻게 밀리는지는 클래식 에디터 규칙을 따릅니다: 간격이 70px 이하면 간격이 유지되고, 70px를 넘으면 10px까지 줄어듭니다. 에디터 높이보다 작게 줄어드는지는 문서에 나오지 않습니다.

**검증 메모:** 세 곳을 고쳐야 합니다. (1) 'iframe 대비 장점으로 명시'는 과장입니다. 원문의 "(compared to iframe-based components)"는 성능 항목("Improve performance")에만 붙어 있고, 높이 변경 항목에는 없습니다. (2) 70px 규칙 문서는 Custom Element를 언급하지 않는 일반 규칙('elements connected to a dataset' 예시)이므로, Custom Element에 적용된다는 것은 추론입니다. (3) '에디터 높이보다 작게 줄어드는지는 문서에 없다'는 부분은 라이브 컴포넌트 CSS로 답할 수 있습니다. rb_wixui.thunderbolt[CustomElementComponent].eabbd161.min.css 전체가 ".DURcgf>:first-child{width:var(--custom-element-width);min-height:var(--custom-element-height)}"입니다. 즉 에디터 높이는 min-height로 적용되어, 내용이 많으면 커지지만 기본적으로 에디터 높이보다 작아지지는 않습니다. 컨트롤러에는 fixHeight("--custom-element-min-height":"auto !important")와 updateMinHeight도 있습니다. 따라서 에디터에서는 높이를 최소로 잡아 두는 것이 안전합니다.

출처:
- https://support.wix.com/en/article/wix-editor-adding-a-custom-element-to-your-site — "Change the height of your element on your published site, such as to avoid layout collisions on the page."
- https://dev.wix.com/docs/velo/velo-only-apis/$w/custom-element/introduction — "Custom elements can alter the page layout by modifying the page height."
- https://dev.wix.com/docs/develop-websites/articles/wix-editor-elements/formatting-layout/how-page-layout-is-affected-when-elements-change-size — "Gaps that are 70 pixels or less are maintained." / "Gaps that are more than 70 pixels shrink until they reach 10 pixels."

## Q2-c. Custom Element는 페이지 DOM에 렌더되는가, iframe 안에 렌더되는가?

에디터와 미리보기에서는 보안상 iframe 안에 렌더된다고 문서에 명시되어 있습니다. 라이브 사이트에서는 iframe 없이 페이지에 직접 붙는 것으로 보입니다. 근거는 세 가지입니다: 문서가 'iframe 기반 컴포넌트보다 성능이 좋다'고 하고, 'Shadow DOM을 쓰지 않으면 페이지 스타일시트가 적용된다'고 하며, 사이트 테마가 '웹 페이지의 CSS 변수'로 노출된다고 합니다. 다만 '라이브에서는 페이지 DOM'이라는 문장이 직접 있지는 않으므로, 이 부분은 문서에서 추론한 것입니다. 실무상 결과는 두 가지입니다: 실제 모습은 게시된 사이트나 테스트 사이트에서만 확인할 수 있고, Wix 전역 CSS와 섞이지 않게 하려면 Shadow DOM을 쓰는 것이 좋습니다.

**검증 메모:** status를 unclear에서 confirmed로 올려도 됩니다. 근거는 문서 추론이 아니라 라이브 렌더러 코드(o.createElement(n,C), iframe 없음)입니다.

출처:
- https://support.wix.com/en/article/wix-editor-adding-a-custom-element-to-your-site — "For security reasons, the custom element is rendered inside an iFrame inside the Editor and in preview mode. This might affect the layout of the component."
- https://dev.wix.com/docs/velo/velo-only-apis/$w/custom-element/introduction — "Custom elements might appear differently in preview and live sites because they are rendered in an iframe during editor and preview modes."
- https://support.wix.com/en/article/wix-editor-adding-a-custom-element-to-your-site — "Improve performance (compared to iframe-based components)."
- https://dev.wix.com/docs/build-apps/develop-your-app/extensions/site-extensions/site-widgets/connect-a-custom-element-s-colors-and-fonts-to-a-site-theme — "Normally, the theme stylesheet is automatically included with the webpage, ensuring consistent styling across the site. However, when working with custom elements that use a shadow DOM or an internal iframe, the page's stylesheet may be inaccessible."

## Q2-d. Custom Element의 소스로 Velo 파일(public/custom-elements)을 쓸 수 있는가? 외부 URL은?

둘 다 됩니다. (1) Wix 호스팅: public/custom-elements/ 폴더에 JS 파일을 만들고 Choose Source → Velo file을 고릅니다. Wix가 이 방식을 권장합니다. (2) 외부 호스팅: Choose Source → Server URL에 HTTPS JS 파일 주소를 넣습니다. 어느 쪽이든 customElements.define()에 쓴 이름과 똑같은 Tag Name을 입력해야 합니다. Velo를 쓰지 않으면 코드를 직접 호스팅해야 합니다. 이 사이트는 Velo Dev Mode가 이미 켜져 있습니다(아래 Q6 참고).

**검증 메모:** 사소한 보정 두 가지입니다. (1) support 문서의 메뉴 경로는 "Click Embed Code. Click the Custom Element"로, Velo 문서의 'Popular Embeds' 경로와 다릅니다. (2) 'Velo Dev Mode가 이미 켜져 있다'의 근거(wixCodePageIds, 페이지 코드 번들)는 사이트에 Velo 코드가 있다는 것까지만 증명합니다. 지금 에디터에서 Dev Mode 토글이 켜져 있는지는 라이브 HTML로 알 수 없습니다.

출처:
- https://dev.wix.com/docs/velo/velo-only-apis/$w/custom-element/add-a-custom-element — "In the editor or your local IDE, create a file in the public/custom-elements/ directory."
- https://dev.wix.com/docs/velo/velo-only-apis/$w/custom-element/add-a-custom-element — "Wix Editor: Select Add Elements > Embed > Popular Embeds > Custom Element." / "Select the element, click Choose Source, and select Velo file." / "If you don't see your file, make sure that it's located in the public/custom-elements directory."
- https://dev.wix.com/docs/velo/velo-only-apis/$w/custom-element/add-a-custom-element — "Select the element, click Choose Source, and select Server URL." / "Enter the Tag Name exactly as it appears in customElements.define()."
- https://dev.wix.com/docs/velo/velo-only-apis/$w/custom-element/introduction — "Wix-hosted (recommended): Integrates directly with your Wix site, simplifies deployment"
- https://support.wix.com/en/article/wix-editor-adding-embeds-and-custom-elements-to-your-mobile-site — "The custom element code must be hosted by you if you are not using Velo."

## Q2-e. Custom Element는 모바일(클래식 모바일 에디터)에서 어떻게 동작하는가?

데스크톱에 추가한 Custom Element와 임베드는 모바일 레이아웃으로 그대로 넘어옵니다. 다만 '다르게 보일 수 있으니' 필요하면 데스크톱 요소를 숨기고 모바일 전용 요소를 따로 추가하라고 안내합니다. 모바일 에디터에서 추가한 요소는 모바일 전용이고 데스크톱에는 나오지 않습니다. 이 사이트의 모바일 페이지는 viewport가 width=320으로 고정되어 있습니다. 그래서 페이지 DOM에서 동작하는 Custom Element 하나가 CSS 미디어쿼리로 320px 화면에 맞추도록 만들면 데스크톱과 모바일을 함께 처리할 수 있습니다(이 부분은 추론).

**검증 메모:** 추론 부분 보완: 라이브에서는 페이지 DOM에 렌더되므로 미디어쿼리는 320px 페이지 viewport를 기준으로 동작합니다. 다만 요소의 폭과 최소 높이(--custom-element-width / --custom-element-height, min-height)는 레이아웃별로 따로 정해지므로, 모바일 에디터에서 모바일 높이를 따로 작게 잡아야 합니다. 그렇지 않으면 모바일 에디터 높이만큼의 빈 공간이 최소로 남습니다.

출처:
- https://support.wix.com/en/article/wix-editor-adding-embeds-and-custom-elements-to-your-mobile-site — "Custom elements and embeds that you have added to your desktop site may be displayed differently on your mobile site."
- https://support.wix.com/en/article/wix-editor-adding-embeds-and-custom-elements-to-your-mobile-site — "Elements added from the mobile editor are mobile-only. This means they are not displayed on the desktop version of your site."
- https://www.smilesnail.org (live HTML, iPhone UA) — "<meta name=\"viewport\" content=\"width=320, user-scalable=yes\" id=\"wixMobileViewport\" />"

## Q3-a. HTML iframe '웹사이트 주소' 모드로 GitHub Pages(https) 페이지를 띄울 수 있는가? GitHub Pages의 X-Frame-Options나 CSP가 막는가?

막지 않습니다. github.io 응답 헤더를 curl로 확인했는데 X-Frame-Options도, Content-Security-Policy(frame-ancestors)도 없었습니다. access-control-allow-origin: * 와 cache-control: max-age=600이 붙어 있습니다. Wix 쪽 조건은 HTTPS URL뿐이고, 삽입을 금지하는 사이트는 Wix 안에서 우회할 수 없다고 안내합니다. GitHub Pages 제약도 있습니다: 무료 플랜에서는 저장소가 public이어야 하고(현재 Doomsfrooky/WIX_DEV는 비로그인 상태에서 HTTP 200으로 열림), 상업용 호스팅으로 쓰는 것은 금지이며, 월 100GB 소프트 대역폭 제한이 있습니다.

**검증 메모:** 보완할 점이 두 가지 있습니다. (1) GitHub의 금지 대상은 '상업용 호스팅' 전반이 아니라 "online business, e-commerce site, or any other website that is primarily directed at either facilitating commercial transactions or providing commercial software as a service (SaaS)"입니다. 연구소 소개 콘텐츠는 여기에 해당하지 않을 가능성이 큽니다. (2) 현재 https://doomsfrooky.github.io/WIX_DEV/ 는 HTTP 404라서 Pages가 아직 켜져 있지 않습니다. 이 방식을 쓰려면 먼저 Pages를 활성화해야 합니다. 그 밖의 제한으로 "Published GitHub Pages sites may be no larger than 1 GB."와 "soft limit of 10 builds per hour"가 있습니다.

출처:
- curl -sI https://pages.github.com/ , https://octocat.github.io/ (2026-09-30) — 헤더: "server: GitHub.com", "access-control-allow-origin: *", "cache-control: max-age=600" (x-frame-options / content-security-policy 없음)
- https://support.wix.com/en/article/wix-editor-embedding-a-site-or-a-widget — "Only HTTPS codes and URLs are displayed." / "Some sites have security policies that forbid them from being embedded on external platforms such as Wix. ... it is not possible to bypass this within Wix."
- https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site — "If the account that owns the repository uses GitHub Free or GitHub Free for organizations, the repository must be public."
- https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits — "GitHub Pages is not intended for or allowed to be used as a free web-hosting service to run your online business" / "GitHub Pages sites have a soft bandwidth limit of 100 GB per month."

## Q3-b. Wix가 HtmlComponent iframe에 붙이는 sandbox 속성은 무엇인가?

공식 문서에는 sandbox 속성 목록이 없습니다. Velo 문서의 'sandboxed environment (an iframe)'라는 표현은 다른 출처(origin)라서 페이지에 접근할 수 없다는 뜻으로 쓰인 것입니다. 라이브 사이트에서는 페이지 설정 요청에 useSandboxInHTMLComp=false가 들어 있습니다. HtmlComponent 속성 데이터에도 url과 "allow":"fullscreen"만 있고 sandbox는 없습니다. 즉 이 사이트에서는 sandbox 속성이 붙지 않는 것으로 보이지만, 공식 출처로는 확인할 수 없습니다.

**검증 메모:** 근거를 더 보강할 수 있습니다. 라이브 렌더러 rb_wixui.thunderbolt[HtmlComponent].0451e486.bundle.min.js는 props의 sandbox를 그대로 전달합니다("iframe",{ref:w,sandbox:f,className:"xxJnkq",scrolling:c,title:d||v.title,name:"htmlComp-iframe",width:"100%",height:"100%",allow:i,"data-src":l}). 그런데 이 사이트의 props에는 sandbox가 없으므로 iframe에 sandbox 속성이 붙지 않는다는 것이 코드로도 확인됩니다.

출처:
- https://www.smilesnail.org (live HTML) — "staticHTMLComponentUrl=https%3A%2F%2Fwww-smilesnail-org.filesusr.com%2F&useSandboxInHTMLComp=false"
- siteassets.parastorage.com features_jemzh (라이브 페이지가 불러오는 JSON) — "\"comp-mne5nuae\":{\"componentConsentPolicy\":\"essential\",\"url\":\"https://www-smilesnail-org.filesusr.com/html/b8629b_917e96e8e6c666926c81ca9d2cee555a.html\",\"allow\":\"fullscreen\""
- https://dev.wix.com/docs/velo/velo-only-apis/$w/html-component/allow — "fullscreen: Allows the HTML Component content to request fullscreen mode. By default, fullscreen isn't allowed unless explicitly permitted."

## Q3-c. 외부 URL(GitHub Pages) 방식에서는 Wix를 다시 게시하지 않아도 내용 변경이 반영되는가? 지금 쓰는 '코드' 방식과는 무엇이 다른가?

외부 URL 방식에서는 Wix에 URL만 저장되고, 방문자 브라우저가 그 URL을 매번 새로 불러옵니다. 그래서 GitHub에 push한 뒤 GitHub Pages 배포(최대 약 10분)와 캐시(max-age=600)만 지나면 Wix를 다시 게시하지 않아도 반영됩니다. 이것은 동작 구조에서 나온 결론이고, Wix 문서에 이 문장이 그대로 있지는 않습니다. 반대로 지금 쓰는 '코드' 방식은 코드를 filesusr.com에 내용 해시를 파일명으로 한 불변(immutable) 파일로 저장합니다. 그래서 코드를 고치면 새 파일이 생기고, 반드시 Wix를 다시 게시해야 합니다. 높이 고정 문제는 어느 방식이든 그대로입니다(Q1-b).

출처:
- https://dev.wix.com/docs/velo/velo-only-apis/$w/html-component/src — "Setting the src property sets the website that's displayed in the HTML Component."
- https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site — "It can take up to 10 minutes for changes to your site to publish after you push the changes to GitHub."
- curl -sI https://www-smilesnail-org.filesusr.com/html/b8629b_917e96e8e6c666926c81ca9d2cee555a.html — "cache-control: public, max-age=15552000, immutable" / "etag: \"917e96e8e6c666926c81ca9d2cee555a\""

## Q4-a. Wix Git Integration은 새 저장소만 만들 수 있는가(기존 저장소를 연결할 수 없는가)? 전제 조건은?

공식 문서에 나온 절차는 Velo에 권한을 준 뒤 '새 repo'를 만드는 것뿐입니다. 기존 저장소(예: Doomsfrooky/WIX_DEV)를 연결하는 방법은 어느 문서에도 없습니다. 전제 조건은 다음과 같습니다: Velo Dev Mode가 켜져 있어야 하고(이 사이트는 이미 켜짐), Velo Packages를 쓰고 있으면 연결할 수 없으며, 로컬 환경에 Node 20.11 이상, Git, npm 또는 yarn, GitHub SSH 키가 있어야 합니다. 연결한 뒤 repo를 지우거나 Velo 앱 권한을 회수하면 복구할 수 없게 깨질 수 있다고 경고합니다.

**검증 메모:** 더 직접적인 근거가 있습니다. disconnect-your-site-from-git-hub 문서의 "Once you disconnect your site from GitHub and from a repo, you can't reconnect the site to that repo again. If you reconnect your site to GitHub later, a new repo is created."와 fixing-a-broken-git-hub-integration 문서입니다. 후자에 따르면 repo 삭제뿐 아니라 이름 변경이나 다른 계정으로 이전해도 연결이 끊기고 원래 repo로는 재연결할 수 없습니다. 반면 Velo 앱 접근 권한 회수는 권한을 다시 주면 복구된다고 되어 있어, setup 문서의 경고보다 완화된 설명입니다.

출처:
- https://dev.wix.com/docs/develop-websites/articles/workspace-tools/developer-tools/git-integration-wix-cli-for-sites/setting-up-git-integration-wix-cli-for-sites — "Follow the prompts to sign in to your GitHub account and authorize Velo to create a new repo for you." / "Choose an owner and enter a name for the new repo to connect to your site."
- https://dev.wix.com/docs/develop-websites/articles/workspace-tools/developer-tools/git-integration-wix-cli-for-sites/about-git-integration-wix-cli-for-sites — "Wix sets up a repository for your project, which you can clone to your computer"
- https://dev.wix.com/docs/develop-websites/articles/workspace-tools/developer-tools/git-integration-wix-cli-for-sites/setting-up-git-integration-wix-cli-for-sites — "You can't connect your site to GitHub if you have Velo Packages set up on your site." / "Node, version 20.11 or later." / "Wix Editor: Click the GitHub Integration icon in the Code sidebar and then Connect to GitHub."

## Q4-b. Git Integration을 켜면 에디터의 코드는 읽기 전용이 되는가?

네. GitHub에 연결된 동안 에디터는 read-only 모드가 됩니다. 코드 파일은 수정하거나 추가할 수 없고, 로컬 IDE에서 고쳐서 기본 브랜치에 push해야 에디터에 반영됩니다. 반영까지 지연이 있을 수 있습니다. 디자인(요소 추가·수정)은 계속 편집할 수 있고, 편집할 때마다 새 UI version이 생깁니다.

출처:
- https://dev.wix.com/docs/develop-websites/articles/workspace-tools/developer-tools/git-integration-wix-cli-for-sites/changes-to-the-editor-when-your-site-is-integrated — "While your site is connected to GitHub, the editor is in read-only mode. This involves the following changes: Code files are read-only. You can't make any changes to your site's code or add new files."
- https://dev.wix.com/docs/develop-websites/articles/workspace-tools/developer-tools/git-integration-wix-cli-for-sites/publishing-a-site-with-git-integration-wix-cli-for-sites — "To sync your code with the editor, push a commit to your repo's default branch." / "There may be a delay between when you push a commit to GitHub and when it appears in the editor."

## Q4-c. Git Integration으로 무엇이 동기화되는가? HTML iframe 요소 안의 코드도 동기화되는가?

동기화되는 것은 Code 사이드바의 세 영역, 즉 src/pages(페이지 코드와 masterpage.js), src/backend, src/public(public/custom-elements 포함)뿐입니다. 그 밖의 위치에 둔 파일은 무시됩니다. HTML iframe 요소의 코드는 코드 파일이 아니라 요소 설정이고, 디자인 스냅샷인 'UI version'에 들어갑니다. repo에는 UI version 번호만 wix.config.json에 기록되므로 HTML iframe 코드는 동기화되지 않습니다. '동기화 안 됨'이라는 문장이 직접 있지는 않고, 문서의 구조 설명에서 도출한 결론입니다. 게시 방법에 따라 쓰이는 UI 버전이 다르다는 점도 주의해야 합니다: 에디터에서 게시하면 최신 UI 버전이, CLI로 게시하면 wix.config.json에 적힌 UI 버전이 쓰입니다. GitHub Actions에서 API 키(권한: 'Wix CLI for Sites - Git Integration')로 npm run wix publish를 실행해 게시를 자동화할 수 있습니다.

**검증 메모:** 실무상 위험을 덧붙이면 다음과 같습니다. CLI나 GitHub Actions로 게시하면 wix.config.json의 UI version이 쓰입니다. 그래서 그 뒤 에디터에서 고친 HTML iframe 코드(=디자인)는 게시에서 빠지거나 이전 버전으로 되돌아갈 수 있습니다.

출처:
- https://dev.wix.com/docs/develop-websites/articles/workspace-tools/developer-tools/git-integration-wix-cli-for-sites/git-hub-repository-file-structure — "The repo's file structure matches the public, backend, and page code sections in the Code sidebar (Wix Editor)." / "Add your code in either the Pages, Backend, or Public folders. Files or folders added to the root of the src folder are ignored."
- https://dev.wix.com/docs/develop-websites/articles/workspace-tools/developer-tools/git-integration-wix-cli-for-sites/about-the-local-editor — "UI versions are snapshots of a site's design. Saving any design changes to a site including adding a new page or adding or modifying elements generates a new UI version." / "The current UI version for the code in your site's repo is indicated in the wix.config.json file."
- https://dev.wix.com/docs/develop-websites/articles/workspace-tools/developer-tools/git-integration-wix-cli-for-sites/publishing-a-site-with-git-integration-wix-cli-for-sites — "EditorThe code in the default branch of your site's repo.The latest UI version" / "CLI - Latest commitThe code in the default branch of your site's repo.The UI version indicated in the wix.config.json file in your site's repo."
- https://dev.wix.com/docs/develop-websites/articles/workspace-tools/developer-tools/git-integration-wix-cli-for-sites/set-up-git-hub-actions-to-work-with-the-wix-cli-for-sites — "Select the Wix CLI for Sites - Git Integration site permission" / "Include npm run wix publish in your workflow to publish the site based on the repo's default branch."

## Q5. 클래식 모바일 에디터에서 하나의 HTML iframe 요소를 데스크톱과 모바일에 함께 쓸 수 있는가(별도 mobileHtml1 없이)? '모바일 전용'과 '모바일에서 숨김'은 어떻게 동작하는가?

함께 쓸 수 있습니다. 데스크톱에 추가한 요소는 자동으로 모바일에도 나타납니다. 모바일 에디터에서는 요소의 크기와 위치만 따로 조정하고, 코드와 내용은 공유합니다. 모바일에서 바꾼 디자인은 데스크톱에 영향을 주지 않습니다. '모바일에서 숨김'은 요소를 지우는 것이 아니라 Hidden on Mobile 패널로 옮기는 것이고, 삭제는 데스크톱 에디터에서만 할 수 있습니다. 모바일 에디터에서 추가한 요소(지금의 mobileHtml1)는 모바일 전용입니다. 라이브에서 확인한 결과, 모바일 홈 HTML에는 모바일 전용 HtmlComponent(comp-mnfop8lu, width:320px, height:1493px)만 있습니다. 데스크톱 #html1(comp-mne5nuae)은 0회 등장하므로 현재 모바일에서 숨겨진 상태입니다. 한 요소로 합쳐도 iframe 높이는 데스크톱과 모바일 레이아웃에서 각각 고정값이라, 320px 폭에서의 높이를 모바일 레이아웃에서 따로 맞춰야 합니다.

출처:
- https://support.wix.com/en/article/wix-editor-about-the-mobile-editor — "Your mobile view is a reflection of your desktop view, which means it displays all the same elements and content." / "The design changes you make on mobile don't affect your desktop version."
- https://support.wix.com/en/article/wix-editor-hidden-elements-in-your-mobile-editor — "Hiding desktop elements on your mobile site does not delete them. If you want to delete an element, you must do it from the desktop editor."
- https://support.wix.com/en/article/wix-editor-adding-and-customizing-mobile-only-elements — "As mobile-only elements don't appear on your desktop site, you can design them as you wish"
- https://support.wix.com/en/article/wix-editor-adding-embeds-and-custom-elements-to-your-mobile-site — "If your element isn't displayed properly on the mobile version of your site, we recommend hiding the desktop version, and re-adding a mobile-friendly alternative"
- https://www.smilesnail.org (live HTML, iPhone UA) — "#comp-mnfop8lu{width:320px;height:1493px;}" 그리고 comp-mne5nuae 0회 등장

## Q6. 이 사이트는 어떤 에디터로 만들었는가(클래식 Wix Editor / Wix Studio / Editor X / Wix Harmony)? 코드 관련 상태는?

클래식 Wix Editor입니다. 근거는 라이브 HTML의 다음 값들입니다: "isResponsive":false, "isStudio":false, "editorName":"Unknown", 섹션 타입 ClassicSection, 스타일 번들 rb_wixui.thunderbolt_bootstrap-classic. Wix 자체 코드도 editorName이 "Studio"일 때만 wix-studio로, isResponsive일 때만 thunderbolt-responsive로 분류하는데 이 사이트는 둘 다 아닙니다. 모바일 viewport가 width=320으로 고정되어 있고 모바일 전용 요소가 따로 있는 것도 클래식 모바일 에디터의 특징입니다. Harmony는 데스크톱 디자인을 모든 화면에 자동으로 맞추는 방식입니다. Velo Dev Mode는 이미 켜져 있습니다: Home(jemzh)과 Audiso(xmx29)에 페이지 코드 파일이 있지만, 내용은 빈 $w.onReady뿐입니다. HtmlComponent 자리는 서버 렌더 HTML에 빈 div로만 있고 iframe은 브라우저에서 나중에 삽입되므로, 본문 텍스트는 페이지 HTML 자체에 들어 있지 않습니다.

**검증 메모:** 사소한 보정: 'Velo Dev Mode는 이미 켜져 있다'의 근거(isWixCodeOnSite=true, 페이지 코드 번들)는 사이트에 Velo 코드가 있다는 것까지만 증명합니다. 에디터의 Dev Mode 토글이 현재 켜져 있는지는 라이브 HTML로 확인할 수 없습니다.

출처:
- https://www.smilesnail.org (live HTML) — "\"siteType\":\"UGC\",\"dc\":\"virginia-usercode\",\"isResponsive\":false,\"editorName\":\"Unknown\"" / "\"accessibilityBrowserZoom\":{\"isBuilder\":false,\"isStudio\":false}"
- https://www.smilesnail.org (live HTML) — "componentId:`${\"Studio\"===window.fedops.data.site.editorName?\"wix-studio\":`thunderbolt${window.fedops.data.site.isResponsive?\"-responsive\":\"\"}`}`"
- https://www.smilesnail.org (live HTML) — "data-block-level-container=\"ClassicSection\"" / "rb_wixui.thunderbolt_bootstrap-classic.95bff5e0.min.css"
- https://www.smilesnail.org (live HTML) — "\"wixCodePageIds\":[\"xmx29\",\"jemzh\"]"; bundler-velo.parastorage.com .../pages_delimiter_jemzh.js 내용 — "return $w.onReady((function(){})),{}"
- https://www.smilesnail.org (live HTML) — "<div id=\"comp-mne5nuae\" class=\"O5G82F comp-mne5nuae\"></div>"
- https://support.wix.com/en/article/wix-harmony-editor-adjusting-your-site-for-mobile — "your design on desktop is automatically adjusted to fit all screens."

## 검증 단계에서 추가로 확인된 제약

- [높이 자동 조절의 비공식 경로 누락] Velo 말고 대시보드 Settings > Custom Code(Body - end)로 최상위 페이지에 스크립트를 넣는 경로를 다루지 않았습니다. 이 스크립트가 iframe의 postMessage를 받아 iframe과 wrapper 높이를 직접 바꾸는 우회법이 있고, Wix Community Manager가 긍정했습니다: forum.wixstudio.com/t/dynamic-height-for-embed-html-or-custom-element-to-resize-with-iframe-content/65727 #9(2026-07-27) "Add Wix Custom Code to the page, placed at Body - end. ... Update the iframe height and its Wix wrapper heights directly." / #10(2026-07-28) "Love this solution". 전제 조건은 support 문서 embedding-custom-code-on-your-site의 "Make sure that your site is published and has a connected domain."이고, 주의점은 "If you assign a different domain to your site, your code snippets will be deleted."입니다. 라이브 배치는 CSS grid이며 position:relative입니다("[data-mesh-id=comp-mne5novuinlineContent-gridContainer] > [id=\"comp-mne5nuae\"]...{position:relative;margin:0px 0 0px 0;left:0;grid-area:1 / 1 / 2 / 2;...}"). 다만 같은 스레드 #3은 "I couldn't make it push down the Wix elements below the HTML Component"라고 보고했으므로, 아래 요소가 밀리는지는 실측해야 합니다.
- [Custom Element 높이는 min-height] 라이브 CSS rb_wixui.thunderbolt[CustomElementComponent].eabbd161.min.css의 전체 내용이 ".DURcgf>:first-child{width:var(--custom-element-width);min-height:var(--custom-element-height)}"입니다. 에디터에서 정한 높이는 고정값이 아니라 최소 높이이므로, 내용이 많으면 커지지만 에디터 높이보다 작아지지는 않습니다. 에디터와 모바일 레이아웃 모두에서 높이를 작게 잡아야 빈 공간이 생기지 않습니다.
- [프리미엄 만료 시 Custom Element 내용 소실] 라이브 렌더러 rb_wixui.thunderbolt[CustomElementComponent].14b8cde6.bundle.min.js는 조건을 충족하지 못하면 (0,e.jsx)("div",{id:i,"wix-disabled-custom-element-reason":"required-wix-premium-account"})만 렌더합니다. 본문 전체를 Custom Element로 옮기면 플랜이 만료되거나 도메인 연결이 끊길 때 모든 페이지 본문이 빈칸이 됩니다. 지금의 HtmlComponent는 이 조건에 의존하지 않습니다.
- [SEO] Velo custom-element intro 문서: "SEO for custom elements is handled through Velo code by defining seoMarkup. ... Without proper SEO markup, only JavaScript-enabled crawlers, like Google, will index the content." 지금의 HtmlComponent도 서버 HTML에는 <div id="comp-mne5nuae" class="O5G82F comp-mne5nuae"></div>만 있습니다. 렌더러가 마운트된 뒤에만 <wix-iframe data-src=...>를 삽입하므로(r.useEffect(()=>h(!0),[]); x&&..."wix-iframe"), 본문 텍스트가 페이지 HTML에 없습니다. 이전 방식을 고를 때 seoMarkup을 쓸지도 함께 정해야 합니다.
- [2025-12 프론트엔드 보안 제약] support 문서 embedding-custom-code-on-your-site: "In December 2025, Wix introduced new frontend security measures for custom code ... This change affects all types of custom code, including dashboard custom code, embedded code, and Velo code." dev.wix.com/docs/develop-websites-sdk/code-your-site/best-practices/about-frontend-security(Last updated: 24 March 2026): "The srcdoc attribute is blocked. Attempts to set srcdoc on an iframe result in an error." / "iframes opened on the same domain as the site, or without a specified domain, are automatically sandboxed." / URL, JSON, addEventListener 등 전역 객체 잠금. 따라서 Custom Element 안에 기존 HTML을 srcdoc iframe으로 감싸는 식의 이전은 동작하지 않습니다.
- [접근성: 모든 HtmlComponent의 iframe title이 영어 기본값 'Embedded Content'] 렌더러 코드는 title:d||v.title입니다. Home features JSON에서 comp-mne5nuae, comp-mne5p5wh, comp-mne5rrh7의 props에는 title이 없고("url":...,"allow":"fullscreen" 다음에 바로 translations가 옴), translations에는 "title":"Embedded Content"가 있습니다. 그래서 스크린리더가 한국어 사이트의 모든 본문 프레임을 똑같이 'Embedded Content'로 읽습니다. 해결: support 문서 wix-editor-embedding-a-site-or-a-widget의 "(Optional) Enter alt text for the embed under What's in the embed?" 입력란에 요소별로 한국어 설명을 넣습니다(심각도 medium).
- [GitHub Pages 미활성] https://doomsfrooky.github.io/WIX_DEV/ 는 curl 결과 HTTP/2 404입니다. Q3의 URL 방식을 쓰려면 먼저 저장소 설정에서 Pages를 켜야 합니다. 저장소가 public이므로 소스 전체가 공개된다는 점도 전제로 두어야 합니다.
- [Git Integration 재연결 불가] disconnect-your-site-from-git-hub 문서: "Once you disconnect your site from GitHub and from a repo, you can't reconnect the site to that repo again. If you reconnect your site to GitHub later, a new repo is created." fixing-a-broken-git-hub-integration 문서에 따르면 repo 이름 변경이나 다른 계정으로 이전해도 연결이 끊깁니다. 기존 Doomsfrooky/WIX_DEV를 Wix 코드 저장소로 쓸 수 없을 뿐 아니라, 한 번 끊으면 새 repo로 갈아타야 합니다.
