def predict(probe):
    # f reverses the string, then inserts "2" at position ceil(n/2) [E1, E2]
    # "hello" -> "olleh" -> "oll"+"2"+"eh" = "oll2eh" [E1]
    # "a" -> "a" -> "a"+"2" = "a2" [E2]
    # "h" -> "h" -> "h"+"2" = "h2" [E2]
    # "" -> "" -> "2" [E2]
    # "ab" -> "ba" -> "b"+"2"+"a" = "b2a" [E2]
    # "xy" -> "yx" -> "y"+"2"+"x" = "y2x" [E2]
    # "xyz" -> "zyx" -> "zy"+"2"+"x" = "zy2x" [E2]
    # "abcd" -> "dcba" -> "dc"+"2"+"ba" = "dc2ba" [E2]
    # "abcdef" -> "fedcba" -> "fed"+"2"+"cba" = "fed2cba" [E2]
    # "1234" -> "4321" -> "432"+"2"+"1" = "43221" [E2]
    # split point = ceil(n/2): extra char goes to left half for odd length [E2]
    out = []
    for s in probe.get("inputs", []):
        r = s[::-1]
        n = len(r)
        h = (n + 1) // 2
        out.append(r[:h] + "2" + r[h:])
    return {"outputs": out}
