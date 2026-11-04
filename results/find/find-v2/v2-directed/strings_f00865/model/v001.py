def predict(probe):
    # Rule: the first character of each word (word = maximal run of letters)
    # is shifted forward by one in the alphabet, preserving case.
    # Evidence: "hello"->"fello", "Hello"->"Fello", "HELLO"->"FELLO",
    # "hello world"->"fello world" (only first word's first letter changed? no:
    #   "world"->"world" unchanged, so only the FIRST word is affected),
    # "two words"->"rwo words" (t->r, w unchanged),
    # "abc123"->"ybc123" (a->y, wrap-around),
    # "a b c"->"y b c" (only first char),
    # "Hello, World!"->"Fello, World!" (only first char),
    # "12345"->"12345", "!@#$%"->"!@#$%" (no letters at start).
    # So: shift the FIRST letter of the string by +1 (wrapping z->a), keep case.
    # '?' uncertain whether it's only the first char or first letter of first word;
    # evidence shows only the very first character position is affected.
    s = probe.get("inputs", [])
    out = []
    for x in s:
        if not x:
            out.append(x)
            continue
        c = x[0]
        if 'a' <= c <= 'z':
            c = chr((ord(c) - ord('a') + 1) % 26 + ord('a'))
        elif 'A' <= c <= 'Z':
            c = chr((ord(c) - ord('A') + 1) % 26 + ord('A'))
        out.append(c + x[1:])
    return {"outputs": out}
