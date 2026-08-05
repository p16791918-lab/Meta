# Search day — step-by-step checklist

Search strings are in `SEARCH_STRINGS_v2.md`. Run everything on the **same day**
and write that date down (it goes in the Methods and PROSPERO).

## 0. Before searching
- [ ] Record today's date = the search date.
- [ ] (Supervisor) PROSPERO amendment submitted before/at the start of searching.
- [ ] Have `SEARCH_STRINGS_v2.md` open.

## 1. MEDLINE + Embase  — PRIMARY screening corpus  (Embase platform)
- [ ] Log in to **Embase.com**.
- [ ] In Search, enable **"Embase + MEDLINE"** (so MEDLINE records are included).
- [ ] Paste the string from **§2** of SEARCH_STRINGS_v2.md.
- [ ] Apply limits if not already in the string: 2000–2025, English, humans; exclude
      review/case report/editorial/note/conference abstract.
- [ ] **Write down the hit count.**  MEDLINE+Embase = ______
- [ ] **Export ALL records** → CSV or RIS. Fields required:
      **Title, Abstract, Author names, Publication year, Source (journal),
      Publication type, PMID, DOI.**  → save the file (this is what I process).
      *(If there are thousands, export in batches and keep all files.)*

## 2. Scopus  (coverage / comprehensiveness)
- [ ] Scopus → Advanced Search → paste **§3**.
- [ ] **Write down the hit count.**  Scopus = ______
- [ ] Export optional (count is enough for now; export CSV if easy —
      Title, Abstract, Authors, Year, Source, DOI, PubMed ID, Document type).
      *(Scopus caps CSV export at 2,000 per run — batch if needed.)*

## 3. Web of Science Core Collection  (coverage)
- [ ] WoS → Advanced Search → paste **§4** (TS= version).
- [ ] **Write down the hit count.**  WoS = ______
- [ ] Export optional (count is enough; export as tab-delimited/RIS if easy —
      include PM = PubMed ID and DT = document type).
      *(WoS caps export at 1,000 per run — batch if needed.)*

## 4. After searching — send me
- [ ] The three hit counts (MEDLINE+Embase / Scopus / WoS) — for the PRISMA
      "Identification" box.
- [ ] The **MEDLINE+Embase export file** (required — this is the screening set).
- [ ] Scopus / WoS export files if you made them (optional).
- [ ] The exact search date.

Then I will: normalize → de-duplicate (report duplicates removed + unique n) →
run two-stage screening → extract any newly eligible studies → re-run the
analysis and update the PRISMA flow, counts, and Methods.

## Practical notes
- Keep the **exact query text** you pasted for each platform (copy into a note) —
  it goes verbatim into Supplementary Table 1.
- Document-type exclusions are already in the strings; if a platform ignores them,
  they get removed at screening instead — that's fine.
- If Embase.com export options differ, prioritise getting **Abstract + PMID + DOI**;
  those drive de-duplication and screening.
