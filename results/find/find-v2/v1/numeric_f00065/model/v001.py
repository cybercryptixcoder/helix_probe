def predict(probe):
    try:
        xs = probe.get("x", [])
        ys = []
        for x in xs:
            if x is None:
                ys.append(None)
                continue
            try:
                x = float(x)
            except Exception:
                ys.append(None)
                continue
            # Piecewise linear fit from E1
            # For x >= 0: slope ~ (-328.4446 - (-8.6723)) / (128 - 0) = -2.4974? 
            # Let's use observed: x=0 -> -8.6723; x=128 -> -328.4446 => slope -2.4974
            # x=64 -> -168.4943 => slope (-168.4943+8.6723)/64 = -2.4972
            # x=32 -> -88.5424 => slope (-88.5424+8.6723)/32 = -2.4960
            # x=16 -> -48.5665 => slope (-48.5665+8.6723)/16 = -2.4934
            # x=8 -> -28.5786 => slope (-28.5786+8.6723)/8 = -2.4883
            # x=4 -> -18.5846 => slope (-18.5846+8.6723)/4 = -2.4781
            # x=2 -> -13.5875 => slope (-13.5875+8.6723)/2 = -2.4576
            # x=1 -> -11.1045 => slope -2.4322
            # Slight curvature; use quadratic-ish. But keep simple: slope ~ -2.5 for x>0
            # For x < 0: x=-1 -> -6.7884; x=-2 -> -5.0842 => slope (-5.0842+6.7884)/(-1) = -1.7042
            # x=-4 -> -1.6258; x=-8 -> 5.4165 => slope (5.4165+1.6258)/(-4) = -1.7606
            # x=-16 -> 19.4414; x=-32 -> 47.4895 => slope (47.4895-19.4414)/(-16) = -1.7530
            # x=-64 -> 103.5874; x=-96 -> 159.678 => slope (159.678-103.5874)/(-32) = -1.7528
            # x=-128 -> 215.7687; x=-96 -> 159.678 => slope (159.678-215.7687)/(-32) = 1.7528? wait
            # (159.678-215.7687)/(-96 - -128) = (-56.0907)/32 = -1.7528. Yes.
            # So for x<0 slope ~ -1.75, intercept at 0 ~ -8.67
            # For x>0 slope ~ -2.5, intercept at 0 ~ -8.67
            if x >= 0:
                y = -8.6723 - 2.50 * x
            else:
                y = -8.6723 - 1.75 * x
            ys.append(y)
        return {"y": ys}
    except Exception:
        return {"y": []}
