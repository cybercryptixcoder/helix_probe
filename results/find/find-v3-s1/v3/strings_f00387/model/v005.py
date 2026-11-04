def predict(probe):
    # Capitalize first char of string, lowercase the rest [E1,E2,E3,E5,E7]
    # Leading whitespace: no capitalization [E2,E4,E5,E7]
    # Delete lowercase 'm' from ORIGINAL input, everywhere [E6,E8]
    #   'M' uppercase kept [E1,E5,E8]
    #   Deletion happens BEFORE capitalization? Check E8:
    #   "mango"->"Ango": m deleted, then 'a' capitalized -> "Ango". Yes.
    #   "mM"->"M": m deleted, M kept -> "M". Capitalization: first char of
    #     result 'M' already upper. Good.
    #   "Mm"->"M": m deleted -> "M". Good.
    #   "m&m"->"&": both m deleted -> "&". Good.
    #   "m m"->" ": both deleted -> " ". Good.
    #   "mama"->"Aa": m's deleted -> "aa", capitalize -> "Aa". Good.
    #   "Mama"->"Maa": m deleted -> "Maa". Good.
    #   "amazing"->"Aazing": m deleted -> "aazing", cap -> "Aazing". Good.
    #   E1 "caseMiXeD": M uppercase kept -> "casemixed" after lower. Good.
    # Order: delete lowercase m first, then capitalize first char (if not space).
    out = []
    for s in probe["inputs"]:
        if not s:
            out.append(s)
            continue
        # delete lowercase 'm' from original
        kept = ''.join(ch for ch in s if ch != 'm')
        if not kept:
            out.append(kept)
            continue
        first = kept[0]
        if first.isspace():
            t = first + kept[1:].lower()
        else:
            t = first.upper() + kept[1:].lower()
        out.append(t)
    return {"outputs": out}
