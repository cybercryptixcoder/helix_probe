def predict(probe):
    # Reverse whole string, append "I" [E1, E2]
    # BUT: if string is a palindrome (reversal == itself), append "I" without reversing? 
    # E1 "level" -> "levelI" (palindrome, reversal same, so consistent either way)
    # E2 "a b c" -> "a b cI" (NOT reversed! "a b c" reversed is "c b a")
    # So: palindrome-like? "a b c" is not a palindrome. Hmm.
    # "a b c" -> "a b cI": no reversal. Why?
    # Maybe: reverse only if it contains no spaces? No—"dog house"->"god esuohI" reversed.
    # Maybe: reverse words? No, "dog house"->"god esuoh" is full reversal.
    # "a b c" has single-char words. Maybe reverse only if... ?
    # Guess: if all words are single characters, don't reverse? "?"
    out = []
    for s in probe.get("inputs", []):
        words = s.split(" ")
        if len(words) > 1 and all(len(w) <= 1 for w in words):
            out.append(s + "I")
        else:
            out.append(s[::-1] + "I")
    return {"outputs": out}
