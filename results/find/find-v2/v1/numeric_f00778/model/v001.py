def predict(probe):
    # Best guess: f(x) ≈ a*x^3 + b*x + c, fitted roughly from E1.
    # Use f(128) ≈ -8181912.66 and f(-128) ≈ 8175362.15 -> odd part dominant.
    # a ≈ (f(128)-f(-128))/(2*128^3)
    try:
        xs = probe.get("x", [])
    except Exception:
        return {"y": []}
    a = (-8181912.6576 - 8175362.1497) / (2 * 128**3)  # ≈ -3.9
    # offset near zero: f(0) ≈ 3.0185, but odd cubic gives 0, so c ≈ 3.0
    c = 3.0185
    # small linear term: use f(1) ≈ 2.8803 => a + b + c = 2.8803
    b = 2.8803 - a - c
    out = []
    for x in xs:
        try:
            xf = float(x)
            y = a * xf**3 + b * xf + c
            out.append(y)
        except Exception:
            out.append(None)
    return {"y": out}
