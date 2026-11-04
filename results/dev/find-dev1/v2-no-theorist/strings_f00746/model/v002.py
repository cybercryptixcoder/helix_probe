def predict(probe):
    # Letters shift +2 in alphabet, wrapping (a->c, x->z, y->a?, z->b?) [E1, E2]
    # Wait: E2 shows xyz -> zyz, XYZ -> ZYZ. So x->z, y->y, z->z?? No.
    # xyz -> zyz means x->z, y->y, z->z. That's not a uniform shift.
    # Let's check: a->c [E1], b->d? E1 "ab"->"cb" so a->c, b->b. Hmm b->b?
    # E1: "ab" -> "cb": a->c, b->b. "AB"->"CB": A->C, B->B.
    # E1: "a1"->"c1": a->c, 1->1.
    # E2: "Hello World" -> "Jello World": H->J, e->e, l->l, l->l, o->o, W->W, o->o, r->r, l->l, d->d.
    # So only the FIRST character shifts +2! Rest unchanged.
    # Check "a b" -> "c b": a->c, space, b->b. Yes first char only.
    # "xy" -> "zy": x->z, y->y. First char only. "XY"->"ZY". Yes.
    # "xyz"->"zyz": x->z, rest same. "XYZ"->"ZYZ". Yes.
    # "xYz"->"zYz": x->z. Yes.
    # "A1!b2"->"C1!b2": A->C, rest same. Yes.
    # "z"->"b": z+2 wraps to b. "Z"->"B". Yes wrap.
    # So: shift only the first character by +2 (letters, wrapping); rest unchanged.
    # Empty string -> empty string [E1]. " "->"" [E1]: single space becomes empty?
    # Hmm " " -> "". And "a b" -> "c b" keeps the space. So a lone space -> ""?
    # Maybe: if first char is space, it's... Actually " "->"" suggests space is dropped?
    # But "a b" keeps space. Maybe rule: shift first char; if result... no.
    # " "->"": first char space shifted? Space isn't a letter. Maybe spaces are stripped?
    # But "a b"->"c b" keeps internal space. Maybe leading space removed?
    # " " is all leading space -> "". Consistent with stripping leading spaces? But then "a b" has no leading space.
    # Uncertain. Guess: first char shifted +2 if letter; spaces... treat " "->"" as: if string is only spaces, return ""? 
    # Simpler: maybe the box strips? Let's just say: shift first letter +2; if first char is space, drop it? " "->"" fits.
    # Mark uncertain.
    def shift(ch):
        if 'a' <= ch <= 'z':
            return chr((ord(ch) - ord('a') + 2) % 26 + ord('a'))
        if 'A' <= ch <= 'Z':
            return chr((ord(ch) - ord('A') + 2) % 26 + ord('A'))
        return ch
    out = []
    for s in probe["inputs"]:
        if s == "":
            out.append("")
        elif s[0] == " ":
            out.append(s[1:])  # ? leading space dropped
        else:
            out.append(shift(s[0]) + s[1:])
    return {"outputs": out}
