def predict(probe):
    try:
        out = []
        for s in probe["inputs"]:
            r = s[::-1]
            if " " in s:
                # Observed: I goes at front of reversed string for space-containing inputs
                # Special case: '  hi  ' -> 'iIh' suggests spaces stripped then middle insert
                stripped = s.replace(" ", "")
                if stripped != s and stripped != "":
                    rs = stripped[::-1]
                    i = (len(rs) + 1) // 2
                    out.append(rs[:i] + "I" + rs[i:])
                else:
                    out.append("I" + r)
            else:
                i = (len(r) + 1) // 2
                out.append(r[:i] + "I" + r[i:])
        return {"outputs": out}
    except Exception:
        return {"outputs": []}
