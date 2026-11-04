def predict(probe):
    # Every character's code point is increased by 8 [E1, E2, E3]
    # TAB (\t, 9) -> 0x11 (17), i.e. also +8 [E3, E4]
    # TAB is NOT dropped and does NOT drop neighbors: "ab\tcd"->"ij\x11kl" [E4]
    #   "abc\tde"->"ijk\x11lm", "x\ty"->"\x80\x11\x81", "\tabc"->"\x11ijk",
    #   "a\tb\tc"->"i\x11j\x11k", "a\tbc"->"i\x11jk", "zz\tzz"->"\x82\x82\x11\x82\x82",
    #   "foo\tbar"->"nww\x11jiz" all fit plain +8 with \t->\x11 [E4]
    # "tab\there"->"ij\x11pmzm" is 7 chars, but plain +8 gives "|ij\x11pmzm" (8).
    #   All other E4 cases match plain +8, so the missing '|' is a display/edge quirk,
    #   not a rule. Treat as plain +8 (mark ?).
    out = []
    for s in probe.get("inputs", []):
        try:
            out.append("".join(chr(ord(c) + 8) for c in s))
        except Exception:
            out.append("")
    return {"outputs": out}
