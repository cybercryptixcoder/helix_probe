def predict(probe):
    # f(x) = round-half-up (floor(x+0.5)) on the interior, with a positive anomaly
    #   and asymmetric cutoffs. Evidence:
    # Interior rounding is floor(x+0.5) [E7,E8,E11].
    # Positive anomaly: 4.0 < x < 4.4 -> 5 [E8,E9,E6]; x=4.0->4 [E9,E10]; x>=4.4->0 [E8,E10]
    # Negative cutoff: x <= -4.39 -> 0 [E11:-4.39,-4.41,-4.4->0; E8:-4.4->0;
    #   E9:-4.35->-4; E8:-4.35->-4]; -4.39 < x rounds normally [E9:-4.35..-4.05->-4]
    # Outside [-4.39, 4.4) (with anomaly) -> 0 [E1,E3,E5]
    import math
    out = []
    for x in probe.get("x", []):
        try:
            if 4.0 < x < 4.4:
                out.append(5.0)
            elif -4.39 < x < 4.4:
                out.append(float(math.floor(x + 0.5)))
            else:
                out.append(0.0)
        except Exception:
            out.append(None)
    return {"y": out}
