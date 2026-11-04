def predict(probe):
    # Beliefs:
    # - Lowercase everything, then capitalize the first character of the whole string [E1, E2]
    # - Leading whitespace is preserved and prevents capitalization [E2]
    # - Drop the 'm' from any word whose first 4 chars are "exam" case-insensitively,
    #   BUT only when the 'm' itself is lowercase in the original [E4, E6]
    #   - "Example"->"Exaple", "exam"->"exa", "eXam"->"exa", "ExAm"->"exa" [E6]
    #   - "EXAM"->"exam" (M uppercase, not dropped) [E4, E6]
    #   - "exAM"->"exam" (M uppercase, not dropped) [E6]
    #   - "an EXAM room" -> "An exam roo": "room" starts with "roo"... wait
    #     Actually "room" -> "roo"? No: "room" starts with "roo", not "exam".
    #     Hmm, "An exam roo" - the 'm' dropped is from "room"? "room"[:4]="room" != "exam".
    #     Re-examine: "an EXAM room" -> "An exam roo". The word "room" lost its 'm'?
    #     "room" -> "roo" drops the final 'm'. But rule says words starting with exam.
    #     Wait - maybe the rule is: drop lowercase 'm' in any word that CONTAINS "exam"
    #     case-insensitively? "room" doesn't contain exam.
    #     Let me recheck E6: "an EXAM room" -> "An exam roo". 
    #     Hmm "room" -> "roo". That's dropping m from "room". Odd.
    #     Actually maybe the rule is: drop the lowercase 'm' in a word if the word
    #     (lowercased) starts with "exam" OR ... no.
    #     Wait, maybe it's simpler: the box drops a lowercase 'm' that is immediately
    #     preceded (in the lowercased string) by "exa"? "exam"->"exa", "example"->"exaple".
    #     "room": preceded by "roo", not "exa". So why "roo"?
    #     Re-read: "An exam roo" — could be "room"->"roo"? Or is it "exam room" where
    #     "exam"->"exa" and "room"->"roo"? Both lost m? "exam"->"exa" yes. "room"->"roo"?
    #     That would mean m dropped from "room" too. But E4 "Exam room"->"Exa roo" also!
    #     So "room"->"roo" in both. So the m-drop applies to "room" as well?!
    #     But E3 "banana data banana" no m. E5 "racecar Example racecar"->"exaple" only.
    #     Hmm what about "room"? Both E4 and E6 show "room"->"roo".
    #     Maybe the rule: drop lowercase 'm' at the END of a word? "room"->"roo", "exam"->"exa".
    #     "example"->"exaple" - m is not at end. Contradiction.
    #     Let's reconsider: maybe drop 'm' when word starts with "exam" (case-insensitive,
    #     lowercase m only) AND ALSO drop trailing 'm'? "room"->"roo" trailing m.
    #     Check E4 "Examine"->"Exaine": starts exam, m lowercase -> dropped. Good.
    #     "room"->"roo": trailing m dropped. Is there other trailing-m evidence? No.
    #     Hmm, but "banana" no m. "level" no m. 
    #     Wait, maybe I misread. "Exam room" -> "Exa roo". If only "exam"->"exa", we'd get
    #     "Exa room". But observed "Exa roo". So "room"->"roo" definitely.
    #     So there IS a trailing-m drop, OR the rule is different.
    #     Alternative: drop lowercase 'm' that comes after "exa" OR at end of word?
    #     "room": m at end -> drop. "exam": m at end -> drop (also after exa).
    #     "example": m after exa -> drop. "Examine": m after exa -> drop.
    #     "EXAMPLE": M uppercase -> not dropped (case-sensitive on the m).
    #     "exAM": M uppercase -> not dropped.
    #     "ExAm": m lowercase, after exa -> dropped -> "Exa". Good.
    #     "room": m lowercase at end -> dropped -> "roo". Good.
    #     So rule: drop a lowercase 'm' if it is at the end of a word OR immediately
    #     preceded by "exa" (case-insensitive on exa, but m must be lowercase).
    #     Check "ExampleWord"->"Exapleword": m after exa dropped. Good.
    #     Check "Examples"->"Exaples": m after exa dropped, s stays. Good.
    #     Check "test Example"->"Test exaple": m after exa dropped. Good.
    #     Check "the example"->"The exaple": good.
    #     Check "an EXAM room"->"An exam roo": EXAM M uppercase not dropped -> "exam";
    #       room m at end lowercase dropped -> "roo". Good!
    #     Check "Exam room"->"Exa roo": Exam m after exa dropped -> "Exa"; room->roo. Good!
    #     This unifies everything. 
    # - So: for each word, remove lowercase 'm' if (a) it ends the word, or
    #   (b) the 3 chars before it are "exa" (case-insensitive). Then lowercase all,
    #   capitalize first char of whole string (if not whitespace).
    import re
    def drop_m(word):
        # remove lowercase 'm' at end of word, or preceded by exa (case-insensitive)
        out = []
        i = 0
        n = len(word)
        while i < n:
            c = word[i]
            if c == 'm':
                at_end = (i == n - 1)
                after_exa = (i >= 3 and word[i-3:i].lower() == 'exa')
                if at_end or after_exa:
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
