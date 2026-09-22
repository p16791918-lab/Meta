5차 피드백 각 항목에 대한 수정 내용과 근거. 모든 수치는 수정 후 재생성한 최종 데이터에서 재계산한 값이며, 표·그림·보충자료·제출 문서는 동일한 추출표에서 함께 재생성.

---

## 1. 자료원과 effect estimate의 비교 방향을 다시 확인해주세요.

- **Miller 2008 자료원·coverage 정정**: 원문 "Native Hawaiian rates calculated only for the state of Hawaii"로 확인 — Hawaii Tumor Registry가 Native Hawaiian 혈통 환자를 전수 분류하기 때문에 Native Hawaiian 발생률만 Hawaii 주로 한정 보고. Table 1·Supplementary Table 4의 "NAACCR/CiNA (~93%)"는 과대 기재였으므로 **Hawaii Tumor Registry(Native Hawaiian은 Hawaii 주 한정)**로 정정하고, 자료원 라벨도 `NAACCR-API` → `HTR`로 맞춰 라벨-coverage 불일치 제거.

- **Native Hawaiian 대표값 재선정**: coverage 정정으로 기존 선정 규칙(전국 SEER > 단일 주)이 그대로 적용 → **Gomez 2026(SEER-21, 2018–2022) 1.27 [1.21–1.33]**이 대표, Miller 2008(1.21 [1.12–1.31])은 sensitivity overlap으로 이동. Results·Discussion의 Native Hawaiian 값 1.21 → **1.27** 갱신. NHPI aggregate 1.21은 Gomez 2026이 보고한 별개 값이므로 불변.

- **연쇄 카운트 갱신**: 대표값 공급 연구 23 → **22편**, overlap 전용 35 → **36편**, 저위험 제한 민감도 60/13/12 → **59/14/12**(unchanged/changed/dropped). 헤드라인 aggregate IRR(Hispanic 0.72·AANHPI 0.77·AI/AN 0.87·NHB 0.93, NHB TNBC 1.95)은 불변.

- **Kong 2020 비교 방향 정정**: 원문이 overall만 NHW를 분자로 서술("non-Hispanic White women was 31.3 …, which was higher compared with the incidence among Black women (IRR, 1.04; 95% CI, 1.02–1.05)")하고 같은 문단의 다른 aggregate는 minority 기준(Asian/PI 0.90, AI/AN 0.82, Hispanic 0.79)임을 확인 — 한 논문 내 방향 혼재. 해당 행을 **Black/NHW 0.96 [0.95–0.98]**로 역수 변환하고 provenance를 `directly-reported-IRR-inverted`로 표기. Supplementary Note 1의 "방향 모호로 미기록" 설명도 실제 처리(역수)와 일치하게 수정. 역수 후 값은 같은 셀 분포(0.81–0.98)·대표값 Ellington 2022(0.933)·동시기 SEER 추정치(Du 0.937, Gomez 0.941, Davis Lynn 0.971)와 정합.

- **비교 방향 전수 점검(추가 확인)**: 같은 문제의 잔존 여부를 추출표 전체로 점검. 발생률에서 계산한 122행은 minority ÷ NHW로 방향이 고정되고 내부 점검에서 원문 발생률로 재검증됨. 원문 보고값 98행 중 같은 셀에 추정치가 3개 이상 있어 상호 대조가 가능한 행에서 방향 이탈 후보 3건 검출 → Nash 2022는 외부 NHW 기준을 쓴 계산값, Wingo 2008은 원문이 national 0.63·Northern Plains 0.89·Southern Plains 0.89·Alaska 0.99로 모두 minority 기준, Zahnd 2019는 원문 "non-Hispanic Black women had … higher rates than non-Hispanic White women (RR = 1.07; 95% CI 1.04–1.11)"로 확인되어 3건 모두 방향 정확. 셀 내 대조가 불가능한 33행 중 1을 넘는 9행도 NHB 여성의 40세·50세 미만 교차(1.01–1.16), Asian/Hispanic/AI·AN의 HR−/HER2+ 아형(1.04–1.41) 등 알려진 소견과 부합. 방향 반전이 필요한 행은 Kong 2020 overall Black 1건.

- **자료원 기재 전수 점검(추가 확인)**: Miller 건과 같은 유형(원문의 실제 자료원 범위와 기재 불일치)이 다른 연구에도 남아 있는지 점검. 이 유형은 라벨-분류 자동 점검으로는 걸러지지 않으므로, 대표값을 공급하는 22개 연구와 overlap 전용 연구까지 자료원 기재를 원문 범위와 대조. ① 소수 subgroup의 대표이면서 전국급 coverage로 분류된 10건은 모두 Gomez 2026이며, 원문이 "21 registries (excluding Alaska and Seattle, Washington)"와 표 제목 "SEER-21 Program"으로 전국 집계를 명시하고 특정 주 한정 서술이 없어 기재가 정확함을 확인. ② 나머지 대표 자료원(Hawaii Tumor Registry, California-CCR, Florida, IHS-PRCDA, Alaska Native Tumor Registry, USCS, SEER)도 모두 실제 범위대로 분류돼 있음 — Navajo Nation 레지스트리는 Navajo 지역 셀의 대표이므로 지역 한정이 정합. ③ SEER 하위범위(9/17/18/21)를 단일 'SEER-national' tier로 묶은 설계상 단순화가 있으나, 좁은 SEER가 같은 셀의 더 넓은 SEER 추정치를 이겨 대표가 된 사례는 **0건**으로 선정 왜곡 없음. ④ overlap 전용 연구까지 같은 기준으로 확대 점검한 결과 **Goggins 2009에서 같은 유형의 오류를 1건 추가 발견** — 추출표 registry에는 "SEER (SF/Seattle/Detroit/Atlanta/CT/LA/SanJose)"로 7개 registry가 정확히 기재돼 있었으나 coverage 분류 규칙이 문자열의 'SEER'만 보고 전국급(SEER-national)으로 tier를 부여하고 있었음. 원문이 "data from the seven SEER registries … Connecticut, and the cities of San Francisco, San Jose, Los Angeles, Detroit, Seattle, and Atlanta"로 전국 SEER이 아님을 명시하므로, registry 표기를 "SEER 7-registry subset"으로 정리하고 분류 규칙에 registry-subset 조건을 추가해 Jin 2016(8-state SEER+NPCR)과 같은 regional tier로 재분류. Goggins는 overlap 전용이어서 주분석 대표·헤드라인 결과는 불변이고, 민감도 카운트도 변동 없음. ⑤ 여기서 두 건 모두 *분류 규칙이 문자열을 잘못 읽은* 유형이었으므로, 점검을 개별 연구가 아니라 **추출표의 고유 registry 문자열 39개 전부 × 부여된 coverage tier**로 확대해 전수 대조 → **2건 추가 발견**. "Metropolitan Atlanta (SEER)"(Lund 2010)와 "New Mexico (SEER)"(Zahrieh 2021)는 SEER 프로그램의 **단일 대도시·단일 주 registry**인데 문자열의 'SEER' 때문에 전국급 tier로 분류돼 있었음. 각각 단일 지역 tier(LA County와 동급)·단일 주 tier로 재분류. 두 연구 모두 overlap 전용이고(Zahrieh 2021은 AI/AN undercount로 이미 강등된 행) 민감도 대표 교체에도 투입되지 않아 주분석 대표·Table 1·헤드라인 결과·민감도 카운트는 모두 불변. 다만 'New Mexico'는 지역을 시사하는 키워드 자동 탐색으로는 걸리지 않아 39개 문자열을 하나씩 확인해 찾았음을 부기함. 결과적으로 자료원 분류 정정은 Miller 2008·Goggins 2009·Lund 2010·Zahrieh 2021 4건이며, 39개 문자열 전수 대조에서 남은 불일치는 없음.

- **이전 점검이 두 건을 놓친 이유와 점검 방식 보완**: 4차 라운드에서 대표 연구 전수를 원문과 대조했고(자료원·기간·비교군·값) 그 기록은 `SOURCE_VERIFICATION_LOG`에 남아 있으나, 자료원 점검이 **논문이 명시한 data system 단위**로 이루어진 것이 한계였음. Miller 2008은 논문 수준 자료원(NAACCR/SEER API registries)이 기재와 일치했고 Native Hawaiian만 Hawaii로 한정된다는 **그룹 단위 제한**은 그 단위에서 드러나지 않아 통과. Goggins 2009는 registry 문자열 자체가 정확해 원문 대조로도 걸리지 않고, **분류 규칙이 문자열의 'SEER'만 보고 tier를 부여**한 것이 문제여서 라벨-분류 자동 점검(라벨과 분류가 서로 모순되는 경우만 탐지)도 통과. 이번 라운드에서는 점검 단위를 **그룹 × 자료원**으로 바꾸고, 기재뿐 아니라 **분류 규칙이 부여한 coverage tier가 원문 범위와 일치하는지**까지 확인하는 방식으로 보완. 그 결과 위 2건을 찾아 정정했고, 동일 기준으로 남은 연구에서는 추가 불일치가 확인되지 않음.

---

## 2. 표준인구의 영향이 비율에서 상쇄된다는 설명을 수정해주세요.

- **지적 수용**: 같은 표준인구를 쓰더라도 두 집단의 연령별 발생률 곡선 형태가 다르면 표준 가중치를 달리 잡을 때 각 집단의 표준화율이 서로 다른 폭으로 움직이므로, 그 비율도 표준인구에 따라 달라짐. 따라서 "비율이 표준인구 선택에 의존하지 않는다"는 종전 서술은 부정확한 것으로 확인.

- **Discussion 한계 문단 수정**: "비율이 공유 표준화를 상쇄한다(a ratio cancels the shared standardization)"는 표현을 삭제하고, ① 셀 내부에서는 분자·분모가 하나의 표준인구·기간·지역을 공유하므로 비율이 **내부적으로 일관**하다는 점과 ② 그럼에도 **비율이 표준인구를 상쇄하지는 않는다**(두 집단의 연령별 발생률 형태가 달라 다른 표준 가중치는 표준화율과 그 비율을 서로 다른 폭으로 이동시킴)는 점을 구분해 기술. 이어서 **셀 간에는 표준인구·연령구조·지역·진단기간 차이가 그대로 남는다**고 명시.

- **Supplementary Table 4 Note 수정**: "연구 내에서 형성되므로 그 연구의 표준인구 선택에 의존하지 않는다"를 삭제하고, 같은 취지(셀 내부 일관성 / 표준인구 비상쇄 / 연구 간 비교 불가)로 재작성. NHW 대비 비율로 제시해도 연구 간 표준인구·기간·지역 차이가 해소되지 않음을 Note에 유지.

- **Supplementary Note 1 표현 정정**: rec 2 항목의 "IRR is invariant to the 20+ vs all-age standard"도 단정적 표현이므로 "essentially unaffected"(0–19세가 분자·분모에 거의 기여하지 않음)로 완화.

- **경험적 근거는 별도로 유지**: 표준인구 제한 민감도분석(2000 US 표준으로 제한)에서 85셀 중 83셀이 불변, 2셀만 변경(1960 Segi 표준 대표가 2000 US 표준 추정치로 교체, HR− 1.80→1.60, HR+ 0.82→0.70)이라는 결과는 그대로 보고. 이는 "표준인구가 비율에 영향이 없다"는 주장이 아니라, 이 자료에서는 대부분 대표값이 이미 2000 US 표준이어서 실제 영향이 제한적이었다는 경험적 관찰로 기술.

---

## 3. 민감도분석의 조건과 실제 결과를 일치시켜주세요.

- **Goggins 2009 SIR — 조건과 코드 불일치 정정**: Methods는 SIR이 간접표준화이므로 directly-reported-IRR 민감도에서 제외한다고 서술했으나, 코드의 필터 집합이 `{directly-reported-IRR, directly-reported-SIR}`로 **SIR을 포함**하고 표 제목도 "IRR/SIR only"였음. 지적대로 코드를 Methods에 맞춰 필터에서 SIR을 제거하고, 표 제목·캡션·Note를 "directly reported IRR only(간접표준화 SIR 제외)"로 수정. 그 결과 Goggins 2009의 0.61 [0.56–0.66]이 Table 6b에서 빠지고 Asian Indian/Pakistani 셀은 dropped로 이동 → **6b 결과가 35 unchanged / 5 changed / 45 dropped → 35 unchanged / 4 changed / 46 dropped**로 갱신(Results 서술도 함께 수정). 한편 Kong 2020의 역수 변환 행(item 1)은 원문 보고값의 방향만 바꾼 것이어서 계산 유도값과 구분해 directly-reported 계열에 포함시키고, 그 처리 근거를 코드 주석과 Note에 명시.

- **제외된 cell 전부 제시**: Table 6b만 changed 셀만 싣고 dropped를 생략하고 있었음(6a·6c·6d는 이미 changed·dropped 모두 제시). 6b도 dropped를 모두 포함하도록 수정해 **네 표 모두 changed·dropped 전 cell을 제시**(보충표 행 수 624 → 669).

- **변경 전후 출처 연구 표시**: 네 표의 값 컬럼에 해당 추정치를 공급한 연구를 병기하도록 변경 — "Main analysis: IRR [95% CI] — study"와 "Under restriction: IRR [95% CI] — study". 따라서 changed 셀에서는 **교체된 연구와 교체한 연구가 한 행에서 함께** 보이고(예: Japanese 아형 셀에서 Gomez 2026 → Jin 2016), dropped 셀은 "not available under this restriction"으로 표시.

- **dropped cell 해석 주의 명시**: 제한을 충족하지 못해 제외된 cell을 견고성 확인으로 읽지 않도록, Supplementary Table 6 Note에 "dropped cell은 그 제한 하에서 **검증되지 않은(untested)** 것이며 확인된 것이 아니다"를 명시. Discussion의 민감도 서술도 "대부분의 차이가 불일치가 아니라 자격 미충족에 따른 drop"이라는 안심형 표현을 걷어내고, **각 제한이 재검토할 수 있었던 cell에 한해 패턴이 유지되었으며 directly-reported 제한만으로도 85개 중 46개 cell이 미검토로 남는다**는 사실을 함께 기술.

---

## 4. RoB 판정 기준과 개별 연구 평가의 일관성을 확인해주세요.

- **불일치 원인 확인**: Q8 판정 코드가 분산 유무를 `s["cis"] > 0 or direct or withvar`로 계산하고 있었고, 여기서 `direct`는 **provenance가 원문 보고 비율이면 참**이 되도록 돼 있었음. 그 결과 원문이 비율을 인쇄했지만 신뢰구간이 없는 연구는 분산이 있는 것처럼 통과 → Melkonian 2019(directly-reported-IRR, 추출 7행 모두 CI 없음)는 Q8=Yes·Low, Harper 2009(computed-from-rates, 추출 4행 모두 CI 없음)는 Q8=No·Moderate로 **같은 조건에서 판정이 갈렸음**.

- **기준을 일관되게 적용**: 지적대로 설정한 기준(적절한 연령표준화 + 분산 추정치)을 그대로 유지하되, 분산 요건을 **원문이 비율을 인쇄했는지가 아니라 추출된 추정치에 분산이 실제로 있는지**(원문 인쇄 또는 원문 정보로 복구 가능)로 판정하도록 수정. 해당되는 5편(Melkonian 2019·Melkonian 2022·Liu 2012·Zhang 2022·Watanabe-Galloway 2015)이 Q8=No로 정정되어 **RoB Low 45 → 41편, Moderate 13 → 17편**, 대표 공급 연구의 RoB는 Low 16·Moderate 6.

- **평가 단위 명시**: "연구 전체와 추출한 추정치 중 무엇을 평가했는지"를 Methods와 Supplementary Table 5 Note에 명시. **각 연구는 이 리뷰가 그 연구에서 가져온 추정치의 출처로서 평가**하며, 항목별 판정 수준을 구분해 기술 — **Q1–Q7은 연구·레지스트리 수준 특성**(표집 프레임, 사례 확인, 사례수, 세팅·인구 기술, 커버리지, 침습성 유방암 확인, 인종·민족 측정 방식)이므로 어떤 추정치를 추출했는지와 무관하게 판정되고, **Q8만 추정치 자체에 의존**하므로 이 리뷰가 추출한 추정치를 기준으로 판정(원문이 구간을 인쇄했거나 원문 정보로 복구 가능하면 분산 있음으로 계산).

- **분산 요건을 Q8에 두는 근거**: 신뢰구간 미보고는 엄밀히 말해 비뚤림(추정치가 참값에서 체계적으로 벗어남)이 아니라 불확실성 보고의 결함이므로, 기준을 완화해 Q8에서 분리하는 선택지도 검토함. 그러나 ① 분산이 없으면 표준화와 가중이 적절했는지, 사례수가 안정적인 율을 낼 만한지 독자가 검증할 수 없어 JBI Q8(적절한 통계분석)의 취지에 직접 닿고, ② 불확실성이 제시되지 않으면 결과가 실제보다 확정적으로 보이며, ③ 특히 사례수가 적은 소수 집단·지역 셀에서는 구간이 넓을 수 있는데 점추정치만 제시되면 그 불안정성이 드러나지 않는다는 점(실제로 AI/AN 지역 추정치 0.57–1.33이 대부분 구간 없이 보고됨)을 고려해 **기준을 유지하고 일관 적용하는 쪽을 택함**. 대신 그 판정이 무엇을 뜻하는지는 아래와 같이 명시.

- **CI 미보고의 해석 주의**: "CI 미보고 자체가 반드시 높은 비뚤림 위험을 의미하지는 않는다"는 지적을 반영해, Methods와 S5 Note에 **이 Q8=No는 불확실성 보고가 불완전하다는 뜻이며 추정치가 편향되었다는 근거가 아니라는 점**과, 그 때문에 비율을 구간 없이 보고한 대규모 레지스트리 분석 몇 편이 moderate로 분류된다는 점을 함께 명시.

- **대안 제시 — 분산 요건을 Q8에서 분리하는 방안(지시 요청)**: 위 근거로 현행(분산 요건 유지)을 기본으로 반영했으나, 신뢰구간 미보고가 엄밀히는 비뚤림이 아니라는 점을 더 중시한다면 **Q8은 "명시된 표준인구로의 적절한 연령표준화"만 판정하고, 분산·구간 보고 여부는 RoB 등급과 분리해 별도로 기록**하는 방식도 가능합니다(분산 출처는 이미 Table 1의 ‡ 표기와 provenance 열로 추적 중이므로 정보 손실은 없습니다). 이 경우 실제 영향을 계산해 보면 Q8=No 9편이 Yes로 바뀌어 **RoB가 Low 41·Moderate 17 → Low 49·Moderate 9**, 저위험 제한 민감도가 **54/19/12 → 63 unchanged·14 changed·8 dropped**가 되고, Melkonian 2019가 Low로 복귀하므로 **AI/AN aggregate의 0.87 → 0.63 교체와 AI/AN 관련 9개 cell의 변경·탈락이 모두 사라집니다**. 두 방식 모두 내부적으로 일관되며 어느 쪽이든 그에 맞춰 RoB 표·민감도·본문 서술을 함께 갱신할 수 있으므로, 비뚤림 위험 평가에 불확실성 보고를 포함할지에 대한 지시를 주시면 반영하겠습니다.

- **low-risk-only 분석에 반영**: 판정 변경을 민감도분석에 그대로 반영해 6a가 **59/14/12 → 54 unchanged / 19 changed / 12 dropped**로 갱신. 가장 큰 변화는 AI/AN 국가 aggregate로, 저위험 제한 시 대표가 **IHS-linked 0.87(2010–2015) → IHS-linked 0.63(1999–2004)**으로 교체됨. 교체 기전은 **불확실성 보고 형식의 차이**로, 주분석 대표인 Melkonian 2019는 추출 7행 모두 신뢰구간이 없어(Q8=No) moderate로 분류되어 제한에서 빠지고, 구간을 모두 보고한 Wingo 2008(7/7행 CI, Low)이 같은 IHS 계열 내에서 그 자리를 채움. 이는 본문에서 이미 기술한 IHS-linked 추정치의 시간적 상승과 같은 방향이지 동일 기간에 대한 두 자료원의 불일치가 아니지만, 이 교체로 **AI/AN이 Hispanic/Latina 아래로 내려가 aggregate 순위가 저위험 제한 하에서는 유지되지 않음**. Results와 Discussion에 해당 수치와 함께 "순위와 일부 near-null 부호를 확정된 것으로 읽지 말 것"을 명시. 반영 여부는 세 가지로 검증 — ① 6a에서 대표로 투입된 Moderate 연구 0건, ② 판정이 바뀐 5편이 6a 대표로 남은 건 0건, ③ 주분석에서 그 5편이 대표였던 5개 cell이 모두 changed로 전환. 내부 점검의 민감도-대표 정합(340쌍)과 본문 카운트 점검도 통과.
---

## 5. 연구의 포함·제외 및 synthesis 분류 기준을 통일해주세요.

- **중복 제외 vs 서술적 종합 잔류 — 구분 원리를 Methods에 명시**: 종전 Methods는 "같은 registry·기간·인구의 재보고는 제외"만 기술해, 같은 사유가 적힌 연구가 narrative로 남아 있는 것과 어긋났음. 실제 판정 기준은 **"이미 포함된 다른 출판물이 그 내용을 담고 있는가"**였으므로 이를 원리로 명시하고 두 경우를 구분해 서술: ① 재보고는 독립 추정치가 아니어서 **어느 경우에도 대표값 후보가 되지 않음**; ② 그중 포함된 다른 출판물이 내용을 이미 담은 것(같은 시리즈의 **이전 연도판**, 포함된 분석의 **preprint·book-chapter판**)은 리뷰에 새 정보를 더하지 않으므로 **제외**(중복 55편 중 51편이 연례 통계 시리즈 이전판, 4편이 preprint·book-chapter 중복); ③ 반면 **시리즈의 최신 적격판**은 그 시리즈의 현재 서술을 담은 유일한 판이므로 리뷰에는 포함하되, 해당 registry·기간의 발생률은 전담 primary 연구가 이미 제공하므로 **서술적 종합에만 기여**; ④ 같은 registry family라도 기간·지역·subset이 다르면 별개 추정치로 보아 **민감도 overlap으로 유지**. 이로써 Giaquinto 2024(rec 0)와 Saka 2025(rec 4294)가 narrative에 남는 근거와, 같은 시리즈 이전판들이 제외된 근거가 하나의 기준으로 설명됨. 참고로 제외된 83편 중 51편이 연례 통계 시리즈의 **이전 연도판**(Breast cancer statistics 2015·2019, Cancer statistics for African Americans 2016·2022, Annual Report to the Nation 1973–1999 ~ 1975–2014 등)임을 확인. 즉 실제로는 "**시리즈별로 최신 적격판 1편만 남기고 이전 판은 중복으로 제외**"하는 규칙이 적용되고 있었으나 Methods에 서술되지 않아 지적된 불일치가 발생. Methods 적격기준에 해당 규칙과, **남긴 최신판은 해당 registry·기간의 발생률을 전담 primary 연구가 이미 제공하므로 대표값 후보로 쓰지 않고 서술적 종합에만 기여**한다는 점을 명시. 이로써 Giaquinto 2024(rec 0, Breast cancer statistics 2024)와 Saka 2025(rec 4294, Cancer statistics for African American and Black people 2025)가 같은 사유로 narrative에 남는 근거가 드러남.

- **Li 2025 분류 사유 수정**: 해당 연구는 rec 46(JAMA Netw Open 2025, SEER 22개 레지스트리 2010–2019, joinpoint 연간변화율 분석)으로 확인. 종전 표기 "single poolable estimate가 아님"은 pooling을 하지 않는 현재 분석 방식과 맞지 않으므로, 실제 사유인 **"연간 추세(annual percentage change)로만 보고해 단면 연령표준화율·비율을 추출할 수 없음"**으로 교체.

- **Supplementary Table 2의 narrative 사유 전면 실제화**: 점검 결과 narrative 118편 중 **103편이 "No recoverable NHW comparison" 한 문구로 일괄 표시**되고 있었음(개별 사유 부여는 15편). 실제 사유는 시리즈 재보고 9, 추세만 28, 사회경제적 비교 6, 비미국 비교군 5, 비율 아님(PIR 등) 5, 그림 전용 4 등으로 다양하므로, 적격성 기록에 사유가 있는 경우 그 사유를 유형별 문구로 표시하도록 수정 → **개별 사유 표시가 15편에서 57편으로 확대**. 사유 기록이 없는 나머지는 포괄 사유("NHW 기준 연령표준화율·비율을 복구할 수 없음")로 표시하고, 어떤 경우에 개별 사유가 표시되고 어떤 경우에 포괄 사유가 표시되는지를 Supplementary Table 2 Note에 명시.

- **대표값 선정 단위 표기 통일**: Introduction("one representative population-based estimate per registry family"), Table 1 Note("one per registry family"), 본문 표·그림 Note에 남아 있던 **"per registry family"를 Methods의 "per analytic cell"로 통일**. registry family는 셀 내부의 중복 판정 단위로만 쓰인다는 점을 작성 지침에도 반영.

---

## 6. Discussion의 일부 해석을 신중하게 수정해주세요.

- **"independent sources" 표현 삭제**: 겹치는 레지스트리에서 나온 논문들을 독립 자료원으로 부르지 않도록, 기여 서술의 "cells corroborated by two or more **independent sources**"를 **"서로 다른 registry family에서 온 둘 이상의 자료원이 뒷받침하는 cell"**로 교체하고, 이어서 **"미국 레지스트리는 중첩 구조이므로 서로 다른 family의 출판물도 겹치는 사례를 포함할 수 있어 이들이 완전히 독립적이지는 않다"**는 단서를 명시. 38 vs 47이라는 구분 자체는 유지하되 그 근거를 "독립성"이 아니라 "자료원 수"로 재정의. **다만 이 교체 과정에서 수치-문구 불일치가 발생했음을 재점검에서 확인하고 정정** — 38/47은 85개 cell 중 **추출 가능한 추정치를 2편 이상 가진 cell(38) 대 1편뿐인 cell(47)** 의 구분으로 계산된 값인데, 교체된 문구가 이를 "**서로 다른 registry family**에서 온 둘 이상"으로 서술해 조건을 더 좁게 표현하고 있었음. 실제로 재계산하면 서로 다른 registry family가 2개 이상인 cell은 **27개**(38개의 부분집합, 나머지 11개는 같은 family 내 복수 연구)이므로, 본문을 "**2편 이상이 채울 수 있었던 cell 38개(그중 27개는 서로 다른 registry family 2개 이상에서 옴) 대 1편뿐인 47개**"로 두 수치를 모두 제시하도록 수정. 이어지는 "레지스트리 중첩으로 서로 다른 family도 완전히 독립적이지는 않다"는 단서는 그대로 유지. Results의 narrative 서술에 있던 "no **independent** quantitative estimate"도 중의성이 있어 "no **extractable** quantitative estimate"로 수정(Introduction과 Supplementary Table 4 Note의 "중첩 레지스트리 추정치는 독립적이지 않다"는 서술은 올바른 취지이므로 유지).

- **AI/AN 0.56 → 0.87 해석 수정**: 두 값이 서로 다른 연구라는 점을 명시하고, 차이를 IHS linkage 단독 효과로 설명하지 않도록 **세 가지 차이를 함께 기술**. ① **관찰기간** — unlinked 추정치(Gopalani 2020, USCS)는 1999–2015, IHS-linked 추정치(Melkonian 2019)는 2010–2015이며 AI/AN 비율은 그 구간에 상승(IHS-linked 내부에서도 1999–2004의 0.63 → 2010–2015의 0.87). ② **대상 지역과 PRCDA 적용 범위** — IHS-linked 값은 Purchased/Referred Care Delivery Area 카운티로 한정되고, 원문이 "(whites) living in IHS purchased/referred care delivery area counties"로 밝힌 대로 **이 제한이 NHW 비교군에도 적용**되므로 분자·분모가 모두 전국 인구와 다른 집단을 기술. 나아가 **PRCDA가 AI/AN 인구를 어느 정도 포함하는지(대표성 범위)**도 함께 명시 — 원문에서 "PRCDA counties … contain or are located adjacent to federally recognized tribal lands … Approximately 53% of the U.S. AI/AN population resides in PRCDA counties"와 표 각주의 지역별 커버리지(East 16.4% ~ Alaska 100%, 전국 53.0%)를 확인해, IHS-linked 값이 AI/AN 인구의 약 절반을 기술하며 커버리지가 높은 지역일수록 카운티 내 AI/AN 인구 비중이 큰 지역이라는 점을 Discussion에 기술. 따라서 이 값은 전국 AI/AN 인구 전체의 추정치로 읽히지 않도록 함. ③ **인종 확인 방식(linkage)** — 셋 중 이것만이 연계 자체의 효과. 본문에 "세 차이가 함께 작용하며 그중 세 번째만 linkage"라고 명시.

- **연쇄 서술 정합**: "unlinked 값이 낮은 것은 불완전한 사례 확인을 반영한다"는 문장도 **더 넓은 진단기간과 PRCDA가 아닌 전국 커버리지를 함께** 반영한 것으로 수정하고, 이어지는 결론도 "AI/AN–NHW 비교는 자료원의 **사례 확인 방식과 진단기간·지리적 범위에 함께 좌우된다**"로 교체.

---

## 7. 표·그림의 수치와 최종 문서의 배치를 확인해주세요.

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
