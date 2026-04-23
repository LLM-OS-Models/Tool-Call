# Data Expansion Plan: Tool-Call

## Objective

- pilot-ready 상태인 현 데이터셋을 실제 학습 가능한 규모로 확장한다.

## Current Strength

- placeholder 없음
- 자산 누락 없음
- 구조가 가장 먼저 pilot 가능한 상태

## Expansion Targets

- total samples: `500+`
- chain-heavy samples: `>= 150`
- relative-date samples: `>= 80`
- schema corner case samples: `>= 50`

## Expansion Sequence

1. single-call 샘플 추가
2. linear chain 추가
3. 3+ step chain 추가
4. relative-date normalization 샘플 추가
5. nested JSON / schema corner case 추가
6. strict JSON 검수

## Required Outputs

- expanded `train.jsonl`
- updated metadata with `chain_depth`
- expected tool call order arrays
- QA completion sheet

## Acceptance

- target sample count 달성
- non-JSON target `0`
- chain depth tag completion `100%`
- hard chaining split 확보
