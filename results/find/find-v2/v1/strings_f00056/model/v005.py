def predict(probe):
    try:
        out = []
        for s in probe.get("inputs", []):
            r = []
            i = 0
            prev_letter = False
            while i < len(s):
                ch = s[i]
                if ch in ('l', 'L'):
                    # collapse run
                    while i + 1 < len(s) and s[i+1] in ('l', 'L'):
                        i += 1
                    if not prev_letter:
                        r.append('k' if ch == 'l' else 'K')
                        prev_letter = True
                    else:
                        r.append(ch)
                        prev_letter = True
                elif ch == 'h':
                    r.append('g'); prev_letter = True
                elif ch == 'H':
                    r.append('G'); prev_letter = True
                elif ch == 'w':
                    r.append('v'); prev_letter = True
                elif ch == 'W':
                    r.append('V'); prev_letter = True
                else:
                    r.append(ch)
                    prev_letter = ch.isalpha()
                i += 1
            out.append(''.join(r))
        return {"outputs": out}
    except Exception:
        return {"outputs": []}
