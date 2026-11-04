def predict(probe):
    # Observations [E1]:
    #  - "apple" -> "applf": last char 'e' -> 'f' (next letter)
    #  - "test case " -> "test case " (trailing space unchanged)
    #  - "test caseMiXeD" -> "test caseMiXeE": last char 'D' -> 'E' (next letter)
    #  - "data a Python " -> "data a Python " (trailing space unchanged)
    #  - "test case Zebra" -> "test case Zebrb": last char 'a' -> 'b' (next letter)
    #  - "...data" -> "...datb": last char 'a' -> 'b' (next letter)
    # Hypothesis: increment the last character by one in ASCII/letter order;
    # non-letters (spaces) are left unchanged.
    out = []
    for s in probe.get("inputs", []):
        if not s:
            out.append(s)
            continue
        last = s[-1]
        if last.isalpha():
            # advance letter, wrapping z->a / Z->A
            if last == 'z':
                nxt = 'a'
            elif last == 'Z':
                nxt = 'A'
            else:
                nxt = chr(ord(last) + 1)
            out.append(s[:-1] + nxt)
        else:
            out.append(s)
    return {"outputs": out}
