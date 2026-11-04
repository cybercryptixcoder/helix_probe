def predict(probe):
    # Leading uppercase letter is removed when followed by a letter [E1, E2]
    #   "Hello"->"ello", "HELLO"->"ELLO", "Hello World"->"ello World",
    #   "Hello!"->"ello!", "H3llo"->"3llo"
    # Leading uppercase letter is KEPT when followed by a non-letter [E1, E2]
    #   "A1!"->"A1!", "X1"->"X1", "A b"->"A b"
    # Single uppercase letter: "A"->"A", "I"->"I" but "H"->"" [E2]
    #   Hmm, inconsistent. "A" and "I" are English words; "H" is not.
    #   (?) Hypothesis: single uppercase letter kept if it's a word ("A","I"),
    #       removed otherwise. Uncertain — only one data point ("H"->"").
    # Leading uppercase followed by space: "H ello"->" ello" [E2]
    #   So space counts as "letter-like" for removal? But "A b"->"A b" kept.
    #   Difference: "H ello" vs "A b" — both uppercase+space+lowercase.
    #   (?) Maybe "A" is special (word "A"). "H ello" removed, "A b" kept.
    #   Rule guess: remove leading uppercase if followed by space AND the
    #   uppercase is not "A"/"I"? Too speculative. Simpler: remove if
    #   followed by space, except when first char is "A" or "I".
    # Lowercase leading: unchanged, including "Zz"->"Zz", "Qq"->"Qq" [E2]
    #   Wait — "Zz" and "Qq" start uppercase and are UNCHANGED. Contradiction!
    #   "Zz"->"Zz", "Qq"->"Qq" but "Hello"->"ello". Both uppercase+lowercase.
    #   (?) Maybe only certain letters removed? H removed, Z/Q kept.
    #   Or maybe it's about the specific letter? H, and... "HELLO" H removed.
    #   "Hello" H removed. "Zz","Qq" kept. "A1!" kept, "A b" kept, "A" kept.
    #   "I" kept. "X1" kept. "H3llo"->"3llo" (H removed even before digit!).
    #   Wait "H3llo"->"3llo": H followed by '3' (non-letter) but removed.
    #   But "X1"->"X1" kept, "A1!"->"A1!" kept.
    #   So H is removed in more cases. Maybe rule is specific to letter "H"?
    #   Check: "hello"->"hello" (lowercase h kept). "Hello"->"ello" (H removed).
    #   "HELLO"->"ELLO". "Hello World"->"ello World". "Hello!"->"ello!".
    #   "H ello"->" ello". "H3llo"->"3llo". "H"->"".
    #   ALL H-leading strings have H removed! And no other letter removed.
    #   "Zz","Qq","A","I","X1","A1!","A b" all kept.
    #   (?) Strong hypothesis: the box removes a leading "H" (case-sensitive
    #       uppercase H) specifically. But that seems odd for a "function".
    #   Alternative: remove leading char if it's uppercase AND ... hmm.
    #   Let me reconsider: maybe it strips a leading "H" always.
    #   "hello" lowercase h kept — so only uppercase H.
    #   This fits ALL evidence. Mark as best guess.
    # Whitespace stripped [E1: "  spaced  "->"spaced"]
    #   But "H ello"->" ello" keeps the internal space (leading H removed,
    #   then space remains). So strip happens... before or after?
    #   "  spaced  "->"spaced" (stripped). "H ello"->" ello" (space kept).
    #   If strip first: "H ello" has no outer spaces, stays "H ello", remove H -> " ello". OK.
    #   So: strip outer whitespace, then remove leading uppercase H.
    out = []
    for s in probe.get("inputs", []):
        try:
            t = s.strip()
            if t.startswith("H"):
                t = t[1:]
            out.append(t)
        except Exception:
            out.append(s)
    return {"outputs": out}
