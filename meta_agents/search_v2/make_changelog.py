#!/usr/bin/env python3
"""Build a reviewer's guide to what changed in the manuscript prose.

The supervisor reads the manuscript, not the repository, so a list of commits is
no use to them. This walks the git history over a range and, for every paragraph
of the manuscript drafts that changed, prints where it is, a phrase to search for
in the Word or PDF file, the sentences before and after, and why.

    python3 make_changelog.py                  # since the 5th-round feedback
    python3 make_changelog.py <base>[..<head>] # any range
    python3 make_changelog.py --round 4        # since the Nth-round feedback

Writes outputs/Changes_for_review.md; outputs/build_changelog_docx.js renders it.
Paragraphs are matched between the two versions so that a rewritten paragraph is
reported as one change rather than as a deletion and an insertion.
"""
import difflib
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "outputs")
DRAFTS = ["Abstract", "Introduction", "Methods", "Results", "Discussion"]
# git names paths from the repository root, which is above this directory.
PREFIX = subprocess.run(["git", "rev-parse", "--show-prefix"], cwd=HERE,
                        capture_output=True, text=True).stdout.strip()
FILES = [PREFIX + "manuscript/%s_draft.md" % d for d in DRAFTS]
# The commit that added each round's feedback file marks where that round begins.


def git(*args):
    return subprocess.run(["git"] + list(args), cwd=HERE, capture_output=True,
                          text=True).stdout


def round_base(n):
    """First commit of the Nth feedback round: the one that added its file."""
    # ":/" makes the pathspec relative to the repository root, not this directory.
    path = ":/Advice/" + ("Feedback" if str(n) == "1" else "Feedback%s.md" % n)
    out = git("log", "--format=%H", "--diff-filter=A", "--", path).split()
    return out[-1] if out else None


def show(rev, path):
    r = subprocess.run(["git", "show", "%s:%s" % (rev, path)], cwd=HERE,
                       capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


def paragraphs(text):
    """[(section heading, paragraph text)], with wrapped lines joined.

    The drafts are hard-wrapped, so a diff by line reports fragments; joining a
    paragraph first makes the before/after readable as prose.
    """
    out, sec, buf = [], "", []
    for line in text.split("\n"):
        if line.startswith("#"):
            if buf:
                out.append((sec, " ".join(buf).strip())); buf = []
            sec = line.lstrip("#").strip()
        elif line.strip() == "":
            if buf:
                out.append((sec, " ".join(buf).strip())); buf = []
        else:
            buf.append(line.strip())
    if buf:
        out.append((sec, " ".join(buf).strip()))
    return [(s, p) for s, p in out if p and not p.startswith("|")]


def sentences(p):
    return [x.strip() for x in re.split(r"(?<=[.;:])\s+(?=[A-Z(])", p) if x.strip()]


def locator(p, n=12):
    """A phrase to search for in the built document."""
    words = re.sub(r"\s+", " ", p).split()
    return " ".join(words[:n]) + ("…" if len(words) > n else "")


def sentence_diff(old, new):
    """The sentences that differ, as (removed, added) lists."""
    a, b = sentences(old), sentences(new)
    rm, add = [], []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b).get_opcodes():
        if tag in ("replace", "delete"):
            rm += a[i1:i2]
        if tag in ("replace", "insert"):
            add += b[j1:j2]
    return rm, add


def changes(base, head):
    """[(commit subject, file, section, kind, before, after)] oldest first."""
    revs = git("rev-list", "--reverse", "%s..%s" % (base, head)).split()
    found = []
    for rev in revs:
        subject = git("log", "-1", "--format=%s", rev).strip()
        touched = git("show", "--name-only", "--format=", rev).split("\n")
        for path in FILES:
            if not any(t.endswith(path) for t in touched):
                continue
            before, after = show(rev + "^", path), show(rev, path)
            if before is None or after is None:
                continue
            pa, pb = paragraphs(before), paragraphs(after)
            ta, tb = [p for _, p in pa], [p for _, p in pb]
            for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, ta, tb).get_opcodes():
                if tag == "equal":
                    continue
                # Pair rewritten paragraphs so an edit reads as one change.
                for k in range(max(i2 - i1, j2 - j1)):
                    o = ta[i1 + k] if i1 + k < i2 else ""
                    n = tb[j1 + k] if j1 + k < j2 else ""
                    sec = (pb[j1 + k][0] if j1 + k < j2 else pa[i1 + k][0])
                    kind = "수정" if o and n else ("추가" if n else "삭제")
                    found.append((subject, path, sec, kind, o, n))
    return found


def main():
    arg = sys.argv[1] if len(sys.argv) > 1 else None
    if arg == "--round":
        base, head = round_base(sys.argv[2]), "HEAD"
    elif arg and ".." in arg:
        base, head = arg.split("..", 1)
        head = head or "HEAD"
    elif arg:
        base, head = arg, "HEAD"
    else:
        base, head = round_base("5"), "HEAD"
    if not base:
        raise SystemExit("could not resolve a base commit")

    rows = changes(base, head)
    lines = ["# 본문 수정 내역 (검토용)", ""]
    lines.append("원고 본문에서 바뀐 문단만 모았습니다. **찾기** 항목을 Word나 PDF에서 "
                 "Ctrl+F로 검색하면 해당 문단으로 바로 갑니다. 표·그림·보충자료의 "
                 "수치 변경은 피드백 응답서에 있습니다.")
    lines.append("")
    lines.append("범위: `%s` … `%s` (%d개 문단)" % (base[:7], head, len(rows)))
    lines.append("")

    by_file = {}
    for r in rows:
        by_file.setdefault(r[1], []).append(r)
    for path in FILES:
        rs = by_file.get(path)
        if not rs:
            continue
        lines += ["---", "", "## %s" % os.path.basename(path).replace("_draft.md", ""), ""]
        for i, (subject, _p, sec, kind, old, new) in enumerate(rs, 1):
            lines.append("### %d. %s — %s" % (i, sec or "(머리말)", kind))
            lines.append("")
            rm, add = sentence_diff(old, new) if kind == "수정" else ([], [])
            # Point at the sentence that changed, not at the top of the paragraph:
            # a long paragraph is hard to search for and hard to find within.
            target = add[0] if add else new
            if target:
                lines.append("**찾기:** `%s`" % locator(target))
                lines.append("")
            if kind == "수정":
                if rm:
                    lines.append("**변경 전**")
                    lines += ["- " + x for x in rm] + [""]
                if add:
                    lines.append("**변경 후**")
                    lines += ["- " + x for x in add] + [""]
                if not rm and not add:
                    lines += ["(줄바꿈만 변경)", ""]
            elif kind == "추가":
                lines += ["**추가된 문단**", new, ""]
            else:
                lines += ["**삭제된 문단**", old, ""]
            lines.append("*사유: %s*" % subject)
            lines.append("")

    dst = os.path.join(OUT, "Changes_for_review.md")
    open(dst, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print("wrote outputs/Changes_for_review.md — %d changed paragraphs across %d files"
          % (len(rows), len(by_file)))


if __name__ == "__main__":
    main()
