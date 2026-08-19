const { Document, Packer, Paragraph, TextRun, HeadingLevel, PageBreak,
  Table, TableRow, TableCell, WidthType, ShadingType, BorderStyle,
  AlignmentType, PageOrientation, ImageRun } = require("docx");
const fs = require("fs");
const M = JSON.parse(fs.readFileSync("_suppl_manifest.json", "utf8"));

const FONT = "Malgun Gothic", MONO = "Consolas";
const PAGEW = 14400; // landscape usable width (DXA)
const border = { style: BorderStyle.SINGLE, size: 3, color: "BBBBBB" };
const borders = { top: border, bottom: border, left: border, right: border,
  insideHorizontal: border, insideVertical: border };

function scaleWidths(ws) {
  const s = ws.reduce((a, b) => a + b, 0);
  const f = PAGEW / s;
  return ws.map(w => Math.round(w * f));
}
function tcell(text, w, { bold = false, shade = null } = {}) {
  return new TableCell({
    width: { size: w, type: WidthType.DXA },
    shading: shade ? { type: ShadingType.CLEAR, color: "auto", fill: shade } : undefined,
    margins: { top: 25, bottom: 25, left: 70, right: 70 },
    children: [new Paragraph({ children: [new TextRun({ text: String(text), font: FONT, size: 15, bold })] })],
  });
}
function buildTable(m) {
  const ws = scaleWidths(m.widths);
  const total = ws.reduce((a, b) => a + b, 0);
  const head = new TableRow({ tableHeader: true,
    children: m.headers.map((h, i) => tcell(h, ws[i], { bold: true, shade: "E7EEF6" })) });
  const body = m.rows.map(r => {
    // A row shaped {section: "..."} is a full-width section header spanning all columns.
    if (r && !Array.isArray(r) && r.section !== undefined) {
      return new TableRow({ children: [new TableCell({
        width: { size: total, type: WidthType.DXA }, columnSpan: ws.length,
        shading: { type: ShadingType.CLEAR, color: "auto", fill: "D9E2EF" },
        margins: { top: 30, bottom: 30, left: 70, right: 70 },
        children: [new Paragraph({ children: [new TextRun({ text: String(r.section), font: FONT, size: 15, bold: true })] })],
      })] });
    }
    return new TableRow({ children: r.map((c, i) => tcell(c, ws[i])) });
  });
  return new Table({ columnWidths: ws, width: { size: PAGEW, type: WidthType.DXA },
    borders, rows: [head, ...body] });
}

// grouped-header table (e.g., Newcastle-Ottawa: Selection/Comparability/Outcome)
function buildGTable(m) {
  const ws = scaleWidths(m.widths);
  const r1 = [];
  let ci = 0;
  for (const g of m.groups) {
    const [label, span, rspan] = g;
    const w = ws.slice(ci, ci + span).reduce((a, b) => a + b, 0);
    r1.push(new TableCell({
      width: { size: w, type: WidthType.DXA },
      columnSpan: span > 1 ? span : undefined,
      rowSpan: rspan ? 2 : undefined,
      shading: { type: ShadingType.CLEAR, color: "auto", fill: "E7EEF6" },
      verticalAlign: "center",
      margins: { top: 25, bottom: 25, left: 70, right: 70 },
      children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: label, font: FONT, size: 15, bold: true })] })],
    }));
    ci += span;
  }
  const r2 = [];
  m.subs.forEach((s, i) => {
    if (s === null) return; // covered by a rowSpan cell above
    r2.push(new TableCell({
      width: { size: ws[i], type: WidthType.DXA },
      shading: { type: ShadingType.CLEAR, color: "auto", fill: "E7EEF6" },
      margins: { top: 25, bottom: 25, left: 50, right: 50 },
      children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: s, font: FONT, size: 14, bold: true })] })],
    }));
  });
  const body = m.rows.map(r => new TableRow({ children: r.map((c, i) =>
    new TableCell({ width: { size: ws[i], type: WidthType.DXA }, margins: { top: 25, bottom: 25, left: 50, right: 50 },
      children: [new Paragraph({ alignment: i === 0 ? AlignmentType.LEFT : AlignmentType.CENTER, children: [new TextRun({ text: String(c), font: FONT, size: 15 })] })] })) }));
  return new Table({ columnWidths: ws, width: { size: PAGEW, type: WidthType.DXA }, borders,
    rows: [new TableRow({ tableHeader: true, children: r1 }), new TableRow({ tableHeader: true, children: r2 }), ...body] });
}

// search-strategy table: metadata columns + a monospace query cell
function buildSTable(m) {
  const ws = scaleWidths(m.widths);
  const head = new TableRow({ tableHeader: true,
    children: ["Database", "Platform", "Date", "Records", "Search string"].map((h, i) => tcell(h, ws[i], { bold: true, shade: "E7EEF6" })) });
  const body = m.rows.map(r => new TableRow({ children: [
    tcell(r.db, ws[0]), tcell(r.platform, ws[1]), tcell(r.date, ws[2]), tcell(r.records, ws[3]),
    new TableCell({ width: { size: ws[4], type: WidthType.DXA }, margins: { top: 25, bottom: 25, left: 70, right: 70 },
      children: r.query.map(l => new Paragraph({ spacing: { after: 0, line: 180 }, children: [new TextRun({ text: l === "" ? " " : l, font: MONO, size: 12 })] })) }),
  ] }));
  return new Table({ columnWidths: ws, width: { size: PAGEW, type: WidthType.DXA }, borders, rows: [head, ...body] });
}

const mainKids = [];
mainKids.push(new Paragraph({ spacing: { after: 200 },
  children: [new TextRun({ text: "Supplementary Materials", font: FONT, bold: true, size: 34 })] }));
mainKids.push(new Paragraph({ spacing: { after: 200 },
  children: [new TextRun({ text: "Racial and Ethnic Differences in Breast Cancer Incidence in the United States: A Systematic Review and Meta-Analysis", font: FONT, italics: true, size: 20 })] }));

const figKids = [];
let inFigures = false;
for (const m of M) {
  if (m.type === "heading" && m.level === 1 && /Supplementary Figure/.test(m.text)) inFigures = true;
  const kids = inFigures ? figKids : mainKids;
  if (m.type === "heading") {
    kids.push(new Paragraph({ heading: m.level === 1 ? HeadingLevel.HEADING_1 : HeadingLevel.HEADING_2,
      spacing: { before: 200, after: 100 },
      children: [new TextRun({ text: m.text, font: FONT, bold: true, size: m.level === 1 ? 24 : 20 })] }));
  } else if (m.type === "para") {
    kids.push(new Paragraph({ spacing: { after: 80 },
      children: [new TextRun({ text: m.text, font: FONT, size: 18, italics: !!m.italic })] }));
  } else if (m.type === "code") {
    for (const line of m.lines) {
      kids.push(new Paragraph({ spacing: { after: 0, line: 190 },
        children: [new TextRun({ text: line === "" ? " " : line, font: MONO, size: 13 })] }));
    }
    kids.push(new Paragraph({ spacing: { after: 80 }, children: [] }));
  } else if (m.type === "table") {
    kids.push(buildTable(m));
    kids.push(new Paragraph({ spacing: { after: 80 }, children: [] }));
  } else if (m.type === "gtable") {
    kids.push(buildGTable(m));
    kids.push(new Paragraph({ spacing: { after: 80 }, children: [] }));
  } else if (m.type === "stable") {
    kids.push(buildSTable(m));
    kids.push(new Paragraph({ spacing: { after: 80 }, children: [] }));
  } else if (m.type === "image") {
    try {
      const buf = fs.readFileSync(m.path);
      kids.push(new Paragraph({ alignment: AlignmentType.CENTER,
        children: [new ImageRun({ type: "png", data: buf, transformation: { width: m.w, height: m.h } })] }));
    } catch (e) { kids.push(new Paragraph({ children: [new TextRun({ text: "[image missing: " + m.path + "]", font: FONT })] })); }
    kids.push(new Paragraph({ spacing: { after: 80 }, children: [] }));
  } else if (m.type === "pagebreak") {
    kids.push(new Paragraph({ children: [new PageBreak()] }));
  }
}

const doc = new Document({
  styles: { default: { document: { run: { font: FONT, size: 18 } } } },
  sections: [
    { // landscape: tables + notes
      properties: { page: { size: { width: 12240, height: 15840, orientation: PageOrientation.LANDSCAPE },
        margin: { top: 720, bottom: 720, left: 720, right: 720 } } },
      children: mainKids,
    },
    { // portrait: figures
      properties: { page: { size: { width: 12240, height: 15840 },
        margin: { top: 720, bottom: 720, left: 720, right: 720 } } },
      children: figKids,
    },
  ],
});
Packer.toBuffer(doc).then(b => { fs.writeFileSync("Supplementary_Materials.docx", b); console.log("wrote Supplementary_Materials.docx (" + (mainKids.length + figKids.length) + " blocks)"); });
