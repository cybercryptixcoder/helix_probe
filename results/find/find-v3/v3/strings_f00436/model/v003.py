def predict(probe):
    # Reverse the whole string [E1-E5]
    # Insert 'I' at position len//2 of the reversed string (before that index) [E1-E5]
    #   - "hello"->"olleh", len 5, mid 2 -> "ollIeh" [E4]
    #   - "abc"->"cba", len 3, mid 1 -> "cbIa" [E2]
    #   - "ab"->"ba", len 2, mid 1 -> "bIa" [E2]
    #   - "a"->"a", len 1, mid 0 -> "aI" [E2]
    #   - ""->"", len 0 -> "I" [E2]
    #   - "Zebra"->"arbeZ", len 5, mid 2 -> "arbIeZ" [E1,E2]
    #   - "level"->"level", len 5, mid 2 -> "levIel" [E1,E3]
    #   - "banana"->"ananab", len 6, mid 3 -> "anaInab" [E3,E4]
    #   - "testing"->"gnitset", len 7, mid 3 -> "gnitIset" [E4]
    #   - "function"->"noitcnuf", len 8, mid 4 -> "noitIcnuf" [E4]
    #   - "example"->"elpmaxe", len 7, mid 3 -> "elpmIaxe" [E4]
    #   - "world42"->"24dlrow", len 7, mid 3 -> "24dlIrow" [E5]
    #   - "aMiXeD"->"DeXiMa", len 6, mid 3 -> "DeXIiMa" [E5]
    #   - "function Hello World"->"dlroW olleH noitcnuf", len 20, mid 10 -> "noitcnuf olleIH dlroW" [E5]
    #   - "banana a data "->" atad a ananab", len 14, mid 7 -> "ananab aI atad" [E5]
    #   - "Example "->" elpmaxE", len 8, mid 4 -> "elpImaxE" [E5]
    #   - "racecar Example racecar"->"racecar elpmaxE racecar", len 25, mid 12 -> "racecar elpmIaxE racecar" [E5]
    out = []
    for s in probe.get("inputs", []):
        r = s[::-1]
        n = len(r)
        m = n // 2
        out.append(r[:m] + "I" + r[m:])
    return {"outputs": out}
