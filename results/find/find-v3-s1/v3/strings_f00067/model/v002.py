def predict(probe):
    # Reverse each whitespace-delimited token; keep token order and internal
    # whitespace runs [E2: "hello  world"->"olleh  ddlrow"].
    # Prepend the last char of the last token to its reversed form, UNLESS
    # the input ends with whitespace [E1 "apple"->"eelppa"; E2 "hello world"
    # ->"olleh ddlrow"; E3 "level123"->"3321level"; E2 "test case "->"tset esac"].
    # Trailing whitespace is stripped from output [E1 "data a Python "->"atad a nohtyP";
    # E3 "test case  "->"tset esac"].
    # ? Leading whitespace: assume also stripped (no evidence).
    import re
    out = []
    for s in probe.get("inputs", []):
        ends_ws = bool(s) and s[-1].isspace()
        core = s.strip()
        if not core:
            out.append("")
            continue
        parts = re.split(r'(\s+)', core)
        token_idx = [i for i, p in enumerate(parts) if p and not p.isspace()]
        orig_last_token = parts[token_idx[-1]]
        for i in token_idx:
            parts[i] = parts[i][::-1]
        if not ends_ws:
            last_char = orig_last_token[-1]
            parts[token_idx[-1]] = last_char + parts[token_idx[-1]]
        out.append("".join(parts))
    return {"outputs": out}
