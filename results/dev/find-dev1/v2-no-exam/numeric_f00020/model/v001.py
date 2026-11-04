def predict(probe):
    # f is ~81 almost everywhere (flat baseline) [E1]
    # f(128) jumps to ~89, so there's an interval near the top where it rises [E1]
    # The jump is only seen at x=128; boundary unknown, likely near the edge [E1]
    # Model: baseline 81, plus a ramp/step near x>=~112 (?) [E1]
    xs = probe.get("x", [])
    out = []
    for x in xs:
        try:
            if x >= 112:
                # linear rise from 81 at 112 to ~89 at 128 (?)
                y = 81.0 + (x - 112) * (8.0 / 16.0)
            else:
                y = 81.0
        except Exception:
            y = None
        out.append(y)
    return {"y": out}
