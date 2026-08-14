# Supplementary Materials — 구성 인덱스 (무엇을 어디서 가져오는가)

각 Supplementary 항목 → 소스 파일 → Feedback 요구사항 매핑. 상태: ✅ 준비됨 /
🔧 손봐야 함 / 🖊 아직 만들어야 함.

| # | Supplementary 항목 | 소스 파일 | Feedback | 상태 |
|---|---|---|---|---|
| **S1 Table** | 데이터베이스별 검색식·플랫폼·검색일·검색결과수 | `../SEARCH_STRINGS_v2.md` + `../SEARCH_LOG.md` | 2번 | ✅ |
| **S2 Fig** | PRISMA 2020 흐름도 | `PRISMA_COUNTS.md`(숫자) + `Advice/PRISMA flowchart.pptx`(템플릿) | 3번 | 🖊 그림 그려야 |
| **S3 Table** | 포함 연구 163편 특성 (registry·기간·군·outcome·정량/서술) | `../TableS_included_studies.csv/.md` | 총평 | ✅ (163 일치) |
| **S4 Table** | 전문 제외 목록 + 사유 | `../TableS_excluded_fulltext.csv/.md` | 총평 | ✅ (재생성함) |
| **S5 Table** | Registry 중복 + 대표연구 선정 이유 | `../TableSA_main_representatives.csv` (권위본) | 5번 | ✅ |
| **S5b Table** | 연구별 registry·지역·기간·overlap cluster 상세 | `../TableSA_registry_overlap.csv` | 5번 | 🔧 대표컬럼 불일치(아래 주1) |
| **S6 Table** | 추정치 provenance 구분 + 계산 유도 로그 | `../DERIVATIONS.md` + provenance 분포(주2) | 6번 | ✅ |
| **S7 Table** | 비뚤림 위험(Newcastle-Ottawa 적응) | `TableS_risk_of_bias.csv/.md` | 4번 | ✅ (검수 필요) |
| **S8 Table** | 이질성: 전부포함 vs 주분석, I²·τ², 추정량(DL/REML/HKSJ) 비교 | `Table_sensitivity_I2.*` + `Table_method_comparison.md` | 6번 | ✅ |
| **S9 Table** | 민감도분석: (1) Good-RoB만, (2) 직접보고 IRR만 | `Sensitivity1_good_rob.*` + `Sensitivity2_directly_reported.*` | 6번 | ✅ |
| **S-Fig 2+** | 아형별 forest plot (집계·세분화 AANHPI·Hispanic·AIAN·subtype) | `Table_main_forest.csv`에서 생성 | 총평 | 🖊 그림 생성 필요 |

## 본문(main text)에는 넣지 말 것 (Feedback 2·7번)
- 전체 검색식 → S1로 이동 (본문엔 "4개 DB, 검색일, 총 건수"만)
- 긴 방법 방어 문장 → 삭제

## 주석

**주1 — S5b registry_overlap 불일치:** `make_registry_overlap.py`는 오래된 coarse
클러스터링(대표 19개 + "20편 미정" 잔여 문구)을 써서, 실제 분석
(`finalize_representatives.py`, 분석셀 88개)과 대표 개수가 다르다. **대표연구
선정의 권위본은 S5(`TableSA_main_representatives.csv`)**이며, S5b는 연구별
registry/지역/기간/중복cluster 서술용으로만 쓰고 대표 플래그는 S5를 따른다.
→ 넣으려면 `make_registry_overlap.py`를 finalize 로직에 맞춰 재작성하거나 S5b의
main_analysis 컬럼을 제거할 것.

**주2 — provenance 분포(144개 추정치):** 직접보고 73 (IRR 61 · SIR 2 · rate 10),
계산 71 (rate+CI 32 · Poisson-SE 10 · 점추정 29). variance 가용 CI 있는 것 103/144.

## 아직 만들어야 할 산출물 (🖊)
1. **PRISMA 2020 흐름도 그림** — `PRISMA_COUNTS.md` 숫자로 `Advice/PRISMA
   flowchart.pptx` 채우기.
2. **Forest plot 그림들** — `Table_main_forest.csv`로 아형별 forest 생성
   (집계 4군 / 세분화 AANHPI 16 / Hispanic 출신 4 / AIAN / subtype).

## 예시 논문 대응 (Advice/Supplementary Materials.docx)
예시 논문 구조: S-Table 1 검색식 / S-Table 3 RoB(Newcastle-Ottawa) / S-Fig 1
forest. 위 번호는 그 관례를 따랐다.
