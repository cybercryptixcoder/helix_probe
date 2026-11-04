def predict(probe):
    # The box reverses the input string and appends 'I' [E1]
    # Evidence: "hello"->"ollehI", "HELLO"->"OLLEHI", " "->"I"
    # Case is preserved, digits/symbols preserved, spaces preserved [E1]
    # "hello world"->"olleh dlrowI" (whole string reversed, not words) [E1]
    out = []
    for s in probe.get("inputs", []):
        try:
            out.append(s[::-1] + "I")
        except Exception:
            out.append("I")
    return {"outputs": out}
