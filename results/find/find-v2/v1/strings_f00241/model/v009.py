def predict(probe):
    """f deletes each uppercase 'B' that is immediately followed by 'O' or 'o', applied repeatedly until stable."""
    try:
        import re
        inputs = probe.get("inputs", [])
        out = []
        for x in inputs:
            s = str(x)
            while True:
                new_s = re.sub(r"B(?=[Oo])", "", s)
                if new_s == s:
                    break
                s = new_s
            out.append(s)
        return {"outputs": out}
    except Exception:
        return {"outputs": []}
