def predict(probe):
    # Rules inferred from evidence:
    # 1. Collapse any run of the same lowercase letter to a single letter [E1: hello->helo, HELLO->HELO; E2: book->bok, see->seh, add->adh, egg->egh, off->ofh, miss->mish, butter->buterh, happy->hapy, coffee->cofeh, summer->sumerh]
    # 2. Append 'h' to every output [E1: Hello->Heloh, 123->123h, A1!->A1!h, a b c->a bch, Test->Testh; E2: all]
    # 3. Uppercase letters are NOT collapsed [E1: HELLO->HELOh keeps... wait, HELLO->HELOh shows LL collapsed even uppercase]
    #    Actually HELLO->HELOh: LL collapsed. So collapse applies regardless of case? But Hello->Heloh keeps 'll'? No: Hello->Heloh has 'll' intact.
    #    Hmm: "hello"->"helo" (ll collapsed), "Hello"->"Heloh" (ll NOT collapsed), "HELLO"->"HELOh" (LL collapsed).
    #    So collapse happens for all-lowercase and all-uppercase, but not mixed? Or: collapse only when the doubled letter is not adjacent to a case change?
    #    Simpler: collapse runs of identical letters only when the whole word is uniform case? "Hello" has mixed case -> no collapse.
    #    Check "two words"->"two rdsh": 'wo'->'rds'? That's odd. Maybe it's a different transformation.
    #    "hello world"->"helo wrd": ll collapsed, 'o' in world dropped.
    #    "test"->"tesh": 't' dropped? test->tes then h? Actually "tes"+"h" = "tesh", so final 't' dropped.
    #    Let me reconsider: maybe rule is collapse doubled letters, then drop last char if it's a consonant? test->tes (drop t) -> tesh. hello->helo (ll->l) -> helo (ends in o, keep) -> heloh? But observed "helo" not "heloh"!
    #    Wait "hello"->"helo" (no h). "test"->"tesh" (h). "book"->"bokh" (h). So h appended sometimes.
    #    Maybe: append 'h' unless the result ends in a vowel? hello->helo ends in 'o' (vowel) -> no h. test->tes ends in 's' (consonant) -> h. book->bok ends in 'k' -> h. see->seh ends in 'e'? see->se (collapse ee->e) ends in 'e' vowel, but observed "seh" has h! Contradiction.
    #    Hmm see->seh: collapse ee->e gives "se", then h appended -> "seh". So vowel ending still gets h.
    #    But hello->helo no h. Difference: hello has 5 letters, see has 3? 
    #    Let's list: hello->helo (no h), Hello->Heloh (h), HELLO->HELOh (h), two words->two rdsh (h), hello world->helo wrd (no h), 123->123h, A1!->A1!h, a b c->a bch, test->tesh, Test->Testh.
    #    book->bokh, see->seh, add->adh, egg->egh, off->ofh, miss->mish, butter->buterh, happy->hapy, coffee->cofeh, summer->sumerh.
    #    Notice: "happy"->"hapy" (no h!), "hello"->"helo" (no h), "hello world"->"helo wrd" (no h).
    #    happy ends in 'y' after collapse pp->p: "hapy" ends in y. hello->helo ends in o. hello world->helo wrd ends in d... but no h. Hmm.
    #    Maybe h appended only if original word (after collapse) ends in a consonant AND ... no, wrd ends in d consonant but no h.
    #    Wait "hello world"->"helo wrd": maybe the 'h' rule applies per-word? "hello"->"helo" (no h), "world"->"wrd" (no h). Combined "helo wrd". So no h for multi-word? But "two words"->"two rdsh" has h at end. And "a b c"->"a bch" has h.
    #    Difference: "two words" and "a b c" have spaces... both have spaces. "hello world" also has space but no h.
    #    Hmm. Maybe h is appended if the last character of the (transformed) string is a letter that is... 
    #    Let's look at last char of output before h: helo->o, Heloh->o (h present), HELOh->O (h present), two rds->s (h), helo wrd->d (no h), 123->3 (h), A1!->! (h), a bc->c (h), tes->s (h), Test->t (h).
    #    bok->k (h), se->e (h), ad->d (h), eg->g (h), of->f (h), mis->s (h), buter->r (h), hapy->y (no h), cofe->e (h), sumer->r (h).
    #    So no-h cases: helo (ends o), helo wrd (ends d), hapy (ends y). h cases include endings o (Heloh, HELOh), e, s, etc.
    #    What distinguishes "helo" from "Heloh"? Case! "Hello" mixed case -> h. "hello" all lower -> no h. "HELLO" all upper -> h.
    #    "happy" all lower -> no h. "book" all lower -> h. Contradiction with "all lower -> no h".
    #    Maybe h appended if the word ends in a consonant after collapse? book->bok ends k (h), happy->hapy ends y (no h), hello->helo ends o (no h), see->se ends e but h present! Contradiction.
    #    Hmm see->seh: maybe collapse ee->e gives "se", then... e is vowel, but h present.
    #    Let me reconsider the collapse: maybe it's not collapse but something else. "see"->"seh": could be "see" -> "se" + "h"? Or "see" -> "seh" by replacing last e with h? 
    #    "coffee"->"cofeh": coffee -> cofe + h? ff->f, ee->e gives "cofe", then h. 
    #    "add"->"adh": dd->d gives "ad", then h.
    #    "egg"->"egh": gg->g gives "eg", then h.
    #    "off"->"ofh": ff->f gives "of", then h.
    #    "miss"->"mish": ss->s gives "mis", then h.
    #    "butter"->"buterh": tt->t gives "buter", then h.
    #    "summer"->"sumerh": mm->m gives "sumer", then h.
    #    "happy"->"hapy": pp->p gives "hapy", NO h.
    #    "hello"->"helo": ll->l gives "helo", NO h.
    #    So after collapse, some get h, some don't. hapy (ends y), helo (ends o). Others end in consonant and get h.
    #    But see->se ends in e (vowel) and gets h. coffee->cofe ends e and gets h.
    #    So maybe: h appended unless the result ends in 'o' or 'y'? helo ends o (no h), hapy ends y (no h). All others end in consonant or e -> h.
    #    Check "hello world"->"helo wrd": ends d, should get h but doesn't! Contradiction.
    #    Unless multi-word handling differs. "two words"->"two rdsh": ends s, gets h. "a b c"->"a bch": ends c, gets h. "hello world"->"helo wrd": ends d, no h.
    #    Hmm "hello world" -> "helo wrd": maybe 'o' in world dropped (world->wrd, dropping o and l? no, world->wrd drops o and l? w-o-r-l-d -> w-r-d, drops o and l). That's weird.
    #    Maybe the rule is: collapse doubled letters, then drop the last letter if it's 'o' or 'y'? helo->hel (drop o)? No, output is "helo".
    #    I'm overcomplicating. Let me focus on E2 which is clean: all single lowercase words. Rule: collapse doubled letters, then append 'h' UNLESS the result ends in 'y' or 'o'? hapy ends y no h, helo ends o no h. But see->seh ends e has h, coffee->cofeh ends e has h. So exception is y and o endings.
    #    Check E1: "hello"->"helo" ends o, no h. Consistent. "happy"->"hapy" ends y, no h. Consistent.
    #    "hello world"->"helo wrd": if we apply per whole string: collapse ll->l gives "helo world", then... world has no doubles. Ends d, should get h but doesn't. 
    #    Unless the rule is: append h only if the string (after collapse) ends in a consonant that is not... hmm wrd ends d.
    #    Maybe "hello world" output "helo wrd" is actually "helo wrd" = "helo" + " " + "wrd"? world->wrd: drop 'o' and 'l'? w-o-r-l-d -> w-r-d. That's dropping o and l. Weird.
    #    Alternatively "world"->"wrd" by collapsing? No doubles. 
    #    Maybe the box removes vowels in some positions? "two words"->"two rds": words->rds (drop w,o? words -> rds: drop w,o). two->two (keep). Hmm.
    #    This is getting too speculative. Let me just implement the clear rules from E2 and E1 for single words, and for multi-word do best guess.
    # Best model: for each word (split by space), collapse consecutive identical letters (case-insensitive? HELLO->HELO shows uppercase collapse too; Hello->Heloh shows no collapse for mixed case 'll').
    #   Actually Hello->Heloh: 'll' not collapsed. So collapse only when the doubled letters are same case AND... hello all lower collapsed, HELLO all upper collapsed, Hello mixed not collapsed.
    #   Rule: collapse runs of identical letters only if the entire word is uniform case (all lower or all upper)? "Hello" mixed -> no collapse. Check "Test"->"Testh": no doubles. "A1!" no doubles.
    #   For E2 all lowercase -> collapse.
    # Then append 'h' unless the resulting word ends in 'o' or 'y' (lowercase) or 'O'/'Y'? HELLO->HELOh ends O and has h! So uppercase O gets h. So exception only for lowercase 'o' and 'y'.
    #   Check: helo (lower o) no h. hapy (lower y) no h. HELO (upper O) h. 
    #   What about "Hello"->"Heloh": ends 'o' lowercase but has h! Contradiction. Hmm Hello->Heloh ends 'o' and has h.
    #   So exception for 'o' ending only when all-lowercase? hello all lower -> helo no h. Hello mixed -> Heloh h. 
    #   So: no h if word is all-lowercase AND ends in 'o' or 'y'. Otherwise h.
    #   Check "happy" all lower ends y -> no h. "hello" all lower ends o -> no h. "book" all lower ends k -> h. "see" all lower ends e -> h. Consistent.
    #   "hello world": two words. Per-word: hello->helo (no h), world->? world all lower, no doubles, ends d -> should get h -> "worldh"? But observed "wrd". Hmm.
    #   Maybe multi-word: apply to whole string? "hello world" all lower, ends d -> h? But no h observed.
    #   I'll handle multi-word as: apply collapse to whole string, then h rule on whole string. "hello world" -> "helo world" (collapse ll), ends d -> h -> "helo worldh". But observed "helo wrd". Doesn't match.
    #   The "world"->"wrd" is unexplained. Maybe it's a vowel-drop in second word? "two words"->"two rds": words->rds (drop w,o). "a b c"->"a bch": b c -> bc (drop space? no, "a b c"->"a bch" keeps spaces? "a bch" = a, space, bch? Actually "a b c" -> "a bch": maybe "b c" -> "bc" then h? "a bc" + h = "a bch". So space between b and c removed? 
    #   This is too messy. I'll implement the clean single-word rule and for multi-word just do best guess: collapse doubles, append h unless all-lower ends o/y.
    # Given uncertainty, mark with ?.
    import re
    def transform(s):
        # collapse runs of identical letters if word is uniform case
        # apply per word? Let's do per whole string for simplicity but handle case.
        # Determine if whole string is all lower or all upper (ignoring non-letters)
        letters = [c for c in s if c.isalpha()]
        uniform = False
        if letters:
            if all(c.islower() for c in letters) or all(c.isupper() for c in letters):
                uniform = True
        if uniform:
            # collapse runs
            res = []
            prev = None
            for c in s:
                if c == prev:
                    continue
                res.append(c)
                prev = c
            s2 = ''.join(res)
        else:
            s2 = s
        # append h unless all-lowercase and ends in o or y
        if letters and all(c.islower() for c in letters) and s2 and s2[-1] in 'oy':
            return s2
        return s2 + 'h'
    out = []
    for s in probe.get("inputs", []):
        try:
            out.append(transform(s))
        except Exception:
            out.append(s + 'h')
    return {"outputs": out}
