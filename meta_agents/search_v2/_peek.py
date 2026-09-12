import sys, re, os
for rid in sys.argv[1:]:
    p=f'fulltext/{rid}.txt'
    if not os.path.exists(p): print(f"\n##### {rid}: NO TEXT"); continue
    t=open(p,encoding='utf-8').read()
    body=t.split('\n\n',1)[1] if '\n\n' in t else t
    head='\n'.join(t.split('\n')[:3])
    print(f"\n################## rec {rid}  ({len(body)} chars) ##################")
    print(head)
    # lines with rate/incidence-by-race signals
    keys=re.compile(r'(per 100,?000|age-adjusted|age-standardized|incidence rate|non-hispanic white|\bIRR\b|rate ratio|/100,?000|SEER|NAACCR|USCS|registry)', re.I)
    hits=[l.strip() for l in body.split('\n') if keys.search(l) and len(l.strip())>20]
    seen=set(); uniq=[]
    for h in hits:
        k=h[:60]
        if k not in seen: seen.add(k); uniq.append(h)
    for h in uniq[:22]: print("  |",h[:150])
