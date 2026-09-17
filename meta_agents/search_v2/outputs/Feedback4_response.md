## 1. AI/AN 자료원 분류와 대표값 선정을 다시 검토해주세요. Gopalani 2020은 CDC WONDER/USCS 자료를 사용했고 PRCDA 분류를 사용하지 않았다고 명시하고 있는데, 현재는 IHS-PRCDA 자료로 분류되어 있습니다. 이는 IHS-linked 자료를 우선한다는 선정 근거에 영향을 주므로, 자료원 분류를 바로잡고 대표값·RoB·민감도분석을 다시 확인해주세요. 같은 원논문에 Northern Plains 추정치도 있으므로, 해당 지역 자료가 한 연구뿐이라는 설명도 재검토해야 합니다.

- **자료원 정정**: Gopalani 2020을 원문대로 USCS(NPCR+SEER, unlinked)로 정정(원문 Methods: "We did not use [PRCDA] classifications"). IHS-linked 오분류를 제거.
- **대표값 재선정**: 진짜 IHS-PRCDA national 자료인 Melkonian 2019(breast RR 0.87 vs NHW, 원문 "Non-Hispanic white was chosen as the reference")가 AI/AN aggregate 대표가 됨. 0.56 → 0.87. 원문에 CI, case count가 없어 point estimate로 제시(근사 계산 안 함).
- **순위 재편**: Hispanic 0.72 < AANHPI 0.77 < AI/AN 0.87 < NHB 0.93 → 최저는 Hispanic(기존엔 AI/AN). Abstract, Results, Discussion 반영.
- **Northern Plains**: Melkonian 2019에 Northern Plains 추정치(IHS-PRCDA, RR 1.05)가 있으므로, 현재 대표를 unlinked Watanabe-Galloway(0.90)에서 IHS-linked Melkonian(1.05)로 교체. "단일 연구뿐" 설명을 삭제(Watanabe-Galloway 2015은 overlap으로 강등). Alaska(1.26), Southern Plains(1.30) 지역값도 추출표에 추가(각각 ANTR 1.09, Melkonian 2021 1.33 대표는 유지, Melkonian 2019는 overlap).
- **RoB**: Gopalani 2020이 unlinked가 되며 JBI Q7(race ascertainment) undercount → RoB Low 39→38, Moderate 9→10.
- **민감도**: 재실행(저위험 55/8/10, 직접보고 36/5/32, NHW 55/1/17). 내부 정합성 검증 전부 통과.
- **기간 정정**: 재확인 중 Melkonian 2019 period 2012-2016 → 2010-2015(Table 2) 오류도 정정.

---

## 2. 연구 포함·분석 배정·대표값 선정 기준을 일관되게 적용해주세요. 일부 중복 연구는 리뷰에서 제외하고 다른 중복 연구는 민감도분석에 포함한 이유가 명확하지 않습니다. Wingo 2008처럼 NHW 비교자료가 있는 연구를 narrative-only로 분류한 이유도 확인해주세요. 연구별로 정량자료 추출 가능 여부와 대표값 선택·미선택 이유를 기록하고, 선정 단위도 'analytic cell당 하나'로 일관되게 기술해주세요. 단순한 registry 명칭뿐 아니라 실제 지역·관찰기간·대상 인구의 중복 여부를 확인해야 합니다.

- **Wingo 2008 재분류**: Wingo 2008는 IHS-linked(CHSDA) AI/AN-vs-NHW breast RR + 95% CI를 IHS region별로 보고하는데 narrative-only로 오분류돼 있었음("overlaps AIAN cells"를 이유로 강등한 것이 오류 — overlap이면 quant 민감도 풀에 있어야 함). include-quant로 재분류하고 CHSDA 값 추출(national 0.63, Northern Plains 0.89, Southern Plains 0.89, Alaska 0.99, 모두 CI 있음). 최근 IHS-linked 값이 대표를 유지하고 Wingo는 overlap/sensitivity로 편입.
- **연구별 로그**: Supplementary Table 2(included studies)에 "Role in synthesis" 컬럼 추가 — 각 연구가 (a) 정량 추출 가능했는지, (b) 몇 개 analytic cell의 대표인지 / overlap-only인지 / narrative-only인지와 그 이유를 명시. 예: Gomez 2026 "Representative for 10 cells; overlap for 6", Wingo "Overlap/sensitivity only (4 cells)", Gopalani "Overlap only (1 cell)", 대표 미선택 사유는 Supplementary Table 4의 main_analysis 열과 연결.
- **선정 단위 통일**: 'analytic cell(group × dimension)당 대표 하나'로 Methods, Supplementary Table 2/4 legend에서 일관 기술.
- **중복 판정 기준**: registry 명칭이 아니라 registry family + 지역 + 관찰기간 + 대상 인구로 겹침을 판정(Supplementary Table 4에 registry, region, period, group을 함께 표기해 셀 내 overlap을 확인).
- **제외 vs 민감도 구분 기준 명시**(Methods): 같은 registry, 기간, 인구의 추정치를 재출판한 중복 데이터셋은 제외, 같은 registry family라도 다른 기간, 지역, subset이면 별개 추정으로 보고 민감도 overlap으로 유지.

## 3. 주요 추출값뿐 아니라 비교군·기간·연령·효과지표를 함께 재검증해주세요. 자료원 분류 오류가 확인된 만큼 master dataset의 핵심 정보를 원문과 다시 대조해주세요. 예를 들어 Sung 2020은 여성 비교자료를 포함하지만, 현재 보충자료의 성별·비교군·관찰기간 표기를 재확인해야 합니다. NHW와 unstratified White를 구분하고, SIR로 보고된 값도 직접표준화 발생률비와 같은 방식으로 해석할 수 있는지 확인해주세요. 표준인구가 원문에 명시되지 않았다면 발생률 크기로 추정하지 말고 '불명확'으로 기록해주세요.

**정량 연구 전수 정독**(55편)으로 각 편의 비교군(NHW vs unstratified White), 관찰기간, 성별(여성 한정), 표준인구, 효과지표(IRR/SIR/rate)를 원문 대조.
- **비교군 명시**: unstratified White(†) = Gleason, Cronin, Baquet, Anderson, Richardson, Gopalani 계열, SIR = Goggins(US White 표준), external NHW = Nash 2022. NHW, White (NH), external을 정확히 구분(민감도3에서 † 제거).
- **오류 교정**: Sung 2020 비교군 White→NHW, 기간 2011-2015→2010-2016, Melkonian 2019 기간 2012-2016→2010-2015 등.
- **표준인구 이질성**: DavisLynn 2025 = Segi 1960 world(2000 US와 이질) 명시.

- **SIR 해석(Goggins Goggins 2009)**: SIR은 US White 연령구조 기준 간접표준화 비율로, 두 집단을 공통 표준으로 직접표준화한 IRR과 표준화 방식이 다름 → 같은 상대-White 스케일로 읽되 SIR로 표기하고 직접보고-IRR 민감도분석에서 제외함을 Methods에 명시.
- **표준인구 원문 대조 오류 3건 정정**: Wilkinson 2002(Wilkinson) 원문 "1970 US standard" 명시인데 std_pop 누락 → 1970 US로; Anderson 2008(Anderson) 원문 "2000 US" 명시인데 "std pop cancels"라 부정확 표기 → 2000 US로; Zahrieh 2021(Zahrieh) Bayesian 소지역 분석으로 표준인구 미명시 → std_pop을 'not stated'로(rate 크기로 추정 안 함).
- **표준인구 기록 방침 명시**(Methods): SEER*Stat, USCS age-adjusted는 2000 US가 프로그램 기본값이라 그대로 기록; 그 외 미명시는 'not stated'. Discussion의 "one older study used the 1970 world standard"도 실제(1970 world/US + 1960 Segi)에 맞게 수정.
- **관찰기간 원문 대조 오류 3건 정정**(표준인구 재점검 후 기간도 전수 대조): Hendrick 2021(Hendrick) 원문 incidence "2014-2017"인데 2013-2017로 → 2014-2017; Cronin 2012(Cronin) 제목, 본문 "2005-2009"인데 2004-2008로 → 2005-2009; Richardson 2016(Richardson) 값 121.5/123.6이 원문 "During 2009-2013"인데 2011로 → 2009-2013. (IRR은 비율이라 불변, 기간 라벨만 정정.)
- **비교군은 오류 없음 확인**: comparison_vs "White" 21행(Loo, Baquet, Gleason, Anderson)은 전수 재확인 결과 모두 unstratified White(†)로 정확. NHW/White(NH)/external은 정확.
- **연령(age band)도 오류 없음 확인**: age-specific 8셀(Gomez 2017 young=<50, 265 <40/≥40, 199 <40, 522 <50/≥50, 146 <50[20-49], 485 ≥50)을 원문 대조 → 모두 정확.


**판단 결정**:
- **Sung 2020 — 대표 유지**: 남성 유방암 논문의 여성 참조패널이지만 자료원이 USCS(~99% 커버리지)로 SEER 기반 Kong 2020보다 넓고 기간도 최신(2010-2016)이라, 커버리지 우선 규칙상 Black subtype 3셀(HR+/HER2- 0.79, HR+/HER2+ 1.01, HR-/HER2+ 1.29)의 대표로 유지. 여성 subtype 값도 USCS 전수라 신뢰. Kong 2020은 overlap/sensitivity로 편입.
- **Keegan 2007 — narrative 강등**: 원문이 6개 Asian subgroup의 rate/trend만 보고하고 same-source NHW rate를 제공하지 않아 IRR 복원 불가 → 정량 정의 미충족으로 narrative 재분류.
- **AI/AN subtype(Kong 2020 HR+/HER2- 0.74, Sung 2023 TNBC 0.86) — 대표 유지**: IHS-linked subtype 자료가 없어 unlinked가 유일 자료이므로, undercount 한계를 명시하고 대표로 유지(Alaska Native 선례와 동일 논리).

## 4. 연령표준화 발생률비의 신뢰구간 계산 방법을 재검토해주세요. Supplementary Note 1에서 총 사건 수만을 이용한 Poisson CI를 연령표준화 발생률비에 적용한 부분은 수정이 필요한지 확인해주세요. 원문 발생률의 SE/CI를 우선 활용하고, 정보가 부족하면 점추정치만 제시하거나 근사 계산의 한계를 명시해주세요. Loo 2019의 1.35 (1.347–1.351)처럼 매우 좁은 CI는 원문에도 있는 값이지만, 계산법이나 정오표를 확인할 필요가 있습니다. 직접 보고된 값이라는 이유만으로 통계적 타당성이 확보되는 것은 아닙니다.

- **항구 점검 추가**: 내부 점검에서 모든 보고 CI의 순서, bracket(점추정 포함)을 검증하고, subgroup×subtype의 비현실적으로 좁은 CI를 경고.
- **Loo 2019 — PDF Table 1 렌더링으로 최종 해결**: poppler 설치 후 Table 1(Number of Cases + IR 95% CI)을 확인. 원문 rate CI는 사례수에 맞게 정상이나 IRR CI만 5–228배 비현실적으로 좁음(rate CI로 재계산 시 예: NH HR+/HER2+ [1.347,1.351]→[0.96,1.88]). 정오표 없이 원문 데이터로 IRR CI 오류 증명. → Loo 14개 subtype IRR CI를 Table 1 rate CI로 delta method 재계산해 교체(computed-from-rates-with-CI, Supplementary Note 1 기록). 전사 오류(NH HR+/HER2+ 1.34→1.35)도 정정. 누락 Japanese TNBC 1.07도 추출.
- **원문 SE/CI 우선**: point 추정(Melkonian 2019 등 CI 미보고)은 점추정으로 제시하고 근사 계산하지 않음. 대규모 national aggregate의 좁은 CI(예: Sung 2023 TNBC 1.95[1.93-1.98])는 큰 N으로 정상임을 확인(경고만).

- **총사건수 Poisson CI를 age-standardized 발생률비에 적용한 부분 재검토**(Supplementary Note 1): 해당 행은 Ellington 2022(Ellington), 182(Cronin), 49(Mills), 3267(Kem). 각 원문의 rate SE/CI 제공 여부를 확인.
- **Cronin 2012(Cronin)**: 원문이 Black 116.9[116.2–117.6]/White 122.1[121.8–122.3] rate CI를 보고 → 총사건수 Poisson을 버리고 delta method로 전환(0.957 [0.944,0.971]→[0.951,0.963]).
- **Ellington 2022(Ellington), 49(Mills), 3267(Kem)**: 원문이 rate CI/SE를 제공하지 않아(rate+AAPC 또는 count만) 총사건수 Poisson 근사 불가피 → 근사임을 Methods와 Supplementary Note 1에 명시("age-standardized rate를 총사건수 분산으로 근사, age별 가중 미반영; 원문 rate SE/CI 부재 시에만 사용"). count조차 없으면 점추정으로.
- Supplementary Note 1의 부정확한 "Brinton 2008, Cronin 2012" 표기 정정(Brinton 2008은 directly-reported-IRR).

## 5. 연구 간 비교의 한계와 민감도분석 결과를 해석에 반영해주세요. NHW 대비 비율로 변환하더라도 표준인구·연령·지역·관찰기간의 차이는 사라지지 않으므로, "standard population largely cancels"라는 설명은 수정해주세요. 오래된 자료를 포함하는 만큼 'contemporary benchmark'라는 표현도 재검토해야 합니다. Figure 2에는 서로 다른 연구의 aggregate와 subgroup을 배치했다는 점을 명시하고, Japanese처럼 low-RoB 분석에서 방향이 바뀌는 결과는 본문에서 설명해주세요. 연구 교체에 따른 변화에는 RoB뿐 아니라 시기·지역·비교군 차이도 영향을 줄 수 있습니다.

- **총괄(민감도 결과를 해석에 반영)**: Discussion에 4개 민감도분석의 결론을 명시 — "제한 시 대표가
 바뀐 셀은 13, 5, 1, 2개뿐이고, 나머지 차이는 자격 추정치 부재로 drop된 것이지 불일치가 아님;
 변화는 near-null AANHPI subgroup, 연령 셀(Japanese 등)에 몰려, aggregate 순서는 robust하나 일부
 near-null subgroup의 부호는 견고하지 않음."
- **① "표준인구 상쇄" 취지 수정(Discussion)**: (a) 한계 문단에 "NHW 비율로 바꿔도 표준인구, 연령구조, 지역, 기간 차이는 비율 안에 남으며 공통 비교군으로 상쇄되지 않는다(셀 내부에서만 스케일 제거 성립)"를
 명시하고, (b) 원래의 과잉 주장 문장("common NHW scale … lets aggregate and subgroup results be
 read side by side")을 직접 수정 → "arranges … on one axis for comparison—though the estimates
 are not fully commensurable, and the arrangement shows the span of published figures rather than a
 set of mutually calibrated rates".
- **② "contemporary benchmark" 재검토(Methods)**: 대표 중 2005년 이전의 오래된 기간(Middle Eastern
 1988-2004, Cambodian, Native Hawaiian 1998-2002, Hispanic-origin 1999-2001 등)이 있어, 'contemporary
 benchmark'라는 표현을 삭제함. 진단 기간이 셀마다 다르고 일부 대표는 2005년 이전이므로 Methods는 대표값을
 더 이상 'contemporary'로 규정하지 않음.
- **③ Figure 2 이질 출처 명시**: forest 그림에 각주 추가("각 점은 별도 연구의 셀 대표값이며 aggregate와
 subgroup은 단일 출처가 아니고 registry, 지역, 기간, 표준인구가 다름; 다이아=aggregate, 원=subgroup,
 막대 없음=원문 CI 없음")하고 Discussion 본문에도 동일 취지 문장 추가.
- **④ Japanese 방향전환 본문 설명(+⑤)**: "대표 Gomez 2026 SEER-21(Moderate RoB)=1.05(NHW 위) →
 low-RoB 제한 시 Jin 2016 8-state SEER+NPCR=0.95(NHW 아래)로 부호 전환. near-null 차이의 부호가
 견고하지 않음을 보이며, 이 변화는 RoB뿐 아니라 대체 연구의 기간, 지역, 비교군 차이도 반영한다.
 Supplementary Table 6의 changed/dropped 셀도 RoB 단독 효과가 아니라 그 관점에서 읽어야 함"을 추가.

## 6. 서술적 종합과 검토 절차의 보고를 완성해주세요. Narrative synthesis 114편이 제공한 결과를 nativity, 연령, 시간 추세, 지역 등 주요 주제로 정리하고 근거 연구를 연결해주세요. LLM 선별에 사용한 모델과 역할, 사람이 재검토한 표본 수, 발견한 누락 및 후속 조치도 보고해주세요. PROSPERO 등록 준비 중 문구는 실제 등록 상태로 정리하고, 사전 프로토콜과 분석 후 변경사항을 구분해주세요. JBI 평가에서는 Q9를 '해당 없음'으로 설명하면서 표에는 Y로 기록한 부분과 전체 RoB 판정 기준도 확인해주세요.

- **① narrative 118편 주제별 정리 + 근거연구 연결**: 6개 주제로 분류(제목, 집단, outcome 키워드) —
 Molecular subtype/histology 28, Geography/region 24, Age/early-onset 20, SES/screening 9,
 Nativity/immigrant 8, Time trends 9, Other(subgroup-descriptive) 20 (합 118). Results의
 narrative 소절을 주제별 서술로 재작성(각 주제의 소견을 정량결과와 대조)하고, Supplementary
 Table 2를 주제별로 그룹화(각 연구에 PMID/DOI 부여)해 근거연구를 연결.
- **② LLM 모델, 역할, 재검토 표본, 누락 보고**: 제목/초록 선별은 large language model
 (Anthropic's Claude)이 포함/제외를 제안하고 저자가 최종 판정(단일선별 + AI). **Methods 본문은 이
 모델 역할과 단일선별을 간결히 기술하고, 사람 재검토의 상세는 supervisor 요청(item 6)에 대한 답으로
 여기 피드백 응답에 보고한다.** 재검토는 제외편 전수를 대상으로 했다 — 명시적 키워드 필터를 **5개 중 4개 이상 신호**(유방암 필수 +
 발생률어[age-adjusted rate·IRR·SIR·per 100,000]·인종/민족·미국 맥락·레지스트리/population-based 중
 3개 이상)로 제외 전수에 걸어, 다섯 신호가 모두 있는 183편과 한 신호만 빠진 478편을 기계 추출하고 그
 초록을 전편 정독했다. 각 편의 overlap/중복 여부는 전문(full text)으로 판정했으며, 잘못 제외된 것으로
 확인해 **17편을 회수·재판정**했다:
   - **quant 편입 6편** — Hossain 2019(Louisiana TNBC, AA vs EA 2.21 [1.96,2.48], PMID 30834239),
     Krieger 2018·Wright 2022(Massachusetts aggregate), Moore 2015(알래스카 원주민 SRR 1.14 vs 미
     백인, IHS-CHSDA), Eheman 2009(NPCR+SEER 전국 ductal/lobular 인종별), Liu 2015(Texas Black vs
     White). 전부 단일주·지역·전국 **sensitivity overlap**으로 편입 — 국가대표(85셀/23연구)·Table 1·
     헤드라인 결과 불변.
   - **narrative 편입 8편** — SEER 흑–백 발생률 RRbw(그래프), ER 표현형×흑백(그래프), Hispanic 이웃
     발생률(논문 내 White 비교 없음), ER-status×인종 전국 추세, 염증성유방암(IBC) 발생률 2편, 선양낭성암
     (ACC) 발생률, IBC 형태학. 정밀 in-paper White rate/IRR가 없거나 형태학·수용체 테마라 서술 종합에 기여.
   - **eligibility 재제외 2편**(라오스 California 비례발생비[PIR]만·발생률 아님; 현역 군인 ACTUR 특수인구),
     **미검색 1편**(Asian enclave 5주, 전문 확보 실패).
 회수·재판정한 17편 외에 배제가 유지된 나머지 후보(다섯 신호 전부지만 배제 사유가 명확했던 것과 한
 신호만 빠진 478편)까지 초록 전문을 정독했으나 **새로 자격을 갖춘 미국 인구기반 인종별 유방암 발생률
 연구는 0편**이었다 — 대다수가 사망/생존·비미국(라틴아메리카·이스라엘·캐나다 등)·위험요인/유전·검진접근·
 이차암 SIR 연구였고, 주제상 근접한 소수(캘리포니아 AANHPI 이웃 SES별 발생률, 뉴멕시코 AI/Hispanic/NHW
 추세, NPCR-SEER TNBC 주별 변이 등)는 전부 학회 초록(사전지정 문헌유형 제외 대상)이거나 이미 포함된
 SEER/NPCR registry family와 중복이었다(4차 재검토에서 보류했던 rec 1027 메인 주 AYA도 전문 재확인 결과
 비히스패닉 백인 단일군을 전국값과 비교해 인종 간 비교가 없어 부적격 확정). 단일선별의 잔여 false-negative를
 한계로 명시한다 — ≥4 완화로 한 신호가 초록에 빠진 표-전용 보고(예: 발생률어가 초록에 없는 3720, US 신호가
 초록에 없는 2609)까지 회수했으므로, 남는 사각지대는 **초록에 신호가 둘 이상 빠진(≤3 신호) 표-전용 보고**로
 좁혀지며, 독립 이중선별은 미시행이다. 포함군 내 재검증에서도 이미지표를 다시 확인해 narrative→quant 4편
 (Shoemaker 2018, Lee Argov 2024, Zahnd 2019, Du 2022)을 재분류했다.
- **③ PROSPERO 상태 정리 + 사전/사후 구분(Methods)**: 자리표시자를 CRD42023437049(저자 제공)로
 교체. 사전 프로토콜(질문, 검색, 적격기준, 중복처리, quant/narrative 분리)과 등록 후 개발, 정련한 사후
 변경(analytic-cell 대표값 프레임, provenance tier, 커버리지 규칙, AI/AN IHS 우선, 수용체 아형, 연령
 셀, 4개 민감도, narrative→quant 4편 재분류)을 구분 명시. Abstract에도 등록번호 추가.
- **④ JBI Q9 정합 + RoB 판정 기준(Methods, 표 legend)**: Q9(response rate)를
 표에 "Yes"→"NA"로 기록(census-like registry엔 survey response rate 없음; NA는 결함으로 미집계)해
 "해당없음" 설명과 표기 일치. 전체 RoB 판정 기준(Low=No≤1 & Q7, Q8 Yes; High=No≥3; else Moderate,
 적용 8개 항목)을 표 legend와 Methods에 명시. 판정 결과 불변(41 Low/11 Moderate).

---

## 7. 이 리뷰가 기존 연구에 추가하는 기여를 명확히 하고, 제출자료를 최종 점검해주세요. 각 cell의 결과가 단일 연구에서 선택된 값인 만큼, 기존 연구들을 함께 검토함으로써 무엇이 추가로 확인되었는지 설명해야 합니다. 하위집단 차이뿐 아니라 연구 간 일치·불일치, 자료의 비교 가능성, 근거가 부족한 집단을 정리하면 기여점이 명확해질 것입니다. 마지막으로 본문·표·그림의 수치와 번호, 비교군 표시, 민감도분석의 changed/dropped 목록을 일치시키고 제출용 PDF에서 그림 잘림도 확인해주세요.

- **① 리뷰 기여 명시(Discussion 신규 문단)**: 단일-연구 cell을 함께 검토해 무엇이 추가됐는지 3가지로:
 (1) 흩어진 추정치를 하나의 NHW 기준 척도로 모아 subgroup을 상호, 대집단과 비교, (2) overlap을
 sensitivity로 남겨 ≥2개 독립 자료원이 뒷받침하는 셀 36개 vs 단일 연구 셀 47개를 구분하고
 일치/불일치를 제시(aggregate 순서, 대다수 subgroup은 제한분석에서 견고, near-null AANHPI subgroup
 일부는 자료원 따라 부호 전환, AI/AN은 IHS-linkage 여부에 좌우), (3) 근거부족 집단 명시(Middle
 Eastern, 일부 NHPI, Hispanic-origin subgroup, AI/AN 아형은 단일 지역, unlinked 자료; AI/AN 지역, 전국
 aggregate는 CI 없는 점추정 → 전용 IHS-linked 1차 연구 필요).
- **② 수치, 번호 정합**: Figure 1-3, Table 1, Supplementary Table 1-6 참조 전부 해소, 결번 없음.
 민감도 changed/dropped 목록을 원자료와 대조 — NHW-comparator: changed 1개(Alaska Native),
 dropped 18개(수용체 아형 16 + age-specific Black 2)로 본문 서술과 정확히 일치. 내부 정합성 검증 통과.
- **③ 비교군 표시**: † (unstratified White, 6셀) 본문, Table 1 일치; ‡ (복원 CI) 신규 표기를
 Table 1, Figure 2에 범례와 함께 추가(항목: 복원 CI vs 원문 CI 구분).
- **④ 그림 잘림**: Figure 2(forest) 하단 캡션이 잘려 있던 것을 발견, 수정(하단 여백 확대). Figure 1(PRISMA), Figure 3(heatmap)은 잘림 없음 확인. 헤드라인 aggregate IRR
 (0.72/0.77/0.87/0.93, NHB TNBC 1.95) 불변 확인.

## 8. 본문과 Supplementary Materials의 서식에서 AI스러운 느낌을 제거해주세요. 제목과 소제목의 파란색 글씨는 검정색으로 변경하고, 제목 왼쪽에 붙은 점(스타일)은 기본 스타일로 적용해주세요. 테이블 상단의 청록색 배경 등 장식적인 색상은 제거하고, 필요한 구분은 굵은 글씨와 최소한의 구분선으로 표시해주세요. 테이블 제목 아래 길게 설명한 내용은 표 아래 Note.로 옮겨 정리하고, Note에는 해당 표를 이해하는 데 필요한 분석 방법, 비교군, 기호 및 약어 설명만 남기고 Methods와 중복되는 설명은 줄여주세요.

- **제목 스타일**: Word Heading 스타일(파란색+왼쪽 점) 제거 → 모든 제목을 검정 굵은 글씨로.
- **표 장식 제거**: 헤더 청록 배경, 섹션 배경 제거 → 굵은 글씨 + 최소 구분선만.
- **표 제목 아래 설명 → 표 아래 Note.로 이동**: 본문 Table 1, Supplementary Table 1, 2, 5. Note에는 분석 방법, 비교군, 기호(†/‡), 약어만 남기고 Methods 중복 축소. Supplementary Table 6a/6c 소캡션은 제한조건+셀 수만 남기고 해석은 Results/Discussion으로.
- 제출용 문서 3종 재생성, 내부 정합성 검증 통과.

---

## 부가. narrative 전편(114→112→110) 개별 재대조

*(이 절은 4차 라운드 당시 포함군 내 narrative 재대조 기록이다. 이후 제외편 전수 재스크리닝(item ②)으로
회수가 더해져 최종은 quant 58 / narrative 118이다 — 아래 48→52, 114→110은 그 시점의 델타.)*

quant를 poppler로 전수 대조한 것과 동일한 기준을 narrative 전편에 적용해, "인종 × 유방암 발생률 ×
NHW 비교"가 이미지 표에 숨어 정량 추출이 가능한데도 텍스트 추출이 놓친 논문(Howlader형)을 찾음.

**절차의 정직한 기록**: 1차는 자동 검출기 2종(소수인종, White 발생률 공존 행, `[Reference]`+IRR(CI)
패턴)을 전편에 돌리고 걸린 후보만 정밀판독 → Shoemaker 2018, Lee Argov 2024 발견. 사용자가 "114개를 다 봤냐"고 지적한
뒤 112편 전편을 한 편씩 표 유형으로 분류하는 감사 로그(`outputs/narrative_verification_log.md`)를
만들어 재확인 → 1차에 narrative로 잘못 넘겼던 Zahnd 2019, 210을 추가 적발. PDF 없는 4편(80, 402, 1637, 1800)은 초록만 있어 설계 근거로 판정(코호트 2, rural-urban supp-only 1, State Cancer Profiles 무CI 1).

**결과 — 실제 누락 정량 4편을 quant로 재분류(48→52), narrative 114→110**:
- **Shoemaker 2018 (Shoemaker 2018, USCS 99.1%, 2004-2013)**: Table 1이 20-49세 2000 US 표준화 IRR vs
 NHW(Tiwari CI) 직접 보고 — Black 1.03, Asian/PI 0.85, AIAN 0.70, Hispanic 0.74. 강등 사유
 "not age-adjusted vs-NHW IRR"는 사실오류. age-lt50 대표(tier 9 > 기존 Xu 2024 SEER → Xu 2024 overlap).
- **Lee Argov 2024 (Lee Argov 2024, JAMA Netw Open, USCS ~99%, 2001-2019)**: Table 1이 ≥65세 age-adjusted
 IRR vs NHW 직접 보고 — Hispanic 0.70, AIAN 0.72, Asian/PI 0.62, Black 0.93. age-ge65 신규 차원 4셀.
- **Zahnd 2019 (Zahnd 2019, Lower Mississippi Delta 7-state NAACCR, 2012-2014)**: Table 3-4가 NHW=Ref
 age-adjusted subtype IRR을 직접 보고 — Black 전체 1.07, HR+/HER2- 0.87, HR-/HER2+ 1.49, TNBC 2.10,
 Hispanic 0.78 등. (1차에 Table 1-2의 Delta-vs-non-Delta만 보고 race-vs-White 표를 놓쳤던 것을 정정.)
 지역 7주 subset이라 전국 대표의 sensitivity overlap(tier 5).
- **Du 2022 (Du 2022, SEER 18, 2000-2018)**: 인종별 age-adjusted rate+CI 보고(API 기준). 동일 출처
 rate로 IRR vs NHW를 delta method 재계산(Supplementary Note 1) — Asian/PI 0.742, Black 0.937,
 AIAN 0.676, Hispanic 0.700. 전국 aggregate 대표의 sensitivity overlap(SEER-18 tier 6).
- 4편 모두 JBI Low. RoB 37/48→41/52 Low, 11 Moderate. 대표 79→83(age-ge65 4셀 신규), Table 1
 헤드라인 불변. 민감도 재계산: low-RoB 62/11/10, directly-reported 31/5/47, NHW-comparator 64/1/18.

**narrative 유지가 옳다고 확인된 주요 후보(오분류 아님)**:
- **사례-사례 subtype 분포 OR**(발생률비 아님): Telli 2011(CCR Asian subtype OR), Tran 2016(Kaiser
 코호트 HR; 인구기반 registry 아님).
- **생존/사망 HR**: Wang 2026(race×subtype "1(Ref)…2.33"은 survival HR; 발생은 joinpoint 그림).
- **추세지표(EAPC/APC/drift)**: Tuan 2021, Hou 2013, Davis Lynn 2018, Miller 2020, Thomas 2019 등.
- **노출, SES 비교군**(NHW 대조 아님): Eldridge 2022(구조적 인종주의 rate ratio), Michaels 2022, Krieger 2006, Sherr 2026, Truong 2025, Williams 2022.
- **연령-교차 미세밴드**(요약 IRR 없음): Joslyn 2005, Clarke 2012.
- **형태학적 아형**(수용체 아형 범위 밖, ILC/IDC/IBC): Il'yasova 2011, Hirko 2013(IBC), Quinn 2025(ILC), Bunte 2025(IDC).
- **지역 하위집단**(자체 비교가 Delta vs non-Delta): Zahnd 2019 — race×subtype rate는 계산가능하나
 전국 대표와 overlap, 자체 비교축이 지리적이라 narrative/sensitivity 등급.
- **비표준 표준화 의심**: Mzizi 2026(2000-2023 전국) — Black/White = 174.9/228.9 = 0.76으로 전국
 합의치(~0.95)와 모순, NHW 228.9는 이례적 고값 → 표준화 이상으로 판단, 이상값 점검 목록에 표시하고
 narrative 유지(대표 대체 불가).

---

**현재 최종 카운트**: included 176 (primary screen 162 + excluded 재스크리닝 회수 14), quant 58, narrative 118, excluded 83, not-retrieved 10, assessed 249, excluded-at-eligibility 73, estimates 219, cells 85, reps 23, sens-only 35, RoB 45 Low / 13 Moderate / 58. 내부 정합성 검증 전부 통과.
