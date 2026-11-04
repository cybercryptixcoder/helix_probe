import math

def predict(probe):
    # Beliefs:
    # A: f(x) = 1.3x^3 + 2.3x^2 - 1.6x - 48.6 outside a special interval [E2,E3,E4,E5,E1]
    # B: There is a special interval around x in [~99, ~115] where f is nearly constant ~7772.85 [E6]
    #    E6: x=99 -> 7772.8241, x=115 -> 7772.9981 (still flat); x=97 -> 1207911.8 (cubic),
    #        x=120 -> 2279279.4 (cubic). So interval is roughly (97, 120), boundaries uncertain.
    #    E3: x=104.5 -> 7772.8522, x=104.9 -> 7772.8879, x=103.0 -> 7772.933 (flat).
    #        x=102.1 -> 7772.8396 (flat). x=79.4 -> 665060.4 (cubic), x=123.6 -> 2489592.6 (cubic).
    #    E5: x=102.1 -> 7772.845 (flat), x=105.7 -> 7772.8271 (flat), x=119.5 -> 2251041.6 (cubic).
    #    So flat region is approximately [99, 115] but E6 shows 99 and 115 both flat, 97 and 120 cubic.
    #    E3 shows 102.1 flat, 103 flat, 104.5 flat, 104.9 flat; 123.6 cubic.
    #    E5 shows 119.5 cubic, 105.7 flat, 102.1 flat.
    #    Boundary: flat for x in [~98, ~116]?  E6: 99 flat, 97 cubic; 115 flat, 120 cubic.
    #    E5: 119.5 cubic. E3: 123.6 cubic.
    #    Need finer boundary. Guess: flat for x in [98, 116]. Values ~7772.85 with tiny noise.
    #    The flat value varies slightly (7772.82 to 7773.00) - looks like noise around ~7772.9.
    #    Use constant 7772.9 in the flat region.
    # C: The flat region only appears on the positive side (no evidence of negative analog).

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

        if 98.0 <= x <= 116.0:
            # Flat special interval, value ~7772.9 (noise ~0.1)
            y = 7772.9
        else:
            y = 1.3*x*x*x + 2.3*x*x - 1.6*x - 48.6

        ys.append(y)

    return {"y": ys}
