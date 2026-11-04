import math

def predict(probe):
    # Beliefs:
    # - For x <= -80: tiny positive value rising slowly with x [E4,E9,E10,E11,E5].
    #   E4: -120->0.0049, -100->0.0059, -80->0.0074. E9: -127.7->0.0046, -79.1->0.0074.
    #   E11: -107.4->0.0055, -100.1->0.0059. E5: -102.2->0.0058.
    #   Linear ramp: v = 0.0049 + (x+120)*(0.0025/40).
    # - For x > -80: outputs are pseudo-random in roughly [-0.25,0.25], no smooth structure [E6,E8,E12].
    #   E12 confirms: -79 -> 0.0074 (still tiny, boundary), -78 onward -> ordinary random.
    #   So boundary is between -79 and -78; use x <= -79 as tiny regime.
    # - No odd symmetry [E2]. No simple magnitude/sign structure [E4].
    # - Deterministic but effectively unpredictable; use a hash-like pseudo-random.
    out = []
    for x in probe.get("x", []):
        try:
            if x <= -79:
                # tiny positive ramp; at -120 ~0.0049, at -79 ~0.0074
                v = 0.0049 + (x + 120) * (0.0025 / 41.0)
            else:
                # pseudo-random bounded in [-0.25, 0.25]
                v = 0.25 * math.sin(x * 12.9898 + 78.233) * math.cos(x * 4.1414)
            out.append(v)
        except Exception:
            out.append(None)
    return {"y": out}
