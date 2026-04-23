# Labeling Guide: Tool-Call

## Goal

- 도구 선택, 호출 순서, 인자 구성을 strict contract로 저장한다.
- 설명문 없는 JSON-only target을 유지한다.

## Required Fields

- `chain_depth`
- `tool_names`
- `expected_tool_calls`
- `strict_json_only`

## Chain Tags

- `single_call`
- `linear_chain`
- `fan_out`
- `relative_date`
- `schema_corner_case`

## Labeling Rules

- expected tool call은 순서 배열로 저장한다.
- intermediate placeholder token은 통일한다.
- 인자 값은 실제 evaluator schema와 같은 key 이름을 사용한다.
- 설명 텍스트, markdown fence, 자연어 해설은 gold에 넣지 않는다.

## Verification

1. JSON parse
2. schema validation
3. tool order 확인
4. argument exactness 확인
5. chain depth 태그 확인

## Common Mistakes

- valid JSON이지만 schema key가 다름
- tool order는 맞지만 intermediate binding contract가 없음
- 상대 날짜 task인데 절대 날짜 정규화 단계가 빠짐
