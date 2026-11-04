import re

def predict(probe):
    """Remove all Unicode whitespace, then append 'F' unless result already ends in 'F'."""
    try:
        inputs = probe.get("inputs", [])
        outputs = []
        for s in inputs:
            try:
                t = re.sub(r"\s+", "", s)
                if not t.endswith("F"):
                    t = t + "F"
                outputs.append(t)
            except Exception:
                outputs.append("F")
        return {"outputs": outputs}
    except Exception:
        return {"outputs": []}
