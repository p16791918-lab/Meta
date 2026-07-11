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
- PubMed(entrez, 정밀 쿼리) + Embase CSV. 예시 정밀 쿼리:
  `("Breast Neoplasms"[Mesh] OR breast cancer[tiab] OR breast carcinoma[tiab])
   AND ("Racial Groups"[Mesh] OR "Ethnicity"[Mesh] OR race[tiab] OR ethnic*[tiab] OR racial[tiab])
   AND ("Incidence"[Mesh] OR incidence[tiab] OR "incidence rate"[tiab])
   AND (2000:2025[dp]) AND English[lang] AND humans[MeSH]
   NOT (review[pt] OR "case reports"[pt] OR editorial[pt] OR comment[pt])`
- Embase는 유방암용으로 새로 export 필요(records_tabular.csv 교체). 사용자가 직접 검색·export 예정.

### Embase 검색어 (사용자가 Embase.com에서 실행 → CSV export)
```
('breast cancer'/exp OR 'breast carcinoma':ti,ab OR 'breast neoplasm':ti,ab)
AND ('ethnicity'/exp OR 'ethnic group'/exp OR 'racial group'/exp OR 'health disparity'/exp
     OR race:ti,ab OR racial:ti,ab OR ethnic*:ti,ab OR minority:ti,ab)
AND ('incidence'/exp OR incidence:ti,ab OR 'incidence rate':ti,ab)
AND [2000-2025]/py AND [english]/lim AND [humans]/lim
NOT ('review'/it OR 'case report'/it OR editorial/it OR note/it)
```
- export 필드: Title, Abstract, Author Names, Publication Year, Source, Publication Type,
  MEDLINE PMID, DOI (Abstract·PMID 필수). 저장: `meta_agents/records_tabular.csv`.

## 구현 순서 (새 대화에서)
1. `orchestrator.py` __main__의 MY_PICO / INCLUSION / EXCLUSION / PRECISE_PUBMED_QUERY를
   위 유방암 버전으로 교체 (title도).
2. `python orchestrator.py multi` → 검색·스크리닝 → 포함 논문 목록 확보 (추출은 null 예상).
3. **Claude가 포함 논문 전문을 읽고** age-adjusted 발생률을 인종별로 추출 →
   `run_meta_analysis.py`의 STUDIES를 유방암 데이터로 새로 작성 (log(minority/nhw), SE).
4. `python run_meta_analysis.py` → pooled IRR·forest plot. 필요시 아형·민감도.

## 주의
- 자동 추출(Agent 3)은 rate를 못 담음 → **데이터는 Claude가 직접 추출**(4-C 하이브리드 핵심).
- Embase 유방암 CSV가 있으면 병합에 넣고, 없으면 PubMed 단독으로 진행 후 나중에 추가.
