def predict(probe):
    # Every character shifts +1 in ASCII code, no wrap [E1, E2]
    #   z->{, Z->[, space->!, comma->-, !->", 9->: [E2]
    # Insert 'Y' at index floor(len/2) of the shifted string [E1, E2]
    results = []
    for s in probe.get("inputs", []):
        shifted = ''.join(chr(ord(c) + 1) for c in s)
        pos = len(s) // 2
        results.append(shifted[:pos] + 'Y' + shifted[pos:])
    return {"outputs": results}
