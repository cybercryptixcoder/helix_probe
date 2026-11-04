def predict(probe):
    # Observations:
    # - Most characters are unchanged.
    # - The LAST character is often incremented by one alphabetically:
    #   "level" -> "levem", "cat" -> "cau", "done" -> "donf" [E1,E2,E4]
    # - BUT if the last character is a digit or punctuation/space, it is unchanged:
    #   "abc123"->"abc123", "hello!"->"hello!", "world "->"world " [E1,E4,E6]
    # - Lowercase letters at the end increment within a-z; 'z' wraps to 'a':
    #   "zzz"->"zza", "quiz"->"quia", "zoo"->"zop" [E2]
    # - Uppercase letters at the end increment within A-Z; 'Z' wraps to 'A':
    #   "bananaUPPER"->"bananaUPPF", "Zebra"->"Zebrb" [E1]
    #   Wait: "Zebra" ends in 'a' -> 'b' (lowercase), consistent.
    #   "aZ"->"aA" shows uppercase Z wraps to A. [E2]
    # - So: increment the final character by one in its own case class,
    #   wrapping z->a / Z->A. Non-letters unchanged.
    # - Check "Hello World function lazy" -> "...lazz": y->z [E1]
    # - "racecar Example racecar" -> "...racecas": r->s [E5]
    # - "aMiXeD" -> "aMiXeE": D->E [E5]
    # - Empty string? Not tested; assume unchanged.

    def bump(ch):
        if 'a' <= ch <= 'z':
            return 'a' if ch == 'z' else chr(ord(ch) + 1)
        if 'A' <= ch <= 'Z':
            return 'A' if ch == 'Z' else chr(ord(ch) + 1)
        return ch

    outputs = []
    for s in probe.get("inputs", []):
        if not s:
            outputs.append(s)
        else:
            outputs.append(s[:-1] + bump(s[-1]))
    return {"outputs": outputs}
