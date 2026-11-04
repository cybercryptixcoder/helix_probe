def predict(probe):
    try:
        out = []
        for s in probe.get("inputs", []):
            r = []
            for ch in s:
                if ch == 'l':
                    continue
                elif ch == 'h':
                    r.append('g')
                elif ch == 'x':
                    r.append('w')
                elif ch == 'a':
                    r.append('z')
                else:
                    r.append(ch)
            out.append(''.join(r))
        return {"outputs": out}
    except Exception:
        return {"outputs": []}
