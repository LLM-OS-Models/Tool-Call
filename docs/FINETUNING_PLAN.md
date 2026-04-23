# Finetuning Plan: Tool-Call

## Current State

- 현재 7개 프로젝트 중 가장 빨리 개선을 확인할 수 있는 트랙이다.
- SFT 데이터는 placeholder가 아니고, 자산 누락도 크지 않다.
- 남은 병목은 multi-step chaining, intermediate binding, 날짜/상대시간 정규화다.

## Priority

- 우선순위: 상
- 이유: 가장 적은 비용으로 student model을 실용 수준까지 끌어올릴 수 있다.

## Base Models

- Primary: `Qwen/Qwen3-4B`
- Secondary: `Qwen/Qwen3-8B`
- Comparator: `Qwen/Qwen3-14B`

## Phase 0

1. 현재 40샘플을 500~1500샘플 규모로 확장한다.
2. data 유형을 아래로 나눈다.
   - single call
   - linear chaining
   - fan-out then summarize
   - relative date normalization
   - JSON schema corner cases
3. intermediate placeholder 토큰 규칙을 통일한다.
   - `<RESULT_1>`
   - `<SEARCH_RESULT>`
   - `<TEAM_EMAILS>`

## Phase 1

- 목표: small model의 stable chaining
- 권장 시작점
  - `max_seq_length=2048`
  - `per_device_train_batch_size=2`
  - `gradient_accumulation_steps=4`
  - `learning_rate=2e-4`
  - `lora_r=16`

## Phase 2

- optional GRPO
- reward 구성
  - valid JSON
  - schema validity
  - tool order exact match
  - argument exactness

## Model Notes

- `Qwen3`는 tool use가 강하고, 이 작업은 non-thinking 모드가 더 안정적이다.
- 출력 형식을 설명문 없이 JSON only로 고정해야 한다.

## Exit Criteria

- `tool_selection_accuracy >= 0.95`
- `argument_validity >= 0.85`
- `schema_validity >= 0.99`
- hard chaining split에서 `task_success >= 0.8`
