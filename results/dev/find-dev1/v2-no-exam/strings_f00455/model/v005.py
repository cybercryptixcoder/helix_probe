def predict(probe):
    # Capitalize input: first char upper, rest lower [E1, E2, E3, E4, E5, E6, E7]
    # Then combine surrogate pairs via UTF-16 decode [E7]
    # Then +1 to each code point; >0x10FFFF -> ERROR [E5, E6]
    # Then encode result to UTF-16 units, read back as chr [E4, E6]
    out = []
    for s in probe.get("inputs", []):
        try:
            s = s.capitalize()
            b = s.encode('utf-16-le', 'surrogatepass')
            s2 = b.decode('utf-16-le', 'surrogatepass')
            r = []
            for c in s2:
                v = ord(c) + 1
                if v > 0x10FFFF:
                    raise ValueError
                r.append(chr(v))
            b2 = ''.join(r).encode('utf-16-le', 'surrogatepass')
            out.append(''.join(chr(int.from_bytes(b2[i:i+2], 'little')) for i in range(0, len(b2), 2)))
        except Exception:
            out.append("ERROR: ValueError")
    return {"outputs": out}
