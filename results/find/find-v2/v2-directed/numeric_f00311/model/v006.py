import math

def predict(probe):
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            x = float(x)
        except Exception:
            ys.append(None)
            continue

        # Region A: x < -9.25 (approximately). The box returns ~8 with noise.
        # Evidence: E1, E3, E9, E12 show values near 8 for x <= -9.5.
        # The transition is around x = -9.25 (E4, E6, E8).
        # For x < -9.25: output ~ 8 (noisy). We use a deterministic ~8.
        #
        # Region B: -9.25 <= x < 0. Output is linear: y = 8 - 9.6*x?
        # Check: at x=-9.25, y=96.8. At x=0, y=8.0. Slope = (8-96.8)/(0-(-9.25)) = -88.8/9.25 = -9.6.
        # So y = 8 - 9.6*x for x in [-9.25, 0).
        # E4: x=-9.25 -> 96.8; x=-8 -> 84.8; matches 8 - 9.6*(-8) = 8+76.8=84.8. Good.
        #
        # Region C: x >= 0. Output linear: y = 8 - 9.6*x?
        # At x=0, y=8. At x=10, y=-88. 8 - 9.6*10 = -88. Yes.
        # At x=128, 8 - 9.6*128 = 8 - 1228.8 = -1220.8. Matches E1, E5.
        # So actually the linear formula y = 8 - 9.6*x works for all x >= -9.25.
        #
        # But wait: E1 shows x=-8 -> 84.8, x=-4 -> 46.4, x=-2 -> 27.2, x=-1 -> 17.6, x=0 -> 8.0.
        # All match y = 8 - 9.6*x.
        # For x < -9.25, the linear formula would give: x=-10 -> 8+96=104, but observed ~8.
        # So there is a cutoff: for x < -9.25, output is ~8 (constant, noisy).
        #
        # The boundary: E4 shows x=-9.25 -> 96.8 (linear), x=-9.255 -> 96.848 (linear), x=-9.26 -> 96.896 (linear).
        # E6: x=-9.251 -> 96.8096 (linear), x=-9.25 -> 96.8 (linear), x=-9.249 -> 96.7904 (linear).
        # E8: x=-9.4 -> 8.0421 (constant ~8), x=-9.38 -> 98.048 (linear? 8 - 9.6*(-9.38) = 8+90.048=98.048. Yes!)
        # So boundary is between -9.4 and -9.38. E8: x=-9.4 -> ~8, x=-9.38 -> 98.048 (linear).
        # E3: x=-9.5 -> 7.9833 (~8), x=-9.25 -> 96.8 (linear). x=-9.1 -> 95.36 (linear).
        # E2: x=-9.5 -> 8.094 (~8), x=-9 -> 94.4 (linear).
        # So threshold is around -9.39? Let's check E8: -9.4 -> ~8, -9.38 -> linear.
        # E4: x=-9.3 -> 97.28 (linear: 8+89.28=97.28). So -9.3 is linear.
        # E8: x=-9.35 -> 97.76 (linear: 8+89.76=97.76). x=-9.4 -> 8.0421 (~8).
        # So threshold between -9.4 and -9.35. E8 has -9.4 -> 8.0421, -9.38 -> 98.048 (linear).
        # Let's check -9.39? Not given. We'll set threshold at -9.39? 
        # Actually E8: -9.4 -> 8.0421, -9.38 -> 98.048. The linear at -9.38 is 8+90.048=98.048. 
        # At -9.4 linear would be 8+90.24=98.24, but observed 8.0421. So cutoff is between -9.4 and -9.38.
        # E3: -9.5 -> 7.9833, -9.25 -> 96.8. No finer.
        # E2: -9.5 -> 8.094, -9 -> 94.4.
        # So threshold ~ -9.39. Let's pick -9.39 as boundary.
        # But E4: -9.3 -> 97.28 (linear), -9.28 -> 97.088 (linear). So -9.3 is linear.
        # E8: -9.4 -> 8.0421 (~8). So boundary is between -9.4 and -9.3? Wait, -9.35 is linear (97.76). So boundary between -9.4 and -9.35.
        # E8: -9.4 -> 8.0421, -9.38 -> 98.048 (linear). So boundary between -9.4 and -9.38.
        # Let's use -9.39 as threshold? But -9.38 is linear, so threshold must be <= -9.38? Actually if threshold is -9.39, then -9.38 > -9.39 so linear. -9.4 < -9.39 so constant. That works.
        # Check E3: -9.5 < -9.39 -> constant (7.9833, yes). -9.25 > -9.39 -> linear (96.8, yes).
        # E2: -9.5 -> constant (8.094), -9 -> linear (94.4). Good.
        # E4: -9.3 > -9.39 -> linear (97.28). Good.
        # So threshold = -9.39 (approximately). We'll use -9.39.

        threshold = -9.39
        if x < threshold:
            # constant region, noisy around 8
            y = 8.0
        else:
            # linear region
            y = 8.0 - 9.6 * x

        ys.append(y)

    return {"y": ys}
