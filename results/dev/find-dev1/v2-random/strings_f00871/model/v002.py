def predict(probe):
    # Reverses the string, then appends "I" [E1, E2]
    # BUT: words within the string are reversed in place, keeping word order [E2]
    #   "test case" -> "tset esac" (not "esac tset")
    #   "banana data banana " -> "ananab atad ananab" (trailing space dropped?)
    # Wait: E2 "banana data banana " -> "ananab atad ananab" - trailing space gone
    #   but "test case" has no trailing space. Check E1 "Hello World function lazy"
    #   -> "olleH dlroW noitcnuf yzal" - word order preserved, each word reversed.
    # So: split on spaces, reverse each word, rejoin with single spaces, append "I"
    # Trailing space in "banana data banana " was dropped -> split/join normalizes.
    out = []
    for s in probe.get("inputs", []):
        try:
            words = s.split(" ")
            rev = " ".join(w[::-1] for w in words)
            out.append(rev + "I")
        except Exception:
            out.append("")
    return {"outputs": out}
