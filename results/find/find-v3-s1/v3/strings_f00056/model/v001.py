def predict(probe):
    # Dedupe characters case-insensitively, keeping first occurrence [E1]
    # Then shift the first character back by 1 in the alphabet, preserving case, wrapping a->z/A->Z [E1]
    out = []
    for s in probe["inputs"]:
        seen = set()
        kept = []
        for ch in s:
            k = ch.lower()
            if k not in seen:
                seen.add(k)
                kept.append(ch)
        if kept:
            c = kept[0]
            if 'a' <= c <= 'z':
                kept[0] = chr((ord(c) - ord('a') - 1) % 26 + ord('a'))
            elif 'A' <= c <= 'Z':
                kept[0] = chr((ord(c) - ord('A') - 1) % 26 + ord('A'))
        out.append(''.join(kept))
    return {"outputs": out}
