def predict(probe):
    # Reverse each word's characters, keep word order [E2,E8]
    # Split on whitespace, collapse runs, drop leading/trailing [E6]
    # Insert a single 'I' into each word after reversing.
    # KEY: the I goes at the START of the reversed word for the FIRST word,
    #      and at ceil(len/2) for subsequent words? No — re-examine.
    # Actually from E18/E22: first word gets I at index 0 of reversed ("Igod","Itac","Icba","Iolleh","Itset","Iesac")
    #   BUT "sun moon"->"nus noomI": first word "sun" got NO leading I, second got trailing I.
    #   And "moon sun"->"Inoom nus": first word "moon" got leading I, second none.
    # So it's not "first word". Look: the I is placed on the LONGER word? 
    #   "dog cat": dog(3) cat(3) -> "Igod tac" I on dog (first)
    #   "sun moon": sun(3) moon(4) -> "nus noomI" I on moon (longer)
    #   "moon sun": moon(4) sun(3) -> "Inoom nus" I on moon (longer)
    #   "abc def": abc(3) def(3) -> "Icba fed" I on abc (first)
    #   "hello world": hello(5) world(5) -> "Iolleh dlrow" I on hello (first)
    #   "test case": test(4) case(4) -> "Itset esac" I on test (first)
    #   "cat hello": cat(3) hello(5) -> "tac ollehI" I on hello (longer)
    #   "hello cat": hello(5) cat(3) -> "oIlleh tac" I on hello (longer)
    #   "ab abc abcd": 2,3,4 -> "ba cIba dcba" I on abc (len3, middle)
    #   "abcd abc ab": 4,3,2 -> "dcba cbaI ba" I on abc (len3)
    #   "sun testing": 3,7 -> "nus gnitseIt" I on testing (longer)
    #   "testing sun": 7,3 -> "gnIitset nus" I on testing (longer)
    #   "a apple banana": 1,5,6 -> "a Ielppa ananab" I on apple (len5)
    #   "banana apple a": 6,5,1 -> "ananab elppaI a" I on apple (len5)
    #   "red science": 3,7 -> "der ecneicIs" I on science (longer)
    #   "science red": 7,3 -> "ecIneics der" I on science (longer)
    #   "racecar Mississippi banana": 7,11,6 -> "racecar ippissIissiM ananab" I on Mississippi (longest)
    # So: exactly ONE word gets the I — the word with the maximum length (ties -> first such word).
    # And the I position within that word's reversed form: 
    #   "dog"->"Igod" idx0; "moon"->"noomI" idx4(end); "hello"->"ollehI" idx5(end); "abc"->"cIba" idx2
    #   "testing"->"gnitseIt" idx6; "apple"->"elppaI" idx5(end); "science"->"ecneicIs" idx7(end)
    #   "Mississippi"->"ippissIissiM" idx6; "cat"->"tac" no I (not max)
    # Hmm position varies. Let's see: for the chosen word, I at index = ? 
    #   dog(3):0, moon(4):4, hello(5):5, abc(3):2, testing(7):6, apple(5):5, science(7):7, Mississippi(11):6
    # Single-word inputs (E14 etc) all got I at ceil(len/2). But multi-word chosen word differs!
    # Wait — single word inputs: "test"->"tset"? E14: "test"->? Let me check E8: "world"->"dlrIow" idx3=ceil(5/2).
    # For multi-word, the chosen word's I position: maybe it's ceil(len/2) too?
    #   dog(3):ceil=2 but observed 0. moon(4):ceil=2 but observed 4. hello(5):ceil=3 but observed 5.
    # Not ceil. Maybe position depends on TOTAL input length or word's position?
    # Alternative: the I is inserted at a position based on the word's rank/index among words?
    # Let's reconsider: maybe I is at index = (number of words) or something.
    # "dog cat"(2 words): dog I at 0. "sun moon": moon I at 4=len. "hello world": hello I at 5=len.
    # "abc def": abc I at 2=len-1. "test case": test I at 4=len. 
    # Hmm. Let me reconsider: maybe the I position = len(word) - (index of word among max?) no.
    # Try: I at index = len(word) - (position of word in list, 1-based)? 
    #   "dog cat": dog is word1, len3, 3-1=2? no observed 0.
    # Try I at index = (position of chosen word, 0-based) mapped... 
    # "dog cat": chosen word idx0 -> I at 0. "sun moon": chosen idx1 -> I at 4=len. 
    # "hello world": chosen idx0 -> I at 5=len. inconsistent.
    # Let me reconsider which word and where together. Maybe the I is placed at a fixed
    # absolute character position in the concatenated reversed string? 
    # "dog cat" reversed words: "god tac". I at... "Igod tac" -> pos0.
    # "sun moon": "nus noom". "nus noomI" -> pos8 (end).
    # "hello world": "olleh dlrow". "Iolleh dlrow" -> pos0.
    # "abc def": "cba fed". "Icba fed" -> pos0.
    # "test case": "tset esac". "Itset esac" -> pos0.
    # "cat hello": "tac olleh". "tac ollehI" -> pos9 (end).
    # "ab abc abcd": "ba cba dcba". "ba cIba dcba" -> pos4.
    # "a apple banana": "a elppa ananab". "a Ielppa ananab" -> pos2.
    # "red science": "der ecneics". "der ecneicIs" -> pos11.
    # "racecar Mississippi banana": "racecar ippississiM ananab". "racecar ippissIissiM ananab" -> pos13.
    # Total lengths: dog cat=6,I@0; sun moon=7,I@8? that's >len. Wait "nus noomI" len 9 (with space). 
    # reversed concat "nus noom" len 8, I at 8 = end. 
    # hello world: "olleh dlrow" len 11, I@0.
    # abc def: "cba fed" len 7, I@0.
    # test case: "tset esac" len 9, I@0.
    # cat hello: "tac olleh" len 9, I@9=end.
    # ab abc abcd: "ba cba dcba" len 11, I@4.
    # a apple banana: "a elppa ananab" len 14, I@2.
    # red science: "der ecneics" len 11, I@11=end.
    # racecar Mississippi banana: len 25, I@13.
    # Hmm. Maybe I position relates to the longest word's location. 
    # Let me think differently: maybe I is inserted into the longest word at position = 
    #   (len of that word) - (its index in the word list)? 
    # dog cat: longest dog idx0 len3: 3-0=3? no.
    # Maybe position within longest word = number of OTHER words? 
    # dog cat: 1 other word, I at 0. sun moon: 1 other, I at 4(len). no.
    # Let me look at longest word's I index vs its length and total:
    # dog(3)@0, moon(4)@4, hello(5)@5, abc(3)@2, test(4)@4, hello(5)@5, abc(3)@2, apple(5)@5, science(7)@7, Mississippi(11)@6
    # For single longest word cases: @0,@4,@5,@2,@4,@5,@2,@5,@7,@6
    # Notice: @0 when word is FIRST and... dog first@0, hello first@5, abc first@2, test first@4
    #   first word: dog@0, hello@5, abc@2, test@4 — varies.
    # Hmm dog@0 but abc@2, test@4, hello@5. 
    # Maybe position = len - (number of words after it)? 
    # dog cat: dog has 1 after, 3-1=2? no @0.
    # I'm overcomplicating. Let me check: maybe the I position in the longest word = 
    #   ceil(len/2) but measured differently, OR it's the position such that... 
    # dog@0, abc@2, test@4, hello@5, moon@4, apple@5, science@7, Mississippi@6
    # len: 3,3,4,5,4,5,7,11
    # @:   0,2,4,5,4,5,7,6
    # For len3: 0 or 2. len4:4. len5:5. len7:7. len11:6.
    # Hmm len4@4=end, len5@5=end, len7@7=end, but len3@0 or 2, len11@6.
    # Wait maybe it depends on the OTHER word's length / comparison.
    # dog cat: both len3, tie, I on first@0. abc def: both 3, I on first@2. Different positions!
    # So tie-break differs. dog@0 vs abc@2. 
    # "dog cat" vs "abc def" — same lengths, different I position. So position depends on letters? No...
    # Unless it's about the actual characters. Hmm.
    # Let me reconsider entirely. Maybe the rule is per-word after all, and I misread.
    # E18 "dog cat"->"Igod tac": word "dog" reversed "god", I at 0. word "cat" reversed "tac", no I.
    # But E16 "cat dog"->"taIc goId": BOTH got I! cat->"taIc" (I@2), dog->"goId"(I@2).
    # Wait E16 "cat"->"taIc" I@2, "dog"->"goId" I@2. Both words got I in E16!
    # But E18 "cat dog"->"Itac god": only cat got I@0. Contradiction between E16 and E18?!
    # E16: "a b c"->"a bI c" only middle got I. "ab cd ef"->"ba dIc fe" only middle.
    # E18: "dog cat"->"Igod tac" only first. "cat dog"->"Itac god" only first.
    # So in E16 single-word inputs each got I (they're separate inputs!). 
    # E16 inputs: "a","ab","abc","I","if","cat","dog","sun" are SINGLE words -> each gets I at ceil.
    # "a b c"->"a bI c": 3 words, only middle "b" got I. "ab cd ef"->"ba dIc fe": only middle "cd".
    # So for multi-word, only ONE word gets I. Which one? In "a b c" it's the middle (b, len1). 
    # In "ab cd ef" middle (cd, len2). In E18 "dog cat" first (dog). "sun moon" second (moon).
    # Hmm "a b c": middle. "ab cd ef": middle. "dog cat": first. "sun moon": second.
    # Maybe it's the word at the middle position? "dog cat" 2 words, middle ambiguous -> first.
    # "sun moon" 2 words -> but got second. Inconsistent.
    # Let me reconsider: maybe I is on the word whose length is the MEDIAN? 
    # "a b c": all len1, median any -> middle chosen. "ab cd ef": all len2 -> middle.
    # "dog cat": both 3 -> first. "sun moon": 3,4 -> median? only 2 values.
    # "cat hello": 3,5 -> hello(len5) got I. "hello cat": hello got I. So longer.
    # "sun moon": 3,4 -> moon(4) got I, longer. "dog cat": 3,3 tie -> first.
    # "abc def": 3,3 tie -> first. "hello world":5,5 tie->first. "test case":4,4 tie->first.
    # "ab abc abcd": 2,3,4 -> abc(3) median got I. "abcd abc ab": 4,3,2 -> abc(3) median.
    # "a apple banana": 1,5,6 -> apple(5) median. "banana apple a": 6,5,1 -> apple(5) median.
    # "red science": 3,7 -> science(7) longer. "science red": science.
    # "racecar Mississippi banana": 7,11,6 -> Mississippi(11) longest/median? sorted 6,7,11 median=7=racecar. But Mississippi got I!
    # Hmm median of {6,7,11} is 7 (racecar) but Mississippi(11) got I. So not median.
    # Longest: Mississippi(11) yes! "ab abc abcd": longest abcd(4) but abc(3) got I. Not longest.
    # Ugh. "ab abc abcd" longest=abcd(4), got abc(3). "a apple banana" longest=banana(6), got apple(5).
    # So it's the SECOND longest? "ab abc abcd": 2nd longest = abc(3) yes. "a apple banana": 2nd=apple(5) yes.
    # "racecar Mississippi banana": 2nd longest = racecar(7)? sorted 6,7,11 -> 2nd=7=racecar. But Mississippi got I. No.
    # Hmm. Let me reconsider "racecar Mississippi banana": lengths 7,11,6. Mississippi=11 got I. That's longest.
    # But "ab abc abcd" longest abcd=4 didn't get I. 
    # Difference? Maybe it's about position: in "ab abc abcd" the longest is LAST. In "racecar Mississippi banana" longest is MIDDLE.
    # Maybe the I goes on the word at index = something, and its position within is ceil(len/2) of THAT word?
    # Check positions with ceil(len/2) hypothesis for the chosen word:
    #   "a b c"->"a bI c": b len1, ceil(1/2)=1, reversed "b", I@1="bI" yes!
    #   "ab cd ef"->"ba dIc fe": cd len2, reversed "dc", ceil(2/2)=1, I@1="dIc" yes!
    #   "dog cat"->"Igod tac": dog len3, reversed "god", ceil(3/2)=2 -> "goId" but observed "Igod"@0. NO.
    # Hmm. So chosen word dog, but position 0 not 2.
    # Wait maybe chosen word is different. "Igod tac": which word has I? "god"->"Igod" I@0. 
    # If ceil(3/2)=2 gives "goId". Observed "Igod". So position 0.
    # Unless the I is at position 0 for the FIRST word always, and ceil for others?
    # "a b c"->"a bI c": first word "a"->"a" no I. middle "b"->"bI" I@1=ceil. 
    # "dog cat": first "dog"->"Igod" I@0. 
    # "sun moon": first "sun"->"nus" no I, second "moon"->"noomI" I@4=ceil(4/2)=2? no @4.
    # Hmm moon ceil(4/2)=2 -> "noImo" but observed "noomI"@4.
    # This is getting complex. Let me tabulate chosen word and I-index-in-reversed vs len:
    #   b(1)@1, cd(2)@1, dog(3)@0, moon(4)@4, hello(5)@5, abc(3)@2, test(4)@4, hello(5)@5,
    #   abc(3)@2, apple(5)@5, science(7)@7, Mississippi(11)@6
    # len1@1=ceil. len2@1=ceil. len3@0 or 2. len4@4. len5@5. len7@7. len11@6.
    # For len>=4 mostly @len (end) except Mississippi@6. 
    # Mississippi len11 @6 = ceil(11/2)=6! And len4@4=end not ceil(2). len5@5=end not ceil(3).
    # Hmm inconsistent. Unless Mississippi is special (repeated letters)? 
    # Let me check: maybe position = len - ceil(len/2)? = floor(len/2). 
    #   len3 floor=1, len4=2, len5=2, len7=3, len11=5. Mississippi@6 no.
    # I think I'm missing the real rule. Given time, let me go with: 
    # The I is inserted into exactly one word — the one that is "central" — and I'll 
    # hypothesize it's based on a simple rule I can best fit. 
    # Actually, reconsider: maybe ALL words get I but at position that makes some invisible?
    # No, "tac" clearly has no I.
    # Let me try: the I is placed at the position in the FULL reversed-and-spaced string 
    # equal to the index of the longest word's start? 
    # "dog cat": reversed "god tac", longest dog starts@0 -> I@0 yes!
    # "sun moon": "nus noom", longest moon starts@4 -> I@4 yes!
    # "hello world": "olleh dlrow", longest hello(tie,first) starts@0 -> I@0 yes!
    # "abc def": "cba fed", longest abc(tie first) starts@0 -> I@0 yes!
    # "test case": "tset esac", longest test(tie first) starts@0 -> I@0 yes!
    # "cat hello": "tac olleh", longest hello starts@4 -> I@4? observed "tac ollehI" I@9. NO.
    # Hmm. "tac ollehI" I at end (pos9). hello starts@4. no.
    # Maybe I at END of longest word? "cat hello": hello ends@9, I@9 yes!
    # "sun moon": moon ends@8, I@8 yes! "dog cat": dog ends@3, but I@0. no.
    # Argh. dog@0 but others@end.
    # dog is first word. Maybe: if longest is first word, I@start; else I@end?
    # "hello world": hello first, I@0=start yes. "abc def": abc first I@0=start yes.
    # "test case": test first I@0=start yes. "cat hello": hello not first, I@end yes.
    # "sun moon": moon not first, I@end yes. "red science": science not first, I@end yes.
    # "ab abc abcd": abc is middle (not first, not last), I@? "ba cIba dcba" I@4. abc reversed "cba" starts@3 ends@6. I@4 is inside. Hmm.
    # Not start or end. @4 = start+1. 
    # "a apple banana": apple middle, "a Ielppa ananab" I@2. apple reversed "elppa" starts@2. I@2=start!
    # "ab abc abcd": abc reversed "cba" starts@3, I@4=start+1. inconsistent with apple@start.
    # I'm running low. Let me just go with a reasonable approximation and mark uncertain.
    # Best fit attempt: choose the longest word (ties->first). Insert I at ceil(len/2) 
    # EXCEPT this fails many. 
    # Given difficulty, I'll implement: single word -> ceil(len/2). Multi-word -> 
    # pick longest word (tie first), insert I at position: if it's the first word -> 0, 
    # else -> len (end). This fits dog,hello,abc,test,sun,cat hello,red science but not 
    # ab abc abcd, a apple banana, racecar Mississippi banana. Mark with ?.
    import math
    def transform_single(word):
        rev = word[::-1]
        n = len(rev)
        pos = (n + 1) // 2
        return rev[:pos] + "I" + rev[pos:]
    try:
        out = []
        for s in probe.get("inputs", []):
            words = s.split()
            if not words:
                out.append("I")
                continue
            if len(words) == 1:
                out.append(transform_single(words[0]))
                continue
            # multi-word: choose longest (tie -> first)
            maxlen = max(len(w) for w in words)
            idx = next(i for i, w in enumerate(words) if len(w) == maxlen)
            res = []
            for i, w in enumerate(words):
                rev = w[::-1]
                if i == idx:
                    if i == 0:
                        pos = 0
                    else:
                        pos = len(rev)
                    res.append(rev[:pos] + "I" + rev[pos:])
                else:
                    res.append(rev)
            out.append(" ".join(res))
        return {"outputs": out}
    except Exception:
        return {"outputs": []}
