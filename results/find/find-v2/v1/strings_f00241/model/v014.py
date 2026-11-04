def predict(probe):
    """Best current guess: delete uppercase B's that are part of a contiguous
    B-run adjacent to O/o, plus lone B. Evidence is confusing; this is a guess."""
    try:
        import re
        inputs = probe.get("inputs", [])
        out = []
        for x in inputs:
            s = str(x)
            # Delete any uppercase B that is adjacent (before or after) to O/o,
            # applied to fixpoint; also delete lone B (whole string is B's).
            prev = None
            while prev != s:
                prev = s
                s = re.sub(r"B(?=[Oo])", "", s)
                s = re.sub(r"(?<=[Oo])B", "", s)
            # lone B deletion: if string is all B's, delete them
            if s and all(c == 'B' for c in s):
                s = ""
            out.append(s)
        return {"outputs": out}
    except Exception:
        return {"outputs": []}
