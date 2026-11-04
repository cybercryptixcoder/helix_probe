def predict(probe):
    # Keep only first occurrence of each char, case-sensitive, in order [E1 all 6]
    # Then append 'h' if lowercase 'h' not already present [E1: 'data a Python ' has h -> no append; others get h]
    # 'H' uppercase does NOT count as 'h' [E1: 'Mississippi Hello World data' -> ...Wrdath]
    results = []
    for s in probe["inputs"]:
        seen = set()
        out = []
        for ch in s:
            if ch not in seen:
                seen.add(ch)
                out.append(ch)
        res = "".join(out)
        if "h" not in res:
            res += "h"
        results.append(res)
    return {"outputs": results}
