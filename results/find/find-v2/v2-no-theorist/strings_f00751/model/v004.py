def predict(probe):
    # Insert 'i' after each vowel (a,e,i,o,u) that is NOT the first letter of a word [E1-E10]
    # Word = maximal run of letters; word-initial = first letter of a letter-run [E1-E10]
    #   "cat"->"ciat", "banana"->"baniana", "dog"->"diog", "pig"->"piig", "sun"->"siun" [E8]
    #   "book"->"boiok", "zoo"->"zioo", "hi there"->"hi tihere" [E8,E10]
    #   "apple"->"apiple", "about"->"abiout", "table"->"taible", "map"->"miap" [E2]
    #   "level"->"leivel", "eve"->"eive", "be"->"bie", "example"->"exaimple" [E4]
    #   "function"->"functiion", "Hello"->"Hiello", "world42"->"worild42" [E1,E5]
    #   "data123"->"datia123", "aMiXeD"->"aMiiXeD" [E5,E7]
    #   "yellow"->"yelilow", "myth"->"myith" (y is NOT a vowel) [E10]
    #   "cry baby"->"cry ibaby" [E10]
    # Word-initial vowel is skipped [E1-E10]:
    #   "apple"->"apiple", "about"->"abiout", "Example"->"Exaimple", "eve"->"eive" [E2,E4]
    #   "end"->"end", "an"->"an", "Apple"->"Apiple", "Eagle"->"Eaigle" [E4,E8]
    #   "ate"->"ate" (a word-initial), "ok"->"ok" [E10]
    #   "1apple"->"1apiple": 'a' preceded by digit is word-initial, skipped [E10]
    #   "x apple"->"x aipple": 'a' after space is word-initial, skipped [E10]
    #   "ok apple"->"ok aipple" [E10]
    #   "banana Apple"->"bananai Apple" (A in Apple word-initial skipped) [E8]
    # Uppercase vowels augmented when not word-initial [E6,E8]:
    #   "Cat"->"Ciat", "CAT"->"CiAT", "cAt"->"ciAt", "xAy"->"xiAy", "xEy"->"xiEy" [E6]
    #   "aA"->"aiA" (first a word-initial len1 skipped; A not word-initial augmented) [E6]
    #   "eE"->"eiE", "1a2"->"1ia2", "a1"->"ai1" [E6]
    #   "a1e2i3"->"a1ei2i3" (a word-initial skipped; e,i not word-initial) [E10]
    # Single-char whole-string vowel IS augmented [E2,E4]:
    #   "a"->"ia", "e"->"ie"
    #   But "a cat"->"a icat": 'a' word-initial (len1 word) NOT augmented [E4]
    # Leading spaces stripped [E7,E9]:
    #   " Zebralower"->"Zebrialower", " Example"->"Exaimple" [E1,E7]
    #   "  apple banana function"->"apple baniana function" [E7]
    #   " hello"->"heillo" [E9]
    # Trailing spaces stripped [E3,E5,E7,E9]:
    #   "banana data banana "->"banana daita banana" [E3]
    #   "Example "->"Examiple", "abc "->"abic" [E5,E7]
    #   "world  "->"worild" [E9]
    #   "banana a data "->"banana ia data" [E5]
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
