// Render outputs/Manuscript_full.md to Manuscript_Full.docx, then append the
// main-text Table 1 and Figures 1-3 (from _maintext_manifest.json) in a second,
// landscape section, so the file is a complete manuscript with its display items.
const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType,
  Table, TableRow, TableCell, WidthType, ShadingType, BorderStyle, ImageRun,
  PageOrientation,
} = require("docx");

const FONT = "Times New Roman";
const SRC = path.join(__dirname, "Manuscript_full.md");
const MANIFEST = path.join(__dirname, "_maintext_manifest.json");
const OUTDOCX = path.join(__dirname, "Manuscript_Full.docx");

// ---- text (markdown) rendering ------------------------------------------------
function runs(text, base = {}) {
  const out = [];
  for (const p of text.split(/(\*\*[^*]+\*\*)/)) {
    if (!p) continue;
    const bold = p.startsWith("**") && p.endsWith("**");
    out.push(new TextRun({ text: bold ? p.slice(2, -2) : p, bold: bold || base.bold,
      italics: base.italics, font: FONT, size: base.size || 24 }));
  }
  return out;
}
function para(text, opts = {}) {
  return new Paragraph({ children: runs(text, opts),
    spacing: { after: opts.after ?? 160, line: opts.line ?? 360 },
    alignment: opts.align, heading: opts.heading, keepNext: opts.keepNext });
}
function textBlocks() {
  const raw = fs.readFileSync(SRC, "utf8").split("\n");
  const blocks = []; let buf = [];
  const flush = () => { if (buf.length) { blocks.push(para(buf.join(" "))); buf = []; } };
  for (const line of raw) {
    const l = line.replace(/\s+$/, "");
    if (l.trim() === "") { flush(); continue; }
    if (l.startsWith("# ")) { flush(); blocks.push(para(l.slice(2), { bold: true, size: 32, align: AlignmentType.CENTER, after: 300, keepNext: true })); }
    else if (l.startsWith("### ")) { flush(); blocks.push(para(l.slice(4), { bold: true, size: 24, heading: HeadingLevel.HEADING_2, after: 80, keepNext: true })); }
    else if (l.startsWith("## ")) { flush(); blocks.push(para(l.slice(3), { bold: true, size: 28, heading: HeadingLevel.HEADING_1, after: 120, keepNext: true })); }
    else if (/^\d+\.\s/.test(l)) { flush(); blocks.push(para(l, { after: 60, line: 300 })); }
    else buf.push(l);
  }
  flush();
  return blocks;
}

// ---- main-text tables/figures (manifest) rendering ---------------------------
const LFONT = "Malgun Gothic";
const PAGEW = 14400;
const bd = { style: BorderStyle.SINGLE, size: 3, color: "BBBBBB" };
const borders = { top: bd, bottom: bd, left: bd, right: bd, insideHorizontal: bd, insideVertical: bd };
function scaleWidths(ws) { const s = ws.reduce((a, b) => a + b, 0); const f = PAGEW / s; return ws.map(w => Math.round(w * f)); }
function tcell(text, w, { bold = false, shade = null } = {}) {
  return new TableCell({ width: { size: w, type: WidthType.DXA },
    shading: shade ? { type: ShadingType.CLEAR, color: "auto", fill: shade } : undefined,
    margins: { top: 25, bottom: 25, left: 70, right: 70 },
    children: [new Paragraph({ children: [new TextRun({ text: String(text), font: LFONT, size: 15, bold })] })] });
}
function buildTable(m) {
  const ws = scaleWidths(m.widths); const total = ws.reduce((a, b) => a + b, 0);
  const head = new TableRow({ tableHeader: true, children: m.headers.map((h, i) => tcell(h, ws[i], { bold: true, shade: "E7EEF6" })) });
  const body = m.rows.map(r => {
    if (r && !Array.isArray(r) && r.section !== undefined) {
      return new TableRow({ children: [new TableCell({ width: { size: total, type: WidthType.DXA }, columnSpan: ws.length,
        shading: { type: ShadingType.CLEAR, color: "auto", fill: "D9E2EF" }, margins: { top: 30, bottom: 30, left: 70, right: 70 },
        children: [new Paragraph({ children: [new TextRun({ text: String(r.section), font: LFONT, size: 16, bold: true })] })] })] });
    }
    return new TableRow({ children: r.map((c, i) => tcell(c, ws[i])) });
  });
  return new Table({ columnWidths: ws, width: { size: PAGEW, type: WidthType.DXA }, borders, rows: [head, ...body] });
}
function figureBlocks() {
  const M = JSON.parse(fs.readFileSync(MANIFEST, "utf8"));
  const out = [para("Tables and Figures", { bold: true, size: 28, heading: HeadingLevel.HEADING_1, after: 160 })];
  for (const m of M) {
    if (m.type === "heading") out.push(new Paragraph({ children: [new TextRun({ text: m.text, font: LFONT, size: 22, bold: true })], spacing: { before: 160, after: 100 } }));
    else if (m.type === "para") out.push(new Paragraph({ children: [new TextRun({ text: m.text, font: LFONT, size: 16, italics: !!m.italic })], spacing: { after: 120, line: 260 } }));
    else if (m.type === "table") out.push(buildTable(m));
    else if (m.type === "image") { const buf = fs.readFileSync(m.path); out.push(new Paragraph({ children: [new ImageRun({ type: "png", data: buf, transformation: { width: m.w, height: m.h } })] })); }
    // ignore pagebreak markers; the section flows continuously
  }
  return out;
}

const doc = new Document({
  styles: { default: { document: { run: { font: FONT, size: 24 } } } },
  sections: [
    { properties: { page: { margin: { top: 1440, bottom: 1440, left: 1440, right: 1440 } } }, children: textBlocks() },
    { properties: { page: { size: { orientation: PageOrientation.LANDSCAPE }, margin: { top: 1080, bottom: 1080, left: 1080, right: 1080 } } }, children: figureBlocks() },
  ],
});
Packer.toBuffer(doc).then(b => { fs.writeFileSync(OUTDOCX, b); console.log("wrote Manuscript_Full.docx (text + Table 1 + Figures 1-3)"); });
