def predict(probe):
    # Observations from E1:
    # - "abc123" -> "abc123" (unchanged; no letters at end? Actually ends in digits)
    # - "level" -> "levem" (last char 'l' -> 'm')
    # - " Zebralower" -> " Zebralowes" (last char 'r' -> 's')
    # - "Hello World function lazy" -> "...lazz" (last char 'y' -> 'z')
    # - "bananaUPPER" -> "bananaUPPES" (last char 'R' -> 'S')
    # - "Zebra" -> "Zebrb" (last char 'a' -> 'b')
    # Rule: the final character is incremented to the next character (ord+1).
    # "abc123" ends in '3' -> would become '4', but observed unchanged.
    # So rule applies only when last char is a letter? Check: '3' digit -> unchanged.
    # Hypothesis: if last char is a letter, replace with next letter (ord+1);
    # otherwise leave unchanged. 'l'->'m', 'r'->'s', 'y'->'z', 'R'->'S', 'a'->'b' all fit.
    # 'z'/'Z' edge case unknown (?): wrap or unchanged? Guess unchanged for now? 
    # Actually 'y'->'z' works; 'z' unknown. Guess: increment, but if beyond 'z'/'Z' leave unchanged (?).
    def f(s):
        if not s:
            return s
        c = s[-1]
        if c.isalpha():
            o = ord(c)
            if c == 'z' or c == 'Z':
                return s  # ? unknown edge
            return s[:-1] + chr(o + 1)
        return s
    return {"outputs": [f(x) for x in probe["inputs"]]}
