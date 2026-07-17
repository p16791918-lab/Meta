#!/usr/bin/env python3
"""Reflow citation numbers to strict order-of-appearance (PLOS Vancouver style).

Reads MANUSCRIPT.md (body, up to the '## References' header) to find every
inline [n] / [n-m] / [n,m] citation token in document order, builds an
old->new number map from first appearance, then rewrites:
  * the inline markers in MANUSCRIPT.md, and
  * REFERENCES.md into a flat list ordered 1..N by first appearance.

The A/B/C/D grouping in REFERENCES.md (quantitative/narrative/excluded/methods)
is preserved as an inline tag on each entry so provenance is not lost.
"""
import re

CITE = re.compile(r'\[(\d[\d,\s–-]*)\]')   # [4,16]  [1–8,12]  not [Fig 1]
CODE = re.compile(r'`[^`]*`')              # inline code span (search queries)
REF_LINE = re.compile(r'^(\d+)\.\s+(.*)$')


def outside_code(text, fn):
    """Apply fn to every non-code-span segment; leave `code spans` untouched."""
    out, last = [], 0
    for m in CODE.finditer(text):
        out.append(fn(text[last:m.start()]))
        out.append(m.group(0))
        last = m.end()
    out.append(fn(text[last:]))
    return ''.join(out)


def parse_group(inner):
    """'1–8,12' -> [1,2,3,4,5,6,7,8,12] (order preserved, ranges expanded)."""
    nums = []
    for part in inner.split(','):
        part = part.strip().replace('–', '-')
        if not part:
            continue
        if '-' in part:
            a, b = part.split('-')
            nums.extend(range(int(a), int(b) + 1))
        else:
            nums.append(int(part))
    return nums


def compress(sorted_nums):
    """[1,3,4,5,6,12] -> '1,3–6,12' (en-dash for ranges)."""
    out, i, n = [], 0, len(sorted_nums)
    while i < n:
        j = i
        while j + 1 < n and sorted_nums[j + 1] == sorted_nums[j] + 1:
            j += 1
        if j - i >= 1:
            out.append(f'{sorted_nums[i]}–{sorted_nums[j]}')
        else:
            out.append(str(sorted_nums[i]))
        i = j + 1
    return ','.join(out)


def build_map(body):
    old_to_new, nxt = {}, [1]

    def scan(seg):
        for m in CITE.finditer(seg):
            for old in parse_group(m.group(1)):
                if old not in old_to_new:
                    old_to_new[old] = nxt[0]
                    nxt[0] += 1
        return seg
    outside_code(body, scan)
    return old_to_new


def rewrite_body(body, old_to_new):
    def repl(m):
        new_nums = sorted(old_to_new[o] for o in parse_group(m.group(1)))
        return '[' + compress(new_nums) + ']'
    return outside_code(body, lambda seg: CITE.sub(repl, seg))


def category_tag(section):
    return {
        'A': 'quantitative', 'B': 'narrative',
        'C': 'excluded', 'D': 'method',
    }.get(section, '')


def load_references(path='REFERENCES.md'):
    """Return {old_num: (text, category)} from REFERENCES.md."""
    refs, section = {}, ''
    for line in open(path, encoding='utf-8'):
        s = line.rstrip('\n')
        hm = re.match(r'^## ([A-D])\.', s)
        if hm:
            section = hm.group(1)
            continue
        m = REF_LINE.match(s)
        if m:
            refs[int(m.group(1))] = (m.group(2).rstrip(), section)
    return refs


def write_references(refs, old_to_new, path='REFERENCES.md'):
    new_to_old = {v: k for k, v in old_to_new.items()}
    lines = [
        '# References — PLOS ONE numbered style (order of appearance)',
        '',
        'Numbered by first appearance in the manuscript body. The bracketed tag '
        'on each entry records its synthesis role (quantitative / narrative / '
        'excluded / method). All entries verified from full-text metadata; see '
        '`EXTRACTION_LOG.md` for provenance.',
        '',
    ]
    for new in range(1, len(new_to_old) + 1):
        old = new_to_old[new]
        text, section = refs[old]
        tag = category_tag(section)
        lines.append(f'{new}. {text}  *[{tag}]*' if tag else f'{new}. {text}')
        lines.append('')
    open(path, 'w', encoding='utf-8').write('\n'.join(lines).rstrip() + '\n')


def main():
    src = open('MANUSCRIPT.md', encoding='utf-8').read()
    split = src.split('\n## References', 1)
    body = split[0]
    tail = '\n## References' + split[1] if len(split) > 1 else ''

    old_to_new = build_map(body)
    refs = load_references()

    missing_body = set(refs) - set(old_to_new)
    if missing_body:
        raise SystemExit(f'References never cited in body: {sorted(missing_body)}')
    missing_ref = set(old_to_new) - set(refs)
    if missing_ref:
        raise SystemExit(f'Cited numbers with no reference entry: {sorted(missing_ref)}')

    new_body = rewrite_body(body, old_to_new)

    # Rewrite the References-section note so its bracketed tokens are not stale.
    tail = re.sub(
        r'The full reference list.*?PLOS ONE uses numbered \(Vancouver\) citations\.\*',
        'The full reference list (Vancouver / PLOS ONE numbered style) is in '
        '`REFERENCES.md`; in-text citation numbers are in strict order of first '
        'appearance and correspond one-to-one to that list.',
        tail, flags=re.S)
    tail = re.sub(
        r'The full reference list \(Vancouver / PLOS ONE numbered style\) is in `REFERENCES\.md`;.*',
        'The full reference list (Vancouver / PLOS ONE numbered style) is in '
        '`REFERENCES.md`; in-text citation numbers are in strict order of first '
        'appearance and correspond one-to-one to that list.',
        tail, flags=re.S)

    open('MANUSCRIPT.md', 'w', encoding='utf-8').write(new_body + tail)
    write_references(refs, old_to_new)

    print('old -> new citation map:')
    for old in sorted(old_to_new):
        print(f'  {old:>2} -> {old_to_new[old]:>2}')
    print(f'total references: {len(old_to_new)}')


if __name__ == '__main__':
    main()
