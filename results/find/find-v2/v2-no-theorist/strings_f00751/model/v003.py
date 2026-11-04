def predict(probe):
    # Insert 'i' after every vowel (a,e,i,o,u) that is NOT the first character of a word [E1-E8]
    #   "cat"->"ciat", "banana"->"baniana", "dog"->"diog", "pig"->"piig", "sun"->"siun",
    #   "book"->"boiok" [E8]
    #   "apple"->"apiple", "about"->"abiout", "table"->"taible", "map"->"miap"
    #   "level"->"leivel", "test case"->"testi case", "the end"->"thei end"
    #   "eve"->"eive", "be"->"bie", "example"->"exaimple"
    #   "function"->"functiion" (u not word-initial), "Hello"->"Hiello" (e not word-initial)
    #   "world42"->"worild42" (o not word-initial), "data123"->"datia123"
    #   "aMiXeD"->"aMiiXeD" (i not word-initial, e not word-initial)
    # Word-initial vowel is skipped [E1,E2,E3,E4,E5,E6,E7,E8]:
    #   "apple"->"apiple", "about"->"abiout", "Example"->"Exaimple", "eve"->"eive",
    #   "end"->"end", "an"->"an", "Apple"->"Apiple", "Eagle"->"Eaigle"
    #   "abc123"->"abci123", "abc "->"abic", "Example "->"Exaimple"
    #   "  apple..."->"apple..." (leading spaces stripped? see below)
    # Uppercase vowels also augmented when not word-initial [E6,E8]:
    #   "Cat"->"Ciat", "CAT"->"CiAT", "cAt"->"ciAt", "xAy"->"xiAy", "xEy"->"xiEy"
    #   "banana Apple"->"bananai Apple" (a in banana augmented; A in Apple word-initial skipped)
    #   "aA"->"aiA" (first a word-initial len2 skipped; A not word-initial augmented)
    #   "eE"->"eiE", "1a2"->"1ia2", "a1"->"ai1"
    # Single-char whole-string vowel IS augmented [E2,E4]:
    #   "a"->"ia", "e"->"ie"
    #   But "a cat"->"a icat": 'a' word-initial (len1 word) NOT augmented. So the
    #   whole-string exception only applies when the string is exactly that vowel.
    # Leading spaces are stripped [E5,E7]:
    #   " Zebralower"->"Zebrialower", " Example"->"Exaimple",
    #   "  apple banana function"->"apple baniana function"
    # Trailing spaces stripped [E3,E5,E7]:
    #   "banana data banana "->"banana daita banana", "Example "->"Examiple",
    #   "abc "->"abic", "banana a data "->"banana ia data"
    # Word = maximal run of letters. Word-initial = first char of a letter-run.
    import re
    def aug(s):
        s = s.strip()
        if s in ('a', 'e', 'i', 'o', 'u'):
            return 'i' + s
        out = []
        for i, ch in enumerate(s):
            out.append(ch)
            if ch.lower() in 'aeiou':
                word_initial = (i == 0) or (not s[i-1].isalpha())
                if word_initial:
                    continue
                out.append('i')
        return ''.join(out)
    return {"outputs": [aug(x) for x in probe["inputs"]]}
