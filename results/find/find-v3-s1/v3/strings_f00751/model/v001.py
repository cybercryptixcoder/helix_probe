def predict(probe):
    # Insert 'i' immediately after every vowel (a,e,i,o,u), case-insensitive [E2, E3]
    # Vowels: a->ai, e->ei, i->ii, o->oi, u->ui [E2]
    # Consonants, digits, symbols, spaces unchanged [E2, E3]
    # Case preserved: 'MiXeD' -> 'MiXeDi' (i after D? no—after e) [E2]
    #   Actually 'MiXeD' -> 'MiXeDi': the 'i' inserted after 'e' (vowel) [E2]
    # 'Mississippi' -> 'Missiissippi': i after each i (i,i,i) [E2]
    # 'test case' -> 'testi case': i after 'e' in 'test' [E2]
    # 'test case  ' -> 'test icase': i after 'e' in 'test', space preserved [E3]
    # 'a e i o u' -> 'a e ii o u': only the standalone 'i' got doubled [E2]
    #   Wait: 'a'->? observed 'a e ii o u' — a,e,o,u unchanged, only i doubled.
    #   Recheck E2: 'cat'->'ciat' (a->ai), 'dog'->'diog' (o->oi), 'banana'->'baniana' (a->ai)
    #   So a,e,o,u DO get i. But 'a e i o u' -> 'a e ii o u' contradicts!
    #   Hmm. Let me recheck: "a e i o u" -> "a e ii o u". Only i doubled.
    #   But 'cat'->'ciat'. Difference: in 'a e i o u' the vowels are single-letter words separated by spaces.
    #   Maybe rule: insert i after vowel only if followed by a consonant or end-of-word? 
    #   'cat': a followed by t -> ai. 'dog': o followed by g -> oi. 'banana': a followed by n -> ai.
    #   'hello world': e followed by l -> ei? observed 'helloi world' — that's o->oi (o followed by space? no, 'hello' o at end).
    #   'hello' -> 'helloi': o at end of word -> oi. So end-of-word counts.
    #   'a e i o u': each vowel is a single-letter word, followed by space. If space counts as "not insert", then no insert.
    #   'test case' -> 'testi case': e followed by s -> ei. Good.
    #   'test case  ' -> 'test icase': e followed by s -> ei. Good.
    #   'data a Python' -> 'data a iPython': 'a' standalone unchanged, 'Python' o followed by n -> oi. Good.
    #   'test caseMiXeD' -> 'test caiseMiXeD': 'case' e at end of word (before M) -> ei. Good.
    #   'test case Zebra' -> 'test caise Zebra': e at end of 'case' -> ei. Good.
    #   'Mississippi' -> 'Missiissippi': i followed by s -> ii (first i), i followed by s -> ii, i at end -> ii. Good.
    #   'racecar' -> 'raciecar': e followed by c -> ei. Good.
    #   'level123' -> 'leveil123': e followed by l -> ei. Good.
    #   'Python!@#' -> 'Pythion!@#': o followed by n -> oi. Good.
    #   'racecar Zebra level' -> 'racecar Ziebra level': e followed by b -> ei. Good.
    #   'level' -> 'level' unchanged? observed 'level' in 'racecar Ziebra level' stays 'level'.
    #     Wait 'level' has e followed by v -> should be 'leveil'. But observed 'level' unchanged!
    #     Hmm, contradiction. Let me recheck E3: "racecar Zebra level" -> "racecar Ziebra level". 'level' unchanged.
    #     But 'level123' -> 'leveil123' (e->ei). So 'level' alone vs 'level123' differ?
    #     In 'level123', e followed by l -> ei. In 'level' (end of string), e followed by l too... same.
    #     Unless: only insert i after vowel if there's a LATER vowel in the word? 'level' has e...l...e...l. 
    #     Hmm 'level' -> 'level' unchanged but 'level123' -> 'leveil123'. The only diff is trailing digits.
    #     Maybe rule: insert after vowel only if vowel is NOT the last vowel in the word? 
    #     'level': vowels e,e. First e -> ei? observed unchanged. So no.
    #   Let me reconsider. Maybe the rule involves the NEXT character being a consonant, AND something else.
    #   'level' unchanged: e followed by v (consonant). 'level123': e followed by l (consonant) -> ei.
    #   Wait 'level' first e followed by v, second e followed by l. Neither inserted.
    #   'level123' first e followed by v -> ei (observed 'leveil123': l-e-v-e-i-l... wait that's second e->ei).
    #   'leveil123': l,e,v,e,i,l. So the SECOND e (followed by l) got i. First e (followed by v) did not.
    #   So maybe: insert i after vowel only if followed by 'l'? No—'cat' a followed by t -> ai.
    #   Hmm, 'cat'->'ciat': a followed by t. 'level' e followed by v: no insert. 
    #   Difference: maybe only certain following consonants? t yes, v no?
    #   'dog' o followed by g -> oi. g yes.
    #   'banana' a followed by n -> ai. n yes.
    #   'hello' o at end -> oi. end yes.
    #   'test' e followed by s -> ei. s yes.
    #   'case' e at end -> ei. end yes.
    #   'Mississippi' i followed by s -> ii. s yes.
    #   'racecar' e followed by c -> ei. c yes.
    #   'Python' o followed by n -> oi. n yes.
    #   'Zebra' e followed by b -> ei. b yes.
    #   'level' e followed by v -> NO. v is the exception?
    #   'level123' second e followed by l -> ei. l yes.
    #   So maybe v is excluded? Only one data point. Hmm.
    #   Actually wait: 'level' -> 'level' unchanged. But maybe the rule is different: insert i after vowel if the vowel is followed by a consonant that is NOT 'v'? Weak.
    #   Let me reconsider 'a e i o u' -> 'a e ii o u'. Single vowels as words. a followed by space: no. e followed by space: no. i followed by space: YES (ii). o followed by space: no. u followed by space: no.
    #   So 'i' behaves differently! i followed by space -> ii, but a,e,o,u followed by space -> unchanged.
    #   And 'Mississippi' i followed by s -> ii (consistent, i always doubles).
    #   So maybe: 'i' always gets doubled (i->ii), and a,e,o,u get 'i' inserted only when followed by a consonant (not space, not end)?
    #   Check 'hello' o at end -> oi. But end is not consonant. Contradiction.
    #   Hmm 'hello' -> 'helloi'. o at end of word -> oi.
    #   But 'a e i o u': o followed by space (end of word) -> unchanged. Contradiction with 'hello'.
    #   Unless 'hello' the o is followed by space too (end of word before space). Same as 'o' in 'a e i o u'.
    #   So why 'hello'->'helloi' but 'o'->'o'? 
    #   Difference: 'hello' has other letters before o. 'o' is a single-letter word.
    #   Maybe rule: insert i after vowel if the word has length > 1? 'a','e','i','o','u' single-letter words: only i doubles.
    #   Hmm but i doubles even as single letter. Weird.
    #   Let me just go with: for each vowel, insert 'i' after it, EXCEPT when the vowel is a single-letter word (surrounded by spaces/boundaries) and is not 'i'. And 'i' always doubles.
    #   Check 'data a Python': 'a' standalone unchanged (single-letter word, not i). Good.
    #   'test case Zebra': no single-letter words. Good.
    #   'level': e followed by v... still need to explain no insert.
    #   Hmm 'level' -> 'level'. Both e's unchanged. But 'level123' second e->ei.
    #   Wait maybe I misread. 'level123' -> 'leveil123'. l-e-v-e-i-l. Yes second e->ei.
    #   'level' -> 'level'. l-e-v-e-l. No insert.
    #   The difference: trailing '123'. Maybe digits after the word affect? Unlikely.
    #   Or maybe: insert i after vowel only if followed by consonant AND there's a character after that consonant? 
    #   'level': first e followed by v, then e. Second e followed by l, then end. 
    #   'level123': second e followed by l, then 1. So insert because l is followed by 1?
    #   'hello': o at end, nothing after. But o->oi. Contradiction.
    #   Hmm. Let me look again: 'hello world' -> 'helloi world'. o followed by space -> oi.
    #   'a e i o u': o followed by space -> o (unchanged). 
    #   So same context (o followed by space) gives different results! 'hello' vs 'o'.
    #   The difference must be word length or position. In 'hello', o is not the first char. In 'o', it is.
    #   Maybe rule: insert i after vowel if it's NOT the first character of a word? 
    #   'cat': a is 2nd char -> ai. Good.
    #   'dog': o is 2nd -> oi. Good.
    #   'banana': a's at positions 2,4,6 -> all ai. Good.
    #   'hello': o at position 5 -> oi. Good.
    #   'a e i o u': each vowel is first char of its word -> unchanged. But i doubled! 
    #   So i is special: always doubles regardless.
    #   'Mississippi': i's at positions 2,5,8,11. First i at position 2 (not first char) -> ii. Good.
    #   'test': e at position 2 -> ei. Good.
    #   'case': e at position 4 -> ei. Good.
    #   'racecar': e at position 4 -> ei. Good.
    #   'Python': o at position 5 -> oi. Good.
    #   'Zebra': e at position 2 -> ei. Good.
    #   'level': e's at positions 2,4. Both not first char. Should be ei. But observed unchanged!
    #   Contradiction again. Unless 'level' is special.
    #   Wait, maybe I should recheck: 'racecar Zebra level' -> 'racecar Ziebra level'. Is 'level' really unchanged? Yes.
    #   But 'level123' -> 'leveil123'. 
    #   Hmm what if the rule is: insert i after vowel if followed by a consonant, but NOT if that consonant is 'v' or 'l'? 
    #   'level': e followed by v (no), e followed by l (no). Good.
    #   'level123': e followed by v (no), e followed by l (no)... but observed ei. Contradiction.
    #   I'm stuck on 'level'. Let me try: maybe the rule is about the LAST vowel in the word getting i, or something with parity.
    #   'level123': only second e got i. 'level': neither. 
    #   Actually maybe 'level' -> 'level' is a typo in my reading. Let me trust the data: 'racecar Ziebra level' — the last word is 'level' unchanged.
    #   Alternatively: maybe insert i after vowel only if the vowel is followed by a consonant that comes before another vowel? No.
    #   Let me try a different hypothesis: insert 'i' after a vowel if the vowel is immediately followed by a consonant, AND that consonant is immediately followed by a vowel OR end-of-string? 
    #   'cat': a followed by t, t followed by end -> ai. Good.
    #   'dog': o followed by g, g followed by end -> oi. Good.
    #   'banana': a followed by n, n followed by a (vowel) -> ai. Good. (all three a's)
    #   'hello': o followed by end -> oi. Good.
    #   'test': e followed by s, s followed by t (consonant) -> should NOT insert. But observed 'testi' -> ei. Contradiction.
    #   Hmm.
    #   Let me try: insert i after vowel if followed by consonant, EXCEPT when the consonant is 'v'. 
    #   'level': e-v (no), e-l (should be yes) -> 'leveil'. But observed 'level'. Contradiction.
    #   OK here's another thought: maybe the rule is insert i after vowel if the vowel is followed by a consonant AND the vowel is not preceded by a consonant that... no.
    #   Let me count: 'level' has e at pos 2 and 4. 'level123' same. Only difference is trailing digits.
    #   Could the rule depend on total length or something? 'level' length 5, 'level123' length 8.
    #   Maybe: insert i after vowel only if the word (or string) has length > some threshold? 'a e i o u' length 9 but no insert (except i).
    #   This is getting too speculative. Let me go with the simplest rule that fits most data:
    #   Rule: insert 'i' after each vowel (a,e,i,o,u) that is followed by a consonant or is at end-of-string, EXCEPT single-letter words (except 'i' which always doubles).
    #   This fits everything except 'level' (which would become 'leveil'). I'll note 'level' as an anomaly / possible exception I can't resolve.
    #   Actually, wait. Let me recheck 'level' in E3: "racecar Zebra level" -> "racecar Ziebra level". 
    #   Hmm what if the box only processes the FIRST occurrence or something? No, 'banana' all a's processed.
    #   What if 'level' is a palindrome and palindromes are treated specially? 'racecar' is a palindrome and it got 'raciecar' (e->ei). So no.
    #   I'll go with the general rule and accept 'level' as unexplained. Actually, let me reconsider: maybe I misread and it's 'leveil'. The observation says "racecar Ziebra level". I'll trust it.
    #   Given uncertainty, I'll implement: insert i after vowel if followed by consonant or end-of-string, but skip single-letter words (except i). Mark 'level' anomaly with ?.
    import re
    def transform(s):
        out = []
        n = len(s)
        for idx, ch in enumerate(s):
            out.append(ch)
            low = ch.lower()
            if low in 'aeiou':
                # determine if single-letter word
                prev = s[idx-1] if idx > 0 else ' '
                nxt = s[idx+1] if idx+1 < n else ' '
                is_single = (prev == ' ' or idx == 0) and (nxt == ' ' or idx+1 == n)
                if low == 'i':
                    out.append('i')
                elif is_single:
                    pass
                else:
                    # insert if followed by consonant or end
                    if idx+1 == n or not s[idx+1].isalpha() or s[idx+1].lower() not in 'aeiou':
                        # followed by consonant, digit, symbol, or end -> insert
                        # but if followed by space (end of word) -> insert? 'hello' o->oi yes
                        out.append('i')
                    # if followed by vowel, no insert
        return ''.join(out)
    return {"outputs": [transform(x) for x in probe["inputs"]]}
