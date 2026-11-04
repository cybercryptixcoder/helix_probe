import math

def predict(probe):
    # Best guess: f(x) is a noisy sum of low harmonics, roughly centered near 0.5
    # Outputs bounded ~[-3.5, 4.5], irregular, no clean periodicity [E1-E6]
    # No exact trig fits found; treating as sin(x)+sin(2x)+sin(3x)+offset with noise [?]
    out = []
    for x in probe["x"]:
        try:
            v = math.sin(x) + math.sin(2*x) + math.sin(3*x) + 0.5
        except Exception:
            v = None
        out.append(v)
    return {"y": out}
