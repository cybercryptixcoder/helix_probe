def predict(probe):
    # Last char is incremented to the next letter [E1, E2]
    #   a->b, ..., z->a? (wrap unknown), lowercase stays lowercase
    # Uppercase last char: increment it, but wrap Z->A [E2: "WORD"->"WOE"? no]
    #   Wait: "WORD"->"WOE": W O R D -> W O E. Last 'D'->'E' (+1). Good, normal.
    #   "AB"->"AC": 'B'->'C' (+1). Good.
    #   "Z"->"A": 'Z'->'A' (wrap!). Good.
    #   "Test"->"Tesu": 't'->'u' (+1). Good.
    # So earlier "bananaUPPER"->"bananaUPPF" was just 'R'->'S'? No, output was F.
    #   Hmm, but E2 shows uppercase just +1 with Z->A wrap.
    #   Recheck "bananaUPPER": b a n a n a U P P E R -> b a n a n a U P P F.
    #   Length 11 -> 10. So 'R' dropped, 'E'->'F'. That contradicts E2's simple +1.
    #   But E2 "WORD"->"WOE" is length 4->3! W O R D -> W O E. 'D' dropped, 'R'->'E'? 
    #   R->E is not +1. Hmm. Wait W O R D -> W O E: that's 4->3.
    #   Actually maybe "WORD"->"WOE" means 'D'->'E' and 'R' dropped? No, order: W,O,R,D.
    #   Output W,O,E. So R and D -> E? Or D->E and R dropped?
    #   Hmm. Let me reconsider. Maybe the rule: last char incremented, but if it 
    #   would be... no.
    #   Let's tabulate E2 carefully:
    #   cat->cau (t->u, +1)
    #   dog->doh (g->h, +1)
    #   Test->Tesu (t->u, +1)
    #   WORD->WOE (D->E +1, but R dropped? length 4->3)
    #   abc9->abc9 (9 unchanged)
    #   x->y (+1)
    #   AB->AC (B->C +1)
    #   hi5->hi5 (5 unchanged)
    #   Z->A (wrap)
    #   a1->a1 (1 unchanged)
    # So most are simple +1. Only WORD is odd: length 4->3.
    #   W O R D -> W O E. If last 'D'->'E', we'd get W O R E. But we got W O E.
    #   So 'R' dropped too? Or 'R'->'E' and 'D' dropped?
    #   Hmm. And "bananaUPPER"->"bananaUPPF": E R -> F, R dropped, E->F.
    #   Pattern: when last char is uppercase AND second-to-last is uppercase?
    #   WORD: R,D both uppercase. bananaUPPER: E,R both uppercase.
    #   In both, the last char dropped and second-to-last incremented.
    #   Test: 's','t' lowercase, both lowercase -> normal +1 on last.
    #   AB: A,B uppercase -> but AB->AC is normal +1! Contradiction.
    #   Hmm AB->AC: B->C +1, length same. So not "both uppercase".
    #   Difference: WORD has 4 chars, AB has 2. bananaUPPER has 11.
    #   Hmm. What distinguishes WORD and bananaUPPER from AB?
    #   Maybe: if the last TWO chars are both uppercase letters AND... 
    #   AB: A,B both uppercase, but normal. 
    #   Wait maybe I misread WORD. W O R D -> W O E. Could it be 'D'->'E' and 
    #   'R' removed because... R is 18, D is 4. 
    #   Actually maybe the rule is: increment last char; if last char is uppercase 
    #   and the char before is also uppercase, drop the last char and increment 
    #   the previous? For AB: A,B -> would give A->B, drop B => "B"? But output AC.
    #   So no.
    #   Let me reconsider: maybe it's about the SECOND-to-last char being 'R'? 
    #   WORD: R. bananaUPPER: E. No.
    #   Hmm, what if the rule is: increment last char, but if the last char is 'D' 
    #   and ... no.
    #   Let me look at lengths: cat 3->3, dog 3->3, Test 4->4, WORD 4->3, abc9 4->4,
    #   x 1->1, AB 2->2, hi5 3->3, Z 1->1, a1 2->2.
    #   Only WORD shrank. bananaUPPER 11->10 shrank.
    #   What's common? WORD: W,O,R,D. bananaUPPER: ...E,R.
    #   Last char D and R. Second-to-last R and E.
    #   Hmm 'R' appears. In WORD, R is second-to-last. In bananaUPPER, R is last.
    #   Maybe rule: if 'R' is involved... no, too specific.
    #   Let me think differently. Maybe the operation is: increment the last 
    #   character, but if the last character is uppercase, increment the 
    #   second-to-last instead and drop the last? 
    #   WORD: last D uppercase -> increment R->S, drop D => W O S. But output WOE.
    #   No.
    #   Hmm. WOE. W O E. From W O R D. If we increment D->E and drop R: W O E. 
    #   So drop the SECOND-to-last, increment last? 
    #   bananaUPPER: drop R (second-to-last), increment E->F => bananaUPPF. Yes!
    #   WORD: drop R (second-to-last), increment D->E => WOE. Yes!
    #   But cat: drop 'a' (second-to-last), increment t->u => "cu"? But output "cau".
    #   So no.
    #   Hmm. So why does WORD drop R but cat doesn't drop a?
    #   Difference: R is uppercase, a is lowercase. D uppercase, t lowercase.
    #   So: if last char is uppercase AND second-to-last is uppercase, drop 
    #   second-to-last and increment last?
    #   WORD: R,D both uppercase -> drop R, D->E => WOE. Yes.
    #   bananaUPPER: E,R both uppercase -> drop E, R->S => bananaUPPS? But output 
    #   bananaUPPF. No, output is F not S. Hmm.
    #   Wait bananaUPPER -> bananaUPPF. If drop E and increment R->S: bananaUPPS. 
    #   Not F. So that's wrong.
    #   Let me recheck bananaUPPER. b a n a n a U P P E R. 
    #   Output b a n a n a U P P F. So E->F, R dropped. Drop LAST, increment 
    #   second-to-last.
    #   WORD: W O R D -> W O E. Drop D, increment R->S => WOS. Not WOE.
    #   So WORD drops second-to-last (R), increments last (D->E).
    #   bananaUPPER drops last (R), increments second-to-last (E->F).
    #   Inconsistent! Unless...
    #   Hmm wait. Maybe I should reconsider: maybe the rule is "increment the last 
    #   letter, and if there are two consecutive uppercase letters at the end, 
    #   collapse them"? 
    #   WORD: R,D -> increment D->E, and R... 
    #   Actually maybe the rule is simpler: increment last char. If last char is 
    #   uppercase and equals 'D'? No.
    #   Let me reconsider whether WORD->WOE might be a typo-like thing. But it's 
    #   ground truth.
    #   New idea: maybe the rule is: increment the last character; but if the 
    #   last character is uppercase, ALSO the character before it gets... 
    #   Hmm.
    #   Let me look at "AB"->"AC". A,B -> A,C. B->C +1, A unchanged. Normal.
    #   "WORD"->"WOE". If normal +1 on D: WORE. But we have WOE. So R removed.
    #   Why would R be removed in WORD but A kept in AB?
    #   Length: WORD 4, AB 2. Maybe if length >= 4 and last two uppercase?
    #   bananaUPPER length 11, last two E,R uppercase. But there E removed, R->? 
    #   Actually in bananaUPPER, E removed and R->F? No wait.
    #   Let me very carefully re-examine bananaUPPER -> bananaUPPF.
    #   Input:  b a n a n a U P P E R  (11)
    #   Output: b a n a n a U P P F      (10)
    #   Align:  b a n a n a U P P [E R] -> [F]
    #   So "ER" -> "F". E->F (+1), R removed.
    #   WORD: W O [R D] -> [E]? W O R D -> W O E. So "RD" -> "E". 
    #   R->? D->E? If "RD"->"E", then R removed, D->E. 
    #   Hmm so in bananaUPPER, "ER"->"F": E->F, R removed (last removed, 
    #   second-to-last incremented).
    #   In WORD, "RD"->"E": D->E, R removed (second-to-last removed, last 
    #   incremented).
    #   These are opposite! Unless...
    #   Wait, maybe in both cases it's: increment the LAST char, and remove 
    #   the SECOND-to-last, but only when... 
    #   bananaUPPER: increment R->S, remove E => bananaUPPS. Not F.
    #   No.
    #   Alternatively: increment the second-to-last, remove last:
    #   bananaUPPER: E->F, remove R => bananaUPPF. Yes!
    #   WORD: R->S, remove D => WOS. But output WOE. No.
    #   Argh.
    #   Let me reconsider WORD. Maybe it's not "RD"->"E". Maybe the whole 
    #   transformation is different. W O R D. Output W O E.
    #   What if 'R'->'E'? R is 18, E is 5. -13. And D removed.
    #   Or what if it's: last char D->E, and R->? removed.
    #   Hmm, what if the rule involves ROT? 
    #   Actually, let me step back. Maybe the rule is: increment the last 
    #   character. If the result is a letter that... no.
    #   Let me consider: maybe the box does TWO things: (1) increment last char, 
    #   (2) if the string contains "RD" or "ER"... no.
    #   Let me look at all data again:
    #   abc123 -> abc123 (last '3' digit, unchanged)
    #   level -> levem (l->m +1)
    #    Zebralower ->  Zebralowes (r->s +1)
    #   Hello World function lazy -> ...lazz (y->z +1)
    #   bananaUPPER -> bananaUPPF (ER->F)
    #   Zebra -> Zebrb (a->b +1)
    #   cat->cau, dog->doh, Test->Tesu, WORD->WOE, abc9->abc9, x->y, AB->AC, 
    #   hi5->hi5, Z->A, a1->a1
    #   So the ONLY anomalies are bananaUPPER and WORD. Both end in two 
    #   uppercase letters where... 
    #   bananaUPPER ends "ER", WORD ends "RD".
    #   Hmm, "ER" and "RD". What if the rule is: if the last two chars are 
    #   uppercase, replace them with the next letter after the FIRST of them? 
    #   "ER": next after E is F => "F". Yes!
    #   "RD": next after R is S => "S". But output is "E". No.
    #   Hmm. "RD" -> "E". Next after D is E. So it's next after the SECOND 
    #   (last) char, dropping the first. "ER" -> next after R is S, but output F.
    #   Inconsistent again.
    #   Wait, maybe I have WORD wrong. Let me re-read: "WORD"->"WOE". 
    #   Could it be that the output is "WOE" meaning W,O,E and the input WORD 
    #   W,O,R,D. If we drop R and D->E: WOE. If we drop D and R->S: WOS.
    #   Output WOE, so drop R, D->E.
    #   For bananaUPPER: drop R, E->F => bananaUPPF. So drop LAST (R), E->F.
    #   In WORD, drop SECOND-to-last (R), D->E.
    #   In bananaUPPER, drop LAST (R), E->F.
    #   Both drop an R! And increment the other one.
    #   WORD: R dropped, D->E. bananaUPPER: R dropped, E->F.
    #   So maybe the rule is: if there's an 'R' near the end... no, too specific.
    #   Hmm, but actually maybe the rule is: the LAST character is incremented, 
    #   and if the SECOND-to-last is 'R', it's dropped? 
    #   WORD: second-to-last R, drop it, D->E => WOE. Yes!
    #   bananaUPPER: second-to-last E, not R. Last R. Hmm.
    #   For bananaUPPER, last is R, second-to-last E. If we increment last R->S 
    #   and drop second-to-last E: bananaUPPS. Not F.
    #   So no.
    #   OK here's another thought: maybe the rule is about the last character 
    #   being 'R' or 'D'? No.
    #   Let me try: maybe the operation is "increment the last character, but 
    #   if the last character is uppercase and the string has more than 3 
    #   characters, drop the second-to-last"? 
    #   WORD (4 chars): last D uppercase, >3 -> drop R, D->E => WOE. Yes!
    #   bananaUPPER (11): last R uppercase, >3 -> drop E, R->S => bananaUPPS. 
    #   But output bananaUPPF. No.
    #   Hmm.
    #   Wait, maybe for bananaUPPER the output really is bananaUPPS and I 
    #   misread? The evidence says "bananaUPPF". Let me trust it.
    #   OK let me try yet another angle. What if the rule is: increment the 
    #   last character; if the last character is uppercase, increment it and 
    #   ALSO the character before it gets removed if it's uppercase? 
    #   WORD: D uppercase, R uppercase before -> remove R, D->E => WOE. Yes!
    #   bananaUPPER: R uppercase, E uppercase before -> remove E, R->S => 
    #   bananaUPPS. But output bananaUPPF. No.
    #   Argh, bananaUPPER is the problem.
    #   Let me reconsider bananaUPPER once more. Maybe the output is 
    #   "bananaUPPF" where F is... E->F. So E incremented, R removed.
    #   What if the rule is: increment the last character, but if the last 
    #   character is 'R', remove it and increment the previous? 
    #   bananaUPPER: last R -> remove, E->F => bananaUPPF. Yes!
    #   WORD: last D, not R. So normal: D->E => WORE. But output WOE. No.
    #   Hmm.
    #   What if the rule is: increment the last character; if the last character 
    #   is 'R' OR the second-to-last is 'R'... 
    #   WORD: second-to-last R -> remove it, D->E => WOE. Yes!
    #   bananaUPPER: last R -> remove it, E->F => bananaUPPF. Yes!
    #   So: if 'R' is the last or second-to-last character, remove that R and 
    #   increment the other of the last two? 
    #   WORD: R is second-to-last, remove it, increment last D->E. WOE. Yes.
    #   bananaUPPER: R is last, remove it, increment second-to-last E->F. 
    #   bananaUPPF. Yes!
    #   But this is weirdly specific to 'R'. Unlikely the real rule.
    #   Hmm, but maybe it's not 'R' specifically. Maybe it's: if the last two 
    #   characters are both uppercase, remove one and increment the other, 
    #   choosing... which one? 
    #   WORD: R,D -> remove R, increment D. (remove first, increment second)
    #   bananaUPPER: E,R -> remove R, increment E. (remove second, increment first)
    #   In WORD, D is the last, R is second-to-last. Remove R (second-to-last), 
    #   increment D (last).
    #   In bananaUPPER, E is second-to-last, R is last. Remove R (last), 
    #   increment E (second-to-last).
    #   So in both cases, remove the one that is... R? Or remove the one that 
    #   comes LATER in alphabet? R(18) vs D(4): remove R (larger). 
    #   E(5) vs R(18): remove R (larger). Yes! Remove the larger, increment 
    #   the smaller!
    #   WORD: R>D, remove R, increment D->E => WOE. Yes!
    #   bananaUPPER: R>E, remove R, increment E->F => bananaUPPF. Yes!
    #   Interesting. But is that the real rule? Seems arbitrary.
    #   Alternatively: remove the one that is 'R'? Both have R. Coincidence?
    #   Hmm. Let me think about what's natural. 
    #   Actually, maybe the rule is simpler and I'm overcomplicating. Let me 
    #   reconsider: maybe the box increments the last character, and if the 
    #   last character is uppercase, it also does something with the previous.
    #   Actually, you know what, let me reconsider the possibility that the 
    #   rule is: "increment the last character; if the last character is 
    #   uppercase, increment the second-to-last instead and drop the last" 
    #   — but this failed for WORD (gave WOS not WOE).
    #   Wait, let me recompute. WORD: last D uppercase -> increment R->S, 
    #   drop D => WOS. Output WOE. So no.
    #   What about "increment the last character; if the last character is 
    #   uppercase, drop the second-to-last and increment the last":
    #   WORD: drop R, D->E => WOE. Yes!
    #   bananaUPPER: drop E, R->S => bananaUPPS. Output bananaUPPF. No.
    #   So these two cases genuinely differ in which of the last two is 
    #   incremented vs dropped. 
    #   Given the "remove larger, increment smaller" hypothesis fits both, 
    #   and it's a clean rule, I'll go with that. But it's a guess.
    #   Actually wait. Let me reconsider. Maybe it's not about uppercase at all.
    #   Maybe the rule is: increment the last character. If the last character 
    #   is a letter and the second-to-last is ALSO a letter, and they form a 
    #   specific pattern... 
    #   Hmm, but cat (a,t both letters) -> cau, normal. So not just "both letters".
    #   The distinguishing feature of WORD and bananaUPPER: last two are both 
    #   UPPERCASE. cat: a,t lowercase. Test: s,t lowercase. AB: A,B uppercase!
    #   AB->AC normal. So AB contradicts "both uppercase -> special".
    #   Unless AB is too short (2 chars). Maybe rule needs length >= 3 or 4?
    #   AB length 2. WORD length 4. bananaUPPER length 11.
    #   Maybe: if last two chars are uppercase AND length >= 3, do the 
    #   remove-larger-increment-smaller? 
    #   Let me check: are there other cases with last two uppercase and length>=3?
    #   None in data except WORD and bananaUPPER. So can't distinguish.
    #   I'll hypothesize: if the last two characters are both uppercase letters 
    #   and the string length >= 3, then remove the alphabetically larger of 
    #   the two and increment the smaller (with Z->A wrap). Otherwise, increment 
    #   the last character (letters +1 with Z->A, z->a; digits unchanged).
    #   Hmm, but "remove larger" is weird. Let me reconsider once more.
    #   Actually, maybe the rule is: increment the last character; if the last 
    #   character is uppercase, increment it but wrap within uppercase; and 
    #   separately, if there are two consecutive uppercase letters at the end, 
    #   the FIRST of them is removed if it's 'R'? No.
    #   I'll go with a cleaner guess: maybe the rule is that the last character 
    #   is incremented, but if the last character is uppercase, the 
    #   second-to-last character is removed IF it is also uppercase AND 
    #   alphabetically greater than the last? 
    #   WORD: R > D, remove R, D->E => WOE. Yes.
    #   bananaUPPER: E < R, so don't remove E? Then R->S => bananaUPPS. No.
    #   Doesn't work.
    #   OK, "remove larger, increment smaller" it is. Let me just also handle 
    #   the possibility that it's specifically about 'R'. But "remove larger" 
    #   is more general and fits. I'll mark with "?".
    #   Actually, let me reconsider one more time whether there's a simpler 
    #   explanation. What if the box does: increment last char; then if the 
    #   result contains two consecutive uppercase letters that are... no.
    #   What if it's: the last character is incremented, and any character 
    #   that equals 'R' is... no, Zebra has no R issue? Zebra -> Zebrb, 
    #   'a'->'b', R stays. So R is fine mid-string.
    #   OK. Let me also reconsider: maybe the rule is "increment the last 
    #   character; if the last character is uppercase, increment the 
    #   second-to-last and drop the last" — but for WORD this gives WOS. 
    #   Unless... wait, is it possible the output for WORD is actually "WOS" 
    #   and I misread as "WOE"? The evidence clearly says "WOE". I'll trust it.
    #   Given uncertainty, I'll implement: 
    #   - If len>=3 and last two are uppercase letters: remove the larger, 
    #     increment the smaller (Z->A wrap). "?"
    #   - Else: increment last char: lowercase a-z +1 (z->a), uppercase A-Z +1 
    #     (Z->A), digits unchanged, other chars unchanged. [E1,E2]
    def inc(c):
        if 'a' <= c <= 'z':
            return 'a' if c == 'z' else chr(ord(c)+1)
        if 'A' <= c <= 'Z':
            return 'A' if c == 'Z' else chr(ord(c)+1)
        return c
    def transform(s):
        if not s:
            return s
        if len(s) >= 3 and s[-1].isupper() and s[-2].isupper() \
           and s[-1].isalpha() and s[-2].isalpha():
            a, b = s[-2], s[-1]
            if a > b:
                # remove a, increment b
                return s[:-2] + inc(b)
            else:
                # remove b, increment a
                return s[:-2] + inc(a)
        return s[:-1] + inc(s[-1])
    return {"outputs": [transform(x) for x in probe["inputs"]]}
