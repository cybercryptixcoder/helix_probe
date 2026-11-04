def predict(probe):
    # Reverse the string, but insert 'W' at the midpoint [E1]
    # "abc123" -> "321cba", then W at middle -> "321Wcba" [E1]
    # "level" -> "level", W at middle -> "leWvel" [E1]
    # " Zebralower" -> "rewolWarbeZ " (reversed, W at middle) [E1]
    # "Hello World function lazy" -> reversed, W at middle [E1]
    # "bananaUPPER" -> "REPPUananab", W at middle -> "REPPUWananab" [E1]
    # "Zebra" -> "arbeZ", W at middle -> "arWbeZ" [E1]
    def f(s):
        r = s[::-1]
        mid = len(r) // 2
        return r[:mid] + "W" + r[mid:]
    return {"outputs": [f(x) for x in probe["inputs"]]}
