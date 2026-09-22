5차 피드백 각 항목에 대한 수정 내용과 근거. 모든 수치는 수정 후 재생성한 최종 데이터에서 재계산한 값이며, 표·그림·보충자료·제출 문서는 동일한 추출표에서 함께 재생성.

---

## 1. 자료원과 effect estimate의 비교 방향을 다시 확인해주세요.

- **Miller 2008 자료원·coverage 정정**: 원문 "Native Hawaiian rates calculated only for the state of Hawaii"로 확인 — Hawaii Tumor Registry가 Native Hawaiian 혈통 환자를 전수 분류하기 때문에 Native Hawaiian 발생률만 Hawaii 주로 한정 보고. Table 1·Supplementary Table 4의 "NAACCR/CiNA (~93%)"는 과대 기재였으므로 **Hawaii Tumor Registry(Native Hawaiian은 Hawaii 주 한정)**로 정정하고, 자료원 라벨도 `NAACCR-API` → `HTR`로 맞춰 라벨-coverage 불일치 제거.

- **Native Hawaiian 대표값 재선정**: coverage 정정으로 기존 선정 규칙(전국 SEER > 단일 주)이 그대로 적용 → **Gomez 2026(SEER-21, 2018–2022) 1.27 [1.21–1.33]**이 대표, Miller 2008(1.21 [1.12–1.31])은 sensitivity overlap으로 이동. Results·Discussion의 Native Hawaiian 값 1.21 → **1.27** 갱신. NHPI aggregate 1.21은 Gomez 2026이 보고한 별개 값이므로 불변.

- **연쇄 카운트 갱신**: 대표값 공급 연구 23 → **22편**, overlap 전용 35 → **36편**, 저위험 제한 민감도 60/13/12 → **59/14/12**(unchanged/changed/dropped). 헤드라인 aggregate IRR(Hispanic 0.72·AANHPI 0.77·AI/AN 0.87·NHB 0.93, NHB TNBC 1.95)은 불변.

- **Kong 2020 비교 방향 정정**: 원문이 overall만 NHW를 분자로 서술("non-Hispanic White women was 31.3 …, which was higher compared with the incidence among Black women (IRR, 1.04; 95% CI, 1.02–1.05)")하고 같은 문단의 다른 aggregate는 minority 기준(Asian/PI 0.90, AI/AN 0.82, Hispanic 0.79)임을 확인 — 한 논문 내 방향 혼재. 해당 행을 **Black/NHW 0.96 [0.95–0.98]**로 역수 변환하고 provenance를 `directly-reported-IRR-inverted`로 표기. Supplementary Note 1의 "방향 모호로 미기록" 설명도 실제 처리(역수)와 일치하게 수정. 역수 후 값은 같은 셀 분포(0.81–0.98)·대표값 Ellington 2022(0.933)·동시기 SEER 추정치(Du 0.937, Gomez 0.941, Davis Lynn 0.971)와 정합.

- **비교 방향 전수 점검(추가 확인)**: 같은 문제의 잔존 여부를 추출표 전체로 점검. 발생률에서 계산한 122행은 minority ÷ NHW로 방향이 고정되고 내부 점검에서 원문 발생률로 재검증됨. 원문 보고값 98행 중 같은 셀에 추정치가 3개 이상 있어 상호 대조가 가능한 행에서 방향 이탈 후보 3건 검출 → Nash 2022는 외부 NHW 기준을 쓴 계산값, Wingo 2008은 원문이 national 0.63·Northern Plains 0.89·Southern Plains 0.89·Alaska 0.99로 모두 minority 기준, Zahnd 2019는 원문 "non-Hispanic Black women had … higher rates than non-Hispanic White women (RR = 1.07; 95% CI 1.04–1.11)"로 확인되어 3건 모두 방향 정확. 셀 내 대조가 불가능한 33행 중 1을 넘는 9행도 NHB 여성의 40세·50세 미만 교차(1.01–1.16), Asian/Hispanic/AI·AN의 HR−/HER2+ 아형(1.04–1.41) 등 알려진 소견과 부합. 방향 반전이 필요한 행은 Kong 2020 overall Black 1건.

- **자료원 기재 전수 점검(추가 확인)**: Miller 건과 같은 유형(원문의 실제 자료원 범위와 기재 불일치)이 다른 연구에도 남아 있는지 점검. 이 유형은 라벨-분류 자동 점검으로는 걸러지지 않으므로, 대표값을 공급하는 22개 연구와 overlap 전용 연구까지 자료원 기재를 원문 범위와 대조. ① 소수 subgroup의 대표이면서 전국급 coverage로 분류된 10건은 모두 Gomez 2026이며, 원문이 "21 registries (excluding Alaska and Seattle, Washington)"와 표 제목 "SEER-21 Program"으로 전국 집계를 명시하고 특정 주 한정 서술이 없어 기재가 정확함을 확인. ② 나머지 대표 자료원(Hawaii Tumor Registry, California-CCR, Florida, IHS-PRCDA, Alaska Native Tumor Registry, USCS, SEER)도 모두 실제 범위대로 분류돼 있음 — Navajo Nation 레지스트리는 Navajo 지역 셀의 대표이므로 지역 한정이 정합. ③ SEER 하위범위(9/17/18/21)를 단일 'SEER-national' tier로 묶은 설계상 단순화가 있으나, 좁은 SEER가 같은 셀의 더 넓은 SEER 추정치를 이겨 대표가 된 사례는 **0건**으로 선정 왜곡 없음. ④ overlap 전용 연구까지 같은 기준으로 확대 점검한 결과 **Goggins 2009에서 같은 유형의 오류를 1건 추가 발견** — 추출표 registry에는 "SEER (SF/Seattle/Detroit/Atlanta/CT/LA/SanJose)"로 7개 registry가 정확히 기재돼 있었으나 coverage 분류 규칙이 문자열의 'SEER'만 보고 전국급(SEER-national)으로 tier를 부여하고 있었음. 원문이 "data from the seven SEER registries … Connecticut, and the cities of San Francisco, San Jose, Los Angeles, Detroit, Seattle, and Atlanta"로 전국 SEER이 아님을 명시하므로, registry 표기를 "SEER 7-registry subset"으로 정리하고 분류 규칙에 registry-subset 조건을 추가해 Jin 2016(8-state SEER+NPCR)과 같은 regional tier로 재분류. Goggins는 overlap 전용이어서 주분석 대표·헤드라인 결과는 불변이고, 민감도 카운트도 변동 없음. 결과적으로 자료원 기재·분류 정정은 Miller 2008과 Goggins 2009 2건.

- **이전 점검이 두 건을 놓친 이유와 점검 방식 보완**: 4차 라운드에서 대표 연구 전수를 원문과 대조했고(자료원·기간·비교군·값) 그 기록은 `SOURCE_VERIFICATION_LOG`에 남아 있으나, 자료원 점검이 **논문이 명시한 data system 단위**로 이루어진 것이 한계였음. Miller 2008은 논문 수준 자료원(NAACCR/SEER API registries)이 기재와 일치했고 Native Hawaiian만 Hawaii로 한정된다는 **그룹 단위 제한**은 그 단위에서 드러나지 않아 통과. Goggins 2009는 registry 문자열 자체가 정확해 원문 대조로도 걸리지 않고, **분류 규칙이 문자열의 'SEER'만 보고 tier를 부여**한 것이 문제여서 라벨-분류 자동 점검(라벨과 분류가 서로 모순되는 경우만 탐지)도 통과. 이번 라운드에서는 점검 단위를 **그룹 × 자료원**으로 바꾸고, 기재뿐 아니라 **분류 규칙이 부여한 coverage tier가 원문 범위와 일치하는지**까지 확인하는 방식으로 보완. 그 결과 위 2건을 찾아 정정했고, 동일 기준으로 남은 연구에서는 추가 불일치가 확인되지 않음.

---

## 2. 표준인구의 영향이 비율에서 상쇄된다는 설명을 수정해주세요.

- **지적 수용**: 같은 표준인구를 쓰더라도 두 집단의 연령별 발생률 곡선 형태가 다르면 표준 가중치를 달리 잡을 때 각 집단의 표준화율이 서로 다른 폭으로 움직이므로, 그 비율도 표준인구에 따라 달라짐. 따라서 "비율이 표준인구 선택에 의존하지 않는다"는 종전 서술은 부정확한 것으로 확인.

- **Discussion 한계 문단 수정**: "비율이 공유 표준화를 상쇄한다(a ratio cancels the shared standardization)"는 표현을 삭제하고, ① 셀 내부에서는 분자·분모가 하나의 표준인구·기간·지역을 공유하므로 비율이 **내부적으로 일관**하다는 점과 ② 그럼에도 **비율이 표준인구를 상쇄하지는 않는다**(두 집단의 연령별 발생률 형태가 달라 다른 표준 가중치는 표준화율과 그 비율을 서로 다른 폭으로 이동시킴)는 점을 구분해 기술. 이어서 **셀 간에는 표준인구·연령구조·지역·진단기간 차이가 그대로 남는다**고 명시.

- **Supplementary Table 4 Note 수정**: "연구 내에서 형성되므로 그 연구의 표준인구 선택에 의존하지 않는다"를 삭제하고, 같은 취지(셀 내부 일관성 / 표준인구 비상쇄 / 연구 간 비교 불가)로 재작성. NHW 대비 비율로 제시해도 연구 간 표준인구·기간·지역 차이가 해소되지 않음을 Note에 유지.

- **Supplementary Note 1 표현 정정**: rec 2 항목의 "IRR is invariant to the 20+ vs all-age standard"도 단정적 표현이므로 "essentially unaffected"(0–19세가 분자·분모에 거의 기여하지 않음)로 완화.

- **경험적 근거는 별도로 유지**: 표준인구 제한 민감도분석(2000 US 표준으로 제한)에서 85셀 중 83셀이 불변, 2셀만 변경(1960 Segi 표준 대표가 2000 US 표준 추정치로 교체, HR− 1.80→1.60, HR+ 0.82→0.70)이라는 결과는 그대로 보고. 이는 "표준인구가 비율에 영향이 없다"는 주장이 아니라, 이 자료에서는 대부분 대표값이 이미 2000 US 표준이어서 실제 영향이 제한적이었다는 경험적 관찰로 기술.
