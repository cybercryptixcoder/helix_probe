def predict(probe):
    def transform(s):
        try:
            out = []
            for ch in s:
                if not out or out[-1] != ch:
                    out.append(ch)
            res = ''.join(out)
            if res.endswith('h') or res.endswith(' ') or res.startswith('h'):
                return res
            return res + 'h'
        except Exception:
            return s
    try:
        return {"outputs": [transform(x) for x in probe.get("inputs", [])]}
    except Exception:
        return {"outputs": []}
