import re

def predict(probe):
    # Identity for everything except: a run of uppercase letters immediately
    # followed by digits loses its second character? [E12: "ABC123" -> "AC123"]
    # All other tested inputs unchanged [E1-E11].
    # Hypothesis: when a string matches ^[A-Z]+[0-9]+$ (all-caps token + digits),
    # the second character is dropped. Only "ABC123" observed; "abc123" unchanged,
    # so the rule is case-sensitive (uppercase run only). "?" uncertain boundary.
    out = []
    for s in probe["inputs"]:
        if re.fullmatch(r"[A-Z]{2,}[0-9]+", s):
            s = s[0] + s[2:]
        out.append(s)
    return {"outputs": out}
