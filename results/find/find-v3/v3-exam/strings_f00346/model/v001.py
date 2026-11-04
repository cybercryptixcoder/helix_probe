def predict(probe):
    # Observations [E1]:
    # - "abc123" -> "cbc123": first char 'a'->'c' (+2), rest unchanged
    # - "level" -> "nevel": first char 'l'->'n' (+2), rest unchanged
    # - " Zebralower" -> "Bebralower": first char ' '->'B'? Actually ' '->'B' is odd.
    #   Wait: " Zebralower" -> "Bebralower". First char ' ' -> 'B', rest "Zebralower" unchanged.
    # - "Hello World function lazy" -> "JelloWorldfunctionlazy": 'H'->'J' (+2), spaces removed
    # - "bananaUPPER" -> "dananaUPPER": 'b'->'d' (+2), rest unchanged
    # - "Zebra" -> "Bebra": 'Z'->'B' (+2 in ASCII, wraps)
    # Rule: shift first character forward by 2 in ASCII, remove spaces.
    # Check " Zebralower": first char ' ' (32) +2 = '"' not 'B'. Contradiction.
    # Hmm. Maybe spaces removed first, then first char shifted?
    # " Zebralower" remove spaces -> "Zebralower", shift 'Z'->'B' -> "Bebralower". Yes!
    # "Hello World function lazy" remove spaces -> "HelloWorldfunctionlazy", shift 'H'->'J' -> "JelloWorldfunctionlazy". Yes!
    # "abc123" no spaces, 'a'->'c'. Yes.
    # So: remove all spaces, then shift first char by +2 (mod 256? or wrap).
    out = []
    for s in probe["inputs"]:
        t = s.replace(" ", "")
        if t:
            t = chr((ord(t[0]) + 2) % 256) + t[1:]
        out.append(t)
    return {"outputs": out}
