# 원천 정본화 기록 — `gdm-wo2026128750a1-agent-memory`

원천 취득은 엔진 범위 밖이다(SPEC §9.0 E8). 이 스테이지가 한 일은 **결정론 변환**과
**다이제스트 고정**뿐이며, 아래 목록이 그 전부다.

## 1. 투입물

- 경로: `/home/laptop/projects/workspaces/docent-rehearsal-01-source/input-raw/WO2026-128750A1.txt`
- 원본 SHA-256: `sha256:0c207938d36425f150817327de0723a4c2ae1ea73401f4e6bfb33c9dba6c2228`

## 2. 적용한 변환 (순서가 곧 정의)

| # | 변환 | 내용 | 적용 |
|---|---|---|---|
| 1 | `nfc` | 유니코드 NFC 정규화 | 0 |
| 2 | `nbsp-to-space` | U+00A0(NBSP) → U+0020 치환 | 66 |
| 3 | `drop-invisible-times` | U+2062(INVISIBLE TIMES) 제거 | 0 |
| 4 | `final-newline` | 파일 끝 개행 보장 | 1 |

- 정본 SHA-256: `sha256:64d5d6271d2921e9bf973dec4a8ef997896c4fcdfa120a55a4d305fb25b7154e`

변환 ②③은 특허 내용이 아니라 변환 아티팩트를 지운다. 검사 1(`read.verbatim`)은 이 정본 위에서 정규화 없이 바이트 비교하며, 그 규율은 변하지 않는다.

## 3. 도면 원본

| 파일 | 바이트 | SHA-256 |
|---|---|---|
| `fig-01.png` | 1039953 | `sha256:7fae4a6d92c033d248834e953ef85f2862a74d324ce9500c4fb7bad1e08104d5` |
| `fig-02.png` | 886143 | `sha256:882555daab66d95f1273e6d2edb3e651b3c8b3b903eef2fa94d8f4dffb0f90fd` |
| `fig-03.png` | 1378632 | `sha256:9e69b8df96a278ee6372bfd6359d6b389d4f640d2fa04c216f4295f29f842955` |
| `fig-04.png` | 962616 | `sha256:0dd9a2ff5beff1e7334d9cc94d7e6385a7fd131f13195159a44e5cd2650141ae` |
| `fig-05.png` | 1067922 | `sha256:e43a93814a38076b78fdb7d96ee7b399f061ff5e44a791cc91642e5b6c6a0611` |
| `fig-06.png` | 1327555 | `sha256:91a066d2a8cb6f5b1ca3e780b68e6488dc3ded1cade01f4c8b74ed05b3599bdf` |
| `fig-07.png` | 1031487 | `sha256:ddfc822e61182c1e0db9bfc687eda089a746e3b5a43503d7f69b64e98c0af5ec` |
| `fig-08-09.png` | 1159519 | `sha256:d024d979092ae9be39735040104a242b0e6e9da26622825b880d87f28df402f3` |
| `fig-10.png` | 928576 | `sha256:2e795a6783df746ae1b6633d91ebfc9bbf77c172d9c20fb2c3be38a8de120046` |
| `fig-11.png` | 876657 | `sha256:a68d897fe3b4312ad4c4310056aa3264243733d195a4a8217fe401e8726fba77` |
| `fig-12.png` | 788834 | `sha256:d67b0375f50c2599e98be0f239dbf824e68532953c2abcd6bfe9592a92fe50a9` |
| `fig-13.png` | 890533 | `sha256:2d74c5f3ea43d45d288b9e45e90ce13c0f8a87deb38a1c8639f7a4a9bcc982be` |
| `fig-14.jpg` | 1578351 | `sha256:81eab2bee5f7f98e180f9e3f47932ed31f1e81a3275f902e9e1e4838163bcfb1` |
| `fig-15.jpg` | 1963566 | `sha256:949844c5eeb6709edff5b522b8720402d2d2d6f48eed8f27b7be3b019e71960c` |
| `fig-16.jpg` | 1304812 | `sha256:dd398d3bb8b70b86c04c38b4f7f7b1d39fb25d28f835a68f3dd393985df7d534` |
| `fig-17.jpg` | 1438766 | `sha256:c5b46695194547fa247ce206b6e1f5c4c0042c93ef0fca7358f2b7dd4639a8b9` |
| `fig-18.jpg` | 1992530 | `sha256:5b1bfc831d116b0ba67872643c34289844cb4985cd79ad78f8d68351605bfda8` |
| `fig-19.jpg` | 1873974 | `sha256:6ffd5fe3e3c2b1e900c729cb6dfac9b9f0fb62fd559ab150a69e2d727d1f2816` |
| `fig-20.jpg` | 1592598 | `sha256:cf1183165bee34312f01dac4ddd19f520f4b4be7422243667e543765aa3c3a55` |
| `fig-21.png` | 1105339 | `sha256:da7888f92b14ed91ca48df927b034b1b7103e06f0a1790a395ec08227e6f417c` |

## 4. 공보 종별 코드의 출처 (재정 T10 ⓒ 의 집행)

이 텍스트 추출본은 **공보 표제면을 포함하지 않는다** — 추출본은 `## Biblio. Data` 에서
시작한다. 종별 코드 `A1` 은 표제면
(`(10) International Publication Number: WO 2026/128750 A1`)에서 확인한 값이며
**이 정본 파일 안에는 없다**(문자열 `A1` 의 본문 출현 0건).
근거 재정 = `docs/decisions/ruling-20260901-01-T10.md`.

표제면에만 있는 것 = **종별 코드 · 대리인 · 지정국 · 출원인 주소.**

원천에 없는 값을 슬쩍 넣는 것과 어디서 왔는지 적고 넣는 것은 다르다 — 뒷날
*"`A1` 이 어디서 왔는가"* 를 물으면 답이 이 파일에 있다.

**이 절은 러너 산출 뒤 오케스트레이터가 추기했다**(발주문 v3 §3). 00-source/ 의
write-once 는 러너의 재실행 거부이며, 이 추기는 러너가 만든 파일에 절을 더한 것이다.
다른 파일은 건드리지 않았다.
