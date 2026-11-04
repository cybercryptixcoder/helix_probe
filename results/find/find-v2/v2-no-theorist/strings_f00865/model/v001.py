def predict(probe):
    # Observations from E1:
    # "abc123" -> "ybc123": first char 'a' -> 'y' (shift -2 in alphabet)
    # "level" -> "jevel": first char 'l' -> 'j' (shift -2)
    # " Zebralower" -> " Zebralower": first char is space, unchanged
    # "Hello World function lazy" -> "Fello World function lazy": 'H' -> 'F' (shift -2)
    # "bananaUPPER" -> "zananaUPPER": 'b' -> 'z' (shift -2, wraps)
    # "Zebra" -> "Xebra": 'Z' -> 'X' (shift -2)
    # Rule: shift the first character back by 2 in the alphabet (case-preserving),
    # leaving non-letters unchanged. Only the first character is affected.
    def shift(c):
        if 'a' <= c <= 'z':
            return chr((ord(c) - ord('a') - 2) % 26 + ord('a'))
        if 'A' <= c <= 'Z':
            return chr((ord(c) - ord('A') - 2) % 26 + ord('A'))
        return c
    out = []
    for s in probe.get("inputs", []):
        if s:
            out.append(shift(s[0]) + s[1:])
        else:
            out.append(s)
    return {"outputs": out}
