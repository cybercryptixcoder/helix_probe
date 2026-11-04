def predict(probe):
    # Capitalize first letter, lowercase the rest [E1, E2]
    # Exception: "Example123" -> "Exaple123" — the 'm' is dropped [E3]
    #   Hypothesis: when the string starts with "Exam", the 'm' is removed? 
    #   Only one data point; mark uncertain.
    def f(s):
        r = s[:1].upper() + s[1:].lower()
        if r.startswith("Exam"):
            r = r[:3] + r[4:]
        return r
    return {"outputs": [f(s) for s in probe["inputs"]]}
