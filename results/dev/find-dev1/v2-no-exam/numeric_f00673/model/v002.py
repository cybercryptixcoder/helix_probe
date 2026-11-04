import math

def predict(probe):
    # f(x) ≈ 16.8*|x| + oscillatory term [E1, E4, E6, E7]
    # The oscillation is in x (not |x|): f is NOT symmetric [E5, E8]
    # At large |x| the oscillation is small relative to linear term [E6, E7]
    # Near origin there's a distinct oscillatory structure [E4, E5, E8]
    # Residual r(x) = f(x) - 16.8*|x| appears roughly sinusoidal in x
    #   with period ~? and amplitude that grows somewhat with |x| [E7, E8]
    # Try: r(x) ≈ A*sin(w*x + phi) with amplitude scaling ~ sqrt(|x|) or similar
    out = []
    for x in probe.get("x", []):
        try:
            base = 16.8 * abs(x)
            # oscillatory residual, amplitude grows slowly with |x|
            amp = 0.5 + 0.35 * math.sqrt(abs(x))
            r = amp * math.sin(2.0 * x + 0.5)
            out.append(base + r)
        except Exception:
            out.append(None)
    return {"y": out}
