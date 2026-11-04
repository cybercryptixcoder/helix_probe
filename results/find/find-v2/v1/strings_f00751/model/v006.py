def predict(probe):
    """Strip leading/trailing spaces and tabs, then insert 'i'.
    If the original had leading whitespace, insert at index 0 of stripped content;
    otherwise insert at index len//2 (empty -> 'i')."""
    try:
        results = []
        for s in probe.get("inputs", []):
            if not isinstance(s, str):
                s = str(s)
            t = s.strip(" \t")
            if t == "":
                results.append("i")
                continue
            had_leading = len(s) > 0 and s[0] in " \t"
            if had_leading:
                k = 0
            else:
                k = len(t) // 2
            results.append(t[:k] + "i" + t[k:])
        return {"outputs": results}
    except Exception:
        return {"outputs": []}
