import math

def predict(probe):
    # Mechanism inferred from the evidence:
    #
    # Regime A: x < -5
    #   f(x) = -0.7 * floor(x)   [E1,E2,E4,E5,E6,E7,E9]
    #
    # Regime B: x >= -5
    #   Sub-region B1 (flat/noisy ~ -402.3): x <= 18.5
    #     [E2,E3,E6,E7,E8,E9,E11,E12] noisy constant ~-402.3.
    #     E12: 18.5 -> -402.2476 (flat), 18.51 -> -402.4583 (flat),
    #          18.55 -> -302.4 (slope!). So boundary is in (18.51, 18.55].
    #     E10: 18.4 flat, 18.6 slope. E8: 18.5 flat.
    #     Best guess: boundary at x = 18.5 (x <= 18.5 flat). ?
    #   Sub-region B2 (slope): x > 18.5
    #     f(x) = -16.8 * floor(x)   [E1,E2,E3,E5,E6,E8,E9,E10,E12]
    #     E12: 18.55 -> -16.8*18 = -302.4 ✓; 19.0 -> -319.2 ✓.
    #
    #   Note: E12 shows 18.55 slope but 18.51 flat, so boundary in (18.51,18.55].
    #   Using 18.5 as threshold; 18.51 would be flat under 18.5? No: 18.51>18.5.
    #   To match E12 (18.51 flat, 18.55 slope), use threshold 18.52. ?

    x = probe["x"]
    y = []
    for xi in x:
        if xi < -5:
            y.append(-0.7 * math.floor(xi))
        elif xi <= 18.52:
            y.append(-402.3)
        else:
            y.append(-16.8 * math.floor(xi))
    return {"y": y}
