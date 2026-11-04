def predict(probe):
    # Reverse the string, but insert a "2" in the middle [E1]
    # "abc123" -> "3212cba": reversed "321cba", then "2" inserted at center
    # "level" -> "lev2el": reversed "level", "2" at center
    # " Zebralower" -> "rewola2rbeZ ": reversed "rewola rbeZ ", "2" at center
    # "Hello World function lazy" -> "yzal noitcnuf2 dlroW olleH": reversed, "2" at center
    # "bananaUPPER" -> "REPPUa2nanab": reversed, "2" at center
    # "Zebra" -> "arb2eZ": reversed, "2" at center
    # Rule: output = reverse(x) with "2" inserted at the middle position
    def transform(s):
        r = s[::-1]
        mid = len(r) // 2
        return r[:mid] + "2" + r[mid:]
    return {"outputs": [transform(x) for x in probe["inputs"]]}
