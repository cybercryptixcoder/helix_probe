def predict(probe):
    try:
        out = []
        for s in probe.get("inputs", []):
            r = []
            i = 0
            while i < len(s):
                ch = s[i]
                if ch == 'l':
                    # 'll' collapses to 'k'; single 'l' -> 'k'
                    if i + 1 < len(s) and s[i+1] == 'l':
                        r.append('k')
                        i += 2
                        continue
                    r.append('k')
                elif ch == 'L':
                    if i + 1 < len(s) and s[i+1] == 'L':
                        r.append('K')
                        i += 2
                        continue
                    r.append('K')
                elif ch == 'h':
                    r.append('g')
                elif ch == 'H':
                    r.append('G')
                elif ch == 'x':
                    r.append('w')
                elif ch == 'X':
                    r.append('W')
                elif ch == 'a':
                    r.append('z')
                elif ch == 'A':
                    r.append('Z')
                else:
                    r.append(ch)
                i += 1
            out.append(''.join(r))
        return {"outputs": out}
    except Exception:
        return {"outputs": []}
