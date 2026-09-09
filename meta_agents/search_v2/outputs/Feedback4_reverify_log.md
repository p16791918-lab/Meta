# 전수 재검수 로그 (Feedback4 #2·#3·#4 재개용)

원문(`fulltext/<rec>.pdf` / `.txt`)을 한 편씩 다시 정독하며 비교군·기간·성별·표준인구·효과지표를
대조하고, 추가로 추출 가능한 정량자료가 있으면 ledger(`breast_extraction.csv`)에 반영한다.
대표값 선택 여부의 최종 판단(어느 추정치를 대표로 쓸지)은 뒤로 미루고, 지금은 **완전한 자료 추출**과
**오류 교정**에 집중한다. 세션이 끊겨도 이 로그의 상태를 보고 이어서 진행한다.

**상태 범례**: ⬜ 미검토 · 🔄 진행 중 · ✅ 재검수 완료
**검수 항목(각 연구)**: (a) 비교군 NHW vs unstratified White, (b) 관찰기간, (c) 여성 한정,
(d) 표준인구, (e) 효과지표(IRR/SIR/rate 계산), (f) CI 유효성(check_G), (g) 추가 추출 가능 자료.

---

## A. 정량(quant) 49편

| rec | author_year | 상태 | 발견/조치 |
|----:|-------------|:----:|-----------|
| 2 | Howlader2014_SEER18 | ✅ | SEER-18 excl. Alaska, 2010, 여성, NHW ref, 2000 US 확인. 9개 값 원문 일치. HR-/HER2+ subtype은 Supplementary Table 3(online-only)라 PDF 추출 불가 → 보류 |
| 10 | DavisLynn2025_SEER17 | ⬜ | subtype-HRpos CI 좁음(대규모 national, 경고만) |
| 12 | Zhang2025_USCS_female | ⬜ | |
| 28 | Nash2019_ANTR | ⬜ | Alaska Native, ANTR, †-comparator |
| 49 | Mills2005 | ⬜ | |
| 51 | Nash2022 | ⬜ | |
| 66 | Hendrick2021_SEER9 | ⬜ | |
| 100 | Liu2012_LACounty | ⬜ | |
| 107 | Zahrieh2021_NM-SEER | ⬜ | |
| 134 | Wingo2008_IHS-CHSDA | ✅ | narrative→quant 재분류(옵션 C). CHSDA national 0.63 + IHS region별 RR·CI 추출. overlap/sensitivity |
| 146 | Xu2024_SEER | ⬜ | |
| 155 | Sung2023_USCS | ✅ | USCS 2015-2019, 여성, NHW ref, 2000 US 확인. national rate(Black 25.2/White 12.9/AIAN 11.2/Hisp 11.1/API 9.0)로 IRR 완전 일치. state별 값은 리뷰 범위 밖(national cell)이라 미추출. AI/AN TNBC 0.86은 unlinked USCS(유일 자료) |
| 161 | Loo2019_HTR | ✅ | 원문 재정독. 원문 CI열 내부모순(1.34 CI 1.347–1.351, 0.58 CI 0.46–0.53 — 점추정 제외) → 해당 2셀 점추정. **누락 추출: Japanese HR-/HER2-(TNBC) 1.07 [1.07,1.09] 추가.** 나머지 좁은 CI는 원문대로 보존(경고), †-comparator overlap |
| 169 | Ellington2022_USCS | ✅ | USCS 1999-2018, 여성 >=20, NHW ref(2018 rate 186.5), 2000 US 확인. Black 0.933/Hisp 0.718/API 0.769/AIAN 0.683(127.3/186.5) 정합. NHB overall 대표 |
| 182 | Cronin2012_VitalSigns | ⬜ | |
| 199 | Baquet2008_SEER9 | ⬜ | |
| 200 | Gleason2012_SEER | ⬜ | |
| 203 | Brinton2008_SEER13 | ⬜ | |
| 209 | Zhang2022 | ⬜ | |
| 234 | Gomez2026_SEER21 | ✅ | SEER-21 2018-2022, 여성, NHW ref(rate 139.5), 2000 US 확인. 11개 AANHPI subgroup 완전(Other Asian/Other PI는 원문도 rate 미계산). rate 스팟체크 일치(NH 177.2/Laotian 54.1/Chinese 106.0). subtype rate는 Supplement online이라 미추출 |
| 236 | Gomez2010 | ⬜ | |
| 265 | Anderson2008_SEER | ⬜ | |
| 286 | Kong2020_SEER18 | ✅ | SEER, 2010-2015, 여성, NHW ref, 2000 US 확인. 기존 10개 subtype 값 원문 완전 일치. **추가 추출**: overall aggregate 4셀(Black 1.04, API 0.90, AI/AN 0.82, Hispanic 0.79)과 AI/AN HR+/HER2- 0.74(AI/AN subtype 유일 추정치→대표, 단 unlinked SEER). AI/AN overall 0.82는 unlinked라 override로 대표 아님(Melkonian 0.87 유지). ⚠️판단: AI/AN subtype 대표가 unlinked SEER임(다른 자료 없음) |
| 324 | Gomez2017_CCR | ⬜ | |
| 333 | Keegan2010_CCR | ⬜ | |
| 346 | Richardson2016 | ⬜ | |
| 381 | Lund2010_AtlantaSEER | ⬜ | |
| 419 | Amirikia2011 | ⬜ | |
| 461 | Watanabe-Galloway2015 | ✅ | Northern Plains, unlinked → IHS-linked Melkonian로 대표 교체, overlap 강등 |
| 463 | Keegan2007_GBACR | ⬜ | |
| 485 | Harper2009_SEER | ✅ | 비교군 "White"가 SEER CSR 정의상 NHW 확인 → 변경 없음(성급한 수정 회피) |
| 500 | Gopalani2020 | ✅ | 원문 Methods "PRCDA 미사용" → IHS-PRCDA 오분류 정정, USCS(NPCR+SEER, unlinked)로. overlap |
| 522 | Ihenacho2023_HTR | ⬜ | |
| 587 | Nasseri2009 | ⬜ | |
| 955 | Goggins2009 | ⬜ | |
| 1478 | Yazzie2025_Navajo | ⬜ | Navajo area AI/AN, IHS-linked |
| 2131 | Xie2022_USCS | ⬜ | |
| 2137 | Melkonian2022 | ⬜ | |
| 2406 | Sung2020_USCS50 | ✅ | 원문 재정독(남성 유방암 논문의 여성 참조패널). **오류 2건 정정**: 비교군 'White'→**NHW**(원문 "white non-Hispanic"), 기간 2011-2015→**2010-2016**(Table 1). **추가 추출**: 여성 subtype 4셀(HR+/HER2- 0.79, HR+/HER2+ 1.01, TNBC 1.93, HR-/HER2+ 1.29; 모두 NHW·CI). ⚠️**판단 필요(나중에)**: USCS(tier9)>SEER(tier6) 규칙상 Sung2020이 Kong2020(rec286)을 제치고 Black HR+/HER2-·HR+/HER2+·HR-/HER2+ 3셀 대표로 자동 교체됨(0.86→0.79, 1.12→1.01, 1.46→1.29). 그러나 이 논문은 남성 유방암 연구의 부수 패널이므로 여성 subtype 대표로 적절한지 재검토 요망 |
| 2510 | Melkonian2019_IHS-PRCDA | ✅ | AI/AN national 대표 0.87(point, 원문 CI 없음). 기간 2012-2016→2010-2015 정정. IHS region 6개 값 추출 |
| 3182 | Pinheiro2009_FL | ⬜ | Hispanic 출신국별 |
| 3267 | Kem2007 | ⬜ | |
| 3298 | Carozza2006_multistate | ⬜ | |
| 3398 | Gomez2003_SEERplusCCR | ⬜ | |
| 3662 | Melkonian2021_IHS-PRCDA | ✅ | Southern Plains 1.33 대표(IHS-linked). region 값 확인 |
| 4027 | Jin2016 | ⬜ | AANHPI subgroup |
| 4040 | Miller2008_NAACCR-API | ⬜ | |
| 4098 | McCracken2007_CCR | ⬜ | |
| 4333 | Wilkinson2002 | ⬜ | |

**진행 요약**: 완료 13 / 49 (rec 2, 134, 155, 161, 169, 234, 286, 461, 485, 500, 2406, 2510, 3662).

**나중에 판단할 목록(대표 교체 후보 등)**:
- rec 2406 Sung2020: 남성 유방암 논문의 여성 패널이 Black subtype 3셀 대표로 자동 선정됨 → 유지/교체 판단.
- rec 286 Kong2020: AI/AN HR+/HER2- 0.74가 unlinked SEER인데 AI/AN subtype 유일 자료라 대표 → AI/AN undercount 방침과 상충 여부 판단.

## B. 서술(narrative) 113편
Wingo(rec 134)처럼 NHW 비교를 복원할 수 있어 quant로 승격 가능한 편이 더 있는지 배치로 재검수.
- 상태: ⬜ 미착수 (배치 단위로 IRR/rate·비교군 존재 여부 스캔 예정)

## C. 항구적 점검
- `crosscheck_master.py` [G] CI validity: 모든 보고 CI가 점추정을 포함(순서·bracket) 하는지 확인,
  subgroup×subtype의 비현실적으로 좁은 CI는 경고. 현재 [A–G] ALL PASS(경고 7건은 전부 대규모
  national aggregate이거나 Loo 원문 보존값).
