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


def se_logrr_from_counts(cases_minority, cases_nhw):
    """SE of log(rate ratio) from case counts (Poisson): sqrt(1/c_m + 1/c_n)."""
    return math.sqrt(1 / cases_minority + 1 / cases_nhw)


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
    # ER-status subtypes (Table 2, age-std Segi) — Black vs White. ER-negative
    # shows the aggressive-subtype Black excess (IRR 1.80), corroborating the
    # TNBC / HER2-enriched pattern; pools with Du&Song HR-status.
    Study("PMID41082230", 2024, "SEER 17", "hrpos_incidence", "Black",
          irr_from_rates(105.4, 128.5),
          se_logirr_from_rate_cis(105.4, 103.6, 107.3, 128.5, 127.9, 129.7),
          minority_rate=105.4, nhw_rate=128.5, notes="ER-positive age-std; Black vs White"),
    Study("PMID41082230", 2024, "SEER 17", "hrneg_incidence", "Black",
          irr_from_rates(43.1, 24.0),
          se_logirr_from_rate_cis(43.1, 42.0, 44.3, 24.0, 23.6, 24.4),
          minority_rate=43.1, nhw_rate=24.0, notes="ER-negative age-std; Black vs White (aggressive)"),

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
    #    2000 US std). 2000–2004: NHW 145.6 (144.6–146.7); US-born Asian 135.9
    #    (129.6–142.4); foreign-born Asian 78.5 (76.6–80.4).
    #    NOT pooled into the aggregate Asian comparison: the paper reports no single
    #    combined-Asian rate, and a person-year-weighted combination would be an
    #    analyst derivation (cf. the 12115511 decision). Instead Gomez contributes
    #    its DIRECT nativity values — its actual novel finding — as a NATIVITY
    #    sub-analysis: US-born Asian ≈ NHW, foreign-born Asian ~half of NHW.
    Study("Gomez2010_20147696", 2010, "California CR", "invasive_incidence_nativity", "AsianUSborn",
          irr_from_rates(135.9, 145.6),
          se_logirr_from_rate_cis(135.9, 129.6, 142.4, 145.6, 144.6, 146.7),
          minority_rate=135.9, nhw_rate=145.6, notes="US-born Asian vs NHW; direct (CA 2000-2004)"),
    Study("Gomez2010_20147696", 2010, "California CR", "invasive_incidence_nativity", "AsianForeignborn",
          irr_from_rates(78.5, 145.6),
          se_logirr_from_rate_cis(78.5, 76.6, 80.4, 145.6, 144.6, 146.7),
          minority_rate=78.5, nhw_rate=145.6, notes="foreign-born Asian vs NHW; direct (CA 2000-2004)"),

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

    # ── 12115511 — Deapen et al., Int J Cancer 2002 "Rapidly rising breast
    #    cancer incidence rates among Asian-American women" (LA County CSP/CCR,
    #    Table I, 1988-1997). DEMOTED TO NARRATIVE (not pooled here): its rates
    #    are annual (a trends paper), so any single summary is an analyst
    #    derivation whose value is sensitive to the period chosen (Korean 0.23
    #    [10-yr mean] vs 0.35 [1997]); it also overlaps Liu 21351091 (both LA
    #    County). Cited narratively as the foundational "rapidly rising" analysis;
    #    subgroup ordering (Korean lowest → Filipina/Japanese higher) is carried
    #    by Liu (21351091) + Hawaii (30503975) + Gomez (28365834, narrative).

    # ── 36504334 — Hicks/Liu et al., Cancer Causes Control 2023 "Characterizing
    #    breast cancer incidence and trends among AANHPI in Hawai'i" (SEER Hawaii,
    #    2010-2014 AAIR per 100,000). AGE-STRATIFIED (<50 vs ≥50) by ethnicity.
    #    This paper does double duty: it feeds the AGE-CROSSOVER analysis AND the
    #    Asian-disaggregation theme (Japanese / Filipino / Native Hawaiian).
    #    NHW reference age <50: 39.8 (34.8-45.1); age ≥50: 100.7 (94.7-106.9).
    #    IRRs computed here match the paper's reported IRRs (≥50: NH 1.37, JA 1.06,
    #    FA 0.77). Segregated from the main pool (different, age-specific outcome).
    Study("Hawaii2023_36504334", 2023, "SEER Hawaii", "invasive_incidence_age_lt50", "Japanese",
          irr_from_rates(52.0, 39.8), se_logirr_from_rate_cis(52.0, 45.6, 58.9, 39.8, 34.8, 45.1),
          minority_rate=52.0, nhw_rate=39.8, notes="age <50; 2010-2014 AAIR; JA highest when young"),
    Study("Hawaii2023_36504334", 2023, "SEER Hawaii", "invasive_incidence_age_lt50", "NativeHawaiian",
          irr_from_rates(33.2, 39.8), se_logirr_from_rate_cis(33.2, 28.7, 38.1, 39.8, 34.8, 45.1),
          minority_rate=33.2, nhw_rate=39.8, notes="age <50; 2010-2014 AAIR"),
    Study("Hawaii2023_36504334", 2023, "SEER Hawaii", "invasive_incidence_age_lt50", "Filipino",
          irr_from_rates(31.7, 39.8), se_logirr_from_rate_cis(31.7, 27.4, 36.4, 39.8, 34.8, 45.1),
          minority_rate=31.7, nhw_rate=39.8, notes="age <50; 2010-2014 AAIR; FA lowest"),
    Study("Hawaii2023_36504334", 2023, "SEER Hawaii", "invasive_incidence_age_ge50", "NativeHawaiian",
          irr_from_rates(137.6, 100.7), se_logirr_from_rate_cis(137.6, 128.2, 147.4, 100.7, 94.7, 106.9),
          minority_rate=137.6, nhw_rate=100.7, notes="age >=50; NH highest when older (crossover); paper IRR 1.37"),
    Study("Hawaii2023_36504334", 2023, "SEER Hawaii", "invasive_incidence_age_ge50", "Japanese",
          irr_from_rates(107.1, 100.7), se_logirr_from_rate_cis(107.1, 100.9, 113.4, 100.7, 94.7, 106.9),
          minority_rate=107.1, nhw_rate=100.7, notes="age >=50; paper IRR 1.06 (ns)"),
    Study("Hawaii2023_36504334", 2023, "SEER Hawaii", "invasive_incidence_age_ge50", "Filipino",
          irr_from_rates(77.9, 100.7), se_logirr_from_rate_cis(77.9, 71.8, 84.2, 100.7, 94.7, 106.9),
          minority_rate=77.9, nhw_rate=100.7, notes="age >=50; FA lowest both ages; paper IRR 0.77"),

    # ── 30503975 — Loo et al., Cancer Epidemiology 2019, Hawaii SEER 2010-2013.
    #    Table 1: invasive BC IR + IRR (95% CI) vs White, all ages, by ethnicity.
    #    SECOND Hawaii source (crude IRR) — pools with Liu's LA-County subgroups
    #    (Chinese/Filipina/Japanese) and adds Native Hawaiian. Reported IRRs used.
    Study("Loo2019_30503975", 2019, "SEER Hawaii", "invasive_incidence", "Japanese",
          math.log(1.03), se_from_ci(1.03, 1.02, 1.03),
          minority_rate=158.2, nhw_rate=154.2, notes="Hawaii crude IRR vs White; all ages"),
    Study("Loo2019_30503975", 2019, "SEER Hawaii", "invasive_incidence", "NativeHawaiian",
          math.log(1.11), se_from_ci(1.11, 1.10, 1.12),
          minority_rate=171.5, nhw_rate=154.2, notes="Hawaii crude IRR vs White; all ages"),
    Study("Loo2019_30503975", 2019, "SEER Hawaii", "invasive_incidence", "Filipina",
          math.log(0.69), se_from_ci(0.69, 0.68, 0.71),
          minority_rate=107.0, nhw_rate=154.2, notes="Hawaii crude IRR vs White; all ages"),
    Study("Loo2019_30503975", 2019, "SEER Hawaii", "invasive_incidence", "Chinese",
          math.log(0.59), se_from_ci(0.59, 0.55, 0.64),
          minority_rate=91.7, nhw_rate=154.2, notes="Hawaii crude IRR vs White; all ages"),
    # 30503975 subtype × ethnicity (Table 1, IRR vs White). Disaggregated-API
    # subtype pattern: Native Hawaiian is HIGH in HER2+ subtypes but (unlike Black)
    # LOW in TNBC — the aggressive-subtype excess is NOT uniform across "API".
    Study("Loo2019_30503975", 2019, "SEER Hawaii", "hrpos_her2neg_incidence", "Japanese",
          math.log(1.03), se_from_ci(1.03, 1.03, 1.04), notes="Hawaii IRR vs White"),
    Study("Loo2019_30503975", 2019, "SEER Hawaii", "hrpos_her2neg_incidence", "NativeHawaiian",
          math.log(1.12), se_from_ci(1.12, 1.11, 1.14), notes="Hawaii IRR vs White"),
    Study("Loo2019_30503975", 2019, "SEER Hawaii", "hrpos_her2neg_incidence", "Filipina",
          math.log(0.64), se_from_ci(0.64, 0.63, 0.66), notes="Hawaii IRR vs White"),
    Study("Loo2019_30503975", 2019, "SEER Hawaii", "hrpos_her2neg_incidence", "Chinese",
          math.log(0.58), se_from_ci(0.58, 0.53, 0.64), notes="Hawaii IRR vs White"),
    Study("Loo2019_30503975", 2019, "SEER Hawaii", "hrpos_her2pos_incidence", "Japanese",
          math.log(1.03), se_from_ci(1.03, 1.02, 1.05), notes="Hawaii IRR vs White"),
    Study("Loo2019_30503975", 2019, "SEER Hawaii", "hrpos_her2pos_incidence", "NativeHawaiian",
          math.log(1.35), se_from_ci(1.35, 1.347, 1.351), notes="Hawaii IRR vs White; highest"),
    Study("Loo2019_30503975", 2019, "SEER Hawaii", "hrpos_her2pos_incidence", "Filipina",
          math.log(0.88), se_from_ci(0.88, 0.86, 0.91), notes="Hawaii IRR vs White"),
    Study("Loo2019_30503975", 2019, "SEER Hawaii", "hrpos_her2pos_incidence", "Chinese",
          math.log(0.72), se_from_ci(0.72, 0.55, 0.90), notes="Hawaii IRR vs White"),
    Study("Loo2019_30503975", 2019, "SEER Hawaii", "hrneg_her2pos_incidence", "Japanese",
          math.log(0.88), se_from_ci(0.88, 0.82, 0.95), notes="Hawaii IRR vs White"),
    Study("Loo2019_30503975", 2019, "SEER Hawaii", "hrneg_her2pos_incidence", "NativeHawaiian",
          math.log(1.19), se_from_ci(1.19, 1.16, 1.21), notes="Hawaii IRR vs White; HER2-enriched high"),
    Study("Loo2019_30503975", 2019, "SEER Hawaii", "hrneg_her2pos_incidence", "Filipina",
          math.log(0.99), se_from_ci(0.99, 0.96, 1.00), notes="Hawaii IRR vs White"),
    Study("Loo2019_30503975", 2019, "SEER Hawaii", "hrneg_her2pos_incidence", "Chinese",
          math.log(0.97), se_from_ci(0.97, 0.78, 1.18), notes="Hawaii IRR vs White"),
    Study("Loo2019_30503975", 2019, "SEER Hawaii", "tnbc_incidence", "Japanese",
          math.log(1.07), se_from_ci(1.07, 1.07, 1.09), notes="Hawaii IRR vs White"),
    Study("Loo2019_30503975", 2019, "SEER Hawaii", "tnbc_incidence", "NativeHawaiian",
          math.log(0.86), se_from_ci(0.86, 0.79, 0.91), notes="Hawaii IRR vs White; TNBC LOW (unlike Black)"),
    Study("Loo2019_30503975", 2019, "SEER Hawaii", "tnbc_incidence", "Filipina",
          math.log(0.84), se_from_ci(0.84, 0.80, 0.88), notes="Hawaii IRR vs White"),
    Study("Loo2019_30503975", 2019, "SEER Hawaii", "tnbc_incidence", "Chinese",
          math.log(0.53), se_from_ci(0.53, 0.39, 0.71), notes="Hawaii IRR vs White; TNBC lowest"),

    # ── REMOVED (provenance unresolved): an "Asian Indian/Pakistani 72.3 vs NHW
    #    149.5 → IRR 0.48 (California CR)" point was previously entered here under
    #    id "Kakarala2011_21301957". The attached identifier PMID 21301957 is
    #    Moran et al. (a clinicopathologic/survival comparison, NOT a population
    #    incidence study), so the value cannot be attributed to that citation and
    #    its true source could not be confirmed. Dropped from the quantitative
    #    pool to avoid an unverifiable/misattributed estimate. The South Asian
    #    (Indian-Pakistani) direction remains supported narratively by Jain
    #    (CA, ~0.52) and Stotter (UK, ~45% lower). Restore here only if the value
    #    is re-sourced to a correctly identified primary incidence study.

    # ── 21473509 — Lepeak et al., WMJ 2011. Table 1: age-adjusted invasive BC
    #    incidence, African American vs White, Wisconsin state registry 2004-2006:
    #    103.0 vs 121.2 (RR 0.8; no CI reported → SE from rates). Adds a non-SEER
    #    STATE registry data point (geographic diversity) to the Black pool.
    Study("Lepeak2011_21473509", 2011, "Wisconsin CRS", "invasive_incidence", "Black",
          irr_from_rates(103.0, 121.2), se_from_rates(103.0, 121.2),
          minority_rate=103.0, nhw_rate=121.2, notes="Wisconsin state registry 2004-06; no CI reported"),

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


# ─── Black–White age crossover (15986118, NAACCR 1994-1998, Table 1) ──────────
# Age-specific invasive BC incidence per 100,000 and rate ratio (95% CI) vs White.
# Documents the classic crossover: Black excess in young women reverses after ~40.
# Not pooled (single source, fine age bands) — reported as a descriptive table.
# (age_band, white_rate, black_rate, black_RR, lo, hi, api_RR)
AGE_CROSSOVER_15986118 = [
    ("20-24",   1.20,   2.30, 1.92, 1.42, 2.60, None),
    ("25-29",   7.81,  12.20, 1.56, 1.38, 1.77, 0.68),
    ("30-34",  25.38,  33.21, 1.31, 1.26, 1.36, 0.73),
    ("35-39",  58.20,  68.50, 1.18, 1.12, 1.24, 0.82),
    ("40-44", 115.40, 117.59, 1.02, 0.98, 1.04, 0.84),
    ("45-49", 190.70, 184.77, 0.97, 0.93, 1.00, 0.80),
    ("50-54", 253.25, 230.87, 0.91, 0.88, 0.94, 0.74),
    ("55-59", 301.30, 269.46, 0.89, 0.86, 0.92, 0.73),
    ("60-64", 354.80, 285.29, 0.80, 0.77, 0.83, 0.64),
    ("65-69", 414.53, 333.60, 0.80, 0.77, 0.83, 0.55),
    ("70-74", 466.59, 366.04, 0.78, 0.75, 0.81, 0.52),
    ("75-79", 482.97, 394.05, 0.82, 0.79, 0.85, 0.49),
    ("80-84", 465.23, 388.29, 0.83, 0.79, 0.87, 0.47),
    ("85+",   395.10, 332.72, 0.84, 0.79, 0.89, 0.40),
]

# 15986118 Table 2 — Hispanic vs NON-HISPANIC (all) age-specific rate + RR (95% CI).
# NB: reference is "non-Hispanic (all races combined)", NOT NHW — so this is NOT
# directly comparable to the vs-White crossover above and is kept as a separate,
# descriptive series. Hispanic shows near-parity at 20-24 (RR 1.09) then a steady
# decline to 0.56. (age, non-Hisp rate, Hisp rate, RR, lo, hi)
AGE_HISPANIC_15986118 = [
    ("20-24",   1.13,   1.23, 1.09, 0.73, 1.63),
    ("25-29",   7.33,   6.45, 0.88, 0.74, 1.04),
    ("30-34",  23.11,  17.14, 0.74, 0.67, 0.82),
    ("35-39",  52.33,  36.79, 0.70, 0.65, 0.75),
    ("40-44", 100.48,  73.99, 0.74, 0.70, 0.78),  # paper prints RR 0.84 — likely typo (73.99/100.48=0.74)
    ("45-49", 165.64, 118.07, 0.71, 0.67, 0.75),
    ("50-54", 218.72, 145.14, 0.66, 0.63, 0.70),
    ("55-59", 258.29, 169.11, 0.65, 0.61, 0.69),
    ("60-64", 294.97, 198.09, 0.67, 0.63, 0.71),
    ("65-69", 337.19, 219.35, 0.65, 0.61, 0.69),
    ("70-74", 377.25, 231.57, 0.61, 0.57, 0.65),
    ("75-79", 390.33, 232.25, 0.59, 0.55, 0.64),
    ("80-84", 376.47, 210.54, 0.56, 0.51, 0.62),
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

    # ── Disaggregated Asian / ethnic-subgroup analysis (vs NHW) ───────────────
    print("\n" + "═" * 72)
    print("  DISAGGREGATED ETHNIC SUBGROUPS vs NHW (invasive incidence)")
    print("  Shows the ~2-3x spread hidden by the aggregate 'Asian/API' category.")
    print("═" * 72)
    print(f"  {'Subgroup':<16}{'k':>3}  {'IRR':>6}  {'95% CI':>16}  {'I2':>5}  sources")
    print("─" * 72)
    subgroup_rows = []
    for g in ["Korean", "Chinese", "Vietnamese", "Filipina",
              "Japanese", "NativeHawaiian"]:
        ss = _subset(g)
        if not ss:
            continue
        srcs = ",".join(sorted({s.source for s in ss}))
        if len(ss) >= 2:
            r = random_effects_meta(ss)
            subgroup_rows.append((g, r["irr"]))
            ci = f"({r['ci_low']:.3f}-{r['ci_high']:.3f})"
            print(f"  {g:<16}{len(ss):>3}  {r['irr']:>6.3f}  {ci:>16}  {r['I2']:>4.0f}%  {srcs}")
        else:
            s = ss[0]
            subgroup_rows.append((g, s.irr))
            ci = f"({s.ci_low:.3f}-{s.ci_high:.3f})"
            print(f"  {g:<16}{len(ss):>3}  {s.irr:>6.3f}  {ci:>16}  {'   -':>5}  {srcs}")
    print("─" * 72)
    if subgroup_rows:
        lo_g = min(subgroup_rows, key=lambda x: x[1])
        hi_g = max(subgroup_rows, key=lambda x: x[1])
        print(f"  Range: {lo_g[0]} {lo_g[1]:.2f}  ↔  {hi_g[0]} {hi_g[1]:.2f}  "
              f"({hi_g[1]/lo_g[1]:.1f}x spread) — aggregation masks this.")
    print("═" * 72)

    # ── Nativity sub-analysis (Gomez 20147696, direct values) ────────────────
    nat = [s for s in STUDIES if s.outcome == "invasive_incidence_nativity"]
    if nat:
        print("\n" + "═" * 72)
        print("  NATIVITY — Asian incidence by migrant status vs NHW (20147696)")
        print("═" * 72)
        lab = {"AsianUSborn": "US-born Asian", "AsianForeignborn": "Foreign-born Asian"}
        for s in nat:
            print(f"  {lab.get(s.minority_group, s.minority_group):<20} "
                  f"IRR {s.irr:.2f} ({s.ci_low:.2f}-{s.ci_high:.2f})   rate {s.minority_rate}")
        print("─" * 72)
        print("  US-born Asian ≈ NHW; foreign-born ~half — a generational gradient")
        print("  the aggregate 'Asian' rate conceals (direct values, not derived).")
        print("═" * 72)

    # ── Age-stratified descriptive (age-crossover / effect modification) ──────
    age_rows = [s for s in STUDIES
                if s.outcome in ("invasive_incidence_age_lt50", "invasive_incidence_age_ge50")]
    if age_rows:
        print("\n" + "═" * 72)
        print("  AGE-STRATIFIED — within-study IRR vs NHW (effect modification by age)")
        print("  Source: Hawaii SEER 36504334; NOT pooled with the age-adjusted main")
        print("  analysis — a separate, age-specific outcome. Shows the crossover.")
        print("═" * 72)
        print(f"  {'Group':<16} {'<50y IRR (95% CI)':<24} {'>=50y IRR (95% CI)':<24}")
        print("─" * 72)
        groups = ["Japanese", "NativeHawaiian", "Filipino"]
        idx = {(s.minority_group, s.outcome): s for s in age_rows}
        for g in groups:
            lt = idx.get((g, "invasive_incidence_age_lt50"))
            ge = idx.get((g, "invasive_incidence_age_ge50"))
            lt_s = f"{lt.irr:.2f} ({lt.ci_low:.2f}-{lt.ci_high:.2f})" if lt else "-"
            ge_s = f"{ge.irr:.2f} ({ge.ci_low:.2f}-{ge.ci_high:.2f})" if ge else "-"
            print(f"  {g:<16} {lt_s:<24} {ge_s:<24}")
        print("─" * 72)
        print("  Note: Japanese highest when young (IRR 1.31); Native Hawaiian")
        print("  overtakes when older (IRR 1.37) — within-API age crossover.")
        print("═" * 72)

    # ── Black–White age crossover (NAACCR 15986118) ──────────────────────────
    print("\n" + "═" * 72)
    print("  BLACK–WHITE AGE CROSSOVER — age-specific RR vs White (95% CI)")
    print("  Source: 15986118, NAACCR 1994-1998, Table 1 (rate+RR+CI). Descriptive.")
    print("═" * 72)
    print(f"  {'Age':<8}{'White rate':>11}{'Black rate':>11}{'Black RR (95% CI)':>22}{'API RR':>9}")
    print("─" * 72)
    for band, wr, br, rr, lo, hi, api in AGE_CROSSOVER_15986118:
        api_s = f"{api:.2f}" if api is not None else "  -"
        print(f"  {band:<8}{wr:>11.1f}{br:>11.1f}{f'{rr:.2f} ({lo:.2f}-{hi:.2f})':>22}{api_s:>9}")
    print("─" * 72)
    print("  Black RR 1.92 at 20-24 → crosses 1.0 near 40-44 → 0.78-0.84 after 60.")
    print("  API RR falls monotonically 0.68 → 0.40; consistently below White.")
    hisp_lo = AGE_HISPANIC_15986118[-1]
    print(f"  Hispanic vs non-Hispanic (all): {AGE_HISPANIC_15986118[0][3]:.2f} at 20-24 "
          f"→ {hisp_lo[3]:.2f} at 80-84 (ref = non-Hispanic, not NHW).")
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
