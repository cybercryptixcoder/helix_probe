def predict(probe):
    # Uppercase the first character of each whitespace-separated word; keep rest as-is [E1]
    # Already-uppercase first char stays uppercase (HELLO -> Hello: rest lowercased?) [E2]
    #   Actually "HELLO"->"Hello": whole word lowercased then first char uppercased.
    #   But "Hello"->"Hello" consistent with that too.
    # Words starting with digit/symbol are left unchanged entirely [E2: 123abc, !abc]
    # Only single spaces separate words; multiple spaces preserved, no cap after them [E2: "hello  world"->"Hello  world"]
    # Leading space: first word not capitalized [E2: " hello"->" hello"]
    # Punctuation within word doesn't split: hello-world->Hello-world [E2]
    # Hypothesis: split on single spaces only; capitalize each token that starts with a letter,
    #   lowercasing the rest of that token? "HELLO"->"Hello" suggests lowercasing rest.
    #   But "Hello"->"Hello" also fits. "hello-world"->"Hello-world" fits lowercasing rest.
    #   "123abc" unchanged (starts with digit). "!abc" unchanged.
    # ? Whether rest is lowercased for mixed case like "hELLO" unknown; assume yes (title-case per token).
    out = []
    for s in probe.get("inputs", []):
        try:
            tokens = s.split(" ")
            res = []
            for t in tokens:
                if t and t[0].isalpha():
                    res.append(t[0].upper() + t[1:].lower())
                else:
                    res.append(t)
            out.append(" ".join(res))
        except Exception:
            out.append(s)
    return {"outputs": out}
