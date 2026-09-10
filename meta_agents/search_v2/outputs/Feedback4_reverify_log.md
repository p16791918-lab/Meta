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
| 10 | DavisLynn2025_SEER17 | ✅ | Ghana/US Black/NHW, SEER-17 2013-2015, 여성 20-74, NHW ref. **표준인구=Segi 1960 world**(원문 명시)→2000 US 연구와 이질(이미 명시). overall 148.5/152.9, ER+ 105.4/128.5, ER- 43.1/24.0 원문 일치. subtype-HRpos(=ER+)/HRneg(=ER-) 대표. CI 좁음은 대규모 SEER |
| 12 | Zhang2025_USCS_female | ✅ | USCS 2017-2021, 여성, NHW ref(139.0). Black 129.3/API 110.3/AIAN 113.0/Hisp 101.2 원문 일치. AIAN unlinked→overlap. registry 라벨 "Other/unspecified"(tier1)지만 AIAN 어차피 non-대표 |
| 28 | Nash2019_ANTR | ✅ | ANTR(IHS-eligibility), 2009-2014, 여성, 2000 US. AN 145.0/USW 133.0 RR 1.09 원문 일치. 비교군 **US White(unstratified)=†** 확인. Alaska Native 셀 대표 |
| 49 | Mills2005 | ✅ | Hmong California. Hmong 23.8/NHW 145.5 원문 일치, NHW ref. ⚠️기간 불일치(Hmong 1988-2000 vs NHW 1995-1999) 이미 period/notes에 명시 — Hmong 소수라 불가피, 유일 자료라 대표 |
| 51 | Nash2022 | ✅ | ANTR 2014-2018, Alaska Native 130.8 vs **external SEER-Explorer NHW 137.4**(같은-source 아님)→overlap only(Methods 명시). RR 0.952 |
| 66 | Hendrick2021_SEER9 | ✅ | SEER 2013-2017, 여성, NHW ref, IRR 직접보고(rate 미보고). Black 0.97/API 0.92/AIAN 0.58/Hisp 0.75 원문 일치. AIAN unlinked→overlap |
| 100 | Liu2012_LACounty | ✅ | LA County 2007, NHW ref(145.8). Black 125.2/Chinese 83.9/Korean 81.3/Hisp 77.5 원문 일치(point) |
| 107 | Zahrieh2021_NM-SEER | ✅ | New Mexico 2005-2014, NHW ref, AIAN 0.384 원문 일치(IRR 직접). NM AI/AN unlinked overlap |
| 134 | Wingo2008_IHS-CHSDA | ✅ | narrative→quant 재분류(옵션 C). CHSDA national 0.63 + IHS region별 RR·CI 추출. overlap/sensitivity |
| 146 | Xu2024_SEER | ✅ | 여성 20-49, 2000-2019, NHW ref, IRR 직접보고. age-lt50 Black 1.01/API 0.96/AIAN 0.75/Hisp 0.76. age-specific 대표 |
| 155 | Sung2023_USCS | ✅ | USCS 2015-2019, 여성, NHW ref, 2000 US 확인. national rate(Black 25.2/White 12.9/AIAN 11.2/Hisp 11.1/API 9.0)로 IRR 완전 일치. state별 값은 리뷰 범위 밖(national cell)이라 미추출. AI/AN TNBC 0.86은 unlinked USCS(유일 자료) |
| 161 | Loo2019_HTR | ✅ | 원문 재정독. 원문 CI열 내부모순(1.34 CI 1.347–1.351, 0.58 CI 0.46–0.53 — 점추정 제외) → 해당 2셀 점추정. **누락 추출: Japanese HR-/HER2-(TNBC) 1.07 [1.07,1.09] 추가.** 나머지 좁은 CI는 원문대로 보존(경고), †-comparator overlap |
| 169 | Ellington2022_USCS | ✅ | USCS 1999-2018, 여성 >=20, NHW ref(2018 rate 186.5), 2000 US 확인. Black 0.933/Hisp 0.718/API 0.769/AIAN 0.683(127.3/186.5) 정합. NHB overall 대표 |
| 182 | Cronin2012_VitalSigns | ✅ | Vital Signs 2004-2008, black/white 언급(Hisp 미층화)→**unstratified White(†)**로 보수 분류. Black 116.9/122.1=0.957. overlap |
| 199 | Baquet2008_SEER9 | ✅ | SEER-9 1995-2004, blacks/whites(unstratified White †), age-lt40 Black 1.16(IRR 직접). age-specific |
| 200 | Gleason2012_SEER | ✅ | SEER-17 2004-2008, black/white만 분류(Hispanic 미층화)→비교군 **unstratified White(†)** 확인. cumulative incidence(CIR) 사용이라 rate 값 큼(비율은 정확). receptor-defined subtype(ERpos-PRneg/ERneg-PRpos) 대표는 † |
| 203 | Brinton2008_SEER13 | ✅ | younger women 1992-2004, NHW ref(173.2). Black 146.9/173.2=0.85 원문 일치(IRR 직접) |
| 209 | Zhang2022 | ✅ | TNBC 2019, NHW ref(12.8). Black 25.0/Hisp 11.5/AIAN 9.4/API 9.5 원문 일치(point). TNBC overlap |
| 234 | Gomez2026_SEER21 | ✅ | SEER-21 2018-2022, 여성, NHW ref(rate 139.5), 2000 US 확인. 11개 AANHPI subgroup 완전(Other Asian/Other PI는 원문도 rate 미계산). rate 스팟체크 일치(NH 177.2/Laotian 54.1/Chinese 106.0). subtype rate는 Supplement online이라 미추출 |
| 236 | Gomez2010 | ✅ | CA 1988-2004, 여성, NHW ref(146.1). 5개 subgroup rate 원문 일치(Chinese 73.5/Japanese 102.5/Filipina 100.4/Korean 46.3/Vietnamese 59.9). migrant-status 층화는 분석단위 밖 |
| 265 | Anderson2008_SEER | ✅ | black/white crossover, 2008, **unstratified White(†)**. age-lt40 1.183(15.5/13.1)/age-ge40 0.851(239.5/281.3). age-specific |
| 286 | Kong2020_SEER18 | ✅ | SEER, 2010-2015, 여성, NHW ref, 2000 US 확인. 기존 10개 subtype 값 원문 완전 일치. **추가 추출**: overall aggregate 4셀(Black 1.04, API 0.90, AI/AN 0.82, Hispanic 0.79)과 AI/AN HR+/HER2- 0.74(AI/AN subtype 유일 추정치→대표, 단 unlinked SEER). AI/AN overall 0.82는 unlinked라 override로 대표 아님(Melkonian 0.87 유지). ⚠️판단: AI/AN subtype 대표가 unlinked SEER임(다른 자료 없음) |
| 324 | Gomez2017_CCR | ✅ | California Asian 2009-2013, NHW ref, IRR 직접보고. TNBC 0.61/HRneg-HER2pos 1.21 원문 일치. Japanese/Filipino(young) age-specific |
| 333 | Keegan2010_CCR | ✅ | California Hispanic(nativity) 1988-2004, NHW ref(125.7). Hispanic 78.3/125.7=0.623 정합. computed A |
| 346 | Richardson2016 | ✅ | age-specific black-white, 2011, **unstratified White(†)**. Black 121.5/123.6=0.983. overlap |
| 381 | Lund2010_AtlantaSEER | ✅ | Atlanta 2003-2004, NHW ref(원문 "white (non-Hispanic)"). HRpos-HER2neg 86.7/110.7=0.783, TNBC 36.3/19.4=1.871(point). overlap |
| 419 | Amirikia2011 | ✅ | TNBC 1988-2006, NHW ref(12.6). Black 23.6/12.6=1.873, Hisp 10.2/12.6=0.810(point). computed A. overlap |
| 461 | Watanabe-Galloway2015 | ✅ | Northern Plains, unlinked → IHS-linked Melkonian로 대표 교체, overlap 강등 |
| 463 | Keegan2007_GBACR | ⚠️보류 | Bay Area 6 Asian subgroup 1990-2002. minority rate만 있고 **원문에 same-source NHW rate 미제공 → IRR 계산 불가**(현재 IRR 공백). 외부 NHW 붙이면 same-source 원칙 위반이라 안 채움. **narrative 재분류 후보(판단 나중에)**; 6 subgroup 모두 overlap이라 대표 영향 없음 |
| 485 | Harper2009_SEER | ✅ | 비교군 "White"가 SEER CSR 정의상 NHW 확인 → 변경 없음(성급한 수정 회피) |
| 500 | Gopalani2020 | ✅ | 원문 Methods "PRCDA 미사용" → IHS-PRCDA 오분류 정정, USCS(NPCR+SEER, unlinked)로. overlap |
| 522 | Ihenacho2023_HTR | ✅ | Hawaii(HTR), 2010-2014, 여성, NHW ref, age-specific(<50/>=50) AANHPI subgroup. computed A 통과. NH/Japanese/Filipina age별 대표 |
| 587 | Nasseri2009 | ✅ | Middle Eastern CA 1988-2004, 여성, NHW ref(원문 "non-Hispanic White (NHW)"), 2000 US. 126.2/146.9 RR 0.86 원문 일치. Middle Eastern(MENA) 대표 |
| 955 | Goggins2009 | ✅ | Asian Indian/Pakistani, 1988-2004, **SIR**(US White std, world std pop) 0.61[0.56-0.66]. comparison_vs=SIR reference로 표시. overlap |
| 1478 | Yazzie2025_Navajo | ✅ | Navajo Nation registry(IHS), 2014-2018, 여성, NHW ref(AZ/NM 6개 county), 2000 US. Navajo 60.9/NHW 123.4 RR 0.49 원문 일치. **NHW rate 123.4[121.6-125.1] 빈칸 보강** |
| 2131 | Xie2022_USCS | ✅ | USCS(CDC WONDER), 1999-2017, 여성, NHW ref(131.0). Black 0.940/AIAN 0.718/API 0.694/Hisp 0.710 원문 일치. AIAN unlinked→overlap. comparison_vs="White (NH)"는 코드 NHW_OK로 NHW 취급(문제없음) |
| 2137 | Melkonian2022 | ✅ | urban NH AI/AN, **IHS-linked(UIHO)**, 2008-2017, NHW ref(129.6), 2000 US. urban US-overall breast 74.2/129.6 RR 0.57 원문 일치. urban subset이라 overlap. 지역별 urban(Alaska 1.31/S.Plains 1.18)은 urban-only subset이라 미추출 |
| 2406 | Sung2020_USCS50 | ✅ | 원문 재정독(남성 유방암 논문의 여성 참조패널). **오류 2건 정정**: 비교군 'White'→**NHW**(원문 "white non-Hispanic"), 기간 2011-2015→**2010-2016**(Table 1). **추가 추출**: 여성 subtype 4셀(HR+/HER2- 0.79, HR+/HER2+ 1.01, TNBC 1.93, HR-/HER2+ 1.29; 모두 NHW·CI). ⚠️**판단 필요(나중에)**: USCS(tier9)>SEER(tier6) 규칙상 Sung2020이 Kong2020(rec286)을 제치고 Black HR+/HER2-·HR+/HER2+·HR-/HER2+ 3셀 대표로 자동 교체됨(0.86→0.79, 1.12→1.01, 1.46→1.29). 그러나 이 논문은 남성 유방암 연구의 부수 패널이므로 여성 subtype 대표로 적절한지 재검토 요망 |
| 2510 | Melkonian2019_IHS-PRCDA | ✅ | AI/AN national 대표 0.87(point, 원문 CI 없음). 기간 2012-2016→2010-2015 정정. IHS region 6개 값 추출 |
| 3182 | Pinheiro2009_FL | ✅ | FL 1999-2001, 여성, NHW ref(140.4). 출신국별 rate 원문 일치(Cuban 108.0/Mexican 71.9/PR 116.9/New Latino 97.8). Hispanic 출신국 대표 |
| 3267 | Kem2007 | ✅ | Cambodian CA+WA 1998-2002. 41.0/NHW 155.5 원문 일치, NHW ref. Cambodian 유일 자료라 대표 |
| 3298 | Carozza2006_multistate | ✅ | US Hispanic 1995-2000, NHW ref(138.7). Hispanic 89.2/138.7=0.643 원문 일치. computed A |
| 3398 | Gomez2003_SEERplusCCR | ✅ | Korean, 1988-1992, NHW ref(98.7). 25.1/98.7=0.254. computed A |
| 3662 | Melkonian2021_IHS-PRCDA | ✅ | Southern Plains 1.33 대표(IHS-linked). region 값 확인 |
| 4027 | Jin2016 | ✅ | Asian American 2009-2011, 여성, NHW ref, 2000 US. 6개 subgroup+aggregate 완전(Hmong/Laotian/Thai 등은 원문도 "too small"→Southeast Asian 합산, 개별 미산출). computed A 통과 |
| 4040 | Miller2008_NAACCR-API | ✅ | NAACCR 1998-2002, NHW ref(145.2). Native Hawaiian 175.8/145.2=1.211 원문 일치 |
| 4098 | McCracken2007_CCR | ✅ | California Asian 2000-2002, NHW ref(152.9). Chinese 75.1/Filipina 102.4/Vietnamese 55.5/Korean 50.7/Japanese 102.8 원문 일치(point, CI 없음) |
| 4333 | Wilkinson2002 | ✅ | South FL Hispanic 1990-1998, NHW ref(125.8). 81.9/125.8=0.651 원문 일치. computed A |

**진행 요약**: 완료 48 / 49 + 보류 1(rec 463). **quant 전수 재검수 완료.** 완료: rec 2,10,12,28,49,66,134,155,161,169,200,234,236,286,324,333,461,485,500,522,587,1478,2131,2137,2406,2510,3182,3267,3662,4027,4040,4098.

**판단 결정 완료(교수 확인, 2026-09-10)**:
- ✅ rec 2406 Sung2020 → **대표 유지(A)**. 커버리지 우선 규칙상 USCS(~99%)가 SEER를 앞섬. 근거를 Feedback4_response 항목 3에 명시.
- ✅ rec 286 Kong2020 AI/AN subtype → **대표 유지(A)** + unlinked undercount 한계를 Discussion에 명시(IHS-linked subtype 자료 부재).
- ✅ rec 463 Keegan2007 → **narrative 강등**. 원문에 same-source NHW rate 없음 재확인. ledger 6행 제거, ft_eligibility narrative, quant 49→48·narrative 113→114·estimates 179→173.
- ✅ rec 1398 → **narrative 유지(A)** + Supp Table 2에 narrative 세부 사유("annual trend, not poolable") 표시(같은 방식으로 trend 6편·중복요약 9편도 사유 구분).

## B. 서술(narrative) 113편 — ✅ 재검수 완료(2패스)

### ⚠️ 1차 스캔의 결함(정직 기록)
1차 스캔은 ASCII 하이픈만 매칭해 **유니코드 하이픈(`non‐Hispanic`, U+2010)** 문서를 통째로 놓쳤다.
"narrative 분류가 견고"라는 1차 결론은 근거가 부실했다. 2차에서 하이픈 정규화 + 넓은 패턴으로 재스캔.

### 2차 스캔(하이픈 정규화)
1차 대비 **9편이 새로 후보에 올라옴**: rec 46, 126, 207, 504, 1101, 1457, 1629, 2453, 4082.
각 편을 원문 정독한 결과:
- **rec 4082**(Annual Report to Nation, 2017-2021 USCS) — **Table에 race별 breast rate 있음**
  (All 123.7 / NHW 130.5 / NHB 125.3 / AIAN 99.1 / API 111.6 / Hisp 95.7 → IRR NHB 0.96·AIAN 0.76·API 0.86·Hisp 0.73).
  recoverable하지만 **rec 12(USCS 2017-2021)와 same registry·period 중복**. ft_eligibility note에 이미
  "secondary synthesis … not pooled to avoid duplication"으로 정확히 기재돼 있었음 → **중복 요약, narrative 유지 정당**.
- **rec 0·18·1453·1457**(ACS Breast Cancer Statistics·MMWR·Cancer Disparities·Cancer Statistics) — 동일하게
  전용 SEER/USCS 대표와 **중복인 종합 surveillance 요약**. ft_eligibility note에 이미 중복 사유 기재됨. narrative 유지.
- **rec 46·126**(subtype APC trend): 절대 rate가 전부 Figure에만 있어 race별 값 추출 불가 → narrative 정당.
- **rec 504**(persistent-poverty area): IRR이 **PPA vs non-PPA**(지역효과)지 race-vs-NHW 아님 → narrative 정당.
- **rec 207·1101·1629·2453**: breast 단독 race-vs-NHW rate/IRR 없음(NHPI trend·Somali 소수·fertility cancer group RR·survival) → narrative 정당.

**결론(2차): 종합요약 리포트는 이미 "중복" 사유로 정확히 narrative 처리돼 있었고, 전용 자료를 놓친 quant 오분류는 없음.**
단 Results의 narrative 설명이 종합리포트 예외를 뭉뚱그렸던 것을 교정함(중복 요약도 narrative 사유임을 명시).

### 1차에서 본 후보 개별 판정(유지):
- **rec 3275** (Nasseri, Middle Eastern CA 1988-2002): female breast RR 0.86(126.16/146.89 vs NHW)를
  보고하나 **rec 587(Nasseri 2009, 1988-2004, RR 0.86)과 사실상 동일 CCR 데이터 → 중복**. narrative 유지.
- **rec 322** (Hawaii/continental female breast, White referent): 비교군이 **unstratified White**이고
  Hawaii/continental 층화 + **histologic**(medullary/inflammatory) subtype 중심이라 national cell 부적합. narrative 유지.
- **rec 1398** (early-onset Black-vs-NHW, SEER 2003-2022): breast IRR+CI가 있으나 **연도별 trend**(2003 1.03 → 2022 0.94)로
  단일 poolable 추정치가 아니며(ft_reason에 이미 명시된 재분류 사유), age-lt50 Black 셀은 rec 146이 대표.
  ⚠️판단 보류: 최신 2022 IRR 0.94를 age-lt50 Black overlap(sensitivity)으로 넣을지.
- 나머지 44 후보: breast의 White-대비 IRR/RR 직접보고 없음(단일집단·trend·SES/구조·survival HR 등) → narrative 정당.

## C. 항구적 점검
- `crosscheck_master.py` [G] CI validity: 모든 보고 CI가 점추정을 포함(순서·bracket) 하는지 확인,
  subgroup×subtype의 비현실적으로 좁은 CI는 경고. 현재 [A–G] ALL PASS(경고 7건은 전부 대규모
  national aggregate이거나 Loo 원문 보존값).
