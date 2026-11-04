def predict(probe):
    """Reverses each input string and inserts '2' at the middle position."""
    try:
        inputs = probe.get("inputs", [])
        outputs = []
        for s in inputs:
            try:
                s = str(s)
            except Exception:
                s = ""
            rev = s[::-1]
            n = len(rev)
            mid = (n + 1) // 2
            outputs.append(rev[:mid] + "2" + rev[mid:])
        return {"outputs": outputs}
    except Exception:
        return {"outputs": []}
