#!/usr/bin/env python3
"""Assemble the five section drafts + unified reference list into one clean
manuscript markdown (outputs/Manuscript_full.md), dropping all drafting
scaffolding (top notes, per-file reference notes, the Introduction reference
table, and the PMID import block). build_manuscript_docx.js renders it to Word.
"""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
M = os.path.join(HERE, "manuscript")
OUT = os.path.join(HERE, "outputs", "Manuscript_full.md")

TITLE = ("Racial and Ethnic Differences in Breast Cancer Incidence in the "
         "United States: A Systematic Review and Meta-analysis")


def body_after_rule(fn):
    """Return the lines after the first horizontal rule (---)."""
    lines = open(os.path.join(M, fn), encoding="utf-8").read().split("\n")
    for i, l in enumerate(lines):
        if l.strip() == "---":
            return lines[i + 1:]
    return lines


def section(fn, heading, stop_at=("---", "## References")):
    """Extract the manuscript section: from its '## <heading>' line up to the
    next horizontal rule or a '## References' scaffolding block."""
    lines = body_after_rule(fn)
    out, capturing = [], False
    for l in lines:
        if l.startswith("## ") and heading.lower() in l.lower():
            capturing = True
            out.append(l)
            continue
        if capturing:
            if l.strip() in ("---",) or l.startswith("## References"):
                break
            out.append(l)
    return "\n".join(out).strip()


def abstract_body():
    # Abstract has no '## ' heading; body is everything after the rule.
    return "\n".join(body_after_rule("Abstract_draft.md")).strip()


def references():
    """Pull the numbered reference sections from References_draft.md, dropping the
    top note and the PMID import block."""
    lines = open(os.path.join(M, "References_draft.md"), encoding="utf-8").read().split("\n")
    out = ["## References", ""]
    for l in lines:
        if l.startswith("## PMID"):
            break
        if re.match(r"^\d+\.\s", l):          # a numbered reference entry
            out.append(l)
    return "\n".join(out).strip()


def main():
    parts = []
    parts.append("# " + TITLE)
    parts.append("")
    parts.append("## Abstract")
    parts.append("")
    parts.append(abstract_body())
    parts.append("")
    parts.append(section("Introduction_draft.md", "Introduction"))
    parts.append("")
    parts.append(section("Methods_draft.md", "Methods"))
    parts.append("")
    parts.append(section("Results_draft.md", "Results"))
    parts.append("")
    parts.append(section("Discussion_draft.md", "Discussion"))
    parts.append("")
    parts.append(references())
    parts.append("")

    text = "\n".join(parts)
    # normalise 3+ blank lines to 1
    text = re.sub(r"\n{3,}", "\n\n", text)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(text)

    from collections import Counter
    c = Counter(l[:3] for l in text.split("\n") if l.startswith("#"))
    print("wrote", os.path.relpath(OUT, HERE))
    print("headings:", dict(c), "| total lines:", len(text.split("\n")))


if __name__ == "__main__":
    main()
