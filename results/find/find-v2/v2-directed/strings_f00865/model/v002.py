def predict(probe):
    # Rule: shift the FIRST letter character in the string by +1 (wrap z->a, Z->A), keep case.
    # Evidence: "hello"->"fello", "Hello"->"Fello", "HELLO"->"FELLO" [E1]
    # "hello world"->"fello world" (only first letter) [E1]
    # "two words"->"rwo words" (t->r) [E1]
    # "abc123"->"ybc123" (a->y wrap) [E1]
    # "a b c"->"y b c" (only first letter) [E1]
    # "Hello, World!"->"Fello, World!" [E1]
    # "12345"->"12345", "!@#$%"->"!@#$%" (no letters) [E1]
    # "world hello"->"uorld hello" (w->u? no: w->u is -2... wait) [E2]
    #   Actually w->u: w=22, u=20, that's -2. Hmm. Let me recheck.
    #   "world"->"uorld": w->u. w(22)->u(20) = -2. But "hello"->"fello": h->f = -2!
    #   Wait h(7)->f(5) = -2. And "two"->"rwo": t(19)->r(17) = -2. a->y = -2 (wrap).
    #   So shift is -2, not +1! I misread earlier.
    # "x y z"->"v y z": x(23)->v(21) = -2 [E2]
    # "ab cd ef"->"yb cd ef": a->y = -2 [E2]
    # "zebra"->"xebra": z->x = -2 [E2]
    # "Zebra"->"Xebra": Z->X = -2 [E2]
    # "a b c d"->"y b c d": a->y = -2 [E2]
    # "  hello"->"  hello" (leading spaces, first letter is h but unchanged?) [E2]
    #   Wait: "  hello" output "  hello" unchanged. So leading non-letters block the shift?
    #   "1abc def"->"1abc def" unchanged. So if first char is not a letter, no change.
    #   So: only shift if the FIRST character is a letter. Shift it by -2.
    s = probe.get("inputs", [])
    out = []
    for x in s:
        if not x:
            out.append(x)
            continue
        c = x[0]
        if 'a' <= c <= 'z':
            c = chr((ord(c) - ord('a') - 2) % 26 + ord('a'))
        elif 'A' <= c <= 'Z':
            c = chr((ord(c) - ord('A') - 2) % 26 + ord('A'))
        out.append(c + x[1:])
    return {"outputs": out}
