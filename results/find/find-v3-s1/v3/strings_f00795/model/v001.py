def predict(probe):
    # Observations from E1:
    # - "apple" -> "ap2plg": insert '2' after position 2, and last char 'e'->'g'? Let's check.
    #   a p p l e -> a p 2 p l g : inserted '2' after "ap", and 'e'->'g'
    # - "test case " -> "test 2case ": insert '2' after "test " (position 5)
    # - "test caseMiXeD" -> "test ca2seMiXeF": insert '2' after "test ca", last 'D'->'F'
    # - "data a Python " -> "data a 2Python ": insert '2' after "data a "
    # - "test case Zebra" -> "test ca2se Zebrc": insert '2' after "test ca", last 'a'->'c'
    # - "Mississippi Hello World data" -> "Mississippi He2llo World datc": insert '2' after "Mississippi He", last 'a'->'c'
    #
    # Pattern: insert '2' at position len//2? Let's check lengths.
    # "apple" len5 -> insert at index 2 (after 2 chars). 5//2=2. yes
    # "test case " len10 -> "test 2case " insert at index 5. 10//2=5. yes
    # "test caseMiXeD" len14 -> "test ca2seMiXeF" insert at index 7. 14//2=7. yes
    # "data a Python " len14 -> "data a 2Python " insert at index 7. yes
    # "test case Zebra" len15 -> "test ca2se Zebrc" insert at index 7. 15//2=7. yes
    # "Mississippi Hello World data" len28 -> "Mississippi He2llo World datc" insert at index 14. 28//2=14. yes
    #
    # So: insert '2' at index len//2.
    #
    # Last char change: 'e'->'g', ' '->' ', 'D'->'F', ' '->' ', 'a'->'c', 'a'->'c'
    # Hmm 'e'->'g' is +2, 'D'->'F' is +2, 'a'->'c' is +2. Space unchanged.
    # So: last char shifted +2 in alphabet if it's a letter; space stays.
    # Check: 'e'+2='g' yes. 'D'+2='F' yes. 'a'+2='c' yes. ' ' stays ' '.
    def shift(c):
        if 'a' <= c <= 'z':
            return chr((ord(c)-ord('a')+2)%26+ord('a'))
        if 'A' <= c <= 'Z':
            return chr((ord(c)-ord('A')+2)%26+ord('A'))
        return c
    outs = []
    for s in probe["inputs"]:
        if len(s) == 0:
            outs.append(s)
            continue
        mid = len(s)//2
        t = s[:mid] + '2' + s[mid:]
        t = t[:-1] + shift(t[-1])
        outs.append(t)
    return {"outputs": outs}
