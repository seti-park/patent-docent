# 미니 스펙 (검사기 픽스처 — K1·K4 결함판)

이 문서는 `tools/check_spec_refs.py`의 K1(미해소 절 참조)·K4(범위 밖 조항 참조)가
**검출해야 하는** 결함을 각각 1건씩 심은 표본이다.

심은 결함 ①: 존재하지 않는 절을 가리키는 참조 §9.9.
심은 결함 ②: 범위 밖 조항 참조 D99.

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
