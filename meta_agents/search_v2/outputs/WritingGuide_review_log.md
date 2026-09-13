# 작성 지침(Writing-guide) 기준 재검수 및 방어적 서술 정리

세션 중 작성 지침(`manuscript/WRITING_GUIDE.md`) 기준으로 재검수하며 교정한 사항 기록.

8개 항목 완료 후 사용자가 작성 지침 기준 재검수를 요청하며 섹션별로 짚었고, 그 과정에서 실제 결함들을 함께 교정.

**정합성, 사실 오류 교정:**
- **Abstract 인코딩 깨짐**: em/en 대시 4곳이 이중 UTF-8 인코딩(`â€"`)으로 깨진 것 바이트 복구.
- **Screening chain 산수 오류**: Results "245 sought / 10 not retrieved"(245−10=235≠237) → PRISMA 도해, 미회수 목록에 맞춰 246 / 9(246−9=237).
- **abstract-only 포함 수 오류**: Methods "four reports whose full text could not be obtained" → 데이터상 실제는 1건(rec 1800, 보충표로 narrative 포함). 166 중 165는 full-text PDF 보유. Discussion "every included study … read"도 "all but one"으로 정정(모순 해소). rec 1800은 not-retrieved 9와 구분(회수, 평가됨)됨을 명시.
- **RoB n 오류**: Methods "all 52 extracted studies" → 55.

**신규성(novelty) 과잉주장 제거(가이드 B7):**
- Abstract "not yet assembled on a common scale" → "not readily comparable across the published literature".
- Introduction "What is missing is a synthesis that…" → "Comparing them therefore calls for…".

**NHW vs unstratified White 구분 강화:**
- Abstract Methods를 "recoverable NHW comparison / IRR versus NHW"에서 "a recoverable White comparison, usually NHW … or versus an unstratified White reference in a minority of cells"로 정정(본문 포함기준과 일치).
- Methods rec 3720 "Black-versus-White" → "Black versus an unstratified White reference"(원장: White=ref, unstratified).
- **non-AI/AN †셀 이유 명시**: 그 셀들(수용체 subtype, age-specific Black 2)은 NHW 출처가 없어 유일이라 unstratified White 유지. AI/AN은 ascertainment override(과소집계 교정)라는 별개 이유. 두 갈래를 대칭으로 기술.

**방어적/로그성 서술 정리(가이드 E "한 일만, 길게 변호 말 것"):**
- Methods 제거/축소: false-negative 개별 로그(→ Supplementary Note 2 신설로 이관), 미국-한정 정당화, 재분류 4편 개별 나열(→ Note 2), 이미지-렌더링 메커니즘, "consistent with … reported below" 안심말, "best-ascertained"(→ ascertainment-preferred), Alaska Native 중복문(이유 붙여 복원), RoB 문단 압축, Eligibility 말미 중복 괄호.
- **"contemporary benchmark" 방어구 완전 제거**: Table 1 note, 그리고 Selection 소절의 "(a single population-based benchmark…)" 잔재까지. "benchmark" 프레이밍은 Table 1, Supplementary Table 4 Note에 유지.

**Supplementary Note 2 신설**: screening false-negative 감사(목적, 방법, 3건 결과, 경계사례, 결론) + 재검증 누락(overlap 6, 재분류 4)을 최종 수치와 정합적으로 편입. Methods의 깨진 참조("in the Supplementary") 해소.

**Supplementary Table 5**: Q9(전 연구 NA, 채점 제외) 열 삭제, 처리 사유는 Note에 유지(피드백의 Q9 보고 요구는 충족). legend에서 NA 제거(Q1–Q8엔 NA 없음).

**민감도 4번째 추가(표준인구 이질성)**: 표준인구 차이가 비교가능성을 제한한다는 지적에 직접 답하도록 "2000 US 표준으로 통일된 추정치만" 재선정(Table 6d) 추가. 결과: representatives 85개 중 83개가 이미 2000 US 표준 → 83 unchanged / 2 changed(Black 수용체 subtype, 1960 Segi world→2000 US, 같은 방향) / 0 dropped. 표준인구 이질성이 실제로는 미미함을 정량 입증. Methods "checked in four ways", Results, Discussion, 내부 정합성 검증(332개 비교) 통과.
