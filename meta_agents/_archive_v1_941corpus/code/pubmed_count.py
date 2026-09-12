"""
Print how many PubMed records the breast-cancer precise query actually returns,
so max_search_results can be set to capture the full set (not just the top-N).

Usage (Codespace, PubMed reachable):
  export NCBI_EMAIL=... NCBI_API_KEY=...
  python pubmed_count.py
"""
import os

QUERY = (
    '("Breast Neoplasms"[Mesh] OR "breast cancer"[tiab] OR "breast carcinoma"[tiab])'
    ' AND (race[ti] OR racial[ti] OR ethnic*[ti] OR minorit*[ti] OR disparit*[ti]'
    ' OR Black[ti] OR Hispanic[ti] OR White[ti] OR Asian[ti] OR "African American"[ti]'
    ' OR "Racial Groups"[Mesh] OR "Ethnicity"[Mesh] OR "Health Status Disparities"[Mesh])'
    ' AND (incidence[ti] OR "incidence rate"[tiab] OR "age-adjusted"[tiab]'
    ' OR "age-standardized"[tiab] OR "Incidence"[Mesh])'
    ' AND (2000:2025[dp]) AND English[lang] AND humans[MeSH]'
    ' NOT (review[pt] OR "case reports"[pt] OR comment[pt] OR editorial[pt] OR letter[pt])'
)


def main():
    from Bio import Entrez
    Entrez.email = os.getenv("NCBI_EMAIL", "researcher@example.com")
    key = os.getenv("NCBI_API_KEY", "")
    if key:
        Entrez.api_key = key
    h = Entrez.esearch(db="pubmed", term=QUERY, retmax=0)
    rec = Entrez.read(h)
    h.close()
    print(f"PubMed total results for the breast-cancer precise query: {rec['Count']}")


if __name__ == "__main__":
    main()
