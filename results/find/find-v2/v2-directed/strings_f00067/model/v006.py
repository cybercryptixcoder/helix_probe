def predict(probe):
    # Mechanism discovered from evidence:
    # 1. Split input into words on any whitespace, collapsing runs and trimming [E3, E9, E12]
    # 2. Reverse the characters of each word [E1, E2, E10]
    # 3. Double the first character of the reversed LAST word [E1, E4, E5, E6]
    # 4. EXCEPTION: if the original input ends with whitespace, no doubling [E7, E9, E12]
    # 5. Join reversed words with single spaces [E3, E9]
    # 6. Empty / whitespace-only input -> empty string [?]
    
    outputs = []
    for s in probe.get("inputs", []):
        try:
            outputs.append(_transform(s))
        except Exception:
            outputs.append("")
    return {"outputs": outputs}

def _transform(s):
    if not isinstance(s, str):
        s = str(s)
    ends_ws = len(s) > 0 and s[-1].isspace()
    words = s.split()
    if not words:
        return ""
    rev = [w[::-1] for w in words]
    if not ends_ws:
        rev[-1] = rev[-1][0] + rev[-1]
    return " ".join(rev)
