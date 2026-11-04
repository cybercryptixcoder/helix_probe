import math

def predict(probe):
    # Observations:
    # - Outputs are small, roughly in [-3, 4] [E1, E2, E3, E4].
    # - E4 fine sweep 0..12 shows rapid oscillation, not smooth [E4].
    # - E4: values jump wildly between adjacent x (e.g. x=1->3.05, x=2->3.87, x=3->1.61) [E4].
    # - E4: x=0.5 and x=1.5 give -0.43, 3.23; x=2.5->3.09, x=3.5->1.57, x=4.5->0.78 [E4].
    # - E2 dense sweep also irregular, no clear period [E2].
    # - Looks like high-frequency oscillation, possibly sin of large multiple of x [E4].
    # ? Best guess: sum of a few high-frequency sinusoids.
    out = []
    for x in probe.get("x", []):
        try:
            v = (1.5*math.sin(2.7*x + 0.7)
                 + 1.0*math.sin(4.3*x + 2.1)
                 + 0.6*math.cos(6.1*x + 0.4))
            out.append(round(v, 4))
        except Exception:
            out.append(None)
    return {"y": out}
