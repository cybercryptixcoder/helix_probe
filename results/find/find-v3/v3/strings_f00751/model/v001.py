def predict(probe):
    # Insert 'i' after the first vowel in each word? Let's check evidence.
    # E1: "abc123" -> "abci123"  (insert 'i' after 'a'? after first vowel 'a')
    # "level" -> "leivel"  (insert 'i' after first 'e')
    # " Zebralower" -> "Zebrialower" (insert 'i' after 'e' in Zebra)
    # "Hello World function lazy" -> "Hello World ifunction lazy" (insert 'i' after 'f'? no... after first vowel of "function" = 'u'? but got "ifunction")
    # Hmm "function" -> "ifunction": insert 'i' BEFORE 'f'? 
    # "bananaUPPER" -> "bananiaUPPER" (insert 'i' after 'a' in banana)
    # "Zebra" -> "Zeibra" (insert 'i' after 'e')
    # Pattern: insert 'i' after the first vowel of the word? 
    # abc123: first vowel 'a' -> abci123 ✓
    # level: first vowel 'e' -> leivel ✓
    # Zebralower: first vowel 'e' -> Zeibralower ✓
    # function: first vowel 'u' -> functiion? but got "ifunction" ✗
    # Wait "Hello World function lazy": only "function" changed to "ifunction". 
    # Maybe insert 'i' before first consonant cluster? Or before 'f'?
    # bananaUPPER: first vowel 'a' -> bananiaUPPER ✓ (after first 'a')
    # Zebra: first vowel 'e' -> Zeibra ✓
    # So function is the odd one. "function" -> "ifunction": insert 'i' at start.
    # Maybe rule: insert 'i' after first vowel, but if word starts with consonant+vowel... 
    # Actually maybe: insert 'i' after first vowel, but 'u' is special? Or insert 'i' before first 'f'?
    # Let's think: maybe insert 'i' after first vowel, EXCEPT insert before first letter if... no.
    # Alternative: insert 'i' after the first vowel that is followed by a consonant? 
    # abc: a followed by b -> abci ✓
    # level: e followed by v -> leivel ✓
    # Zebra: e followed by b -> Zeibra ✓
    # banana: a followed by n -> banania ✓
    # function: u followed by n -> functiion, not ifunction ✗
    # Hmm. Maybe the rule is different: insert 'i' after first vowel, but "function" -> "ifunction" suggests insert before 'f'.
    # Wait maybe it's insert 'i' after the first vowel of the FIRST word? No, "Hello World function lazy" only function changed.
    # Maybe insert 'i' before first 'f'? abc123 no f. level no f. Zebra no f. banana no f. function has f -> ifunction ✓
    # But then why insert after vowel in others? Maybe two rules: insert 'i' after first vowel AND insert 'i' before 'f'? 
    # function: before f gives ifunction, but also after first vowel u would give functiion. Only one i appeared.
    # Maybe rule: insert 'i' before the first letter that is 'f'? and after first vowel otherwise?
    # Or: insert 'i' after first vowel, unless word contains 'f', then insert before 'f'?
    # Let's test: "function" contains f -> insert before f = ifunction ✓
    # Others no f -> insert after first vowel ✓
    # That's a guess. Could also be: insert 'i' after first vowel, but skip if... 
    # Actually maybe simpler: insert 'i' after first vowel, but 'u' doesn't count as vowel? Then function: first vowel 'o'? f-u-n-c-t-i-o-n, o followed by n -> functiion? no.
    # If 'u' not vowel: first vowel 'i'? function has i at position 5, followed by o -> functiion? no.
    # Hmm. Let's go with: insert 'i' after first vowel (a,e,i,o,u), but if word starts with 'f' insert 'i' before 'f'? 
    # "function" starts with f -> ifunction ✓
    # But what about words with f not at start? Unknown.
    # Let's just do: for each word, if it contains 'f', insert 'i' before first 'f'; else insert 'i' after first vowel.
    # Actually maybe the rule is: insert 'i' after first vowel, but for "function" specifically... no, must be general.
    # Let me reconsider: maybe insert 'i' after first vowel, but the vowel must be followed by a consonant that is not... 
    # abc: a-b -> abci ✓
    # level: e-v -> leivel ✓
    # Zebra: e-b -> Zeibra ✓
    # banana: a-n -> banania ✓
    # function: u-n -> should be functiion, but got ifunction.
    # Unless "function" is treated differently because... hmm.
    # Maybe the rule is: insert 'i' after first vowel, but if the word starts with a consonant cluster? "function" starts with 'f' then 'u'. 
    # Actually maybe insert 'i' before the first vowel if the word starts with a consonant? No, abc starts with vowel a.
    # level starts with consonant l, got leivel (after e). So no.
    # I'll go with: insert 'i' after first vowel, except insert 'i' before first 'f' if 'f' present.
    # This is a guess. Mark with ?.
    import re
    def transform(word):
        # ? guess: if contains 'f', insert 'i' before first 'f'
        if 'f' in word:
            idx = word.index('f')
            return word[:idx] + 'i' + word[idx:]
        # else insert 'i' after first vowel
        for i, c in enumerate(word):
            if c in 'aeiouAEIOU':
                return word[:i+1] + 'i' + word[i+1:]
        return word
    def process(s):
        # split into words preserving spaces? "Hello World function lazy" -> only function changed
        # So process each word separately, keep spaces.
        return re.sub(r'[A-Za-z0-9]+', lambda m: transform(m.group()), s)
    return {"outputs": [process(x) for x in probe["inputs"]]}
