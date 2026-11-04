def predict(probe):
    # Insert 'i' after the first vowel (a,e,i,o,u) in each word [E1]
    # "abc123"->"abci123", "level"->"leivel", " Zebralower"->"Zebrialower",
    # "Hello World function lazy"->"Hello World ifunction lazy",
    # "bananaUPPER"->"bananiaUPPER", "Zebra"->"Zeibra" [E1]
    # Only the first vowel of each word gets an 'i' inserted after it.
    def transform(s):
        out = []
        i = 0
        n = len(s)
        while i < n:
            c = s[i]
            out.append(c)
            # if c is a vowel and we haven't yet inserted for this word
            # track per-word: reset at non-letter boundaries
            i += 1
        return ''.join(out)
    # Simpler: process word by word, splitting on non-letters.
    import re
    def fix_word(w):
        for idx, ch in enumerate(w):
            if ch in 'aeiouAEIOU':
                return w[:idx+1] + 'i' + w[idx+1:]
        return w
    def repl(m):
        return fix_word(m.group(0))
    return {"outputs": [re.sub(r'[A-Za-z]+', repl, s) for s in probe["inputs"]]}
