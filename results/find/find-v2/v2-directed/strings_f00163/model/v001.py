def predict(probe):
    # f reverses the string, then inserts "2" between the two halves [E1]
    # "hello" -> "olleh" -> "oll" + "2" + "eh" = "oll2eh" [E1]
    # "world" -> "dlrow" -> "dlr" + "2" + "ow" = "dlr2ow" [E1]
    # "123"   -> "321"   -> "32"  + "2" + "1"  = "3221"   [E1]
    # "!?"    -> "?!"    -> "?"   + "2" + "!"  = "?2!"    [E1]
    # "a1b2"  -> "2b1a"  -> "2b"  + "2" + "1a" = "2b21a"  [E1]
    # "two words" -> "sdrow owt" -> "sdrow" + "2" + " owt" = "sdrow2 owt" [E1]
    # "a b c" -> "c b a" -> "c b" + "2" + " a" = "c b2 a" [E1]
    # "  spaced  " -> "  decaps  " -> "  dec" + "2" + "aps  " = "  dec2aps  " [E1]
    # split point = len//2 (floor): odd length puts extra char in left half [E1]
    out = []
    for s in probe.get("inputs", []):
        r = s[::-1]
        n = len(r)
        h = n // 2
        out.append(r[:h] + "2" + r[h:])
    return {"outputs": out}
