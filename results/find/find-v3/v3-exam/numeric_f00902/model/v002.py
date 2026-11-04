def predict(probe):
    # f(x) = 1.3x^3 + 2.3x^2 - 1.6x - 48.6 for |x| < ~100 [E1, E2]
    # For x >= ~100 (and x <= -100?), output is clipped/constant ~7772.86 [E3]
    # E3: x=104.5 -> 7772.8597, x=104.9 -> 7772.8975, x=103.0 -> 7773.005
    # These are NOT constant but close. Let's check: cubic at 103 = 1.3*1092727+2.3*10609-164.8-48.6
    # = 1420545.1+24400.7-213.4 = 1444732.4 (matches v1 prediction). But actual ~7773.
    # So there's a regime change near x~100. Values ~7773 are tiny.
    # At 104.5, 104.9, 103.0 all give ~7772.86-7773.0. Slight variation.
    # Maybe it's a different function in this region. Let's look:
    # 103.0 -> 7773.005
    # 104.5 -> 7772.8597
    # 104.9 -> 7772.8975
    # Not monotonic clearly. Hmm 104.9 > 104.5 in x but 7772.8975 > 7772.8597.
    # 103.0 -> 7773.005 (highest). 
    # Maybe it's sin or something? Or maybe x mod something?
    # 103, 104.5, 104.9. Differences: 1.5, 0.4.
    # y diffs: 7772.8597-7773.005=-0.1453 (for +1.5); 7772.8975-7772.8597=0.0378 (for +0.4)
    # slope ~ -0.0969 and +0.0945. Roughly ±0.1. Could be oscillation.
    # 123.6 -> 2489592.5808 which IS the cubic value! Check: 123.6^3=1888... let's verify
    # 123.6^2=15276.96, ^3=1888232.256
    # 1.3*1888232.256=2454701.93, 2.3*15276.96=35137.0, -1.6*123.6=-197.76
    # sum=2454701.93+35137.0-197.76-48.6=2489592.57 YES matches!
    # So 123.6 gives cubic, but 103-104.9 give ~7773. Weird!
    # 79.4 -> 665060.4272: cubic? 79.4^2=6304.36, ^3=500566.184
    # 1.3*500566.184=650736.04, 2.3*6304.36=14500.03, -127.04-48.6
    # =650736.04+14500.03-175.64=665060.43 YES cubic.
    # So 79.4 cubic, 103-104.9 NOT cubic, 123.6 cubic again.
    # This suggests a narrow regime change around x in [~100, ~110]?
    # Let's check: 104.5, 104.9, 103.0 all in that band. 123.6 outside.
    # What about negative side? -55.8, -63.9 are cubic (matches).
    # So there's an interval around x~100-110 where f behaves differently.
    # Values ~7773. Let's see if it's a constant plus small variation.
    # 7773.005, 7772.8597, 7772.8975. Mean ~7772.92, spread ~0.15.
    # Could be 7773 - something small. Or maybe it's a different polynomial.
    # With only 3 points in the band, hard to fit. Let's guess it's roughly constant ~7772.9.
    # But wait - maybe it's a periodic thing. 103, 104.5, 104.9.
    # Actually maybe the function is x^3 mod something? No.
    # Let's think: maybe the regime is [100, 110] and value is ~7773.
    # Or maybe it's a "clipping" to some range? But 123.6 is huge, so no.
    # Best guess: there's an interval around [100,110] where f is ~7773 (roughly constant).
    # Need boundaries. 79.4 cubic, 103 not, 123.6 cubic. So boundary between 79.4 and 103, and between 104.9 and 123.6.
    # Let's guess [100, 110]. Mark with "?".
    def cubic(x):
        return 1.3*x**3 + 2.3*x**2 - 1.6*x - 48.6
    def f(x):
        # ? regime change interval around [100, 110] where value ~7773
        if 100 <= x <= 110:
            # rough: values 7773.005 at 103, 7772.86 at 104.5, 7772.90 at 104.9
            # fit linear? slope between 103 and 104.5: -0.0969
            # between 104.5 and 104.9: +0.0945
            # not linear. Just use ~7772.9 constant, or slight model.
            # Try: maybe it's cubic but with different coefficients? 
            # With 3 points can't fit cubic. Use average ~7772.92.
            return 7772.92
        return cubic(x)
    return {"y": [f(x) for x in probe["x"]]}
