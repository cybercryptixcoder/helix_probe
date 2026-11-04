def predict(probe):
    # Capitalize first letter of each word (title-ish but only first char of each word) [E1]
    # Evidence: "hello"->"Hello", "hello world"->"Hello world", "a b c"->"A b c",
    # "the quick brown fox"->"The quick brown fox". Only the first character of each
    # whitespace-separated word is uppercased; the rest is preserved. [E1]
    # Unknown: behavior on digits/symbols/uppercase already present. [E1]
    out = []
    for s in probe.get("inputs", []):
        try:
            # Uppercase first char of each whitespace-delimited word, keep rest.
            res = ""
            prev_space = True
            for ch in s:
                if prev_space and ch.isalpha():
                    res += ch.upper()
                else:
                    res += ch
                prev_space = ch.isspace()
            out.append(res)
        except Exception:
            out.append(s)
    return {"outputs": out}
