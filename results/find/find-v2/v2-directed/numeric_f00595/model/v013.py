import math

def predict(probe):
    """
    Model of the black-box function f(x).

    Beliefs (each citing evidence):
    # Base rule outside the special interval: f(x) = ceil(x) + 1 [E1, E4, E5, E12, E21]
    #   e.g. f(1.5)=2, f(-20)=-19? no: f(-20)=-19? E1 f(-16)=-17, f(-8)=-9 => ceil(x)+1
    #   Check negatives: ceil(-16)+1 = -15? but E1 says -17. So it's sign-dependent.
    # Correct base rule: for x > 0, f(x) = ceil(x)+1; for x <= 0, f(x) = floor(x)-1.
    #   E1: x=-16 -> floor(-16)-1 = -17 ✓ ; x=16 -> ceil(16)+1=17 ✓
    #   E1: x=0 -> floor(0)-1 = -1 ✓ ; x=1 -> 2 ✓
    #   E2: x=-3 -> -4 ✓ ; x=-0.5 -> floor(-0.5)-1 = -1-1=-2 ✓
    #   E2: x=0.1 -> ceil(0.1)+1 = 1+1 = 2? but E2 says 1. Hmm.
    #   Recheck: E2 x=0.1 -> 1. So for small positive x, f=1 not 2.
    #   E4: x=0.01 -> 1. x=1 -> 2. x=1.99 -> 2. x=10 -> 11.
    #   So for 0 < x, f = floor(x)+1? x=0.1 -> 1 ✓; x=1.5 -> 2 ✓; x=1.99 -> 2 ✓; x=10 -> 11 ✓; x=16 -> 17 ✓.
    #   For x <= 0: f = floor(x)-1? x=0 -> -1 ✓; x=-0.5 -> -2 ✓; x=-1 -> -2 ✓; x=-16 -> -17 ✓.
    #   But x=-1 E1 says -2, floor(-1)-1 = -2 ✓. x=-2 -> -3 ✓. Good.
    #   So base rule: f(x) = floor(x)+1 if x>0 else floor(x)-1. Equivalent: floor(x) + sign-ish.
    #   Actually for x>0: floor(x)+1; for x<=0: floor(x)-1. Check x=0: floor(0)-1=-1 ✓.
    # Special interval: for 33.31 <= x < 42.0 (approx), f is a noisy negative value around -0.45. [E6-E21]
    #   Boundary left: at x=33.3 -> 34 (base), at x=33.31 -> noisy negative. [E9, E11, E12, E21]
    #   Boundary right: at x=41.99 -> noisy negative, at x=42.0 -> base (43). [E9, E11, E21]
    #   Wait E11 x=42.0 -> -0.2854 (noisy!), E21 x=42.0 -> -0.3218 (noisy). But E9 x=42.0 -> -0.5325 noisy.
    #   E21 x=42.005 -> -0.3218? no E21: 42.0->-0.3218, 42.005->-0.3997, 42.01->-0.6599, 42.015->-0.5067, 42.02->-0.518, 42.1->43.
    #   E11: 42.0->-0.2854, 42.01->-0.3958, 42.02->-0.6159, 42.5->43.
    #   E12: 42.005->-0.5044, 42.01->-0.3431, 42.015->-0.5772.
    #   So the interval seems to be 33.31 <= x < 42.01? At 42.01 still noisy in E9/E11/E12, but E21 42.01->-0.6599 noisy, 42.02->-0.518 noisy, 42.1->43.
    #   Hmm E9: 42.01->-0.501 noisy, 42.05->43. E11: 42.02->-0.6159 noisy, 42.5->43.
    #   So right boundary is somewhere in (42.02, 42.05]. E21: 42.02->-0.518 noisy, 42.1->43. 
    #   E12: 42.015->-0.5772 noisy, 42.5->51.
    #   So interval is [33.31, 42.02] roughly? At 42.02 noisy in E11/E21. At 42.05 base in E9.
    #   Let's say interval is 33.31 <= x <= 42.02 (inclusive-ish). Actually 33.3 is base, 33.31 noisy.
    #   Right: 42.02 noisy, 42.05 base. So interval [33.31, 42.02].
    #   Inside interval, output is noisy around -0.45, values range roughly -0.19 to -0.74.
    #   We can't predict exact noise; return a representative value like -0.45.
    #   Also E5 x=33.5 -> -0.4681 (inside interval) ✓.
    #   E5 x=64.5 -> 65 base ✓.
    #   E5 x=127.5 -> 128 base (floor(127.5)+1=128) ✓.
    #   E5 x=-127.5 -> -129 (floor(-127.5)-1 = -128-1=-129) ✓.
    #   E1 x=-128 -> -129 ✓.
    # Note E5 x=33.5 -> -0.4681 inside interval ✓.
    # Note E5 x=64.5 -> 65 ✓.
    # Note E5 x=127.5 -> 128 ✓.
    # Note E5 x=-127.5 -> -129 ✓.
    # Note E1 x=-128 -> -129 ✓.
    """
    try:
        xs = probe["x"]
        ys = []
        for x in xs:
            if x is None:
                ys.append(None)
                continue
            x = float(x)
            # Special noisy interval
            if 33.31 <= x <= 42.02:
                # noisy negative value around -0.45; best guess is a constant
                ys.append(-0.45)
            else:
                if x > 0:
                    ys.append(float(math.floor(x) + 1))
                else:
                    ys.append(float(math.floor(x) - 1))
        return {"y": ys}
    except Exception:
        # never raise
        return {"y": [None] * len(probe.get("x", []))}
