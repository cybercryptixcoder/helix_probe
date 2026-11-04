def predict(probe):
    # f(x) = 1.3x^3 + 2.3x^2 - 1.6x - 48.6 outside the flat band [E1-E5,E7,E9]
    # Flat band: constant ~7772.9 (noise) for x in [97.75, 117.75] [E6,E8,E10]
    #   97.7 -> flat, 97.74 -> flat; 97.75 -> cubic [E8,E10]
    #   117.75 -> cubic, 117.76 -> cubic; 117.7 -> flat [E10]
    #   So band is (97.75, 117.75) open? E8: 97.75 flat, 117.75 cubic.
    #   E10: 97.74 flat, 97.76 flat, 97.75 cubic. 117.75 cubic, 117.76 cubic, 117.7 flat.
    #   => band = [97.74, 117.7]? Check E8: 97.75 flat (contradicts). Hmm.
    #   E8 97.75 -> 7772.8627 (flat). E10 97.75 -> 2154047 (cubic). Noise/edge ambiguity.
    #   Best: band is 97.75 <= x < 117.75 with boundary noise; use 97.75..117.75.
    out = []
    for x in probe["x"]:
        if 97.75 <= x < 117.75:
            out.append(7772.95)
        else:
            out.append(1.3*x**3 + 2.3*x**2 - 1.6*x - 48.6)
    return {"y": out}
