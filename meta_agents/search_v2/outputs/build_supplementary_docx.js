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
  const head = new TableRow({ tableHeader: true,
    children: m.headers.map((h, i) => tcell(h, ws[i], { bold: true, shade: "E7EEF6" })) });
  const body = m.rows.map(r => new TableRow({ children: r.map((c, i) => tcell(c, ws[i])) }));
  return new Table({ columnWidths: ws, width: { size: PAGEW, type: WidthType.DXA },
    borders, rows: [head, ...body] });
}

const kids = [];
kids.push(new Paragraph({ spacing: { after: 200 },
  children: [new TextRun({ text: "Supplementary Materials", font: FONT, bold: true, size: 34 })] }));
kids.push(new Paragraph({ spacing: { after: 200 },
  children: [new TextRun({ text: "Racial and Ethnic Differences in Breast Cancer Incidence in the United States: A Systematic Review and Meta-Analysis", font: FONT, italics: true, size: 20 })] }));

for (const m of M) {
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
  sections: [{
    properties: { page: { size: { width: 12240, height: 15840, orientation: PageOrientation.LANDSCAPE },
      margin: { top: 720, bottom: 720, left: 720, right: 720 } } },
    children: kids,
  }],
});
Packer.toBuffer(doc).then(b => { fs.writeFileSync("Supplementary_Materials.docx", b); console.log("wrote Supplementary_Materials.docx (" + kids.length + " blocks)"); });
