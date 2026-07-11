# 프로젝트 상태 / 인계 노트 (Handoff)

> 새 대화에서 이 파일을 읽고 이어서 작업하기 위한 요약.
> Branch: `claude/usage-question-q3vm84`

## 무엇을 하는 프로젝트인가
"인종·민족별 피부암 격차" 메타분석. 두 개의 **서로 다른** 경로가 저장소에 공존한다:

1. **`meta_agents/orchestrator.py`** — 자동 파이프라인 (검색→스크리닝→추출→분석→논문).
   이번 세션에 많이 개선했지만 **핵심 한계**: 데이터 추출(Agent 3)이 "발생률(rate)"
   데이터를 못 담는다(모델에 events/total·mean/sd·HR만 있고 rate/IRR 필드가 없음).
   → 실행하면 `data.R`가 전부 `null`. 즉 **정량 결과를 낸 적이 없다.**

2. **`meta_agents/run_meta_analysis.py`** — ⭐ **실제로 작동하는 진짜 메타분석.**
   Claude Code가 논문을 읽고 인종별 발생률을 `STUDIES` 리스트에 직접 채워넣은 것
   (log(IRR), SE, minority_rate, nhw_rate). `python run_meta_analysis.py`로 돌면
   Black/Hispanic/API vs NHW 등의 pooled IRR·I²·forest plot이 나온다.
   완성 출력은 `meta_agents/output_20260417_093053/` (manuscript.pdf, forest plots 등, 14편).

## 이번 세션에 orchestrator에 넣은 것 (전부 커밋됨)
- Agent 1 검색식 생성을 `claude` CLI로 (API 키 불필요); `claude` 바이너리 자동 탐색
- 2단계 PRISMA 스크리닝(초록→전문), 전문 확보(PMC OA 자동 + 로컬 `fulltext/<PMID>.pdf`)
- 다중소스 병합+중복제거(`merge_sources.py`, PMID→DOI→퍼지제목)
- 이어하기 캐시(`cache_utils.py`, `.cache/<hash>/`), 검색세트 freeze(`studies.json`)
- 정밀 PubMed 쿼리 override, abstract fallback, 합성 전 "구할 논문" 제시하고 멈춤
- `report_status.py`(상태 요약), robust JSON 파서, CLI 타임아웃 600s

## 핵심 발견 / 미해결 논의
- 자동 추출은 rate 데이터에 안 맞음 → **실데이터는 Claude가 논문 읽고 넣어야 함**
  (run_meta_analysis.py 방식). 이게 표준 SR 관행이기도 함.
- 이번 orchestrator 자동 실행은 **엄격 기준으로 3편만 포함** + 데이터 null → 실익 없음.
  전 실행 14편(run_meta_analysis.py)이 실체.
- **선별기준 재조정 필요** (아래 열린 결정 참고).

## 열린 결정 (사용자와 정할 것)
1. **분석 방식**: A) 연구 내 IRR(2인종 이상 연구만, 엄격) vs A+B) 인종별 rate pooling
   추가(단일인종 연구도 활용, 이질성↑). 현재 run_meta_analysis.py는 방식 A.
2. **아웃컴 범위**: 발생률/유병률만? vs 사망률·생존율·병기 격차까지 확장?
   (이 분야 문헌 본체는 사망률·생존율. 확장하면 논문 수·HR 데이터 크게 늘어남)
3. **배제기준 수정**: 이번 세션에 과하게 조임. 특히
   - "head/neck"을 비피부암 예시로 넣은 건 실수(두경부 **피부**암은 적격) → 제거/명확화
   - "리뷰·사망률생존율만·단일집단" 배제가 14→3의 주원인
   - 원본 기준(loose)은 `git show 221640e:meta_agents/orchestrator.py` 참고
4. **경로 선택**: run_meta_analysis.py(14편)를 확정·확장할지, orchestrator를 rate 지원으로
   재설계할지, 둘을 연결할지.

## 실행 방법 (Codespace)
```bash
cd meta_agents
# 자동 파이프라인(주의: 추출 null):
export NCBI_EMAIL=... NCBI_API_KEY=...
python orchestrator.py multi          # 스크리닝 후 "구할 논문" 제시하고 멈춤
python orchestrator.py multi proceed  # 남은 것 무시하고 합성까지
# 진짜 메타분석(손/Claude가 채운 데이터):
python run_meta_analysis.py
python report_status.py               # 현재 캐시 상태 요약
```
- `claude` CLI 로그인 필요(구독). 바이너리 경로는 자동 탐색되지만 안 되면
  `export CLAUDE_BIN=$(find ~ -name claude -type f -path '*claude-code*' 2>/dev/null | head -1)`
- `fulltext/<PMID>.pdf`에 넣은 유료 PDF로 전문 심사·추출.

## 추천 다음 스텝 (제안)
run_meta_analysis.py(14편)를 실체로 확정하고, 필요하면 Claude가 새 논문의 발생률을
읽어 STUDIES에 추가. orchestrator는 검색·스크리닝 보조로만 사용. 선별기준은
"사망률·생존율 포함 + 리뷰/증례보고만 배제"로 완화, head/neck 예시 제거.
