# 3차 피드백 문장별 체크리스트 및 적용 검증

원문: `Advice/Feedback3.md`. 각 항목을 검증 가능한 문장 단위로 분해하고 **현재 원고 상태**로 확인했다.
`[x]` 적용됨 · `[~]` 부분/판단필요 · `[ ]` 미적용. 근거는 파일·데이터로 확인.

---

## 1. "meta-analysis" 규정 재검토
- [x] 제목의 "meta-analysis" 제거 → "A Systematic Review **with Quantitative Synthesis**" (`Abstract_draft.md` 헤더)
- [x] Abstract에 "meta-analysis" 표현 없음
- [x] PRISMA figure(`prisma_flow.py`)에 "meta-analysis" 없음
- [x] 본문에 "meta-analysis" 없음 — 유일 등장은 부정문 "not a meta-analytic pooled estimate"
- [x] 연구설계가 실제 분석과 일치: Methods가 random-effects pooling 미시행을 명시, 셀당 representative estimate 제시

## 2. Representative estimate 선정 기준 명료화
- [x] **analytic cell = racial/ethnic group × analytic dimension**으로 명시 정의 (`Methods_draft.md` §대표선정)
- [x] "one per registry family"와 "one per group×dimension" 혼재 해소: **분석단위=cell, registry-family는 셀 내 우선순위**로 재배치
- [x] 동일 cell 내 우선순위를 재현 가능하게 기술: coverage tier(USCS>NAACCR>SEER-national>state) → 최근·최장 기간 → 표준화 → 직접보고 CI; AI/AN은 IHS-PRCDA 우선
- [x] Supplementary Table 4에 중복표·대표 선정 이유 제시

## 3. RoB ↔ sensitivity 내부 일관성 (교수님 지적: Gopalani 2020)
- [x] Gopalani 2020(rec 500) = **Low RoB** 확인 (`TableS_risk_of_bias.csv`)
- [x] 저위험-only 감도에서 AI/AN overall 대표(rec 500) **status = unchanged** (교수님이 본 "대표 변경"은 제거됨)
- [x] 원인 규명·수정: `sensitivity_analyses.py`의 best()가 finalize의 **IHS-linked override를 미반영**해 허위 'changed' 발생 → override 반영 + drift 가드 추가
- [x] master dataset부터 재검증: crosscheck A–F PASS, 현재 감도 62/40/56 (unchanged), 3/5/1 changed, 13/33/21 dropped

## 4. Study selection 기술 통일
- [x] Methods의 "2인 독립 reviewer + 제3자" 문안 **철회** → 실제(단일 리뷰어+AI)로 재작성
- [x] Figure 1 "single-reviewer screening with AI assistance"와 일치
- [x] PRISMA reporting 일치 (`PRISMA_COUNTS.md`: single-reviewer with AI assistance)
- [x] AI 역할 단계별 투명 기술: T/A 선별=AI(저자가 제외 표본 재검증), **전문 포함판정=저자 직접**, 추출=AI 보조+저자 원문 대조 검증, RoB=저자(단일)+AI

## 5. Eligibility ↔ population 일치 (male BC)
- [x] male breast cancer **제외** — 78 대표 셀에 male-BC 0개, Results/Abstract에 male-breast 언급 0
- [x] eligibility 여성 명시: Methods "invasive breast cancer incidence among women", Abstract "female invasive"

## 6. Comparator 정의 정확화
- [x] Abstract: "versus a non-Hispanic White reference (**unstratified White for a minority of estimates**)"
- [x] Methods: NHW 우선, unstratified White도 일부 포함됨을 명시 (†로 표기)
- [x] Supplementary Table 4 + sensitivity(6c)에서 NHW-comparator만 제한한 분석으로 구분

## 7. 재구성 estimate 방법·main 포함 기준
- [x] **추정/외부 comparator 분모를 쓴 main 대표값 = 0** (검증: 78 대표 provenance에 estimated/external 없음)
- [x] Hispanic-origin(Pinheiro rec 3182): 추정 분모 폐기 → **원문 보고 NHW-Florida rate 140.4 [137.6, 143.2]** 사용
- [x] provenance 3구분 명시: directly-reported(IRR 39 + SIR 1) / same-paper computed-from-rates(28+5+5) / external-estimated(0)
- [x] "외부·추정 comparator estimate를 main 대표로 사용" → 해당 없음(0)이므로 타당성 문제 해소

## 8. Quantitative vs narrative 3분류 명료화
- [x] **43 extractable / 5 eligible-but-non-extractable / 114 narrative-only** 3범주 일관 사용
- [x] "162 = 43 + 5 + 114" 명시 (Results); "48 = 43 + 5" (quant-eligible)
- [x] 모호한 "115 not entered" 표현 해소: 5편(적격·비추출)을 별도 명시, 나머지 114가 narrative
- [~] 총계는 163→**162**, narrative 115→**114**로 갱신됨 (rec 1569 preprint 제외). 교수님 원문의 163/115는 당시 수치.

## 9. AI/AN 해석 ↔ selection rule 일치
- [x] Discussion에서 논리 구분: "unlinked registries misclassify/undercount AI/AN → IHS-linked(**undercount-adjusted**) estimates 사용, unlinked의 더 낮은 값은 배제" (`Discussion_draft.md` L36–38)
- [x] Abstract도 동일: "unlinked registries undercount AI/AN incidence, IHS-linked estimates were used"
- [x] "main estimate가 undercounting 때문에 낮다"는 오독 소지 문장 제거

## 10. 핵심 메시지 단순화 (Discussion 재구성)
- [x] Discussion을 (1)주요 결과 → (2)subgroup heterogeneity → (3)registry/data-quality → (4)synthesis 방법의 의미 → (5)limitations 순으로 재구성
- [x] "aggregate categories conceal heterogeneity" 반복 감소 (문단별 1회 수준)
- [x] registry overlap·representative selection·comparator harmonization·provenance를 방법 기여로 집약

## 11. 시각화 강화
- [x] Figure 2: broad category 대표 + 세부 subgroup 추정치 + **95% CI 함께** (AANHPI forest) — aggregate가 이질성을 가림을 직관 표시
- [x] group × analytic-dimension **heatmap** 존재 (overall/age/subtype/TNBC 교차, NHW=1.0 발산 컬러)
- [x] 별도 main **Table 2 없음** — Table 1만 유지("Supplementary Table 2"만 존재), Fig 2 중복 회피
- [~] **번호 차이**: 교수님 제안은 heatmap=Figure 3이나, 현재 heatmap=**Figure 4**이고 Figure 3은 aggregate/AI-AN/ME overview forest. 핵심 요구(subgroup+CI forest, heatmap, Table 1 유지, Table 2 없음)는 충족. 저자 판단: heatmap을 Figure 3으로 승격하고 overview forest를 재배치할지 선택 가능.

---

## 종합
- **11항목 중 실질 요구는 전부 적용**([x]). `[~]` 2건은 (a) 항목8의 총계 수치가 최신화됨(163→162), (b) 항목11의 heatmap 번호가 3 대신 4 — 둘 다 요구 내용 자체는 충족, 저자 확인용 표시.
- 항목 4·5·7·9는 이번 세션에서 실데이터로 재검증(단일+AI 문안, male-BC 0, 추정분모 0, AI/AN status unchanged).
- 원고 내 관련 카운트(PRISMA·162/48/43/114·78셀·RoB 37/6·대표 26)는 `crosscheck_master.py` E(30개 숫자)가 자동 검증 — 드리프트 시 FAIL.
