"""
Convert manuscript.md → manuscript.pdf using WeasyPrint
"""
import markdown
import re
from pathlib import Path
from weasyprint import HTML, CSS

MD_PATH   = Path("output_20260417_093053/manuscript.md")
PDF_PATH  = Path("output_20260417_093053/manuscript.pdf")
IMG_DIR   = Path("output_20260417_093053")

# ── 1. Read markdown ──────────────────────────────────────────────────────────
md_text = MD_PATH.read_text(encoding="utf-8")

# ── 1b. Inject figures into markdown before Figure Legends section ───────────
FIGURES_HTML = """

---

## Figures

**Figure 1. PRISMA 2020 Flow Diagram**

*Records identified from Embase (2000–2025): n = 107. After duplicate removal: n = 43. Phase 1 exclusions (title/abstract): n = 15. Full-text assessed: n = 28. Phase 2 exclusions: n = 14. Included in qualitative synthesis: n = 14; quantitative meta-analysis: n = 13.*

<img src="output_20260417_093053/figure1_prisma.png"
     alt="PRISMA 2020 flow diagram" style="width:72%; margin:1em auto; display:block;">

---

**Figure 2. Risk of Bias Assessment — Newcastle-Ottawa Scale (NOS)**

*Nine NOS domains assessed across 14 included studies. Green = low risk; yellow = moderate risk. Eight studies (57.1%) rated low risk (NOS ≥ 7); six (42.9%) rated moderate risk (NOS 4–6). No studies rated high or critical risk.*

<img src="output_20260417_093053/figure2_rob.png"
     alt="Risk of Bias NOS summary" style="width:100%; margin:1em 0;">

---

**Figure 3. Forest Plot: Melanoma Incidence Rate Ratios by Race/Ethnicity**

*(A) Black/African American, (B) Hispanic/Latino, (C) Asian/Pacific Islander, (D) American Indian/Alaska Native vs. Non-Hispanic White. Random-effects model (DerSimonian-Laird). I² = 0% for all comparisons. Squares proportional to study weight; diamond = pooled estimate with 95% CI; dashed line = null (IRR = 1).*

<img src="output_20260417_093053/forest_plot_combined.png"
     alt="Forest plot — combined four-panel" style="width:100%; margin:1em 0;">

---

**Figure 4. Subgroup — Acral Lentiginous Melanoma Incidence**

*ALM incidence rate ratios for Black and Asian/Pacific Islander vs. Non-Hispanic White (Holman 2023, SEER 2010–2019). Pooled IRR = 0.766 (95% CI: 0.517–1.134; p = 0.183), in contrast to overall melanoma IRRs of 0.052–0.150, supporting UV-independent pathogenesis.*

<img src="output_20260417_093053/forest_alm.png"
     alt="Forest plot — ALM incidence" style="width:85%; margin:1em 0;">

---

**Figure 5. Melanoma Survival — Black vs. Non-Hispanic White (Hazard Ratio)**

*Adjusted HR for overall survival (Lam 2022: 1.42, 95% CI 1.25–1.60), melanoma-specific survival (Lam 2022: 1.27, 95% CI 1.03–1.56), and all-cause death (Zell 2008: 1.60, 95% CI 1.17–2.18). HR > 1.0 = worse survival in Black patients despite lower absolute incidence.*

<img src="output_20260417_093053/forest_survival_black.png"
     alt="Forest plot — survival Black vs NHW" style="width:85%; margin:1em 0;">

---

**Figure 6. Summary Dot-and-Whisker Plot — Pooled IRRs by Race/Ethnicity**

*Pooled incidence rate ratios with 95% confidence intervals on a log scale. All comparisons significant at p < 0.001 except ALM (p = 0.183).*

<img src="output_20260417_093053/irr_summary_ggplot.png"
     alt="IRR summary ggplot" style="width:90%; margin:1em 0;">

---

**Figure 7. Funnel Plot — Black/African American vs. NHW (Melanoma Incidence)**

*Four contributing studies plotted as log(IRR) against standard error. No overt asymmetry; formal Egger's test was not performed due to k < 10.*

<img src="output_20260417_093053/funnel_plot.png"
     alt="Funnel plot" style="width:70%; margin:1em 0;">

"""

# Insert figures block before "## Figure Legends"
if "## Figure Legends" in md_text:
    md_text = md_text.replace("## Figure Legends", FIGURES_HTML + "\n## Figure Legends")
else:
    md_text += FIGURES_HTML

# ── 2. Convert to HTML ────────────────────────────────────────────────────────
md_engine = markdown.Markdown(extensions=["tables", "fenced_code", "nl2br"])
body_html  = md_engine.convert(md_text)

# ── 3. Wrap in full HTML document with academic CSS ───────────────────────────
html_doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Racial and Ethnic Disparities in Skin Cancer</title>
</head>
<body>
{body_html}
</body>
</html>"""

# ── 4. Academic stylesheet ────────────────────────────────────────────────────
CSS_TEXT = """
@page {{
    size: A4;
    margin: 2.5cm 2.2cm 2.5cm 2.2cm;
    @top-center {{
        content: "Racial/Ethnic Disparities in Skin Cancer — Systematic Review and Meta-Analysis";
        font-size: 8pt;
        color: #555;
    }}
    @bottom-center {{
        content: counter(page);
        font-size: 9pt;
    }}
}}

/* Reset */
* {{ box-sizing: border-box; margin: 0; padding: 0; }}

body {{
    font-family: "Times New Roman", Times, serif;
    font-size: 11pt;
    line-height: 1.6;
    color: #111;
    text-align: justify;
    hyphens: auto;
}}

/* ── Title block ── */
h1 {{
    font-size: 16pt;
    font-weight: bold;
    text-align: center;
    line-height: 1.3;
    margin-bottom: 0.5em;
    page-break-after: avoid;
}}

/* Author / affiliation lines just below title */
h1 + p, h1 + p + p, h1 + p + p + p, h1 + p + p + p + p,
h1 + p + p + p + p + p, h1 + p + p + p + p + p + p {{
    text-align: center;
    font-size: 10pt;
    margin-bottom: 0.2em;
}}

/* ── Headings ── */
h2 {{
    font-size: 13pt;
    font-weight: bold;
    margin-top: 1.4em;
    margin-bottom: 0.4em;
    border-bottom: 1.5px solid #333;
    padding-bottom: 2px;
    page-break-after: avoid;
}}

h3 {{
    font-size: 11.5pt;
    font-weight: bold;
    margin-top: 1.1em;
    margin-bottom: 0.3em;
    page-break-after: avoid;
}}

h4 {{
    font-size: 11pt;
    font-weight: bold;
    font-style: italic;
    margin-top: 0.9em;
    margin-bottom: 0.2em;
    page-break-after: avoid;
}}

/* ── Paragraphs ── */
p {{
    margin-bottom: 0.55em;
    orphans: 3;
    widows: 3;
}}

/* ── Abstract box ── */
h2:first-of-type + p,
section.abstract p {{
    background: #f8f8f8;
    border-left: 3px solid #2a6099;
    padding: 6px 10px;
    margin-bottom: 0.4em;
    font-size: 10.5pt;
}}

/* ── Tables ── */
table {{
    width: 100%;
    border-collapse: collapse;
    margin: 1em 0 1.2em 0;
    font-size: 9pt;
    page-break-inside: avoid;
}}

thead tr {{
    background-color: #2a6099;
    color: white;
}}

th, td {{
    border: 1px solid #aaa;
    padding: 5px 7px;
    text-align: left;
    vertical-align: top;
}}

tbody tr:nth-child(even) {{
    background-color: #f4f4f4;
}}

/* ── Code blocks (search strings) ── */
pre, code {{
    font-family: "Courier New", Courier, monospace;
    font-size: 8.5pt;
    background: #f0f0f0;
    border: 1px solid #ddd;
    border-radius: 3px;
}}

pre {{
    padding: 8px 10px;
    white-space: pre-wrap;
    word-break: break-all;
    margin: 0.7em 0;
}}

code {{ padding: 1px 4px; }}

/* ── Horizontal rules ── */
hr {{
    border: none;
    border-top: 1px solid #999;
    margin: 1.2em 0;
}}

/* ── Blockquotes (notes / word counts) ── */
blockquote {{
    border-left: 3px solid #ccc;
    padding: 4px 10px;
    color: #555;
    font-size: 9.5pt;
    margin: 0.6em 0;
}}

/* ── Lists ── */
ul, ol {{
    margin: 0.4em 0 0.4em 1.5em;
}}

li {{
    margin-bottom: 0.2em;
}}

/* ── Bold labels in abstract ── */
strong {{ font-weight: bold; }}

/* ── References (numbered list) ── */
ol li {{
    font-size: 10pt;
    line-height: 1.5;
}}

/* ── Force page break before certain sections ── */
h2[id*="references"],
h2[id*="supplementary"] {{
    page-break-before: always;
}}
"""

print("Converting markdown → HTML …")
print("Rendering PDF (this may take ~30 seconds) …")

HTML(string=html_doc, base_url=str(Path(".").resolve())).write_pdf(
    str(PDF_PATH),
    stylesheets=[CSS(string=CSS_TEXT)],
)

size_kb = PDF_PATH.stat().st_size // 1024
print(f"✓  Saved → {PDF_PATH}  ({size_kb} KB)")
