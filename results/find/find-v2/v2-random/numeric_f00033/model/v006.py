import math

def predict(probe):
    # Main structure: a narrow positive Gaussian bump near x≈0.5, sitting on a
    # shallow negative baseline, plus a negative dip near x≈12 on the positive side.
    #
    # Positive bump near x=0.5, height ~0.23, width σ²≈2.25:
    #   [E2 x=1.2->0.228, E5 x=-1.6->0.0919, E6 x=2.0->0.12,
    #    E1 x=2.9->0.0362, E10 x=-3.5->0.0066]
    # Negative-side baseline grows with |x| (power ~0.6):
    #   [E5 x=-127.7->-0.0044, E3 x=-102.2->-0.004,
    #    E3 x=-48.6->-0.0032, E1 x=-20.3->-0.0013]
    # Positive-side baseline: plateau ~-0.0004 mid-range, shrinking to 0 at large x:
    #   [E7 x=26.4->-0.0004, E9 x=101.1->-0.0001, E10 x=127->-0.0]
    # Negative dip near x≈12 on positive side:
    #   [E6 x=12.1->-0.0061, E4 x=12.5->-0.0058, E9 x=10.4->-0.0047]
    xs = probe.get("x", []) if isinstance(probe, dict) else []
    ys = []
    for x in xs:
        try:
            x = float(x)
        except Exception:
            ys.append(None)
            continue
        try:
            # positive bump near 0
            bump = 0.23 * math.exp(-((x - 0.5) ** 2) / 4.5)
            # baseline
            if x < 0:
                base = -0.0044 * (abs(x) / 128.0) ** 0.6
            else:
                if x <= 20.0:
                    base = -0.0004 * (x / 20.0)
                elif x <= 60.0:
                    base = -0.0004
                else:
                    base = -0.0004 * (128.0 - x) / 68.0
            # negative dip near x=12 (positive side only)
            if x > 0:
                dip = -0.005 * math.exp(-((x - 12.0) ** 2) / 18.0)
            else:
                dip = 0.0
            ys.append(bump + base + dip)
        except Exception:
            ys.append(None)
    return {"y": ys}
