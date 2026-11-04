def predict(probe):
    # Mechanism: append 'h' to the input, then keep only the FIRST occurrence
    # of each character (case-sensitive), preserving order. [E1-E6 all consistent]
    # - "abcdefghij" -> "abcdefghijh" -> dedupe drops 2nd h -> "abcdefghij" [E4]
    # - "hh" -> "hhh" -> "h"; "h" -> "hh" -> "h" [E2]
    # - "level" -> "levelh" -> "levh" [E1]
    # - "a b a b" -> "a b a bh" -> "a bh" [E2]
    # - "mississippi" -> "mississippih" -> "misph" [E4]
    # - "Hh" -> "Hhh" -> "Hh" (case-sensitive: H != h) [E2]
    outputs = []
    for s in probe.get("inputs", []):
        t = s + "h"
        seen = set()
        result = []
        for ch in t:
            if ch not in seen:
                seen.add(ch)
                result.append(ch)
        outputs.append("".join(result))
    return {"outputs": outputs}
