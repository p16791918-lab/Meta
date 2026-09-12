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
## Loo 2019 계산법 확정 (PDF Table 1 렌더링으로 검증 완료)
poppler-utils 설치 후 Loo Table 1을 렌더링하니 **Number of Cases와 IR(95% CI)**가 확인됨.
결과: **rate CI(IR 95% CI)는 사례 수에 맞게 정상인데, IRR CI만 비현실적으로 좁다** — 즉 원문의
rate·사례수·rate CI는 신뢰 가능하고 **IRR의 CI 계산만 오류**다. rate CI로 delta method 재계산하면:

| 셀 (N) | 원문 IRR (95% CI) | rate CI로 재계산한 올바른 CI | 원문 대비 |
|---|---|---|---|
| Japanese HR+/HER2− (908) | 1.03 (1.03–1.04) | 1.03 [0.93, 1.15] | 21배 좁음 |
| Native Hawaiian HR+/HER2− (615) | 1.12 (1.11–1.14) | 1.12 [1.01, 1.25] | 8배 |
| Native Hawaiian HR+/HER2+ (75) | **1.35** (1.347–1.351) | 1.34 [0.96, 1.88] | 228배 |
| Japanese TNBC (116) | 1.07 (1.07–1.09) | 1.08 [0.79, 1.46] | 33배 |
| Filipina HR+/HER2− (434) | 0.64 (0.63–0.66) | 0.64 [0.57, 0.73] | 5배 |

→ **정오표 없이 원문 자체 데이터로 IRR CI 오류가 증명됨.** rate CI는 옳으므로, 우리는 Loo의 각 IRR CI를
Table 1의 rate CI로 delta method 재계산해 교체할 수 있다(점추정보다 정확). 사례 수:
전체 4,430건(HR+/HER2− 3,244; HR+/HER2+ 353; HR−/HER2+ 202; TNBC 409).

**전사 오류 정정**: Native Hawaiian HR+/HER2+ 우리 ledger가 1.34였으나 **원문·교수 피드백 모두 1.35** → 정정.
(1.35는 CI 1.347–1.351 안에 들어가므로 "CI 밖"이 아니라 "비현실적으로 좁은 CI"가 정확한 진단.)

---
**요약**: 원문 직접 보고값 중 통계적으로 신뢰하기 어려운 것은 **Loo 2019의 IRR CI**뿐이며, PDF Table 1
검증으로 **원문 rate CI는 정상·IRR CI만 오류**임이 확정됨 → Table 1 rate CI로 재계산해 교체 가능.
나머지 좁은 CI는 대규모 national 전수라 정상.

---
## 대표 22개 원문-표 전수 대조 (사용자 요청, poppler 설치 후)
provenance별로 원문 layout 텍스트/이미지와 대조:
- **18개 ✓**: rate·IRR·CI가 원문과 직접 일치 (10, 28, 49, 146, 169, 200, 265, 286, 324, 485, 522, 587, 1478, 2406, 2510, 3182, 3267, 3662, 4040 — Nash/Kong/Xu/Ellington/Gleason/Anderson/Ihenacho/Nasseri/Yazzie/Sung2020/Melkonian/Pinheiro/Kem/Miller 등).
- **rec 2 Howlader**: all-ages subtype rate가 원문 본문에 없으나 이는 정상 — Supplement Table 3의 age-specific rate를 2000 US로 우리가 표준화한 값(DERIVATIONS §1, anchor 검증됨).
- **rec 234 Gomez 2026**: subgroup rate·rate-CI 원문 일치; NHW 분모 139.5는 eTable3(Supplement, DERIVATIONS §4 기록) — 이번 세션 재확인은 PMC egress 차단으로 불가.
- **rec 155 Sung 2023**: PDF 부재, txt로 national rate 검증(Black 25.2/White 12.9 등).
- **rec 161 Loo 2019**: 유일한 실제 데이터 오류(IRR CI) — Table 1 rate CI로 재계산해 교체 예정.

**결론**: 22개 대표 중 실제 데이터 오류는 Loo CI 하나. 나머지는 원문 대조로 검증되었거나 Supplement 기반으로 문서화됨.

---
## overlap-only quant 25편 원문 대조 (사용자 질문 "quant 다 봤냐"에 따라)
provenance별 layout 대조: 22편 값 원문 일치. 이슈 3편도 확인 완료:
- rec 51 (Nash 2022): external SEER-Explorer NHW 137.4 — 원문에 없는 게 정상(external anchor, DERIVATIONS §4).
- rec 419 (Amirikia 2011): Table 2의 age-group별 TNBC rate를 2000 US 표준화 → NHB 23.6/NHW 12.6/Hisp 10.2 재현(이미지 표 렌더링 확인, DERIVATIONS §1).
- rec 500 (Gopalani 2020): AI/AN breast RR 0.56 [0.55–0.57] 원문 확인(CI 표기 차이로 자동 대조가 놓쳤을 뿐).

**결론: quant 48편(대표 23 + overlap 25) 전수 원문 대조 완료. 실제 데이터 오류는 Loo 하나뿐이었고 해결됨.**

---
## narrative 재대조에서 발견한 비표준 표준화 의심값 (추출 제외, flag만)
- **rec 436 (2000-2023 전국 female breast, "age-standardized rates")**: Table 1이 인종별 발생률을
  NHW 228.9 / NHB 174.9 / API 143.8 / AIAN 134.1 / Hispanic 116.6 per 100,000로 보고. 두 가지 이상:
  (1) **NHW 228.9는 2000 US 표준화 유방암 발생률(~128)의 약 1.8배**로 이례적 고값; (2) 여기서
  Black/White = 174.9/228.9 = **0.76**으로, SEER·USCS 등 모든 전국 자료의 합의치(overall Black≈White,
  ~0.93-0.98)와 정면 배치. 동일 표준을 전 인종에 적용했다면 IRR은 표준 선택에 불변이어야 하므로,
  0.76이라는 이탈은 **연령구조 차이가 남는 조율(crude에 가까운) 또는 자료·표준화 이상**을 시사.
  → age-adjusted IRR로 신뢰 불가. **추출 제외(narrative 유지), 대표 대체 불가.** 원저자 표준인구·분모
  정의 확인 권장.
