# Source verification log — extracted values vs. source full text

Prompted by a spot-check (Howlader 2014) that found 95% CIs recorded as
point-only. Two problems were then swept systematically:

## A. Overlooked 95% CIs (recorded point-only although the source reported them)
Fixed by propagating the source rate/IRR CIs; every point estimate reproduced
to <0.01, so no IRR or direction changed. RoB O2/O3 now met → these move
Poor→Good.

| rec | study | where the CI was | fixed |
|---|---|---|---|
| 2 | Howlader 2014 | Suppl Table 3 age-specific rate CIs (Fig 1 footnote) | ✓ |
| 200 | Gleason 2012 | Table 1 CIRW/CIRB 95% CI | ✓ |
| 265 | Anderson 2008 | explicit IRR (95% CI) column | ✓ |
| 346 | Richardson 2016 (MMWR) | Rate (95% CI) column | ✓ |
| 333 | Keegan 2010 | Table 1 Rate (95% CI) — see B | ✓ |

Confirmed genuinely point-only (source reports no CI): rec 381 (Lund), rec 485
(Harper — adjacent columns are Population %, not SE), rec 4098 (McCracken — 0 CI
in paper).

## B. Wrong values picked at extraction (not a CI issue)
| rec | study | error | correction |
|---|---|---|---|
| 333 | Keegan 2010 | used a SES-subgroup rate 88.3 and an NHW rate 134.0 absent from the table → IRR 0.659 | overall Hispanic 78.3 (77.4–79.1) / NHW 125.7 (125.1–126.2) → **IRR 0.623 [0.616, 0.630]** |
| 203 | Brinton 2008 | aggregate-vs-NHW (146.9/173.2) and age≥50 (394.9/478.6) rates are not in this younger-women paper | untraceable rows **removed**; verified age<40 row (IRR 1.53 [1.35,1.74], matches paper's 1.52 [1.34,…]) kept. age≥50 Black representative re-selected → Harper 2009 |

## C. Systematic cross-check (extracted rate/IRR must appear in the source PDF)
Automated match of every extracted value against the source full text.

- **27 records with local full text: all pass (0 flags)** after A+B.
- **16 records without local full text: not verifiable by this method** —
  rec 10, 28, 51, 107, 146, 155, 161, 169, 234, 286, 324, 500, 522, 2131, 2406, 4040.
  (rec 234 Gomez 2026 and rec 324 Gomez 2017 CIs are directly reported and were
  transcribed as such; still, full-text confirmation is pending PDFs.)

Statistics are unaffected by A (labels/CIs only); B changes two Hispanic/Black
point estimates in overlap/sensitivity cells and drops two untraceable rows.
