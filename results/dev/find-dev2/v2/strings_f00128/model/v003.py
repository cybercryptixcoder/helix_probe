def predict(probe):
    # Capitalize first char, lowercase the rest [E1: HELLO->Hello, Hello->Hello]
    # Insert "10" at position len//2 of the capitalized string [E1,E2,E3]
    #   E2: cat->C10at, rhythm->Rhy10thm, a->10a all match len//2
    #   E3: "A"->"10a" (len1, pos0, but output is "10a" lowercase!) 
    #   Wait: "A"->"10a": the 'A' became lowercase 'a'! And "ab"->"A10b" (capitalized).
    #   So for single char "A": output "10a" — lowercase, not "10A".
    #   Hmm. "a"->"10a" [E2] and "A"->"10a" [E3]. Both give "10a".
    #   But "ab"->"A10b" (capitalized). "abc"->"A10bc".
    #   So capitalization applies normally, but "A"->"10a" is lowercase.
    #   Maybe: capitalize first char, then insert "10" at len//2. For "A": cap->"A", pos0, "10"+"A"="10A". But observed "10a".
    #   Unless: the "10" insertion happens, then... no.
    #   Alternative: lowercase whole string first, then capitalize first char, then insert. Same thing.
    #   Why "10a" lowercase? Maybe when "10" is inserted at position 0, the following char is lowercased?
    #   Check "a"->"10a" [E2]: consistent (already lowercase).
    #   Check "x"->"10x" [E1]: lowercase x! And "x" cap would be "X". So "10x" not "10X".
    #   So rule: if insertion position is 0, the char after "10" is lowercase.
    #   Actually maybe simpler: the whole string is lowercased, THEN first char capitalized, THEN "10" inserted at len//2, but if pos==0 the capitalization is lost because "10" goes before it.
    #   Wait: "x"->cap "X", insert at 0: "10X". Observed "10x". So the 'X' got lowercased.
    #   Hmm. Or: insert "10" at len//2 into the LOWERCASED string, then capitalize the first char of the RESULT? 
    #     "x": lower "x", insert at 0: "10x", capitalize first char: "10x" (first char is '1', no change) -> "10x" ✓
    #     "a": "10a" ✓
    #     "A": lower "a", insert at 0: "10a", cap first: "10a" ✓
    #     "ab": lower "ab", insert at 1: "a10b", cap first: "A10b" ✓
    #     "abc": "ab"+"10"+"c"="ab10c", cap: "Ab10c"? observed "A10bc". ✗
    #   Hmm abc len3 pos1: "a"+"10"+"bc"="a10bc", cap->"A10bc" ✓. I miscalculated.
    #     "hello": lower "hello", pos2: "he10llo", cap: "He10llo" ✓
    #     "HELLO": lower "hello", pos2: "he10llo", cap: "He10llo" ✓
    #     "Hello, World!": lower "hello, world!", len13 pos6: "hello,"+"10"+" world!"="hello,10 world!", cap: "Hello,10 world!" ✓
    #     "New York": lower "new york", len8 pos4: "new "+"10"+"york"="new 10york", cap: "New 10york" ✓
    #     "two words": lower "two words", len9 pos4: "two "+"10"+"words"="two 10words", cap: "Two 10words" ✓
    #     "a b c": lower "a b c", len5 pos2: "a "+"10"+"b c"="a 10b c", cap: "A 10b c" ✓
    #     "abc123": lower "abc123", len6 pos3: "abc"+"10"+"123"="abc10123", cap: "Abc10123" ✓
    #     "12345": lower, len5 pos2: "12"+"10"+"345"="1210345", cap: "1210345" ✓
    #     "test!": lower "test!", len5 pos2: "te"+"10"+"st!"="te10st!", cap: "Te10st!" ✓
    #     "cat": "ca10t"->"Ca10t"? observed "C10at". ✗!
    #   Wait cat len3 pos1: "c"+"10"+"at"="c10at", cap: "C10at" ✓. I keep miscalculating.
    #   OK so rule: lowercase whole string, insert "10" at len//2, then capitalize first char.
    #   Check "rhythm": len6 pos3: "rhy"+"10"+"thm"="rhy10thm", cap: "Rhy10thm" ✓
    #   Check "apple": len5 pos2: "ap"+"10"+"ple"="ap10ple", cap: "Ap10ple" ✓
    #   Check "open": len4 pos2: "op"+"10"+"en"="op10en", cap: "Op10en" ✓
    #   Check "eat": len3 pos1: "e"+"10"+"at"="e10at", cap: "E10at" ✓
    #   Check "be": len2 pos1: "b"+"10"+"e"="b10e", cap: "B10e" ✓
    #   Check "by": len2 pos1: "b"+"10"+"y"="b10y", cap: "B10y" ✓
    #   Check "sky": len3 pos1: "s"+"10"+"ky"="s10ky", cap: "S10ky" ✓
    #   Check "dog": "d"+"10"+"og"="d10og", cap: "D10og" ✓
    #   Check "world": len5 pos2: "wo"+"10"+"rld"="wo10rld", cap: "Wo10rld" ✓
    #   Check "the quick brown fox": lower, len19 pos9: "the quic"+"10"+"k brown fox"="the quic10k brown fox", cap: "The quic10k brown fox"? observed "The quick10 brown fox". ✗
    #   Hmm. "the quick brown fox" len19, pos9. chars: t-h-e-space-q-u-i-c-k = indices 0-8, so pos9 is 'k'. "the quic"+"10"+"k brown fox". Observed "The quick10 brown fox" = "the quick"+"10"+" brown fox", pos10.
    #   Wait let me recount. "the quick brown fox": t(0)h(1)e(2) (3)q(4)u(5)i(6)c(7)k(8) (9)b(10)... len=19. pos=9. Insert at 9: after "the quic" (9 chars: t,h,e,space,q,u,i,c,k). So "the quic"+"10"+"k brown fox". But observed "The quick10 brown fox" = "the quick"+"10"+" brown fox" = insert at 10.
    #   Hmm. len19//2=9, but observed insert at 10. 
    #   Wait maybe len is 19, and it's ceil? 19/2=9.5, ceil=10. Let me recheck others with ceil.
    #     cat len3 ceil=2: "ca"+"10"+"t"="ca10t"->"Ca10t"? observed "C10at". ✗
    #   So not ceil. 
    #   Let me recount "the quick brown fox". "the"=3, space=1 (4), "quick"=5 (9), space=1 (10), "brown"=5 (15), space=1 (16), "fox"=3 (19). Yes len19.
    #   Observed "The quick10 brown fox": "The quick" is 9 chars (T,h,e,space,q,u,i,c,k), then "10", then " brown fox". So insert at position 9? "The quick"+"10"+" brown fox". That's pos 9!
    #   Wait "The quick" = T-h-e-space-q-u-i-c-k = 9 chars. Yes pos9. I miscounted before. So len//2=9 ✓.
    #   Let me recheck: "the quic" is 8 chars (t,h,e,space,q,u,i,c), not 9. So pos9 gives "the quic"+"k"+"10"... no. pos9 = after 9 chars = "the quick". ✓ Good.
    #   Check "Hello, World!": H,e,l,l,o,comma,space,W,o,r,l,d,! = 13 chars. pos6: "Hello,"+"10"+" World!"="Hello,10 World!"? observed "Hello,10 world!" (lowercase w). With lowercase-first: "hello, world!" pos6: "hello,"+"10"+" world!"="hello,10 world!", cap first: "Hello,10 world!" ✓
    #   Check "one two three": len13 pos6: "one tw"+"10"+"o three"="one tw10o three", cap: "One tw10o three" ✓
    #   Check "abc def ghi": len11 pos5: "abc d"+"10"+"ef ghi"="abc d10ef ghi", cap: "Abc d10ef ghi" ✓
    #   Check "ab cd": len5 pos2: "ab"+"10"+" cd"="ab10 cd", cap: "Ab10 cd" ✓
    #   Check "a b": len3 pos1: "a"+"10"+" b"="a10 b", cap: "A10 b" ✓
    #   Check "New York": len8 pos4: "new "+"10"+"york"="new 10york", cap: "New 10york" ✓
    #   Check "A": len1 pos0: ""+"10"+"a"="10a", cap first (which is '1'): "10a" ✓
    #   Check "x": len1 pos0: "10x", cap: "10x" ✓
    #   Check "a": "10a" ✓
    #   ALL MATCH! Rule: lower(s), insert "10" at len//2, capitalize first char.
    def transform(s):
        t = s.lower()
        p = len(t) // 2
        t = t[:p] + '10' + t[p:]
        if t:
            t = t[0].upper() + t[1:]
        return t
    return {"outputs": [transform(x) for x in probe["inputs"]]}
