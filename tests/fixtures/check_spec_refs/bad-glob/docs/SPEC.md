# 미니 스펙 (검사기 픽스처 — K2 글로브 결함판)

이 문서는 `ok` 표본에서 **§6.7 글로브 행만** 어긋나게 만든 판이다(재감수 N-02).
K2만 결함을 내야 하며 다른 검사는 오탐하지 않아야 한다.
실제 스펙이 아니며, 검사기 자신의 회귀 표본으로만 쓴다.

## §0 문서 지위

이 표본은 헌장 D1의 정체성 조항과 D15의 굿하트 가드를 근거로 삼는다(D8도 함께 본다).
절 참조는 §6.1·§6.7처럼 쓴다.

## §6 리포 레이아웃

### §6.1 전체 트리

```
mini/
  contracts/
    parameters.yaml
    lexicon/
    stages/
  reader/
    schemas/material-spec.schema.json
```

### §6.7 계약 파일 현황표

| 경로 | 상태 | 소관 |
|---|---|---|
| `reader/schemas/material-spec.schema.json` | 현행 | M0.5 |
| `contracts/parameters.yaml` | 현행 | M0.5 |
| `contracts/lexicon/*.yaml` | 현행 | M0.5 |
| `contracts/stages/*.yaml` | 예정 | M2 |
| `contracts/schemas/thread.schema.json` | 예정 | M3 |

글로브 행의 판정 기준은 매칭 **파일 수**다 — `현행`은 1개 이상, `예정`은 0개.
이 표본은 두 방향을 모두 어긋내 둔다 — `contracts/lexicon/`은 `현행`인데 파일이 없고,
`contracts/stages/`는 `예정`인데 파일이 이미 있다. 부모 디렉터리는 양쪽 다 실재하므로
디렉터리 부재 결함과 구분된다.

## §8 계약 라인

재료 명세 계약 라인은 `material-spec/v0`, 파라미터 계약 라인은 `parameters/v0`이다.
`thread/v0`은 §6.7이 `예정`으로 기록한 계약이므로 아직 실파일이 없다(D6).
