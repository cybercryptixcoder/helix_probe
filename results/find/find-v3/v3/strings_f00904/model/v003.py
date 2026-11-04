def predict(probe):
    # Mechanism: reverse the entire string, then map 'W' -> 'r'.
    # Evidence:
    # - Full reversal: "abc123"->"321cba" [E1], "Hello, World!"->"!dlror ,olleH" [E2/E4]
    # - 'W' -> 'r' after reversal: "World"->"dlror" [E4], "W"->"r", "WWW"->"rrr" [E4]
    # - lowercase 'w' unaffected: "Ww"->"wr", "wW"->"rw" [E6]
    # - spaces/digits/symbols preserved and reversed in place [E2, E4]
    # - "Hello World function lazy"->"yzal noitcnuf dlror olleH" confirms both rules [E1]
    outs = []
    for s in probe.get("inputs", []):
        outs.append(s[::-1].replace("W", "r"))
    return {"outputs": outs}
