def predict(probe):
    # f(x) = floor(x + 0.5) for -4.5 < x < 4.5, EXCEPT:
    # Positive anomaly: 4.0 < x < 4.4 -> 5 [E6:4.05->5, E8:4.1..4.35->5, E9:4.05..4.35->5, E10:4.4->0]
    #   E10: 4.0->4, 4.4->0, 4.45->0, 4.5->0. So anomaly is (4.0, 4.4), and >=4.4 -> 0.
    # Negative side: floor(x+0.5) down to -4.5, no anomaly [E8,E9,E10]
    #   E9: -4.05..-4.35 -> -4, -4.4..-4.5 -> 0. So cutoff at -4.4 (x <= -4.4 -> 0).
    #   E10: -3.9->-3, -4.0->-4, -4.45->0, -4.5->0. Consistent.
    # floor(x+0.5): -0.5->-0.0, 0.5->1, 1.5->2, 2.5->3, 3.5->4, -1.5->-1, -2.5->-2, -3.5->-3 [E7,E8]
    # Outside [-4.4, 4.4) (with anomaly) -> 0 [E1,E3,E5]
    import math
    out = []
    for x in probe.get("x", []):
        try:
            if 4.0 < x < 4.4:
                out.append(5.0)
            elif -4.4 < x < 4.4:
                out.append(float(math.floor(x + 0.5)))
            else:
                out.append(0.0)
        except Exception:
            out.append(None)
    return {"y": out}
