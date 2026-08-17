# 미니 스펙 (검사기 픽스처 — 전 검사 통과판)

이 문서는 `tools/check_spec_refs.py`의 K1~K7이 **통과**하는 최소 리포 표본이다.
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
    stages/
  reader/
    schemas/material-spec.schema.json
```

### §6.7 계약 파일 현황표

| 경로 | 상태 | 소관 |
|---|---|---|
| `reader/schemas/material-spec.schema.json` | 현행 | M0.5 |
| `contracts/parameters.yaml` | 현행 | M0.5 |
| `contracts/stages/*.yaml` | 예정 | M2 |
| `contracts/schemas/thread.schema.json` | 예정 | M3 |

## §8 계약 라인

재료 명세 계약 라인은 `material-spec/v0`, 파라미터 계약 라인은 `parameters/v0`이다.
`thread/v0`은 §6.7이 `예정`으로 기록한 계약이므로 아직 실파일이 없다(D6).
