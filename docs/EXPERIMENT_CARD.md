# Experiment Card: Tool-Call

## task_type
`tool_call`

## 목적
도구 선택, 인자 생성, schema 준수, 실행 성공을 포함하는 tool-use 능력을 실험한다.

## 핵심 지표
- tool_selection_accuracy — 도구명 일치 여부 (0/1)
- argument_validity — 인자 매칭 비율 (0~1)
- schema_validity — JSON Schema 준수 여부 (0/1)
- task_success — 선택 + 인자 종합 성공 (0/1)

## 평가 실행
```bash
bash eval/run_phase1.sh
bash eval/run_phase2.sh
```

## 평가 모델
- Phase 1: 8개 모델
- Phase 2: Qwen3.6-27B + LFM 모델
