import math

def predict(probe):
    # Beliefs:
    # A: Outside the special interval, f(x) = 1.3x^3 + 2.3x^2 - 1.6x - 48.6 [E2,E4,E5,E7,E11,E12,E13]
    # B: Flat special interval on positive side, value ~7772.9 (noisy) [E6,E8,E10,E14]
    #    E14: x=97.999 -> 7772.98 (flat), x=98.0 -> 7772.92 (flat): boundary at 98.0
    #    E14: x=117.999 -> 2167674.6 (cubic), x=118.0 -> 2167729.4 (cubic): boundary at 118.0
    #    Wait: 117.999 is cubic, 117.99 is cubic, 117.5 is flat (E10,E14). So upper boundary in (117.99, 118.0].
    #    E14: 117.999 -> cubic, so boundary <= 117.999. And 117.99 -> cubic. 117.5 -> flat.
    #    So flat region is [98.0, B) with B in (117.5, 117.99]. Use 117.99? But E10 had 117.5 flat.
    #    Actually E14: 117.99 -> 2167180.99 (cubic). So upper bound < 117.99.
    #    E10: 117.5 -> 7773.01 (flat). So flat region is [98.0, ~117.5..117.99).
    #    Let's say [98.0, 117.5] flat, (117.5, ...) cubic. But E14 117.99 cubic, consistent.
    #    Lower: 97.999 flat, 98.0 flat. So lower boundary <= 97.999. E8: 97.5 cubic, 98 flat.
    #    So lower boundary in (97.5, 97.999]. Use 98.0? 97.999 is flat so boundary <= 97.999.
    #    Hmm, 97.99 flat (E14), 97.9 flat (E14). E8: 97.5 cubic. So boundary in (97.5, 97.9].
    #    Let's use 98.0 as lower... but 97.999 flat contradicts. Use 97.9? 97.9 flat.
    #    Actually all of 97.9,97.99,97.999,98.0 flat. E8 97.5 cubic. So boundary in (97.5, 97.9].
    #    Use 98.0 for simplicity? No—97.999 flat means boundary <= 97.999. Use 97.9.
    #    Hmm but then 97.95 unknown. Best guess: boundary at 98.0 is wrong; use 97.9? 
    #    Actually maybe boundary is exactly 98.0 but 97.999 rounds... no, 97.999 < 98.0.
    #    Let's set lower boundary = 97.9 (flat from 97.9). Upper boundary: 117.5 flat, 117.99 cubic.
    #    Use 117.5 as last flat? But could extend to 117.9. E14 117.9 -> 2162249.5 cubic!
    #    So 117.9 is cubic. 117.5 flat. Boundary in (117.5, 117.9]. Use 117.5.
    # C: No flat region on negative side [E12].

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

        if 97.9 <= x <= 117.5:
            y = 7772.9
        else:
            y = 1.3*x*x*x + 2.3*x*x - 1.6*x - 48.6

        ys.append(y)

    return {"y": ys}
