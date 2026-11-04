def predict(probe):
    # f(x) = 1.3x^3 + 2.3x^2 - 1.6x - 48.6 everywhere [E1, E2]
    # BUT for x >= ~100, output is clamped/constant ~7772.8 [E3: x=104.5,104.9,103.0 all give ~7772.8]
    # Below that threshold the cubic holds [E3: 123.6, 79.4, 65.5 etc. match cubic]
    # Threshold: 103.0 -> 7772.8 (clamped), 123.6 -> cubic. So clamp region is a band, not x>=100.
    # ? Guess: clamp applies for x in [~100, ~110]? 103 clamped, 104.5/104.9 clamped, 123.6 not.
    # ? Need boundary. Use 100 <= x <= 110 as clamp band, value 7772.8.
    out = []
    for x in probe["x"]:
        if 100.0 <= x <= 110.0:
            out.append(7772.8)
        else:
            out.append(1.3*x**3 + 2.3*x**2 - 1.6*x - 48.6)
    return {"y": out}
