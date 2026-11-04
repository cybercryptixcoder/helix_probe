def predict(probe):
    # Reverse each whitespace-delimited token; keep token order [E2].
    # Whitespace runs collapse to a single space [E4: "  two  spaces  "->"owt secaps",
    #   "one two  three"->"eno owt eeerht"].
    # Leading/trailing whitespace stripped [E1,E3,E4].
    # Prepend last char of last token to its reversed form, UNLESS input ends
    #   with whitespace [E1 "apple"->"eelppa"; E2 "hello world"->"olleh ddlrow";
    #   E3 "level123"->"3321level"; E1 "test case "->"tset esac"].
    import re
    out = []
    for s in probe.get("inputs", []):
        ends_ws = bool(s) and s[-1].isspace()
        tokens = s.split()
        if not tokens:
            out.append("")
            continue
        rev = [t[::-1] for t in tokens]
        if not ends_ws:
            rev[-1] = tokens[-1][-1] + rev[-1]
        out.append(" ".join(rev))
    return {"outputs": out}
