# 유방암 인종격차 메타분석 — 프로젝트 계획서

> 새 대화에서 이 파일을 읽고 시작. Branch: `claude/usage-question-q3vm84`
> (스킨암 버전 인계는 `PROJECT_STATUS.md` 참고 — 도구·파이프라인 구조는 재사용)

## 확정된 결정
1. **아웃컴 = Incidence(발생률)만.** Prevalence는 생존율과 뒤섞여 해석 불가하므로
   incidence와 **절대 pool하지 않음**(별도로만 다룸). 사실상 발생률 메타분석.
2. **분석 = 방식 A (연구 내 IRR)** 주 분석. 데이터가 너무 부족하면 방식 B
   (인종별 rate pooling, 단일인종 연구 포함)를 **보조**로 추가.
3. **선별기준** = 아래(1·2에서 도출). 사용자 검토·승인 대상.
4. **경로 = 하이브리드** — orchestrator로 검색·스크리닝 → Claude가 논문 읽고 발생률을
   `run_meta_analysis.py` 형식(log_irr, se, minority_rate, nhw_rate)으로 추출 → 통계 스크립트 실행.

## PICO
- **P**: 일반 인구 여성, 인종·민족군 (NH White, Black/AA, Hispanic/Latina, Asian/PI, AIAN)
- **E(노출)**: 소수 인종·민족
- **C**: Non-Hispanic White
- **O**: 침습성 유방암 **발생률**(age-adjusted incidence rate, per 100,000) 및 인종간 IRR
- **Study design**: 관찰연구 (cohort, cross-sectional, registry/population-based)
- **Time**: 2000-2025 (조정 가능)

## 유방암 특유 방법론
- **연령표준화(age-adjusted) rate만** 사용 (crude rate 배제 또는 별도)
- **침습성(invasive) 유방암** 기준. DCIS(in situ)는 별도/배제
- **아형 층화 가능하면** ER/PR/HER2, TNBC 별로 (흑인 TNBC↑)
- **핵심 교란 = 유방촬영 검진 접근성** (발생률 탐지에 영향) — 논의·민감도에 반영
- **남성 유방암 제외**

## 선별기준 초안 (검토 요망)
INCLUSION
- 관찰연구(cohort/cross-sectional/registry/population-based)
- 사람, 여성
- **침습성 유방암 발생률(age-adjusted incidence)을 인종·민족별로 보고**
- **최소 2개 인종·민족군** (방식 A). 방식 B 채택 시 단일군도 허용
- 영어, 2000-2025

EXCLUSION
- 모든 리뷰(narrative/systematic/scoping)·사설·논평·레터
- 증례보고/증례군 (n<10)
- **발생률(incidence)을 인종별로 보고하지 않음** (사망률·생존율·병기·치료결과만인 것)
- **Prevalence만** 보고 (incidence 없이) → 별도 분류
- 비유방암 / 남성 유방암 / DCIS만 다룬 연구(맥락따라)
- 동물·시험관
- 인식·지식·검진행동·위험요인 노출만 다룬 연구
- crude rate만 보고(age-adjusted 없음) — 또는 민감도에서만

## 검색 (하이브리드)
- PubMed(entrez, 정밀 쿼리) + Embase CSV. Embase와 같은 강도로 조인 PubMed 쿼리
  (orchestrator.py의 PRECISE_PUBMED_QUERY에 넣을 것):
  `("Breast Neoplasms"[Mesh] OR "breast cancer"[tiab] OR "breast carcinoma"[tiab])
   AND (race[ti] OR racial[ti] OR ethnic*[ti] OR minorit*[ti] OR disparit*[ti]
        OR Black[ti] OR Hispanic[ti] OR White[ti] OR Asian[ti] OR "African American"[ti]
        OR "Racial Groups"[Mesh] OR "Ethnicity"[Mesh] OR "Health Status Disparities"[Mesh])
   AND (incidence[ti] OR "incidence rate"[tiab] OR "age-adjusted"[tiab]
        OR "age-standardized"[tiab] OR "Incidence"[Mesh])
   AND (2000:2025[dp]) AND English[lang] AND humans[MeSH]
   NOT (review[pt] OR "case reports"[pt] OR editorial[pt] OR comment[pt] OR letter[pt])`
- Embase는 유방암용으로 새로 export 필요(records_tabular.csv 교체). 사용자가 직접 검색·export 예정.

### Embase 검색어 (확정 — 506건, 사용자가 export → records_tabular.csv)
```
('breast cancer'/exp OR 'breast carcinoma':ti,ab OR 'breast neoplasm':ti,ab)
AND (race:ti OR racial:ti OR ethnic*:ti OR minorit*:ti OR disparit*:ti
     OR black:ti OR hispanic:ti OR white:ti OR asian:ti OR 'african american':ti)
AND (incidence:ti OR 'incidence rate':ti,ab OR 'age-adjusted':ti,ab
     OR 'age-standardized':ti,ab OR 'age standardization'/exp)
AND [2000-2025]/py AND [english]/lim AND [humans]/lim
NOT ('review'/it OR 'case report'/it OR editorial/it OR note/it)
```
- export 필드: Title, Abstract, Author Names, Publication Year, Source, Publication Type,
  MEDLINE PMID, DOI (Abstract·PMID 필수). 저장: `meta_agents/records_tabular.csv`.
- 이 검색어는 race/disparity를 **제목(ti)**, incidence를 **제목 또는 rate 용어**에 요구해
  발생률 격차 논문으로 좁힌 것(5272→2000→506).

## 구현 순서 (새 대화에서)
- ✅ **완료**: orchestrator.py의 PICO/기준/검색어/title 유방암 버전으로 교체됨(commit 5a49488).
- ✅ **완료**: Embase 501건이 `meta_agents/records_tabular.csv`에 변환·저장됨
  (필드형 export를 `convert_embase.py`로 표 형식 변환).

**새 대화는 여기서 시작:**
1. Codespace에서 `python orchestrator.py multi` 실행 → PubMed 자동검색 + Embase 병합
   → 2단계 스크리닝 → **[PAUSED] 포함 논문 목록** 제시 (추출은 null 예상, 정상).
   (`export NCBI_EMAIL/NCBI_API_KEY` 먼저; claude CLI 로그인 필요)
2. `python report_status.py`로 포함 논문·구할 PDF 확인.
3. **Claude가 포함 논문 전문(fulltext/<PMID>.pdf 또는 OA)을 읽고** age-adjusted
   발생률을 인종별로 추출 → `run_meta_analysis.py`의 STUDIES를 유방암 데이터로 새로 작성
   (log(minority_rate/nhw_rate), se_from_ci/se_from_rates).
   - ⚠️ PDF 읽기: 이 환경은 `pip install --force-reinstall cffi` 후 pdfminer.six 사용 가능.
4. `python run_meta_analysis.py` → pooled IRR·forest plot. 필요시 아형(TNBC 등)·민감도.

## 주의
- 자동 추출(Agent 3)은 rate를 못 담음 → **데이터는 Claude가 직접 추출**(4-C 하이브리드 핵심).
- Embase 유방암 CSV가 있으면 병합에 넣고, 없으면 PubMed 단독으로 진행 후 나중에 추가.

## 진행 로그 (2026-07-11)
- ⚠️ **이 원격환경은 NCBI/PubMed(eutils)가 네트워크 정책으로 차단됨**(proxy 403).
  → orchestrator의 PubMed 자동검색·claude CLI 스크리닝 경로 **사용 불가**.
  대신 Claude(=본 세션)가 **Embase 501건 abstract에서 직접 스크리닝·추출**하는
  하이브리드로 진행(계획의 4-C 핵심을 네이티브로 수행).
- ✅ 스크리닝: 501건 → 발생률+인종+유방암 키워드 → rate 값이 담긴 abstract 22건 선별
  → 연령표준화 발생률(per 100k)을 인종별로 추출.
- ✅ 추출 결과: `meta_agents/extracted_studies_breast.md`
- ✅ 메타분석 스크립트: `meta_agents/run_meta_analysis_breast.py`
  (DL random-effects, forest plot PNG, JSON, 요약)
- ✅ 결과: `meta_agents/RESULTS_breast.md`, `output_breast/forest_breast.png`,
  `output_breast/meta_results_breast.json`
- **핵심 결론**: 전체 침습성 발생률은 모든 소수인종 < 백인(흑인 0.69·히스패닉 0.70·
  아시안 0.74·AIAN 0.68). **유일한 예외 = 흑인 TNBC 발생률 백인의 1.9배**(ER- 1.8배).
  즉 흑인 유방암 격차는 전체 발생률이 아니라 **공격적 아형(TNBC/ER-)에 집중**.
- 한계: abstract 기반 추출(전문 미검증), US SEER/USCS 연구 간 데이터 중복(독립성 위배 →
  pooled CI 과소추정), 검진접근 교란. → RESULTS_breast.md 참조.
- 다음 할 일(선택): PubMed 접근 가능한 환경에서 전문 확인·연구 추가, 아형 세분화,
  민감도분석(검진율 보정), 방식 B(단일인종 rate pooling) 보조 분석.
