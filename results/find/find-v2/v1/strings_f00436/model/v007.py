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
                rev_tokens = [t[::-1] for t in tokens]
                joined = " ".join(rev_tokens)
                n = len(joined)
                numsp = len(tokens) - 1
                first_len = len(tokens[0])
                second_len = len(tokens[1]) if len(tokens) > 1 else 0
                if first_len >= 3:
                    idx = 0
                elif second_len > first_len:
                    idx = n if n % 2 == 1 else n - 1
                else:
                    idx = max(0, (n - numsp) // 2 - 1)
                out.append(joined[:idx] + "I" + joined[idx:])
            else:
                r = s[::-1]
                i = (len(r) + 1) // 2
                out.append(r[:i] + "I" + r[i:])
        return {"outputs": out}
    except Exception:
        return {"outputs": []}
