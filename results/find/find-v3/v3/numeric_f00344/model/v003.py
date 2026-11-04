import math

def predict(probe):
    # Beliefs:
    # - Positive side (x>0): f(x) = -1.2x^4 - 3x^3 + 0.9x^2 - 1.6x - 36.8 [E2,E8,E19]
    # - Negative side, ordinary (-93 < x < 0): f(x) = -1.2x^4 - 3x^3 + 0.9x^2 - 1.6x - 11.7 [E2,E20,E23]
    # - Negative side clamp: for x <= -93, f(x) ≈ -24973124.6 (constant, noisy) [E22,E24]
    #   E24: x=-93.5 clamped, x=-93 NOT clamped (=-87345249). So boundary is -93.5 < b <= -93.
    #   Use x <= -93.5 as clamp (i.e. x < -93). Actually -93.5 clamped, -93 not.
    #   So clamp for x <= -93.5. Boundary between -93.5 and -93.
    #   Guess: clamp when x <= -93.5. (mark ?)
    # - x=0: f(0)=472.73 [E2,E6]
    CLAMP = -24973124.6
    def f(x):
        if x == 0:
            return 472.73
        if x > 0:
            return -1.2*x**4 - 3*x**3 + 0.9*x**2 - 1.6*x - 36.8
        # x < 0
        if x <= -93.5:  # ? boundary between -93.5 (clamped) and -93 (not)
            return CLAMP
        return -1.2*x**4 - 3*x**3 + 0.9*x**2 - 1.6*x - 11.7
    xs = probe.get("x", [])
    return {"y": [f(x) for x in xs]}
