def predict(probe):
    # First char: title(s[0]) then +1 per codepoint [E1-E12]
    # Non-first chars: lower() then +1 per codepoint [E1-E5, E9-E12]
    # BUT: lower() is applied to the WHOLE remaining substring at once, not per-char,
    #   so context-sensitive lowercasing (final sigma) applies [E13]
    #   e.g. "ΣΣ": first Σ.title()=Σ+1=Τ; rest "Σ".lower()="σ"+1=τ -> "Ττ" [E13]
    #   "aΣΣ": a->B; "ΣΣ".lower()="σς"+1="τσ" [E13]
    #   "ΣaΣ": Σ->Τ; "aΣ".lower()="aς"+1="bσ" [E13]
    #   "ΣΣa": Σ->Τ; "Σa".lower()="σa"+1="τb" [E13]
    #   "ΣΣΣ": Σ->Τ; "ΣΣ".lower()="σς"+1="τσ" [E13]
    #   "ΟΣ": Ο->Π; "Σ".lower()="σ"+1=τ -> "Πτ" [E13]
    #   "ΣΟ": Σ->Τ; "Ο".lower()="ο"+1=π -> "Τπ" [E13]
    #   "ΟΣΟ": Ο->Π; "ΣΟ".lower()="σο"+1="τπ" -> "Πτπ" [E13]
    out = []
    for s in probe.get("inputs", []):
        try:
            if not s:
                out.append("")
                continue
            res = []
            for c in s[0].title():
                res.append(chr(ord(c) + 1))
            for d in s[1:].lower():
                res.append(chr(ord(d) + 1))
            out.append("".join(res))
        except Exception:
            out.append("")
    return {"outputs": out}
