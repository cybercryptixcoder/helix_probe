def predict(probe):
    # Last char of each string is shifted forward by 1 in alphabet [E1]
    #   "level"->"levem" (l->m), "Zebra"->"Zebrb" (a->b)
    #   "bananaUPPER"->"bananaUPPF" (R->S)
    #   "abc123"->"abc123" (3->? but digit unchanged? actually 3->3... hmm)
    # Wait: "abc123" unchanged, " Zebralower"->" Zebralowes" (r->s)
    #   "Hello World function lazy"->"...lazz" (y->z)
    # So: last char is incremented by 1 in ASCII/alphabet, but digits?
    #   "abc123": last char '3' -> '3'? That contradicts. Unless digit wraps?
    #   Actually '3'+1='4', but observed '3'. So digits are NOT shifted.
    # Rule: last character shifted +1 if it's a letter; digits/symbols unchanged.
    # 'z'->? 'Z'->? wrap? unknown. 'y'->'z' ok. Try wrap z->a? mark with ?
    def shift(s):
        if not s:
            return s
        c = s[-1]
        if 'a' <= c <= 'y':
            return s[:-1] + chr(ord(c)+1)
        if 'A' <= c <= 'Y':
            return s[:-1] + chr(ord(c)+1)
        if c == 'z':
            return s[:-1] + 'a'  # ? wrap
        if c == 'Z':
            return s[:-1] + 'A'  # ? wrap
        return s  # digits, symbols, spaces unchanged
    return {"outputs": [shift(x) for x in probe["inputs"]]}
