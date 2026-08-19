#!/usr/bin/env python3
"""Reader-facing display labels for racial/ethnic groups. The analysis ledger keeps
its internal group strings (used for clustering); these are applied only at render
time (figures/tables). Terminology is unified to current standard umbrellas:

  - Asian + Pacific Islander combined -> "Asian American, Native Hawaiian, and
    Pacific Islander (AANHPI)" (older registry sources term the same population
    "Asian/Pacific Islander (API)"; Gomez 2026 uses AANHPI).
  - the Pacific-Islander subset -> "Native Hawaiian and Pacific Islander (NHPI)".
  - "Black" -> "non-Hispanic Black (NHB)", parallel to the non-Hispanic White (NHW)
    comparator. A few older sources did not stratify by Hispanic origin (comparator
    shown as "White"); those cells are flagged in the ledger's comparison field and
    in Supplementary Note 1.
"""

GROUP_DISPLAY = {
    "Asian/PI (aggregate)": "Asian American, Native Hawaiian, and Pacific Islander (AANHPI)",
    "Native Hawaiian/PI (aggregate)": "Native Hawaiian and Pacific Islander (NHPI)",
    "Black": "non-Hispanic Black (NHB)",
    # AI/AN keeps the standard umbrella (no "non-Hispanic" prefix): the headline
    # representative is IHS-linked, defined by tribal/IHS enrollment, and the salient
    # issue is undercount correction rather than Hispanic-origin stratification.
    "AIAN": "American Indian and Alaska Native (AI/AN)",
    # unify the feminine ethnonym across sources (some registries record "Filipino"
    # for the same female population labelled "Filipina" elsewhere).
    "Filipino": "Filipina",
}


def disp_group(g):
    if g in GROUP_DISPLAY:
        return GROUP_DISPLAY[g]
    if g.startswith("AIAN ("):          # region subgroups: "AIAN (Navajo)" -> "AI/AN (Navajo)"
        return "AI/AN " + g[len("AIAN "):]
    return g


# Reader-facing labels for the internal analytic-dimension keys (the "Dimension"
# column of the GRADE / heterogeneity / sensitivity tables).
DIM_DISPLAY = {
    "aggregate-vs-NHW": "Overall (aggregate)",
    "disaggregated-AANHPI": "AANHPI subgroup",
    "Hispanic-origin": "Hispanic by origin",
    "AIAN": "AI/AN by region",
    "disaggregated-MENA": "Middle Eastern",
    "subtype-TNBC": "TNBC",
    "subtype-HRpos": "HR+",
    "subtype-HRneg": "HR−",
    "subtype-HRpos-HER2neg": "HR+/HER2−",
    "subtype-HRpos-HER2pos": "HR+/HER2+",
    "subtype-HRneg-HER2pos": "HR−/HER2+",
    "subtype-ERpos-PRneg": "ER+/PR−",
    "subtype-ERneg-PRpos": "ER−/PR+",
    "age-lt40": "Age <40", "age-ge40": "Age ≥40",
    "age-lt50": "Age <50", "age-ge50": "Age ≥50",
    "male-BC": "Male BC",
    "male-BC-TNBC": "Male BC, TNBC",
    "male-BC-HRpos-HER2neg": "Male BC, HR+/HER2−",
    "male-BC-HRpos-HER2pos": "Male BC, HR+/HER2+",
    "male-BC-HRneg-HER2pos": "Male BC, HR−/HER2+",
    "nativity": "By nativity",
}


def disp_dim(d):
    return DIM_DISPLAY.get(d, d)


# Faithful display of the comparator (reference group) actually used by each source.
# We do NOT relabel a plain-White comparator as NHW: studies that stratified the
# reference by Hispanic origin are shown as non-Hispanic White; those that used an
# unstratified White reference are shown as "White (not NH-stratified)". This keeps
# the terminology faithful to each original study (per the supervisor's feedback),
# rather than smoothing every reference to NHW.
_NHW_SRC = {"NHW", "White (NH)", "NHW (external SEER-Explorer)"}


def disp_comparator(cv):
    cv = (cv or "").strip()
    if cv in _NHW_SRC:
        return "non-Hispanic White (NHW)"
    if cv.startswith("foreign-born"):
        return cv  # nativity contrast, not a White reference
    low = cv.lower()
    if "men" in low:
        return "White men (not NH-stratified)"
    if "white" in low:
        return "White (not NH-stratified)"
    return cv or "non-Hispanic White (NHW)"
