def predict(probe):
    # Insert 'i' after a vowel (a,e,i,o,u) that is NOT the first letter of a word [E1-E16]
    # Word = maximal run of letters; word-initial = first letter of a letter-run [E1-E16]
    # Vowel runs: insert 'i' only after the LAST vowel of a consecutive vowel run [E16]
    #   "quick"->"quiick" (u+i run, i after last), "brown"->"briown", "cooperate"->"coopierate" [E16]
    #   "out"->"oiut", "eat"->"eiat", "beautiful"->"beauitiful", "queue"->"quieue" [E16]
    #   "squeeze"->"squieeze", "flower"->"floiwer" [E16]
    # Word-initial vowel skipped [E1-E16]:
    #   "apple"->"apiple", "about"->"abiout", "end"->"end", "ate"->"ate" [E2,E4,E10]
    #   "1apple"->"1apiple", "x apple"->"x aipple", "ok apple"->"ok aipple" [E10]
    #   "a cat"->"a icat", "an apple"->"an aipple" [E4]
    # Uppercase vowels augmented when not word-initial [E6,E8,E12]:
    #   "Cat"->"Ciat", "CAT"->"CiAT", "cAt"->"ciAt", "BANANA"->"BANiANA" [E6,E12]
    #   "aA"->"aiA", "eE"->"eiE", "1a2"->"1ia2", "a1"->"ai1" [E6]
    # Single-char whole-string vowel IS augmented [E2,E4]: "a"->"ia", "e"->"ie"
    # Leading/trailing spaces stripped [E3,E5,E7,E9,E13,E15]:
    #   " Zebralower"->"Zebrialower", "world  "->"worild", "  xyz "->"xiyz" [E1,E9,E15]
    # Hyphen/apostrophe are word boundaries (non-letters) [E14]:
    #   "don't"->"doin't", "well-known"->"well-iknown", "re-enter"->"re-einter" [E14]
    #   "o'clock"->"o'cilock", "a-b"->"ai-b", "x-ray"->"x-iray", "ice-cream"->"ice-icream" [E14]
    #   "cooperate"->"coopierate" (oo run, i after last o) [E14,E16]
    #   "pre-existing"->"pre-exiisting", "self-aware"->"self-iaware" [E14]
    def aug(s):
        s = s.strip()
        if s in ('a', 'e', 'i', 'o', 'u'):
            return 'i' + s
        out = []
        n = len(s)
        for i, ch in enumerate(s):
            out.append(ch)
            if ch.lower() in 'aeiou':
                word_initial = (i == 0) or (not s[i-1].isalpha())
                if word_initial:
                    continue
                # only insert after the last vowel of a run
                if i + 1 < n and s[i+1].lower() in 'aeiou':
                    continue
                out.append('i')
        return ''.join(out)
    return {"outputs": [aug(x) for x in probe["inputs"]]}
