def predict(probe):
    # Insert 'i' after every 'a' [E1, E2]
    #   "cat"->"ciat", "banana"->"baniana", "aaa"->"aiaa", "a"->"ia", "ba"->"bia"
    #   "apple"->"apiple": first 'a' NOT followed by i (word-initial 'a' skipped?),
    #     but second 'a' in "apple" -> "apiple" yes. Check: "about"->"abiout" (a skipped),
    #     "zebra"->"zeibra" (a followed by i). So word-initial 'a' is NOT augmented.
    #   "table"->"taible": 'a' not word-initial -> augmented. Consistent.
    #   "map"->"miap": 'a' not word-initial -> augmented. Consistent.
    #   "Zebralower"->"Zebrialower": 'a' not word-initial -> augmented.
    #   "bananaUPPER"->"bananiaUPPER": both 'a's not word-initial -> both augmented.
    #   "abc123"->"abci123": 'a' word-initial -> skipped. Consistent.
    #   "Hello World function lazy"->"Hello World ifunction lazy": 'a' in "lazy"
    #     not word-initial -> augmented. Consistent.
    # Rule: insert 'i' after each 'a' that is NOT the first character of a word.
    #   Word boundary = start of string or after a non-letter? "abc123" a at pos0 skipped.
    #   "bananaUPPER": 'a' at end of "banana" before 'U' still augmented (not word-initial).
    #   So only skip 'a' at position 0 of the whole string OR right after a non-letter?
    #   No multi-word evidence with word-initial 'a' after space. Use: skip 'a' if it is
    #   at index 0 or preceded by a non-alphanumeric character (word start). [E1,E2]
    import re
    def aug(s):
        out = []
        for i, ch in enumerate(s):
            out.append(ch)
            if ch == 'a':
                word_initial = (i == 0) or (not s[i-1].isalnum())
                if not word_initial:
                    out.append('i')
        return ''.join(out)
    return {"outputs": [aug(x) for x in probe["inputs"]]}
