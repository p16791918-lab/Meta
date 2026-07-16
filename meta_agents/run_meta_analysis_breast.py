"""
Meta-Analysis: Racial/Ethnic Disparities in Breast Cancer INCIDENCE
===================================================================
Random-effects meta-analysis (DerSimonian-Laird) of the within-study
incidence rate ratio  IRR = (minority age-adjusted rate) / (NHW rate).

Scope (locked decisions):
  • Outcome        : INVASIVE breast cancer INCIDENCE only.
                     NOT prevalence (confounded by survival), NOT mortality,
                     NOT survival HRs. Never pool incidence with prevalence.
  • Rates          : age-standardized / age-adjusted, per 100,000 person-years.
  • Method A       : within-study IRR = minority_rate / nhw_rate (reference NHW).
                     Method B (cross-study rate pooling) is a fallback only if
                     the within-study pairs are too sparse — not used here yet.
  • Excluded       : male breast cancer, DCIS/in-situ-only, crude (non-adjusted)
                     rates, single-race studies with no NHW comparator.
  • Optional        : TNBC / ER-negative subtype as a separate stratum.

HOW THE DATA GETS IN
--------------------
Agent 3's automated extractor returns NULL for age-adjusted rate tables, so
the `STUDIES` list below is filled BY HAND from the full text of each INCLUDED
study (Claude reads methods/results and transcribes the rate table). Until that
extraction is done the list is empty and this script simply reports that it is
awaiting data — it does NOT invent numbers.

Each row is one minority-vs-NHW comparison from one study. A study that reports
Black, Hispanic, and Asian rates against the same NHW reference contributes
THREE rows (one per minority_group), all citing the same `id`.
"""

import math
import json
import os
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

OUTPUT_DIR = "output_breast"

# ─── Data model ──────────────────────────────────────────────────────────────

@dataclass
class Study:
    id: str              # first-author + year, e.g. "Smith2019"
    year: int
    source: str          # SEER, NPCR, state registry, etc.
    outcome: str         # invasive_incidence | tnbc_incidence  (incidence only)
    minority_group: str  # Black | Hispanic | Asian | AIAN
    log_irr: float       # log(minority age-adj rate / NHW age-adj rate)
    se: float            # standard error of log_irr
    minority_rate: Optional[float] = None   # per 100,000 person-years
    nhw_rate: Optional[float] = None         # per 100,000 person-years
    notes: str = ""

    @property
    def irr(self): return math.exp(self.log_irr)

    @property
    def ci_low(self): return math.exp(self.log_irr - 1.96 * self.se)

    @property
    def ci_high(self): return math.exp(self.log_irr + 1.96 * self.se)


# ─── SE helpers ──────────────────────────────────────────────────────────────

def se_from_rates(r_minority, r_nhw, py_minority=1_000_000, py_nhw=5_000_000):
    """
    Approximate SE of log(IRR) under a Poisson assumption when the paper gives
    rates but no CI:  SE ≈ sqrt(1/cases_minority + 1/cases_nhw), with
    cases = rate * person-years / 100,000.

    Use realistic person-years for the population/period if the paper reports
    them; the defaults are placeholders and will understate/overstate precision.
    """
    cases_m = max(r_minority * py_minority / 100_000, 1)
    cases_n = max(r_nhw * py_nhw / 100_000, 1)
    return math.sqrt(1 / cases_m + 1 / cases_n)


def se_from_ci(irr, ci_low, ci_high):
    """Back-calculate SE of log(IRR) from a published 95% CI (preferred)."""
    return (math.log(ci_high) - math.log(ci_low)) / (2 * 1.96)


def irr_from_rates(r_minority, r_nhw):
    """Convenience: log(IRR) from two rates."""
    return math.log(r_minority / r_nhw)


def se_logirr_from_rate_cis(r_m, lo_m, hi_m, r_n, lo_n, hi_n):
    """SE of log(IRR) when the paper gives a 95% CI for EACH rate (not the IRR).
    Treats the two age-standardized rates as independent:
       SE(log r) = (ln hi - ln lo) / (2*1.96);  SE(log IRR) = sqrt(SE_m^2 + SE_n^2).
    """
    se_m = (math.log(hi_m) - math.log(lo_m)) / (2 * 1.96)
    se_n = (math.log(hi_n) - math.log(lo_n)) / (2 * 1.96)
    return math.sqrt(se_m ** 2 + se_n ** 2)


# ─── Dataset — FILL FROM FULL-TEXT EXTRACTION ────────────────────────────────
# Populate one Study(...) per minority-vs-NHW comparison. Prefer se_from_ci when
# the paper reports a 95% CI for the rate ratio; fall back to se_from_rates only
# when just point rates (+ ideally person-years) are given.
#
# Template (delete the leading '#' and fill in real values):
#   Study("Author2021", 2021, "SEER", "invasive_incidence", "Black",
#         irr_from_rates(126.0, 133.0), se_from_ci(0.95, 0.93, 0.97),
#         minority_rate=126.0, nhw_rate=133.0, notes="SEER 2015-2019, age-adj"),

STUDIES: List[Study] = [

    # ── 41082230 — "Breast Cancer Incidence Rates in Ghanaian and US Black
    #    Women From 2013 to 2017" (SEER 17). Full-text Table 2, age-standardized
    #    (Segi world std), women 20–74, 2013–2015 (US SEER comparison window).
    #    NHB 148.5 (146.4–150.7); NHW 152.9 (151.9–153.8) per 100,000.
    #    (Ghana/GBHS 84.4 excluded — a foreign population, not a US racial minority.)
    Study("PMID41082230", 2024, "SEER 17", "invasive_incidence", "Black",
          irr_from_rates(148.5, 152.9),
          se_logirr_from_rate_cis(148.5, 146.4, 150.7, 152.9, 151.9, 153.8),
          minority_rate=148.5, nhw_rate=152.9,
          notes="SEER17 2013-2015, age-std Segi world, 20-74y; full-text Table 2"),

    # ── 35025856 — Ellington et al., MMWR 2022 "Trends in Breast Cancer
    #    Incidence, by Race, Ethnicity, and Age — United States, 1999–2018"
    #    (USCS = SEER+NPCR, ~99% of US pop). Age-adjusted rates per 100,000,
    #    year 2018 (Table). NHW 186.5; NHB 174.0; Hispanic 134.0; A/PI 143.5;
    #    AI/AN 127.3. No rate CIs in source → SE is Poisson-approx from
    #    annualized national case counts (rates are extremely stable, ~99% cover).
    Study("MMWR2022_35025856", 2022, "USCS", "invasive_incidence", "Black",
          irr_from_rates(174.0, 186.5),
          se_from_rates(174.0, 186.5, py_minority=12_980_000, py_nhw=89_600_000),
          minority_rate=174.0, nhw_rate=186.5, notes="USCS 2018; SE Poisson-approx"),
    Study("MMWR2022_35025856", 2022, "USCS", "invasive_incidence", "Hispanic",
          irr_from_rates(134.0, 186.5),
          se_from_rates(134.0, 186.5, py_minority=11_380_000, py_nhw=89_600_000),
          minority_rate=134.0, nhw_rate=186.5, notes="USCS 2018; SE Poisson-approx"),
    Study("MMWR2022_35025856", 2022, "USCS", "invasive_incidence", "Asian",
          irr_from_rates(143.5, 186.5),
          se_from_rates(143.5, 186.5, py_minority=5_080_000, py_nhw=89_600_000),
          minority_rate=143.5, nhw_rate=186.5, notes="USCS 2018 A/PI (incl. PI); SE Poisson-approx"),
    Study("MMWR2022_35025856", 2022, "USCS", "invasive_incidence", "AIAN",
          irr_from_rates(127.3, 186.5),
          se_from_rates(127.3, 186.5, py_minority=798_000, py_nhw=89_600_000),
          minority_rate=127.3, nhw_rate=186.5, notes="USCS 2018; SE Poisson-approx"),

    # ── 34861613 — Du & Song, Cancer Epidemiology 2022. SEER age-adjusted
    #    incidence per 100,000 (2000 US std), Table 2, period 2012–2018:
    #    NHW 190.5 (189.8–191.2); NHB 183.1 (181.5–184.8); NHAPI 149.2
    #    (147.7–150.7); AIAN 139.9 (134.5–145.5); Hispanic 137.0 (135.9–138.2).
    #    NOTE: SEER-based → overlaps MMWR/USCS (non-independence to handle).
    Study("DuSong2022_34861613", 2022, "SEER", "invasive_incidence", "Black",
          irr_from_rates(183.1, 190.5),
          se_logirr_from_rate_cis(183.1, 181.5, 184.8, 190.5, 189.8, 191.2),
          minority_rate=183.1, nhw_rate=190.5, notes="SEER 2012-2018, Table 2"),
    Study("DuSong2022_34861613", 2022, "SEER", "invasive_incidence", "Hispanic",
          irr_from_rates(137.0, 190.5),
          se_logirr_from_rate_cis(137.0, 135.9, 138.2, 190.5, 189.8, 191.2),
          minority_rate=137.0, nhw_rate=190.5, notes="SEER 2012-2018, Table 2"),
    Study("DuSong2022_34861613", 2022, "SEER", "invasive_incidence", "Asian",
          irr_from_rates(149.2, 190.5),
          se_logirr_from_rate_cis(149.2, 147.7, 150.7, 190.5, 189.8, 191.2),
          minority_rate=149.2, nhw_rate=190.5, notes="SEER 2012-2018 NHAPI, Table 2"),
    Study("DuSong2022_34861613", 2022, "SEER", "invasive_incidence", "AIAN",
          irr_from_rates(139.9, 190.5),
          se_logirr_from_rate_cis(139.9, 134.5, 145.5, 190.5, 189.8, 191.2),
          minority_rate=139.9, nhw_rate=190.5, notes="SEER 2012-2018, Table 2"),
    # DuSong Table 3 — subtype by HR status (age-adj rates 2000-2018, per 100k)
    # HR-negative (aggressive): NHW 28.0; NHB 46.5; NHAPI 22.3; AIAN 21.9; Hisp 23.3
    Study("DuSong2022_34861613", 2022, "SEER", "hrneg_incidence", "Black",
          irr_from_rates(46.5, 28.0), se_logirr_from_rate_cis(46.5,46.0,47.1, 28.0,27.9,28.2),
          minority_rate=46.5, nhw_rate=28.0, notes="SEER HR-negative, Table 3"),
    Study("DuSong2022_34861613", 2022, "SEER", "hrneg_incidence", "Hispanic",
          irr_from_rates(23.3, 28.0), se_logirr_from_rate_cis(23.3,22.9,23.6, 28.0,27.9,28.2),
          minority_rate=23.3, nhw_rate=28.0, notes="SEER HR-negative, Table 3"),
    Study("DuSong2022_34861613", 2022, "SEER", "hrneg_incidence", "Asian",
          irr_from_rates(22.3, 28.0), se_logirr_from_rate_cis(22.3,21.9,22.7, 28.0,27.9,28.2),
          minority_rate=22.3, nhw_rate=28.0, notes="SEER HR-negative NHAPI, Table 3"),
    Study("DuSong2022_34861613", 2022, "SEER", "hrneg_incidence", "AIAN",
          irr_from_rates(21.9, 28.0), se_logirr_from_rate_cis(21.9,20.5,23.3, 28.0,27.9,28.2),
          minority_rate=21.9, nhw_rate=28.0, notes="SEER HR-negative, Table 3"),
    # HR-positive: NHW 146.6; NHB 114.1; NHAPI 109.5; AIAN 96.5; Hisp 97.7
    Study("DuSong2022_34861613", 2022, "SEER", "hrpos_incidence", "Black",
          irr_from_rates(114.1, 146.6), se_logirr_from_rate_cis(114.1,113.3,115.0, 146.6,146.2,147.0),
          minority_rate=114.1, nhw_rate=146.6, notes="SEER HR-positive, Table 3"),
    Study("DuSong2022_34861613", 2022, "SEER", "hrpos_incidence", "Hispanic",
          irr_from_rates(97.7, 146.6), se_logirr_from_rate_cis(97.7,97.0,98.4, 146.6,146.2,147.0),
          minority_rate=97.7, nhw_rate=146.6, notes="SEER HR-positive, Table 3"),
    Study("DuSong2022_34861613", 2022, "SEER", "hrpos_incidence", "Asian",
          irr_from_rates(109.5, 146.6), se_logirr_from_rate_cis(109.5,108.7,110.4, 146.6,146.2,147.0),
          minority_rate=109.5, nhw_rate=146.6, notes="SEER HR-positive NHAPI, Table 3"),
    Study("DuSong2022_34861613", 2022, "SEER", "hrpos_incidence", "AIAN",
          irr_from_rates(96.5, 146.6), se_logirr_from_rate_cis(96.5,93.5,99.5, 146.6,146.2,147.0),
          minority_rate=96.5, nhw_rate=146.6, notes="SEER HR-positive, Table 3"),

    # ── 26513636 — DeSantis et al., "Breast Cancer Statistics, 2015" CA Cancer
    #    J Clin. NAACCR (~93% of US), age-adjusted 2000 std, 2008–2012 (Fig 1):
    #    NHW 128.1; NHB 124.3; AI/AN 91.9; Hispanic 91.9; API 88.3 per 100,000.
    #    No published CIs → SE Poisson-approx from estimated national case counts.
    #    NAACCR base makes this less SEER-overlapping than the other US studies.
    Study("DeSantis2016_26513636", 2016, "NAACCR", "invasive_incidence", "Black",
          irr_from_rates(124.3, 128.1),
          se_from_rates(124.3, 128.1, py_minority=101_800_000, py_nhw=673_000_000),
          minority_rate=124.3, nhw_rate=128.1, notes="NAACCR 2008-2012; SE approx"),
    Study("DeSantis2016_26513636", 2016, "NAACCR", "invasive_incidence", "Hispanic",
          irr_from_rates(91.9, 128.1),
          se_from_rates(91.9, 128.1, py_minority=100_100_000, py_nhw=673_000_000),
          minority_rate=91.9, nhw_rate=128.1, notes="NAACCR 2008-2012; SE approx"),
    Study("DeSantis2016_26513636", 2016, "NAACCR", "invasive_incidence", "Asian",
          irr_from_rates(88.3, 128.1),
          se_from_rates(88.3, 128.1, py_minority=65_100_000, py_nhw=673_000_000),
          minority_rate=88.3, nhw_rate=128.1, notes="NAACCR 2008-2012 API; SE approx"),
    Study("DeSantis2016_26513636", 2016, "NAACCR", "invasive_incidence", "AIAN",
          irr_from_rates(91.9, 128.1),
          se_from_rates(91.9, 128.1, py_minority=6_260_000, py_nhw=673_000_000),
          minority_rate=91.9, nhw_rate=128.1, notes="NAACCR 2008-2012 CHSDA; SE approx"),

    # ── 31764279 — Gopalani et al., Epidemiology 2020 "Trends in Cancer Incidence
    #    Among AI/AN and NHW" (IHS-linked, corrects AI/AN misclassification;
    #    age-std 2000, 1999–2015, Table 1). Female breast: AI/AN 72.7 (71.6–73.8);
    #    NHW 130.4 (130.3–130.6); RR 0.56 (0.55–0.57). Methodologically the best
    #    AI/AN estimate (registry studies overestimate the AI/AN rate → RR nearer 1).
    Study("Gopalani2020_31764279", 2020, "IHS-linked", "invasive_incidence", "AIAN",
          math.log(0.56), se_from_ci(0.56, 0.55, 0.57),
          minority_rate=72.7, nhw_rate=130.4, notes="IHS-linked, misclassification-corrected"),

    # ── 33074325 — Zhao et al., JAMA Netw Open 2020 "Variation in BC Subtype
    #    Incidence by Race/Ethnicity" (SEER 18, 2010–2015). Age-standardized IRR
    #    vs NHW (Fig 1 + text). Overall: Black 1.04 (1.02–1.05); Hispanic 0.79
    #    (0.75–0.83); API 0.90 (0.89–0.92); AIAN 0.82 (0.81–0.83).
    Study("Zhao2020_33074325", 2020, "SEER 18", "invasive_incidence", "Black",
          math.log(1.04), se_from_ci(1.04, 1.02, 1.05),
          notes="SEER18 2010-2015 IRR; Black slightly HIGHER (convergence era)"),
    Study("Zhao2020_33074325", 2020, "SEER 18", "invasive_incidence", "Hispanic",
          math.log(0.79), se_from_ci(0.79, 0.75, 0.83), notes="SEER18 2010-2015 IRR"),
    Study("Zhao2020_33074325", 2020, "SEER 18", "invasive_incidence", "Asian",
          math.log(0.90), se_from_ci(0.90, 0.89, 0.92), notes="SEER18 2010-2015 API IRR"),
    Study("Zhao2020_33074325", 2020, "SEER 18", "invasive_incidence", "AIAN",
          math.log(0.82), se_from_ci(0.82, 0.81, 0.83), notes="SEER18 2010-2015 IRR"),
    # Subtype IRRs vs NHW (Fig 1, panels A-D)
    # A. HR+/ERBB2- (luminal A-like)
    Study("Zhao2020_33074325", 2020, "SEER 18", "hrpos_her2neg_incidence", "Black",
          math.log(0.86), se_from_ci(0.86, 0.84, 0.87), notes="SEER18 HR+/HER2- IRR"),
    Study("Zhao2020_33074325", 2020, "SEER 18", "hrpos_her2neg_incidence", "Hispanic",
          math.log(0.78), se_from_ci(0.78, 0.76, 0.79), notes="SEER18 HR+/HER2- IRR"),
    Study("Zhao2020_33074325", 2020, "SEER 18", "hrpos_her2neg_incidence", "Asian",
          math.log(0.87), se_from_ci(0.87, 0.85, 0.88), notes="SEER18 HR+/HER2- API IRR"),
    Study("Zhao2020_33074325", 2020, "SEER 18", "hrpos_her2neg_incidence", "AIAN",
          math.log(0.74), se_from_ci(0.74, 0.69, 0.79), notes="SEER18 HR+/HER2- IRR"),
    # B. HR+/ERBB2+ (luminal B-like)
    Study("Zhao2020_33074325", 2020, "SEER 18", "hrpos_her2pos_incidence", "Black",
          math.log(1.12), se_from_ci(1.12, 1.08, 1.16), notes="SEER18 HR+/HER2+ IRR"),
    Study("Zhao2020_33074325", 2020, "SEER 18", "hrpos_her2pos_incidence", "Hispanic",
          math.log(0.91), se_from_ci(0.91, 0.88, 0.94), notes="SEER18 HR+/HER2+ IRR"),
    Study("Zhao2020_33074325", 2020, "SEER 18", "hrpos_her2pos_incidence", "Asian",
          math.log(1.04), se_from_ci(1.04, 1.00, 1.08), notes="SEER18 HR+/HER2+ API IRR"),
    Study("Zhao2020_33074325", 2020, "SEER 18", "hrpos_her2pos_incidence", "AIAN",
          math.log(0.94), se_from_ci(0.94, 0.81, 1.09), notes="SEER18 HR+/HER2+ IRR"),
    # C. HR-/ERBB2+ (HER2-enriched)
    Study("Zhao2020_33074325", 2020, "SEER 18", "hrneg_her2pos_incidence", "Black",
          math.log(1.46), se_from_ci(1.46, 1.38, 1.54), notes="SEER18 HR-/HER2+ IRR"),
    Study("Zhao2020_33074325", 2020, "SEER 18", "hrneg_her2pos_incidence", "Hispanic",
          math.log(1.05), se_from_ci(1.05, 0.99, 1.11), notes="SEER18 HR-/HER2+ IRR"),
    Study("Zhao2020_33074325", 2020, "SEER 18", "hrneg_her2pos_incidence", "Asian",
          math.log(1.41), se_from_ci(1.41, 1.33, 1.49), notes="SEER18 HR-/HER2+ API IRR"),
    Study("Zhao2020_33074325", 2020, "SEER 18", "hrneg_her2pos_incidence", "AIAN",
          math.log(1.04), se_from_ci(1.04, 0.82, 1.31), notes="SEER18 HR-/HER2+ IRR"),
    # D. TNBC
    Study("Zhao2020_33074325", 2020, "SEER 18", "tnbc_incidence", "Black",
          math.log(2.07), se_from_ci(2.07, 2.01, 2.14), notes="SEER18 TNBC IRR"),
    Study("Zhao2020_33074325", 2020, "SEER 18", "tnbc_incidence", "Hispanic",
          math.log(0.94), se_from_ci(0.94, 0.91, 0.98), notes="SEER18 TNBC IRR"),
    Study("Zhao2020_33074325", 2020, "SEER 18", "tnbc_incidence", "Asian",
          math.log(0.79), se_from_ci(0.79, 0.75, 0.83), notes="SEER18 TNBC API IRR"),
    Study("Zhao2020_33074325", 2020, "SEER 18", "tnbc_incidence", "AIAN",
          math.log(0.89), se_from_ci(0.89, 0.76, 1.04), notes="SEER18 TNBC IRR"),

    # ── 20147696 — Gomez et al., Am J Public Health 2010 "Hidden Breast Cancer
    #    Disparities in Asian Women" (California Cancer Registry, Table 2, age-adj
    #    2000 US std). 2000–2004: NHW 145.6 (144.6–146.7); US-born Asian aggregate
    #    135.9 (129.6–142.4); foreign-born Asian aggregate 78.5 (76.6–80.4).
    #    Primary point = person-year-weighted combined Asian 96.4 vs NHW 145.6
    #    (cases: Asian 1804+6858=8662, NHW 76 235). Nativity strata kept for a
    #    secondary analysis.
    Study("Gomez2010_20147696", 2010, "California CR", "invasive_incidence", "Asian",
          irr_from_rates(96.4, 145.6),
          se_from_rates(96.4, 145.6, py_minority=8_985_000, py_nhw=52_360_000),
          minority_rate=96.4, nhw_rate=145.6,
          notes="CA 2000-2004; derived PY-weighted US-born+foreign-born Asian; age-adj 2000 std"),

    # ── 21351091 — Liu et al., Int J Cancer 2012 "Invasive breast cancer
    #    incidence trends by detailed race/ethnicity and age" (LA County SEER).
    #    Multivariable-adjusted incidence RR vs NH white (adj. period + age):
    #    Black 0.78 (0.77-0.79); Hispanic 0.49 (0.48-0.50); Chinese 0.45
    #    (0.44-0.47); Filipina 0.76 (0.73-0.78); Japanese 0.68 (0.65-0.70);
    #    Korean 0.34 (0.32-0.36). NOTE: model-adjusted RR (not ratio-of-rates);
    #    LA County (Hispanic much lower than national).
    Study("Liu2012_21351091", 2012, "LA County SEER", "invasive_incidence", "Black",
          math.log(0.78), se_from_ci(0.78, 0.77, 0.79),
          minority_rate=None, nhw_rate=None, notes="adj RR, LA County"),
    Study("Liu2012_21351091", 2012, "LA County SEER", "invasive_incidence", "Hispanic",
          math.log(0.49), se_from_ci(0.49, 0.48, 0.50),
          notes="adj RR, LA County (much lower than national)"),
    # Asian ethnic subgroups (disaggregated dataset — not in the aggregate Asian pool)
    Study("Liu2012_21351091", 2012, "LA County SEER", "invasive_incidence", "Chinese",
          math.log(0.45), se_from_ci(0.45, 0.44, 0.47), notes="adj RR vs NHW"),
    Study("Liu2012_21351091", 2012, "LA County SEER", "invasive_incidence", "Filipina",
          math.log(0.76), se_from_ci(0.76, 0.73, 0.78), notes="adj RR vs NHW"),
    Study("Liu2012_21351091", 2012, "LA County SEER", "invasive_incidence", "Japanese",
          math.log(0.68), se_from_ci(0.68, 0.65, 0.70), notes="adj RR vs NHW"),
    Study("Liu2012_21351091", 2012, "LA County SEER", "invasive_incidence", "Korean",
          math.log(0.34), se_from_ci(0.34, 0.32, 0.36), notes="adj RR vs NHW"),

    # ── T_e7879b363303 — "Incidence trends in triple-negative breast cancer
    #    among women in the US" (full paper, 14pp). Age-adjusted TNBC incidence
    #    per 100,000: Black 33.8, White 17.5, Hispanic 14.7, AIAN 14.7, Asian ~12.
    #    Black vs White TNBC IRR 1.93 (1.88–1.97). SUBTYPE stratum (not primary).
    Study("TNBC_Te7879b3", 2023, "SEER/USCS", "tnbc_incidence", "Black",
          math.log(1.93), se_from_ci(1.93, 1.88, 1.97),
          minority_rate=33.8, nhw_rate=17.5,
          notes="TNBC subtype; Black vs White IRR 1.93 (1.88-1.97); full-text; citation TBD"),
    Study("TNBC_Te7879b3", 2023, "SEER/USCS", "tnbc_incidence", "Hispanic",
          math.log(0.84), se_from_ci(0.84, 0.82, 0.86),
          minority_rate=14.7, nhw_rate=17.5,
          notes="TNBC subtype; Hispanic vs White IRR 0.84 (0.82-0.86)"),
    Study("TNBC_Te7879b3", 2023, "SEER/USCS", "tnbc_incidence", "Asian",
          math.log(0.69), se_from_ci(0.69, 0.68, 0.69),
          minority_rate=12.0, nhw_rate=17.5,
          notes="TNBC subtype; Asian vs White IRR 0.69 (0.68-0.69)"),
    Study("TNBC_Te7879b3", 2023, "SEER/USCS", "tnbc_incidence", "AIAN",
          math.log(0.84), se_from_ci(0.84, 0.75, 0.93),
          minority_rate=14.7, nhw_rate=17.5,
          notes="TNBC subtype; AIAN vs White IRR 0.84 (0.75-0.93)"),

]


# ─── Random-effects meta-analysis (DerSimonian-Laird) ─────────────────────────

def random_effects_meta(studies: List[Study]):
    k = len(studies)
    if k == 0:
        return None

    yi = [s.log_irr for s in studies]
    vi = [s.se ** 2 for s in studies]
    wi_fixed = [1 / v for v in vi]

    theta_fixed = sum(w * y for w, y in zip(wi_fixed, yi)) / sum(wi_fixed)

    Q = sum(w * (y - theta_fixed) ** 2 for w, y in zip(wi_fixed, yi))
    df = k - 1

    I2 = max(0, (Q - df) / Q * 100) if Q > 0 else 0.0

    c = sum(wi_fixed) - sum(w ** 2 for w in wi_fixed) / sum(wi_fixed)
    tau2 = max(0, (Q - df) / c) if c > 0 else 0.0

    wi_re = [1 / (v + tau2) for v in vi]
    theta_re = sum(w * y for w, y in zip(wi_re, yi)) / sum(wi_re)
    se_re = math.sqrt(1 / sum(wi_re))

    ci_low = theta_re - 1.96 * se_re
    ci_high = theta_re + 1.96 * se_re
    pi_low = theta_re - 1.96 * math.sqrt(tau2 + se_re ** 2)
    pi_high = theta_re + 1.96 * math.sqrt(tau2 + se_re ** 2)

    z = theta_re / se_re
    p = 2 * (1 - _norm_cdf(abs(z)))

    return {
        "k": k, "theta": theta_re, "se": se_re,
        "irr": math.exp(theta_re),
        "ci_low": math.exp(ci_low), "ci_high": math.exp(ci_high),
        "pi_low": math.exp(pi_low), "pi_high": math.exp(pi_high),
        "I2": I2, "tau2": tau2, "Q": Q, "Q_df": df,
        "p_Q": 1 - _chi2_cdf(Q, df),
        "z": z, "p": p,
    }


def _norm_cdf(x):
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def _chi2_cdf(x, df):
    return _reg_gamma(df / 2, x / 2)


def _reg_gamma(a, x, max_iter=200, tol=1e-10):
    if x <= 0:
        return 0.0
    ln_gamma_a = math.lgamma(a)
    total = 1.0
    term = 1.0
    for n in range(1, max_iter):
        term *= x / (a + n)
        total += term
        if abs(term) < tol:
            break
    return math.exp(-x + a * math.log(x) - ln_gamma_a) * total / a


# ─── Forest plot (ASCII) ─────────────────────────────────────────────────────

def forest_plot(studies: List[Study], result: dict, title: str, width=72):
    lines = []
    lines.append("=" * width)
    lines.append(f"  {title}")
    lines.append("=" * width)
    lines.append(f"  {'Study':<20} {'IRR':>6} {'95% CI':>20}  {'Weight%':>7}")
    lines.append("-" * width)

    tau2 = result["tau2"]
    vi = [s.se ** 2 for s in studies]
    wi = [1 / (v + tau2) for v in vi]
    total_w = sum(wi)

    for s, w in zip(studies, wi):
        pct = w / total_w * 100
        ci_str = f"({s.ci_low:.2f}-{s.ci_high:.2f})"
        lines.append(f"  {s.id:<20} {s.irr:>6.3f} {ci_str:>20}  {pct:>6.1f}%")

    lines.append("-" * width)
    lines.append(
        f"  {'Pooled (RE)':<20} {result['irr']:>6.3f} "
        f"({result['ci_low']:.3f}-{result['ci_high']:.3f})"
    )
    lines.append(
        f"  {'Prediction interval':<20}       "
        f"({result['pi_low']:.3f}-{result['pi_high']:.3f})"
    )
    lines.append("-" * width)
    lines.append(
        f"  I2 = {result['I2']:.1f}%   tau2 = {result['tau2']:.4f}   "
        f"Q({result['Q_df']}) = {result['Q']:.2f}   p = {result['p_Q']:.3f}"
    )
    lines.append("=" * width)
    return "\n".join(lines)


# ─── Main analyses ────────────────────────────────────────────────────────────

def _subset(group, outcome="invasive_incidence"):
    return [s for s in STUDIES if s.outcome == outcome and s.minority_group == group]


def run_all():
    if not STUDIES:
        print("\n" + "━" * 72)
        print("  BREAST CANCER INCIDENCE META-ANALYSIS")
        print("  Racial/Ethnic Disparities (minority vs NHW)")
        print("━" * 72)
        print("\n  [WAITING] STUDIES is empty — no data extracted yet.")
        print("  Fill in run_meta_analysis_breast.py :: STUDIES from the full")
        print("  text of the INCLUDED studies (age-adjusted invasive incidence")
        print("  rates by race), then re-run this script.\n")
        return {}

    results = {}
    analyses = {
        "Invasive BC Incidence — Black vs NHW":    _subset("Black"),
        "Invasive BC Incidence — Hispanic vs NHW": _subset("Hispanic"),
        "Invasive BC Incidence — Asian vs NHW":    _subset("Asian"),
        "Invasive BC Incidence — AIAN vs NHW":     _subset("AIAN"),
        "TNBC Incidence — Black vs NHW":           _subset("Black", "tnbc_incidence"),
    }

    print("\n" + "━" * 72)
    print("  META-ANALYSIS RESULTS")
    print("  Racial/Ethnic Disparities in Breast Cancer Incidence")
    print("━" * 72 + "\n")

    for label, subset in analyses.items():
        if len(subset) < 2:
            print(f"[SKIP] {label} — only {len(subset)} study\n")
            continue
        res = random_effects_meta(subset)
        if res is None:
            continue
        results[label] = res
        print(forest_plot(subset, res, label))
        print()

    print("\n" + "═" * 72)
    print("  SUMMARY TABLE — Pooled IRRs (Minority vs NHW)")
    print("═" * 72)
    print(f"  {'Comparison':<44} {'IRR':>6}  {'95% CI':>16}  {'I2':>5}  p")
    print("─" * 72)
    for label, res in results.items():
        ci = f"({res['ci_low']:.3f}-{res['ci_high']:.3f})"
        p_str = f"{res['p']:.4f}" if res['p'] >= 0.0001 else "<0.001"
        print(f"  {label:<44} {res['irr']:>6.3f}  {ci:>16}  {res['I2']:>4.0f}%  {p_str}")
    print("═" * 72)

    return results


if __name__ == "__main__":
    results = run_all()
    if results:
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        out = {}
        for k, v in results.items():
            out[k] = {
                "k": v["k"],
                "irr": round(v["irr"], 3),
                "ci_low": round(v["ci_low"], 3),
                "ci_high": round(v["ci_high"], 3),
                "pi_low": round(v["pi_low"], 3),
                "pi_high": round(v["pi_high"], 3),
                "I2": round(v["I2"], 1),
                "tau2": round(v["tau2"], 4),
                "Q": round(v["Q"], 2),
                "Q_df": v["Q_df"],
                "p_Q": round(v["p_Q"], 4),
                "p_effect": round(v["p"], 6),
            }
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = os.path.join(OUTPUT_DIR, f"meta_results_{stamp}.json")
        with open(path, "w") as f:
            json.dump(out, f, indent=2)
        print(f"\n[✓] Results saved to {path}")
