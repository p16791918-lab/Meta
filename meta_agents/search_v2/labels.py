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
}


def disp_group(g):
    return GROUP_DISPLAY.get(g, g)
