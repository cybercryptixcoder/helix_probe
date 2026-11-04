import math

def predict(probe):
    # Observations are small (~0.05-0.25) and irregular in sign, not odd [E2].
    # f(-x) != -f(x): e.g. f(88.2)=-0.0513 but f(-88.2)=0.0067 [E2].
    # Values look like a bounded oscillatory function of x, roughly in [-0.25, 0.25].
    # Best guess: something like sin(x)/something or a product of trig terms.
    # Try: f(x) = sin(x) * cos(x/3) / something? Hard to pin down.
    # Without more structure, guess a smooth bounded oscillation.
    # Use a small-amplitude sinusoid as placeholder hypothesis.
    out = []
    for x in probe.get("x", []):
        try:
            # ? placeholder: bounded oscillation, amplitude ~0.15
            v = 0.15 * math.sin(x * 0.7) * math.cos(x * 0.13)
        except Exception:
            v = None
        out.append(v)
    return {"y": out}
