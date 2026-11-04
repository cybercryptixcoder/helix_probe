def predict(probe):
    # Lowercase 'p' -> 'k' everywhere [E1-E11]
    # BUT: when a lowercase 'p' is immediately followed by 'l', the 'l' is deleted [E12]
    #   APpLE -> APkE  (p->k, then "kl"->"k": l dropped)
    #   aPpLe -> aPke  (p->k, l dropped)
    #   aPple -> aPkle (p->k, but no l-drop? wait)
    # Let's recheck E12:
    #   APpLE: A P p L E -> A P k L E expected, got APkE. So "kL"->"k"? l dropped (uppercase L).
    #   aPple: a P p l e -> a P k l e expected, got aPkle. l NOT dropped here.
    #   ApPle: A p P l e -> A k P l e expected, got AkPle. l NOT dropped.
    #   APPle: no lowercase p -> unchanged. ok.
    #   apPle: a p P l e -> a k P l e, got akPle. l kept.
    #   PpP: P p P -> P k P, got PkP. ok.
    #   pPp: p P p -> k P k, got kPk. ok.
    #   aPpLe: a P p L e -> a P k L e expected, got aPke. L dropped!
    #   CamelPcase: no lowercase p. ok.
    #   MiXeDPp: M i X e D P p -> ...P k, got MiXeDPk. ok.
    # So the l-drop happens when the 'l' after 'p' is UPPERCASE 'L', not lowercase 'l'.
    #   APpLE: p followed by L (uppercase) -> k, and L deleted.
    #   aPpLe: p followed by L (uppercase) -> k, L deleted.
    #   aPple: p followed by l (lowercase) -> k, l kept.
    #   ApPle: p followed by l (lowercase) -> k, l kept.
    # So rule: lowercase p -> k; if the char after p is uppercase 'L', delete that 'L'.
    # Check E4: apple -> akkle: p followed by p (not L), p followed by l (lowercase, kept). ok.
    #   simple -> simkle: p followed by l lowercase kept. ok.
    # Check E6: "ple" -> "kle": p followed by l lowercase, kept. ok.
    # Check E10: APpLE -> APkE: yes matches.
    #   p-p -> k-k: p followed by '-', ok.
    # So: replace 'p' with 'k'; then remove any 'L' that immediately follows a (now) 'k' 
    #   that came from a 'p'? Careful: need to know it was p->k.
    # Simpler: process char by char. When we see 'p', output 'k'; if next char is 'L', skip it.
    def f(s):
        out = []
        i = 0
        while i < len(s):
            c = s[i]
            if c == 'p':
                out.append('k')
                if i + 1 < len(s) and s[i+1] == 'L':
                    i += 2
                    continue
                i += 1
            else:
                out.append(c)
                i += 1
        return ''.join(out)
    return {"outputs": [f(s) for s in probe["inputs"]]}
