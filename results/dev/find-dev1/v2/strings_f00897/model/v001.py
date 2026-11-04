def predict(probe):
    # Observations from E1:
    # "" -> ""            (empty stays empty)
    # "a" -> "c"          (lowercase letter shifted +2)
    # "A" -> "C"          (uppercase letter shifted +2)
    # "1" -> "5"          (digit shifted +4)
    # "!" -> "%"          (ASCII '!'=33 -> '%'=37, +4)
    # " " -> "$"          (ASCII ' '=32 -> '$'=36, +4)
    # "ab" -> "cf"        (each lowercase +2)
    # "a b" -> "c$f"      (letters +2, space +4)
    # "Hello" -> "Jipps"  (H+2=J, e+2=g? but observed 'i'... let's check)
    #   H(72)+2=J(74) ok; e(101)+2=g(103) but observed 'i'(105) -> +4?
    #   Actually "Hello" -> "Jipps": H->J(+2), e->i(+4), l->p(+4), l->p(+4), o->s(+4)
    #   Hmm inconsistent. Let's recheck: J i p p s
    #   H->J +2, e->i +4, l->p +4, l->p +4, o->s +4
    #   Maybe rule: first char +2, rest +4? Check "ab"->"cf": a->c +2, b->f +4. Yes!
    #   "a b"->"c$f": a->c +2, space->$ +4, b->f +4. Yes!
    #   "123"->"567": 1->5 +4, 2->6 +4, 3->7 +4. First char +4? But "ab" first +2.
    #   Hmm. "123" first char '1'->'5' is +4. "Hello" first +2. "ab" first +2.
    #   Maybe: first char +2 if letter, +4 otherwise? "1"->"5" +4 (single digit). "A"->"C" +2 (letter). "!"->"%" +4. " "->"$" +4.
    #   So: first char: +2 if letter, +4 otherwise. Rest: +4 always.
    #   Check "a"->"c": single letter, +2. ok. "A"->"C" +2 ok.
    #   Check "Hello": H+2=J, e+4=i, l+4=p, l+4=p, o+4=s -> "Jipps" ok!
    #   Check "123": 1+4=5, 2+4=6, 3+4=7 -> "567" ok!
    #   Check "ab": a+2=c, b+4=f -> "cf" ok!
    #   Check "a b": a+2=c, space+4=$, b+4=f -> "c$f" ok!
    #   Check "": "" ok.
    # Rule: for each char at index i: shift = 2 if (i==0 and char.isalpha()) else 4.
    #   Wait "A"->"C" +2, "1"->"5" +4. Consistent.
    #   But what about non-ASCII / overflow? Use chr(ord(c)+shift) with wraparound? Unknown. Use simple add, mod 128? Just add.
    # ? Wraparound behavior unknown; use plain chr(ord+shift).
    def shift(c, s):
        return chr(ord(c) + s)
    out = []
    for i, ch in enumerate(probe.get("inputs", [])):
        pass
    results = []
    for s in probe.get("inputs", []):
        r = ""
        for i, ch in enumerate(s):
            if i == 0 and ch.isalpha():
                r += shift(ch, 2)
            else:
                r += shift(ch, 4)
        results.append(r)
    return {"outputs": results}
