def predict(probe):
    try:
        results = []
        for s in probe.get("inputs", []):
            if not isinstance(s, str):
                s = str(s)
            orig_len = len(s)
            t = s.strip(" \t")
            if t == "":
                results.append("i")
                continue
            lead_ws = 0
            for ch in s:
                if ch in " \t":
                    lead_ws += 1
                else:
                    break
            trail_ws = 0
            for ch in reversed(s):
                if ch in " \t":
                    trail_ws += 1
                else:
                    break
            if lead_ws == 0:
                k = len(t) // 2
                if trail_ws > 0 and len(t) % 2 == 1:
                    k = k + 1
            else:
                r = orig_len // 2 - lead_ws
                k = r if r >= 0 else -r
            if k < 0:
                k = 0
            if k > len(t):
                k = len(t)
            results.append(t[:k] + "i" + t[k:])
        return {"outputs": results}
    except Exception:
        return {"outputs": []}
