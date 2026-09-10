# 4차 피드백 대응 정리 (Response to 4th-round comments)

각 코멘트에 대해 어떻게 수정했는지 항목별로 정리합니다. 원 코멘트는 `Advice/Feedback4.md` 참조.
(진행 상태: ✅ 완료 · 🔄 진행 중 · ⬜ 예정)

---

## 항목 1. AI/AN 자료원 분류와 대표값 선정 — ✅ 완료

**지적**: Gopalani 2020이 CDC WONDER/USCS를 썼고 PRCDA를 쓰지 않았다고 명시했는데 IHS-PRCDA로 분류됨. 자료원을 바로잡고 대표값·RoB·민감도 재확인. Northern Plains가 한 연구뿐이라는 설명도 재검토.

**수정**:
- **자료원 정정**: Gopalani 2020(rec 500)을 원문대로 **USCS(NPCR+SEER, unlinked)**로 정정(원문 Methods: "We did not use [PRCDA] classifications"). IHS-linked 오분류를 제거.
- **대표값 재선정**: 진짜 IHS-PRCDA national 자료인 **Melkonian 2019**(rec 2510, breast RR **0.87** vs NHW, 원문 "Non-Hispanic white was chosen as the reference")가 AI/AN aggregate 대표가 됨. **0.56 → 0.87**. 원문에 CI·case count가 없어 **point estimate**로 제시(피드백 4항 취지와 일치, 근사 계산 안 함).
- **순위 재편**: Hispanic 0.72 < AANHPI 0.77 < AI/AN 0.87 < NHB 0.93 → **최저는 Hispanic**(기존엔 AI/AN). Abstract·Results·Discussion 반영.
- **Northern Plains**: Melkonian 2019에 Northern Plains 추정치(IHS-PRCDA, RR **1.05**)가 있으므로, 현재 대표를 unlinked Watanabe-Galloway(0.90)에서 **IHS-linked Melkonian(1.05)**로 교체. "단일 연구뿐" 설명을 삭제(rec 461은 overlap으로 강등). Alaska(1.26)·Southern Plains(1.30) 지역값도 ledger에 추가(각각 ANTR 1.09·Melkonian 2021 1.33 대표는 유지, Melkonian 2019는 overlap).
- **RoB**: rec 500이 unlinked가 되며 JBI Q7(race ascertainment) undercount → RoB Low 39→38, Moderate 9→10.
- **민감도**: 재실행(저위험 55/8/10, 직접보고 36/5/32, NHW 55/1/17). crosscheck [A–F] ALL PASS.
- **기간 정정**: 재확인 중 rec 2510 period 2012-2016 → **2010-2015**(Table 2) 오류도 정정.
- **부수 효과**: Discussion을 "unlinked 0.56은 불완전 ascertainment, IHS-linked로 0.87 보정"으로 재서술 → **항목 9(3차 피드백, AI/AN 해석)도 동시 해결**.

---

## 항목 2. 포함·분석 배정·대표값 선정 기준의 일관 적용 — ✅ 완료

**지적**: 중복 연구의 제외/민감도 포함 기준 불명확, Wingo 2008을 narrative-only로 분류한 이유, 연구별 추출가능·선택/미선택 이유 기록, 'analytic cell당 하나' 일관 기술, 중복 판정을 registry 명칭이 아니라 지역·기간·인구로.

**수정**:
- **Wingo 2008 재분류**: rec 134는 IHS-linked(CHSDA) AI/AN-vs-NHW breast **RR + 95% CI**를 IHS region별로 보고하는데 narrative-only로 오분류돼 있었음("overlaps AIAN cells"를 이유로 강등한 것이 오류 — overlap이면 quant 민감도 풀에 있어야 함). **include-quant로 재분류**하고 CHSDA 값 추출(national 0.63, Northern Plains 0.89, Southern Plains 0.89, Alaska 0.99, 모두 CI 있음). 최근 IHS-linked 값이 대표를 유지하고 Wingo는 overlap/sensitivity로 편입(옵션 C).
- **연구별 로그**: Supplementary Table 2(included studies)에 **"Role in synthesis" 컬럼** 추가 — 각 연구가 (a) 정량 추출 가능했는지, (b) 몇 개 analytic cell의 대표인지 / overlap-only인지 / narrative-only인지와 그 이유를 명시. 예: Gomez 2026 "Representative for 10 cells; overlap for 6", Wingo "Overlap/sensitivity only (4 cells)", Gopalani "Overlap only (1 cell)", 대표 미선택 사유는 Supplementary Table 4의 main_analysis 열과 연결.
- **선정 단위 통일**: 'analytic cell(group × dimension)당 대표 하나'로 Methods·Supplementary Table 2/4 legend에서 일관 기술.
- **중복 판정 기준**: registry 명칭이 아니라 **registry family + 지역 + 관찰기간 + 대상 인구**로 겹침을 판정(Supplementary Table 4에 registry·region·period·group을 함께 표기해 셀 내 overlap을 확인).
- **제외 vs 민감도 구분 기준 명시**(Methods): 같은 registry·기간·인구의 추정치를 재출판한 **중복 데이터셋은 제외**, 같은 registry family라도 **다른 기간·지역·subset이면 별개 추정으로 보고 민감도 overlap으로 유지**.

## 항목 3. 비교군·기간·연령·효과지표 재검증 — ✅ 완료
**정량 연구 전수 정독**(48편, `Feedback4_reverify_log.md`)으로 각 편의 비교군(NHW vs unstratified White)·
관찰기간·성별(여성 한정)·표준인구·효과지표(IRR/SIR/rate)를 원문 대조.
- **비교군 명시**: unstratified White(†) = Gleason·Cronin·Baquet·Anderson·Richardson·Gopalani 계열, SIR = Goggins(US White 표준), external NHW = Nash 2022. 코드가 `NHW_OK={NHW, White (NH), external}`로 정확히 구분(민감도3에서 † 제거).
- **오류 교정**: Sung 2020 비교군 White→NHW·기간 2011-2015→2010-2016, Melkonian 2019 기간 2012-2016→2010-2015 등.
- **표준인구 이질성**: DavisLynn 2025 = Segi 1960 world(2000 US와 이질) 명시.

**추가 재검토(초기 '완료' 표시가 성급했던 부분 보완)**:
- **SIR 해석(Goggins rec 955)**: SIR은 US White 연령구조 기준 **간접표준화** 비율로, 두 집단을 공통 표준으로 직접표준화한 IRR과 표준화 방식이 다름 → 같은 상대-White 스케일로 읽되 SIR로 표기하고 **직접보고-IRR 민감도분석에서 제외**함을 Methods에 명시.
- **표준인구 원문 대조 오류 3건 정정**: rec 4333(Wilkinson) 원문 "1970 US standard" 명시인데 std_pop 누락 → **1970 US**로; rec 265(Anderson) 원문 "2000 US" 명시인데 "std pop cancels"라 부정확 표기 → **2000 US**로; rec 107(Zahrieh) Bayesian 소지역 분석으로 **표준인구 미명시** → std_pop을 **'not stated'**로(rate 크기로 추정 안 함).
- **표준인구 기록 방침 명시**(Methods): SEER*Stat·USCS age-adjusted는 2000 US가 프로그램 기본값이라 그대로 기록; 그 외 미명시는 'not stated'. Discussion의 "one older study used the 1970 world standard"도 실제(1970 world/US + 1960 Segi)에 맞게 수정.
- **관찰기간 원문 대조 오류 3건 정정**(표준인구 재점검 후 기간도 전수 대조): rec 66(Hendrick) 원문 incidence "2014-2017"인데 **2013-2017**로 → 2014-2017; rec 182(Cronin) 제목·본문 "2005-2009"인데 **2004-2008**로 → 2005-2009; rec 346(Richardson) 값 121.5/123.6이 원문 "During 2009-2013"인데 **2011**로 → 2009-2013. (IRR은 비율이라 불변, 기간 라벨만 정정.)
- **비교군은 오류 없음 확인**: comparison_vs "White" 21행(Loo·Baquet·Gleason·Anderson)은 전수 재확인 결과 모두 unstratified White(†)로 정확. NHW/White(NH)/external은 코드 NHW_OK로 정확.
- **연령(age band)도 오류 없음 확인**: age-specific 8셀(rec 324 young=<50, 265 <40/≥40, 199 <40, 522 <50/≥50, 146 <50[20-49], 485 ≥50)을 원문 대조 → 모두 정확.

**항목 3 재점검 종합(4개 필드 전수 대조)**: 비교군 오류 0 · 연령 오류 0 · **표준인구 오류 3건 정정** · **기간 오류 3건 정정**. 첫 전수 정독이 값·비교군 위주였고 표준인구·기간 필드는 소홀했던 점을 인정하고 두 필드를 전수 재대조해 총 6건을 교정.

**판단 결정(교수 확인)**:
- **Sung 2020(rec 2406) — 대표 유지(A)**: 남성 유방암 논문의 여성 참조패널이지만 자료원이 USCS(~99% 커버리지)로 SEER 기반 Kong 2020보다 넓고 기간도 최신(2010-2016)이라, **커버리지 우선 규칙상 Black subtype 3셀(HR+/HER2- 0.79, HR+/HER2+ 1.01, HR-/HER2+ 1.29)의 대표로 유지**. 여성 subtype 값도 USCS 전수라 신뢰. Kong 2020은 overlap/sensitivity로 편입.
- **Keegan 2007(rec 463) — narrative 강등**: 원문이 6개 Asian subgroup의 rate/trend만 보고하고 same-source NHW rate를 제공하지 않아 IRR 복원 불가 → 정량 정의 미충족으로 narrative 재분류.
- **AI/AN subtype(rec 286 HR+/HER2- 0.74, rec 155 TNBC 0.86) — 대표 유지(A)**: IHS-linked subtype 자료가 없어 unlinked가 유일 자료이므로, undercount 한계를 명시하고 대표로 유지(Alaska Native 선례와 동일 논리).

## 항목 4. 연령표준화 IRR의 CI 계산 재검토 — ✅ 완료
- **항구 점검 추가**: `crosscheck_master.py [G]`가 모든 보고 CI의 순서·bracket(점추정 포함)을 검증하고, subgroup×subtype의 비현실적으로 좁은 CI를 경고.
- **Loo 2019(rec 161)**: 원문 CI열 내부모순(1.34 CI 1.347-1.351, 0.58 CI 0.46-0.53 — 점추정 제외) → 해당 셀 점추정화. 누락된 Japanese TNBC 1.07 추가 추출.
- **원문 SE/CI 우선**: point 추정(Melkonian 2019 등 CI 미보고)은 점추정으로 제시하고 근사 계산하지 않음. 대규모 national aggregate의 좁은 CI(예: Sung 2023 TNBC 1.95[1.93-1.98])는 큰 N으로 정상임을 확인(경고만).

**추가 재검토(핵심 요구였는데 초기 '완료'에서 빠졌던 부분)**:
- **총사건수 Poisson CI를 age-standardized 발생률비에 적용한 부분 재검토**(Supplementary Note 1 = DERIVATIONS §3): 해당 행은 rec 169(Ellington)·182(Cronin)·49(Mills)·3267(Kem). 각 원문의 rate SE/CI 제공 여부를 확인.
  - **rec 182(Cronin)**: 원문이 Black 116.9[116.2–117.6]/White 122.1[121.8–122.3] **rate CI를 보고** → 총사건수 Poisson을 버리고 **delta method로 전환**(0.957 [0.944,0.971]→**[0.951,0.963]**).
  - **rec 169(Ellington)·49(Mills)·3267(Kem)**: 원문이 rate CI/SE를 제공하지 않아(rate+AAPC 또는 count만) 총사건수 Poisson 근사 불가피 → **근사임을 Methods와 DERIVATIONS §3에 명시**("age-standardized rate를 총사건수 분산으로 근사, age별 가중 미반영; 원문 rate SE/CI 부재 시에만 사용"). count조차 없으면 점추정으로.
  - DERIVATIONS의 부정확한 "rec 203, rec 182" 표기 정정(rec 203은 directly-reported-IRR).

## 항목 5. 연구 간 비교 한계·민감도 해석 반영 — ⬜ 예정
"standard population largely cancels" 수정, "contemporary benchmark" 재검토, Figure 2에 이질 출처 명시, Japanese 등 방향전환 설명.

## 항목 6. 서술적 종합·검토 절차 보고 완성 — ⬜ 예정
narrative 114편 주제별 정리+근거 연결, LLM 모델·역할·재검토 표본·누락 보고, PROSPERO 상태 정리, JBI Q9 표기 정합·RoB 판정 기준.

## 항목 7. 리뷰 기여 명확화·제출자료 최종 점검 — ⬜ 예정
기존 연구 대비 추가 확인점, 연구 간 일치/불일치·비교가능성·근거부족 집단, 본문·표·그림 수치/번호·비교군·민감도 목록 정합, PDF 그림 잘림.

## 항목 8. 서식 de-AI (본문·Supplementary) — ⬜ 예정
파란 제목→검정, 제목 스타일 점 제거→기본, 표 상단 청록 배경 제거→굵은 글씨+최소 구분선, 표 제목 아래 설명을 표 아래 Note.로 이동, Note는 방법·비교군·기호·약어만.
