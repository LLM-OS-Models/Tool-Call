# Tool-Call

함수 호출, 도구 선택, 인자 생성, 실행 성공을 다루는 도구 에이전트 프로젝트입니다.

## 목표
- 도구 선택
- 인자 생성
- schema 준수
- 실행 성공
- task success

## 실행
```bash
uv sync --extra dev
```

## 평가 파이프라인

### 디렉토리 구조
```
eval/
├── eval_runner.py      # → llm-os-eval-core (symlink)
├── summarize.py        # → llm-os-eval-core (symlink)
├── run_phase1.sh       # 8-GPU 병렬 평가 (소형~중형 모델)
├── run_phase2.sh       # 추가 모델 평가 (Qwen3.6-27B, LFM 계열)
└── internal/v1.jsonl   # 평가 데이터셋
data/
├── prepare_sft.py      # → llm-os-eval-core (symlink)
├── sft_train.py        # → llm-os-eval-core (symlink)
└── sft/                # SFT 학습 데이터
    ├── train.jsonl
    └── val.jsonl
```

### 실행 방법
```bash
# Phase 1: 소형~중형 모델 8종 병렬 평가
bash eval/run_phase1.sh

# Phase 2: 추가 모델 평가 (Qwen3.6-27B, LFM2-24B-A2B, LFM2.5-1.2B-Instruct, LFM2-2.6B)
bash eval/run_phase2.sh

# 결과 요약
python eval/summarize.py --results-dir eval/results
```

### 평가 모델

**Phase 1** (8-GPU 병렬):
- GPU0: Qwen3.5-4B
- GPU1: gemma-4-E2B-it
- GPU2: gemma-4-E4B-it
- GPU3: Qwen3.5-9B-text-only
- GPU4: Qwen3.5-2B
- GPU5: gemma-4-26B-A4B-it
- GPU6: Qwen3.5-27B
- GPU7: gemma-4-31B-it

**Phase 2** (추가):
- Qwen/Qwen3.6-27B
- LiquidAI/LFM2-24B-A2B (23.84B MoE)
- LiquidAI/LFM2.5-1.2B-Instruct
- LiquidAI/LFM2-2.6B
