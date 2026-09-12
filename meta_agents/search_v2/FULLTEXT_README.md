# Full-text stage — run in a Codespace (not the web sandbox)

The Claude Code web session runs behind an egress proxy that blocks `doi.org`,
publisher hosts, and NCBI E-utilities, so full-text PDFs cannot be fetched there.
A GitHub Codespace on this repo has open network egress, so the retrieval runs
cleanly there.

## Inputs (already in this folder)
- `merged_unique.csv` — 4,793 unique records (has `pmid`, `doi`).
- `screening_decisions.csv` — title/abstract decisions; 242 `include`.
- `includes_characterization.csv` — publication series per include.

## Steps in the Codespace

```bash
cd meta_agents/search_v2
pip install requests

# 1) Fetch full text (PMC open-access) + record OA links for the rest.
NCBI_API_KEY=<key> NCBI_EMAIL=<you@example.com> UNPAYWALL_EMAIL=<you@example.com> \
    python3 fetch_fulltext.py
#   -> writes fulltext/<record_id>.txt and fulltext_coverage.csv

# 2) Build the author screening + extraction template (no network needed).
python3 ft_screen_template.py
#   -> writes ft_screening_log.csv (242 rows, empty decision/extraction columns)
```

## What each file gives you
- `fulltext/<id>.txt` — flattened PMC full text (Methods/Results/tables) where the
  article is open-access.
- `fulltext_coverage.csv` — per record: pmid/doi/pmcid, retrieval `source`
  (`pmc` / `unpaywall-oa-link` / `no-oa-full-text` / `none`), char count, `oa_url`.
- `manual_download_needed.csv` — **the manual worklist**: every record the fetch
  could NOT pull as PMC full text, with a ready `doi_url`. Work through these with
  institutional access; some already carry an `oa_url` (free copy) to try first.
- `download_links.csv` — pre-generated (already committed) link sheet for ALL 242
  (`doi_url`, `pubmed_url`) so manual retrieval can start before/independently of
  the Codespace run. Record 2038 has no DOI/PMID — find it by title:
  "Incidence trends in triple-negative breast cancer among women in the United
  States from 2010 to 2019 by race/ethnicity".
- `ft_screening_log.csv` — the working sheet. For each record the author fills:
  - `ft_decision` = include | exclude
  - `ft_reason` (when excluding) = one of, EXACTLY:
    - `Did not report the outcome of interest`
    - `Ineligible population`
    - `Overlapping or duplicate dataset`
    - `Full text unavailable`
  - `registry_family_confirmed`, `diagnosis_years`, and the extracted rates
    (`minority_rate`/`minority_ci`, `nhw_rate`/`nhw_ci`, `irr`/`irr_ci`) with the
    exact `source_location` (table/figure number, page).

## Eligibility criterion (apply at full text)
Include only if the article reports **age-adjusted (age-standardized) invasive
female breast-cancer incidence** for **≥1 US racial/ethnic group relative to
non-Hispanic White women**, as rates permitting an incidence rate ratio or a
directly reported rate ratio. Then dedup by registry family (SEER ⊂ NAACCR ⊂
USCS; county ⊂ state ⊂ SEER) so overlapping registry-years are not double-counted.

## Note on the scripts
`fetch_fulltext.py` only *retrieves* — it never invents content; unreachable
records are logged as `no-oa-full-text`/`none`. Every eligibility decision and
every extracted value is entered by the author against the source PDF; the tools
prepare the material and leave those columns blank.
