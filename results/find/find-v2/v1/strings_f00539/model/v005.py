def predict(probe):
    def transform(s):
        try:
            # collapse runs
            collapsed = []
            for ch in s:
                if not collapsed or collapsed[-1] != ch:
                    collapsed.append(ch)
            # remove chars already seen
            seen = set()
            deduped = []
            for ch in collapsed:
                if ch not in seen:
                    seen.add(ch)
                    deduped.append(ch)
            res = ''.join(deduped)
            if res.endswith('h') or res.startswith('h'):
                return res
            return res + 'h'
        except Exception:
            return s
    try:
        return {"outputs": [transform(x) for x in probe.get("inputs", [])]}
    except Exception:
        return {"outputs": []}
