# Search day — step-by-step checklist (4 databases, all screened)

Search strings are in `SEARCH_STRINGS_v2.md` (§1 PubMed/MEDLINE, §2 Embase,
§3 Scopus, §4 Web of Science). Run all four on the **same day**; write that date
down (it goes in the Methods and PROSPERO). **Export all four** — every unique
record will be screened.

For every export, the key fields I need are: **Title · Abstract · Authors ·
Year · Source (journal) · DOI · PMID · Document/Publication type.**
Abstract + DOI + PMID drive de-duplication and screening — make sure they're in.

---

## 1. PubMed/MEDLINE  —  pubmed.ncbi.nlm.nih.gov
1. Paste the **§1** string into the search box → Search.
2. Write the count:  PubMed/MEDLINE = ______
3. **Export:** click **Save** (under the search bar) →
   - Selection: **All results**
   - Format: **PubMed**  ← this is the MEDLINE tagged .txt (includes AB abstract,
     PMID, and DOI). *(The "CSV" option does NOT include abstracts — don't use it.)*
   - → downloads a `.txt` file. Keep it.
   *(PubMed saves up to 10,000 at once — fine.)*

## 2. Embase  —  embase.com   (primary corpus)
1. Paste the **§2** string → Search. Apply limits if not in the string
   (2000–2025, English, humans; exclude review/case report/editorial/note/
   conference abstract).
2. Write the count:  Embase = ______
3. **Export:** top-right **Export** button →
   - Format: **CSV** (or RIS)
   - Content/fields: **Full Record** (or tick Title, Abstract, Author names,
     Source, Publication year, PMID, DOI, Publication type)
   - → download. *(If it caps per export, do it in batches and keep every file.)*

## 3. Scopus  —  scopus.com
1. **Advanced document search** → paste **§3** → Search.
2. Write the count:  Scopus = ______
3. **Export:** select **All** → **Export** → **CSV** →
   - Tick **Citation information** + **Abstract & keywords** (so abstracts come)
     + make sure **DOI** and **PubMed ID** are included.
   - → download. *(Scopus exports up to **2,000** rows per run — if more, sort and
     export in 2,000 batches: 1–2000, 2001–4000, … keep all files.)*

## 4. Web of Science Core Collection  —  webofscience.com
1. **Advanced Search** → paste **§4** (the TS= version) → Search.
2. Write the count:  WoS = ______
3. **Export:** **Export** → **Tab delimited file** (or RIS / Excel) →
   - Record Content: **Full Record** (so abstracts + DOI + PubMed ID come)
   - → download. *(WoS exports up to **1,000** per run — if more, do 1–1000,
     1001–2000, … keep all files.)*

---

## 5. After searching — send me
- [ ] The **four hit counts** (PubMed/MEDLINE / Embase / Scopus / WoS) + search date.
- [ ] **All four export files** (batches included). Embase is essential; the other
      three let me screen every unique record.

Then I will: normalize all four → cross-database **de-duplicate** (report duplicates
removed + unique n) → two-stage **screening** of every unique record → extract newly
eligible studies → re-run analysis and update PRISMA, counts, and Methods.

## Practical notes
- Copy the **exact query text** you pasted for each database into a note — it goes
  verbatim into Supplementary Table 1 (with platform, date, and count).
- If a platform ignores the document-type exclusions, they're removed at screening
  instead — fine.
- Don't worry about de-duplicating yourself — send raw exports; I handle overlap.
- File formats are flexible (CSV / RIS / tab / MEDLINE .txt) — I convert them.
