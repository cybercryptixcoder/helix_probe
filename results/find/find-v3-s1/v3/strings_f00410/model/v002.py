def predict(probe):
    # Reverse the order of whitespace-separated words, keeping each word's
    # characters in their original order [E1, E2].
    #   "abc def" -> "def abc"  -> observed "ded cba"?? no...
    # Wait: observed "abc def" -> "ded cba". That's full-string reversal.
    # But "a b c" -> "a b a" (not "c b a"), and "AbC dEf" -> "dEd CbA"
    # (not "fEd CbA"). So it's NOT pure reversal.
    #
    # Look again:
    #   "abc def"    -> "ded cba"   (reverse chars, then...? "fed cba" expected)
    #   "abc  def"   -> "ded  cba"
    #   "abc def "   -> " fed cba"
    #   " abc def"   -> "ded cba "  (leading space moved to end)
    #   "a b c"      -> "a b a"     (last char 'c' -> 'a'??)
    #   "ab cd ef"   -> "de dc ba"
    #   "Hello, world!" -> "!dlrow ,olleH"  (pure reversal!)
    #   "123 456"    -> "654 321"   (pure reversal)
    #   "AbC dEf"    -> "dEd CbA"   (pure reversal would be "fEd CbA")
    #   "x"          -> "v"         (x -> v?!)
    #
    # Pattern: it's full-string reversal, but certain characters get
    # transformed. Compare reversed vs observed:
    #   "abc def" rev="fed cba" obs="ded cba"  : 'f'->'d'
    #   "a b c"   rev="c b a"   obs="a b a"    : 'c'->'a'
    #   "AbC dEf" rev="fEd CbA" obs="dEd CbA"  : 'f'->'d'
    #   "x"       rev="x"       obs="v"        : 'x'->'v'
    #   "Hello, world!" rev matches exactly (no f/c/x present)
    #   "123 456" rev matches (no f/c/x)
    #   "abc  def" rev="fed  cba" obs="ded  cba": f->d
    #   "abc def " rev=" fed cba" obs=" fed cba": f->d
    #   " abc def" rev="fed cba " obs="ded cba ": f->d
    #
    # So: reverse the whole string, then map f->d, c->a, x->v.
    # Check "Mississippi Hello World data" rev = "atad dlroW olleH ippississiM"
    #   observed "ytad dlroW olleH ippississiM": 'a'->'y'?? 
    # Hmm "atad" -> "ytad": first char a->y. But "data a Python " rev =
    #   " nohtyP a atad" observed " nohtyP a atad" — 'a' unchanged there.
    # So not a global char map.
    #
    # Reconsider. Maybe it's reversal of words AND reversal of chars within
    # words, i.e. full reversal, but with a Caesar-like shift on some chars?
    # "apple" -> "clppa": rev="elppa", obs="clppa": e->c, l->l, p,p,a same.
    # "test case " -> " esac tset": rev=" esac tset" exact match.
    # "test caseMiXeD" -> "BeXiMesac tset": rev="DeXiMesac tset", D->B.
    # "data a Python " -> " nohtyP a atad": rev exact.
    # "test case Zebra" -> "yrbeZ esac tset": rev="arbeZ esac tset", a->y.
    # "Mississippi Hello World data" -> "ytad dlroW olleH ippississiM":
    #    rev="atad dlroW olleH ippississiM", a->y.
    #
    # So after reversal, some leading-ish chars change. Look at positions:
    #   "elppa" -> "clppa": pos0 e->c (-2)
    #   "DeXiMesac tset" -> "BeXiMesac tset": pos0 D->B (-2)
    #   "arbeZ esac tset" -> "yrbeZ esac tset": pos0 a->y (-2 mod 26)
    #   "atad dlroW..." -> "ytad dlroW...": pos0 a->y (-2)
    #   "fed cba" -> "ded cba": pos0 f->d (-2)
    #   "c b a" -> "a b a": pos0 c->a (-2)
    #   "fEd CbA" -> "dEd CbA": pos0 f->d (-2)
    #   "x" -> "v": pos0 x->v (-2)
    #   " esac tset" -> " esac tset": pos0 is space, unchanged
    #   " nohtyP a atad" -> same: pos0 space unchanged
    #   "!dlrow ,olleH" -> same: pos0 '!' unchanged
    #   "654 321" -> same: pos0 '6' -> '6'? digit unchanged
    #
    # So: reverse the string, then shift the FIRST character back by 2
    # in the alphabet if it's a letter (case preserved); non-letters
    # unchanged. Let's verify "abc def " rev=" fed cba": pos0 space,
    # unchanged -> " fed cba" ✓. " abc def" rev="fed cba ": pos0 f->d
    # -> "ded cba " ✓.
    #
    # Check E1 "test caseMiXeD" rev="DeXiMesac tset": D->B ✓.
    # "apple" rev="elppa": e->c ✓.
    #
    # Great, consistent. Rule: reverse whole string; then if first char
    # is an ASCII letter, shift it back 2 (wrap a->y, b->z, A->Y, B->Z).
    def shift(ch):
        if 'a' <= ch <= 'z':
            return chr((ord(ch) - ord('a') - 2) % 26 + ord('a'))
        if 'A' <= ch <= 'Z':
            return chr((ord(ch) - ord('A') - 2) % 26 + ord('A'))
        return ch
    out = []
    for s in probe["inputs"]:
        r = s[::-1]
        if r:
            r = shift(r[0]) + r[1:]
        out.append(r)
    return {"outputs": out}
