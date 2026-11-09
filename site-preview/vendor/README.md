# site/vendor

페이지가 상대 경로로 부르는 라이브러리입니다. CDN을 쓰지 않고, npm 패키지에서 필요한 파일만 꺼내 버전째로 둡니다.
`tools/build.py` 는 `<script src>` 가 이 폴더의 상대 경로가 아니면 빌드를 멈춥니다.

| 폴더 | 출처 | 파일 | 라이선스 |
|---|---|---|---|
| `gsap@3.15.0/` | npm `gsap@3.15.0` (tarball sha256 `d2e33ad202d4811e9084883f7ff9a27967ac4095caef51ca4c9d20697a253b1c`) | `gsap.min.js`, `SplitText.min.js`, `CustomEase.min.js`, `DrawSVGPlugin.min.js` (패키지의 `dist/`) | GreenSock Standard "no charge" License, https://gsap.com/standard-license |

다시 받거나 버전을 올릴 때(저장소 루트에서):

```
npm pack gsap@<버전>          # registry.npmjs.org 에서 tarball만 받습니다(스크립트 실행 없음)
tar -xzf gsap-<버전>.tgz
mkdir -p site/vendor/gsap@<버전> && cp package/dist/{gsap,SplitText,CustomEase,DrawSVGPlugin}.min.js site/vendor/gsap@<버전>/
```

그 뒤 `tools/core.py` 의 `VENDOR_GSAP` 를 바꾸고 다시 빌드합니다. 새 버전은 나온 지 2주 넘은 것을 씁니다.
