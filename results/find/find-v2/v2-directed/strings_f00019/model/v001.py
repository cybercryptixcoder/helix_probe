def predict(probe):
    # Last character of each word is shifted +1 in alphabet [E1]
    # "hello"->"hellp", "world"->"worle", "abc"->"abd", "Hello"->"Hellp",
    # "HELLO"->"HELLP", "hELLo"->"hELLp", "two words"->"two wordt",
    # "a b c"->"a b d", "abc123"->"abc123", "123"->"123"
    # Non-letter last chars unchanged (digits) [E1]
    # Only the last character of each whitespace-separated word is changed [E1]
    def shift_word(w):
        if not w:
            return w
        c = w[-1]
        if 'a' <= c <= 'y':
            return w[:-1] + chr(ord(c) + 1)
        if c == 'z':
            return w[:-1] + 'a'  # ? wrap
        if 'A' <= c <= 'Y':
            return w[:-1] + chr(ord(c) + 1)
        if c == 'Z':
            return w[:-1] + 'A'  # ? wrap
        return w
    out = []
    for s in probe.get("inputs", []):
        parts = s.split(' ')
        out.append(' '.join(shift_word(p) for p in parts))
    return {"outputs": out}
