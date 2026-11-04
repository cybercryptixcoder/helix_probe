def predict(probe):
    # Capitalize first letter of each whitespace-separated word, remove spaces [E1]
    # "hello"->"Hello", "two words"->"Twowords", "Hello, World!"->"Hello,world!" [E1]
    # "  spaced  "->"spaced" (strip + remove internal spaces), "the quick brown fox"->"Thequickbrownfox" [E1]
    # "12345"->"12345", "!@#$%"->"!@#$%" (no letters, unchanged) [E1]
    # "a1b2c3"->"A1b2c3" (capitalize first char of word) [E1]
    # "HELLO"->"Hello" (lowercase rest of word) [E1]
    # "Hello"->"Hello" [E1]
    def cap(w):
        return w[:1].upper() + w[1:].lower()
    words = probe.get("inputs", [])
    out = []
    for s in words:
        parts = s.split()
        out.append("".join(cap(p) for p in parts))
    return {"outputs": out}
