def predict(probe):
    # Beliefs:
    # - Strip, split on whitespace [E4,E7,E9,E13,E15]
    # - Reverse each word, dedupe adjacent identical chars [E9 hello->oleh, E11 Hello->oleH]
    # - Single word that is a palindrome of odd length: output = middle char + right half [E9 racecar->ecar, E11 level->vel]
    # - Single word otherwise: output = dedupe(reverse(word)) [E9 world->dlrow, E15 xyz->zyx]
    # - Multi-word: first word processed as single-word rule, then " " + blob
    # - Blob = for remaining words in REVERSE order, take dedupe(reverse(word)), drop first char, take up to 2 chars, concat [E16 one two->wt, one two three->rhwt, one two three four->ufrhwt]
    # - ? blob rule is approximate; some cases like four->uf not fully explained
    def proc_word(w):
        r = w[::-1]
        d = []
        for c in r:
            if not d or d[-1] != c:
                d.append(c)
        d = "".join(d)
        if w == w[::-1] and len(w) % 2 == 1:
            m = len(w) // 2
            return w[m] + w[m+1:]
        return d
    def proc_blob(w):
        r = w[::-1]
        d = []
        for c in r:
            if not d or d[-1] != c:
                d.append(c)
        d = "".join(d)
        return d[1:3]
    def process(s):
        words = s.split()
        if not words:
            return ""
        first = proc_word(words[0])
        if len(words) == 1:
            return first
        blob = "".join(proc_blob(w) for w in reversed(words[1:]))
        return first + " " + blob
    return {"outputs": [process(s) for s in probe["inputs"]]}
