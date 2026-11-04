def predict(probe):
    try:
        out = []
        for s in probe.get("inputs", []):
            words = s.split()
            if not words:
                out.append("")
                continue
            # E3 evidence: "abc def ghi" -> "cba ihgfed"
            # "cba" = reversed("abc"), "ihgfed" = reversed("defghi")
            # So first word reversed, rest concatenated then reversed?
            # Check "hello, world!" -> ",oleh !drw"
            # reversed("hello,")=",olleh" but observed ",oleh" -> reversed("hello")="olleh", then ","? no
            # ",oleh" = "," + "oleh" = "," + reversed("helo")? hmm
            # "!drw" = "!" + "wrd"? reversed("world!")="!dlrow", not match
            # Try: reverse each word but keep punctuation in place? 
            # "hello," -> "olleh," no. Observed ",oleh".
            # Maybe reverse whole string then... "hello, world!" reversed = "!dlrow ,olleh"
            # observed ",oleh !drw" 
            # Hmm: split into words: "hello," and "world!"
            # ",oleh" : reverse "hello," -> ",olleh"; observed ",oleh" differs (l and e swapped)
            # "!drw": reverse "world!" -> "!dlrow"; observed "!drw" 
            # Looks like: reverse the letters only (not punctuation), keep punctuation at same relative position?
            # "hello," letters h e l l o -> o l l e h, punctuation ',' at end -> "olleh,"? no
            # observed ",oleh": comma first, then o l e h. That's reverse of "helo"? 
            # Actually "hello," -> strip punct -> "hello" reversed "olleh", punct ',' moved to front -> ",olleh"? no
            # Let me reconsider: maybe reverse whole string per word including punct, then... 
            # "hello," reversed = ",olleh". observed ",oleh". Not equal.
            # Difference: "olleh" vs "oleh" - one l missing? "hello" has 5 chars, "oleh" has 4.
            # Hmm maybe it's reversing pairs or something.
            # Let's check "abc def ghi" -> "cba ihgfed"
            # "abc"->"cba" (reversed). "def ghi" -> "ihgfed" = reversed("defghi")? "defghi" reversed = "ihgfed" yes!
            # So: first word reversed, remaining words concatenated and reversed.
            # "hello, world!" -> first word "hello," reversed = ",olleh"? but observed ",oleh"
            # Hmm not matching. Unless "hello," -> reverse = ",olleh" and observed ",oleh" is typo? 
            # Let's check "a,b c" -> "b,a c": first word "a,b" reversed = "b,a" ✓, second "c" reversed = "c" ✓
            # "a b,c" -> "a c,b": first "a"->"a" ✓, "b,c"->"c,b" ✓
            # "x-y z" -> "y-x z": "x-y"->"y-x" ✓, "z"->"z" ✓
            # "1 2 3" -> "1 32": "1"->"1", "2 3" concat "23" reversed "32" ✓
            # "A B C" -> "A CB": "A"->"A", "B C" concat "BC" reversed "CB" ✓
            # "a  b  c" -> "a cb": "a"->"a", "b c" concat "bc" reversed "cb" ✓
            # "  a  b  " -> "ba": words ["a","b"], "a"->"a", "b"->"b"? but observed "ba"
            # Hmm "  a  b  " -> "ba". If first word "a" reversed "a", rest "b" reversed "b" -> "a b". Not "ba".
            # Wait maybe rule: reverse first word, then reverse the rest as one block, but join without space?
            # "abc def ghi": "abc"->"cba", "def ghi"->"ihgfed", joined "cba ihgfed" with space ✓
            # "  a  b  ": "a"->"a", "b"->"b", joined "a b". Observed "ba". ✗
            # Hmm. Let me recheck E2: "ab cd ef" -> "ba fedc". 
            # "ab"->"ba", "cd ef" concat "cdef" reversed "fedc" -> "ba fedc" ✓
            # "one two three four" -> "eno ufrhwt"
            # "one"->"eno", "two three four" concat "twothreefour" reversed "ruofeerhtowt"? 
            # "twothreefour" reversed = "ruofeerhtowt". Observed "ufrhwt". Not matching.
            # Hmm. "ufrhwt" - that's 6 chars. "two three four" has 12 letters.
            # Maybe it's not concatenation. Let me think differently.
            # "one two three four" -> "eno ufrhwt"
            # "eno" = reversed("one"). "ufrhwt" = ? reversed("twothreefour")= "ruofeerhtowt" no.
            # Maybe reverse each word but only keep... no.
            # "ufrhwt": could be reversed("tw hruf")? 
            # Actually maybe it reverses the whole string then does something.
            # "one two three four" reversed = "ruof eerht owt eno"
            # observed "eno ufrhwt"
            # Hmm "eno" matches first word reversed. "ufrhwt"?
            # Let's count: "two three four" -> "ufrhwt" (6 chars from 12). 
            # Maybe it takes every other char? "two three four" = t w o t h r e e f o u r
            # odd positions: t o h e f u = "tohefu", even: w t r e o r = "wt reor"
            # reversed of "tohefu" = "ufeh ot"? no
            # Hmm. Let me look at E1: "hi there" -> "ih ret"
            # "hi"->"ih" ✓, "there"->"ret"? reversed("there")="ereht". "ret" is 3 chars.
            # "there" = t h e r e. "ret" = r e t. That's reversed("ter")? 
            # Or maybe it's reverse then take... hmm.
            # "two words" -> "owt sdr": "two"->"owt" ✓, "words"->"sdr"? reversed("words")="sdrow". "sdr" 3 chars.
            # "HELLO WORLD" -> "OLEH DRW": "HELLO"->"OLEH" ✓, "WORLD"->"DRW"? reversed="DLROW", "DRW" 3 chars.
            # Pattern: first word fully reversed, subsequent words truncated to 3 chars then reversed?
            # "there"->"ret": take first 3 "the" reversed "eht"? no. take last 3 "ere" reversed "ere"? no.
            # "words"->"sdr": reversed("rds")="sdr". "rds" = last 3 of "words"? "rds" yes! last 3 of "words" = "rds", reversed = "sdr" ✓
            # "WORLD"->"DRW": last 3 "RLD" reversed "DLR"? no. Hmm "DRW" reversed = "WRD". 
            # "WORLD" last 3 = "RLD", reversed "DLR". Not "DRW".
            # Hmm. "WORLD" -> "DRW". Maybe first 3 "WOR" reversed "ROW"? no.
            # Let me reconsider. Maybe it's not truncation.
            # "hello, world!" -> ",oleh !drw"
            # "hello," -> ",oleh". "world!" -> "!drw"
            # "world!" reversed = "!dlrow". "!drw" is 4 chars.
            # "hello," reversed = ",olleh". ",oleh" is 5 chars.
            # Hmm ",oleh" vs ",olleh": missing one 'l'. 
            # Maybe it removes duplicate consecutive letters? "hello" -> "helo" -> reversed "oleh", with comma -> ",oleh" ✓!
            # "world!" -> "world!" no dupes. reversed "!dlrow". But observed "!drw". 
            # Hmm "!drw" - maybe remove 'l','o'? 
            # Wait maybe it's reversing and removing vowels? "world" -> remove vowels "wrld" reversed "dlrw"? no.
            # Let me try: maybe the rule is reverse each word, then remove... 
            # "two words" -> "owt sdr". "words" reversed "sdrow". "sdr" = remove 'o','w'? 
            # Hmm. "sdrow" -> "sdr" removes 'o' and 'w'. 
            # "there" reversed "ereht" -> "ret" removes 'e','h'? 
            # "WORLD" reversed "DLROW" -> "DRW" removes 'L','O'? 
            # "world!" reversed "!dlrow" -> "!drw" removes 'l','o'? 
            # Interesting: it seems to remove some letters. Which ones?
            # "sdrow" remove o,w -> sdr. "ereht" remove e,h -> ret. "DLROW" remove L,O -> DRW. "!dlrow" remove l,o -> !drw.
            # Removed: o,w / e,h / L,O / l,o. Hmm not consistent.
            # Wait "ereht" remove e,h gives "ret"? e r e h t, remove e,h -> r e t = "ret" ✓
            # "sdrow" remove o,w -> s d r = "sdr" ✓
            # "DLROW" remove L,O -> D R W = "DRW" ✓
            # "!dlrow" remove l,o -> ! d r w = "!drw" ✓
            # What's removed? In "sdrow": o and w. In "ereht": e and h. In "DLROW": L and O. In "!dlrow": l and o.
            # Hmm, maybe it's removing the 2nd and 4th characters? "sdrow": s(1)d(2)r(3)o(4)w(5). Remove 4,5? no.
            # "ereht": e(1)r(2)e(3)h(4)t(5). Remove 3,4? gives "ert". no.
            # Let me think: maybe it's not removing, maybe it's a different operation.
            # Actually maybe the box reverses the whole string, then splits differently.
            # Let me step back. This is getting complex. Let me just try a simpler hypothesis.
            # E3: "abc def ghi" -> "cba ihgfed". 
            # If rule = reverse first word, then reverse rest-of-string-as-block:
            # rest = "def ghi" -> "ihg fed"? no, observed "ihgfed" (no space).
            # Hmm but "abc def ghi" has spaces. Output "cba ihgfed" has one space.
            # So maybe: reverse first word, then concatenate remaining words (removing spaces) and reverse.
            # "def ghi" concat "defghi" reversed "ihgfed" ✓
            # "two three four" concat "twothreefour" reversed "ruofeerhtowt". Observed "ufrhwt". ✗
            # So that doesn't work for E2.
            # Unless E2 was with model v1 which was wrong. Let me trust E3 more.
            # E3 "1 2 3" -> "1 32": "1"->"1", "2 3" concat "23" reversed "32" ✓
            # E3 "A B C" -> "A CB": "A"->"A", "B C" concat "BC" reversed "CB" ✓
            # E3 "a  b  c" -> "a cb": "a"->"a", "b c" concat "bc" reversed "cb" ✓
            # E3 "  a  b  " -> "ba": words ["a","b"]. "a"->"a", "b"->"b", concat "ab" reversed "ba"? 
            # Wait if first word reversed "a", rest "b" concat "b" reversed "b", joined "a b". But observed "ba".
            # Hmm. Unless when there's leading whitespace, the "first word" is empty?
            # "  a  b  " split -> ["a","b"]. Hmm.
            # Or maybe the rule is: reverse the entire string (all chars), then... 
            # "  a  b  " reversed = "  b  a  ", strip = "b  a", collapse = "b a". Not "ba".
            # Hmm.
            # Let me look at "hello, world!" -> ",oleh !drw" again.
            # If rule = reverse first word, concat rest and reverse:
            # first "hello," reversed = ",olleh". rest "world!" reversed = "!dlrow". joined ",olleh !dlrow". 
            # Observed ",oleh !drw". Doesn't match.
            # So E3 has inconsistent data with the concat rule too.
            # Let me reconsider: maybe the box reverses each word but with some letter-dropping.
            # Actually wait - maybe I'm miscounting. Let me carefully check "hello, world!" -> ",oleh !drw"
            # h e l l o , -> reversed , o l l e h = ",olleh"
            # w o r l d ! -> reversed ! d l r o w = "!dlrow"
            # observed ",oleh !drw"
            # ",oleh" vs ",olleh": observed has o,l,e,h (4 letters) vs o,l,l,e,h (5). Missing one l.
            # "!drw" vs "!dlrow": observed d,r,w (3) vs d,l,r,o,w (5). Missing l,o.
            # Hmm. Maybe it removes letters that appear... no.
            # Let me check "abc def ghi" -> "cba ihgfed"
            # a b c -> c b a = "cba" ✓ (no drop)
            # d e f g h i -> i h g f e d = "ihgfed" ✓ (no drop)
            # So no dropping here. But "hello," dropped an l. 
            # Hmm, maybe the comma matters. "hello," has comma at end.
            # Maybe rule: reverse word, but punctuation stays at its original position?
            # "hello," : reverse letters "olleh", comma at position 6 (end) stays at end -> "olleh,". Not ",oleh".
            # Maybe punctuation moves to front? ",olleh". Not ",oleh".
            # I'm stuck on exact rule. Let me try: maybe it's reversing and the "l l" becomes "l" due to some dedup.
            # "hello" -> "helo" (dedup ll) -> reversed "oleh" ✓ with comma front ",oleh" ✓
            # "world" -> no dupes -> "world" reversed "dlrow". But observed "drw". 
            # Hmm "world" has no consecutive dupes. So dedup doesn't explain "drw".
            # Unless... "world!" -> remove vowels? "wrld!" reversed "!dlrw". no.
            # I think I'm overanalyzing. Let me just go with the simplest rule that fits most: reverse each word individually, keep order, collapse whitespace.
            # That's model v2 which got 40% on E3. Let me see which it got wrong:
            # "abc def ghi" -> predicted "cba fed ihg", observed "cba ihgfed" ✗
            # "hello, world!" -> predicted ",olleh !dlrow", observed ",oleh !drw" ✗
            # "a  b  c" -> predicted "a b c", observed "a cb" ✗
            # "  a  b  " -> predicted "a b", observed "ba" ✗
            # "A B C" -> predicted "A B C", observed "A CB" ✗
            # "1 2 3" -> predicted "1 2 3", observed "1 32" ✗
            # Got right: "ab cd"->"ba dc", "a,b c"->"b,a c", "a b,c"->"a c,b", "x-y z"->"y-x z"
            # Pattern in wrong ones: multi-word where later words get merged/reversed together.
            # "abc def ghi" -> "cba" + " " + reverse("defghi") = "cba ihgfed" ✓
            # "a  b  c" -> "a" + " " + reverse("bc") = "a cb" ✓
            # "A B C" -> "A" + " " + reverse("BC") = "A CB" ✓
            # "1 2 3" -> "1" + " " + reverse("23") = "1 32" ✓
            # "  a  b  " -> "a" + " " + reverse("b") = "a b". Observed "ba". ✗ Hmm.
            # Wait "  a  b  " observed "ba". If rule = reverse first word, then reverse(concat rest):
            # first "a" reversed "a", rest "b" reversed "b", "a b". Not "ba".
            # Unless leading whitespace changes which is "first". Maybe leading whitespace means no first word?
            # Or maybe the rule is: reverse(concat all words) but with first word separate? 
            # "  a  b  " -> maybe "ba" = reverse("ab") = reverse(concat all). 
            # But "abc def ghi" -> reverse(concat all) = reverse("abcdefghi") = "ihgfedcba". Not "cba ihgfed".
            # Hmm.
            # Let me check "hello, world!" with the concat rule:
            # first "hello," reversed ",olleh", rest "world!" reversed "!dlrow", ",olleh !dlrow". Observed ",oleh !drw". ✗
            # So concat rule fails on "hello, world!".
            # I wonder if the observed data has some noise or if I'm misreading.
            # Given uncertainty, let me go with: reverse first word, then reverse the concatenation of remaining words, joined by space. This fits most E3 cases except "  a  b  " and "hello, world!".
            # Actually for "  a  b  ", maybe leading whitespace causes the first "word" to be empty, so first word reversed = "", rest "a b" concat "ab" reversed "ba" -> " ba" strip -> "ba" ✓!
            # Let me test: if we split preserving leading empty: "  a  b  ".split() gives ["a","b"] (no empty). 
            # But if we split on single space: "  a  b  ".split(" ") = ["","","a","","b","",""]. First word "" reversed "", rest "a","","b","","" concat "ab" reversed "ba". Join with space: " ba" -> strip "ba" ✓!
            # Let me test "abc def ghi": split(" ") = ["abc","def","ghi"]. first "abc"->"cba", rest "defghi" reversed "ihgfed", "cba ihgfed" ✓
            # "hello, world!": split(" ") = ["hello,","world!"]. first ",olleh", rest "!dlrow", ",olleh !dlrow". Observed ",oleh !drw". ✗ still.
            # Hmm. Unless "hello," -> ",oleh" via some other rule. 
            # I'll accept the concat rule and note the "hello, world!" discrepancy as unexplained.
            # Actually wait, let me reconsider "hello, world!" -> ",oleh !drw"
            # What if it's: reverse each word, but then remove duplicate letters across the whole output? 
            # ",olleh !dlrow" -> remove dupes: , o l e h ! d r w (removing second l, second o) = ",oleh !drw" ✓!!!
            # Let me verify: ",olleh !dlrow" chars: , o l l e h space ! d l r o w
            # Remove duplicates (keep first occurrence): , o l e h space ! d r w = ",oleh !drw" ✓
            # Test "abc def ghi" -> "cba fed ihg" remove dupes: c b a space f e d space i h g. No dupes across? c,b,a,f,e,d,i,h,g all unique. = "cba fed ihg". But observed "cba ihgfed". ✗
            # Hmm. So dedup doesn't give "cba ihgfed".
            # I'm going in circles. Let me just pick the concat rule (reverse first word, reverse concat of rest) and accept some errors.
            # Actually, let me reconsider whether E2 and E3 are consistent with each other.
            # E2 "ab cd ef" -> "ba fedc": first "ab"->"ba", rest "cdef" reversed "fedc", "ba fedc" ✓
            # E2 "one two three four" -> "eno ufrhwt": first "one"->"eno", rest "twothreefour" reversed "ruofeerhtowt". Observed "ufrhwt". ✗
            # Hmm E2 also has this issue. "ufrhwt" is much shorter.
            # Maybe there's dedup: "ruofeerhtowt" remove dupes: r u o f e h t w = "ruofehtw". Not "ufrhwt".
            # Hmm. "ufrhwt" = u f r h w t. 
            # "ruofeerhtowt": r u o f e e r h t o w t. Remove dupes: r u o f e h t w = "ruofehtw". 
            # Not matching. 
            # What if it's reverse then take every other? "ruofeerhtowt" odd: r o e r t w = "roertw", even: u f e h o t = "ufeh ot". no.
            # I give up on exact. Let me go with concat rule.
            words = s.split()
            if not words:
                out.append("")
                continue
            first = words[0][::-1]
            if len(words) == 1:
                out.append(first)
            else:
                rest = "".join(words[1:])[::-1]
                out.append(first + " " + rest)
        return {"outputs": out}
    except Exception:
        return {"outputs": []}
