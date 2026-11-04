def predict(probe):
    # Rules (from evidence):
    # 1. Strip leading/trailing whitespace from input [E1 " Zebralower"->"rrewolarbeZ", E2 "  leading"->"ggnidael", "trailing  "->"gniliart"]
    # 2. Split into words on whitespace; reverse each word [E1, E2]
    # 3. Prepend the last character of the stripped string to the LAST reversed word [E1 "yyzal", E2 "oowt","eeerht","bb","ffEd","6654","zz"]
    # 4. Join words with single space [E2 "a  b"->"a bb", "x y z"->"x y zz"]
    # 5. Empty/whitespace-only input -> "" (?)
    outs = []
    for x in probe.get("inputs", []):
        if not isinstance(x, str):
            outs.append("")
            continue
        s = x.strip()
        if not s:
            outs.append("")
            continue
        words = s.split()
        rev = [w[::-1] for w in words]
        rev[-1] = s[-1] + rev[-1]
        outs.append(" ".join(rev))
    return {"outputs": outs}
