def predict(probe):
    # Beliefs (revised on E3):
    # 1. Collapse runs of identical letters, but only within a word that is uniform case (all-lower or all-upper) [E1: hello->helo, HELLO->HELO; E2 all; Hello->Heloh keeps ll]
    # 2. Append 'h' to each word, unless that word is all-lowercase and ends in 'o' or 'y' [E1: hello->helo, happy->hapy; E2: see->seh, coffee->cofeh; E3: two->twoh, world->worldh]
    # 3. Multi-word: apply per word, join with single spaces [E3: big cat->big cath, cat dog->cat dogh, red blue->red bluh]
    # 4. BUT: interior words that are "long" get their vowels stripped? E3: "hello hello"->"helo " (second hello vanished!), "sun moon"->"sun moh" (moon->mo, not moonh).
    #    Hmm. Let's look again:
    #    "hello hello" -> "helo " : first hello->helo (no h, ends o), second hello->"" (empty)? That's odd.
    #    "sun moon" -> "sun moh": sun->sun (no h? but sun ends n consonant, should be sunh). Actually "sun moh" = "sun" + " " + "moh"? moon->mo+h? moon ends n, collapse oo->o gives "mon", ends n -> monh. But observed "moh".
    #    Wait "sun moh": maybe sun->sun (no h), moon->moh. moon: collapse oo->o -> "mon", then... drop n? -> "mo", then h -> "moh". So drop final consonant? 
    #    "hello hello"->"helo ": first hello->helo (no h), second hello->"" (dropped entirely?).
    #    "big cat"->"big cath": big->big (no h!), cat->cath. So first word "big" no h, second "cat" gets h.
    #    "cat dog"->"cat dogh": cat->cat (no h), dog->dogh.
    #    "red blue"->"red bluh": red->red (no h), blue->bluh (blue ends e, gets h; but blue has no doubles).
    #    "a b"->"a bh": a->a (no h), b->bh.
    #    So pattern: in multi-word, the FIRST word does NOT get h appended, but subsequent words do? 
    #    Check "big cat": big (first, no h), cat (second, h) -> "big cath" ✓
    #    "cat dog": cat (first, no h), dog (second, h) -> "cat dogh" ✓
    #    "red blue": red (first, no h), blue (second, h) -> "red bluh" ✓
    #    "a b": a (first, no h), b (second, h) -> "a bh" ✓
    #    "sun moon": sun (first, no h), moon (second, h) -> "sun monh"? But observed "sun moh". Hmm moon->moh not monh.
    #    "hello hello": hello (first, no h) -> helo, hello (second, h?) -> heloh? But observed "helo " (second empty).
    #    Hmm. Let me reconsider.
    #    Actually maybe the rule is: only the LAST word gets h, and earlier words get h stripped if they'd have it? 
    #    "big cat": big (no h), cat (h) -> big cath ✓
    #    "sun moon": sun (no h), moon (h) -> sun monh? observed sun moh. moon->moh: maybe collapse oo->o gives mon, then... hmm.
    #    Wait maybe "moon" -> "mo" + "h"? moon: m-o-o-n. Collapse oo->o: m-o-n = "mon". Then drop last consonant n? -> "mo", then h -> "moh". 
    #    But "cat"->"cath" doesn't drop t. 
    #    Difference: moon has a doubled letter that was collapsed. Maybe after collapsing, if the word had a double, drop the last letter? 
    #    Check E2: book->bokh: book collapse oo->o -> bok, ends k, h -> bokh. No drop. So no.
    #    Hmm "moon"->"moh". Maybe moon->mo (drop n) then h. Why drop n? 
    #    Let me look at "hello hello"->"helo ". First hello->helo (no h, ends o). Second hello->"" (empty). 
    #    Maybe the rule is: the box processes the string and the LAST word's h-rule applies, but interior words lose their last letter? 
    #    "hello hello": first hello->helo (ends o, no h) -> "helo", second hello->? -> "" 
    #    Actually "helo " has trailing space, so second word is empty string. 
    #    Maybe: repeated word gets removed? "hello hello" -> "helo " (second hello removed). 
    #    "sun moon" -> "sun moh": not repeated.
    #    This is getting complicated. Let me focus on what's clear:
    #    - Single word: collapse doubles (if uniform case), append h unless all-lower ends o/y.
    #    - Multi-word: first word no h, last word gets h (with same o/y exception?). 
    #    Check "hello world"->"helo wrd" from E1: hello (first, no h) -> helo, world (last, h?) -> wrd? world->wrd is weird (drop o,l). 
    #    Hmm "world"->"wrd" in E1 but "world"->"worldh" in E3 (single word). So context matters!
    #    In E1 "hello world" -> "helo wrd": world became wrd (dropped o and l). In E3 "world" alone -> "worldh".
    #    So multi-word second word gets vowels removed? "world"->"wrd" (remove o), and l? w-o-r-l-d -> w-r-d removes o and l. 
    #    "words"->"rds" in E1 "two words"->"two rds": words->rds removes w,o. 
    #    "moon"->"moh" in E3 "sun moon": moon->mo (remove n?) then h. Hmm not vowel removal.
    #    "hello"->"" in "hello hello": removes everything?
    #    I think there's a rule I'm missing. Let me hypothesize: in multi-word, the LAST word gets its vowels removed? 
    #    "hello world": last=world, remove vowels -> wrld, but observed wrd (also removed l). No.
    #    "two words": last=words, remove vowels -> wrds, observed rds (removed w too). No.
    #    "sun moon": last=moon, remove vowels -> mn, observed moh. No.
    #    Maybe remove first letter and vowels? world->orld->rld? no.
    #    Let me try: last word, remove letters that appear in first word? "hello world": hello has h,e,l,o. world remove those -> w,r,d = wrd ✓!
    #    "two words": two has t,w,o. words remove t,w,o -> r,d,s = rds ✓!
    #    "sun moon": sun has s,u,n. moon remove s,u,n -> m,o,o = moo? observed moh. Hmm close but moo vs mo.
    #    Wait moon: m,o,o,n. Remove s,u,n -> m,o,o = "moo". Then h -> "mooh"? observed "moh". 
    #    Maybe also collapse doubles: moo->mo, then h -> moh ✓!
    #    "hello hello": first hello has h,e,l,o. second hello remove those -> (empty) = "" ✓!
    #    "big cat": big has b,i,g. cat remove b,i,g -> c,a,t = cat, then h -> cath ✓!
    #    "cat dog": cat has c,a,t. dog remove c,a,t -> d,o,g = dog, then h -> dogh ✓!
    #    "red blue": red has r,e,d. blue remove r,e,d -> b,l,u = blu, then h -> bluh ✓!
    #    "a b": a has a. b remove a -> b, then h -> bh ✓!
    #    "hello world": hello has h,e,l,o. world remove h,e,l,o -> w,r,d = wrd ✓!
    #    "two words": two has t,w,o. words remove t,w,o -> r,d,s = rds ✓!
    #    "a b c": a has a. b remove a -> b. c remove a -> c. "a bc"? observed "a bch". Hmm "a b c" -> "a bch": a, space, b, space, c -> ? 
    #    Actually "a b c" has 3 words: a, b, c. First word a (no h). Then b remove letters of a -> b. Then c remove letters of a -> c. Result "a b c"? observed "a bch". 
    #    Maybe only first and last? "a b c": a (first, no h), b (middle), c (last, h). b remove a -> b. c remove a -> c, then h -> ch. "a b ch"? observed "a bch". Close: "a bch" vs "a b ch". Maybe spaces collapse? "a bch" = a, space, bch. So b and c merged? 
    #    Hmm maybe middle words also remove letters of first word, and spaces between non-first words removed? 
    #    Let me not overfit. The key insight: in multi-word, each word after the first has the letters of the FIRST word removed, then h appended to the last word (with o/y exception?).
    #    Check "hello world": world remove hello's letters -> wrd, append h? observed "helo wrd" no h! So last word doesn't get h here. 
    #    But "big cat"->"big cath" has h. Difference: cat after removal is "cat" (unchanged), world after removal is "wrd". 
    #    Maybe h appended only if the word was unchanged by removal? cat unchanged -> h. world changed -> no h. 
    #    "sun moon": moon remove sun's letters -> moo, collapse -> mo, changed -> no h? but observed moh has h. Contradiction.
    #    Hmm. "sun moon"->"sun moh": moon->moo->mo, then h. So changed but still h.
    #    "hello world"->"helo wrd": world->wrd, no h. 
    #    Difference: wrd ends in d (consonant), mo ends in o (vowel). Maybe h appended if ends in vowel? But single-word rule was opposite (no h for o/y).
    #    Ugh. Let me just go with: multi-word, first word transformed normally (collapse, no h), subsequent words: remove letters present in first word, collapse doubles, append h unless ends in o/y (same as single word rule).
    #    Check "hello world": world remove hello letters -> wrd, ends d -> h? observed no h. ✗
    #    Hmm. 
    #    Let me re-examine: maybe the h rule is: append h if the word (after all transforms) ends in a consonant OR ends in 'e'. No h if ends in o, y, or is empty.
    #    Single word: helo ends o -> no h ✓. hapy ends y -> no h ✓. bok ends k -> h ✓. se ends e -> h ✓. cofe ends e -> h ✓. 
    #    Multi: wrd ends d -> h? but observed no h. ✗
    #    I'm stuck on "hello world"->"helo wrd" (no h) vs "big cat"->"big cath" (h).
    #    Maybe the difference: "hello world" the first word hello ends in o (no h), and the whole thing... 
    #    Actually maybe the h is appended to the FIRST word if it qualifies, and the last word gets h only if first didn't? 
    #    "hello world": hello ends o -> no h. world -> wrd, no h? 
    #    "big cat": big ends g -> h? but observed "big cath" has h at end not after big. 
    #    Hmm "big cath": is it "big" + " " + "cath" or "bigh" + " " + "cat"? It's "big cath" = big, space, cath. So h on cat.
    #    OK let me just implement the removal rule and append h to last word unless it ends in o/y or is empty, and accept some error on "hello world".
    #    Actually wait: "hello world"->"helo wrd". If world->wrd and we append h we get "helo wrdh". Observed "helo wrd". So no h. 
    #    Maybe h is appended only if the last word after removal is non-empty AND ends in a letter that was NOT removed? cat: c,a,t none removed (big has b,i,g) -> h. wrd: w,r,d none removed (hello has h,e,l,o) -> should h. ✗
    #    I'll just go with: last word gets h unless ends in o/y/empty. Accept "hello world" error.
    #    Actually, let me reconsider "hello world"->"helo wrd" — maybe it's "helo" + " " + "wrd" where wrd is world with vowels removed? world vowels: o -> wrld, but observed wrd (also l removed). 
    #    Or world -> wrd by removing o and l (l is doubled? no). 
    #    I'll implement removal-of-first-word-letters and move on.
    import re
    def collapse(s):
        # collapse runs of identical letters if uniform case
        letters = [c for c in s if c.isalpha()]
        if letters and (all(c.islower() for c in letters) or all(c.isupper() for c in letters)):
            res = []
            prev = None
            for c in s:
                if c == prev:
                    continue
                res.append(c)
                prev = c
            return ''.join(res)
        return s
    def add_h(s):
        letters = [c for c in s if c.isalpha()]
        if letters and all(c.islower() for c in letters) and s and s[-1] in 'oy':
            return s
        return s + 'h'
    def transform_word(w):
        return collapse(w)
    inputs = probe.get("inputs", [])
    out = []
    for s in inputs:
        try:
            words = s.split(' ')
            if len(words) == 1:
                out.append(add_h(collapse(s)))
            else:
                first = collapse(words[0])
                first_letters = set(first.lower())
                parts = [first]
                for w in words[1:]:
                    # remove letters present in first word
                    filtered = ''.join(c for c in w if c.lower() not in first_letters)
                    filtered = collapse(filtered)
                    parts.append(filtered)
                # append h to last word unless ends o/y/empty
                last = parts[-1]
                if last:
                    letters = [c for c in last if c.isalpha()]
                    if not (letters and all(c.islower() for c in letters) and last[-1] in 'oy'):
                        parts[-1] = last + 'h'
                out.append(' '.join(parts))
        except Exception:
            out.append(s + 'h')
    return {"outputs": out}
