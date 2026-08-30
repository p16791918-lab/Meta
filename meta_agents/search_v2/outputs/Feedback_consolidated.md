# 지도교수 피드백 합본 (1차 + 2차) 및 반영 현황

*Racial and Ethnic Differences in Breast Cancer Incidence in the United States: A Systematic Review with Quantitative Synthesis*

원문 출처: `Advice/Feedback`(1차), `Advice/Feedback2.md`(2차). 충돌 시 2차가 우선. 각 항목 아래 **반영**은 현재 원고·산출물 기준 처리 결과입니다.

---

## 1차 피드백

### 1. 전체적인 문장 수정
1인칭 단수(I searched/tested/…)를 We 또는 객관적 수동태로. 수사적·공격적 표현(misleading, the reassuring picture dissolves, quantitative indictment 등) 및 절대적 표현(every, all, no single study 등) 자제. 동일 결론이 Abstract/Results/Discussion에서 반복되고 문장이 매끄럽고 방어적이라 AI 인상이 강함 → 참고 논문을 직접 읽고 요약해 전체를 다시 작성.

**반영.** 5개 섹션을 소스 기반으로 재작성. 1인칭 단수 0건, 수사·절대·AI-클리셰 0건(자동 검수), 결론 반복 제거. 구체 수치·명명 연구로 서술.

### 2. 문헌검색
PubMed/MEDLINE, Embase, Scopus, Web of Science Core Collection 포함(스크리닝은 Embase 단독 가능하나 multiple database 결과는 제시). `PubMed/MEDLINE` 또는 `MEDLINE via PubMed`로 표기. 전체 검색식은 본문 제외·Supplementary Table에 DB별 검색식·플랫폼·검색일·건수 제시. 검색일 최신화, PROSPERO 재등록. 인종·민족 검색어를 제목에 한정하지 말고 title/abstract 포함.

**반영.** 4개 DB 검색(2026-08-07), `MEDLINE via PubMed` 표기, 검색식·플랫폼·건수는 Supplementary Table 1, title/abstract 검색. **PROSPERO 등록은 저자 조치 필요**(placeholder + 체크리스트).

### 3. PRISMA flowchart
예시 논문과 PRISMA 2020 형식으로 재작성.

**반영.** PRISMA 2020 흐름도(Figure 1): 9,099 → 중복 4,306 → 4,793 스크리닝 → 242 확보시도 → 9 미확보(not retrieved) → 233 평가 → 71 제외 → 162 포함. (미확보 9건을 PRISMA 논리대로 'not retrieved' 칸으로 분리; estimates 143·대표공급 26편으로 정정.)

### 4. Risk of bias
예시 논문의 평가도구·항목·그림 형식 참고해 재정리(가능하면 AI로 하고 일부만 확인).

**반영.** 2차 피드백에 따라 JBI 도구로 교체(아래 2차 #2 참조).

### 5. 중복 registry 자료의 처리
SEER/NAACCR/USCS/주별 등록부는 지역·기간 중복 → 독립연구처럼 합산 금지. 각 연구의 registry·지역·기간·연령·집단·outcome을 표로 정리해 중복 확인. 동일 질문에서 중복 시 가장 포괄적·큰 표본·최근/긴 기간·명확한 연령표준화·직접보고 CI를 가진 1편을 대표로. 주분석은 one estimate per registry family, 전체포함·중복제외 분석을 sensitivity로 비교. Supplementary에 중복 가능성·주분석 포함 여부·대표 선정 이유 제시.

**반영.** one representative per registry family를 주분석으로. 중복표(Supplementary Table 4)·대표 선정 이유·sensitivity(Supplementary Table 6). AI/AN은 IHS 연계 우선 규칙 명시.

### 6. 통계분석과 결과 해석
I²=99–100%를 "약점/noise 아님"이라 단정 금지(해석 제한 먼저 제시). DL 사용 시 REML/Hartung-Knapp 비교 없이 영향 없다 단정 금지. 직접보고 IRR/발생률 계산 IRR/그림 추출/근사 SE 구분. 동일 표준인구·기간·비교군 확인 후 발생률비 계산. 연령표준화 자체를 artefact로 표현 금지. 인종차이를 유전·생물학 기전으로 직접 연결 금지(가설로 제한).

**반영.** 2차 피드백에 따라 pooling을 주분석에서 제거(I²/DL 논쟁 자체가 비해당). provenance 4종 Methods 명시, IRR 계산 전 표준인구·기간·비교군 확인(전수 교차검증). age-standardization artefact 표현 없음, 유전·생물학 연결은 부정문으로만.

### 7. 본문 구성
제목은 결과 단정형 대신 간결하게(현재 제목 채택). Intro는 배경·기존연구 한계·목적 중심 간결하게. Methods는 실제 수행만(장문 방어 금지). Results는 객관 수치 중심. Discussion은 주요결과→기존연구 비교→가능한 설명→임상·공중보건 의미→강점·제한점→결론 순. "aggregate categories conceal disparities" 반복 금지(문단별 1회). Black/NHB, White/NHW, API/세부집단 용어를 원 논문 정의대로 통일.

**반영.** 제목 채택. Intro/Methods/Results/Discussion을 지정 순서로 구성, Abstract 포함 5섹션. 용어 통일(NHW/NHB/AANHPI/NHPI/AI/AN/TNBC), 반복 제거.

---

## 2차 피드백 (2차가 1차에 우선)

### 1. GRADE 삭제
race/ethnicity의 causal effect가 아니라 population-based incidence를 기술·비교하는 연구이므로 GRADE(관찰근거 Low 시작→IRR 크기로 upgrade)는 부적합. Main/Supplementary에서 제거.

**반영.** GRADE 완전 삭제(Table 1 GRADE 열, Supplementary certainty 표 제거). Methods는 "certainty was not graded" 근거만 서술.

### 2. Risk of bias 도구 재정비(NOS → JBI)
adapted NOS는 registry 기반 기술연구에 부적절 → JBI 등 prevalence/incidence용 도구로. "AI-generated first pass" 문구 삭제. 최소 2인 독립 수행 + consensus/third reviewer로 Methods 기술.

**반영(수정됨).** JBI 9문항 적용(37 Low/6 Moderate/0 High). "AI-generated first pass" 0건. 리뷰어 문안은 **3차 피드백 #4에 따라 실제 프로세스대로 재작성**: 제목·초록은 AI가 선별(저자가 제외 표본 재검증), **전문 포함판정은 저자가 직접 수행**, 추출값은 저자가 원문 대조 검증, RoB는 저자(단일)+AI. 2차의 "2인 독립+제3자" 문안은 실제와 달라 철회하고 **단일 리뷰어+AI를 한계로 명시**(Methods·Discussion). ⚠️ 이 항목만 2차 문안과 의도적으로 다름 — 제2 독립 리뷰어를 실제 투입하면 문구·일치율 갱신 필요.

### 3. 포함 논문 수 명확화 (163 / 48 / 43)
163 included / 48 quantitative-synthesis eligible / 43 with extractable data의 의미를 구분하고 Abstract/Methods/Results/PRISMA에서 일관되게.

**반영.** 162 = 48(그중 43 추출) + 114 narrative를 Abstract·Methods·Results에 일관 명시(rec 1569 preprint 제외로 163→162; crosscheck E가 27개 카운트 자동 검증). 실제 narrative synthesis 소절 추가. Supplementary Table 2를 synthesis 종류별로 그룹핑.

### 4. Study design 재정리
핵심 연구는 cohort가 아니라 SEER/USCS/NAACCR/주별 등록부 기반 population-based registry/incidence study. Supplementary Table 2에 Study design 열 추가, Methods에서 cohort 통칭 금지.

**반영.** Study design 열 추가(158 registry/incidence, 4 cohort; 계 162). Methods는 "registry or incidence studies … rather than cohort"로 기술.

### 5. Overlapping registry pooling을 primary에서 제외
중복 인구를 독립연구처럼 random-effects pooling해 pooled IRR/I²/CI를 제시하는 것은 해석상 문제 → 삭제하거나 보조 sensitivity로 제한.

**반영.** pooled IRR/I²/τ²/HKSJ를 Main·Supplementary에서 완전 삭제. 주분석은 registry family당 대표추정치.

### 6. Representative study — benchmark로 제시(pool 아님)
가장 최근·넓은 coverage·적절한 population definition/standardization을 가진 registry estimate를 "representative population-based estimate/contemporary benchmark"로 제시. 선정 기준을 Methods에 명확히. Main Figure는 disparity와 aggregate 내부 subgroup heterogeneity에 초점.

**반영.** 캡션·본문을 "representative population-based (contemporary benchmark) estimate … not a meta-analytic pooled estimate"로. 선정 기준을 Methods 전용 절에 명시(coverage tier·기간·표준화·직접 CI, AI/AN은 IHS 연계 우선). Figure는 대표값(사각 마커, pooled diamond 아님)으로 disparity·subgroup heterogeneity 표시.

### 7. Derived IRR 전수 검증 + 단일 master dataset
저자 계산 IRR/CI의 계산식·denominator·standardization·CI 산출법 재확인. main과 sensitivity 불일치 존재 → 단일 master extraction dataset 기준으로 Main/Supplementary·Figures 재생성 또는 전수 cross-check.

**반영.** `crosscheck_master.py`로 4단계 전수 검증(파생 IRR 78·CI 37 재계산, Table 1·forest·sensitivity 추적) — 전부 PASS. 검증이 실제 원장 오류 2건(rec 234 TNBC 분모, rec 3182 근사분모)을 발견해 원문에서 수정. 모든 표·그림을 단일 원장(`breast_extraction.csv`)에서 재생성.

---

## 저자 조치 필요(원고 외)
- PROSPERO 재등록 → Methods placeholder 채우기
- 리뷰어 프로세스: 현재 단일 리뷰어+AI로 정직히 기술(3차 #4). 제2 독립 리뷰어 실제 투입은 선택 — 투입 시 Methods 문구와 일치율(agreement) 보고
- 최종 타깃 저널 스타일로 참조 서지 형식 조정(현재 47편 Vancouver 완성)
