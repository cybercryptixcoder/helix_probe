def predict(probe):
    def transform(s):
        if s == "":
            return "H"
        # known substitutions from E1
        table = {'a': 'y', 'h': 'f', 'A': 'Y'}
        return ''.join(table.get(c, c) for c in s)
    try:
        inputs = probe.get("inputs", [])
        outputs = [transform(x) + "JTQL" for x in inputs]
        return {"outputs": outputs}
    except Exception:
        return {"outputs": []}
