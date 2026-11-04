import math

def predict(probe):
    # Mechanism inferred from the evidence:
    #
    # Regime A: x < -5
    #   f(x) = -0.7 * floor(x)
    #   [E1,E2,E4,E5,E6,E7,E9] all consistent.
    #
    # Regime B: x >= -5
    #   Sub-region B1 (flat/noisy ~ -402.3): where floor(x) < 18, i.e. x < 18
    #     [E2,E3,E6,E7,E8,E9] show noisy constant ~-402.3 for x in [-5,18).
    #     E8: x=18.0 -> -402.33 (flat), x=18.5 -> -402.29 (flat).
    #     E10: x=18.4 -> -402.2561 (flat), x=18.6 -> -302.4 (slope!).
    #     So the boundary is between 18.4 and 18.6, i.e. floor(x)>=18 -> slope.
    #     floor(18.4)=18 but still flat; floor(18.6)=18 and slope.
    #     So it's not floor-based on 18; boundary is at x=18.5.
    #     Check: 18.4<18.5 flat ✓; 18.6>=18.5 slope ✓; 18.5? untested.
    #     E8: 18.5 -> -402.29 (flat) => boundary is > 18.5.
    #     E10: 18.6 -> slope. So boundary in (18.5, 18.6]. Use 18.5 < x.
    #     Actually E8 x=18.5 flat, E10 x=18.6 slope => boundary at 18.5 (x<=18.5 flat).
    #   Sub-region B2 (slope): x > 18.5
    #     f(x) = -16.8 * floor(x)
    #     [E1,E2,E3,E5,E6,E8,E9,E10] consistent.
    #     E10: 18.6 -> -16.8*18 = -302.4 ✓; 19.0 -> -319.2 ✓.
    #
    #   Boundary B1/B2: x <= 18.5 -> flat; x > 18.5 -> slope.
    #   [E8: 18.5 flat; E10: 18.6 slope]

    x = probe["x"]
    y = []
    for xi in x:
        if xi < -5:
            y.append(-0.7 * math.floor(xi))
        elif xi <= 18.5:
            y.append(-402.3)  # noisy constant; use mean
        else:
            y.append(-16.8 * math.floor(xi))
    return {"y": y}
