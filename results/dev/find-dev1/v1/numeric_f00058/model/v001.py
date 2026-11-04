def predict(probe):
    try:
        xs = probe.get("x", [])
        ys = []
        for x in xs:
            if x is None:
                ys.append(None)
                continue
            x = float(x)
            # Flat plateau region
            if -32.0 <= x <= 32.0:
                ys.append(-84.3663)
            else:
                # Outside: steep growth. Fit roughly quadratic in (|x|-32) with
                # a linear term, anchored to observed points.
                a = abs(x)
                d = a - 32.0
                # Use two anchor points per side to estimate quadratic:
                # at a=64 -> 15971.28 (pos) / 44756.72 (neg)
                # at a=128 -> 258083.98 (pos) / 326549.81 (neg)
                if x > 0:
                    # solve through (32,0)->(-84.37), (64,15971.28), (128,258083.98)
                    # quadratic in d: c2*d^2 + c1*d + c0
                    # d=32: 1024c2+32c1+c0 = 15971.28+84.3663
                    # d=96: 9216c2+96c1+c0 = 258083.98+84.3663
                    # c0 = -84.3663
                    y0 = -84.3663
                    # 1024 c2 + 32 c1 = 16055.65
                    # 9216 c2 + 96 c1 = 258168.34
                    A = 16055.6505
                    B = 258168.3446
                    # from first: c1 = (A - 1024 c2)/32
                    # substitute: 9216 c2 + 96*(A-1024c2)/32 = B
                    # 9216 c2 + 3*(A - 1024 c2) = B
                    # 9216 c2 + 3A - 3072 c2 = B
                    # 6144 c2 = B - 3A
                    c2 = (B - 3*A) / 6144.0
                    c1 = (A - 1024*c2) / 32.0
                    ys.append(c2*d*d + c1*d + y0)
                else:
                    y0 = -84.3663
                    # at a=64: d=32 -> 44756.7193
                    # at a=128: d=96 -> 326549.8085
                    A = 44756.7193 + 84.3663
                    B = 326549.8085 + 84.3663
                    c2 = (B - 3*A) / 6144.0
                    c1 = (A - 1024*c2) / 32.0
                    ys.append(c2*d*d + c1*d + y0)
        return {"y": ys}
    except Exception:
        return {"y": [None for _ in probe.get("x", [])]}
