# Pilot Run Sheet: Tool-Call

## Objective

- 가장 빨리 small model 개선을 확인할 수 있는 pilot을 고정한다.
- chaining failure가 데이터 부족인지 모델 한계인지 구분한다.

## Run IDs

- `TC-P0`: dataset expansion / taxonomy tagging
- `TC-P1`: `Qwen3-4B` QLoRA baseline
- `TC-P2`: mixed-depth chaining ablation
- `TC-P3`: optional RL 후보 평가

## Dataset Gate

- missing assets `0`
- strict JSON-only targets 유지
- task taxonomy:
  - single call
  - linear chain
  - fan-out + summarize
  - relative date normalization
  - schema corner case

## Model Matrix

| Run ID | Model | Context | Rank | Dataset Mix | Purpose |
|---|---|---:|---:|---|---|
| TC-P1 | `Qwen3-4B` | 4096 | 32 | mixed | primary student |
| TC-P2 | `Qwen3-4B` | 4096 | 32 | chain-heavy | chaining stress |
| TC-P3 | `Qwen3-8B` | 4096 | 32 | mixed | medium comparator |

## Fixed Decisions

- chat template: official `Qwen3`
- reasoning mode: off
- output: JSON only
- first stage: SFT only
- RL은 `TC-P1` 검토 후에만 추가

## Primary Metrics

- `tool_selection_accuracy`
- `argument_validity`
- `schema_validity`
- `task_success`

## Slice Metrics

- single-call split
- 2-step chain split
- 3+ step chain split
- relative-date split
- nested JSON argument split

## Accept

- `schema_validity >= 0.99`
- hard chaining `task_success >= 0.80`
- `Qwen3-4B`가 8B 대비 현저히 뒤처지지 않음

## Reject

- JSON formatting 오류가 반복됨
- chain depth가 올라갈수록 intermediate binding이 무너짐
- 8B만 유의미하게 버티고 4B는 개선 여지가 없음

## Review Questions

1. 실패가 도구 선택보다 인자 채우기 쪽에 몰려 있는가
2. 상대 날짜 정규화가 별도 subtask로 분리되어야 하는가
3. RL이 format 문제를 푸는지, 아니면 데이터 설계로 먼저 해결되는가
