#!/usr/bin/env python3
"""Build the registry-overlap characterization table (Table S-A) for included
studies, so non-independent (overlapping) registry data can be collapsed to one
representative estimate per registry family in the quantitative synthesis.

For each included study (ft_eligibility.csv include-*), extract from the full text:
  - registry system  : SEER version(s), USCS(NPCR+SEER), NAACCR/CiNA, or the
                        state/regional registry named in ft_eligibility.
  - study period      : preferring an explicit "diagnosed from X to/through Y"
                        statement; year-range fallbacks are flagged (verify).
  - US coverage       : "% of the US population" if stated.
SEER version -> geographic scope is a fixed lookup (version defines the registries).

Output: TableSA_registry_overlap.csv  (record_id, citation, registry_family,
        seer_version, study_period, pct_us, coverage_note, verify).
"""
import csv
import os
import re
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
MERGED = os.path.join(HERE, "merged_unique.csv")
ELIG = os.path.join(HERE, "ft_eligibility.csv")
OUT = os.path.join(HERE, "TableSA_registry_overlap.csv")

# SEER version -> approximate geographic scope (version defines the registry set)
SEER_SCOPE = {
    "9": "SEER9 ~10% US (SF, CT, Detroit, HI, IA, NM, Seattle, UT, Atlanta; 1975+)",
    "12": "SEER12 (+San Jose, LA, rural GA, AK Native)",
    "13": "SEER13 ~14% US (+LA, San Jose-Monterey, rural GA, AK Native; 1992+)",
    "17": "SEER17 ~26% US (+Greater CA, KY, LA, NJ, GA; 2000+)",
    "18": "SEER18 ~28% US (SEER17 + Greater GA)",
    "21": "SEER21 ~37% US (+ID, MA, etc.)",
    "22": "SEER22 ~48% US (expanded)",
}


def scan(rid):
    p = os.path.join(HERE, "fulltext", "%d.txt" % rid)
    if not os.path.isfile(p):
        return None
    t = open(p, encoding="utf-8").read()
    body = t.split("\n\n", 1)[1] if "\n\n" in t else t

    versions = sorted(set(re.findall(r"SEER[\s-]?(\d\d?)\b", body)),
                      key=lambda x: int(x))
    versions = [v for v in versions if v in SEER_SCOPE]  # drop stray numbers
    uscs = bool(re.search(r"\bUSCS\b|U\.?S\.? Cancer Statistics|National Program of Cancer Registries|\bNPCR\b", body))
    naaccr = bool(re.search(r"\bNAACCR\b|\bCiNA\b|North American Association of Central", body))

    # study period: prefer an explicit diagnosis-window statement
    period, verify = "", ""
    m = re.search(r"diagnos\w+[^.]{0,60}?\b(19[7-9]\d|20[0-2]\d)\s*(?:to|through|[–\-—])\s*(20[0-2]\d|19[7-9]\d)\b",
                  body, re.I)
    if not m:
        m = re.search(r"\b(?:from|during|between)\s+(19[7-9]\d|20[0-2]\d)\s*(?:to|through|and|[–\-—])\s*(20[0-2]\d|19[7-9]\d)\b",
                      body, re.I)
    if m:
        period = "%s-%s" % (m.group(1), m.group(2))
    else:
        ranges = Counter("%s-%s" % (a, b) for a, b in
                         re.findall(r"\b(19[7-9]\d|20[0-2]\d)\s*[–\-—]\s*(20[0-2]\d|19[7-9]\d)\b", body))
        if ranges:
            period = ranges.most_common(1)[0][0]
            verify = "period auto-guess - verify"

    pct = re.findall(r"(\d{1,2}(?:\.\d)?)\s*%\s*of the (?:total\s+)?U\.?S\.?(?:\s|-)?population", body, re.I)
    return {
        "seer_version": ",".join("SEER" + v for v in versions),
        "uscs": uscs, "naaccr": naaccr,
        "period": period, "verify": verify,
        "pct_us": pct[0] if pct else "",
        "scope": "; ".join(SEER_SCOPE[v] for v in versions),
    }


def registry_family_norm(fam, system):
    """Collapse to a coarse registry FAMILY for overlap grouping (per Feedback 5)."""
    s = (fam + " " + system).lower()
    if "alaska native" in s or "antr" in s:
        return "Alaska-Native-Registry"
    if "navajo" in s:
        return "Navajo/IHS"
    if "california cancer registry" in s or "ccr" in s or "greater bay" in s or "la county" in s or "csp" in s:
        return "California-CCR"
    if "hawaii" in s or "htr" in s:
        return "Hawaii-HTR"
    if "guam" in s or "pacific regional" in s or "prccr" in s:
        return "Pacific-PRCCR"
    if "multiethnic cohort" in s or "mec" in s or "aarp" in s or "kaiser" in s or "hchs" in s or "earth" in s or "rochester" in s or "cohort" in s:
        return "Cohort(non-registry)"
    if "uscs" in s or "npcr" in s:
        return "USCS(NPCR+SEER~99%)"
    if "naaccr" in s or "cina" in s:
        return "NAACCR(~93%)"
    if "seer" in s:
        return "SEER-national"
    for st in ["wisconsin", "pennsylvania", "connecticut", "new mexico", "texas",
               "north carolina", "florida", "detroit", "minnesota", "massachusetts",
               "arizona", "michigan", "new york", "south carolina", "ohio", "northern plains", "state cancer profiles"]:
        if st in s:
            return "State/regional:" + st
    return "UNSPECIFIED"


def outcome_dimension(groups, note):
    s = (groups + " " + note).lower()
    if re.search(r"\bmen\b|male breast", s):
        return "male-BC"
    if re.search(r"tnbc|triple[- ]neg|er[-/ ]|hr[-+/]|her2|subtype|lobular|\bilc\b|ductal|\bibc\b|inflammatory|molecular|histolog", s):
        return "subtype"
    if re.search(r"chinese|japanese|korean|filipino|vietnamese|cambodian|hmong|south asian|asian indian|pakistani|hawaiian|chamorro|pacific|okinawa|aanhpi|asian american|api\b", s):
        return "disaggregated-AANHPI"
    if re.search(r"navajo|seneca|american indian|alaska native|ai/an|aian", s):
        return "AIAN"
    if re.search(r"cuban|mexican|puerto|nativity|heritage|enclave|hispanic", s):
        return "Hispanic-origin"
    if re.search(r"middle eastern|arab", s):
        return "MiddleEastern-Arab"
    if re.search(r"ghanaian|somali|sub-saharan|african-born|african descent", s):
        return "African-born"
    if re.search(r"\bnhb\b|\bnhw\b|black|white|caucasian|european american", s):
        return "aggregate-BlackWhite"
    return "aggregate-multi"


def _cov_rank(x):
    """Higher = more comprehensive coverage (for representative selection)."""
    fam = x["registry_family_norm"]
    order = {"USCS(NPCR+SEER~99%)": 6, "NAACCR(~93%)": 5, "SEER-national": 4}
    base = order.get(fam, 2)
    try:
        pct = float(x["pct_us"]) if x["pct_us"] else 0
    except ValueError:
        pct = 0
    return (base, pct)


def _period_len(p):
    m = re.match(r"(\d{4})-(\d{4})", p or "")
    if not m:
        return (0, 0)
    a, b = int(m.group(1)), int(m.group(2))
    return (b - a, b)  # length, recency


def main():
    recs = list(csv.DictReader(open(MERGED, encoding="utf-8")))
    elig = list(csv.DictReader(open(ELIG, encoding="utf-8")))
    out = []
    for r in elig:
        dec = r.get("ft_decision", "")
        if not dec.startswith("include"):
            continue
        rid = int(r["record_id"])
        s = scan(rid) or {"seer_version": "", "uscs": False, "naaccr": False,
                          "period": "", "verify": "", "pct_us": "", "scope": ""}
        rec = recs[rid]
        system = s["seer_version"]
        if s["uscs"]:
            system = (system + " + " if system else "") + "USCS(NPCR+SEER ~99%)"
        if s["naaccr"] and "NAACCR" not in system:
            system = (system + " + " if system else "") + "NAACCR/CiNA(~93%)"
        fam_norm = registry_family_norm(r.get("registry_family", ""), system)
        dim = outcome_dimension(r.get("groups_vs_nhw", ""), r.get("note", ""))
        out.append({
            "record_id": rid,
            "citation": "%s (%s)" % (rec.get("title", "")[:60], rec.get("year", "")),
            "registry_family": r.get("registry_family", ""),
            "registry_family_norm": fam_norm,
            "registry_system_detected": system or "(state/regional)",
            "study_period": s["period"],
            "pct_us": s["pct_us"],
            "outcome_dimension": dim,
            "synthesis": "quantitative" if dec == "include-quant" else "narrative",
            "overlap_cluster": "%s | %s" % (fam_norm, dim),
        })

    # Representative selection per overlap cluster (Feedback 5): among quantitative
    # studies in a cluster, pick widest coverage -> longest -> most recent period.
    from collections import defaultdict
    clusters = defaultdict(list)
    for x in out:
        if x["synthesis"] == "quantitative":
            clusters[x["overlap_cluster"]].append(x)
    reps = {}
    for cl, members in clusters.items():
        best = max(members, key=lambda x: (_cov_rank(x), _period_len(x["study_period"])))
        reps[cl] = best["record_id"]
    for x in out:
        if x["synthesis"] != "quantitative":
            x["main_analysis"], x["representative_reason"] = "no (narrative)", "narrative synthesis only"
        elif reps.get(x["overlap_cluster"]) == x["record_id"]:
            n = sum(1 for m in clusters[x["overlap_cluster"]])
            x["main_analysis"] = "yes (representative)"
            x["representative_reason"] = ("widest coverage/longest-recent period in cluster (%d studies)" % n) if n > 1 else "sole study in cluster"
        else:
            x["main_analysis"] = "no (overlaps representative)"
            x["representative_reason"] = "collapses to rep %d (same registry-family x outcome)" % reps[x["overlap_cluster"]]

    out.sort(key=lambda x: (x["overlap_cluster"], x["record_id"]))
    cols = ["record_id", "citation", "registry_family", "registry_family_norm",
            "registry_system_detected", "study_period", "pct_us", "outcome_dimension",
            "overlap_cluster", "synthesis", "main_analysis", "representative_reason"]
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(out)
    nq = sum(1 for x in out if x["synthesis"] == "quantitative")
    print("registry-overlap rows: %d (quantitative %d)" % (len(out), nq))
    print("overlap clusters: %d ; main-analysis representatives: %d"
          % (len(clusters), len(reps)))
    print("PROVISIONAL: finalize after the 20 pending studies are assessed and author confirms.")


if __name__ == "__main__":
    main()
