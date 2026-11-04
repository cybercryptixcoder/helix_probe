def predict(probe):
    # Only the FIRST letter of each input is shifted back 2 in the alphabet [E1,E2,E3]
    #   'abc123'->'ybc123', 'level'->'jevel', 'Hello World...'->'Fello World...'
    #   'Example123'->'Cxample123', 'test case'->'rest case', 'world42'->'uorld42'
    #   'function Hello World'->'dunction Hello World', 'racecar...'->'pacecar...'
    # Rest of the string is unchanged [E1,E2,E3]
    # Case preserved; wrap around [E1: 'banana'->'zanana', 'Zebra'->'Xebra']
    def shift(c):
        if 'a' <= c <= 'z':
            return chr((ord(c) - ord('a') - 2) % 26 + ord('a'))
        if 'A' <= c <= 'Z':
            return chr((ord(c) - ord('A') - 2) % 26 + ord('A'))
        return c
    out = []
    for s in probe["inputs"]:
        if s:
            out.append(shift(s[0]) + s[1:])
        else:
            out.append(s)
    return {"outputs": out}
