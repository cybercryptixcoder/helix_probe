def predict(probe):
    """Best guess: piecewise. For x>=0: x^3 + 2^x + 22. For x<0: mirrored/negative-side cubic+exponential, still uncertain."""
    try:
        xs = probe.get("x", [])
        ys = []
        for x in xs:
            try:
                if x >= 0:
                    y = x**3 + 2.0**x + 22.0
                else:
                    # negative side: much more negative; try -( (-x)^3 + 2^(-x) + 22 ) scaled
                    # f(-1)=-37.091, f(-2)=-1502.006, f(-4)=-40769.54, f(-8)=-1202333.656
                    # try -(x^3) + 2^x + 22 form? x^3 for x=-1 is -1 -> -(-1)=1...
                    # Use -( (-x)^3 * 2^(-x) )? test: x=-1: -(1)*0.5=-0.5 no
                    # Fit: f(-1)=-37.091, f(-2)=-1502.006. ratio ~40.5
                    # try -(2^(-x)) * ((-x)^3) - 2^(-x)*22? 
                    y = -((-x)**3) * (2.0**(-x)) - 22.0 * (2.0**(-x)) + 22.0
                    # fallback: use negative of positive formula at -x
                    y = -( (-x)**3 + 2.0**(-x) + 22.0 ) + 22.0
            except Exception:
                y = None
            ys.append(y)
        return {"y": ys}
    except Exception:
        return {"y": []}
