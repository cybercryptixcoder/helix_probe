def predict(probe):
    try:
        xs = probe["x"]
        ys = []
        for x in xs:
            if x >= 0:
                if x >= 1.0:
                    # Linear law 11.0 - 16.9*x fits x>=1 well (E15,E17,E18)
                    ys.append(11.0 - 16.9 * x)
                else:
                    # Steep near-zero curve, x in [0,1): fit to E19
                    # f(0)=5.4186, f(1)~-5.32. Use a smooth concave decreasing form.
                    # Try f(x) = 5.4186 - a*x - b*x^2 - c*x^3 fitted roughly.
                    # From E19: slope near 0 ~ -3.0, curvature increasing.
                    # Simple fit: f(x) = 5.4186 - 3.0*x - 4.5*x^2 - 3.5*x^3
                    # Check: x=0.5 -> 5.4186-1.5-1.125-0.4375=2.356 (obs 2.118)
                    # x=0.9 -> 5.4186-2.7-3.645-2.5515=-3.478 (obs -3.757)
                    # Refine coefficients via least squares intuition:
                    # Use f(x) = 5.4186 - 2.8*x - 5.5*x^2 - 3.0*x^3
                    # x=0.5: 5.4186-1.4-1.375-0.375=2.269 (obs 2.118)
                    # x=0.9: 5.4186-2.52-4.455-2.187=-3.743 (obs -3.757) good
                    # x=0.25: 5.4186-0.7-0.34375-0.0469=4.328 (obs 4.417)
                    # x=0.75: 5.4186-2.1-3.094-1.266=-1.041 (obs -1.367)
                    # Try adding more curvature: f = 5.4186 - 2.5x - 6.5x^2 - 2.5x^3
                    # x=0.25: 5.4186-0.625-0.406-0.039=4.349 (obs 4.417)
                    # x=0.5: 5.4186-1.25-1.625-0.3125=2.231 (obs 2.118)
                    # x=0.75: 5.4186-1.875-3.656-1.055=-1.168 (obs -1.367)
                    # x=0.9: 5.4186-2.25-5.265-1.8225=-3.919 (obs -3.757)
                    # Good enough; use this
                    val = 5.4186 - 2.5 * x - 6.5 * x * x - 2.5 * x * x * x
                    ys.append(val)
            else:
                # Negative side: exact linear law -6.8*x + 5.42, softened near zero
                b = -6.8
                c = 5.42
                ax = abs(x)
                g = b * x * ax / (ax + 0.6)
                ys.append(g + c)
        return {"y": ys}
    except Exception:
        return {"y": [None] * len(probe.get("x", []))}
