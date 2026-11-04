def predict(probe):
    # f(x) = 1.3x^3 + 2.3x^2 - 1.6x - 48.6 everywhere except a flat band.
    # Flat band: constant ~7772.9 (noisy) for x in [97.75, 117.75).
    #   Left edge: E22 shows 97.745 cubic, 97.75 flat => edge at 97.75 (flat at/above).
    #   Right edge: E24 shows 117.75 cubic, 117.751 cubic, ... 117.8 cubic => NO flat band on right side here!
    #   Wait: E24 all cubic up to 118.0. E20 also cubic from 117.755 up. E12/E10 had flat at 117.75-117.78.
    #   Conflict: E10/E12 show flat at 117.7-117.78; E20/E24 show cubic there.
    #   E20 and E24 are the latest and densest => trust them: right edge is NOT at 117.75.
    #   But E4/E6 show flat at 100-115. So flat band exists on left, ends somewhere.
    #   E12: 117.7 cubic, 117.72 cubic, 117.74 cubic, 117.75 cubic(2154047), 117.76 cubic, 117.78 cubic.
    #   Actually E12 observed: 117.7=2151317(cubic), 117.75=2154047(cubic), 117.76=2154593(cubic), 117.78=2155685(cubic).
    #   So E12 is ALL cubic on right side too! The flat is only 97.75..~115?
    #   E12: 100,105,110,115 flat; 116.5 flat (7772.8215); 117.0 cubic(1207911.8).
    #   E6: 116 flat, 118 cubic. E4: 115 flat, 120 cubic.
    #   Right edge between 116.5 and 117.0. E12: 116.5 flat, 117.0 cubic => edge in (116.5,117.0].
    #   E8: 116.75? E8 has 116.75 -> check: E8 x includes 116.75, 117.25. 
    #   Need edge: test says between 116.5 and 117.0. Use 117.0? E12 117.0 cubic. 
    #   E16/E14 confirm left edge 97.75.
    # Left edge: 97.75 flat (E22: 97.75=7772.8575 flat). 97.745 cubic (E22: 7772.952? no that's flat-ish).
    #   E22: 97.745=7772.952 (flat!), 97.75=7772.8575 flat. So left edge <= 97.745.
    #   E16: 97.5 cubic, 97.55 flat => edge in (97.5,97.55]. 
    #   E14: 97.68 flat. So edge <= 97.68.
    #   E16 says 97.55 flat, 97.5 cubic => edge in (97.5, 97.55].
    #   Use 97.55.
    # Right edge: between 116.5 (flat) and 117.0 (cubic). E8 has 116.75.
    out = []
    for x in probe["x"]:
        if 97.55 <= x < 117.0:
            out.append(7772.95)
        else:
            out.append(1.3*x**3 + 2.3*x**2 - 1.6*x - 48.6)
    return {"y": out}
