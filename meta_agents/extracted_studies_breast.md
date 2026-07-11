# Extracted studies — breast-cancer incidence by race/ethnicity

Source: Embase export (`records_tabular.csv`), abstract-level extraction.
Outcome = **age-adjusted / age-standardized invasive breast-cancer incidence
rate (per 100,000)**. Reference group = non-Hispanic White (NHW) / White.
IRR = minority rate / reference rate (values <1 = minority lower).

> Note: PubMed / NCBI eutils are blocked by this environment's network policy
> (403 at the proxy), so extraction is abstract-based. Where an abstract gives
> rate 95% CIs or case counts, those are used for the SE; otherwise a Poisson
> SE is derived from estimated case counts.

## A. Overall invasive BC incidence (minority vs NHW/White)

| # | Study | Source / period | Group | rate | ref (White) | notes |
|---|-------|-----------------|-------|------|-------------|-------|
| 180 | Wang 2022 (row180) | SEER 18, 2000–2018, age≥20 | Black | 178.4 | 190.4 | NHB vs NHW |
| 180 | Wang 2022 | SEER 18, 2000–2018 | API | 141.3 | 190.4 | |
| 180 | Wang 2022 | SEER 18, 2000–2018 | Hispanic | 133.3 | 190.4 | |
| 180 | Wang 2022 | SEER 18, 2000–2018 | AIAN | 128.8 | 190.4 | |
| 63 | England 2025 (row63) | NCRAS England, 2011–2019, age≥25 | Black (African) | 118.2 (111.6–125.1) | 199.6 (198.9–200.3) | ASIR, distinct population |
| 88 | Brazil 2024 (row88) | 13 Brazilian registries, 2010–2015 | Black | 59.7 | 101.3 | distinct population |

US-SEER studies (180 & the ER-split 67) overlap; only 180 kept for the overall pool.

## B. Triple-negative BC (TNBC) incidence (minority vs White)

| # | Study | Source / period | Group | rate | White ref | counts |
|---|-------|-----------------|-------|------|-----------|--------|
| 150 | Xie 2023 (row150) | SEER 18, 2010–2019, age≥20 | Black | 33.8 | 17.5 | TNBC n=62,623 |
| 150 | | | AIAN | 14.7 | 17.5 | |
| 150 | | | Hispanic | 14.7 | 17.5 | |
| 150 | | | Asian | 12.4 | 17.5 | |
| 137 | Kong 2023 (row137) | USCS / NPCR-SEER, 2015–2019 | Black | 25.2 | 12.9 | Black 28,710; White 86,195 |
| 137 | | | AIAN | 11.2 | 12.9 | AIAN 768 |
| 137 | | | Hispanic | 11.1 | 12.9 | Hispanic 12,937 |
| 137 | | | API | 9.0 | 12.9 | API 4,969 |
| 367 | Yao 2013 (row367) | SEER 18 national, 2010 | Black | 20.4 | 11.3 | single year |

Row 147 is a duplicate of 137 (same NPCR-SEER 2015–2019 data) → excluded.

## C. Subtype context (single-study, reported not pooled)

| # | Study | Group | ER-negative rate | White ref |
|---|-------|-------|------------------|-----------|
| 67 | Jenkins 2025 (row67) | Black | 43.1 (42.0–44.3) | 24.0 (23.6–24.4) | SEER 2013–2015, ER− |

## D. Age crossover (documented context, not pooled)

- Row 453 (Anderson 2008, SEER 1975–2004): <40y Black 15.5 vs White 13.1
  (IRR 1.18); ≥40y Black 239.5 vs White 281.3 (IRR 0.85) — classic crossover.
- Row 110 (Xu 2024, SEER 2000–2019, age 20–49): Black vs NHW IRR 1.53
  (20–29y), 1.15 (30–39y), 0.96 (40–49y).
