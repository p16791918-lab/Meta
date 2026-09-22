5차 피드백 각 항목에 대한 수정 내용과 근거. 모든 수치는 수정 후 재생성한 최종 데이터에서 재계산한 값이며, 표·그림·보충자료·제출 문서는 동일한 추출표에서 함께 재생성.

---

## 1. 자료원과 effect estimate의 비교 방향을 다시 확인해주세요.

- **Miller 2008 자료원·coverage 정정**: 원문 "Native Hawaiian rates calculated only for the state of Hawaii"로 확인 — Hawaii Tumor Registry가 Native Hawaiian 혈통 환자를 전수 분류하기 때문에 Native Hawaiian 발생률만 Hawaii 주로 한정 보고. Table 1·Supplementary Table 4의 "NAACCR/CiNA (~93%)"는 과대 기재였으므로 **Hawaii Tumor Registry(Native Hawaiian은 Hawaii 주 한정)**로 정정하고, 자료원 라벨도 `NAACCR-API` → `HTR`로 맞춰 라벨-coverage 불일치 제거.

- **Native Hawaiian 대표값 재선정**: coverage 정정으로 기존 선정 규칙(전국 SEER > 단일 주)이 그대로 적용 → **Gomez 2026(SEER-21, 2018–2022) 1.27 [1.21–1.33]**이 대표, Miller 2008(1.21 [1.12–1.31])은 sensitivity overlap으로 이동. Results·Discussion의 Native Hawaiian 값 1.21 → **1.27** 갱신. NHPI aggregate 1.21은 Gomez 2026이 보고한 별개 값이므로 불변.

- **연쇄 카운트 갱신**: 대표값 공급 연구 23 → **22편**, overlap 전용 35 → **36편**, 저위험 제한 민감도 60/13/12 → **59/14/12**(unchanged/changed/dropped). 헤드라인 aggregate IRR(Hispanic 0.72·AANHPI 0.77·AI/AN 0.87·NHB 0.93, NHB TNBC 1.95)은 불변.

- **Kong 2020 비교 방향 정정**: 원문이 overall만 NHW를 분자로 서술("non-Hispanic White women was 31.3 …, which was higher compared with the incidence among Black women (IRR, 1.04; 95% CI, 1.02–1.05)")하고 같은 문단의 다른 aggregate는 minority 기준(Asian/PI 0.90, AI/AN 0.82, Hispanic 0.79)임을 확인 — 한 논문 내 방향 혼재. 해당 행을 **Black/NHW 0.96 [0.95–0.98]**로 역수 변환하고 provenance를 `directly-reported-IRR-inverted`로 표기. Supplementary Note 1의 "방향 모호로 미기록" 설명도 실제 처리(역수)와 일치하게 수정. 역수 후 값은 같은 셀 분포(0.81–0.98)·대표값 Ellington 2022(0.933)·동시기 SEER 추정치(Du 0.937, Gomez 0.941, Davis Lynn 0.971)와 정합.

- **비교 방향 전수 점검**: 같은 문제의 잔존 여부를 추출표 전체로 점검. 발생률에서 계산한 122행은 minority ÷ NHW로 방향이 고정되고 내부 점검에서 원문 발생률로 재검증됨. 원문 보고값 98행 중 같은 셀에 추정치가 3개 이상 있어 상호 대조가 가능한 행에서 방향 이탈 후보 3건 검출 → Nash 2022는 외부 NHW 기준을 쓴 계산값, Wingo 2008은 원문이 national 0.63·Northern Plains 0.89·Southern Plains 0.89·Alaska 0.99로 모두 minority 기준, Zahnd 2019는 원문 "non-Hispanic Black women had … higher rates than non-Hispanic White women (RR = 1.07; 95% CI 1.04–1.11)"로 확인되어 3건 모두 방향 정확. 셀 내 대조가 불가능한 33행 중 1을 넘는 9행도 NHB 여성의 40세·50세 미만 교차(1.01–1.16), Asian/Hispanic/AI·AN의 HR−/HER2+ 아형(1.04–1.41) 등 알려진 소견과 부합. 방향 반전이 필요한 행은 Kong 2020 overall Black 1건.
