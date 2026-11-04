def predict(probe):
    xs = probe.get("x", [])
    out = []
    for x in xs:
        try:
            x = float(x)
        except Exception:
            out.append(None)
            continue
        # Baseline flat region
        y = 81.0
        # Rising region near the upper end; breakpoint uncertain, start ~110
        if x > 110:
            # linear-ish rise reaching ~88.6 at 127
            y = 81.0 + (x - 110) * (7.6 / 17.0)
        out.append(y)
    return {"y": out}
