def predict(probe):
    def transform(s):
        try:
            out = []
            for ch in s:
                if not out or out[-1] != ch:
                    out.append(ch)
            res = ''.join(out)
            if not res.endswith('h'):
                res = res + 'h'
            return res
        except Exception:
            return s
    try:
        return {"outputs": [transform(x) for x in probe.get("inputs", [])]}
    except Exception:
        return {"outputs": []}
