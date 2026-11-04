def predict(probe):
    """Hypothesis: insert '2' after the 2nd character, and add 2 to the last character's ASCII code."""
    try:
        inputs = probe.get("inputs", [])
        outputs = []
        for s in inputs:
            if not isinstance(s, str):
                s = str(s)
            if len(s) == 0:
                outputs.append("")
                continue
            # Insert '2' after index 1 (second char)
            if len(s) >= 2:
                result = s[:2] + "2" + s[2:]
            else:
                result = s + "2"
            # Increment last character by +2
            last = result[-1]
            result = result[:-1] + chr(ord(last) + 2)
            outputs.append(result)
        return {"outputs": outputs}
    except Exception:
        return {"outputs": []}
