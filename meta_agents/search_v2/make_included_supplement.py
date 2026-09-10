#!/usr/bin/env python3
"""Compile the PRISMA supplementary "Characteristics of included studies" table
(the companion to the excluded-with-reasons table). Re-runnable — regenerates
from ft_eligibility.csv as the eligibility assessment progresses.

Included = ft_decision in {include-quant, include-narrative}. 'include-quant'
means the study contributed extractable NHW-referenced rates/IRRs to quantitative
synthesis; 'include-narrative' means eligible but synthesized narratively.

Outputs:
  TableS_included_studies.csv   (machine-readable)
  TableS_included_studies.md    (manuscript-ready supplementary table)
"""
import csv
import os
import re


def norm_groups(s):
    """Standardize umbrella shorthand in the free-text 'groups vs NHW' coverage note
    to match the analysis labels: API -> AANHPI, AIAN -> AI/AN (word-boundary)."""
    s = re.sub(r"\bAPI\b", "AANHPI", s)
    s = re.sub(r"\bAIAN\b", "AI/AN", s)
    return s

HERE = os.path.dirname(os.path.abspath(__file__))
MERGED = os.path.join(HERE, "merged_unique.csv")
ELIG = os.path.join(HERE, "ft_eligibility.csv")
OUT_CSV = os.path.join(HERE, "TableS_included_studies.csv")
OUT_MD = os.path.join(HERE, "TableS_included_studies.md")


def study_design(data_source, title):
    s = (data_source + " " + title).lower()
    if any(k in s for k in ("multiethnic cohort", "mec ", "nih-aarp", "aarp", "kaiser",
                            "black women's health", "nurses' health", "cohort study",
                            "prospective cohort", "women's health initiative", "whi ")):
        return "Cohort study"
    if "case-control" in s or "case control" in s:
        return "Case-control study"
    # SEER / NAACCR / USCS / NPCR / state / IHS-linked / tribal registries and their
    # statistics reports are population-based registry (descriptive incidence) studies
    return "Population-based registry/incidence study"


import re as _re
_THEME = [
    ("Nativity & immigrant generation",
     _re.compile(r"nativity|immigrant|foreign-born|us-born|generation|enclave|acculturat", _re.I)),
    ("Molecular subtype & histology",
     _re.compile(r"subtype|receptor|\bER[-+ ]|HER2|triple|molecular|lobular|ductal|inflammatory|luminal|histolog|in situ", _re.I)),
    ("Age & early-onset",
     _re.compile(r"young|early-onset|premenopaus|aged? \d|20-4|20-3|<\s?40|<\s?50|older wom|age-specific", _re.I)),
    ("Socioeconomic status & screening",
     _re.compile(r"poverty|socioeconomic|\bSES\b|insurance|screening|mammograph|deprivation|income|mortgage|segregation|redlining", _re.I)),
    ("Geography & region",
     _re.compile(r"region|county|rural|urban|\bstate\b|geograph|delta|appalach|neighborhood|spatial|hawaii|california|new york|florida|carolina|alaska|new mexico", _re.I)),
    ("Time trends",
     _re.compile(r"trend|annual|joinpoint|over time|temporal|\bAPC\b|declin|increas|changing|rising|no longer declining|update", _re.I)),
]


def narr_theme(title, groups, outcome):
    hay = " ".join([title or "", groups or "", outcome or ""])
    for name, rx in _THEME:
        if rx.search(hay):
            return name
    return "Other (subgroup-specific descriptive)"


def main():
    recs = list(csv.DictReader(open(MERGED, encoding="utf-8")))
    # record_ids that actually contributed extractable estimates to the master ledger
    LEDGER = os.path.join(HERE, "breast_extraction.csv")
    extractable_ids = {r["record_id"].strip()
                       for r in csv.DictReader(open(LEDGER, encoding="utf-8"))}
    out = []
    for r in csv.DictReader(open(ELIG, encoding="utf-8")):
        dec = r.get("ft_decision", "").strip()
        if dec not in ("include-quant", "include-narrative"):
            continue
        rid = int(r["record_id"])
        rec = recs[rid] if 0 <= rid < len(recs) else {}
        if dec == "include-quant":
            # quantitative-synthesis eligible: split those that yielded extractable
            # data (in the master ledger) from those eligible but without usable data
            extracted = str(rid) in extractable_ids
            synth_group = "quant-extracted" if extracted else "quant-eligible"
            synthesis = ("Quantitative (data extracted)" if extracted
                         else "Quantitative (eligible, no extractable data)")
        else:
            synth_group = "narrative"
            synthesis = "Narrative"
        theme = (narr_theme(rec.get("title", ""), r.get("groups_vs_nhw", ""),
                            r.get("rate_location", "")) if dec == "include-narrative" else "")
        out.append({
            "record_id": rid,
            "citation": "%s (%s)" % (rec.get("title", ""), rec.get("year", "")),
            "data_source": r.get("registry_family", "").strip(),
            "study_design": study_design(r.get("registry_family", ""), rec.get("title", "")),
            "groups_vs_nhw": norm_groups(r.get("groups_vs_nhw", "").strip()),
            "outcome_measure": r.get("rate_location", "").strip(),
            "synthesis": synthesis,
            "synth_group": synth_group,
            "narr_theme": theme,
            "note": r.get("note", "").strip(),
            "pmid": rec.get("pmid", ""),
            "doi": rec.get("doi", ""),
        })
    # group the rows so quantitative (extracted, then eligible-only) precede narrative,
    # and order the narrative rows by theme (professor's thematic synthesis grouping)
    grp_order = {"quant-extracted": 0, "quant-eligible": 1, "narrative": 2}
    theme_order = {name: i for i, (name, _) in enumerate(_THEME)}
    theme_order["Other (subgroup-specific descriptive)"] = len(_THEME)
    out.sort(key=lambda x: (grp_order[x["synth_group"]],
                            theme_order.get(x.get("narr_theme", ""), -1),
                            x["record_id"]))

    with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["record_id", "citation", "data_source",
                                          "study_design", "groups_vs_nhw", "outcome_measure",
                                          "synthesis", "synth_group", "narr_theme", "note", "pmid", "doi"])
        w.writeheader()
        w.writerows(out)

    from collections import Counter
    gc = Counter(x["synth_group"] for x in out)
    n_ext, n_elig, n_narr = gc["quant-extracted"], gc["quant-eligible"], gc["narrative"]
    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write("# Table S. Characteristics of included studies\n\n")
        f.write("Studies included after full-text review (PRISMA 2020). "
                "Total included: **%d** = quantitative-synthesis eligible **%d** "
                "(of which **%d** provided extractable data and **%d** were eligible but "
                "provided no extractable data) + narrative synthesis only **%d**.\n\n"
                % (len(out), n_ext + n_elig, n_ext, n_elig, n_narr))
        f.write("| # | Study (title, year) | Data source / registry | "
                "Racial/ethnic groups (vs NHW) | Outcome measure | Synthesis | "
                "PMID | DOI |\n")
        f.write("|---|---|---|---|---|---|---|---|\n")
        for i, x in enumerate(out, 1):
            f.write("| %d | %s | %s | %s | %s | %s | %s | %s |\n" % (
                i, x["citation"].replace("|", "/"), x["data_source"].replace("|", "/"),
                x["groups_vs_nhw"].replace("|", "/"), x["outcome_measure"].replace("|", "/"),
                x["synthesis"], x["pmid"], x["doi"]))

    print("included studies: %d (quant-extracted %d, quant-eligible %d, narrative %d)"
          % (len(out), n_ext, n_elig, n_narr))
    print("wrote %s and %s" % (os.path.basename(OUT_CSV), os.path.basename(OUT_MD)))


if __name__ == "__main__":
    main()
