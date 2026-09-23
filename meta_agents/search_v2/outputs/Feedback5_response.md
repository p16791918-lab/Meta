## 1. 자료원과 effect estimate의 비교 방향을 다시 확인해주세요.

> Miller 2008의 Native Hawaiian 자료는 Hawaii에 한정되는데, Table 1과 Supplementary Table 4에는 "NAACCR/CiNA (~93%)"로 기재되어 있습니다. 자료원과 coverage를 수정하고, Gomez 2026의 추정치를 포함해 기존 선정 규칙에 따라 대표값을 다시 확인해주세요.
>
> 또한 Supplementary Note 1에서는 Kong 2020의 overall Black 값 1.04가 NHW/Black 방향이어서 기록하지 않았다고 설명하지만, 추출표에는 Black/NHW 값처럼 남아 있습니다. 원문을 확인해 제외 여부 또는 역수 변환을 일관되게 반영해주세요.

- **Miller 2008 자료원·coverage 정정**: 원문 "Native Hawaiian rates calculated only for the state of Hawaii"로 확인 — Hawaii Tumor Registry가 Native Hawaiian 혈통 환자를 전수 분류하기 때문에 Native Hawaiian 발생률만 Hawaii 주로 한정 보고. Table 1·Supplementary Table 4의 "NAACCR/CiNA (~93%)"는 과대 기재였으므로 **Hawaii Tumor Registry(Native Hawaiian은 Hawaii 주 한정)**로 정정하고, 자료원 라벨도 `NAACCR-API` → `HTR`로 맞춰 라벨-coverage 불일치 제거.

- **Native Hawaiian 대표값 재선정**: coverage 정정으로 기존 선정 규칙(전국 SEER > 단일 주)이 그대로 적용 → **Gomez 2026(SEER-21, 2018–2022) 1.27 [1.21–1.33]**이 대표, Miller 2008(1.21 [1.12–1.31])은 sensitivity overlap으로 이동. Results·Discussion의 Native Hawaiian 값 1.21 → **1.27** 갱신. NHPI aggregate 1.21은 Gomez 2026이 보고한 별개 값이므로 불변.

- **연쇄 카운트 갱신**: 대표값 공급 연구 23 → **22편**, overlap 전용 35 → **36편**, 저위험 제한 민감도 60/13/12 → **59/14/12**(unchanged/changed/dropped). 헤드라인 aggregate IRR(Hispanic 0.72·AANHPI 0.77·AI/AN 0.87·NHB 0.93, NHB TNBC 1.95)은 불변.

- **Kong 2020 비교 방향 정정**: 원문이 overall만 NHW를 분자로 서술("non-Hispanic White women was 31.3 …, which was higher compared with the incidence among Black women (IRR, 1.04; 95% CI, 1.02–1.05)")하고 같은 문단의 다른 aggregate는 minority 기준(Asian/PI 0.90, AI/AN 0.82, Hispanic 0.79)임을 확인 — 한 논문 내 방향 혼재. 해당 행을 **Black/NHW 0.96 [0.95–0.98]**로 역수 변환하고 provenance를 `directly-reported-IRR-inverted`로 표기. Supplementary Note 1의 "방향 모호로 미기록" 설명도 실제 처리(역수)와 일치하게 수정. 역수 후 값은 같은 셀 분포(0.81–0.98)·대표값 Ellington 2022(0.933)·동시기 SEER 추정치(Du 0.937, Gomez 0.941, Davis Lynn 0.971)와 정합.

- **비교 방향 전수 점검**: 같은 문제의 잔존 여부를 추출표 전체로 점검. 발생률에서 계산한 122행은 minority ÷ NHW로 방향이 고정되고 내부 점검에서 원문 발생률로 재검증됨. 원문 보고값 98행 중 같은 셀에 추정치가 3개 이상 있어 상호 대조가 가능한 행에서 방향 이탈 후보 3건 검출 → Nash 2022는 외부 NHW 기준을 쓴 계산값, Wingo 2008은 원문이 national 0.63·Northern Plains 0.89·Southern Plains 0.89·Alaska 0.99로 모두 minority 기준, Zahnd 2019는 원문 "non-Hispanic Black women had … higher rates than non-Hispanic White women (RR = 1.07; 95% CI 1.04–1.11)"로 확인되어 3건 모두 방향 정확. 셀 내 대조가 불가능한 33행 중 1을 넘는 9행도 NHB 여성의 40세·50세 미만 교차(1.01–1.16), Asian/Hispanic/AI·AN의 HR−/HER2+ 아형(1.04–1.41) 등 알려진 소견과 부합. 방향 반전이 필요한 행은 Kong 2020 overall Black 1건.

- **자료원 기재 전수 점검**: Miller 건과 같은 유형(원문의 실제 자료원 범위와 기재 불일치)이 다른 연구에도 남아 있는지 점검. 이 유형은 라벨-분류 자동 점검으로는 걸러지지 않으므로, 대표값을 공급하는 22개 연구와 overlap 전용 연구까지 자료원 기재를 원문 범위와 대조. ① 소수 subgroup의 대표이면서 전국급 coverage로 분류된 10건은 모두 Gomez 2026이며, 원문이 "21 registries (excluding Alaska and Seattle, Washington)"와 표 제목 "SEER-21 Program"으로 전국 집계를 명시하고 특정 주 한정 서술이 없어 기재가 정확함을 확인. ② 나머지 대표 자료원(Hawaii Tumor Registry, California-CCR, Florida, IHS-PRCDA, Alaska Native Tumor Registry, USCS, SEER)도 모두 실제 범위대로 분류돼 있음 — Navajo Nation 레지스트리는 Navajo 지역 셀의 대표이므로 지역 한정이 정합. ③ SEER 하위범위(9/17/18/21)를 단일 'SEER-national' tier로 묶은 설계상 단순화가 있으나, 좁은 SEER가 같은 셀의 더 넓은 SEER 추정치를 이겨 대표가 된 사례는 **0건**으로 선정 왜곡 없음. ④ overlap 전용 연구까지 같은 기준으로 확대 점검한 결과 **Goggins 2009에서 같은 유형의 오류를 1건 추가 발견** — 추출표 registry에는 "SEER (SF/Seattle/Detroit/Atlanta/CT/LA/SanJose)"로 7개 registry가 정확히 기재돼 있었으나 coverage 분류 규칙이 문자열의 'SEER'만 보고 전국급(SEER-national)으로 tier를 부여하고 있었음. 원문이 "data from the seven SEER registries … Connecticut, and the cities of San Francisco, San Jose, Los Angeles, Detroit, Seattle, and Atlanta"로 전국 SEER이 아님을 명시하므로, registry 표기를 "SEER 7-registry subset"으로 정리하고 분류 규칙에 registry-subset 조건을 추가해 전국급에서 내림. **다만 이를 Jin 2016(8-state SEER+NPCR)과 같은 라벨로 묶은 것은 부정확하여 재검토함** — Goggins의 7개 registry는 Connecticut 1개 주를 빼면 San Francisco·San Jose·Los Angeles·Detroit·Seattle·Atlanta의 **대도시 단위**이고, Jin 2016은 California·Florida·Hawaii·Illinois·New Jersey·New York·Texas·Washington **8개 주 전체**로 원문 기준 미국 Asian American 인구의 68%를 포괄함. 따라서 Goggins에는 별도 라벨("SEER multi-registry subset (metropolitan areas)")을 부여해 대도시 집합임이 드러나도록 함. 등급(tier)은 같은 구간에 둠 — 분류 사다리에 "여러 주"와 "한 주" 사이의 중간 등급이 없고, 두 연구가 같은 셀에서 만나는 유일한 지점인 Asian Indian/Pakistani 셀에서는 등급이 같아도 **진단기간 순위(2009–2011 vs 1988–2004)로 Jin이 선택**되므로 등급 동률이 선정 결과를 바꾸지 않음을 확인. Goggins는 overlap 전용이어서 주분석 대표·헤드라인 결과는 불변이고, 민감도 카운트도 변동 없음. ⑤ 여기서 두 건 모두 *분류 규칙이 문자열을 잘못 읽은* 유형이었으므로, 점검을 개별 연구가 아니라 **추출표의 고유 registry 문자열 39개 전부 × 부여된 coverage tier**로 확대해 전수 대조 → **2건 추가 발견**. "Metropolitan Atlanta (SEER)"(Lund 2010)와 "New Mexico (SEER)"(Zahrieh 2021)는 SEER 프로그램의 **단일 대도시·단일 주 registry**인데 문자열의 'SEER' 때문에 전국급 tier로 분류돼 있었음. 각각 단일 지역 tier(LA County와 동급)·단일 주 tier로 재분류. 두 연구 모두 overlap 전용이고(Zahrieh 2021은 AI/AN undercount로 이미 강등된 행) 민감도 대표 교체에도 투입되지 않아 주분석 대표·Table 1·헤드라인 결과·민감도 카운트는 모두 불변. 다만 'New Mexico'는 지역을 시사하는 키워드 자동 탐색으로는 걸리지 않아 39개 문자열을 하나씩 확인해 찾았음을 부기함. 결과적으로 자료원 분류 정정은 Miller 2008·Goggins 2009·Lund 2010·Zahrieh 2021 4건이며, 39개 문자열 전수 대조에서 남은 불일치는 없음.

- **이전 점검이 두 건을 놓친 이유와 점검 방식 보완**: 4차 라운드에서 대표 연구 전수를 원문과 대조했고(자료원·기간·비교군·값) 그 기록은 `SOURCE_VERIFICATION_LOG`에 남아 있으나, 자료원 점검이 **논문이 명시한 data system 단위**로 이루어진 것이 한계였음. Miller 2008은 논문 수준 자료원(NAACCR/SEER API registries)이 기재와 일치했고 Native Hawaiian만 Hawaii로 한정된다는 **그룹 단위 제한**은 그 단위에서 드러나지 않아 통과. Goggins 2009는 registry 문자열 자체가 정확해 원문 대조로도 걸리지 않고, **분류 규칙이 문자열의 'SEER'만 보고 tier를 부여**한 것이 문제여서 라벨-분류 자동 점검(라벨과 분류가 서로 모순되는 경우만 탐지)도 통과. 이번 라운드에서는 점검 단위를 **그룹 × 자료원**으로 바꾸고, 기재뿐 아니라 **분류 규칙이 부여한 coverage tier가 원문 범위와 일치하는지**까지 확인하는 방식으로 보완. 그 결과 위 2건을 찾아 정정했고, 동일 기준으로 남은 연구에서는 추가 불일치가 확인되지 않음.

---

## 2. 표준인구의 영향이 비율에서 상쇄된다는 설명을 수정해주세요.

> Discussion과 Supplementary Table 4 Note에 같은 연구 내 비율은 표준인구의 영향을 받지 않는다는 설명이 남아 있습니다. 같은 표준인구를 사용하더라도 연령표준화율의 비율은 표준인구의 가중치에 따라 달라질 수 있습니다. 해당 표현을 수정하고, NHW 대비 비율로 제시하더라도 연구 간 표준인구·지역·관찰기간의 차이가 해소되지는 않음을 명시해주세요.

- **Discussion 한계 문단 수정**: "비율이 공유 표준화를 상쇄한다(a ratio cancels the shared standardization)"는 표현을 삭제하고, ① 셀 내부에서는 분자·분모가 하나의 표준인구·기간·지역을 공유하므로 비율이 **내부적으로 일관**하다는 점과 ② 그럼에도 **비율이 표준인구를 상쇄하지는 않는다**(두 집단의 연령별 발생률 형태가 달라 다른 표준 가중치는 표준화율과 그 비율을 서로 다른 폭으로 이동시킴)는 점을 구분해 기술. 이어서 **셀 간에는 표준인구·연령구조·지역·진단기간 차이가 그대로 남는다**고 명시.

- **①(셀 내부 일관성) 근거 확인**: "셀 내부에서는 분자·분모가 하나의 표준인구·기간·지역을 공유한다"는 서술이 예외 없이 성립하는지 대표값 85개를 전수 확인 — 모든 대표값이 **한 논문 안에서 소수집단 발생률과 NHW 발생률을 짝지어 만든 비율**이며, 외부 자료의 비교군을 끌어온 행(SEER*Explorer NHW율을 빌린 Nash 2022 등)은 **대표값에 1건도 없음**(overlap 전용으로만 보유). 간접표준화 SIR도 대표값에 **0건**(provenance 분포: computed-from-rates-with-CI 41, directly-reported-IRR 35, Poisson-SE 5, computed-from-rates 4). 따라서 ①은 85개 셀 전부에 대해 성립하며, ②(표준인구 비상쇄)와 모순되지 않음 — ①은 *한 비율 안에서 두 율이 같은 가중치로 표준화됐다*는 뜻이고, ②는 *그 가중치를 바꾸면 비율 자체가 움직인다*는 뜻으로 서로 다른 층위의 진술.

- **Supplementary Table 4 Note 수정**: "연구 내에서 형성되므로 그 연구의 표준인구 선택에 의존하지 않는다"를 삭제하고, 같은 취지(셀 내부 일관성 / 표준인구 비상쇄 / 연구 간 비교 불가)로 재작성. NHW 대비 비율로 제시해도 연구 간 표준인구·기간·지역 차이가 해소되지 않음을 Note에 유지.

- **Supplementary Note 1 표현 정정**: rec 2 항목의 "IRR is invariant to the 20+ vs all-age standard"도 단정적 표현이므로 "essentially unaffected"(0–19세가 분자·분모에 거의 기여하지 않음)로 완화.

- **경험적 근거는 별도로 유지**: 표준인구 제한 민감도분석(2000 US 표준으로 제한)에서 85셀 중 83셀이 불변, 2셀만 변경(1960 Segi 표준 대표가 2000 US 표준 추정치로 교체, HR− 1.80→1.60, HR+ 0.82→0.70)이라는 결과는 그대로 보고. 이는 "표준인구가 비율에 영향이 없다"는 주장이 아니라, 이 자료에서는 대부분 대표값이 이미 2000 US 표준이어서 실제 영향이 제한적이었다는 경험적 관찰로 기술.

---

## 3. 민감도분석의 조건과 실제 결과를 일치시켜주세요.

> Methods와 답변서에서는 Goggins 2009의 SIR을 directly-reported-IRR 분석에서 제외했다고 했지만, Supplementary Table 6b에는 해당 값인 0.61 [0.56–0.66]이 남아 있습니다. 분석 조건과 코드를 확인해 수정해주세요.
>
> Table 6b에서 제외됐다고 보고한 45개 cell도 표에 제시하고, 대표값이 변경된 경우에는 변경 전후의 출처 연구를 함께 표시해주세요. 제한조건을 충족하지 못해 제외된 cell은 결과의 견고함이 확인된 것으로 해석하지 않도록 주의해주세요.

- **Goggins 2009 SIR — 조건과 코드 불일치 정정**: Methods는 SIR이 간접표준화이므로 directly-reported-IRR 민감도에서 제외한다고 서술했으나, 코드의 필터 집합이 `{directly-reported-IRR, directly-reported-SIR}`로 **SIR을 포함**하고 표 제목도 "IRR/SIR only"였음. 지적대로 코드를 Methods에 맞춰 필터에서 SIR을 제거하고, 표 제목·캡션·Note를 "directly reported IRR only(간접표준화 SIR 제외)"로 수정. 그 결과 Goggins 2009의 0.61 [0.56–0.66]이 Table 6b에서 빠지고 Asian Indian/Pakistani 셀은 dropped로 이동 → **6b 결과가 35 unchanged / 5 changed / 45 dropped → 35 unchanged / 4 changed / 46 dropped**로 갱신(Results 서술도 함께 수정). 한편 Kong 2020의 역수 변환 행(item 1)은 원문 보고값의 방향만 바꾼 것이어서 계산 유도값과 구분해 directly-reported 계열에 포함시키고, 그 처리 근거를 코드 주석과 Note에 명시.

- **제외된 cell 전부 제시**: Table 6b만 changed 셀만 싣고 dropped를 생략하고 있었음(6a·6c·6d는 이미 changed·dropped 모두 제시). 6b도 dropped를 모두 포함하도록 수정해 **네 표 모두 changed·dropped 전 cell을 제시**(보충표 행 수 624 → 669; 이후 S2 사유 문구 정리로 현재 665).

- **변경 전후 출처 연구 표시**: 네 표의 값 컬럼에 해당 추정치를 공급한 연구를 병기하도록 변경 — "Main analysis: IRR [95% CI] — study"와 "Under restriction: IRR [95% CI] — study". 따라서 changed 셀에서는 **교체된 연구와 교체한 연구가 한 행에서 함께** 보이고(예: Japanese 아형 셀에서 Gomez 2026 → Jin 2016), dropped 셀은 "not available under this restriction"으로 표시.

- **dropped cell 해석 주의 명시**: 제한을 충족하지 못해 제외된 cell을 견고성 확인으로 읽지 않도록, Supplementary Table 6 Note에 "dropped cell은 그 제한 하에서 **검증되지 않은(untested)** 것이며 확인된 것이 아니다"를 명시. Discussion의 민감도 서술도 "대부분의 차이가 불일치가 아니라 자격 미충족에 따른 drop"이라는 안심형 표현을 걷어내고, **각 제한이 재검토할 수 있었던 cell에 한해 패턴이 유지되었으며 directly-reported 제한만으로도 85개 중 46개 cell이 미검토로 남는다**는 사실을 함께 기술.

---

## 4. RoB 판정 기준과 개별 연구 평가의 일관성을 확인해주세요.

> 현재 Q8 기준은 적절한 연령표준화와 분산 추정치를 요구하지만, CI가 없다고 설명한 Melkonian 2019는 Q8=Yes, Low로 평가한 반면 Harper 2009는 분산 미보고로 Q8=No입니다. CI 미보고 자체가 반드시 높은 비뚤림 위험을 의미하지는 않지만, 설정한 기준은 일관되게 적용해야 합니다. 연구 전체와 추출한 추정치 중 무엇을 평가한 것인지 명확히 하고, 판정이 변경되면 low-risk-only 분석에도 반영해주세요.

- **불일치 원인 확인**: Q8 판정 코드가 분산 유무를 `s["cis"] > 0 or direct or withvar`로 계산하고 있었고, 여기서 `direct`는 **provenance가 원문 보고 비율이면 참**이 되도록 돼 있었음. 그 결과 원문이 비율을 인쇄했지만 신뢰구간이 없는 연구는 분산이 있는 것처럼 통과 → Melkonian 2019(directly-reported-IRR, 추출 7행 모두 CI 없음)는 Q8=Yes·Low, Harper 2009(computed-from-rates, 추출 4행 모두 CI 없음)는 Q8=No·Moderate로 **같은 조건에서 판정이 갈렸음**.

- **기준을 일관되게 적용**: 지적대로 설정한 기준(적절한 연령표준화 + 분산 추정치)을 그대로 유지하되, 분산 요건을 **원문이 비율을 인쇄했는지가 아니라 추출된 추정치에 분산이 실제로 있는지**(원문 인쇄 또는 원문 정보로 복구 가능)로 판정하도록 수정. 해당되는 5편(Melkonian 2019·Melkonian 2022·Liu 2012·Zhang 2022·Watanabe-Galloway 2015)이 Q8=No로 정정되어 **RoB Low 45 → 41편, Moderate 13 → 17편**, 대표 공급 연구의 RoB는 Low 16·Moderate 6.

- **평가 단위 명시**: "연구 전체와 추출한 추정치 중 무엇을 평가했는지"를 Methods와 Supplementary Table 5 Note에 명시. **각 연구는 이 리뷰가 그 연구에서 가져온 추정치의 출처로서 평가**하며, 항목별 판정 수준을 구분해 기술 — **Q1–Q7은 연구·레지스트리 수준 특성**(표집 프레임, 사례 확인, 사례수, 세팅·인구 기술, 커버리지, 침습성 유방암 확인, 인종·민족 측정 방식)이므로 어떤 추정치를 추출했는지와 무관하게 판정되고, **Q8만 추정치 자체에 의존**하므로 이 리뷰가 추출한 추정치를 기준으로 판정(원문이 구간을 인쇄했거나 원문 정보로 복구 가능하면 분산 있음으로 계산).

- **분산 요건을 Q8에 두는 근거**: 신뢰구간 미보고는 엄밀히 말해 비뚤림(추정치가 참값에서 체계적으로 벗어남)이 아니라 불확실성 보고의 결함이므로, 기준을 완화해 Q8에서 분리하는 선택지도 검토함. 그러나 ① 분산이 없으면 표준화와 가중이 적절했는지, 사례수가 안정적인 율을 낼 만한지 독자가 검증할 수 없어 JBI Q8(적절한 통계분석)의 취지에 직접 닿고, ② 불확실성이 제시되지 않으면 결과가 실제보다 확정적으로 보이며, ③ 특히 사례수가 적은 소수 집단·지역 셀에서는 구간이 넓을 수 있는데 점추정치만 제시되면 그 불안정성이 드러나지 않는다는 점(실제로 AI/AN 지역 추정치 0.57–1.33이 대부분 구간 없이 보고됨)을 고려해 **기준을 유지하고 일관 적용하는 쪽을 택함**. 대신 그 판정이 무엇을 뜻하는지는 아래와 같이 명시.

- **CI 미보고의 해석 주의**: "CI 미보고 자체가 반드시 높은 비뚤림 위험을 의미하지는 않는다"는 지적을 반영해, Methods와 S5 Note에 **이 Q8=No는 불확실성 보고가 불완전하다는 뜻이며 추정치가 편향되었다는 근거가 아니라는 점**과, 그 때문에 비율을 구간 없이 보고한 대규모 레지스트리 분석 몇 편이 moderate로 분류된다는 점을 함께 명시.

- **대안 제시 — 분산 요건을 Q8에서 분리하는 방안(지시 요청)**: 위 근거로 현행(분산 요건 유지)을 기본으로 반영했으나, 신뢰구간 미보고가 엄밀히는 비뚤림이 아니라는 점을 더 중시한다면 **Q8은 "명시된 표준인구로의 적절한 연령표준화"만 판정하고, 분산·구간 보고 여부는 RoB 등급과 분리해 별도로 기록**하는 방식도 가능합니다(분산 출처는 이미 Table 1의 ‡ 표기와 provenance 열로 추적 중이므로 정보 손실은 없습니다). 이 경우 실제 영향을 계산해 보면 Q8=No 9편이 Yes로 바뀌어 **RoB가 Low 41·Moderate 17 → Low 49·Moderate 9**, 저위험 제한 민감도가 **54/19/12 → 63 unchanged·14 changed·8 dropped**가 되고, Melkonian 2019가 Low로 복귀하므로 **AI/AN aggregate의 0.87 → 0.63 교체와 AI/AN 관련 9개 cell의 변경·탈락이 모두 사라집니다**. **다만 JBI 원문 지침을 확인한 결과, 이 대안은 채택하지 않는 쪽을 권고드립니다.** *JBI Critical Appraisal Checklist for Prevalence Studies*(2017) Q8 해설 원문은 다음과 같습니다 — "Was there appropriate statistical analysis? **Importantly, the numerator and denominator should be clearly reported, and percentages should be given with confidence intervals.** The methods section should be detailed enough for reviewers to identify the analytical technique used and how specific variables were measured…" 즉 **신뢰구간 보고는 JBI가 Q8에서 명시적으로 요구하는 요건**이므로, 분산 요건을 Q8에서 떼어내는 것은 체크리스트 해설로부터의 이탈이 되며 그만큼 별도 정당화가 필요해집니다. 현행(분산 요건을 Q8 안에 유지)이 도구의 지침을 그대로 따르는 쪽입니다. 이 근거는 응답서에만 두고 Methods에는 넣지 않았습니다 — Methods는 실제로 수행한 바만 적고 선택을 변론하지 않는다는 원칙에 따른 것이며, Q8을 '명시된 표준인구로의 연령표준화 + 분산'으로 판정했다는 사실 자체는 이미 Methods에 기술돼 있습니다.

  참고로 일반론으로는 비뚤림 위험과 정밀도(imprecision)를 별개로 다루는 것도 표준적이며(GRADE가 imprecision을 독립 영역으로 둠), prevalence 문헌에도 JBI 항목을 적용 가능한 형태로 고쳐 쓴 선례가 있습니다 — SeroTracker-RoB(Bobrovitz 외, *Res Synth Methods* 2023;14:414-426)는 JBI Q8을 '검사 특성 보정'과 '인구 특성 보정' 두 항목으로 **분할**하고 Q4는 '비뚤림이 아니라 보고 항목'이라며 **제외**했습니다. 다만 같은 연구가 분할한 두 항목 **양쪽 모두에 "the information necessary to determine the numerator, denominator, prevalence estimate, and confidence interval"을 Yes 조건으로 유지**했다는 점에서, 신뢰구간 요건 자체를 RoB에서 빼는 선례로는 볼 수 없습니다. 이 점까지 고려해 현행 유지를 권고드리며, 그럼에도 분리를 지시하시면 위 수치(Low 49·Moderate 9, 6a 63/14/8)대로 즉시 반영하겠습니다.

- **low-risk-only 분석에 반영**: 판정 변경을 민감도분석에 그대로 반영해 6a가 **59/14/12 → 54 unchanged / 19 changed / 12 dropped**로 갱신. 가장 큰 변화는 AI/AN 국가 aggregate로, 저위험 제한 시 대표가 **IHS-linked 0.87(2010–2015) → IHS-linked 0.63(1999–2004)**으로 교체됨. 교체 기전은 **불확실성 보고 형식의 차이**로, 주분석 대표인 Melkonian 2019는 추출 7행 모두 신뢰구간이 없어(Q8=No) moderate로 분류되어 제한에서 빠지고, 구간을 모두 보고한 Wingo 2008(7/7행 CI, Low)이 같은 IHS 계열 내에서 그 자리를 채움. 이는 본문에서 이미 기술한 IHS-linked 추정치의 시간적 상승과 같은 방향이지 동일 기간에 대한 두 자료원의 불일치가 아니지만, 이 교체로 **AI/AN이 Hispanic/Latina 아래로 내려가 aggregate 순위가 저위험 제한 하에서는 유지되지 않음**. Results와 Discussion에 해당 수치와 함께 "순위와 일부 near-null 부호를 확정된 것으로 읽지 말 것"을 명시. 반영 여부는 세 가지로 검증 — ① 6a에서 대표로 투입된 Moderate 연구 0건, ② 판정이 바뀐 5편이 6a 대표로 남은 건 0건, ③ 주분석에서 그 5편이 대표였던 5개 cell이 모두 changed로 전환. 내부 점검의 민감도-대표 정합(340쌍)과 본문 카운트 점검도 통과.
---

## 5. 연구의 포함·제외 및 synthesis 분류 기준을 통일해주세요.

> Methods에서는 같은 registry·기간·인구의 재보고를 제외한다고 했지만, Supplementary Table 2의 Giaquinto 2024와 Saka 2025는 같은 이유를 기재하면서 narrative 연구로 포함하고 있습니다. 중복 연구를 제외하는 경우와 서술적 종합에 남기는 경우를 명확히 구분해주세요.
>
> Li 2025의 분류 사유인 "single poolable estimate가 아님"도 현재 분석 방식과 맞지 않으므로, 수치 추출 가능 여부 등 실제 사유로 수정해주세요. Introduction과 Table 1에 남아 있는 대표값 선정 단위 "per registry family"도 Methods의 "per analytic cell"과 통일해주세요.

- **중복 제외 vs 서술적 종합 잔류 — 구분 원리를 Methods에 명시**: 종전 Methods는 "같은 registry·기간·인구의 재보고는 제외"만 기술해, 같은 사유가 적힌 연구가 narrative로 남아 있는 것과 어긋났음. 실제 판정 기준은 **"이미 포함된 다른 출판물이 그 내용을 담고 있는가"**였으므로 이를 원리로 명시하고 두 경우를 구분해 서술: ① 재보고는 독립 추정치가 아니어서 **어느 경우에도 대표값 후보가 되지 않음**; ② 그중 포함된 다른 출판물이 내용을 이미 담은 것(같은 시리즈의 **이전 연도판**, 포함된 분석의 **preprint·book-chapter판**)은 리뷰에 새 정보를 더하지 않으므로 **제외**(중복 55편 중 51편이 연례 통계 시리즈 이전판, 4편이 preprint·book-chapter 중복); ③ 반면 **시리즈의 최신 적격판**은 그 시리즈의 현재 서술을 담은 유일한 판이므로 리뷰에는 포함하되, 해당 registry·기간의 발생률은 전담 primary 연구가 이미 제공하므로 **서술적 종합에만 기여**; ④ 같은 registry family라도 기간·지역·subset이 다르면 별개 추정치로 보아 **민감도 overlap으로 유지**. 이로써 Giaquinto 2024(rec 0)와 Saka 2025(rec 4294)가 narrative에 남는 근거와, 같은 시리즈 이전판들이 제외된 근거가 하나의 기준으로 설명됨. 참고로 제외된 83편 중 51편이 연례 통계 시리즈의 **이전 연도판**(Breast cancer statistics 2015·2019, Cancer statistics for African Americans 2016·2022, Annual Report to the Nation 1973–1999 ~ 1975–2014 등)임을 확인. 즉 실제로는 "**시리즈별로 최신 적격판 1편만 남기고 이전 판은 중복으로 제외**"하는 규칙이 적용되고 있었으나 Methods에 서술되지 않아 지적된 불일치가 발생. Methods 적격기준에 해당 규칙과, **남긴 최신판은 해당 registry·기간의 발생률을 전담 primary 연구가 이미 제공하므로 대표값 후보로 쓰지 않고 서술적 종합에만 기여**한다는 점을 명시. 이로써 Giaquinto 2024(rec 0, Breast cancer statistics 2024)와 Saka 2025(rec 4294, Cancer statistics for African American and Black people 2025)가 같은 사유로 narrative에 남는 근거가 드러남.

- **Li 2025 분류 사유 수정**: 해당 연구는 rec 46(JAMA Netw Open 2025, SEER 22개 레지스트리 2010–2019, joinpoint 연간변화율 분석)으로 확인. 종전 표기 "single poolable estimate가 아님"은 pooling을 하지 않는 현재 분석 방식과 맞지 않으므로, 실제 사유인 **"연간 추세(annual percentage change)로만 보고해 단면 연령표준화율·비율을 추출할 수 없음"**으로 교체.

- **Supplementary Table 2의 narrative 사유 전면 실제화**: 점검 결과 narrative 118편 중 **103편이 "No recoverable NHW comparison" 한 문구로 일괄 표시**되고 있었음(개별 사유 부여는 15편). 실제 사유는 시리즈 재보고 9, 추세만 28, 사회경제적 비교 6, 비미국 비교군 5, 비율 아님(PIR 등) 5, 그림 전용 4 등으로 다양하므로, 적격성 기록에 사유가 있는 경우 그 사유를 유형별 문구로 표시하도록 수정 → **개별 사유 표시가 15편에서 57편으로 확대**. 사유 기록이 없는 나머지는 포괄 사유("NHW 기준 연령표준화율·비율을 복구할 수 없음")로 표시하고, 어떤 경우에 개별 사유가 표시되고 어떤 경우에 포괄 사유가 표시되는지를 Supplementary Table 2 Note에 명시.

- **Supplementary Table 2 사유 문구 간결화**: 사유 문구가 최장 164자로 길어 표에서 읽기 어려웠으므로 전 유형을 축약 — "연간 추세로만 보고해 단면 연령표준화율·비율을 추출할 수 없음"(164자) → "Reports an annual trend, not a cross-sectional rate or ratio"(60자) 식으로, 최장 119자·대부분 65자 이내로 정리. 표시되는 사유 유형과 편수는 그대로 유지.

- **자료원 약어 표기 정정**: Supplementary Table 2의 Data source 열에 약어가 풀리지 않거나 앞뒤가 어긋난 곳을 정정. 특히 **`SC`가 두 가지 뜻으로 쓰이고 있었음** — rec 402는 "State Cancer Profiles (SC)"로 적혀 SC가 State Cancer Profiles의 약어처럼 읽혔으나 원문은 **South Carolina** 주 연구였고, rec 453의 "SC + Ohio"도 South Carolina를 뜻함. 각각 **"State Cancer Profiles (South Carolina)"**, **"South Carolina and Ohio state registries (non-SEER)"**로 수정. 나머지 약어도 초출에서 풀어씀 — **CI5 = Cancer Incidence in Five Continents**(IARC 국제 발생률 자료집, rec 284·2732), **HCHS/SOL = Hispanic Community Health Study/Study of Latinos**(rec 1637). 셋 다 narrative 전용 연구로 추정치에는 관여하지 않음.

- **대표값 선정 단위 표기 통일**: Introduction("one representative population-based estimate per registry family"), Table 1 Note("one per registry family"), 본문 표·그림 Note에 남아 있던 **"per registry family"를 Methods의 "per analytic cell"로 통일**. registry family는 셀 내부의 중복 판정 단위로만 쓰인다는 점을 작성 지침에도 반영.

---

## 6. Discussion의 일부 해석을 신중하게 수정해주세요.

> 겹치는 registry를 이용한 여러 논문을 "independent sources"로 표현하지 않도록 수정해주세요. 또한 AI/AN 추정치가 0.56에서 0.87로 달라진 것은 서로 다른 연구의 비교이므로, 그 차이 전체를 IHS linkage의 효과로 설명해서는 안 됩니다. 관찰기간과 대상 지역의 차이 및 PRCDA 자료의 적용 범위를 함께 설명해주세요.

- **"independent sources" 표현 삭제**: 겹치는 레지스트리에서 나온 논문들을 독립 자료원으로 부르지 않도록, 기여 서술의 "cells corroborated by two or more **independent sources**"를 **"서로 다른 registry family에서 온 둘 이상의 자료원이 뒷받침하는 cell"**로 교체하고, 이어서 **"미국 레지스트리는 중첩 구조이므로 서로 다른 family의 출판물도 겹치는 사례를 포함할 수 있어 이들이 완전히 독립적이지는 않다"**는 단서를 명시. 38 vs 47이라는 구분 자체는 유지하되 그 근거를 "독립성"이 아니라 "자료원 수"로 재정의. **다만 이 교체 과정에서 수치-문구 불일치가 발생했음을 재점검에서 확인하고 정정** — 38/47은 85개 cell 중 **추출 가능한 추정치를 2편 이상 가진 cell(38) 대 1편뿐인 cell(47)** 의 구분으로 계산된 값인데, 교체된 문구가 이를 "**서로 다른 registry family**에서 온 둘 이상"으로 서술해 조건을 더 좁게 표현하고 있었음. 실제로 재계산하면 서로 다른 registry family가 2개 이상인 cell은 **27개**(38개의 부분집합, 나머지 11개는 같은 family 내 복수 연구)이므로, 본문을 "**2편 이상이 채울 수 있었던 cell 38개(그중 27개는 서로 다른 registry family 2개 이상에서 옴) 대 1편뿐인 47개**"로 두 수치를 모두 제시하도록 수정. 이어지는 "레지스트리 중첩으로 서로 다른 family도 완전히 독립적이지는 않다"는 단서는 그대로 유지. Results의 narrative 서술에 있던 "no **independent** quantitative estimate"도 중의성이 있어 "no **extractable** quantitative estimate"로 수정(Introduction과 Supplementary Table 4 Note의 "중첩 레지스트리 추정치는 독립적이지 않다"는 서술은 올바른 취지이므로 유지).

- **AI/AN 0.56 → 0.87 해석 수정**: 두 값이 서로 다른 연구라는 점을 명시하고, 차이를 IHS linkage 단독 효과로 설명하지 않도록 **세 가지 차이를 함께 기술**. ① **관찰기간** — unlinked 추정치(Gopalani 2020, USCS)는 1999–2015, IHS-linked 추정치(Melkonian 2019)는 2010–2015이며 AI/AN 비율은 그 구간에 상승(IHS-linked 내부에서도 1999–2004의 0.63 → 2010–2015의 0.87). ② **대상 지역과 PRCDA 적용 범위** — IHS-linked 값은 Purchased/Referred Care Delivery Area 카운티로 한정되고, 원문이 "(whites) living in IHS purchased/referred care delivery area counties"로 밝힌 대로 **이 제한이 NHW 비교군에도 적용**되므로 분자·분모가 모두 전국 인구와 다른 집단을 기술. 나아가 **PRCDA가 AI/AN 인구를 어느 정도 포함하는지(대표성 범위)**도 함께 명시 — 원문에서 "PRCDA counties … contain or are located adjacent to federally recognized tribal lands … Approximately 53% of the U.S. AI/AN population resides in PRCDA counties"와 표 각주의 지역별 커버리지(East 16.4% ~ Alaska 100%, 전국 53.0%)를 확인해, IHS-linked 값이 AI/AN 인구의 약 절반을 기술하며 커버리지가 높은 지역일수록 카운티 내 AI/AN 인구 비중이 큰 지역이라는 점을 Discussion에 기술. 따라서 이 값은 전국 AI/AN 인구 전체의 추정치로 읽히지 않도록 함. ③ **인종 확인 방식(linkage)** — 셋 중 이것만이 연계 자체의 효과. 본문에 "세 차이가 함께 작용하며 그중 세 번째만 linkage"라고 명시.

- **연쇄 서술 정합**: "unlinked 값이 낮은 것은 불완전한 사례 확인을 반영한다"는 문장도 **더 넓은 진단기간과 PRCDA가 아닌 전국 커버리지를 함께** 반영한 것으로 수정하고, 이어지는 결론도 "AI/AN–NHW 비교는 자료원의 **사례 확인 방식과 진단기간·지리적 범위에 함께 좌우된다**"로 교체.

---

## 7. 표·그림의 수치와 최종 문서의 배치를 확인해주세요.

> 색상과 표 서식은 개선됐지만, PDF 변환본에서는 Figure 2 하단의 일부 지역값과 설명이 여전히 잘립니다. 또한 AANHPI aggregate의 CI가 Table 1에서는 [0.752–0.788], Figure 2에서는 [0.751–0.787]로 다릅니다. 표와 그림을 동일한 최종 데이터에서 생성하고, 추가된 지역값과 White/NHW 비교군 표시도 일치하는지 확인해주세요.

- **CI 불일치 원인 확인 — 그림이 구간을 재계산하고 있었음**: Table 1은 추출표에 저장된 구간을 그대로 인쇄하는 반면, 그림의 원본 데이터(`Table_main_forest.csv`)는 구간을 버리고 **로그척도 표준오차만 보관한 뒤 exp(y ± 1.96·SE)로 다시 만들고** 있었음. 원문 보고 구간은 로그척도에서 대칭이 아닌 경우가 많아 이 왕복 과정에서 소수 셋째 자리가 이동 → 지적하신 AANHPI aggregate가 표 [0.752–0.788], 그림 [0.751–0.787]로 갈렸음. 점검 결과 같은 유형의 불일치가 **76행 중 47행**에 있었음(예: Hispanic aggregate 0.707–0.731 vs 0.706–0.730, Navajo 0.44–0.55 vs 0.438–0.548). 그림 데이터가 추출표의 구간을 **그대로** 싣도록 수정(SE는 가중·pooling 계산에만 사용) → 47건 전부 해소되어 **표와 그림의 구간이 전 cell에서 동일**.

- **AI/AN 지역값 누락 정정**: 그림 데이터가 신뢰구간 없는 대표값(점추정치)을 **aggregate 차원에서만** 싣도록 되어 있어, Melkonian 2019의 지역 점추정치 4건(Southwest 0.57·East 0.61·Pacific Coast 0.93·Northern Plains 1.05)이 아예 빠져 있었음. 그 결과 Table 1은 AI/AN 지역을 7개 제시하는데 Figure 2는 3개만 보여주고 있었음. 모든 차원의 점추정치를 싣도록 수정(그림 데이터 77행 → **85행 = 85개 cell 전부**)하고, Figure 2의 AI/AN 블록도 **Table 1과 같은 7개 지역·같은 순서**로 제시. 구간이 없는 값은 막대 없이 점으로 그리고 "(point est.)"로 표기.

- **White/NHW 비교군 표시 일치**: 그림에는 비교군 표시가 없어 Table 1의 † 표기와 대조할 수 없었음. 그림 데이터에 comparator 열을 추가하고, 비교군이 비층화 White인 행에 Figure 2에서도 **†**를 표기(Figure 2 범위에서는 Alaska Native 1.09 [0.99–1.21] †). ‡(리뷰가 계산한 구간) 표기도 표와 동일 기준으로 적용.

- **PDF 변환본에서 하단이 잘리던 원인**: Manuscript 문서에서 Table 1과 Figure 1–3을 **하나의 가로(landscape) 섹션**에 함께 배치하고 있었음. 가로 페이지의 사용 가능한 높이는 7.0인치인데 Figure 2는 세로로 긴 그림이라 8.25인치로 삽입돼 **아래쪽이 페이지 밖으로 밀려 잘렸음** — 지적하신 "하단 일부 지역값과 설명"이 정확히 그 부분. 표(가로)와 그림(세로)을 **별도 섹션으로 분리**하고, 그림은 파일의 실제 종횡비를 읽어 인쇄 영역 안에 맞추도록 변경(Figure 2 = 6.33 × 8.12인치, 세로 페이지 인쇄 영역 7.0 × 9.5인치). 종횡비를 코드에 상수로 박아두던 것(660×792, 실제 비율과 불일치)도 제거해 그림을 다시 생성해도 늘어나거나 넘치지 않도록 함. Figure 1·3도 같은 방식으로 재산정(Figure 3은 7.92인치로 인쇄 영역 폭을 넘고 있었음).

- **그림 안에 넣던 설명을 문서 본문으로 이동**: Figure 2 하단 5줄짜리 범례를 PNG 안에 그려 넣고 있어서 그림이 잘리면 설명도 함께 잘렸음. 이를 그림 아래 **Note 문단(실제 텍스트)**으로 옮겨 페이지에 맞춰 흐르도록 하고, 중복되던 그림 내부 제목도 제거(그림 제목은 Figure 2 heading이 이미 담고 있음).

- **용지 크기 미지정 문제 발견·수정**: 제출 문서(Manuscript)가 **용지 크기를 지정하지 않고** 있었음. Word는 Letter, LibreOffice 등 변환기는 A4를 기본값으로 삼기 때문에 **같은 파일이 변환 도구에 따라 다르게 페이지가 나뉘고**, A4는 인쇄 가능 폭이 Letter보다 0.25인치 좁아 그림이 더 쉽게 넘침. 세 섹션 모두 Letter로 명시하고, 그림 크기는 Letter·A4 중 **좁은 쪽 기준**으로 맞춰 어느 용지로 변환해도 넘치지 않도록 함. 아울러 그림 섹션이 페이지 나눔 표시를 무시하고 있어 **Figure 2 제목만 앞 페이지 하단에 남고 그림은 다음 페이지로 밀리는** 현상이 있어 페이지 나눔을 반영하도록 수정.

- **실제 PDF로 확인**: 수정본을 PDF로 변환해 해당 페이지를 직접 확인 — Figure 2는 **제목·그림 전체(AI/AN 7개 지역 포함)·Note 전문이 한 페이지 안에** 들어가고 잘리는 부분이 없음. Figure 1·3도 인쇄 영역 안에 들어감.

- **보충자료 점검**: 같은 기준으로 Supplementary_Materials도 PDF 변환해 전수 확인 — 용지 크기는 이미 Letter로 명시돼 있었고, 표 9개의 열 너비 합계가 모두 가로 페이지 인쇄 폭(10인치) 이내여서 **가로로 잘리는 표는 없음**(최대 Table 4 = 9.65인치). Table 6a의 변경 전후 연구 병기(예: Native Hawaiian 1.270 Gomez 2026 → 1.211 Miller 2008)도 정상 출력. Supplementary Table 4의 값 셀 222개가 모두 추출표의 값과 일치함을 대조로 확인. 다만 **문서 끝에 빈 페이지 1장**이 붙고 있었음 — 그림 전용 세로 섹션을 보충자료에도 두었는데 보충자료에는 그림이 없어 빈 섹션이 페이지 하나를 만들고 있었음. 그림이 없으면 섹션 자체를 만들지 않도록 수정(39쪽 → 38쪽).

- **지역값·비교군 표시 일치 확인**: Figure 2가 실제로 그린 27개 행 전부를 Table 1과 1:1 대조 — 새로 넣은 AI/AN 지역 4건(Southwest 0.57·East 0.61·Pacific Coast 0.93·Northern Plains 1.05)이 모두 "(point est.)"로 표와 동일하게 표시되고, † 표기는 Alaska Native 1.09 [0.99–1.21] 한 건으로 표·그림이 일치하며 그 외 행에 잘못 붙은 †는 없음. ‡ 표기(리뷰 계산 구간)도 전 행 일치. **불일치 0건.**

- **재발 방지 점검 추가**: 표와 그림이 다시 어긋나지 않도록 교차점검에 **[I] Table 1 vs 본문 그림** 항목을 신설 — Table 1의 38개 cell과 **Figure 2가 실제로 그린 27개 행**을 각각 **값·구간·† 표기·‡ 표기 네 가지 모두** 대조(총 65건). Figure 2는 행 목록을 코드에 직접 적는 방식이라 입력 파일만 대조하면 *행이 빠지거나 다른 cell을 가리키는* 오류를 못 잡으므로, 그림 생성 시 **실제로 그린 내용을 별도 파일로 남기고** 그것을 검사 대상으로 삼음. 검사가 실제로 작동하는지는 고의로 값·구간·† 세 가지를 틀리게 넣어 **3건 모두 검출됨**을 확인. 현재 65/65 통과. 대조를 정확히 하기 위해 Table 1 출력에 analytic dimension 열을 추가(표의 섹션 제목은 표시용이라 AANHPI가 두 섹션으로 나뉘어 있었음). 전체 교차점검 A–I 전부 통과.

---

## 추가 수정 (피드백 항목 외, 자체 점검에서 발견)

- **비층화 White 비교군 셀 수 명시 및 구성 정정**: 본문이 해당 셀을 "a minority of cells"로만 서술하고 있어 Table 1의 † 표기 수와 대조가 안 됐음. 실제로 세어 **85개 셀 중 19개**임을 확인하고 Abstract·Results 개요·Discussion 2곳을 숫자로 교체("in 19 of the 85 cells", "NHW for 66 of the 85 representatives and an unstratified White group for the other 19").

  다만 **85개 중 Table 1에 실리는 것은 38개**(18개 analytic dimension 중 6개)이므로, 본문의 19라는 숫자와 Table 1에서 세어지는 † 개수가 어긋납니다. 실제로 **19개 중 Table 1에 보이는 것은 5개, 나머지 14개는 보충자료에만** 있음. 이 점을 Results에 명시하고("marked † wherever they appear—five of them in Table 1 and the other 14 in Supplementary Table 4"), Table 1 Note에도 **이 표가 85개 중 38개를 싣는다는 점**과 **† 19개 중 5개가 이 표에 나타난다는 점**을 추가.

  이어서 **Supplementary Table 4에도 같은 유형의 불일치가 없는지 확인**한 결과 2건을 추가로 정정. ① S4는 **† 표기를 쓰지 않고** `Comparator` 열에 `non-Hispanic White (NHW)` / `White (not NH-stratified)`로 풀어 쓰는데, 본문이 "나머지 14개는 Supplementary Table 4에 †로 표시"처럼 읽히게 적혀 있었음(S4에서 †를 찾으면 0건) → "S4는 모든 추출 추정치의 비교군을 열에 이름으로 표시한다"로 수정. ② Methods가 "19 of the 85 representatives **carry the mark**"로 적고 있었으나 실제로 †가 **눈에 보이는 것은 5건뿐**이고 나머지 14건은 본문 표·그림에 실리지 않아 표기 자체가 존재하지 않음 → "19개가 **비층화 White 기준을 쓴다**, 비교군은 S4에 이름으로 기재되며 본문에 실리는 셀에 한해 †를 붙인다"로 정정. Discussion 마지막 문장의 같은 표현도 함께 수정. ③ S4에서 비층화 White 행을 세면 **31개**로 본문의 19와 다른데(대표값 19 + overlap 전용 12), 이 관계가 S4에 적혀 있지 않아 **Comparator Note에 명시** — "31 of the 222 rows use an unstratified White reference; 19 of those are the representative for their cell, which is the count the main text reports, and the other 12 are overlapping estimates listed here only." 수치는 표의 행에서 직접 세도록 해 다시 어긋나지 않게 함.

  정리하면 세 숫자가 각각 다른 것을 세며, 이제 세 곳 모두에 근거가 적혀 있음 — **5**(Table 1에 †로 보이는 수, Table 1 Note), **19**(85개 대표값 중 비층화 White, Abstract·Results·Methods·Discussion), **31**(S4 222행 중 비층화 White, S4 Comparator Note).

  구성 서술에도 두 건의 오류가 있어 함께 정정. ① Methods·Results가 해당 셀을 "**the** receptor-defined subtype cells and two age-specific Black cells"로 적어 **아형 셀 전부(36개)가 해당되는 것처럼** 읽혔으나 실제는 **36개 중 16개** → "16 of the 36 receptor-defined subtype cells"로 수정. ② **Alaska Native 1건이 목록에서 누락**돼 있었음 — Table 1에서 †가 붙은 셀을 본문 목록과 대조하면 찾을 수 없는 상태였음. 다만 이 셀은 성격이 달라 별도로 기술: 나머지 18개는 **NHW 비교군 자료가 아예 없어** †가 붙은 반면, Alaska Native는 **NHW 자료가 존재하는데도 coverage 우선 규칙이 비층화 White 기준 registry를 선택**해 붙은 것. 이 차이가 6c(NHW 비교군 제한)에서 18개는 dropped, Alaska Native만 changed(1.09 → IHS-linked 1.25)로 갈리는 이유이므로 Methods에 명시.

- **SIR 개수 오기 정정 및 표기 약속 삭제**: 본문·보충자료가 일관되게 **"the single SIR"**(SIR 1건)로 서술하고 있었으나 실제로는 **2건** — Goggins 2009(Asian Indian/Pakistani, 0.61)와 **Moore 2015(Alaska Native, 1.14)**. Methods·Results·Supplementary Table 6b 캡션·6 Note·민감도 코드 주석을 모두 2건으로 정정.

  아울러 **두 SIR 모두 overlap 전용이어서 85개 대표값에는 SIR이 0건**임을 확인. 그런데 Table 1 Note와 Results 머리말이 "IRR unless marked as an SIR", "or noted as an SIR"처럼 **독자가 찾을 수 없는 표기를 약속**하고 있었으므로 해당 문구를 삭제하고 "본문 추정치는 전부 IRR"로 명시. Methods에도 "Neither is the representative for its cell, so no estimate reported in the main text is an SIR"을 추가해 두 SIR이 어디에 남아 있는지(Supplementary Table 4) 분명히 함. 6b 민감도는 코드가 이미 두 건 모두 제외하고 있어 **수치는 불변**(35 unchanged / 4 changed / 46 dropped).

- **Table 1 Effect 열 삭제**: 대표값 85개가 전부 IRR이므로 Table 1의 Effect 열이 38행 모두 "IRR" 한 값이었음 → 열 삭제하고 남은 열 너비를 재배분. 효과측정 단위는 Note에 "the effect measure is the incidence rate ratio (IRR) throughout"로 기술.

- **Methods의 SIR·provenance 서술 보완**: SIR 관련 서술을 재점검하며 두 건을 추가 정정. ① **비율 방향 규칙이 Methods에 없었음** — 모든 추정치를 소수집단÷White 방향으로 기록하고, 원문이 반대 방향으로 보고한 경우 **역수 변환 후 그렇게 표시한다**는 규칙(item 1의 Kong 2020 처리 근거)이 Methods에 기술돼 있지 않아 추가. ② provenance 목록이 실제 라벨을 다 포괄하지 못해(분산 없이 원문 발생률만 있는 경우) "with a reported or Poisson-derived variance, or none where neither was available"로 보완.

- **Supplementary Table 4의 SIR 표시 누락 정정**: Methods가 두 SIR을 "labelled as SIRs (Supplementary Table 4)"라고 하나, 실제 S4에서는 **Goggins 2009만 Std pop 칸에 "SIR (indirect…)"로 드러나고 Moore 2015는 "world standard (IARC)"로 적혀 SIR인지 알 수 없었음**. 손으로 적은 Std pop 문자열이 아니라 **provenance 라벨에서 자동으로** 추정치 옆에 `(SIR)`을 붙이도록 수정 → 두 건 모두 표시됨. S4에 효과측정 Note도 추가("an incidence rate ratio unless marked (SIR)… 두 SIR은 모두 overlap이므로 모든 대표값과 본문 추정치는 rate ratio").

- **Discussion 민감도 문단의 수치 오류 정정**: "저위험 제한이 가장 많은 셀을 움직였다(**19 of the 66** it could re-examine)"에서 분모가 틀렸음 — 6a가 재검토할 수 있었던 셀은 85 − dropped 12 = **73개**이고, **66은 6c(NHW 비교군 제한)의 unchanged 수**로 다른 민감도의 값이 섞여 들어간 것. **73**으로 정정(19/73).

  같은 유형(네 민감도 사이에서 숫자가 교차 오염되는 오류)이 재발하지 않도록 교차점검 [E]에 **민감도 수치 probe를 추가** — 6a–6d 각각의 unchanged·changed·dropped와 **재검토 가능 셀 수(unchanged+changed)**를 해당 산출 파일에서 재계산해 본문 서술과 대조(점검 대상 32개 → **42개**). 검사가 실제로 작동하는지는 고의로 66으로 되돌려 **검출됨**을 확인.

- **AI/AN 선정 예외의 커버리지 양보를 명시**: AI/AN은 IHS 연계 확인 방식이 커버리지·비교군 기준을 **덮어쓰는 예외**인데, Methods가 예외임은 밝히면서 **비교군 양보만 사례(Alaska Native)로 설명하고 커버리지 양보는 설명하지 않고** 있었음. 실제로 전국 AI/AN 셀에서는 **USCS(미국 인구 ~99% 커버리지, Ellington 2022, 0.683)를 강등하고 IHS-PRCDA(AI/AN 인구의 ~53%, Melkonian 2019, 0.87)를 대표로** 선택하므로, 6번 응답에서 PRCDA 53%를 본문에 명시한 이상 "왜 99%를 제치고 53%를 쓰는가"가 바로 제기될 수 있는 상태였음. Methods에 **양보의 실제 내용을 한 문장으로** 명시 — 전국 AI/AN 셀에서 미국 인구 ~99%를 포괄하는 자료원 대신 PRCDA 카운티 한정 자료원을 택했고 강등된 추정치는 민감도분석에 유지됨. 왜 커버리지보다 확인 방식이 우선인지에 대한 논증은 넣지 않음 — 이유는 바로 앞 문장("unlinked 레지스트리가 이 인구를 과소집계하므로")에 이미 있고, Methods는 수행한 바를 적는 자리이기 때문.

- **Results 민감도 서술의 과잉 주장 정정 및 문장 분리**: 3번 항목에서 Discussion의 안심형 표현은 걷어냈으나 **Results에는 "the pattern held **throughout**"(전반에 걸쳐 패턴이 유지됨)이 남아 있어** Discussion의 신중한 서술("각 제한이 재검토할 수 있었던 cell에 한해, 그것도 일률적이지 않게")과 어긋나고, 실제 결과(6a에서 AI/AN aggregate가 0.87→0.63으로 바뀌어 **aggregate 순위가 유지되지 않음**)와도 맞지 않았음 → "각 제한은 채울 수 있는 cell에서 대표를 재선정하고 나머지는 제외했다"는 사실 서술로 교체하고, 6a 문단에 **순위가 뒤바뀐 사실**을 명시. 아울러 네 민감도가 **세미콜론 7개로 이어진 219단어 한 문장**이었으므로 제한별로 문단을 나눔(문단당 21~73단어). 수치는 불변이며 교차점검 [E]의 민감도 probe 전부 통과.

- **Discussion 한계 문단의 누락 보완 및 분리**: 한계 문단이 293단어 한 덩어리에 여섯 가지 한계를 담고 있었고, **"Finally,"** 뒤에 두 개의 한계가 더 이어져 신호가 어긋났음 → 네 문단으로 나누고 "Finally"를 실제 마지막 항목으로 옮김(31·142·55·74단어). 내용상 **단일 평가자 한계에서 비뚤림 평가가 빠져 있던 것을 보완** — 종전에는 "Screening, full-text selection, and extraction"만 단일 평가자로 수행했다고 적었으나 **비뚤림 평가도 저자 1인이 수행**했고(Methods에 기술돼 있음) **JBI 체크리스트 자체가 두 명의 평가자를 권장**하므로, 해당 목록에 risk-of-bias appraisal을 포함하고 체크리스트 권고와 다르다는 점을 명시. 2차 피드백이 "JBI를 2인 독립 평가로"를 지적한 사안이므로 한계에 드러나 있어야 함.

- **기여점 문단의 근거 공백 서술 정정**: "AI/AN의 **지역값과 전국 aggregate가 신뢰구간 없는 점추정치**"라고 일반화하고 있었으나, 지역값 7개 중 **구간이 있는 것이 3개**(Navajo 0.49 [0.44–0.55], Alaska Native 1.09 [0.99–1.21], Southern Plains 1.33 [1.26–1.41])이므로 사실과 달랐음 → **"지역값 7개 중 4개와 전국 aggregate"**로 정정. 같은 문장의 다른 주장도 데이터로 재확인해 구체화 — 단일 자료원 셀은 Middle Eastern 1개, **Hispanic-origin 4개 전부**, Pacific Islander 2개이고, AI/AN 아형은 **4개 셀 모두 unlinked 레지스트리 기반이되 단일 자료원인 것은 3개**(TNBC는 3개 자료원)이므로 "each rest on a single regional or unlinked source"라는 뭉뚱그린 표현을 각각의 실제 수로 교체.

- **본문 수정 내역 문서 신설**: 어느 문단이 어떻게 바뀌었는지 원고에서 바로 확인하실 수 있도록 **`Changes_for_review`(별도 문서)**를 함께 제출. 문단별로 ① 소속 섹션 ② **원고에서 Ctrl+F로 검색할 문구**(바뀐 문장 기준) ③ 변경 전/후 문장 ④ 수정 사유를 표시. 이번 라운드 기준 **28개 문단**(Discussion 11·Methods 9·Results 6·Abstract 1·Introduction 1). 이후 라운드에서도 자동 갱신됨.
