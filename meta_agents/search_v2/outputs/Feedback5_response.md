본 응답은 5차 피드백의 각 항목에 대해 수정 내용과 근거를 정리한 것입니다. 모든 수치는 수정 후 재생성한 최종 데이터에서 다시 계산한 값이며, 표·그림·보충자료·제출 문서는 동일한 추출표에서 함께 재생성했습니다.

---

## 1. 자료원과 effect estimate의 비교 방향을 다시 확인해주세요.

- **Miller 2008의 자료원·coverage 정정**: 원문을 다시 확인한 결과 "Native Hawaiian rates calculated only for the state of Hawaii"로, Hawaii Tumor Registry가 Native Hawaiian 혈통을 가진 모든 환자를 분류하는 노력 때문에 Native Hawaiian 발생률만 Hawaii 주로 한정해 보고하고 있었습니다. 지적대로 Table 1과 Supplementary Table 4의 "NAACCR/CiNA (~93%)" 표기는 과대 기재였으므로 자료원을 **Hawaii Tumor Registry(Native Hawaiian은 Hawaii 주 한정)**로 정정하고, 자료원 라벨도 `NAACCR-API` → `HTR`로 맞춰 라벨과 coverage 분류가 어긋나지 않게 했습니다.

- **Native Hawaiian 대표값 재선정**: coverage가 정정되면서 기존 선정 규칙(전국 SEER > 단일 주 레지스트리)이 그대로 적용되어, Gomez 2026(SEER-21, 2018–2022) **1.27 [1.21–1.33]**이 대표가 되고 Miller 2008(1.21 [1.12–1.31])은 sensitivity overlap으로 이동했습니다. Results와 Discussion의 Native Hawaiian 값을 1.21 → **1.27**로 갱신했습니다. NHPI aggregate 1.21은 Gomez 2026이 보고한 별개 값이므로 변동이 없습니다.

- **연쇄 카운트 갱신**: 대표값을 공급한 연구가 23 → **22편**, overlap 전용이 35 → **36편**이 되었고, 저위험 제한 민감도분석은 unchanged/changed/dropped가 60/13/12 → **59/14/12**로 바뀌었습니다. 헤드라인 aggregate IRR(Hispanic 0.72·AANHPI 0.77·AI/AN 0.87·NHB 0.93, NHB TNBC 1.95)은 영향을 받지 않았습니다.

- **Kong 2020의 비교 방향 정정**: 원문은 "non-Hispanic White women was 31.3 …, which was higher compared with the incidence among Black women (IRR, 1.04; 95% CI, 1.02–1.05)"로 **overall 값만 NHW를 분자로** 서술하고, 같은 문단의 다른 aggregate는 minority를 분자로 보고합니다(Asian/PI 0.90, AI/AN 0.82, Hispanic 0.79). 즉 한 논문 안에서 방향이 섞여 있었습니다. 지적대로 일관되게 반영하기 위해 해당 행을 **Black/NHW 0.96 [0.95–0.98]**로 역수 변환하고 provenance를 `directly-reported-IRR-inverted`로 표기했으며, Supplementary Note 1에 남아 있던 "방향이 모호하여 미기록"이라는 설명도 실제 처리(역수 변환)와 일치하게 고쳤습니다. 역수 후 값은 같은 셀의 다른 추정치 분포(0.81–0.98)와 대표값 Ellington 2022(0.933), 동시기 SEER 추정치(Du 0.937·Gomez 0.941·Davis Lynn 0.971)에 부합합니다.

- **비교 방향 전수 점검**: 같은 문제가 다른 연구에도 있는지 추출표 전체를 점검했습니다. 발생률에서 계산한 122행은 minority ÷ NHW로 방향이 고정되며 내부 점검에서 원문 발생률로 재검증됩니다. 원문 보고값 98행 중 같은 셀에 추정치가 3개 이상 있어 상호 대조가 가능한 행에서 방향 이탈 후보 3건이 검출되었으나, Nash 2022는 외부 NHW 기준을 사용한 계산값이고, Wingo 2008은 원문이 national 0.63·Northern Plains 0.89·Southern Plains 0.89·Alaska 0.99로 모두 minority 기준이며, Zahnd 2019는 원문이 "non-Hispanic Black women had … higher rates than non-Hispanic White women (RR = 1.07; 95% CI 1.04–1.11)"로 확인되어 세 건 모두 방향이 정확했습니다. 셀 내 대조가 불가능한 33행 중 1을 넘는 9행도 NHB 여성의 40세·50세 미만 교차(1.01–1.16)와 Asian/Hispanic/AI·AN의 HR−/HER2+ 아형(1.04–1.41)처럼 알려진 소견과 부합합니다. 결과적으로 방향 반전이 필요한 행은 Kong 2020의 overall Black 한 건이었습니다.
