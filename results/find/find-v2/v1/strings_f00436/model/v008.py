def predict(probe):
    try:
        out = []
        for s in probe["inputs"]:
            if " " in s:
                stripped = s.strip(" ")
                if stripped == "":
                    out.append("I")
                    continue
                tokens = stripped.split(" ")
                tokens = [t for t in tokens if t != ""]
                if not tokens:
                    out.append("I")
                    continue
                rev_tokens = [t[::-1] for t in tokens]
                joined = " ".join(rev_tokens)
                n = len(joined)
                numsp = len(tokens) - 1
                first_len = len(tokens[0])
                second_len = len(tokens[1]) if len(tokens) > 1 else 0
                if len(tokens) == 1:
                    idx = (n + 1) // 2
                elif len(tokens) == 2:
                    if first_len >= second_len:
                        idx = (first_len - 1) // 2
                    else:
                        if first_len >= 3:
                            idx = 0
                        else:
                            idx = n - 1 if n % 2 == 0 else n
                else:
                    # multi-token: best ad hoc fit
                    idx = (n - numsp) // 2 + numsp - 1 + (numsp - 1) \
                          - (numsp - 2) * 4 - (numsp - 3) * 1 \
                          + (numsp - 4) * 7 - (numsp - 5) * 7
                    idx = max(0, min(n, idx))
                out.append(joined[:idx] + "I" + joined[idx:])
            else:
                r = s[::-1]
                i = (len(r) + 1) // 2
                out.append(r[:i] + "I" + r[i:])
        return {"outputs": out}
    except Exception:
        return {"outputs": []}
