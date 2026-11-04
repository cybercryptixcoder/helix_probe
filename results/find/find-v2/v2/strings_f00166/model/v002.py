def predict(probe):
    # Identity on most strings [E1, E2, E3]
    # "HELLO WORLD" -> "HEO WORD": drop every 'L'? "HELLO"->"HEO" (drop L,L), "WORLD"->"WORD" (drop L) [E2]
    # "Example123" -> "Examkle123": 'p' -> 'k'? Actually "Example"->"Examkle": p replaced by k [E3]
    # Hypothesis: some letter substitutions/removals occur, but inconsistently.
    # Maybe: replace 'p' with 'k' [E3], and remove 'L' when uppercase? [E2]
    # But E1 "Hello World function lazy" unchanged (has lowercase l's, no uppercase L).
    # E2 "HELLO WORLD" -> "HEO WORD": uppercase L removed. Lowercase l kept.
    # E3 "Example123" -> "Examkle123": lowercase p -> k.
    # Check other p's: E2 "the quick brown fox" no p. E1 "bananaUPPER" no p. 
    # "Example123" has one p -> k. Consistent with p->k rule? Only one data point.
    # Also "Zebralower" in E1 unchanged (no p, no uppercase L).
    # Rule guess: uppercase 'L' deleted; lowercase 'p' -> 'k'. Mark uncertain.
    out = []
    for s in probe["inputs"]:
        s = s.replace("L", "")
        s = s.replace("p", "k")
        out.append(s)
    return {"outputs": out}
