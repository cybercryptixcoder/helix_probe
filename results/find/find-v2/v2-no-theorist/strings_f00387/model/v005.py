def predict(probe):
    # Beliefs:
    # - Lowercase everything, then capitalize the first character of the whole string [E1, E2]
    # - Leading whitespace is preserved and prevents capitalization [E2, E7]
    # - Drop lowercase 'm' when it is at the END of a word [E4, E6, E8]
    #   "room"->"roo", "program"->"progra", "team"->"tea", "swim"->"swi",
    #   "album"->"albu", "column"->"colun", "ham"->"ha", "jam"->"ja",
    #   "them"->"the", "system"->"syste", "item"->"ite" [E8]
    # - Drop lowercase 'm' when preceded by "exa" (case-insensitive) [E4, E6]
    #   "example"->"exaple", "exam"->"exa", "Examine"->"Exaine"
    # - The m must be lowercase in the original to be dropped [E4, E6]
    #   "EXAMPLE"->"Example", "exAM"->"Exam" (M uppercase, kept)
    # - "maximum"->"axiu": drop 'm' after "exa"? no. Let's check: "maximum"
    #   lowercased "maximum". m at index 2 (after "ma"), index 4 (after "imu"),
    #   index 6 (end). End-m dropped -> "maximu". But observed "axiu"!
    #   Hmm. "maximum" -> "axiu". That drops m at 0? "maximum"[0]='m' at start.
    #   Wait "maximum" -> "axiu": m,a,x,i,m,u,m -> a,x,i,u. Dropped m at 0, m at 4, m at 6.
    #   m at 0 is at start of word. m at 4 preceded by "axi"? no, "maxi". 
    #   Hmm. Let's reconsider. "minimum" -> "iniu": m,i,n,i,m,u,m -> i,n,i,u.
    #   Dropped m at 0, m at 4, m at 6. Same pattern.
    #   So m at start of word dropped too? "maximum"->"axiu", "minimum"->"iniu".
    #   But "room"->"roo" (m at end), "ham"->"ha" (m at end). 
    #   What about m at start? "maximum" starts with m -> dropped. 
    #   But E4 "Exam"->"Exa" m not at start. "example" m not at start.
    #   Wait, is it: drop m if at start OR at end OR after "exa"?
    #   "maximum": m at 0 (start) drop, m at 4? "maxim" - m at index 4 preceded by "axi",
    #     not exa, not end (index 4 of 7, not end). But observed dropped!
    #   Hmm "maximum" -> "axiu". Let me index: m(0)a(1)x(2)i(3)m(4)u(5)m(6).
    #   Result "axiu" = a,x,i,u. So kept a(1),x(2),i(3),u(5). Dropped m(0),m(4),m(6).
    #   m(4) is between i and u. Why dropped? 
    #   "minimum": m(0)i(1)n(2)i(3)m(4)u(5)m(6). Result "iniu"=i,n,i,u. Dropped m(0),m(4),m(6).
    #   m(4) between i and u again.
    #   Maybe: drop m if it's at start, at end, or between two vowels? m(4) in "maximum" is i_m_u, between i and u (vowels). 
    #   In "minimum" m(4) between i and u. 
    #   Check "exam": e,x,a,m. m at end -> dropped. Good.
    #   "example": e,x,a,m,p,l,e. m at index 3, between a and p. a vowel, p consonant. Not between two vowels. But dropped (after exa).
    #   Hmm, so "after exa" still needed.
    #   Let me reconsider. Maybe simpler: drop m if at start of word, at end of word, or after "exa".
    #   "maximum": m(0) start -> drop. m(6) end -> drop. m(4)? not start, not end, not after exa ("axi"). But dropped!
    #   So that doesn't work.
    #   Alternative: drop m if at start, at end, or preceded by a vowel AND followed by a vowel?
    #   m(4) in maximum: preceded by i (vowel), followed by u (vowel) -> drop. Good.
    #   m(4) in minimum: preceded by i, followed by u -> drop. Good.
    #   "exam": m at end -> drop.
    #   "example": m(3) preceded by a (vowel), followed by p (consonant). Not both vowels. But dropped (after exa).
    #   So need "after exa" too.
    #   Hmm, this is getting complex. Let me reconsider from scratch.
    #   Maybe the rule is: drop m if at start of word, at end of word, or after "exa".
    #   But maximum m(4) contradicts.
    #   Wait maybe I should reconsider: maybe it's not "after exa" but "m preceded by a vowel and followed by a consonant"? 
    #   "example": m after a, before p (consonant). Drop.
    #   "exam": m at end. Drop.
    #   "maximum" m(4): after i, before u (vowel). Not consonant. But dropped.
    #   Hmm no.
    #   Let me just look: which m's are dropped?
    #   maximum: m0, m4, m6 all dropped.
    #   minimum: m0, m4, m6 all dropped.
    #   So ALL m's in maximum/minimum dropped!
    #   "maximum" has 3 m's, all dropped -> "axiu". "minimum" 3 m's all dropped -> "iniu".
    #   So maybe: drop m if at start, at end, after exa, OR ... between vowels?
    #   Actually all m in maximum: m0 start, m4 between i,u, m6 end. All covered by start/end/between-vowels.
    #   minimum: m0 start, m4 between i,u, m6 end. All covered.
    #   So rule: drop m if at start of word, at end of word, between two vowels, or after "exa".
    #   Check "room": m at end -> drop. Good.
    #   "program": m at end -> drop. Good.
    #   "team": m at end -> drop. Good.
    #   "swim": m at end -> drop. Good.
    #   "album": m at end -> drop. Good.
    #   "column": m at end -> drop. Good.
    #   "ham","jam": m at end -> drop. Good.
    #   "them": m at end -> drop. Good.
    #   "system": m at end -> drop. Good.
    #   "item": m at end -> drop. Good.
    #   "exam": m at end -> drop. Good.
    #   "example": m after exa -> drop. Good.
    #   "Examine": m after exa -> drop. Good.
    #   "EXAMPLE": M uppercase -> not dropped. Good.
    #   "exAM": M uppercase -> not dropped. Good.
    #   "ExAm": m lowercase after exa -> drop. Good.
    #   "ExampleWord": m after exa -> drop. Good.
    #   "Examples": m after exa -> drop. Good.
    #   "banana": no m. Good.
    #   "level": no m. Good.
    #   "racecar": no m. Good.
    #   "aMiXeD": m? "amixed" lowercased. m at index 1, between a and i (both vowels) -> drop?!
    #     But observed "Amixed" (m kept!). Contradiction!
    #   Hmm. "aMiXeD" -> "Amixed". m at index 1 in "amixed", between a and i (vowels). If between-vowels rule, would drop -> "aixed". But observed "Amixed".
    #   So between-vowels rule is WRONG.
    #   Let me recheck maximum. "maximum" -> "axiu". 
    #   Maybe the rule is: drop m if at start of word, at end of word, or after "exa".
    #   Then maximum: m0 start drop, m6 end drop, m4? not covered -> would keep -> "maxiu". But observed "axiu".
    #   Hmm. Contradiction either way.
    #   Wait, maybe "maximum" -> "axiu" means m0 dropped, m4 dropped, m6 dropped. Let me recount.
    #   "maximum" = m-a-x-i-m-u-m. 7 chars.
    #   "axiu" = a-x-i-u. 4 chars. So 3 chars dropped: m(0), m(4), m(6). Yes.
    #   So m(4) dropped. m(4) is between i and u.
    #   But "amixed" m(1) between a and i, NOT dropped.
    #   Difference? In maximum, m(4) is preceded by "maxi"... hmm.
    #   Wait, maybe the rule involves "m" being preceded by a consonant? No, i is vowel.
    #   Let me think differently. Maybe the rule is about consecutive... no.
    #   Actually, maybe the rule is: drop m if at start, at end, or if the word contains "exa" before it... no.
    #   Let me reconsider: maybe "maximum"->"axiu" and "minimum"->"iniu" are because of a DIFFERENT rule: drop m if it's the FIRST or LAST letter, OR if preceded by 'i' and followed by 'u'? Too specific.
    #   Hmm, let me reconsider whether m(4) really dropped. "maximum" -> "axiu". 
    #   Could it be "maximum" -> "axiu" via: drop m0 (start), then "aximum", drop m at end -> "aximu", then... "aximu" -> "axiu"? drop m(4) which is now at position 3, between i and u.
    #   Maybe the rule is iterative: repeatedly drop m at start, end, or after exa, until no change? No, m(4) never becomes start/end/after-exa.
    #   Let me try: maybe the rule is drop m if at start OR end OR immediately after "exa" OR immediately before "u"? 
    #   maximum m(4) before u -> drop. minimum m(4) before u -> drop. 
    #   "amixed" m(1) before i, not u -> keep. Good!
    #   Check "room": m at end (also before nothing). Drop via end. Good.
    #   Check "album": m at end. Good.
    #   Check "column": m at end. Good.
    #   Check "exam": m at end. Good.
    #   Check "example": m before p, not u, not end, not start, after exa -> drop via exa. Good.
    #   Check "Examine": m after exa -> drop. Good.
    #   Check "maximum": m0 start drop, m4 before u drop, m6 end drop. -> "axiu". 
    #   Check "minimum": m0 start drop, m4 before u drop, m6 end drop -> "iniu". 
    #   Check "amixed": m before i, not start/end/exa/u -> keep. "Amixed". 
    #   Check "ham": m at end -> drop -> "ha". Good.
    #   Check "jam": m at end -> drop -> "ja". Good.
    #   Check "them": m at end -> drop -> "the". Good.
    #   Check "system": m at end -> drop -> "syste". Good.
    #   Check "item": m at end -> drop -> "ite". Good.
    #   Check "program": m at end -> drop -> "progra". Good.
    #   Check "team": m at end -> drop -> "tea". Good.
    #   Check "swim": m at end -> drop -> "swi". Good.
    #   Check "room": m at end -> drop -> "roo". Good.
    #   Check "zoom": m at end -> drop -> "zoo". Good.
    #   Check "problem": m at end -> drop -> "proble". Good.
    #   Check "from": m at end -> drop -> "fro". Good.
    #   Check "Exam room": Exam m after exa drop -> "Exa"; room m end drop -> "roo". "Exa roo". Good.
    #   Check "an EXAM room": EXAM M uppercase kept -> "exam"; room -> "roo". "An exam roo". Good.
    #   Check "ExampleWord": m after exa drop -> "Exapleword". Good.
    #   Check "Examples": m after exa drop -> "Exaples". Good.
    #   Check "Example": m after exa drop -> "Exaple". Good.
    #   Check "Exam": m after exa drop -> "Exa". Good.
    #   Check "Examine": m after exa drop -> "Exaine". Good.
    #   Check "exam": m after exa drop (also end) -> "exa". Good.
    #   Check "EXAMPLE": M uppercase, not dropped. Good.
    #   Check "eXam": m lowercase after exa (case-insensitive exa) -> drop -> "exa". Good.
    #   Check "exAM": M uppercase -> not dropped -> "exam". Good.
    #   Check "ExAm": m lowercase after exa -> drop -> "exa". Good.
    #   Check "test Example": m after exa drop -> "exaple". "Test exaple". Good.
    #   Check "the example": m after exa drop -> "exaple". "The exaple". Good.
    #   Check "Example test": "Exaple test". Good.
    #   Check "An example": "An exaple". Good.
    #   Check "example text": "Exaple text". Good.
    #   Check "Example123": m after exa drop -> "Exaple123". Good.
    #   So the rule: drop lowercase m if (a) at start of word, (b) at end of word, (c) immediately preceded by "exa" (case-insensitive), or (d) immediately followed by 'u' (lowercase u? or any u?).
    #   Wait, is (d) "followed by u" or "followed by a vowel"? Let me check "amixed": m followed by i (vowel) but kept. So not any vowel. Specifically 'u'? 
    #   Hmm, that's oddly specific. Let me reconsider.
    #   Actually maybe it's simpler: drop m if at start, end, after exa, OR before 'u'. But why 'u'?
    #   Alternatively, maybe the rule is: drop m if at start, end, after exa, or between 'i' and 'u'? In maximum m(4) is i-m-u. minimum i-m-u. amixed a-m-i (not i-m-u). 
    #   Hmm "before u" and "between i and u" both fit. Let me think which is more natural.
    #   Actually, maybe I'm overcomplicating. Let me reconsider: maybe the rule is just "drop m if at start, end, or after exa" and maximum/minimum are special because... no, they're not special.
    #   Wait, let me re-examine "maximum" -> "axiu". What if it's "maximum" -> "axiu" because: drop m at start -> "aximum", then the word "aximum"... no.
    #   Let me just go with: drop m if at start, end, after exa, or before 'u'. Mark with "?".
    #   Actually, let me reconsider "before u". Is there a cleaner rule? 
    #   What if it's: drop m if at start, end, after exa, or if the m is followed by 'u'? 
    #   Hmm, but "mum" -> "mu"? m at start drop, m before u drop, m at end drop -> "u". 
    #   Let me just test: "before u" seems to fit all evidence. But it's suspicious.
    #   Alternative: maybe the rule is drop m if at start, end, after exa, or if preceded by 'i' and followed by 'u'. 
    #   Both fit. I'll go with "before u" as simpler? Or "between i and u"?
    #   Actually, let me reconsider whether there's an even simpler unified rule.
    #   What if: drop m if at start, end, after exa, or if it's the middle of three consecutive... no.
    #   Let me just go with: drop m if at start of word, at end of word, immediately after "exa" (case-insensitive), or immediately before 'u'. Mark "?" on the before-u part.
    #   Hmm, but actually "before u" - is u lowercase? In "maximum" u is lowercase. Let me assume lowercase u.
    #   Wait, actually let me reconsider. What if the rule is: drop m if at start, end, after exa, or if it's followed by a vowel that is NOT 'i'? No, too weird.
    #   Let me reconsider "amixed" once more. "aMiXeD" -> "Amixed". So m kept. m is between a and i.
    #   In maximum, m(4) between i and u, dropped.
    #   Difference: preceded by i vs a. So maybe "preceded by i and followed by u"? Or "preceded by i"?
    #   "minimum" m(4) preceded by i, followed by u. Dropped.
    #   Is there any m preceded by i but not followed by u? "swim": m at end (preceded by i). Dropped via end anyway.
    #   Hmm. Let me go with "followed by u" as the rule since it's simpler and fits.
    #   Actually wait, let me reconsider. What if the rule is: drop m if at start, end, after exa, or if the character after is 'u'? 
    #   I'll go with that. Mark "?".
    import re
    def drop_m(word):
        out = []
        i = 0
        n = len(word)
        while i < n:
            c = word[i]
            if c == 'm':
                at_start = (i == 0)
                at_end = (i == n - 1)
                after_exa = (i >= 3 and word[i-3:i].lower() == 'exa')
                before_u = (i + 1 < n and word[i+1] == 'u')
                if at_start or at_end or after_exa or before_u:
                    i += 1
                    continue
            out.append(c)
            i += 1
        return ''.join(out)
    def f(s):
        words = re.split(r'(\s+)', s)
        s2 = ''.join(drop_m(w) if w.strip() else w for w in words)
        if not s2:
            return s2
        return s2[:1].upper() + s2[1:].lower()
    return {"outputs": [f(s) for s in probe["inputs"]]}
