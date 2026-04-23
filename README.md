# Tool-Call

함수 호출(Tool Calling) 능력 평가 트랙.

사용자 질문과 사용 가능한 도구(tools) 스키마가 주어지면, 모델이 올바른 도구를 선택하고 적절한 인자를 생성하여 JSON 형식으로 출력하는 능력을 평가한다. 단일 도구 호출부터 다중 도구 연속 호출까지 포함한다.

## 평가 메트릭

| 메트릭 | 설명 |
|--------|------|
| `tool_selection_accuracy` | gold tool_calls 중 모델이 올바르게 선택한 비율 |
| `argument_validity` | gold 인자 중 모델이 정확히 일치하게 생성한 비율 |
| `schema_validity` | 생성된 인자가 도구 스키마를 만족하는지 |
| `task_success` | selection_accuracy>0 AND argument_validity>=0.5 |

**성공 조건**: `task_success > 0`

## 샘플 데이터 형식

### 단일 도구 호출 (tool_0001)

```json
{
  "sample_id": "tool_0001",
  "user_query": "이번 달 서울 출장 경비 합계를 계산하고 50만원 넘는 항목만 보여줘.",
  "artifacts": {
    "tools": [{
      "name": "query_expenses",
      "description": "출장 경비를 조회한다.",
      "schema": {"type": "object", "properties": {"city": {"type": "string"}, "month": {"type": "string"}, "min_amount": {"type": "integer"}}}
    }]
  },
  "gold": {
    "tool_calls": [{"name": "query_expenses", "arguments": {"city": "서울", "month": "2026-04", "min_amount": 500000}}]
  }
}
```

### 다중 도구 호출 (tool_0002) — 3개 도구 연속 호출

```json
{
  "sample_id": "tool_0002",
  "user_query": "지난주 장애 리포트에서 로그인 오류 건수와 결제 오류 건수를 각각 모아서 슬랙 요약 메시지로 보내줘.",
  "gold": {
    "tool_calls": [
      {"name": "search_incident_reports", "arguments": {"keyword": "장애 리포트", "time_range": "last_week"}},
      {"name": "count_errors", "arguments": {"text": "<REPORT_TEXT>", "error_types": ["login", "payment"]}},
      {"name": "send_slack_message", "arguments": {"channel": "#ops", "message": "지난주 로그인/결제 오류 요약"}}
    ]
  }
}
```

### 단일 도구 호출 (tool_0003) — get_weather

```json
{
  "sample_id": "tool_0003",
  "user_query": "서울 내일 날씨 알려줘.",
  "artifacts": {
    "tools": [{
      "name": "get_weather",
      "description": "지정한 도시의 날씨 정보를 반환한다.",
      "schema": {"type": "object", "properties": {"city": {"type": "string"}, "date": {"type": "string"}}}
    }]
  },
  "gold": {
    "tool_calls": [{"name": "get_weather", "arguments": {"city": "서울", "date": "내일"}}]
  }
}
```

### 다중 도구 연속 호출 (tool_0004) — search_wiki + summarize_text 체이닝

```json
{
  "sample_id": "tool_0004",
  "user_query": "양자컴퓨팅에 대해 위키백과에서 검색하고 그 내용을 요약해줘.",
  "gold": {
    "tool_calls": [
      {"name": "search_wiki", "arguments": {"query": "양자컴퓨팅"}},
      {"name": "summarize_text", "arguments": {"text": "<SEARCH_RESULT>"}}
    ]
  }
}
```

## 모델 출력 형식

```json
{
  "tool_calls": [
    {"name": "query_expenses", "arguments": {"city": "서울", "month": "2026-04", "min_amount": 500000}}
  ]
}
```

## 프로젝트 구조

```
Tool-Call/
├── README.md
├── pyproject.toml
├── eval/
│   ├── internal/
│   │   └── v0.jsonl        # 평가 데이터셋 (4샘플: 단일 + 다중 + 단일 + 체이닝)
│   └── results/            # 모델별 결과
├── tests/
│   └── test_eval.py
└── data/
```

## 실행

```bash
uv sync

llm-os-eval run tool_call \
  --model Qwen/Qwen3-4B \
  --samples eval/internal/v0.jsonl \
  --output eval/results/Qwen3-4B_v0.jsonl \
  --base-url http://localhost:8001/v1
```

## 벤치마크 결과 (2026-04-23, Round 3)

| 모델 | Size | selection | arg_validity | task_success | 성공률 |
|------|------|-----------|-------------|-------------|--------|
| Qwen3-4B | 4B | 50% | 0.33 | 50% | **50%** |
| gemma-4-E2B-it | MoE | 67% | 0.33 | 50% | **50%** |
| Qwen3-8B | 8B | 50% | 0.33 | 50% | **50%** |
| Qwen2.5-14B-Instruct | 14B | 67% | 0.33 | 50% | **50%** |
| gemma-4-31B-it | 31B | 67% | 0.33 | 50% | **50%** |
| Llama-3.1-8B-Instruct | 8B | 17% | 0.08 | 0% | 0% |
| Nemotron-Terminal-8B | 8B | 0% | 0.00 | 0% | 0% |
| Qwen3-0.6B | 0.6B | 50% | 0.17 | 0% | 0% |

Tool Call은 모든 트랙 중 가장 높은 성공률을 보인다. 다중 도구 호출(tool_0002)에서는 대부분의 모델이 첫 번째 도구만 올바르게 호출하고 나머지는 누락하는 경향이 있다. 동 크기 8B 비교에서 Qwen3-8B만 성공한다.
