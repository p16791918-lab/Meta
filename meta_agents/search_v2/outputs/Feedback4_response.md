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
- **Loo 2019(rec 161) — PDF Table 1 렌더링으로 최종 해결**: poppler 설치 후 Table 1(Number of Cases + IR 95% CI)을 확인. 원문 **rate CI는 사례수에 맞게 정상이나 IRR CI만 5–228배 비현실적으로 좁음**(rate CI로 재계산 시 예: NH HR+/HER2+ [1.347,1.351]→[0.96,1.88]). 정오표 없이 원문 데이터로 IRR CI 오류 증명. → **Loo 14개 subtype IRR CI를 Table 1 rate CI로 delta method 재계산해 교체**(computed-from-rates-with-CI, DERIVATIONS §2 등록). 전사 오류(NH HR+/HER2+ 1.34→**1.35**)도 정정. 누락 Japanese TNBC 1.07도 추출.
- **원문 SE/CI 우선**: point 추정(Melkonian 2019 등 CI 미보고)은 점추정으로 제시하고 근사 계산하지 않음. 대규모 national aggregate의 좁은 CI(예: Sung 2023 TNBC 1.95[1.93-1.98])는 큰 N으로 정상임을 확인(경고만).

**추가 재검토(핵심 요구였는데 초기 '완료'에서 빠졌던 부분)**:
- **총사건수 Poisson CI를 age-standardized 발생률비에 적용한 부분 재검토**(Supplementary Note 1 = DERIVATIONS §3): 해당 행은 rec 169(Ellington)·182(Cronin)·49(Mills)·3267(Kem). 각 원문의 rate SE/CI 제공 여부를 확인.
  - **rec 182(Cronin)**: 원문이 Black 116.9[116.2–117.6]/White 122.1[121.8–122.3] **rate CI를 보고** → 총사건수 Poisson을 버리고 **delta method로 전환**(0.957 [0.944,0.971]→**[0.951,0.963]**).
  - **rec 169(Ellington)·49(Mills)·3267(Kem)**: 원문이 rate CI/SE를 제공하지 않아(rate+AAPC 또는 count만) 총사건수 Poisson 근사 불가피 → **근사임을 Methods와 DERIVATIONS §3에 명시**("age-standardized rate를 총사건수 분산으로 근사, age별 가중 미반영; 원문 rate SE/CI 부재 시에만 사용"). count조차 없으면 점추정으로.
  - DERIVATIONS의 부정확한 "rec 203, rec 182" 표기 정정(rec 203은 directly-reported-IRR).

## 항목 5. 연구 간 비교 한계·민감도 해석 반영 — ✅ 완료
- **① "표준인구 상쇄" 취지 수정(Discussion 한계)**: "NHW 비율로 바꿔도 표준인구·연령구조·지역·기간
  차이는 비율 안에 남으며 공통 비교군으로 상쇄되지 않는다. 비율이 표준인구 스케일을 제거하는 것은
  분자·분모가 같은 출처·표준화일 때뿐이며, 이는 셀 내부에서만 성립하고 셀 간에는 성립하지 않는다"를
  명시.
- **② "contemporary benchmark" 재검토(Methods)**: 대표 중 오래된 기간(Middle Eastern 1988-2004,
  Cambodian·Native Hawaiian 1998-2002, Hispanic-origin 1999-2001 등 2005년 이전)이 있어
  "a single population-based benchmark ... not a contemporary one—diagnosis periods vary by cell,
  and some representatives predate 2005"로 수정.
- **③ Figure 2 이질 출처 명시**: forest 그림에 각주 추가("각 점은 별도 연구의 셀 대표값이며 aggregate와
  subgroup은 단일 출처가 아니고 registry·지역·기간·표준인구가 다름; 다이아=aggregate, 원=subgroup,
  막대 없음=원문 CI 없음")하고 Discussion 본문에도 동일 취지 문장 추가.
- **④ Japanese 방향전환 본문 설명(+⑤)**: "대표 Gomez 2026 SEER-21(Moderate RoB)=1.05(NHW 위) →
  low-RoB 제한 시 Jin 2016 8-state SEER+NPCR=0.95(NHW 아래)로 부호 전환. near-null 차이의 부호가
  견고하지 않음을 보이며, 이 변화는 RoB뿐 아니라 대체 연구의 기간·지역·비교군 차이도 반영한다.
  Supplementary Table 6의 changed/dropped 셀도 RoB 단독 효과가 아니라 그 관점에서 읽어야 함"을 추가.

## 항목 6. 서술적 종합·검토 절차 보고 완성 — ⬜ 예정
narrative 112편 주제별 정리+근거 연결, LLM 모델·역할·재검토 표본·누락 보고, PROSPERO 상태 정리, JBI Q9 표기 정합·RoB 판정 기준.

---

## 추가 검증. narrative 전편(114→112→110) 개별 재대조 (사용자 "narrative는"·"114개를 다 봤다고") — ✅ 완료

quant를 poppler로 전수 대조한 것과 동일한 기준을 **narrative 전편에 적용**해, "인종 × 유방암 발생률 ×
NHW 비교"가 이미지 표에 숨어 정량 추출이 가능한데도 텍스트 추출이 놓친 논문(Howlader형)을 찾음.

**절차의 정직한 기록**: 1차는 자동 검출기 2종(소수인종·White 발생률 공존 행, `[Reference]`+IRR(CI)
패턴)을 전편에 돌리고 **걸린 후보만** 정밀판독 → rec 369·14 발견. 사용자가 "114개를 다 봤냐"고 지적한
뒤 **112편 전편을 한 편씩 표 유형으로 분류**하는 감사 로그(`outputs/narrative_verification_log.md`)를
만들어 재확인 → **1차에 narrative로 잘못 넘겼던 rec 93·210을 추가 적발**. PDF 없는 4편(80·402·1637·
1800)은 초록만 있어 설계 근거로 판정(코호트 2·rural-urban supp-only 1·State Cancer Profiles 무CI 1).

**결과 — 실제 누락 정량 4편을 quant로 재분류(48→52), narrative 114→110**:
- **rec 369 (Shoemaker 2018, USCS 99.1%, 2004-2013)**: Table 1이 20-49세 **2000 US 표준화 IRR vs
  NHW(Tiwari CI)** 직접 보고 — Black 1.03, Asian/PI 0.85, AIAN 0.70, Hispanic 0.74. 강등 사유
  "not age-adjusted vs-NHW IRR"는 사실오류. **age-lt50 대표**(tier 9 > 기존 rec 146 SEER → rec 146 overlap).
- **rec 14 (Lee Argov 2024, JAMA Netw Open, USCS ~99%, 2001-2019)**: Table 1이 **≥65세 age-adjusted
  IRR vs NHW** 직접 보고 — Hispanic 0.70, AIAN 0.72, Asian/PI 0.62, Black 0.93. **age-ge65 신규 차원 4셀**.
- **rec 93 (Zahnd 2019, Lower Mississippi Delta 7-state NAACCR, 2012-2014)**: Table 3-4가 **NHW=Ref
  age-adjusted subtype IRR**을 직접 보고 — Black 전체 1.07·HR+/HER2- 0.87·HR-/HER2+ 1.49·TNBC 2.10,
  Hispanic 0.78 등. (1차에 Table 1-2의 Delta-vs-non-Delta만 보고 race-vs-White 표를 놓쳤던 것을 정정.)
  지역 7주 subset이라 전국 대표의 **sensitivity overlap**(tier 5).
- **rec 210 (Du 2022, SEER 18, 2000-2018)**: 인종별 age-adjusted rate+CI 보고(API 기준). 동일 출처
  rate로 **IRR vs NHW를 delta method 재계산**(DERIVATIONS §2) — Asian/PI 0.742, Black 0.937,
  AIAN 0.676, Hispanic 0.700. 전국 aggregate 대표의 **sensitivity overlap**(SEER-18 tier 6).
- 4편 모두 JBI Low. RoB 37/48→**41/52 Low**, 11 Moderate. 대표 79→83(age-ge65 4셀 신규), Table 1
  헤드라인 불변. 민감도 재계산: low-RoB **62/11/10**, directly-reported 31/5/47, NHW-comparator 64/1/18.

**narrative 유지가 옳다고 확인된 주요 후보(오분류 아님)**:
- **사례-사례 subtype 분포 OR**(발생률비 아님): rec 3861(CCR Asian subtype OR), rec 3780(Kaiser
  코호트 HR; 인구기반 registry 아님).
- **생존/사망 HR**: rec 1336(race×subtype "1(Ref)…2.33"은 survival HR; 발생은 joinpoint 그림).
- **추세지표(EAPC/APC/drift)**: rec 2302, rec 405, rec 31, rec 1106, rec 2453 등.
- **노출·SES 비교군**(NHW 대조 아님): rec 3640(구조적 인종주의 rate ratio), rec 226·448·474·427·541.
- **연령-교차 미세밴드**(요약 IRR 없음): rec 17, rec 103.
- **형태학적 아형**(수용체 아형 범위 밖, ILC/IDC/IBC): rec 259·3845(IBC), rec 426(ILC), rec 425(IDC).
- **지역 하위집단**(자체 비교가 Delta vs non-Delta): rec 93 — race×subtype rate는 계산가능하나
  전국 대표와 overlap, 자체 비교축이 지리적이라 narrative/sensitivity 등급.
- **비표준 표준화 의심**: rec 436(2000-2023 전국) — Black/White = 174.9/228.9 = **0.76**으로 전국
  합의치(~0.95)와 모순, NHW 228.9는 이례적 고값 → 표준화 이상으로 판단, `suspicious_CI_audit`에 flag하고
  narrative 유지(대표 대체 불가).

## 항목 7. 리뷰 기여 명확화·제출자료 최종 점검 — ⬜ 예정
기존 연구 대비 추가 확인점, 연구 간 일치/불일치·비교가능성·근거부족 집단, 본문·표·그림 수치/번호·비교군·민감도 목록 정합, PDF 그림 잘림.

## 항목 8. 서식 de-AI (본문·Supplementary) — ⬜ 예정
파란 제목→검정, 제목 스타일 점 제거→기본, 표 상단 청록 배경 제거→굵은 글씨+최소 구분선, 표 제목 아래 설명을 표 아래 Note.로 이동, Note는 방법·비교군·기호·약어만.
