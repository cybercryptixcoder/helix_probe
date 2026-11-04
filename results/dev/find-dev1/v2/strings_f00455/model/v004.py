def predict(probe):
    # Mechanism discovered from the evidence:
    # 1. Each character is shifted by +1 in its own "case region":
    #    - lowercase letters a-z -> next lowercase (z->{, but see rule 3)
    #    - uppercase letters A-Z -> next uppercase (Z->[)
    #    - digits 0-9 -> next digit (9->:)
    #    - other chars (symbols, space, accented letters) -> next codepoint
    #    This is Caesar +1 on the codepoint, EXCEPT for case folding below.
    #
    # 2. Case folding: if a character is a lowercase letter, it is shifted
    #    as if it were uppercase (i.e. +1 to the uppercase codepoint), then
    #    the result is lowercased. Wait — evidence:
    #    "a"->"B" (lowercase a becomes uppercase B!) [E1]
    #    "A"->"B" [E1]
    #    "b"->"C", "B"->"C" [E4]
    #    So lowercase letters are shifted to UPPERCASE next letter.
    #    But "hello"->"Ifmmp": h->I, e->f, l->m, l->m, o->p.
    #    Hmm h->I is uppercase, e->f is lowercase. So not all lowercased.
    #
    #    Let's re-examine: "hello" -> "Ifmmp"
    #    h(104)->I(73)? No. 'h'+1='i', but output 'I'. 'e'+1='f' output 'f'.
    #    So only first char uppercased? "hello world"->"Ifmmp!xpsme":
    #    h->I, e->f, l->m, l->m, o->p, space->!, w->x, o->p, r->s, l->m, d->e.
    #    So first char h->I (uppercase), rest lowercase +1.
    #    "abc DEF 123" -> "Bcd!efg!234": a->B (upper), b->c, c->d, D->e (lower!), E->f, F->g.
    #    So uppercase letters become lowercase +1! And lowercase become lowercase +1
    #    except the very first character of the string becomes uppercase.
    #
    #    Check "A1b"->"B2c": A->B (upper, first char), 1->2, b->c. Yes.
    #    "1A"->"2b": 1->2, A->b (lowercase!). Yes.
    #    "a1B"->"B2c": a->B (first), 1->2, B->c. Yes.
    #    "Z9"->"[:" : Z->[ (first char, uppercase region +1), 9->:. Yes.
    #    "z"->"[" : z->[ (first char). Yes.
    #    "zz"->"[{" : first z->[, second z->{. Yes.
    #    "ZZ"->"[{" : first Z->[, second Z->{. Yes.
    #    So: ALL letters (upper or lower) shift +1 in lowercase, EXCEPT the
    #    first character of the string, which shifts +1 in uppercase.
    #    Wait "zz"->"[{" : second z->{ which is lowercase-region +1 (z->{).
    #    "ZZ"->"[{" : second Z->{ . Z+1='[', but output '{'. So Z->{ means
    #    uppercase letters map to lowercase +1 too? Z(90)+1=91='[' not '{'.
    #    '{' is 123 = 'z'(122)+1. So Z is treated as z then +1 -> {.
    #    Yes! Uppercase letters are lowercased first, then +1.
    #    "Z"->"[" : first char, so uppercase: Z+1='['. Yes.
    #    "Zz"->"[{" : first Z->[ (first, upper), z->{ (lower +1). Yes.
    #    "aZ"->"B{" : a->B (first, upper), Z->{ (lower +1). Yes.
    #    "az"->"B{" : a->B, z->{. Yes.
    #
    # 3. Non-letters: shifted +1 in codepoint, but only if... let's check.
    #    "1"->"2", "9"->":", "!"->"\"", " "->"!", "~"->"\x7f". Yes +1.
    #    But first char rule: "1abc"->"2bcd": 1->2 (not letter, +1). Yes.
    #    "!abc"->"\"bcd": !->" (+1). Yes.
    #    " abc"->"!bcd": space->! (+1). Yes.
    #    So non-letters always +1 codepoint regardless of position.
    #
    # 4. Accented/unicode: "é"->"Ê" first char? "é"->"Ê" [E2]. é(233)+1=234='ê',
    #    but output 'Ê'(202). Hmm. 'é' lowercase, first char -> uppercase region?
    #    Upper of é is É(201), +1 = Ê(202). Yes!
    #    "éa"->"Êb": é->Ê (first, upper), a->b (lower +1). Yes.
    #    "aé"->"Bê": a->B (first), é->ê (lower +1). Yes.
    #    "Éa"->"Êb": É->Ê (first, upper +1), a->b. Yes.
    #    "éé"->"Êê": first é->Ê, second é->ê. Yes.
    #    "ÉÉ"->"Êê": first É->Ê, second É->ê (lowercased then +1). Yes.
    #    "中"->"丮": 中(20013)+1=20014='丮'. Non-letter, +1. Yes.
    #    "中a"->"丮b": 中->丮, a->b. Yes.
    #    "中é"->"丮ê"? E7 "中éa"->"丮êb": 中->丮, é->ê (not first, lower +1), a->b. Yes.
    #
    # 5. So the rule:
    #    For each character c at index i:
    #      if c is a letter (has upper/lower):
    #         base = c.lower()
    #         shifted = chr(ord(base)+1)  # lowercase region +1
    #         if i == 0: shifted = shifted.upper()  # first char uppercased
    #         # but careful: z->{ , then .upper() of { is { . 
    #         # "z"->"[" : z lower +1 = {, upper = { ? But output is '['.
    #         # Hmm. So first char: use uppercase region +1 directly.
    #      else:
    #         shifted = chr(ord(c)+1)
    #
    #    First char letter: shift in uppercase region: c.upper() then +1.
    #    "z"->"[" : z.upper()='Z', +1='['. Yes.
    #    "a"->"B" : A+1=B. Yes.
    #    "é"->"Ê": É+1=Ê. Yes.
    #    Non-first letter: c.lower() then +1.
    #    "Z"->"{" (non-first): z+1={. Yes.
    #    "É"->"ê" (non-first): é+1=ê. Yes.
    #
    # 6. Edge: what about characters with no case (digits, symbols)?
    #    Always +1 codepoint, regardless of position. "1"->"2", "9"->":".
    #    "~"->"\x7f". Yes.
    #
    # 7. Boundary: z->{ (lower) and Z->[ (upper) and 9->: and ~->\x7f.
    #    No wraparound observed. "{"->"|", "["->"\\", "@"->"A", "`"->"a" [E9].
    #    So it's pure +1, no wrapping.

    def shift_char(c, first):
        if c.isalpha() and c.lower() != c.upper():
            # letter with case
            if first:
                u = c.upper()
                return chr(ord(u) + 1)
            else:
                l = c.lower()
                return chr(ord(l) + 1)
        else:
            # no case: +1 codepoint
            return chr(ord(c) + 1)

    s = probe.get("inputs", [])
    if not isinstance(s, list):
        s = [s]
    out = []
    for inp in s:
        if not isinstance(inp, str):
            inp = str(inp)
        res = []
        for i, ch in enumerate(inp):
            res.append(shift_char(ch, i == 0))
        out.append("".join(res))
    return {"outputs": out}
