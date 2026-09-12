# 논문 초안 수정 의견 (2차 피드백)

거버닝 대전제 (1차 `Advice/Feedback`과 함께 적용). 충돌 시 최신(2차)이 우선.

## 1. GRADE 삭제
GRADE는 삭제하는 방향으로 수정할 것. 본 연구는 race/ethnicity의 causal effect를 평가하는 연구라기보다 미국 내 population-based breast cancer incidence 차이를 기술·비교하는 연구이므로, 현재처럼 observational evidence를 Low에서 시작하고 IRR magnitude에 따라 certainty를 upgrade하는 방식은 연구 질문과 잘 맞지 않음. 특히 큰 IRR만으로 High/Moderate certainty가 되는 구조는 과도한 해석이 될 수 있으므로 Main/Supplementary에서 GRADE 관련 내용은 제거하는 것이 좋겠음.

## 2. Risk of bias 평가도구 재정비 (NOS → JBI)
Risk of bias 평가는 유지하되 방법을 재정비할 것. 현재 adapted NOS는 registry-based descriptive incidence study에는 적절성이 떨어지므로 JBI tool 등 population-based prevalence/incidence study에 적합한 평가도구를 활용하는 방향으로 수정할 것.
또한 "AI-generated first pass" 등의 문구는 삭제할 것. 논문 작성 시에는 최소 2명의 저자가 독립적으로 수행하고, disagreement는 consensus 또는 third reviewer를 통해 해결하는 방식으로 Methods에 기술할 것.

## 3. 포함 논문 수 명확화 (163 / 48 / 43)
포함 논문 수를 명확히 정리할 것. Supplementary Table 2의 163편은 systematic review에 포함된 전체 논문 수이며 모두 meta-analysis에 포함된 것은 아님. 논문 전체에서 163 included studies/publications, 48 quantitative-synthesis eligible, 43 with extractable quantitative data의 의미를 명확하게 구분하고 Abstract, Methods, Results, PRISMA에서 일관되게 표현할 것.

## 4. Study design 재정리 (registry/incidence study)
포함 연구의 study design을 다시 정리할 것. 대부분의 핵심 연구는 전형적인 cohort study라기보다 SEER, USCS, NAACCR, state cancer registry 등을 이용한 population-based registry/incidence study임. Supplementary Table 2에 Study design 열을 추가하여 population-based registry/incidence study, cohort 등으로 구분하고, Methods에서 포함 연구를 단순히 cohort studies라고 통칭하지 말 것.

## 5. Overlapping registry pooling을 primary analysis에서 제외
현재의 overlapping registry pooling은 primary analysis로 사용하지 않는 방향을 검토할 것. SEER, NPCR, USCS, NAACCR 및 여러 state registries는 underlying population이 상당 부분 중복될 수 있으므로 서로 다른 논문 또는 database라는 이유만으로 independent studies처럼 random-effects pooling하면 중복 문제가 발생함. 특히 동일하거나 nested된 registry population을 이용한 estimate를 함께 pooling하여 pooled IRR, I², confidence interval을 제시하는 것은 해석상 문제가 있으므로, 이러한 분석은 삭제하거나 보조적인 consistency/sensitivity analysis로 제한할 것.

## 6. Representative study approach — benchmark로 제시 (pool 아님)
Representative study approach는 일부 Main Figure에서는 유지 가능함. 다만 이를 meta-analytic pooled estimate처럼 표현하면 안 됨. 각 racial/ethnic group에서 가장 최근이고 coverage가 넓으며 population definition과 standardization이 적절한 registry estimate를 "representative population-based estimate" 또는 "contemporary benchmark estimate"로 제시하는 방향이 좋겠음. Representative estimate의 선정 기준을 Methods에서 명확히 정의하고, Main Figure에서는 현재의 racial/ethnic disparity와 aggregate category 내부의 subgroup heterogeneity를 보여주는 데 초점을 둘 것.

## 7. Derived IRR 전수 검증 + 단일 master dataset
Derived IRR와 전체 dataset의 정합성을 반드시 전수 검증할 것. 상당수 IRR/CI가 원 논문에서 직접 보고된 값이 아니라 저자 계산값이므로 계산식, denominator, standardization, CI 산출방법을 다시 확인할 것. 현재 Supplement 내부에도 main estimate와 sensitivity table 값이 일치하지 않는 부분이 있으므로 하나의 master extraction dataset을 기준으로 Main/Supplementary Tables와 Figures를 다시 생성하거나 전수 cross-check할 것.
