// Render outputs/Manuscript_full.md to Manuscript_Full.docx.
// Minimal Markdown: '# ' title, '## ' H1, '### ' H2, '**bold**' inline,
// numbered reference lines as their own paragraphs, blank line = paragraph break.
const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType,
} = require("docx");

const FONT = "Times New Roman";
const SRC = process.argv[2];
const OUTDOCX = process.argv[3];

// split a line into runs honouring **bold**
function runs(text, base = {}) {
  const out = [];
  const parts = text.split(/(\*\*[^*]+\*\*)/);
  for (const p of parts) {
    if (!p) continue;
    const bold = p.startsWith("**") && p.endsWith("**");
    out.push(new TextRun({ text: bold ? p.slice(2, -2) : p, bold: bold || base.bold,
      font: FONT, size: base.size || 24 }));
  }
  return out;
}

function para(text, opts = {}) {
  return new Paragraph({
    children: runs(text, opts),
    spacing: { after: opts.after ?? 160, line: opts.line ?? 360 },
    alignment: opts.align,
    heading: opts.heading,
    keepNext: opts.keepNext,
  });
}

function build() {
  const raw = fs.readFileSync(SRC, "utf8").split("\n");
  const blocks = [];
  let buf = [];
  const flush = () => {
    if (buf.length) { blocks.push(para(buf.join(" "))); buf = []; }
  };
  for (const line of raw) {
    const l = line.replace(/\s+$/, "");
    if (l.trim() === "") { flush(); continue; }
    if (l.startsWith("# ")) {                       // title
      flush();
      blocks.push(para(l.slice(2), { bold: true, size: 32,
        align: AlignmentType.CENTER, after: 300, keepNext: true }));
    } else if (l.startsWith("### ")) {              // H2 subsection
      flush();
      blocks.push(para(l.slice(4), { bold: true, size: 24,
        heading: HeadingLevel.HEADING_2, after: 80, keepNext: true }));
    } else if (l.startsWith("## ")) {               // H1 section
      flush();
      blocks.push(para(l.slice(3), { bold: true, size: 28,
        heading: HeadingLevel.HEADING_1, after: 120, keepNext: true }));
    } else if (/^\d+\.\s/.test(l)) {                // a numbered reference
      flush();
      blocks.push(para(l, { after: 60, line: 300 }));
    } else {
      buf.push(l);
    }
  }
  flush();

  const doc = new Document({
    styles: { default: { document: { run: { font: FONT, size: 24 } } } },
    sections: [{
      properties: { page: { margin: { top: 1440, bottom: 1440, left: 1440, right: 1440 } } },
      children: blocks,
    }],
  });
  Packer.toBuffer(doc).then((b) => {
    fs.writeFileSync(OUTDOCX, b);
    console.log("wrote Manuscript_Full.docx (%d blocks)", blocks.length);
  });
}

build();
