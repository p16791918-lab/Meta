# 4차 피드백 대응 정리 (Response to 4th-round comments)

각 코멘트에 대해 어떻게 수정했는지 항목별로 정리합니다. 원 코멘트는 `Advice/Feedback4.md` 참조.
(진행 상태: ✅ 완료 · 🔄 진행 중 · ⬜ 예정)

---

## 항목 1. AI/AN 자료원 분류와 대표값 선정 — ✅ 완료

**지적**: Gopalani 2020이 CDC WONDER/USCS를 썼고 PRCDA를 쓰지 않았다고 명시했는데 IHS-PRCDA로 분류됨. 자료원을 바로잡고 대표값·RoB·민감도 재확인. Northern Plains가 한 연구뿐이라는 설명도 재검토.

**수정**:
- **자료원 정정**: Gopalani 2020(rec 500)을 원문대로 **USCS(NPCR+SEER, unlinked)**로 정정(원문 Methods: "We did not use [PRCDA] classifications"). IHS-linked 오분류를 제거.
- **대표값 재선정**: 진짜 IHS-PRCDA national 자료인 **Melkonian 2019**(rec 2510, breast RR **0.87** vs NHW, 원문 "Non-Hispanic white was chosen as the reference")가 AI/AN aggregate 대표가 됨. **0.56 → 0.87**. 원문에 CI·case count가 없어 **point estimate**로 제시(피드백 4항 취지와 일치, 근사 계산 안 함).
- **순위 재편**: Hispanic 0.72 < AANHPI 0.77 < AI/AN 0.87 < NHB 0.93 → **최저는 Hispanic**(기존엔 AI/AN). Abstract·Results·Discussion 반영.
- **Northern Plains**: Melkonian 2019에 Northern Plains 추정치(IHS-PRCDA, RR **1.05**)가 있으므로, 현재 대표를 unlinked Watanabe-Galloway(0.90)에서 **IHS-linked Melkonian(1.05)**로 교체. "단일 연구뿐" 설명을 삭제(rec 461은 overlap으로 강등). Alaska(1.26)·Southern Plains(1.30) 지역값도 ledger에 추가(각각 ANTR 1.09·Melkonian 2021 1.33 대표는 유지, Melkonian 2019는 overlap).
- **RoB**: rec 500이 unlinked가 되며 JBI Q7(race ascertainment) undercount → RoB Low 39→38, Moderate 9→10.
- **민감도**: 재실행(저위험 55/8/10, 직접보고 36/5/32, NHW 55/1/17). crosscheck [A–F] ALL PASS.
- **기간 정정**: 재확인 중 rec 2510 period 2012-2016 → **2010-2015**(Table 2) 오류도 정정.
- **부수 효과**: Discussion을 "unlinked 0.56은 불완전 ascertainment, IHS-linked로 0.87 보정"으로 재서술 → **항목 9(3차 피드백, AI/AN 해석)도 동시 해결**.

---

## 항목 2. 포함·분석 배정·대표값 선정 기준의 일관 적용 — ⬜ 예정
중복 연구의 제외/민감도 포함 기준, Wingo 2008의 narrative-only 분류 이유, 연구별 추출가능·선택/미선택 로그, 'analytic cell당 하나' 서술 통일, 중복 판정을 registry 명칭이 아니라 지역·기간·인구로.

## 항목 3. 비교군·기간·연령·효과지표 재검증 — ⬜ 예정
master dataset 핵심정보 원문 재대조(Sung 2020 성별·비교군·기간), NHW vs unstratified White 구분, SIR 해석, 표준인구 미상 시 '불명확' 기록.

## 항목 4. 연령표준화 IRR의 CI 계산 재검토 — ⬜ 예정
Poisson CI(총 사건 수) 적용 재검토, 원문 SE/CI 우선, 부족 시 점추정 또는 한계 명시, Loo 2019의 좁은 CI 확인.

## 항목 5. 연구 간 비교 한계·민감도 해석 반영 — ⬜ 예정
"standard population largely cancels" 수정, "contemporary benchmark" 재검토, Figure 2에 이질 출처 명시, Japanese 등 방향전환 설명.

## 항목 6. 서술적 종합·검토 절차 보고 완성 — ⬜ 예정
narrative 114편 주제별 정리+근거 연결, LLM 모델·역할·재검토 표본·누락 보고, PROSPERO 상태 정리, JBI Q9 표기 정합·RoB 판정 기준.

## 항목 7. 리뷰 기여 명확화·제출자료 최종 점검 — ⬜ 예정
기존 연구 대비 추가 확인점, 연구 간 일치/불일치·비교가능성·근거부족 집단, 본문·표·그림 수치/번호·비교군·민감도 목록 정합, PDF 그림 잘림.

## 항목 8. 서식 de-AI (본문·Supplementary) — ⬜ 예정
파란 제목→검정, 제목 스타일 점 제거→기본, 표 상단 청록 배경 제거→굵은 글씨+최소 구분선, 표 제목 아래 설명을 표 아래 Note.로 이동, Note는 방법·비교군·기호·약어만.
