def predict(probe):
    # Reverse whole string [E1]
    # Then reverse each word's letters back? No: E2 shows words are reversed
    # in order AND each word's letters are reversed, EXCEPT the first word
    # of multi-word inputs is NOT letter-reversed... let's check.
    #
    # E2 observations:
    #  "one two three" -> "cerht owt eno"  (all words letter-reversed, order reversed)
    #  "a b c d"       -> "b c b a"        (order reversed: d c b a, but letters? single chars)
    #  "hello there"   -> "creht olleh"    (both reversed)
    #  "x y"           -> "w x"            (!!) "x y" -> "w x"  -- x became w? y became x?
    #  "ab cd ef"      -> "de dc ba"       (ef->de? cd->dc, ab->ba)
    #  "  spaced  words  " -> "  sdrow  decaps  " (words reversed+letter-reversed, spaces preserved)
    #  "word"          -> "brow"           (w->b? o->r? r->o? d->w?  "word" reversed = "drow", got "brow")
    #  "two words"     -> "qdrow owt"      (words reversed: "words two", letters: "sdrow owt", got "qdrow owt")
    #
    # Pattern: it's a Caesar-like shift? "word"->"brow": w->b (+5), o->r (+3)? no.
    # Actually "word" reversed is "drow". Got "brow". d->b (-2), r->r, o->o, w->w. Only first char shifted?
    # "two words" reversed = "sdrow owt". Got "qdrow owt". s->q (-2). First char shifted -2!
    # "x y" reversed = "y x". Got "w x". y->w (-2). First char shifted -2!
    # "ab cd ef" reversed = "fe dc ba". Got "de dc ba". f->d (-2). First char shifted -2!
    # "hello there" reversed = "ereht olleh". Got "creht olleh". e->c (-2). First char -2!
    # "one two three" reversed = "eerht owt eno". Got "cerht owt eno". e->c (-2). First char -2!
    # "a b c d" reversed = "d c b a". Got "b c b a". d->b (-2). First char -2!
    # "  spaced  words  " reversed = "  sdrow  decaps  ". Got same. First char is space, space-2? space is 0x20, -2 = 0x1e, not space. Hmm.
    #   Wait leading spaces: first char is space. space-2 would be non-space. But output starts with space.
    #   Maybe only shift if first char is a letter? Or shift applies to first non-space char?
    #   "  spaced..." first non-space is 's' -> 'q'? but output has 's'. Hmm output "  sdrow  decaps  " matches plain reverse.
    #   Actually maybe the shift is on the LAST char of the reversed string? Let's recheck.
    #   "word" reversed "drow", got "brow": last char w->w no. First char d->b yes.
    #   For spaced: reversed "  sdrow  decaps  ", first char space. If we shift first char by -2: space(32)-2=30, not space. Output keeps space. So maybe shift only letters.
    #   Let's test: first char space -> unchanged (not a letter). Consistent!
    # "Zebra" E1 -> "yrbeZ". reversed "arbeZ". first char a->y (-2). Yes!
    # "abc123" -> "321cba". reversed "321cba". first char '3'->'1'? 3-2=1 yes! digit shifted too.
    # "level" -> "jevel". reversed "level". first char l->j (-2). yes!
    # " Zebralower" -> "pewolarbeZ ". reversed "rewolarbeZ ". first char r->p (-2). yes!
    # "Hello World function lazy" -> "wzal noitcnuf dlroW olleH". reversed "yzal noitcnuf dlroW olleH". first y->w (-2). yes!
    # "bananaUPPER" -> "PEPPUananab". reversed "REPPUananab". first R->P (-2). yes!
    # "Zebra" -> "yrbeZ". reversed "arbeZ". a->y (-2). yes!
    #
    # So: reverse string, then shift the FIRST character back by 2 (if it's alphanumeric? or always?).
    # For spaced case first char is space -> unchanged. So shift only if alphanumeric, or shift wraps?
    # space-2 = 0x1e not space, so must be conditional. Let's say: if first char is alnum, shift -2.
    # What about digit '0'? 0-2 wraps? Unknown. Use mod within digits/letters? Mark with ?.
    def f(s):
        r = s[::-1]
        if r and r[0].isalnum():
            c = r[0]
            if c.isdigit():
                c = chr((ord(c) - ord('0') - 2) % 10 + ord('0'))
            elif c.islower():
                c = chr((ord(c) - ord('a') - 2) % 26 + ord('a'))
            else:
                c = chr((ord(c) - ord('A') - 2) % 26 + ord('A'))
            r = c + r[1:]
        return r
    return {"outputs": [f(s) for s in probe["inputs"]]}
