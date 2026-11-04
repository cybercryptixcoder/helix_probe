import math

def predict(probe):
    # Beliefs:
    # - Outputs are bounded roughly [-0.25, 0.25] for |x|<~80 [E1-E11].
    # - For |x|>=~80 outputs are tiny positive ~0.005, slowly rising with |x| [E4,E9,E10,E11].
    #   E4: -120..-80 -> 0.0049,0.0059,0.0074 ; E10 same; E9 -127.7->0.0046, 94.1->0.0809? no.
    #   Actually E9 x=94.1 -> 0.0809 (NOT tiny!). So plateau is NOT simply |x|>=80.
    # - Re-examine: E11 x=110.8 -> 0.1788 (not tiny), x=-107.4->0.0055, x=-100.1->0.0059.
    #   E5 x=102.1->0.1053, x=-102.2->0.0058, x=105.7->-0.1217, x=119.5->-0.0634.
    #   E3 x=104.5->0.1586, 104.9->-0.0552, 123.6->-0.0437, 103.0->-0.1567.
    #   So large |x| is NOT a plateau. Only very negative x (<=~-80) gives ~0.005.
    # - Check: E4 -120,-100,-80 -> 0.0049,0.0059,0.0074. E10 -120..-80 same.
    #   E9 -127.7->0.0046, -79.1->0.0074. E11 -107.4->0.0055, -100.1->0.0059.
    #   E5 -102.2->0.0058. So x <= -80 gives tiny ~0.005 rising with x.
    #   But E4 x=-60 -> 0.0288 (not tiny). So boundary near -80.
    # - For x > -80: outputs look pseudo-random in [-0.25,0.25], no smooth structure [E6,E8].
    #   Nearby integers give uncorrelated values [E8].
    # - No odd symmetry [E2]. No simple magnitude/sign structure [E4].
    # Best model: deterministic pseudo-random for x>-80; tiny ramp for x<=-80.
    out = []
    for x in probe.get("x", []):
        try:
            if x <= -80:
                # tiny positive, rises with x: at -120 ~0.0049, at -80 ~0.0074
                v = 0.0049 + (x + 120) * (0.0025 / 40.0)
            else:
                # pseudo-random bounded in [-0.25, 0.25]
                v = 0.25 * math.sin(x * 12.9898 + 78.233) * math.cos(x * 4.1414)
            out.append(v)
        except Exception:
            out.append(None)
    return {"y": out}
