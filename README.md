# Meta-Analysis Agent System
> 의학 메타분석 논문을 자동으로 생성하는 Claude Code 서브에이전트 시스템

## 파일 구조

```
meta_agents/
├── orchestrator.py          ← 지휘자 (여기서 실행)
├── agent_1_search.py        ← 문헌 검색 에이전트
├── agent_2_screening.py     ← PRISMA 선별 에이전트
├── agent_3_extraction.py    ← 데이터 추출 에이전트
├── agent_4_analysis.py      ← 통계 분석 에이전트 (R 코드 생성)
├── agent_5_writer.py        ← 논문 작성 에이전트 (IMRAD)
└── shared/
    ├── prompts.py           ← 각 에이전트 시스템 프롬프트
    └── models.py            ← 데이터 모델 (Pydantic)
```

## 설치

```bash
pip install biopython pypdf           # entrez(PubMed) 검색 + PDF 전문 파싱
export NCBI_EMAIL="your@email.com"    # PubMed 실제 검색 시
export NCBI_API_KEY="..."             # 선택 (초당 10건)
```

> **API 키 관련**: 모든 에이전트는 `claude` CLI를 통해 Claude 구독으로 동작하므로
> `ANTHROPIC_API_KEY`가 **필요하지 않습니다.** 단, `pubmed_mcp` 모드(Mode A)만
> Anthropic SDK의 hosted-MCP 기능을 써서 예외적으로 API 키가 필요합니다.
> (`pip install anthropic` + `export ANTHROPIC_API_KEY=...`)
> 로컬/Codespaces에서 `claude` CLI를 못 찾으면 `export CLAUDE_BIN=$(which claude)`.

## 사용법

### 1. 빠른 시작 (데모 모드)
```bash
cd meta_agents
python orchestrator.py
```

### 2. 본인 PICO로 실행
`orchestrator.py` 하단의 `MY_PICO` 섹션을 수정:

```python
MY_PICO = PICO(
    population="연구 대상 환자군",
    intervention="중재 (약물/시술)",
    comparison="대조군",
    outcome="주요 결과변수",
    study_design="Randomized controlled trial"
)
```

### 3. 실제 PubMed 검색
```python
run_meta_analysis(
    ...
    search_mode="entrez"    # "demo" → "entrez" 변경
)
```

### 4. 전문(full-text) 확보 워크플로우
정식 2단계 선별에서는 초록 통과분의 **전문**이 필요합니다.

1. 먼저 한 번 실행하면 Phase 1(초록) 통과분에 대해 PMC 오픈액세스 전문을 자동 수집합니다.
2. 확보 못 한 유료 논문은 `output_.../fulltext_needed.csv` 에 목록으로 나옵니다.
3. 그 논문들을 **기관 계정으로 PDF 다운로드** → `meta_agents/fulltext/<PMID>.pdf` 로 저장.
4. **다시 실행**하면 이제 그 PDF들을 전문으로 읽어 Phase 2(전문 선별)·데이터 추출에 사용합니다.

## 산출물 (output_YYYYMMDD_HHMMSS/)

| 파일 | 내용 |
|------|------|
| `search_queries.json` | PubMed/Cochrane/Embase 검색식 |
| `prisma_flow.txt` | PRISMA 2020 흐름도 숫자 |
| `data.R` | 추출된 데이터 (R data.frame) |
| `meta_analysis.R` | 생성된 메타분석 R 스크립트 |
| `manuscript.md` | 초안 논문 (Abstract~Conclusion) |

## 각 에이전트 역할

### Agent 1: Search
- PICO → MeSH term 생성
- Boolean operator 검색식 자동 생성
- PubMed Entrez API 호출

### Agent 2: Screening (2단계 PRISMA)
- **Phase 1 (초록)**: 제목/초록만 보고 전문을 확보할 가치가 있는지 판정 (`screen_phase1`)
- **전문 확보**: Phase 1 통과분만 전문 수집 (`fetch_fulltext.py`)
  - PMC 오픈액세스 논문 → 자동 수집 (biopython 필요)
  - 유료 논문 → `fulltext/<PMID>.pdf` 로 직접 넣기 (기관 계정으로 다운로드)
  - 확보 못 한 논문은 `output_.../fulltext_needed.csv` 에 목록으로 남음
- **Phase 2 (전문)**: 실제 전문을 읽고 최종 포함/제외 + RoB/NOS 평가 (`screen_phase2`)

### Agent 3: Extraction
- **전문(full-text)에서** 수치 추출 (초록 아님)
- 연속형 (mean ± SD) / 이진형 (events/total) 데이터 추출
- R data.frame 코드 자동 생성

### Agent 4: Analysis
- I² 기반 모델 선택 (fixed/random-effects)
- metafor::rma() 완성 코드 생성
- Forest plot, Funnel plot, Egger's test
- GRADE 근거 수준 평가

### Agent 5: Writer
- IMRAD 전 섹션 작성
- PRISMA 2020 체크리스트 준수
- 목표 저널 스타일 적용

## Claude Code에서 실행하는 법

```bash
# Claude Code 터미널에서
cd meta_agents
python orchestrator.py

# 또는 각 에이전트 개별 테스트
python agent_1_search.py
```

## 검색 모드 선택 가이드

| 모드 | 명령어 | 필요 조건 |
|------|--------|-----------|
| PubMed MCP | `python orchestrator.py mcp` | pubmed-mcp 서버 설치 |
| Entrez API | `python orchestrator.py entrez` | pip install biopython |
| CSV 가져오기 | `python orchestrator.py csv` | Embase/Cochrane CSV 파일 |
| 데모 | `python orchestrator.py demo` | 없음 (기본값) |

## 참고

- PRISMA 2020: http://www.prisma-statement.org/
- GRADE: https://www.gradeworkinggroup.org/
- PROSPERO 등록: https://www.crd.york.ac.uk/prospero/
- metafor R package: https://www.metafor-project.org/
