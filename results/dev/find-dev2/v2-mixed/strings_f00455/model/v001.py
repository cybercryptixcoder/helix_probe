def predict(probe):
    # Each character's ASCII code is increased by 1 [E1: 'abc123'->'Bcd234', 'level'->'Mfwfm', 'Zebra'->'[fcsb']
    #   'Hello World function lazy'->'Ifmmp!xpsme!gvodujpo!mb{z', 'bananaUPPER'->'Cbobobvqqfs', ' Zebralower'->'!{fcsbmpxfs']
    # Non-alphanumeric characters also shift by 1 (' '->'!', 'z'->'{') [E1]
    # Digits shift too ('1'->'2', '2'->'3', '3'->'4') [E1]
    out = []
    for s in probe.get("inputs", []):
        out.append("".join(chr(ord(c) + 1) for c in s))
    return {"outputs": out}
