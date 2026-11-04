import re

def predict(probe):
    try:
        inputs = probe.get("inputs", [])
        outputs = []
        for s in inputs:
            if not isinstance(s, str):
                outputs.append(s)
                continue
            # Split into tokens and separators, preserving whitespace runs
            parts = re.split(r'(\s+)', s)
            tokens = parts[0::2]
            seps = parts[1::2]
            # Reverse tokens, keep separators in place
            new_tokens = list(reversed(tokens))
            rebuilt = []
            for i, tok in enumerate(new_tokens):
                rebuilt.append(tok)
                if i < len(seps):
                    rebuilt.append(seps[i])
            outputs.append(''.join(rebuilt))
        return {"outputs": outputs}
    except Exception:
        return {"outputs": []}
