const {
  Document, Packer, Paragraph, TextRun, HeadingLevel,
  Table, TableRow, TableCell, WidthType, ShadingType, BorderStyle, AlignmentType,
} = require("docx");
const fs = require("fs");

const FONT = "Malgun Gothic"; // Korean-capable; LibreOffice falls back if absent
const TW = 9360; // table width (DXA) within US-Letter margins

function t(text, opts = {}) { return new TextRun({ text, font: FONT, size: 20, ...opts }); }
function p(text, opts = {}) {
  return new Paragraph({ children: [t(text, opts)], spacing: { after: 120 }, ...(opts.pOpts || {}) });
}
function h(text, level) {
  return new Paragraph({ heading: level, spacing: { before: 240, after: 120 },
    children: [new TextRun({ text, font: FONT, bold: true })] });
}
function cell(text, w, { bold = false, shade = null } = {}) {
  return new TableCell({
    width: { size: w, type: WidthType.DXA },
    shading: shade ? { type: ShadingType.CLEAR, color: "auto", fill: shade } : undefined,
    margins: { top: 40, bottom: 40, left: 80, right: 80 },
    children: [new Paragraph({ children: [t(text, { bold })] })],
  });
}
function table(headers, rows, widths) {
  const border = { style: BorderStyle.SINGLE, size: 4, color: "BBBBBB" };
  const borders = { top: border, bottom: border, left: border, right: border,
    insideHorizontal: border, insideVertical: border };
  const headRow = new TableRow({
    tableHeader: true,
    children: headers.map((hd, i) => cell(hd, widths[i], { bold: true, shade: "E7EEF6" })),
  });
  const bodyRows = rows.map(r => new TableRow({
    children: r.map((c, i) => cell(c, widths[i])),
  }));
  return new Table({ columnWidths: widths, width: { size: TW, type: WidthType.DXA },
    borders, rows: [headRow, ...bodyRows] });
}

const kids = [];
kids.push(new Paragraph({ spacing: { after: 80 },
  children: [new TextRun({ text: "Feedback 대응표", font: FONT, bold: true, size: 32 })] }));
kids.push(p("교수님 Feedback의 7개 항목 + 총평 각각에 대해, 무엇을 어떻게 반영했는지와 해당 자료 파일을 정리했습니다. 상태: 완료 / 부분(선생님 확인·작성 필요) / 미착수.", { size: 18, italics: true }));

kids.push(h("1. 전체적인 문장 수정 (1인칭·수사적·절대적 표현, 재작성)", HeadingLevel.HEADING_2));
kids.push(table(["지적", "조치", "상태"], [
  ["1인칭 단수 (I searched/found)", "Results 초안을 중립·수동태로 작성", "부분"],
  ["수사·공격적 표현 (misleading 등)", "초안에서 배제, 객관 서술만", "부분"],
  ["절대 표현 (every/all/no single)", "결과가 뒷받침하는 범위로 한정", "부분"],
  ["결론 반복·AI 티 → 재작성", "본문 재작성은 선생님 영역", "미착수"],
], [3000, 4560, 1800]));
kids.push(p("자료: RESULTS_DRAFT.md", { size: 18 }));

kids.push(h("2. 문헌검색 — 완료 (PROSPERO 제외)", HeadingLevel.HEADING_2));
kids.push(table(["지적", "조치", "상태"], [
  ["2개 DB로 부족 → 4개 DB", "PubMed/MEDLINE·Embase·Scopus·Web of Science (9,099건)", "완료"],
  ["PubMed/MEDLINE 표기", "단일 표기로 통일", "완료"],
  ["검색식은 Supplementary로", "S1 Table (DB별 식·플랫폼·날짜·건수)", "완료"],
  ["제목 제한 → title/abstract", "인종·민족 개념 title/abstract/keyword 확장", "완료"],
  ["PROSPERO 재등록", "선생님이 직접 등록 필요", "미착수"],
], [3000, 4560, 1800]));
kids.push(p("자료: SEARCH_STRINGS_v2.md, SEARCH_LOG.md", { size: 18 }));

kids.push(h("3. PRISMA flowchart — 완료", HeadingLevel.HEADING_2));
kids.push(p("PRISMA 2020 형식으로 재작성. 4개 DB 식별(9,099) → 중복제거(4,306) → 스크리닝(4,793) → 전문검토(242) → 제외 79건(사유별 건수 명시) → 포함 163 → 추출 43."));
kids.push(p("자료: Fig_PRISMA.png, PRISMA_COUNTS.md", { size: 18 }));

kids.push(h("4. Risk of bias — 완료 (검수 필요)", HeadingLevel.HEADING_2));
kids.push(p("예시 논문의 Newcastle-Ottawa Scale 형식(Selection/Comparability/Outcome, Good/Fair/Poor)을 발생률 연구에 맞게 적용. 43편 → Good 35 / Poor 8. Feedback대로 AI 1차안이며 선생님이 몇 개 검수 필요."));
kids.push(p("자료: TableS_risk_of_bias.md/.csv", { size: 18 }));

kids.push(h("5. 중복 registry 자료 처리 — 완료", HeadingLevel.HEADING_2));
kids.push(table(["지적", "조치"], [
  ["registry·지역·기간·연령·군·outcome 표로 중복 확인", "대표선정 표 작성"],
  ["가장 포괄적/최근/명확한 연구 1편을 대표로", "one-per-registry-family 원칙"],
  ["전체·세부민족·아형·연령은 다른 연구 가능", "분석셀(차원×군×family)별 대표 선정"],
  ["주분석=one-per-family, 민감도=전부/중복제외", "주분석 + 전부포함 민감도 비교"],
  ["대표선정 이유를 Supplementary에", "representative_reason 컬럼 기록"],
], [4680, 4680]));
kids.push(p("자료: TableSA_main_representatives.csv, Table_sensitivity_I2.md", { size: 18 }));

kids.push(h("6. 통계분석과 결과 해석 — 완료", HeadingLevel.HEADING_2));
kids.push(table(["지적", "조치"], [
  ["I² 99–100%를 'noise 아니다' 단정 금지", "중복 registry 투입에 의한 비독립성 인공물로 설명; pooled 해석 제한 명시"],
  ["DL만 쓰고 영향없다 단정 금지", "DL vs Paule-Mandel(REML) vs Hartung-Knapp 비교표"],
  ["직접보고/계산/그림추출/근사SE 구분", "provenance 6종 분류 + 유도 로그"],
  ["같은 표준인구·기간·비교군 확인", "std_pop·period·comparator 기록, 불일치 flag"],
  ["age-std 자체가 잘못된 것처럼 표현 금지", "'전체 표준화가 연령별 차이를 충분히 못 보여줄 수 있다' 수준"],
  ["인종차를 유전·생물기전 직결 금지", "가설·가능한 설명으로만 (Discussion 가이드)"],
], [4680, 4680]));
kids.push(p("자료: Table_sensitivity_I2.md, Table_method_comparison.md, DERIVATIONS.md, Sensitivity1/2", { size: 18 }));

kids.push(h("7. 본문 구성 — 부분", HeadingLevel.HEADING_2));
kids.push(table(["지적", "조치", "상태"], [
  ["제목 간결하게", "'Racial and Ethnic Differences in Breast Cancer Incidence in the United States: A Systematic Review and Meta-Analysis' 채택", "완료"],
  ["Intro/Methods/Results/Discussion 재구성", "구성 가이드 + Results 초안", "부분"],
  ["동일 주장 반복 금지", "문단별 1회만", "부분"],
  ["용어 통일 (NHB/NHW/세부민족)", "원 논문 정의 기준 통일", "부분"],
], [3000, 4560, 1800]));

kids.push(h("총평 — 8개 항목 요약 (선생님 본인 문장 작성 영역)", HeadingLevel.HEADING_2));
kids.push(p("교수님이 학생에게 '직접 읽고 본인 문장으로 요약하라'고 한 항목. 아래 자료를 참고해 선생님이 직접 작성: 1.연구질문·목적 2.검색DB·전략 3.포함·제외기준 4.PRISMA 작성법 5.RoB 방법 6.중복처리 7.통계분석 8.Results/Discussion 구성."));

kids.push(h("첨부 파일 목록 (교수님께 함께 전달)", HeadingLevel.HEADING_2));
kids.push(p("본문용: Table1_main.md (Table 1: 인종군별 IRR + RoB + GRADE) · Fig_PRISMA.png · Fig_forest_AANHPI.png · Fig_forest_overview.png", { size: 18 }));
kids.push(p("Supplementary: S1 검색식(SEARCH_STRINGS_v2, SEARCH_LOG) · S3/S4 포함·제외(TableS_included/excluded) · S5 registry중복(TableSA_main_representatives) · S6 provenance(DERIVATIONS) · S7 RoB(TableS_risk_of_bias) · S-GRADE(TableS_GRADE) · S8 이질성(Table_sensitivity_I2, Table_method_comparison) · S9 민감도(Sensitivity1/2)", { size: 18 }));
kids.push(p("선생님 확인·작성 필요: RoB·GRADE 몇 개 검수 · PROSPERO 등록 · 본문 재작성 · 총평 8항목 요약", { size: 18, bold: true }));

const doc = new Document({
  styles: { default: { document: { run: { font: FONT, size: 20 } } } },
  sections: [{
    properties: { page: { size: { width: 12240, height: 15840 }, margin: { top: 1080, bottom: 1080, left: 1080, right: 1080 } } },
    children: kids,
  }],
});
Packer.toBuffer(doc).then(b => { fs.writeFileSync("FEEDBACK_RESPONSE.docx", b); console.log("wrote FEEDBACK_RESPONSE.docx"); });
