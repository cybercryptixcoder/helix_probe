def predict(probe):
    # Remove duplicate chars keeping first occurrence [E1: level->lev, bananaUPPER->banUPER]
    # Then shift first char back 1 if letter, wrapping a->z, A->Z [E1: abc123->zbc123, Zebra->Yebra]
    # Non-letters unchanged [E1: leading space stays]
    out = []
    for s in probe["inputs"]:
        seen = set()
        kept = []
        for c in s:
            if c not in seen:
                seen.add(c)
                kept.append(c)
        if kept:
            c = kept[0]
            if 'a' <= c <= 'z':
                kept[0] = chr((ord(c) - ord('a') - 1) % 26 + ord('a'))
            elif 'A' <= c <= 'Z':
                kept[0] = chr((ord(c) - ord('A') - 1) % 26 + ord('A'))
        out.append(''.join(kept))
    return {"outputs": out}
