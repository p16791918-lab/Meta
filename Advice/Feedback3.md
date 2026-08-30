# 논문 초안 수정 의견 (3차 피드백)

거버닝 대전제 (1차 `Advice/Feedback`, 2차 `Advice/Feedback2.md`와 함께 적용). 충돌 시 최신(3차)이 우선. 원문은 채팅으로 전달됨(2026, 세션 중)을 아래에 그대로 보존.

## 1. meta-analysis 규정 재검토
본 연구를 "meta-analysis"로 규정하는 것이 적절한지 재검토가 필요합니다. 현재 분석에서는 registry 간 자료 중복과 비독립성을 이유로 effect size들을 통계적으로 pooling하지 않고, 각 analytic cell에서 하나의 representative estimate를 선택하여 제시하고 있습니다. 실제 Methods에서도 random-effects pooling을 시행하지 않았음을 명확히 기술하고 있습니다. 따라서 현재 연구는 전통적인 의미의 meta-analysis라기보다는 systematic review with quantitative synthesis에 더 가깝습니다. 논문 제목, Abstract, PRISMA figure 및 본문의 "meta-analysis"라는 용어를 전반적으로 재검토하고, 연구 설계를 실제 분석 방법과 일치시키는 것이 필요합니다.

## 2. Representative estimate 선정 기준 명료화
Representative estimate 선정 기준을 보다 명확하고 일관되게 정립할 필요가 있습니다. 본 연구의 핵심 방법론은 overlapping registry data를 직접 pooling하지 않고 하나의 대표값을 선택하는 것입니다. 그러나 현재 manuscript에서는 "one representative estimate per registry family"와 "one representative estimate per racial/ethnic group × analytic dimension"이 혼재되어 있어 실제 selection unit이 명확하지 않습니다. 각 결과를 구성하는 analytic cell을 명시적으로 정의하고, 동일 cell 내 여러 registry/publication이 존재할 경우 어떤 우선순위로 하나를 선택했는지 재현 가능한 수준으로 정리할 필요가 있습니다. 이 부분은 본 연구의 가장 중요한 methodological contribution이므로 보다 명료해야 합니다.

## 3. RoB와 sensitivity analysis 내부 일관성
Risk-of-bias assessment와 sensitivity analysis 간 내부 일관성을 다시 확인해야 합니다. Supplementary Table 5에서는 일부 연구가 low risk of bias로 분류되어 있으나, low-risk-only sensitivity analysis에서 해당 연구의 representative estimate가 제외되거나 다른 연구로 대체되는 경우가 확인됩니다. 예를 들어 Gopalani 2020은 Supplementary Table 5에서 low risk로 평가되어 있으나, low-risk-only analysis에서는 overall AI/AN representative가 변경됩니다. 따라서 RoB classification, sensitivity-analysis filtering rule, 또는 분석 코드 중 어느 부분에서 불일치가 발생했는지 master dataset부터 다시 검증할 필요가 있습니다. 이 문제는 결과의 신뢰성과 직접 연결되므로 반드시 수정되어야 합니다.

## 4. Study selection 기술 통일 (실제 수행 방법과 일치)
Study selection 과정에 대한 기술이 서로 상충하므로 실제 수행 방법에 맞게 통일해야 합니다. Methods에서는 title/abstract 및 full-text screening을 두 명의 reviewer가 독립적으로 수행했다고 기술하고 있습니다. 반면 Figure 1에는 "single-reviewer screening with AI assistance"라는 설명이 포함되어 있습니다. 두 방식은 방법론적으로 상당히 다르므로 동시에 성립하기 어렵습니다. 실제 screening이 어떤 방식으로 이루어졌는지 확인한 후 Methods, Figure 1, PRISMA reporting을 모두 일치시켜야 합니다. 특히 AI-assisted screening을 시행한 경우에는 AI가 어느 단계에서 어떤 역할을 했는지도 투명하게 기술할 필요가 있습니다.

## 5. Eligibility criteria와 포함 population 일치 (male BC)
연구의 eligibility criteria와 실제 포함된 population이 일치하도록 범위를 재정의해야 합니다. Eligibility criteria에서는 U.S. women의 invasive breast cancer incidence를 대상으로 명시하고 있으나, 결과와 Table 1에는 male breast cancer가 포함되어 있습니다. 여성 breast cancer가 연구의 주요 대상이라면 male breast cancer 분석은 제외하는 것이 가장 일관됩니다. 반대로 남성까지 포함하고자 한다면 objective, population definition, eligibility criteria 및 Abstract 전반을 이에 맞게 수정해야 합니다. 현재 상태에서는 연구 대상 정의가 불명확합니다.

## 6. Comparator 정의 정확화 (NHW vs unstratified White)
Comparator의 정의를 보다 정확하게 정리해야 합니다. 논문은 전체 결과를 NHW women 대비 IRR로 제시하는 것으로 설명하고 있으나, 실제 일부 연구에서는 comparator가 non-Hispanic White가 아니라 Hispanic origin으로 stratification되지 않은 White population입니다. 저자들도 이를 Supplementary Table 및 sensitivity analysis에서 구분하고 있습니다. 따라서 Abstract와 Methods에서 모든 estimate가 NHW comparator에 기반한다고 단정하기보다는, NHW를 우선 comparator로 사용하되 unstratified White comparator도 일부 포함되었음을 명확하게 설명하는 것이 필요합니다.

## 7. 재구성 estimate의 방법·main 포함 기준 엄격화
직접 보고되지 않은 effect estimate의 재구성 방법과 main analysis 포함 기준을 더 엄격하게 검토할 필요가 있습니다. 본 연구에서는 일부 IRR을 원 논문에서 직접 추출하지 않고, 보고된 incidence rate 또는 외부/추정 comparator를 이용해 계산했습니다. 특히 일부 Hispanic-origin estimates에서는 원문에 제시되지 않은 NHW reference rate를 저자의 rounded ratio와 일치하도록 추정하여 denominator로 사용한 것으로 기술되어 있습니다. 이러한 방식은 재현성과 불확실성 측면에서 reviewer의 주요 지적 대상이 될 수 있습니다. 직접 보고된 estimate, 동일 논문 내 자료로 계산된 estimate, 외부 또는 추정 comparator를 사용한 estimate를 명확히 구분하고, 후자의 경우 main analysis의 대표값으로 사용하는 것이 타당한지 다시 검토할 필요가 있습니다.

## 8. Quantitative vs narrative synthesis 분류 명료화
Quantitative synthesis와 narrative synthesis의 study classification을 명료하게 정리해야 합니다. 현재 총 163편 중 48편이 quantitative synthesis에 eligible하였고, 이 중 실제 extractable data가 있는 연구는 43편이며, 5편은 quantitative eligibility는 충족하지만 extractable data가 없었던 것으로 설명되어 있습니다. 나머지 115편은 narrative synthesis only입니다. 그러나 main text에서는 "115 studies not entered into the quantitative synthesis"와 같은 표현을 사용하고 있어, 실제로 quantitative analysis에 들어가지 않은 5편의 위치가 다소 모호합니다. 43 extractable quantitative studies, 5 quantitatively eligible but non-extractable studies, 115 narrative-only studies의 세 범주를 일관되게 사용하면 연구 흐름이 훨씬 명확해질 것입니다.

## 9. AI/AN 해석과 selection rule 일치
AI/AN 결과에 대한 해석은 main-analysis selection rule과 일치하도록 보다 신중하게 수정할 필요가 있습니다. 저자들은 unlinked national registry에서 AI/AN race misclassification 및 undercounting이 발생할 수 있기 때문에 IHS-linked estimates를 우선적으로 선택했다고 설명합니다. 그럼에도 Abstract와 Discussion에서는 aggregate AI/AN estimate 자체가 registry undercounting의 영향을 받은 것처럼 읽힐 수 있는 문장이 있습니다. 실제 main analysis에서는 undercounting을 줄이기 위해 IHS-linked data를 선택한 것이므로, "main estimate가 undercounting 때문에 낮다"는 해석과 "unlinked registry estimate는 undercounting 우려가 있어 배제하였다"는 논리를 구분해야 합니다.

## 10. 핵심 메시지 단순화 (Discussion 재구성)
논문의 핵심 메시지를 보다 단순화할 필요가 있습니다. 현재 Discussion에서는 aggregate racial/ethnic categories가 subgroup heterogeneity를 가릴 수 있다는 메시지가 여러 차례 반복됩니다. 반면 이 논문의 더 독창적인 부분인 registry overlap 처리, representative estimate selection, comparator harmonization, estimate provenance 문제는 상대적으로 분산되어 있습니다. Discussion을 재구성하여 (1) 주요 결과, (2) subgroup heterogeneity, (3) registry/data-quality issues, (4) 본 synthesis 방법의 의미, (5) limitations 순으로 정리하면 논문의 기여점이 훨씬 명확해질 것입니다.

## 11. 시각화 강화 (pooled 대신 synthesis 시각화)
본 연구는 전통적인 의미의 메타분석보다는 systematic review with quantitative synthesis의 성격이 강하므로, pooled effect를 제시하는 방식보다는 synthesis의 결과를 여러 형태로 시각화하여 연구의 강점을 부각하는 것이 좋겠습니다. 예를 들어 Figure 2에서는 broad racial/ethnic category의 대표 추정치와 세부 subgroup별 추정치 및 95% 신뢰구간을 함께 제시하여 aggregate category가 내부의 큰 이질성을 가릴 수 있음을 직관적으로 보여줄 수 있습니다. 또한 Figure 3에서는 racial/ethnic group과 analytic dimension(overall incidence, age group, receptor-defined subtype, TNBC 등)을 교차한 heatmap을 제시하여 동일한 집단에서도 분석 차원에 따라 상대적 incidence pattern이 달라질 수 있음을 보여주면 본 연구의 novelty가 더욱 분명해질 것으로 생각됩니다. 반면 별도의 Table 2에서 aggregate와 subgroup range를 다시 요약하는 것은 Figure 2와 내용이 상당 부분 중복될 수 있으므로, 현재의 Table 1을 주요 수치 확인용 표로 유지하고 Figure 2와 Figure 3을 중심으로 결과의 시각적 synthesis를 강화하는 방향이 더 효율적일 것으로 보입니다.

---

## 항목 11 예시 그림 (교수님 첨부)
- `Advice/Feedback3_ExampleFig2_forest.png` — "Aggregate-to-disaggregated heterogeneity with 95% CI": AANHPI·Hispanic/Latina·AI/AN을 **한 forest에** 각 aggregate diamond + subgroup + 95% CI로 제시.
- `Advice/Feedback3_ExampleFig3_heatmap.png` — "Incidence heterogeneity across groups and analytic dimensions": group(행) × analytic dimension(열: Overall, Age <50, HR−, HR+, HR+/HER2−, HR+/HER2+, TNBC) heatmap. Blank = 대표값 없음.

두 그림은 illustrative template(값은 예시). 현재 원고의 Figure 2(AANHPI forest)·Figure 3(overview forest)·Figure 4(heatmap)와의 정합은 `outputs/Feedback3_checklist.md` 항목 11 참조.
