# 직접 보고 CI/값 통계 타당성 점검 (Feedback4 #4: "직접 보고된 값이라는 이유만으로 타당성 확보 안 됨")

전 ledger 행의 CI를 log 스케일 상대 반폭(rel.half-width)과 비대칭으로 스크리닝하고,
**자료원 규모(national 전수 vs 단일 주·소집단)**로 정상/의심을 구분함. 좁은 CI 자체는
대규모 national에서 정상이므로, 문제는 **N에 비해 좁은** 단일 주·소집단 값이다.

---

## 1순위 — 통계적으로 명백히 의심: **Loo 2019 (rec 161, PMID 30503975)**
*"The high and heterogeneous burden of breast cancer in Hawaii", Cancer Epidemiology 2019.*

**진단(원문 내부 모순)**:
- 원문 Methods: "confidence intervals were calculated **for all rates**" — CI를 *rate*에 대해 계산.
- 원문 Results: 개별 인종 subpopulation은 "**could not be calculated due to the small population sizes**"라고 스스로 인정.
- 그런데 Table 1의 *IRR*(=소수인종 rate / White rate)에는 ±0.5–2.4%의 초정밀 CI를 붙임 → **모순**. rate의 CI를 IRR CI로 잘못 옮겼거나 IRR CI 전파에 오류가 있는 것으로 의심.
- 이미 **2건은 CI가 점추정을 아예 벗어남**(불가능): Native Hawaiian HR+/HER2+ IRR 1.34인데 원문 CI **1.347–1.351**; Chinese HR+/HER2− IRR 0.58인데 원문 CI **0.46–0.53**. → 이 2건은 점추정으로 이미 정정.

**남은 의심 좁은 CI(원문값 보존 중, 정오표/계산법 확인 대상)**:
| 셀 | IRR [CI] | 상대반폭 |
|---|---|---|
| Japanese HR+/HER2− | 1.03 [1.03, 1.04] | ±0.5% |
| Japanese HR−/HER2− (TNBC) | 1.07 [1.07, 1.09] | ±0.9% |
| Native Hawaiian HR+/HER2− | 1.12 [1.11, 1.14] | ±1.3% |
| Japanese HR+/HER2+ | 1.03 [1.02, 1.05] | ±1.5% |
| Native Hawaiian HR−/HER2+ | 1.19 [1.16, 1.21] | ±2.1% |
| Filipina HR+/HER2− | 0.64 [0.63, 0.66] | ±2.4% |
| Filipina HR+/HER2+ | 0.88 [0.86, 0.91] | (좁음) |

→ **권장**: 저널(Cancer Epidemiology)의 published correction/erratum 유무와, Table 1의 CI가 rate CI인지 IRR CI인지 원 저자에게 확인. Loo는 대표가 아닌 overlap(†-comparator)이라 주 결과엔 영향 없으나, sensitivity에 남기려면 CI 신뢰성 확인 필요.

## 경계 사례 — 확인 권장(단일 주 소집단, 좁은 편)
- **Nasseri 2009 Middle Eastern** (California-CCR, PMID 19292805): 0.86 [0.84, 0.88], ±2.4%. CA에서 Middle Eastern은 소수인데 CI가 좁은 편(단, 1988–2004 17년 누적이라 사건 수는 어느 정도). → 원문 case count/CI 계산법 확인 가능.

## 정상 — 좁은 CI가 당연 (대규모 national 전수, 문제 아님)
SEER-21 / USCS(~99%) / SEER-national 기반 aggregate·subgroup은 사건 수가 수천~수십만이라
±0.3–2% CI가 통계적으로 정상: Gomez 2026, Zhang 2025, Xu 2024, Davis Lynn 2025, Brinton 2008,
Anderson 2008, Hendrick 2021, Ellington 2022, Kong 2020, Xie 2022, Sung 2020/2023, Carozza 2006,
Keegan 2010, SEER-Explorer anchor 등. (엄밀 확인은 각 원문 case count로 예상 CI 대조 가능.)

## 비대칭 CI — 반올림 아티팩트 (실질 문제 아님)
Sung 2023 TNBC 1.95 [1.93, 1.98], Hendrick 2021 Black 0.97 [0.95, 1.00] 등 log 스케일 비대칭은
소수점 2자리 반올림에서 생기는 표시상 현상으로, 계산 오류가 아님.

---
**요약**: 원문 직접 보고값 중 **통계적으로 신뢰하기 어려운 것은 사실상 Loo 2019 하나**이며(원문 스스로 소집단 계산 불가를 인정), 정오표·계산법 확인 대상. 나머지 좁은 CI는 대규모 national 전수라 정상.
