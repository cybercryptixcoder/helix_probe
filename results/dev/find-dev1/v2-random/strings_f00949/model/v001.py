def predict(probe):
    # Rule: insert "I8" after the first vowel (a,e,i,o,u) in the string [E1]
    #   - "abc123" -> "abc8I123"?? wait, output is "abc8I123"
    #   Let's look: "abc123" -> "abc8I123": inserted "8I" after "abc"? Actually after 'c'? no.
    #   "level" -> "leI8vel": inserted "I8" after "le"? after first 'e'? "le"+"I8"+"vel" yes after 'e'.
    #   " Zebralower" -> " ZebrI8alower": after "Zebr"? inserted "I8" before 'a'. Hmm after 'r'? 
    #   "Hello World function lazy" -> "Hello World I8function lazy": inserted "I8" before "function", i.e. after space.
    #   "bananaUPPER" -> "bananI8aUPPER": after "banan", before 'a'.
    #   "Zebra" -> "ZeI8bra": after "Ze", before 'b'.
    # Pattern: insert "I8" at position len//2? 
    #   abc123 len6 -> pos3? "abc"+"8I"+"123" but got "abc8I123" -> inserted "8I" at pos3? "abc"+"8I"+"123" = "abc8I123" yes! but order "8I" not "I8".
    #   level len5 -> pos2? "le"+"I8"+"vel" = "leI8vel" yes pos2, order "I8".
    #   Hmm inconsistent order. Let's check: abc123 pos3 inserted "8I"; level pos2 inserted "I8".
    #   " Zebralower" len12 -> pos? " Zebr"+"I8"+"alower" pos5, order "I8".
    #   "Hello World function lazy" len26 -> "Hello World "+"I8"+"function lazy" pos12, order "I8".
    #   "bananaUPPER" len11 -> "banan"+"I8"+"aUPPER" pos5, order "I8".
    #   "Zebra" len5 -> "Ze"+"I8"+"bra" pos2, order "I8".
    # So insertion point = len//2 (floor). abc123: 6//2=3 -> "abc"+"??"+"123". Got "abc8I123" so inserted "8I".
    # level: 5//2=2 -> "le"+"I8"+"vel" inserted "I8".
    # Why "8I" vs "I8"? Maybe it's "I8" but for abc123... "abc"+"I8"+"123"="abcI8123" not matching. Got "abc8I123".
    # Hmm. Maybe insertion is at len//2 but the inserted string depends? Or maybe it's inserting "8I" reversed?
    # Check: maybe it's not len//2. abc123: maybe insert after 3rd char "8I". 
    # Could be "I8" inserted at position len//2 but then... no.
    # Alternative: insert "I8" at index len//2, but for even length insert "8I"? abc123 len6 even -> "8I". Others odd -> "I8".
    # Check all: level 5 odd I8 ok. Zebralower 12 even -> should be "8I" but got "I8". Contradiction.
    # Let me recount " Zebralower": space,Z,e,b,r,a,l,o,w,e,r = 11 chars. 11//2=5 -> " Zebr"+"I8"+"alower". ok odd.
    # "Hello World function lazy": count: H e l l o(5) space(6) W o r l d(11) space(12) f u n c t i o n(20) space(21) l a z y(25). len25. 25//2=12 -> "Hello World "+"I8"+"function lazy". ok odd.
    # "bananaUPPER": b a n a n a U P P E R = 11. 11//2=5 -> "banan"+"I8"+"aUPPER". ok odd.
    # "Zebra" 5 -> 2 -> "Ze"+"I8"+"bra". ok odd.
    # abc123 len6 even -> 6//2=3 -> "abc"+"8I"+"123". So even -> "8I", odd -> "I8".
    # Only one even example. Best guess: even length insert "8I", odd insert "I8" at len//2.
    s = probe.get("inputs", [])
    out = []
    for x in s:
        n = len(x)
        p = n // 2
        ins = "8I" if n % 2 == 0 else "I8"
        out.append(x[:p] + ins + x[p:])
    return {"outputs": out}
