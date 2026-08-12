# Tables / supplementary materials to fetch

These studies are **include-quant** but their poolable numbers are not in the
available full text — the data lives in a Supplementary file, or in a table
that the flattened PMC text (or the PDF we have) does not contain. Extraction is
deferred until the item is obtained. Grab the linked PDF/supplement and drop it
in `fulltext/` as `<record>.pdf`, or paste the specific table.

## A. Highest priority (core dimensions)
| record | PMID | fetch this |
|--------|------|-----------|
| 2   | 24777111 | Kohler 2015 JNCI — **Supplementary Table 3** (age-adjusted incidence rate by race × subtype). Main PDF has only age-specific peaks. |
| 286 | 33074325 | Zhao 2020 — race × subtype rate table **with CIs**. ⚠️ paper reports IRR as NHW-vs-minority; invert for minority/NHW. |
| 155 | 36862439 | Scott 2023 — TNBC 95% CIs by race (we have point rates 25.2/12.9/11.2/11.1/9.0; need CIs). |
| 100 | 21351091 | Liu 2012 LA County — overall age-adjusted breast AAIR by Asian subgroup vs NHW (text has only age-scattered values). |
| 12  | 41086189 | race-specific breast incidence rates (only NHW 139.0 in text; NHB/AIAN/AAPI/Hispanic in Table 1). |
| 17  | 15986118 | Annual Report to the Nation — breast incidence rate by race (NAACCR/CiNA table). |

## B. Subtype / ER-PR tables
| record | PMID | fetch this |
|--------|------|-----------|
| 200 | 23166647 | race × ER/PR age-adjusted incidence rate table (full PDF). |
| 141 | 34508608 | ER-negative incidence table by race (full PDF). |
| 126 | 32804214 | race × molecular subtype incidence rate table (full PDF). |
| 405 | 23446808 | race × subtype trend/rate table. |
| 455 | 23907433 | race × subtype incidence table (has incidence + mortality — need incidence, get NHW). |
| 1336| (npj)    | recent subtype incidence by race — **no PDF locally**, fetch it. |

## C. Disaggregated / regional
| record | PMID | fetch this |
|--------|------|-----------|
| 49  | 16247793 | Hmong breast AAIR table (Hmong vs API vs NHW columns). |
| 54  | 33099777 | AIPA (Asian Indian/Pakistani) overall incidence IRR vs NHW (text has slopes/age only). |
| 701 | 39937364 | early-onset BC by region × race (regional table). |
| 1478| 41385397 | Navajo breast 60.9 — an NHW comparator for the same period (or confirm none reported). |
| 4058| 28553811 | White–Black 65+ breast incidence (age-stratified table). |
| 402 | 26741869 | African-American vs European-American breast rates. |
| 461 | 26320932 | race breast rates table. |
| 955 | 19067192 | race breast rates table. |

## D. Partial — extracted, just need the CI
| record | PMID | fetch this |
|--------|------|-----------|
| 2510| 31575554 | AI/AN vs white breast RR = 0.87 recorded; need its 95% CI from Table 3. |

## E. Verify (may not be usable)
| record | PMID | check |
|--------|------|-------|
| 436 | 42466659 | NHW rate 228.9 anomalously high (~1.6× normal); confirm definition (in-situ+invasive? age subset) before use. |
| 4026| 37119997 | confirm breast-by-race is actually reported, else exclude. |
| 4039| 16388524 | LIFETIME RISK (DevCan) by race — a separate outcome dimension, not an incidence IRR. |
