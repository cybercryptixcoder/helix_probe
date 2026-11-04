def predict(probe):
    # Reverse the string, then append "I" [E1: "ab"->"baI", ""->"I", "a"->"aI"]
    # Spaces are preserved in place (not stripped) [E2: "a b"->"a bI", "ab cd"->"ba dcI"]
    # Leading/trailing spaces are stripped from input first [E2: "  a  "->"aI", " a b "->"a bI"]
    # Tab is treated like space [E2: "a\tb"->"a bI"]
    out = []
    for s in probe.get("inputs", []):
        s = s.strip().replace("\t", " ")
        out.append(s[::-1] + "I")
    return {"outputs": out}
