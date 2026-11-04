def predict(probe):
    # Split input on ANY whitespace run (tabs, newlines, multiple spaces) [E4, E6]
    # Drop empty tokens (leading/trailing whitespace, collapsed runs) [E4, E6]
    # Reverse each token's characters [E1, E2, E3, E5]
    # Join tokens with a single space [E4, E6]
    # "a\tb"->"a b", "a  b"->"a b", " lead"->"dael", "trail "->"liart" [E4, E6]
    # "one two three"->"eno rhwt" (word order NOT reversed) [E4]
    # "Hello World"->"oleH drW", "abc123"->"321cba" [E1, E2]
    import re
    out = []
    for s in probe["inputs"]:
        tokens = s.split()
        out.append(" ".join(t[::-1] for t in tokens))
    return {"outputs": out}
