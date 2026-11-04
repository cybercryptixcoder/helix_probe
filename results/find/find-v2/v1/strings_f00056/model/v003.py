def predict(probe):
    try:
        out = []
        for s in probe.get("inputs", []):
            r = []
            i = 0
            while i < len(s):
                ch = s[i]
                if ch == 'l':
                    while i + 1 < len(s) and s[i+1] == 'l':
                        i += 1
                    r.append('k')
                elif ch == 'L':
                    while i + 1 < len(s) and s[i+1] == 'L':
                        i += 1
                    r.append('K')
                elif ch == 'h':
                    r.append('g')
                elif ch == 'H':
                    r.append('G')
                elif ch == 'w':
                    r.append('v')
                elif ch == 'W':
                    r.append('V')
                else:
                    r.append(ch)
                i += 1
            out.append(''.join(r))
        return {"outputs": out}
    except Exception:
        return {"outputs": []}
