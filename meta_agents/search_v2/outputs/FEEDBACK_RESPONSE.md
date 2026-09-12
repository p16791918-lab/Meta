# Feedback 대응표 (교수님 지적사항 → 조치 → 자료)

교수님 Feedback의 7개 항목 + 총평 각각에 대해, 무엇을 어떻게 반영했는지와 해당
자료 파일을 정리했습니다. 상태: ✅ 완료 / ◐ 부분(선생님 확인·작성 필요) / ⬜ 미착수.

---

## 1. 전체적인 문장 수정 (1인칭·수사적·절대적 표현, 재작성)

| 지적 | 조치 | 상태 |
|---|---|---|
| `I searched/found/My results` 1인칭 단수 | Results 초안을 중립·수동태("A systematic search was conducted", "Data were extracted")로 작성 | ◐ |
| `misleading`, `dissolves`, `indictment` 등 수사·공격적 표현 | 초안에서 전부 배제, 객관적 서술만 | ◐ |
| `every/all/no single study` 절대 표현 | 결과가 뒷받침하는 범위로 한정 | ◐ |
| 결론 반복·AI 티 → 직접 읽고 재작성 | **본문 재작성은 선생님 영역** (아래 총평 참조) | ⬜ |

자료: `RESULTS_DRAFT.md` (객관 수치 위주 초안)

## 2. 문헌검색 ✅ (PROSPERO 제외)

| 지적 | 조치 | 상태 |
|---|---|---|
| PubMed/Embase만으로 부족 → 4개 DB | **PubMed/MEDLINE·Embase·Scopus·Web of Science** 검색 완료 (9,099건) | ✅ |
| PubMed/MEDLINE 표기 통일 | "PubMed/MEDLINE" 단일 표기 | ✅ |
| 검색식은 본문 제외, Supplementary에 | S1 Table로 이동 (DB별 검색식·플랫폼·검색일·건수) | ✅ |
| 제목 제한 → title/abstract 검색 | 인종·민족 개념을 title/abstract/keyword로 확장 | ✅ |
| PROSPERO 재등록 | **선생님이 직접 등록 필요** | ⬜ |

자료: `SEARCH_STRINGS_v2.md`, `SEARCH_LOG.md`

## 3. PRISMA flowchart ✅

PRISMA 2020 형식으로 재작성. 4개 DB 식별(9,099) → 중복제거(4,306) → 스크리닝(4,793)
→ 전문검토(242) → **제외 79건(사유별 건수 명시)** → 포함 163 → 추출 43.

자료: `Fig_PRISMA.png`, `PRISMA_COUNTS.md`

## 4. Risk of bias ✅ (검수 필요)

예시 논문의 **Newcastle-Ottawa Scale** 형식(Selection/Comparability/Outcome,
Good/Fair/Poor)을 발생률 연구에 맞게 적용. 43편 → Good 35 / Poor 8.
Feedback대로 **AI 1차안이며 선생님이 몇 개 검수** 필요.

자료: `TableS_risk_of_bias.md/.csv`

## 5. 중복 registry 자료 처리 ✅

| 지적 | 조치 |
|---|---|
| registry·지역·기간·연령·군·outcome 표로 중복 확인 | 대표선정 표 작성 |
| 가장 포괄적/최근/명확한 연구 1편을 대표로 | one-per-registry-family 원칙 적용 |
| 전체·세부민족·아형·연령은 서로 다른 연구 가능 | 분석셀(차원×군×family)별로 대표 선정 |
| 주분석 = one-per-family, 민감도 = 전부/중복제외 비교 | 주분석 + 전부포함 민감도 비교 완료 |
| 대표선정 이유를 Supplementary에 | representative_reason 컬럼 기록 |

자료: `TableSA_main_representatives.csv`, `Table_sensitivity_I2.md`

## 6. 통계분석과 결과 해석 ✅

| 지적 | 조치 |
|---|---|
| I² 99–100%를 "noise 아니다" 단정 금지 | **중복 registry 투입에 의한 비독립성 인공물**로 설명; 전체 pooled 해석 제한 명시 | 
| DL만 쓰고 영향없다 단정 금지 | **DL vs Paule-Mandel(REML) vs Hartung-Knapp** 비교표 | 
| 직접보고 IRR / 계산 IRR / 그림추출 / 근사 SE 구분 | provenance 6종 분류 + 유도 로그 | 
| 같은 표준인구·기간·비교군 확인 후 IRR | std_pop·period·comparator 기록, 불일치 flag | 
| age-std 자체가 잘못된 것처럼 표현 금지 | "전체 연령표준화가 연령별 차이를 충분히 못 보여줄 수 있다" 수준으로 | 
| 인종차를 유전·생물기전 직결 금지 | 가설·가능한 설명으로만 (Discussion 가이드) | 

자료: `Table_sensitivity_I2.md`, `Table_method_comparison.md`, `DERIVATIONS.md`,
`Sensitivity1_good_rob.md`, `Sensitivity2_directly_reported.md`

## 7. 본문 구성 ◐

| 지적 | 조치 | 상태 |
|---|---|---|
| 제목 간결하게 | "Racial and Ethnic Differences in Breast Cancer Incidence in the United States: A Systematic Review and Meta-Analysis" 채택 | ✅ |
| Intro/Methods/Results/Discussion 재구성 | 구성 가이드 + Results 초안 | ◐ |
| `aggregate categories conceal disparities` 반복 금지 | 문단별 1회만 | ◐ |
| Black/NHB, White/NHW, API/세부민족 용어 통일 | 용어 통일 (원 논문 정의 기준) | ◐ |

## 총평 — 8개 항목 요약 (선생님 본인 문장 작성 영역) ◐

교수님이 학생에게 "직접 읽고 본인 문장으로 요약하라"고 한 항목. 아래 자료를 참고해
**선생님이 직접 작성**:
1. 연구질문·목적 · 2. 검색 DB·전략(`SEARCH_*`) · 3. 포함·제외기준
(`TableS_included/excluded`) · 4. PRISMA 작성법(`Fig_PRISMA`) · 5. RoB 방법
(`TableS_risk_of_bias`) · 6. 중복처리(`TableSA_main_representatives`) · 7. 통계분석
(`Table_sensitivity_I2`, `Table_method_comparison`) · 8. Results/Discussion 구성.

---

## 첨부 파일 목록 (교수님께 함께 전달)

**본문용**
- `Table1_main.md` — Table 1 (인종군별 IRR + RoB + GRADE)
- `Fig_PRISMA.png` — PRISMA 2020 흐름도
- `Fig_forest_AANHPI.png`, `Fig_forest_overview.png` — forest plots

**Supplementary**
- S1 `SEARCH_STRINGS_v2.md` + `SEARCH_LOG.md` — 검색식
- S3/S4 `TableS_included_studies.md`, `TableS_excluded_fulltext.md`
- S5 `TableSA_main_representatives.csv` — registry 중복·대표선정
- S6 `DERIVATIONS.md` — provenance·계산 유도
- S7 `TableS_risk_of_bias.md` — RoB (Newcastle-Ottawa)
- S-GRADE `TableS_GRADE.md` — 근거등급
- S8 `Table_sensitivity_I2.md`, `Table_method_comparison.md` — 이질성·추정량
- S9 `Sensitivity1_good_rob.md`, `Sensitivity2_directly_reported.md` — 민감도

**선생님 확인·작성 필요**
- RoB·GRADE 몇 개 검수 · PROSPERO 등록 · 본문 재작성 · 총평 8항목 요약
