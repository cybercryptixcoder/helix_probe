def predict(probe):
    # f is odd-ish and nearly linear with slope ~4.75 across the range [E1]
    # Small positive offset at 0 (~3.9) suggests a smooth nonlinearity, not pure linear [E1]
    # Slope ~4.75: (607.6-(-595.7))/(128-(-128)) = 1203.3/256 = 4.70 [E1]
    # Near 0: f(0)=3.9, f(1)=8.9, f(-1)=-0.24 -> slope ~4.6, offset ~4.3 [E1]
    # Slight curvature: slope between 64 and 128 is (607.6-305.9)/64=4.71;
    #   between -128 and -64 is (-295.7-(-595.7))/64=4.69; fairly linear [E1]
    # Model: f(x) ≈ 4.7*x + 4.0 (a smooth MLP approximating a line with small offset)
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            ys.append(4.7 * x + 4.0)
        except Exception:
            ys.append(None)
    return {"y": ys}
