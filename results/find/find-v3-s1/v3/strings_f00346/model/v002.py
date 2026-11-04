def predict(probe):
    # First non-space char shifted +2 in alphabet (wrap), case preserved [E1,E2,E3,E4,E5,E6]
    # All whitespace removed (spaces AND tabs) [E1,E6: "hello\tworld"->"jelloworld"]
    # Non-letter first char: unchanged (digits, punctuation) [E2,E4,E6]
    # Leading/trailing/multiple spaces collapse away; all-space -> "" [E4]
    def shift(c):
        if 'a' <= c <= 'z':
            return chr((ord(c) - ord('a') + 2) % 26 + ord('a'))
        if 'A' <= c <= 'Z':
            return chr((ord(c) - ord('A') + 2) % 26 + ord('A'))
        return c
    outs = []
    for s in probe["inputs"]:
        s2 = "".join(ch for ch in s if not ch.isspace())
        if s2:
            s2 = shift(s2[0]) + s2[1:]
        outs.append(s2)
    return {"outputs": outs}
