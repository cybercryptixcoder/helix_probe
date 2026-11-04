def predict(probe):
    # f reverses the input, but whitespace handling differs from plain reversal:
    # - "two words" -> "owt sdrowI": words reversed in place, word order kept [E2]
    # - "a b" -> "a bI": single chars unchanged, order kept [E2]
    # - "abc def ghi" -> "cba fed ihgI": each word reversed, order kept [E2]
    # - "  " -> "I", "\t" -> "I", "\n" -> "I": whitespace-only -> just "I" [E2]
    # - "Hello" -> "olleHI": single word reversed [E1]
    # - "ab" -> "baI", "AB" -> "BAI", "aB" -> "BaI": single word reversed [E1]
    # - "" -> "I", " " -> "I": empty/whitespace -> "I" [E1, E2]
    # - digits/punct single token reversed: "12345"->"54321I", "!@#$%"->"%$#@!I" [E2]
    # So: split on whitespace, reverse each token, rejoin with single spaces,
    # then append "I". Whitespace-only/empty collapses to "" then + "I".
    out = []
    for s in probe["inputs"]:
        words = s.split()
        out.append(" ".join(w[::-1] for w in words) + "I")
    return {"outputs": out}
