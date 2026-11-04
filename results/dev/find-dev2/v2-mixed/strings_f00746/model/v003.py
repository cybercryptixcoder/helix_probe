def predict(probe):
    # First character of each string is shifted up by 2 (a->c, b->d, ... y->a, z->b) [E1, E2]
    # Rest of the string is unchanged [E1, E2]
    # Non-letter first chars (space, digit, symbol) are unchanged [E1: " Zebralower", E2: "123abc"]
    # Case is preserved: uppercase first letter shifts within uppercase [E2: "ABC"->"CBC", "Hello"->"Jello", "Zebra"->"Bebra"]
    # Lowercase first letter shifts within lowercase [E1: "abc123"->"cbc123", "level"->"nevel", "bananaUPPER"->"dananaUPPER"]
    # Trailing whitespace is stripped from the output [E3: "banana data banana "->"danana data banana"]
    def shift(s):
        if not s:
            return s
        c = s[0]
        if 'a' <= c <= 'z':
            c = chr((ord(c) - ord('a') + 2) % 26 + ord('a'))
        elif 'A' <= c <= 'Z':
            c = chr((ord(c) - ord('A') + 2) % 26 + ord('A'))
        return (c + s[1:]).rstrip()
    return {"outputs": [shift(x) for x in probe["inputs"]]}
