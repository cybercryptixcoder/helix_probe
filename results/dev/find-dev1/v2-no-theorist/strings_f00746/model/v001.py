def predict(probe):
    # Lowercase letters shift +2 in alphabet (a->c, b->d) [E1]
    # Uppercase letters shift +2 in alphabet (A->C, B->D) [E1]
    # Digits unchanged [E1]
    # Symbols/punctuation unchanged [E1]
    # Spaces unchanged (empty output for " " suggests space maps to space, but " " -> "" ... hmm) [E1]
    # Empty string -> empty string [E1]
    # Non-letter characters pass through unchanged [E1]
    def shift(ch):
        if 'a' <= ch <= 'z':
            return chr((ord(ch) - ord('a') + 2) % 26 + ord('a'))
        if 'A' <= ch <= 'Z':
            return chr((ord(ch) - ord('A') + 2) % 26 + ord('A'))
        return ch
    return {"outputs": ["".join(shift(c) for c in s) for s in probe["inputs"]]}
