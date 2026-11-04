def predict(probe):
    # Insert a 2-char marker at index len//2 of each input string [E1]
    #   odd length  -> insert "I8"  (e.g. "hello"->"heI8llo", "a b"->"aI8 b") [E1]
    #   even length -> insert "8I"  (e.g. "aBc123 xyz"->"aBc128I3 xyz") [E1]
    # Position is exactly len//2 in every case; only the marker order flips with parity [E1]
    outs = []
    for s in probe.get("inputs", []):
        n = len(s)
        mid = n // 2
        ins = "I8" if n % 2 == 1 else "8I"
        outs.append(s[:mid] + ins + s[mid:])
    return {"outputs": outs}
