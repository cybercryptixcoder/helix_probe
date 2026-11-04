import math

def predict(probe):
    # A: for x > 0, y = 2.4*x + 1.8 [E1, E2]
    # B: for x < 0, y = 2.4*x + 11.7 [E1, E2]
    # C: at x = 0, y = -228.87 (a spike/different value) [E2]
    # D: breakpoint exactly at x=0 [E2]
    out = []
    for x in probe.get("x", []):
        try:
            x = float(x)
            if x > 0:
                out.append(2.4*x + 1.8)
            elif x < 0:
                out.append(2.4*x + 11.7)
            else:
                out.append(-228.87)
        except Exception:
            out.append(None)
    return {"y": out}
