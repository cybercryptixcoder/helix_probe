def predict(probe):
    # Model beliefs:
    # - The box changes at most one character per input string [E1-E6].
    # - It finds the LAST occurrence of a lowercase letter in the string and
    #   replaces it with the next letter in the alphabet (wrapping z->a) [E1,E2,E3,E5].
    #   Evidence: "abc123"->"abc123" (last lowercase is 'c'? no output same... wait)
    #   Actually "abc123" unchanged: no? Let's re-check: E1 "abc123"->"abc123".
    #   Hmm. "level"->"levem" ('l'->'m' at last position). "Zebra"->"Zebrb" ('a'->'b').
    #   "bananaUPPER"->"bananaUPPES" ('R'->'S' uppercase!).
    #   "Hello World function lazy"->"...lazz" ('y'->'z').
    #   " Zebralower"->" Zebralowes" ('r'->'s').
    # - Wait "abc123" unchanged. Last lowercase is 'c' at index 2. Should become 'd'.
    #   But it didn't. Why? Maybe it only changes the LAST character of the string
    #   if that character is a letter? "abc123" ends with digit '3' -> unchanged.
    #   "level" ends 'l'->m. "Zebra" ends 'a'->b. "bananaUPPER" ends 'R'->S.
    #   "lazy" ends 'y'->z. "aMiXeD" ends 'D'->E. "racecar Example racecar" ends 'r'->s.
    #   "world42" ends '2' -> unchanged. "Example " ends space -> unchanged.
    #   "banana data banana " ends space -> unchanged.
    #   "cat dog " ends space -> unchanged. "cat dog!" ends '!' -> unchanged.
    #   "cat dog9" ends '9' -> unchanged.
    #   "dog-cat" ends 't'->u. "dog.cat"->"dog.cau". "dog,cat"->"dog,cau".
    #   "dog9cat"->"dog9cau". "dog\tcat"->"dog\tcau". "dog cat"->"dog cau".
    #   "dog  cat"->"dog  cau".
    # - So rule: if the last character is an ASCII letter, increment it to the
    #   next letter (case preserved, z->a, Z->A). Otherwise unchanged.
    # - Check "az"->"aa": last char 'z'->'a'. Yes.
    # - "Z"->"A": 'Z'->'A'. "z"->"a". "a z"->"a a". "az bz"->"az ba".
    # - "hello z"->"hello a". "zz"->"za". "aZ"->"aA". "Az"->"Aa". "  "->"  ".
    # - "Example123" ends '3' -> unchanged. "test case" ends 'e'->'f'. Yes.
    # - "cat  dog" ends 'g'->'h'. "cat-dog"->"cat-doh". Yes.
    # - "cat\tDog" ends 'g'->'h' but case: 'g'->'h' lowercase -> "cat\tDoh". Yes.
    # - "function Hello World" ends 'd'->'e'. Yes.
    # - "banana a data " ends space -> unchanged. Yes.
    # - "dog-cat dog" ends 'g'->'h'. Yes.
    # So the mechanism: increment the final character if it's a letter.
    out = []
    for s in probe.get("inputs", []):
        if s and s[-1].isalpha() and s[-1].isascii():
            c = s[-1]
            if c == 'z':
                nc = 'a'
            elif c == 'Z':
                nc = 'A'
            else:
                nc = chr(ord(c) + 1)
            out.append(s[:-1] + nc)
        else:
            out.append(s)
    return {"outputs": out}
