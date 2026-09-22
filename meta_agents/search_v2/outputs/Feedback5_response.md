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

## 5. 연구의 포함·제외 및 synthesis 분류 기준을 통일해주세요.

- **중복 제외 vs 서술적 종합 잔류 — 구분 원리를 Methods에 명시**: 종전 Methods는 "같은 registry·기간·인구의 재보고는 제외"만 기술해, 같은 사유가 적힌 연구가 narrative로 남아 있는 것과 어긋났음. 실제 판정 기준은 **"이미 포함된 다른 출판물이 그 내용을 담고 있는가"**였으므로 이를 원리로 명시하고 두 경우를 구분해 서술: ① 재보고는 독립 추정치가 아니어서 **어느 경우에도 대표값 후보가 되지 않음**; ② 그중 포함된 다른 출판물이 내용을 이미 담은 것(같은 시리즈의 **이전 연도판**, 포함된 분석의 **preprint·book-chapter판**)은 리뷰에 새 정보를 더하지 않으므로 **제외**(중복 55편 중 51편이 연례 통계 시리즈 이전판, 4편이 preprint·book-chapter 중복); ③ 반면 **시리즈의 최신 적격판**은 그 시리즈의 현재 서술을 담은 유일한 판이므로 리뷰에는 포함하되, 해당 registry·기간의 발생률은 전담 primary 연구가 이미 제공하므로 **서술적 종합에만 기여**; ④ 같은 registry family라도 기간·지역·subset이 다르면 별개 추정치로 보아 **민감도 overlap으로 유지**. 이로써 Giaquinto 2024(rec 0)와 Saka 2025(rec 4294)가 narrative에 남는 근거와, 같은 시리즈 이전판들이 제외된 근거가 하나의 기준으로 설명됨. 참고로 제외된 83편 중 51편이 연례 통계 시리즈의 **이전 연도판**(Breast cancer statistics 2015·2019, Cancer statistics for African Americans 2016·2022, Annual Report to the Nation 1973–1999 ~ 1975–2014 등)임을 확인. 즉 실제로는 "**시리즈별로 최신 적격판 1편만 남기고 이전 판은 중복으로 제외**"하는 규칙이 적용되고 있었으나 Methods에 서술되지 않아 지적된 불일치가 발생. Methods 적격기준에 해당 규칙과, **남긴 최신판은 해당 registry·기간의 발생률을 전담 primary 연구가 이미 제공하므로 대표값 후보로 쓰지 않고 서술적 종합에만 기여**한다는 점을 명시. 이로써 Giaquinto 2024(rec 0, Breast cancer statistics 2024)와 Saka 2025(rec 4294, Cancer statistics for African American and Black people 2025)가 같은 사유로 narrative에 남는 근거가 드러남.

- **Li 2025 분류 사유 수정**: 해당 연구는 rec 46(JAMA Netw Open 2025, SEER 22개 레지스트리 2010–2019, joinpoint 연간변화율 분석)으로 확인. 종전 표기 "single poolable estimate가 아님"은 pooling을 하지 않는 현재 분석 방식과 맞지 않으므로, 실제 사유인 **"연간 추세(annual percentage change)로만 보고해 단면 연령표준화율·비율을 추출할 수 없음"**으로 교체.

- **Supplementary Table 2의 narrative 사유 전면 실제화**: 점검 결과 narrative 118편 중 **103편이 "No recoverable NHW comparison" 한 문구로 일괄 표시**되고 있었음(개별 사유 부여는 15편). 실제 사유는 시리즈 재보고 9, 추세만 28, 사회경제적 비교 6, 비미국 비교군 5, 비율 아님(PIR 등) 5, 그림 전용 4 등으로 다양하므로, 적격성 기록에 사유가 있는 경우 그 사유를 유형별 문구로 표시하도록 수정 → **개별 사유 표시가 15편에서 57편으로 확대**. 사유 기록이 없는 나머지는 포괄 사유("NHW 기준 연령표준화율·비율을 복구할 수 없음")로 표시하고, 어떤 경우에 개별 사유가 표시되고 어떤 경우에 포괄 사유가 표시되는지를 Supplementary Table 2 Note에 명시.

- **대표값 선정 단위 표기 통일**: Introduction("one representative population-based estimate per registry family"), Table 1 Note("one per registry family"), 본문 표·그림 Note에 남아 있던 **"per registry family"를 Methods의 "per analytic cell"로 통일**. registry family는 셀 내부의 중복 판정 단위로만 쓰인다는 점을 작성 지침에도 반영.
