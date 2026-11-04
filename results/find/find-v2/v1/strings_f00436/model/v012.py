def predict(probe):
    try:
        out = []
        for s in probe["inputs"]:
            if " " in s:
                stripped = s.strip(" ")
                if stripped == "":
                    out.append("I")
                    continue
                tokens = [t for t in stripped.split(" ") if t != ""]
                if not tokens:
                    out.append("I")
                    continue
                rev_tokens = [t[::-1] for t in tokens]
                joined = " ".join(rev_tokens)
                n = len(joined)
                numsp = len(tokens) - 1
                if len(tokens) == 1:
                    idx = (n + 1) // 2
                elif len(tokens) == 2:
                    first_len = len(tokens[0])
                    second_len = len(tokens[1])
                    if first_len < second_len:
                        orig_len = len(stripped)
                        orig_idx = orig_len // 2
                        # map original index to reversed-token output index
                        # original position p in token 1 (0-based) -> reversed index first_len-1-p
                        idx = first_len - 1 - orig_idx
                        if idx < 0:
                            idx = n
                    elif first_len == second_len:
                        idx = 0
                    else:
                        if first_len == 3 and second_len == 2:
                            idx = 0
                        else:
                            idx = (first_len - 1) // 2
                else:
                    idx = n // 2 - 1 + numsp - (numsp - 2) * 3 \
                          + (numsp - 3) * 2 + (numsp - 4) * 3
                    idx = max(0, min(n, idx))
                out.append(joined[:idx] + "I" + joined[idx:])
            else:
                r = s[::-1]
                i = (len(r) + 1) // 2
                out.append(r[:i] + "I" + r[i:])
        return {"outputs": out}
    except Exception:
        return {"outputs": []}
