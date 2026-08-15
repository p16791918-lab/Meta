#!/usr/bin/env python3
"""Reader-facing display labels for racial/ethnic groups. The analysis ledger
keeps its internal group strings (used for clustering); these are applied only at
render time (figures/tables). Terminology follows the source studies: Sung 2026
uses 'Native Hawaiian and Pacific Islander' (NHPI); the older aggregate SEER
grouping is 'Asian and Pacific Islander (API)'."""

GROUP_DISPLAY = {
    "Asian/PI (aggregate)": "Asian and Pacific Islander (API)",
    "Native Hawaiian/PI (aggregate)": "Native Hawaiian and Pacific Islander (NHPI)",
}


def disp_group(g):
    return GROUP_DISPLAY.get(g, g)
