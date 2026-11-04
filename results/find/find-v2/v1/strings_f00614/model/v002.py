import re

def predict(probe):
    """Best guess: remove all whitespace, then append 'F'."""
    try:
        inputs = probe.get("inputs", [])
        outputs = []
        for s in inputs:
            try:
                outputs.append(re.sub(r"\s+", "", s) + "F")
            except Exception:
                outputs.append("F")
        return {"outputs": outputs}
    except Exception:
        return {"outputs": []}
