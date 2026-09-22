// Convert outputs/Feedback5_response.md to Feedback5_Response.docx (plain, black).
const fs = require("fs");
const path = require("path");
const { Document, Packer, Paragraph, TextRun } = require("docx");

const FONT = "Malgun Gothic";
const SRC = path.join(__dirname, "Feedback5_response.md");
const OUT = path.join(__dirname, "Feedback5_Response.docx");

// Split a text string into runs, bolding **...** spans; all text black.
function runs(text, base = {}) {
  const out = [];
  for (const part of text.split(/(\*\*[^*]+\*\*)/)) {
    if (!part) continue;
    const bold = part.startsWith("**") && part.endsWith("**");
    out.push(new TextRun({
      text: bold ? part.slice(2, -2) : part,
      bold: bold || !!base.bold,
      font: FONT,
      size: base.size || 20,
      color: "000000",
    }));
  }
  return out;
}

// Parse markdown into logical blocks, joining wrapped continuation lines.
function parseBlocks(md) {
  const blocks = [];
  let cur = null;
  const flush = () => { if (cur) { blocks.push(cur); cur = null; } };
  for (const raw of md.split("\n")) {
    const line = raw.replace(/\s+$/, "");
    if (line.trim() === "") { flush(); continue; }
    if (line.startsWith("## ")) { flush(); blocks.push({ type: "h2", text: line.slice(3) }); continue; }
    if (line.startsWith("# ")) { flush(); blocks.push({ type: "h1", text: line.slice(2) }); continue; }
    if (line.trim() === "---") { flush(); continue; }
    if (line.startsWith("- ")) { flush(); cur = { type: "bullet", text: line.slice(2) }; continue; }
    if (/^\s/.test(raw) && cur) { cur.text += " " + line.trim(); continue; }   // wrapped continuation
    if (cur && cur.type === "para") { cur.text += " " + line.trim(); continue; }
    flush(); cur = { type: "para", text: line };
  }
  flush();
  return blocks;
}

function render(blocks) {
  const kids = [];
  for (const b of blocks) {
    if (b.type === "h1") {
      kids.push(new Paragraph({ children: runs(b.text, { bold: true, size: 30 }),
        spacing: { before: 200, after: 160 } }));
    } else if (b.type === "h2") {
      kids.push(new Paragraph({ children: runs(b.text, { bold: true, size: 24 }),
        spacing: { before: 260, after: 120 } }));
    } else if (b.type === "bullet") {
      kids.push(new Paragraph({ children: runs(b.text), bullet: { level: 0 },
        spacing: { after: 80, line: 276 } }));
    } else {
      kids.push(new Paragraph({ children: runs(b.text),
        spacing: { after: 120, line: 276 } }));
    }
  }
  return kids;
}

const md = fs.readFileSync(SRC, "utf8");
const doc = new Document({ sections: [{ children: render(parseBlocks(md)) }] });
Packer.toBuffer(doc).then((buf) => {
  fs.writeFileSync(OUT, buf);
  console.log("wrote Feedback5_Response.docx");
});
