def predict(probe):
    # Capitalize first letter of whole string, lowercase the rest [E1: HELLO->Hello, abc123->Abc123]
    # Insert "10" after the first character of each word? No — see below.
    # "10" position rule (priority order):
    #   - If string has a space: insert "10" right after the first space [E1: "a b c"->"A 10b c", "two words"->"Two 10words"]
    #   - Else if string has a digit: insert "10" before first digit if letters precede, else after first digit [E1: abc123->Abc10123, 12345->1210345]
    #   - Else (pure letters): insert "10" after the first character [E2: cat->C10at, dog->D10og, sky->S10ky, rhythm->Rhy10thm? no...]
    #   Wait E2: rhythm->Rhy10thm: "10" after "Rhy" (3 chars). apple->Ap10ple (after 2). eat->E10at (after 1). be->B10e (after 1). a->10a (after 0). by->B10y (after 1). open->Op10en (after 2).
    #   Hmm not fixed position. Let's find pattern:
    #     cat->C|10|at (after 1), dog->D|10|og (after 1), sky->S|10|ky (after 1)
    #     rhythm->Rhy|10|thm (after 3), apple->Ap|10|ple (after 2), eat->E|10|at (after 1)
    #     be->B|10|e (after 1), a->|10|a (after 0), by->B|10|y (after 1), open->Op|10|en (after 2)
    #   Look at the letter before "10": cat: 'C'(cons), dog:'D'(cons), sky:'S'(cons), rhythm:'y'(vowel!), apple:'p'(cons), eat:'E'(vowel), be:'B'(cons), a: nothing, by:'B'(cons), open:'p'(cons).
    #   Hmm rhythm: Rhy|10|thm — 'y' before. apple: Ap|10|ple — 'p'. open: Op|10|en — 'p'.
    #   Maybe insert "10" before the first vowel that is NOT the first character? 
    #     cat: first vowel 'a' at idx1, not first char -> insert before 'a': C|10|at yes!
    #     dog: 'o' at idx1 -> D|10|og yes!
    #     sky: no vowel except 'y'? 'y' at idx2. If y counts as vowel: S k |10| y? that's after 2, but observed S|10|ky (after 1). So y not vowel here, and no vowel -> insert after 1st char? S|10|ky yes.
    #     rhythm: vowels? 'y' at idx2? observed Rhy|10|thm = after 3 chars, before 't'. If 'y' is vowel at idx2, insert after it -> Rhy|10|thm yes!
    #     apple: first vowel 'a' at idx0 (first char), skip; next vowel 'e' at idx4 -> insert before 'e': Appl|10|e? observed Ap|10|ple. No.
    #   Hmm. apple->Ap|10|ple: before 'p' at idx2? or after 'p' idx1.
    #   Let me reconsider: maybe insert "10" after the first consonant cluster? 
    #     cat: C|10|at (after C, 1 cons), dog: D|10|og, sky: Sk|10|y? no observed S|10|ky.
    #   Try: insert "10" after the first letter that is a consonant followed by a vowel? 
    #     cat: C then a(vowel) -> after C: C|10|at yes
    #     dog: D then o -> D|10|og yes
    #     sky: S then k(cons) no, k then y? y cons? -> S k |10| y? observed S|10|ky. no.
    #   Let me tabulate index where "10" inserted (number of chars before it):
    #     cat:1, dog:1, sky:1, rhythm:3, apple:2, eat:1, be:1, a:0, by:1, open:2
    #   Number of chars before = position. Look at char at that position (the char right after "10"):
    #     cat: 'a', dog:'o', sky:'k', rhythm:'t', apple:'p', eat:'a', be:'e', a:'a', by:'y', open:'e'
    #   Char before "10":
    #     cat:'C', dog:'D', sky:'S', rhythm:'y', apple:'p', eat:'E', be:'B', a:none, by:'B', open:'p'
    #   Hmm. Maybe: insert "10" after the first vowel, but if the first vowel is the first character, insert after the SECOND character? 
    #     cat: first vowel 'a' idx1 -> after -> C a |10| t? that's Ca|10|t, but observed C|10|at. No.
    #   Let me reconsider from scratch. Maybe insert "10" before the first vowel, unless vowel is at index 0, then after first char?
    #     cat: 'a' idx1 -> before: C|10|at yes
    #     dog: 'o' idx1 -> D|10|og yes
    #     sky: no vowel -> ? S|10|ky (after 1)
    #     rhythm: 'y'? if y vowel idx2 -> before: Rh|10|ythm? observed Rhy|10|thm. no.
    #   Try: insert "10" after the first vowel, unless vowel at index 0 then after index 1?
    #     cat: 'a' idx1 -> after: Ca|10|t? no, observed C|10|at.
    #   Hmm cat is C|10|at. So "10" is between C and a. That's BEFORE the vowel 'a'.
    #   dog: D|10|og, before 'o'. sky: S|10|ky, before 'k'. rhythm: Rhy|10|thm, before 't'. apple: Ap|10|ple, before 'p'. eat: E|10|at, before 'a'. be: B|10|e, before 'e'. a: |10|a, before 'a'. by: B|10|y, before 'y'. open: Op|10|en, before 'e'.
    #   So "10" is inserted right before some character. Which character?
    #     cat: before 'a' (vowel)
    #     dog: before 'o' (vowel)
    #     sky: before 'k' (cons)
    #     rhythm: before 't' (cons)
    #     apple: before 'p' (cons)
    #     eat: before 'a' (vowel)
    #     be: before 'e' (vowel)
    #     a: before 'a' (vowel)
    #     by: before 'y' (cons? or vowel)
    #     open: before 'e' (vowel)
    #   Number of chars before insertion: cat:1, dog:1, sky:1, rhythm:3, apple:2, eat:1, be:1, a:0, by:1, open:2.
    #   Hmm. Maybe it's about the FIRST vowel position: insert "10" at position = index of first vowel, but if that's 0, insert at 0? 
    #     cat: first vowel 'a' idx1 -> insert at 1: C|10|at yes!
    #     dog: 'o' idx1 -> D|10|og yes!
    #     sky: no vowel -> ? observed insert at 1. Maybe default 1?
    #     rhythm: first vowel? 'y' idx2 (if y vowel) -> insert at 2: Rh|10|ythm? observed Rhy|10|thm (insert at 3). If y not vowel, no vowel -> default 1? but observed 3. Hmm.
    #   Wait rhythm: R h y t h m. If 'y' is a vowel at idx2, insert at 2 gives Rh|10|ythm. Observed Rhy|10|thm = insert at 3. So insert AFTER first vowel? cat: after 'a' idx1 -> insert at 2: Ca|10|t, no.
    #   I'm going in circles. Let me look at apple: A p p l e. Observed Ap|10|ple = insert at 2. First vowel 'a' idx0, second vowel 'e' idx4. Insert at 2 = after "Ap". Hmm.
    #   open: O p e n. Observed Op|10|en = insert at 2. First vowel 'o' idx0, second 'e' idx2. Insert at 2 = before 'e' = before second vowel!
    #   apple: insert at 2 = before 'p' idx2, second vowel 'e' idx4. Not before second vowel.
    #   Hmm apple insert at 2, open insert at 2. Both start with vowel. 
    #   eat: E a t. insert at 1. Starts with vowel 'E' idx0, second vowel 'a' idx1. Insert at 1 = before second vowel 'a'! yes!
    #   So for words starting with a vowel: insert before the SECOND vowel (or after first vowel).
    #     eat: E|10|at yes (after E, before a)
    #     apple: A p p l e: after first vowel 'A'? that's insert at 1: A|10|pple? observed Ap|10|ple (insert at 2). Hmm no.
    #   Wait apple: A p p l e. If insert after first vowel 'A' (idx0) -> insert at 1: A|10|pple. Observed Ap|10|ple. So insert at 2, after 'Ap'.
    #   Hmm. Let me reconsider: maybe insert "10" after the first consonant-vowel pair? 
    #     apple: A(vowel) p(cons) p(cons) l(cons) e(vowel). First cons-vowel pair? 'p' then... no vowel after p until e. 
    #   Let me try: insert "10" after the first letter, then skip if... no.
    #   Let me look at number of chars before "10" again and the string:
    #     cat(3):1, dog(3):1, sky(3):1, rhythm(6):3, apple(5):2, eat(3):1, be(2):1, a(1):0, by(2):1, open(4):2
    #   Ratio? cat 1/3, rhythm 3/6=0.5, apple 2/5=0.4, open 2/4=0.5, eat 1/3, be 1/2=0.5, by 1/2=0.5, a 0/1=0.
    #   Hmm rhythm 3, open 2 (half). apple 2 (not half of 5). 
    #   Maybe insert "10" after the first syllable? Vowel-consonant boundary?
    #     cat: C-a-t: after C (onset) -> C|10|at
    #     dog: D-o-g -> D|10|og
    #     sky: S-k-y -> S|10|ky (after first cons, since 'y' acts as vowel nucleus)
    #     rhythm: R-h-y-t-h-m: 'y' is nucleus -> Rhy|10|thm (after onset Rhy)
    #     apple: A-p-p-l-e: first syllable "Ap"? -> Ap|10|ple
    #     eat: E-a-t: first syllable "E"? -> E|10|at
    #     be: B-e: -> B|10|e
    #     a: A: -> |10|a (empty onset)
    #     by: B-y: -> B|10|y
    #     open: O-p-e-n: first syllable "Op"? -> Op|10|en
    #   This is syllable-based! Insert "10" after the first syllable (onset+nucleus, i.e., after the first vowel and any following consonants that close... no).
    #   Actually simpler: insert "10" after the first vowel AND the consonants immediately following it that belong to onset of next syllable? Too complex.
    #   Let me try: insert "10" after the first vowel, then also include following consonants up to (but not including) the next vowel? 
    #     cat: after 'a' (idx1), next vowel none -> Ca|10|t? no observed C|10|at.
    #   Hmm cat is C|10|at, before 'a'. So it's before the first vowel, not after.
    #   But eat is E|10|at, after 'E' (first vowel). Contradiction unless first char special.
    #   Let me try: insert "10" at position = index of first vowel, but if first vowel is at index 0, then position = index of second vowel, but if no second vowel, position = 1?
    #     cat: first vowel 'a' idx1 -> insert at 1: C|10|at yes
    #     dog: 'o' idx1 -> D|10|og yes
    #     sky: no vowel -> ? observed 1. default 1?
    #     rhythm: 'y'? if y vowel idx2 -> insert at 2: Rh|10|ythm? observed 3. If y not vowel, no vowel -> default 1? but observed 3. Hmm.
    #   rhythm is the problem. R h y t h m. Observed Rhy|10|thm. If we treat 'y' as vowel at idx2, insert at 2 gives Rh|10|ythm (wrong). Insert after y (idx3) gives Rhy|10|thm (right). So for rhythm, insert AFTER first vowel.
    #   But cat: insert BEFORE first vowel 'a'. Contradiction.
    #   Unless: insert after first vowel, but cat's first vowel... C a t. After 'a' idx1 -> insert at 2: Ca|10|t. Observed C|10|at. No.
    #   I'm stuck on a clean rule. Let me try yet another: insert "10" after the first letter that is a consonant, if the next letter is a vowel? 
    #     cat: C(cons) next a(vowel) -> after C: C|10|at yes
    #     dog: D next o -> D|10|og yes
    #     sky: S next k(cons) no; k next y? y cons? no; -> no match. observed S|10|ky (after S). Hmm.
    #   Try: insert "10" after the first consonant (regardless):
    #     cat: after C -> C|10|at yes
    #     dog: after D -> D|10|og yes
    #     sky: after S -> S|10|ky yes
    #     rhythm: after R -> R|10|hythm? observed Rhy|10|thm. No.
    #   rhythm breaks it. Rhy|10|thm: after "Rhy". 'y' is the vowel here.
    #   Maybe: insert "10" after the first vowel (a,e,i,o,u, and y when it's the only vowel-like)?
    #     cat: first vowel 'a' idx1 -> after: Ca|10|t? no.
    #   OK let me just look at it as: insert "10" after the first "vowel group" where vowel group = maximal run of vowels? 
    #     cat: 'a' run at idx1 -> after idx2: Ca|10|t no.
    #   Hmm. Let me reconsider whether it's "before first vowel" for most, and rhythm/apple/open are different because...
    #   Actually wait: maybe insert "10" after the first consonant cluster (onset), i.e., after leading consonants:
    #     cat: leading cons "C" -> C|10|at yes
    #     dog: "D" -> D|10|og yes
    #     sky: "Sk" -> Sk|10|y? observed S|10|ky. No.
    #   sky: S|10|ky. Leading cons "Sk", but insert after "S" only. Hmm. Unless 'y' is vowel and 'k' is... no.
    #   Let me try: insert "10" after the first character that is a consonant followed by a vowel OR at end of leading consonants if next is consonant... 
    #   sky: S k y. S cons, k cons, y vowel. Insert after S (first cons)? S|10|ky yes. So after first consonant.
    #   rhythm: R h y t h m. R cons, h cons, y vowel. After first consonant R -> R|10|hythm. Observed Rhy|10|thm. No.
    #   Argh rhythm.
    #   Let me reconsider rhythm: maybe 'y' is treated as vowel, and rule is "insert after first vowel" but for cat 'a' is vowel... 
    #   Wait, maybe the rule is: insert "10" after the first vowel, BUT the "first vowel" search treats the string differently. Let me check: cat C-a-t, insert after 'a' = Ca|10|t. But observed C|10|at. 
    #   Unless... the observed is C10at and I should read it as insert after C. Yes C|10|at.
    #   Hmm what if it's: insert "10" before the first vowel, EXCEPT if the word starts with a vowel, then insert after the first consonant following it? 
    #     cat: before 'a' -> C|10|at yes
    #     dog: before 'o' -> D|10|og yes
    #     sky: no vowel (y cons?) -> ? S|10|ky. before 'k'? 'k' is first cons after S. Hmm.
    #     rhythm: before first vowel? 'y' vowel idx2 -> Rh|10|ythm? no.
    #   I'll try a different tack: maybe it's "insert 10 after the first letter, then move it right past any following consonants until just before a vowel"? 
    #     cat: after C, next 'a' vowel -> stop before 'a': C|10|at yes
    #     dog: after D, next 'o' -> D|10|og yes
    #     sky: after S, next 'k' cons -> move past k, next 'y'? if y vowel stop before y: Sk|10|y? observed S|10|ky. No.
    #   Hmm sky S|10|ky means 10 right after S, before k. So it did NOT move past k.
    #   I think I'm overcomplicating. Let me just fit: position = index of first vowel (a,e,i,o,u), and if that index is 0, use index of next vowel, and if no vowel, use 1, and treat 'y' as vowel only if no other vowel.
    #     cat: 'a' idx1 -> 1 ✓
    #     dog: 'o' idx1 -> 1 ✓
    #     sky: no aeiou, 'y' idx2 -> but observed 1. ✗ (would give 2)
    #   Hmm sky observed 1.
    #   What if 'y' never counts as vowel, and no-vowel -> position 1?
    #     sky: no vowel -> 1 ✓
    #     rhythm: no aeiou -> 1? observed 3. ✗
    #   rhythm is really the outlier. Rhy|10|thm. 
    #   Let me reconsider: maybe the rule is "insert 10 after the first vowel, where y counts as vowel, but if the first vowel is at index 0, insert after it (position 1)"? 
    #     cat: 'a' idx1 -> after -> 2? no observed 1.
    #   OK here's another idea: insert "10" at position = (index of first vowel) if vowel not at 0, else (index of first vowel after 0)... 
    #   Let me just look at ALL positions and see if there's a simple formula:
    #     cat:1, dog:1, sky:1, rhythm:3, apple:2, eat:1, be:1, a:0, by:1, open:2
    #   What if position = number of leading consonants + (1 if starts with vowel else 0)? 
    #     cat: leading cons 1 -> 1 ✓
    #     dog: 1 ✓
    #     sky: leading cons "Sk" = 2 -> 2? observed 1 ✗
    #   Hmm sky leading cons is Sk (2) but observed 1.
    #   What if leading consonants but stop at first consonant if next is consonant? no.
    #   Let me try: position = index of first vowel (aeiouy), but if that's the last... 
    #     cat: 'a' idx1 -> 1 ✓
    #     dog: 'o' idx1 -> 1 ✓
    #     sky: 'y' idx2 -> 2? observed 1 ✗
    #   Hmm sky again.
    #   Wait, maybe sky: S|10|ky, and 'y' is NOT a vowel, so no vowel, and the rule for no-vowel is position 1. And rhythm: R-h-y-t-h-m, 'y' NOT vowel, no vowel, position 1? but observed 3. Contradiction between sky and rhythm both no-vowel.
    #   Unless rhythm has a vowel I'm missing... R h y t h m. No aeiou. So both no aeiou. sky->1, rhythm->3. Different! So 'y' must matter differently, or length matters.
    #   sky length 3 -> 1, rhythm length 6 -> 3. Half? sky 3/2=1.5->1, rhythm 6/2=3. apple 5/2=2.5->2. open 4/2=2. eat 3/2=1.5->1. be 2/2=1. by 2/2=1. a 1/2=0.5->0. cat 3/2=1.5->1. dog 3/2=1.5->1. 
    #   WOW. position = floor(length/2)? Let me check:
    #     cat len3 -> 1 ✓
    #     dog len3 -> 1 ✓
    #     sky len3 -> 1 ✓
    #     rhythm len6 -> 3 ✓
    #     apple len5 -> 2 ✓
    #     eat len3 -> 1 ✓
    #     be len2 -> 1 ✓
    #     a len1 -> 0 ✓
    #     by len2 -> 1 ✓
    #     open len4 -> 2 ✓
    #   ALL MATCH! position = len//2 (integer division).
    #   Check E1 pure-letter words: hello len5 -> 2: He|10|llo ✓. world len5 -> 2: Wo|10|rld ✓. test! len5 -> 2: Te|10|st! ✓. x len1 -> 0: |10|x ✓.
    #   And "two words" len9 -> 4: "Two "|10|"words" = Two 10words ✓ (position 4 = after "Two "). 
    #   "a b c" len5 -> 2: "A "|10|"b c" = A 10b c ✓ (position 2 = after "A ").
    #   abc123 len6 -> 3: "Abc"|10|"123" = Abc10123 ✓!
    #   12345 len5 -> 2: "12"|10|"345" = 1210345 ✓!
    #   IT'S JUST len//2! Insert "10" at the middle (floor) of the string, after capitalization.
    #   Capitalization: first char upper, rest lower [E1: HELLO->Hello].
    #   Let me verify all E1/E2 with this simple rule.
    import re
    def transform(s):
        if not s:
            return s
        t = s[0].upper() + s[1:].lower()
        p = len(t) // 2
        return t[:p] + '10' + t[p:]
    return {"outputs": [transform(x) for x in probe["inputs"]]}
