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
                    j = i
                    while j + 1 < len(s) and s[j+1] in ('l', 'L'):
                        j += 1
                    run_len = j - i + 1
                    if not prev_letter:
                        # run at word start -> k/K
                        r.append('k' if ch == 'l' else 'K')
                        i = j + 1
                        prev_letter = True
                    elif run_len == 1:
                        # single l after letter: keep l, tail verbatim
                        r.append(ch)
                        i = j + 1
                        prev_letter = True
                    else:
                        # run of 2+ after letter: predecessor(letter)+l+tail-drop-first
                        # remove the previously appended predecessor letter
                        if r:
                            r.pop()
                        # predecessor of the letter before the run
                        prev_ch = s[i-1]
                        if prev_ch == 'a':
                            pred = 'z'
                        elif prev_ch == 'A':
                            pred = 'Z'
                        else:
                            pred = chr(ord(prev_ch) - 1)
                        r.append(pred)
                        r.append('l' if ch == 'l' else 'L')
                        tail = s[j+1:]
                        if len(tail) > 0:
                            r.append(tail[1:])
                        i = len(s)
                        prev_letter = True
                elif ch.isalpha():
                    if ch == 'a':
                        r.append('z')
                    elif ch == 'A':
                        r.append('Z')
                    else:
                        r.append(chr(ord(ch) - 1))
                    prev_letter = True
                    i += 1
                else:
                    r.append(ch)
                    prev_letter = False
                    i += 1
            out.append(''.join(r))
        return {"outputs": out}
    except Exception:
        return {"outputs": []}
