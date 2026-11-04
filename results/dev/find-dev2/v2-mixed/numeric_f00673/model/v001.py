import math

def predict(probe):
    # f(x) ≈ 16.8 * x^2 + small offset [E2]
    #   E2: x=1 ->17.18, x=2 ->34.02, x=10 ->167.88, x=100 ->1679.6
    #   ratio y/x^2 ≈ 16.8 consistently for both signs and all magnitudes
    # Small additive offset ~ -0.86 at x=0 [E2]
    # Slight asymmetry/noise between +x and -x [E2]
    # E1 values also fit ~16.8*x^2 (e.g. 88.2^2*16.8≈130700? no—check)
    #   Actually E1: 88.2 -> 1481.4; 1481.4/88.2^2 = 0.1904... not 16.8
    #   Hmm: 88.2^2=7779; 1481/7779=0.190. So E1 does NOT match 16.8*x^2.
    #   But E2 x=100 -> 1679.6; 1679.6/10000=0.168. So coefficient ~0.168, not 16.8.
    #   Recheck E2: x=10 ->167.88; /100 = 1.6788. x=1 ->17.18; /1 = 17.18.
    #   So y/x^2 varies: 17.18, 8.5, 5.6, 4.17, 3.37, 1.68, 0.168...
    #   That's not x^2. Looks like y ≈ 16.8*x for small x? x=1->17.18, x=2->34.02 (≈16.8*2=33.6), x=3->50.58(≈50.4), x=10->167.88(≈168), x=100->1679.6(≈1680).
    #   Yes! y ≈ 16.8 * x, LINEAR, not quadratic. Check negatives: -1->17.73 (not -16.8). Hmm.
    #   -1 -> 17.73, -2 -> 30.77, -5 -> 84.31, -10 -> 168.4, -100 -> 1678.9.
    #   So for negative x, y ≈ 16.8*|x|. That's y ≈ 16.8*|x|.
    #   Check E1: 88.2 -> 16.8*88.2 = 1481.8 ✓ (1481.4)
    #   -20.3 -> 16.8*20.3 = 341.0 ✓ (340.2)
    #   -61.7 -> 16.8*61.7 = 1036.6 ✓ (1036.3)
    #   2.9 -> 48.7 ✓ (46.7, close-ish)
    #   -24.3 -> 408.2 ✓ (406.4)
    #   72.7 -> 1221.4 ✓ (1221.7)
    #   -50.4 -> 846.7 ✓ (847.8)
    #   -6.0 -> 100.8 ✓ (99.1)
    #   21.3 -> 357.8 ✓ (358.4)
    # So f(x) ≈ 16.8 * |x| + small noise. x=0 -> -0.86 ≈ 0.
    # Coefficient: fit ~16.8. Use 16.8.
    out = []
    for x in probe.get("x", []):
        try:
            out.append(16.8 * abs(x))
        except Exception:
            out.append(None)
    return {"y": out}
