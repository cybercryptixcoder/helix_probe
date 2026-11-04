def predict(probe):
    # Insert '4' at index len//2 [E1]
    # Increment last char by one if letter (a-z,A-Z), wrap z->a, Z->A [E1]
    outs = []
    for s in probe["inputs"]:
        mid = len(s) // 2
        t = s[:mid] + "4" + s[mid:]
        if t:
            c = t[-1]
            if 'a' <= c <= 'z':
                t = t[:-1] + ('a' if c == 'z' else chr(ord(c)+1))
            elif 'A' <= c <= 'Z':
                t = t[:-1] + ('A' if c == 'Z' else chr(ord(c)+1))
        outs.append(t)
    return {"outputs": outs}
