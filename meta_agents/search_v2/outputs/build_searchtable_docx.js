const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  WidthType, ShadingType, BorderStyle, AlignmentType, PageOrientation } = require("docx");
const fs = require("fs");
const data = JSON.parse(fs.readFileSync("_searchtable.json", "utf8"));

const FONT = "Malgun Gothic", MONO = "Consolas";
const TW = 14400; // landscape US-letter usable width (DXA)
const W = [2600, 1100, 10700]; // DB | records | query  (sum = TW)
const border = { style: BorderStyle.SINGLE, size: 4, color: "BBBBBB" };
const borders = { top: border, bottom: border, left: border, right: border,
  insideHorizontal: border, insideVertical: border };

function cellText(runs, w, { shade = null, align = AlignmentType.LEFT } = {}) {
  return new TableCell({
    width: { size: w, type: WidthType.DXA },
    shading: shade ? { type: ShadingType.CLEAR, color: "auto", fill: shade } : undefined,
    margins: { top: 40, bottom: 40, left: 90, right: 90 },
    children: runs.map(r => new Paragraph({ alignment: align, children: [r] })),
  });
}
function tr(dbRuns, recRuns, queryLines) {
  const qParas = queryLines.map(l => new Paragraph({
    spacing: { after: 0, line: 200 },
    children: [new TextRun({ text: l === "" ? " " : l, font: MONO, size: 13 })],
  }));
  return new TableRow({ children: [
    new TableCell({ width: { size: W[0], type: WidthType.DXA }, margins: { top: 40, bottom: 40, left: 90, right: 90 }, children: dbRuns.map(r => new Paragraph({ children: [r] })) }),
    new TableCell({ width: { size: W[1], type: WidthType.DXA }, margins: { top: 40, bottom: 40, left: 90, right: 90 }, children: recRuns.map(r => new Paragraph({ alignment: AlignmentType.CENTER, children: [r] })) }),
    new TableCell({ width: { size: W[2], type: WidthType.DXA }, margins: { top: 40, bottom: 40, left: 90, right: 90 }, children: qParas }),
  ]});
}

const head = new TableRow({ tableHeader: true, children:
  ["Database (platform; search date)", "Records", "Search string"].map((h, i) =>
    cellText([new TextRun({ text: h, font: FONT, bold: true, size: 20 })], W[i],
      { shade: "E7EEF6", align: i === 1 ? AlignmentType.CENTER : AlignmentType.LEFT }))
});
const rows = [head];
for (const d of data) {
  rows.push(tr(
    [new TextRun({ text: d.db, font: FONT, bold: true, size: 20 }),
     new TextRun({ text: `${d.platform}`, font: FONT, size: 16, break: 1 }),
     new TextRun({ text: d.date, font: FONT, size: 16, break: 1 })],
    [new TextRun({ text: d.records, font: FONT, size: 20 })],
    d.query));
}
// summary rows
function sumRow(label, val, bold) {
  return new TableRow({ children: [
    cellText([new TextRun({ text: label, font: FONT, bold, size: 20 })], W[0]),
    cellText([new TextRun({ text: val, font: FONT, bold, size: 20 })], W[1], { align: AlignmentType.CENTER }),
    cellText([new TextRun({ text: "", font: FONT })], W[2]),
  ]});
}
rows.push(sumRow("Total records identified", "9,099", true));
rows.push(sumRow("Duplicate records removed (cross-database)", "4,306", false));
rows.push(sumRow("Unique records screened", "4,793", true));

const table = new Table({ columnWidths: W, width: { size: TW, type: WidthType.DXA }, borders, rows });

const doc = new Document({
  styles: { default: { document: { run: { font: FONT, size: 20 } } } },
  sections: [{
    properties: { page: { size: { width: 12240, height: 15840, orientation: PageOrientation.LANDSCAPE },
      margin: { top: 720, bottom: 720, left: 720, right: 720 } } },
    children: [
      new Paragraph({ spacing: { after: 80 }, children: [new TextRun({ text: "Supplementary Table 1. Final search strategy for each database", font: FONT, bold: true, size: 26 })] }),
      new Paragraph({ spacing: { after: 160 }, children: [new TextRun({ text: "Search conducted 7 August 2026. Concept blocks combined with AND: breast cancer × race/ethnicity × incidence/age-adjusted rate × United States. Limits: 2000–2026, English, human; document-type exclusions (review, letter, editorial, note, conference abstract).", font: FONT, size: 18, italics: true })] }),
      table,
    ],
  }],
});
Packer.toBuffer(doc).then(b => { fs.writeFileSync("S1_search_strategy_combined.docx", b); console.log("wrote S1_search_strategy_combined.docx"); });
