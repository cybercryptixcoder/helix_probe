def predict(probe):
    # Last alphabetic char of each whitespace-separated token shifts +1, preserving case [E1, E2]
    # Non-alphabetic chars unchanged [E1]
    # Only the final letter of each whitespace-separated token changes [E1, E2]
    # z->a, Z->A wrap [E2: "z"->"a", "Z"->"A", "buzz"->"buza"]
    # Punctuation is part of the token; last alphabetic char before punctuation shifts [E2: "fizz!"->"fizz!", "end."->"end."]
    #   Wait: "fizz!" -> "fizz!" means the 'z' before '!' did NOT shift. So trailing punctuation blocks the shift?
    #   "end." -> "end." : 'd' before '.' did NOT shift.
    #   "a-b" -> "a-c": 'b' is last alpha, shifts to 'c' (no trailing punct after it).
    #   "one,two" -> "one,twp": 'o' at end shifts to 'p'.
    #   "cat's" -> "cat't": 's' at end shifts to 't'.
    #   So: if the token ends with a non-alphabetic char, no shift happens? Check "hello!"->"hello!" yes.
    #   And "  spaced  " -> "  spaced  ": 'd' not last char (trailing spaces), no shift. Consistent.
    #   "12345","a1b2c3" unchanged: last char non-alpha -> no shift. Consistent.
    # Rule: shift the last character of the token only if that last character is alphabetic.
    def transform(s):
        out = []
        i = 0
        n = len(s)
        while i < n:
            if s[i].isspace():
                out.append(s[i])
                i += 1
            else:
                j = i
                while j < n and not s[j].isspace():
                    j += 1
                w = s[i:j]
                if w and w[-1].isalpha():
                    c = w[-1]
                    if c == 'z':
                        nc = 'a'
                    elif c == 'Z':
                        nc = 'A'
                    else:
                        nc = chr(ord(c) + 1)
                    w = w[:-1] + nc
                out.append(w)
                i = j
        return ''.join(out)

    return {"outputs": [transform(x) for x in probe["inputs"]]}
