def predict(probe):
    # Beliefs:
    # 1. Collapse runs of identical letters, but only if the word is uniform case (all-lower or all-upper) [E1, E2]
    # 2. Single word: append 'h' unless all-lowercase and ends in 'o' or 'y' [E1, E2]
    # 3. Multi-word: first word transformed normally (collapse), NO h appended [E1, E3, E4]
    # 4. Multi-word: each later word has letters of the FIRST word (case-insensitive) removed, then collapse [E3, E4]
    # 5. Multi-word: all later words are concatenated (no spaces between them) after the first word + one space [E5]
    # 6. Multi-word: append 'h' to the concatenated tail unless tail is empty, or tail ends in o/y (lowercase),
    #    or (first word ends in o/y AND tail ends in a consonant other than 's') [E4, E5]
    #    E5: "hello dogs"->"helo dgs" (no h): first=helo ends o, tail=dgs ends s? no, ends s -> wait dgs ends s.
    #    Hmm "helo dgs": dgs ends s, but no h. So the 's' exception is wrong.
    #    Let me recheck E5: "hello dogs"->"helo dgs" (no h). dogs remove h,e,l,o -> dgs. dgs ends s. No h.
    #    "hello cats"->"helo cats" (no h). cats remove h,e,l,o -> cats. ends s. No h.
    #    "two cats"->"two cash" (h). cats remove t,w,o -> cas. ends s. h.
    #    "two dogs"->"two dgsh" (h). dogs remove t,w,o -> dgs. ends s. h.
    #    So first=two (ends o) -> h, first=helo (ends o) -> no h. Both end o!
    #    Difference: two vs helo. Hmm.
    #    "moon words"->"mon wrdsh": moon->mon ends n (not o/y) -> h ✓
    #    "sun words"->"sun wordh": sun ends n -> h ✓
    #    "cat words"->"cat wordsh": cat ends t -> h ✓
    #    "big words"->"big wordsh": big ends g -> h ✓
    #    So only first-word-ends-o/y cases: hello (no h), two (h).
    #    What distinguishes "two" from "hello"? 
    #    "two" is 3 letters, "hello" is 5. Maybe length? Or maybe "two" collapse... two has no doubles.
    #    Wait — maybe the rule is about whether the first word was CHANGED by collapse?
    #    "hello"->"helo" (changed). "two"->"two" (unchanged).
    #    "hello cat"->"helo cat" (no h): hello changed, no h ✓
    #    "hello world"->"helo wrd" (no h): hello changed, no h ✓
    #    "hello dogs"->"helo dgs" (no h): hello changed, no h ✓
    #    "hello cats"->"helo cats" (no h): hello changed, no h ✓
    #    "two words"->"two rdsh" (h): two unchanged, h ✓
    #    "two cats"->"two cash" (h): two unchanged, h ✓
    #    "two dogs"->"two dgsh" (h): two unchanged, h ✓
    #    "hello hello"->"helo " (empty tail, no h anyway) ✓
    #    So: h appended unless (first word was collapsed/changed AND ends in o/y)? 
    #    But what about first word ends in o/y and NOT changed? e.g. "two" -> h. 
    #    And first word not ending o/y -> always h (regardless of change).
    #    So rule: append h unless (first ends in o/y AND first was changed by collapse) OR tail empty OR tail ends o/y.
    #    Check "hello cat": helo ends o, changed -> no h ✓
    #    Check "two words": two ends o, unchanged -> h ✓
    #    Check "hello world": helo ends o, changed -> no h ✓
    #    Check "two cats": two ends o, unchanged -> h ✓
    #    Check "hello dogs": helo ends o, changed -> no h ✓
    #    Check "hello cats": helo ends o, changed -> no h ✓
    #    Check "sun moon": sun ends n -> h ✓
    #    Check "big cat": big ends g -> h ✓
    #    This fits all! Let me use this.
    #    Also need: tail ends o/y -> no h. "sun moon"->"sun moh": moon->mo ends o, but h appended! 
    #    Wait "sun moh": mo + h. So tail ends o but h appended. So tail-ends-o/y does NOT block h.
    #    Hmm. "cat hello"->"cat helo": helo ends o, no h. But first=cat ends t (not o/y) -> would append h. 
    #    So tail ends o/y DOES block h in "cat hello".
    #    But "sun moon"->"sun moh": mo ends o, h appended. Contradiction?
    #    Difference: "cat hello": hello->helo (changed). "sun moon": moon->mo (changed). Both changed.
    #    Hmm. "cat hello": helo ends o. "sun moon": mo ends o. Both end o.
    #    Wait, maybe "sun moon"->"sun moh" the h is because... let me recheck. moon remove s,u,n -> moo -> collapse -> mo. Then h -> moh. 
    #    And "cat hello": hello remove c,a,t -> helo. Then no h.
    #    Both tails end in o. One gets h, one doesn't.
    #    Difference: first word sun vs cat. sun ends n, cat ends t. Both consonants.
    #    Hmm. Maybe the rule is: h appended unless tail ends in o/y AND first word ends in o/y? No, sun doesn't end o/y.
    #    Let me reconsider. Maybe "sun moh" - is it possible the h is not appended but part of something else? "sun moh" = sun + " " + moh. moon->mo, +h.
    #    And "cat helo" = cat + " " + helo. hello->helo, no h.
    #    Maybe: h appended if tail (after removal) is SHORTER than original last word? 
    #    "sun moon": moon(4)->mo(2), shorter -> h ✓
    #    "cat hello": hello(5)->helo(4), shorter -> h? but no h ✗
    #    Nope.
    #    Maybe: h appended if tail ends in o/y AND tail has no other vowel? mo has o only. helo has e,o. 
    #    "sun moh": mo, only vowel o -> h ✓
    #    "cat helo": helo, vowels e,o -> no h ✓
    #    "hello cat": cat, vowel a, ends t (not o/y) -> h? but no h ✗. Hmm cat doesn't end o/y so this rule doesn't apply.
    #    Wait "hello cat"->"helo cat" no h. cat ends t. So h blocked by first-word rule (helo ends o, changed).
    #    OK so two separate blocking conditions:
    #    (a) first word ends o/y AND was changed by collapse -> no h
    #    (b) tail ends o/y AND tail has only that one vowel (no other vowels)? 
    #    Check "cat hello": helo ends o, has e too -> no h ✓ (condition b)
    #    Check "sun moon": mo ends o, only o -> h ✓ (condition b doesn't block)
    #    Check "hello hello": tail empty -> no h ✓
    #    Check "two words": two ends o, unchanged -> condition a doesn't block. rds ends s -> h ✓
    #    Check "hello dogs": helo ends o changed -> condition a blocks -> no h ✓
    #    Check "hello cats": helo ends o changed -> no h ✓
    #    Check "two cats": two ends o unchanged -> a doesn't block. cas ends s -> h ✓
    #    Check "big cat": big ends g -> a doesn't block. cat ends t -> h ✓
    #    Check "sun moon": sun ends n -> a doesn't block. mo ends o, only vowel -> b doesn't block -> h ✓
    #    Check "cat hello": cat ends t -> a doesn't block. helo ends o, has e -> b blocks -> no h ✓
    #    Check "red blue": red ends d -> a doesn't block. blue->blu ends u (not o/y) -> h ✓
    #    Check "cat dog": cat ends t. dog->dog ends g -> h ✓
    #    Check "a b": a ends a. b->b ends b -> h ✓
    #    Check "a b c": a, tail=bc ends c -> h ✓
    #    Check "a b d": a, tail=bd ends d -> h ✓
    #    Check "a b cd": a, tail=bcd ends d -> h ✓
    #    Check "hello world": helo ends o changed -> a blocks -> no h ✓
    #    Check "two words": two ends o unchanged -> a doesn't block. rds ends s -> h ✓
    #    Check "moon words": mon ends n -> a doesn't block. wrd ends d -> h ✓
    #    Check "sun words": sun ends n -> h ✓
    #    Check "cat words": cat ends t -> h ✓
    #    Check "big words": big ends g -> h ✓
    #    Check "hello hello": tail empty -> no h ✓
    #    Check "hello cat": helo ends o changed -> a blocks -> no h ✓
    #    Check "cat hello": cat ends t -> a doesn't block. helo ends o, has e -> b blocks -> no h ✓
    #    Check "world big": world ends d -> a doesn't block. big->big ends g -> h ✓
    #    Check "big world": big ends g -> a doesn't block. world->wrd ends d -> h ✓
    #    Check "moon dog": mon ends n -> a doesn't block. dog->dgh ends h? wait dog remove m,o,n -> dg -> dgh. dg ends g -> h ✓
    #    Check "dog moon": dog ends g -> a doesn't block. moon->mn ends n -> h ✓
    #    Check "sun cat": sun ends n -> a doesn't block. cat->cat ends t -> h ✓
    #    Check "cat sun": cat ends t -> a doesn't block. sun->sun ends n -> h ✓
    #    Check "red cat": red ends d -> a doesn't block. cat->cat ends t -> h ✓
    #    Check "cat red": cat ends t -> a doesn't block. red->red ends d -> h ✓
    #    Check "world big": world ends d -> a doesn't block. big->big ends g -> h ✓
    #    Check "big world": big ends g -> a doesn't block. world->wrd ends d -> h ✓
    #    Check "two dogs": two ends o unchanged -> a doesn't block. dgs ends s -> h ✓
    #    Check "two cats": two ends o unchanged -> a doesn't block. cas ends s -> h ✓
    #    Check "hello dogs": helo ends o changed -> a blocks -> no h ✓
    #    Check "hello cats": helo ends o changed -> a blocks -> no h ✓
    #    Check "moon words": mon ends n -> a doesn't block. wrd ends d -> h ✓
    #    Check "sun words": sun ends n -> h ✓
    #    Check "cat words": cat ends t -> h ✓
    #    Check "big words": big ends g -> h ✓
    #    Check "a b d": a, tail=bd ends d -> h ✓
    #    Check "a b cd": a, tail=bcd ends d -> h ✓
    #    All fit! Great.
    #    Condition b: tail ends o/y AND tail has only one distinct vowel (the ending one)? 
    #    "mo": vowels {o}, ends o -> b blocks? but h appended. So b should NOT block when only one vowel.
    #    Wait I said "b blocks when tail ends o/y AND has other vowels". Let me restate:
    #    b blocks h if tail ends in o/y AND tail contains a vowel other than the ending o/y.
    #    "helo": ends o, has e -> b blocks ✓
    #    "mo": ends o, no other vowel -> b doesn't block ✓
    #    "blu": ends u (not o/y) -> b doesn't apply ✓
    #    OK. Let me also double check "hello hello": tail empty -> no h (empty check).
    #    Also "hello hello" tail is "" -> no h ✓.
    #    Let me also handle single-word case separately (rule 2).
    #    Single word: append h unless all-lowercase and ends in o/y [E1, E2].
    #    "hello"->"helo" (ends o) no h ✓
    #    "book"->"bokh" (ends k) h ✓
    #    "see"->"seh" (ends e) h ✓
    #    "two"->"twoh" (ends o) -> no h? but observed "twoh"! 
    #    Wait E3: "two"->"twoh". two ends o, all lowercase -> should be no h by rule 2, but observed h!
    #    Hmm. "hello"->"helo" no h. "two"->"twoh" h. Both end o, lowercase.
    #    Difference: hello collapsed to helo (changed). two unchanged.
    #    So single word: append h unless (all-lowercase AND ends o/y AND was changed by collapse)?
    #    "hello"->"helo" changed, ends o -> no h ✓
    #    "two"->"two" unchanged, ends o -> h ✓
    #    "happy"->"hapy" changed, ends y -> no h? but observed "hapy"! no h. ✓
    #    "coffee"->"cofeh" changed, ends e -> h ✓
    #    "butter"->"buterh" changed, ends r -> h ✓
    #    "summer"->"sumerh" changed, ends r -> h ✓
    #    "miss"->"mish" changed, ends s -> h ✓
    #    "off"->"ofh" changed, ends f -> h ✓
    #    "egg"->"egh" changed, ends g -> h ✓
    #    "add"->"adh" changed, ends d -> h ✓
    #    "see"->"seh" changed, ends e -> h ✓
    #    "book"->"bokh" changed, ends k -> h ✓
    #    "world"->"worldh" unchanged, ends d -> h ✓
    #    "words"->"wordsh" unchanged, ends s -> h ✓
    #    "word"->"wordh" unchanged, ends d -> h ✓
    #    "test"->"tesh" changed, ends t -> h ✓
    #    "Test"->"Testh" mixed case, no collapse, ends t -> h ✓
    #    "Hello"->"Heloh" mixed case, no collapse, ends o -> h ✓ (not all-lowercase)
    #    "HELLO"->"HELOh" all-upper, collapse, ends O -> h ✓ (not all-lowercase)
    #    "123"->"123h" no letters, ends 3 -> h ✓
    #    "A1!"->"A1!h" ends ! -> h ✓
    #    So single word rule: append h unless (all-lowercase AND ends in o/y AND was changed by collapse).
    #    Wait "happy"->"hapy": changed, ends y, all-lowercase -> no h ✓
    #    What about a word that's all-lowercase, ends o/y, unchanged? "two"->"twoh" h ✓.
    #    What about "go"->? unchanged, ends o -> h (predict "goh"). Unknown but consistent.
    #    Hmm, but is it really "changed by collapse"? Or maybe the rule is about length or something?
    #    Let me reconsider. Maybe the rule is: append h unless all-lowercase AND ends o/y AND has a doubled letter somewhere?
    #    "hello" has ll -> no h ✓
    #    "happy" has pp -> no h ✓
    #    "two" no double -> h ✓
    #    "go" no double -> h (predict goh)
    #    "coffee" has ff,ee -> changed, ends e (not o/y) -> h ✓
    #    Both "changed" and "has double" give same results on data. 
    #    Actually "changed by collapse" = "has a doubled letter" (for uniform case). So equivalent.
    #    Let me use "has a doubled letter" as the condition — cleaner.
    #    Actually for multi-word first word: "hello" has ll -> changed. "two" no double -> unchanged. Same.
    #    Let me use "has doubled letter" for both.
    #    Wait, but what about a word like "book" (has oo) ending in o? "boo"->"bo" ends o, has double -> no h? Unknown. 
    #    Let me just use "was changed by collapse" as the condition since that's what I derived.
    #    Actually let me reconsider: is it "changed by collapse" or "has a doubled letter"? For uniform-case words these are the same. For mixed-case, no collapse happens so "changed" is false but "has double" could be true. E.g. "aAbB". But mixed case words don't collapse anyway. Let me use "changed by collapse" (i.e., collapse(s) != s).
    #    Hmm, but for mixed-case, collapse returns s unchanged, so "changed" is false. Good.
    #    Let me code it up.
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
    def all_lower(s):
        letters = [c for c in s if c.isalpha()]
        return bool(letters) and all(c.islower() for c in letters)
    def ends_oy(s):
        return bool(s) and s[-1] in 'oy'
    def vowels(s):
        return set(c for c in s.lower() if c in 'aeiou')
    inputs = probe.get("inputs", [])
    out = []
    for s in inputs:
        try:
            words = s.split(' ')
            if len(words) == 1:
                w = collapse(s)
                changed = (w != s)
                if all_lower(w) and ends_oy(w) and changed:
                    out.append(w)
                else:
                    out.append(w + 'h')
            else:
                first = collapse(words[0])
                first_changed = (first != words[0])
                first_letters = set(first.lower())
                tail_parts = []
                for w in words[1:]:
                    filtered = ''.join(c for c in w if c.lower() not in first_letters)
                    filtered = collapse(filtered)
                    tail_parts.append(filtered)
                tail = ''.join(tail_parts)
                add = True
                if not tail:
                    add = False
                elif all_lower(first) and ends_oy(first) and first_changed:
                    add = False
                elif ends_oy(tail) and all_lower(tail):
                    vs = vowels(tail)
                    if len(vs) > 1:
                        add = False
                if add:
                    tail = tail + 'h'
                out.append(first + ' ' + tail)
        except Exception:
            out.append(s + 'h')
    return {"outputs": out}
