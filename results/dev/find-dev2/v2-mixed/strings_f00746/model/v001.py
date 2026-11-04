def predict(probe):
    # First character of each string is shifted up by 1 (a->b, b->c, ... z->a) [E1]
    # Rest of the string is unchanged [E1]
    # Non-letter first chars (space, digit, symbol) are unchanged [E1: " Zebralower"]
    # Case is preserved: uppercase first letter shifts within uppercase [E1: "Zebra"->"Bebra", "Hello"->"Jello"]
    # Lowercase first letter shifts within lowercase [E1: "abc123"->"cbc123", "level"->"nevel", "bananaUPPER"->"dananaUPPER"]
    def shift(s):
        if not s:
            return s
        c = s[0]
        if 'a' <= c <= 'z':
            c = chr((ord(c) - ord('a') + 1) % 26 + ord('a'))
        elif 'A' <= c <= 'Z':
            c = chr((ord(c) - ord('A') + 1) % 26 + ord('A'))
        return c + s[1:]
    return {"outputs": [shift(x) for x in probe["inputs"]]}
