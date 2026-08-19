# 리뷰어 예상질문 및 대응 (rebuttal 준비용)

*Racial and Ethnic Differences in Breast Cancer Incidence in the United States: A Systematic Review and Meta-analysis*

이 논문의 실제 설계·선택에 근거한 예상 질문과 답변. 각 답 끝의 (→ …)는 원고 내 근거 위치.

---

## A. 프레이밍·제목

### Q1. 제목은 "Meta-analysis"인데 실제로는 pooling(random-effects)을 하지 않았다. 메타분석이라 부를 수 있나?
A. 타당한 지적이다. 본 연구는 중복·nested registry 인구에서 나온 추정치를 독립연구처럼 pooling하는 것이 부적절하다고 판단해, 각 집단에서 대표 population-based estimate를 선정하는 정량합성을 수행했다. 이는 pooled summary가 아니므로, 제목을 **"A Systematic Review"** 또는 **"A Systematic Review with Quantitative Synthesis"**로 조정하는 것이 정확하다. (→ Methods §Statistical analysis; 저자 확정 필요 사항)

## B. 핵심 방법 — 왜 pooling을 안 했나

### Q2. 왜 메타분석 pooling 대신 대표추정치를 썼나?
A. SEER·NPCR/USCS·NAACCR·주별 등록부는 대상 인구가 상당 부분 중첩·포함관계(county⊂state⊂SEER⊂NAACCR⊂USCS)에 있어 서로 다른 논문이라도 같은 사례를 반복 계수한다. 이런 비독립 추정치를 pooling하면 특정 인구가 중복 반영되고 I²가 인위적으로 부풀려진다. 따라서 registry family당 대표 추정치 1편을 주분석으로 두었다. (→ Methods §Selection, §Statistical analysis)

### Q3. 대표추정치 선정은 주관적이지 않나?
A. 선정 기준을 사전 정의했다: 가장 넓은 coverage(USCS>NAACCR>SEER-national>주/지역), 가장 최근·긴 진단기간, 명확한 연령표준화, 직접 보고된 CI. AI/AN은 미연계 등록부의 인종 오분류·과소집계 때문에 IHS 연계 추정치를 우선했다. 선정의 안정성은 세 가지 sensitivity(저-RoB만, 직접보고값만, NHW-비교군만)로 확인했다. (→ Methods §Selection; Supplementary Table 6)

### Q4. 이중 계수를 어떻게 방지했나?
A. 모든 추정치를 registry family에 배정하고, outcome×집단×family 셀마다 1편만 대표로 남겼다. 각 연구의 registry·지역·기간·연령·집단·outcome을 표로 정리해 중복을 가시화했다. (→ Methods §Selection; Supplementary Table 4)

## C. 비교군·범위

### Q5. 왜 미국 연구로 제한했나? 일반화 가능성은?
A. 비교군인 non-Hispanic White는 미국 인구총조사 구성개념이다. 타국 연구는 다른 백인 기준(예: White British), 다른 인종·민족 분류, 다른 표준인구를 써서 rate ratio가 미국 추정치와 commensurable하지 않다. 따라서 미국 제한은 자의적 축소가 아니라 비교가능성(commensurability) 확보를 위한 실질적 기준이다. 다만 결과는 타국 인구에 일반화되지 않는다는 점을 한계로 명시했다. (→ Methods §Eligibility; Discussion 한계)

### Q6. NHW와 unstratified White 비교군이 섞여 있다(† 표시). IRR을 편향시키지 않나?
A. 대다수 셀은 NHW 비교군이며, unstratified White를 쓴 소수 셀(수용체 아형, 남성 유방암)은 †로 표시했다. unstratified White는 히스패닉을 포함하므로 IRR을 약간 높일 수 있다. NHW-비교군 sensitivity(Supplementary Table 6c)에서 대표값의 안정성을 확인했고, 해당 셀만 영향을 받았다. (→ Results §RoB and sensitivity; Methods §Eligibility)

## D. 데이터 정합성

### Q7. 상당수 IRR이 저자 계산값이다. 신뢰할 수 있나?
A. 모든 추정치를 provenance(직접보고 IRR/SIR, 발생률로 계산, 그림 추출)로 라벨링했다. 계산값은 하나의 master extraction dataset에서 자기 원율로 재계산하고, CI는 성분율 구간에서 델타법(또는 고정분모의 경우 소수율 구간 스케일링)으로 재현했다. 전 표시값이 원장으로 추적됨을 전수 cross-check했다. 직접보고값만으로 제한한 sensitivity도 제시했다. (→ Methods §Statistical analysis; Supplementary Table 6b)

### Q8. 연구마다 표준인구·진단기간이 다르다. 비교 가능한가?
A. 대표 선정에서 2000 US 표준인구와 최근·긴 기간을 우선했고, 예외(예: 1970 world standard를 쓴 오래된 1편)는 명시했다. 표준인구·기간 차이는 직접 비교를 제한하는 한계로 기술했다. (→ Discussion 한계)

### Q8b. 흑인 수용체-아형 두 셀(HR+/HER2−, HR−/HER2+)의 대표는 2000 US가 아닌 Segi world 표준을 쓴다. 왜 그 estimate를 골랐나?
A. 이 두 셀에서는 NHW 비교군과 2000 US 표준을 동시에 만족하는 연구가 없었다. 대표로 쓴 Davis Lynn 2025는 NHW 비교군을 갖지만 Segi world 표준이고, 대안인 Gleason 2012는 2000 US 표준이지만 unstratified White 비교군이다. 발생률비는 각 연구 안에서 형성돼 표준인구가 대체로 상쇄되지만 비교군 차이는 참조집단 자체를 바꾸므로, **비교군(NHW)을 우선**했다. 비-2000 표준은 Supplementary Table 4의 "Std pop" 열에 표시했다. (→ Supplementary Table 4)

## E. 평가·확실성

### Q9. 왜 GRADE로 근거 확실성을 평가하지 않았나?
A. 본 연구는 race/ethnicity의 causal effect 추정이 아니라 population-based incidence를 기술·비교한다. 관찰근거를 Low에서 시작해 IRR 크기로 upgrade하는 GRADE 구조는 연구질문과 맞지 않고, 큰 IRR만으로 높은 확실성을 부여하면 과잉해석이 된다. 따라서 확실성 등급은 매기지 않았다. (→ Methods §Risk of bias)

### Q10. 위험비뚤림 도구로 왜 JBI를 골랐나?
A. adapted Newcastle-Ottawa는 노출-결과 비교연구용으로 registry 기반 기술적 발생률 연구에 적합성이 떨어진다. JBI prevalence/incidence 체크리스트는 표본틀·사례확인·커버리지·표준화 등 기술연구 특성을 평가하도록 설계돼 본 연구에 더 적합하다. 43편 중 37 Low/6 Moderate였다. (→ Methods §Risk of bias; Supplementary Table 5)

### Q11. 출판편향은 평가했나?
A. 주분석은 독립연구를 pooling하지 않으므로 funnel plot/Egger 같은 소규모연구 비대칭 검정은 적용·해석이 어렵다. 또한 population-based registry 발생률은 사례확인이 거의 완전해 선택적 출판의 영향을 덜 받는다. 이 때문에 형식적 출판편향 검정은 수행하지 않았다. (→ 필요 시 rebuttal 문장으로 사용; 현재 본문에는 미기재)

## F. 합성 범위

### Q12. narrative synthesis가 얇다(115편을 주제·방향만 요약).
A. 이 115편은 포함기준은 충족했으나 NHW 대비 IRR(또는 재계산 가능한 표준화율)을 복원할 수 없었다. 비교군·표준인구·보고형식이 제각각이라 공통 IRR 척도에 올릴 수 없었고, 대신 주제(세부집단·연령·추세·지역/SES·아형·병기)와 방향적 일치를 서술했다. 전 목록은 식별자(PMID/DOI)와 함께 Supplementary Table 2에 있다. (→ Results §Narrative synthesis; Supplementary Table 2)

### Q13. 남성 유방암은 추정치 1개뿐이다.
A. 남성 유방암은 드물고 NHW 대비 IRR을 보고한 미국 population-based 연구가 제한적이어서 대표 추정치 1개(흑인 남성 1.52)만 제시했다. 이는 완전한 synthesis가 아니라 참고 수치로 제한 해석해야 한다. (→ Results §Male breast cancer)

## G. 절차·등록

### Q14. 스크리닝·RoB는 실제로 2인 독립으로 수행됐나? PROSPERO 등록은?
A. Methods는 스크리닝과 RoB를 2인 독립 + consensus/third reviewer로 수행했다고 기술한다. 제출 전 실제 이중검토 기록(불일치·합의)을 확보해야 한다. PROSPERO 등록은 진행 예정이며 등록번호를 Methods에 삽입할 것이다. (→ 저자 확정 필요 사항)

### Q15. 2025·2026년 문헌이 있다(예: Gomez 2026, Davis Lynn 2025).
A. 이는 SEER-21 등 가장 최근 등록부 업데이트로, 최신 현황을 반영한 정당한 인용이다. (→ References 15, 26)

---

## 최우선 대비 3가지
- 제목의 "Meta-analysis" 처리 (Q1) — 사전에 조정 여부 결정.
- 2인 reviewer 실제 수행 기록 + PROSPERO 등록 (Q14) — 저자 조치.
- 출판편향 질문 대비 문장 준비 (Q11) — 본문에서 뺐으므로 rebuttal용으로 보관.
