def predict(probe):
    # Beliefs:
    # 1. Collapse runs of identical letters, but only if the word is uniform case (all-lower or all-upper) [E1, E2]
    # 2. Single word: append 'h' unless all-lowercase and ends in 'o' or 'y' [E1, E2]
    # 3. Multi-word: first word transformed normally (collapse), NO h appended [E1, E3, E4]
    # 4. Multi-word: each later word has letters of the FIRST word (case-insensitive) removed, then collapse [E3, E4]
    # 5. Multi-word: last word gets 'h' appended unless it ends in 'o'/'y' (lowercase) or is empty [E1, E3, E4]
    #    E4: "hello cat" -> "helo cat" (cat unchanged by removal, but NO h!) — so h-rule differs when first word ends in o?
    #    Actually "hello cat": first=helo (ends o, no h). cat remove h,e,l,o -> cat. observed "cat" no h.
    #    vs "big cat"->"big cath": big ends g. cat -> cath.
    #    Hypothesis: h appended to last word only if FIRST word got an h (i.e., first word doesn't end in o/y)?
    #    Check: "cat sun"->"cat sunh": cat ends t (would get h) -> sunh ✓
    #    "sun cat"->"sun cath": sun ends n (would get h) -> cath ✓
    #    "dog moon"->"dog mnh": dog ends g (would h) -> mnh ✓
    #    "moon dog"->"mon dgh": moon ends n (would h) -> dgh ✓
    #    "red cat"->"red cath": red ends d (would h) -> cath ✓
    #    "cat red"->"cat redh": cat ends t (would h) -> redh ✓
    #    "big world"->"big worldh": big ends g -> worldh ✓
    #    "world big"->"world bigh": world ends d -> bigh ✓
    #    "hello cat"->"helo cat": hello ends o (no h) -> cat no h ✓
    #    "cat hello"->"cat helo": cat ends t (would h) -> helo... but observed "helo" no h! 
    #    Hmm "cat hello": hello remove c,a,t -> helo, ends o -> no h anyway ✓ (o exception)
    #    "hello world"->"helo wrd": hello ends o -> no h on wrd ✓
    #    "two words"->"two rdsh": two ends o -> no h? but observed "rdsh" has h! ✗
    #    Hmm. "two words": two ends o, but rds gets h. So first-word-ends-o doesn't block h.
    #    Let me reconsider. "hello cat"->"helo cat": why no h on cat?
    #    Maybe: h appended to last word only if the last word (after removal) equals... no.
    #    Maybe: h appended only if last word after removal is non-empty AND first word's last letter is not in... 
    #    "hello cat": cat contains no letters of hello? c,a,t vs h,e,l,o - none shared. cat unchanged.
    #    "big cat": cat vs b,i,g - none shared. cat unchanged. But big cat -> cath (h), hello cat -> cat (no h).
    #    Difference: first word hello ends in o. big ends in g. two ends in o but words->rds gets h.
    #    Hmm "two words"->"two rdsh": words remove t,w,o -> rds, gets h. So first ends o but h added.
    #    Difference between "hello cat" and "two words": in "two words", the second word was CHANGED (words->rds). In "hello cat", cat unchanged.
    #    "big cat": cat unchanged, got h. Contradiction.
    #    Wait, maybe I should check: is it "helo cat" or could cat have gotten h and I misread? Observed "helo cat" - no h.
    #    Let me look at "hello world"->"helo wrd": world changed to wrd, no h. So changed -> no h here.
    #    "two words"->"two rdsh": words changed to rds, got h. Contradiction with "hello world".
    #    Difference: wrd ends in d (consonant), rds ends in s (consonant). Both consonants.
    #    Hmm. "sun moon"->"sun moh": moon->moo->mo (changed), got h. mo ends o.
    #    "hello world": wrd ends d, no h. "two words": rds ends s, h. "sun moon": mo ends o, h.
    #    Maybe h appended if last word (after removal+collapse) ends in vowel OR is a "complete" word? 
    #    wrd: no vowels left -> no h? rds: no vowels -> but got h. ✗
    #    I'm going in circles. Let me just use: append h to last word unless it ends in o/y (lowercase) or empty, EXCEPT when first word ends in o and last word unchanged? Too hacky.
    #    Let me try simplest consistent rule across E1,E3,E4:
    #    - "hello world"->"helo wrd" (no h): world->wrd
    #    - "two words"->"two rdsh" (h): words->rds
    #    - "hello cat"->"helo cat" (no h): cat unchanged
    #    - "big cat"->"big cath" (h): cat unchanged
    #    - "sun moon"->"sun moh" (h): moon->mo
    #    - "hello hello"->"helo " (empty): hello->""
    #    - "a b c"->"a bch": a, b, c -> a, b, ch
    #    Hmm "a b c": b remove a -> b, c remove a -> c, then h -> ch. Result "a b ch" but observed "a bch". Space between b and c removed?
    #    Maybe when a middle word becomes empty, spaces collapse? b is not empty. 
    #    "a bch" could be "a" + " " + "bch" where b and c merged? Or "a b" + "ch"? 
    #    Maybe only first and last words matter, middle words removed? "a b c": a (first), c (last) -> "a ch"? observed "a bch". No.
    #    Maybe middle words get letters of first removed AND joined without space to next? 
    #    Let me try: "a b c" -> a, then b (remove a -> b), then c (remove a -> c, +h -> ch). If b and c joined: "bch". Result "a bch" ✓!
    #    Check "hello hello": hello, then hello remove hello -> "" (empty). Result "helo " (trailing space). So empty second word keeps space.
    #    Hmm but "a b c" b is non-empty, c non-empty, joined. Why join b and c but not a and b?
    #    Maybe: the LAST word is appended to the previous word without space? "a b c": a, b, then c appended to b -> "a bc", +h -> "a bch" ✓
    #    "hello hello": hello, then hello->"" appended to first? "helo" + "" = "helo"? but observed "helo " with space.
    #    Hmm. Or maybe spaces are preserved but... 
    #    Let me check "a b"->"a bh": a, b remove a -> b, +h -> bh. "a bh" ✓ (space preserved).
    #    "a b c"->"a bch": if space preserved: "a b ch"? observed "a bch". So space between b and c removed.
    #    Maybe: only ONE space total? No, "a b" has one space.
    #    Maybe: the last word is joined to previous if previous is single char? b is single char. "a b" b is single char but space kept.
    #    Ugh. "a b c" is a weird edge case. Let me not worry too much.
    #    Let me focus: the main E4 surprise is "hello cat"->"helo cat" (no h) vs "big cat"->"big cath" (h).
    #    Both have cat unchanged. Difference: first word hello vs big.
    #    hello ends in o. big ends in g. 
    #    Maybe: h appended to last word only if first word would get h (first word doesn't end in o/y)?
    #    Check "two words": two ends o -> no h? but rds got h. ✗
    #    Unless "two" is special? two ends in 'o' but... hmm.
    #    Wait, maybe the rule is about the FIRST word's last letter being in the last word? 
    #    "hello cat": hello ends o, cat has no o. 
    #    "two words": two ends o, words has o (removed). 
    #    "big cat": big ends g, cat no g.
    #    Not obviously.
    #    Let me try yet another: h appended to last word if last word (after removal) is non-empty AND (first word doesn't end in o OR last word was changed by removal).
    #    "hello cat": hello ends o, cat unchanged -> no h ✓
    #    "two words": two ends o, words changed -> h ✓
    #    "hello world": hello ends o, world changed -> h? but observed no h ✗
    #    Argh.
    #    "hello world"->"helo wrd" no h, "two words"->"two rdsh" h. Both first ends o, both last changed.
    #    Difference: wrd vs rds. wrd ends d, rds ends s. 
    #    Maybe h appended if last word ends in s? No, "big cat"->cath ends t.
    #    Maybe h appended if last word (after removal) still contains a vowel? wrd no vowel -> no h. rds no vowel -> h. ✗
    #    I'll go with the "first word ends in o and last unchanged -> no h" rule plus default h, and accept errors.
    #    Actually, let me reconsider "hello world". Maybe world->wrd is not "remove hello letters". world remove h,e,l,o -> w,r,d = wrd ✓. 
    #    And h not appended. Maybe because wrd has no vowel? "two words": rds has no vowel but h appended. 
    #    OK I give up on perfect. Let me use: append h to last word unless (ends in o/y lowercase) or empty. This gets most cases. The "hello cat" and "hello world" will be wrong but that's 2/10 in E4.
    #    Actually wait — let me reconsider whether "hello cat"->"helo cat" might mean cat got h but then... no, output is "helo cat".
    #    Let me try: h appended to last word only if first word (after collapse) does NOT end in 'o'. 
    #    "hello cat": helo ends o -> no h ✓
    #    "hello world": helo ends o -> no h ✓
    #    "two words": two ends o -> no h? but observed h ✗
    #    Damn, "two" ends in o.
    #    Unless "two" collapse... two has no doubles. two ends o.
    #    Hmm, but "two" is 3 letters, "hello" is 5. Maybe length?
    #    "a b": a ends a, b->bh ✓ (a not o)
    #    "red blue": red ends d, blue->bluh ✓
    #    "cat dog": cat ends t, dog->dogh ✓
    #    "big cat": big ends g, cat->cath ✓
    #    "sun moon": sun ends n, moon->moh ✓
    #    "hello hello": helo ends o, second->"" (empty, no h anyway) ✓
    #    "hello cat": helo ends o, cat->cat (no h) ✓
    #    "hello world": helo ends o, world->wrd (no h) ✓
    #    "two words": two ends o, words->rds (h!) ✗
    #    Only "two words" contradicts. Maybe "two" is special because... t-w-o. Hmm.
    #    Or maybe the rule is: h appended if first word ends in consonant OR first word is "two"? No.
    #    Let me check: maybe "two words" the h comes from somewhere else. "two rdsh" - could be "two" + " " + "rds" + "h". 
    #    What if the rule is: append h to last word if last word (after removal) ends in a letter that is NOT in the first word? 
    #    "hello cat": cat ends t, t not in hello -> h? but no h observed ✗
    #    "two words": rds ends s, s not in two -> h ✓
    #    "hello world": wrd ends d, d not in hello -> h? but no h ✗
    #    Nope.
    #    I'll go with: append h to last word unless first word (collapsed) ends in 'o' or 'y', OR last word ends in o/y/empty.
    #    This gets "hello cat", "hello world" right, "two words" wrong. 
    #    Actually let me check E3 "hello hello"->"helo ": first ends o, second empty -> no h ✓ (empty anyway).
    #    Let me also handle "a b c" -> "a bch". With my rule: a (first), b remove a -> b, c remove a -> c. Last=c, first=a ends a (not o/y) -> c+h=ch. Join: "a b ch". Observed "a bch". Off by space.
    #    Maybe when there are 3+ words, the last two are joined? Or middle words joined to last?
    #    "a b c": a, b, c. If b and c joined: "a bch" ✓
    #    Let me hypothesize: for 3+ words, words after the first are all concatenated (no spaces between them), then h. 
    #    "a b c": a + " " + (b + c + h) = "a bch" ✓
    #    Check if any other 3-word case... none in data. Mark with ?.
    #    Actually simpler: maybe only the first space is kept, subsequent spaces removed? "a b c" -> "a b c" -> "a bc" -> +h -> "a bch" ✓
    #    "hello hello" (2 words): "helo " - space kept, second empty. ✓
    #    I'll go with: join first word, then space, then concatenation of remaining transformed words (no spaces between them), then h on the whole tail.
    #    Wait but "a b"->"a bh": a + " " + b + h = "a bh" ✓ (2 words, tail is just b)
    #    "big cat"->"big cath": big + " " + cat + h = "big cath" ✓
    #    "hello hello"->"helo ": helo + " " + "" = "helo " ✓ (tail empty, no h)
    #    "a b c"->"a bch": a + " " + (b + c) + h = "a bch" ✓
    #    This works! Let me use this.
    #    But wait, does the h-rule apply to the concatenated tail or per word? For "a b c", tail = "bc", ends c (consonant) -> +h = "bch" ✓.
    #    For "hello cat": tail = "cat", first=helo ends o -> no h? "helo cat" ✓
    #    For "two words": tail = "rds", first=two ends o -> no h? but observed h ✗. Still the two-words problem.
    #    Hmm. Let me just accept "two words" error, or... maybe the rule is: h appended unless first ends in o/y AND tail is unchanged from original last word? 
    #    "hello cat": cat unchanged -> no h ✓
    #    "hello world": world changed to wrd -> h? but no h ✗
    #    Nope.
    #    Let me just go with: h appended unless first (collapsed) ends in o/y, OR tail ends in o/y/empty.
    #    "two words" will be wrong (predicts "two rds", observed "two rdsh"). Accept.
    #    Actually, let me reconsider once more. What if the h-rule is: append h to the last word if the last word (after removal) is non-empty AND does not end in o/y, AND the first word (collapsed) is not "longer than" ... no.
    #    Let me just check: is there any way "two words" is special? two->two (no collapse). words remove t,w,o -> rds. rds+h.
    #    vs "hello world": hello->helo. world remove h,e,l,o -> wrd. wrd no h.
    #    Maybe: h appended if the removed letters include a letter that appears at the END of the first word? 
    #    "two words": two ends o, o is in words (removed) -> h ✓
    #    "hello world": hello ends o, o is in world (removed) -> h? but no h ✗
    #    Nope.
    #    OK final decision: use rule "h unless first ends o/y or tail ends o/y/empty". Accept "two words" error.
    #    Actually, you know what, let me just try: h appended unless tail ends in o/y/empty. Don't condition on first word.
    #    "hello cat": cat ends t -> cath? but observed cat ✗
    #    "hello world": wrd ends d -> wrdh? but observed wrd ✗
    #    So conditioning on first word IS needed for those two.
    #    Let me go with: h appended unless (first collapsed ends in o/y) OR (tail ends in o/y) OR tail empty.
    #    This gets hello cat, hello world, hello hello right. Gets two words wrong.
    #    Let me also verify E1 "two words"->"two rdsh" - I'll be wrong here but it's one case.
    #    Hmm, but E1 is in the notebook. Let me see if there's a better rule.
    #    What if: h appended if tail (after removal) is non-empty AND (first doesn't end o/y OR tail was changed by removal)?
    #    "hello cat": cat unchanged -> no h ✓
    #    "hello world": wrd changed -> h? but no h ✗
    #    Nope.
    #    What if: h appended if tail non-empty AND (first doesn't end o/y OR tail has no vowel)?
    #    "hello cat": cat has vowel a -> no h ✓
    #    "hello world": wrd no vowel -> h? but no h ✗
    #    Nope.
    #    What if: h appended if tail non-empty AND (first doesn't end o/y OR tail ends in s)?
    #    "hello cat": cat ends t -> no h ✓
    #    "hello world": wrd ends d -> no h ✓
    #    "two words": rds ends s -> h ✓
    #    "hello hello": tail empty -> no h ✓
    #    "sun moon": sun ends n (not o/y) -> h ✓
    #    This works for all! But "tail ends in s" is weird. Let me generalize: maybe tail ends in a "sibilant" or... 
    #    Actually maybe the rule is: h appended if first doesn't end o/y, OR tail ends in a letter that was NOT in the first word?
    #    "two words": rds, s not in two -> h ✓
    #    "hello cat": cat, t not in hello -> h? but no h ✗
    #    Nope.
    #    Let me just use: h appended if tail non-empty AND (first collapsed doesn't end in o/y OR tail ends in 's').
    #    This is hacky but fits all data. Mark with ?.
    #    Actually, let me reconsider "two words" once more. Maybe the output is "two rdsh" where "rds" is words with t,w,o removed, and h is appended because... 
    #    What if the rule is: h appended to last word if last word (after removal) is non-empty AND the first word (collapsed) does not end in 'o'... but "two" ends in o.
    #    Unless "two" is treated as ending in 'w'? No.
    #    I'll go with the hacky rule. Let me write it.
    import re
    def collapse(s):
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
    def ends_oy(s):
        letters = [c for c in s if c.isalpha()]
        return bool(letters) and all(c.islower() for c in letters) and s and s[-1] in 'oy'
    inputs = probe.get("inputs", [])
    out = []
    for s in inputs:
        try:
            words = s.split(' ')
            if len(words) == 1:
                w = collapse(s)
                if ends_oy(w):
                    out.append(w)
                else:
                    out.append(w + 'h')
            else:
                first = collapse(words[0])
                first_letters = set(first.lower())
                tail_parts = []
                for w in words[1:]:
                    filtered = ''.join(c for c in w if c.lower() not in first_letters)
                    filtered = collapse(filtered)
                    tail_parts.append(filtered)
                tail = ''.join(tail_parts)
                # h rule: append unless tail empty, or (first ends o/y and tail doesn't end in s)
                add = False
                if tail:
                    if not ends_oy(first):
                        add = True
                    elif tail.endswith('s'):
                        add = True
                if add and not ends_oy(tail):
                    tail = tail + 'h'
                out.append(first + ' ' + tail)
        except Exception:
            out.append(s + 'h')
    return {"outputs": out}
