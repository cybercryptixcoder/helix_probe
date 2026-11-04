def predict(probe):
    try:
        out = []
        for s in probe.get("inputs", []):
            r = []
            i = 0
            prev_letter = False
            while i < len(s):
                ch = s[i]
                if ch in ('l', 'L'):
                    while i + 1 < len(s) and s[i+1] in ('l', 'L'):
                        i += 1
                    if not prev_letter:
                        r.append('k' if ch == 'l' else 'K')
                    else:
                        r.append(ch)
                    prev_letter = True
                elif ch.isalpha():
                    if ch == 'a':
                        r.append('z')
                    elif ch == 'A':
                        r.append('Z')
                    else:
                        r.append(chr(ord(ch) - 1))
                    prev_letter = True
                else:
                    r.append(ch)
                    prev_letter = False
                i += 1
            out.append(''.join(r))
        return {"outputs": out}
    except Exception:
        return {"outputs": []}
