def predict(probe):
    # Reverse the string [E1-E20]
    # Insert 'I' at index len//2 of the reversed string [E1, E9, E11, E20]
    #   "abc123"->"321cba"->"321Icba"; "hello"->"olleh"->"ollIeh"; "a"->"a"->"Ia"
    out = []
    for s in probe.get("inputs", []):
        r = s[::-1]
        m = len(r) // 2
        out.append(r[:m] + "I" + r[m:])
    return {"outputs": out}
