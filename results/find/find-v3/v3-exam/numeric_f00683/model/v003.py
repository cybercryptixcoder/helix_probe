import math

def predict(probe):
    # Model of the black box f(x).
    #
    # Positive branch (x > 0): f(x) = 13.1*x - 5, essentially linear.
    #   [E4,E6,E7,E9] large positives match to ~1.
    #   Small positives: E8 shows f(0.05)=-2.845, f(0.15)=-0.535, f(0.3)=-0.57,
    #   f(0.6)=3.36, f(0.9)=6.29, f(1.1)=11.91, f(1.3)=12.53, f(1.7)=16.77.
    #   Line 13.1x-5: -4.35,-3.04,-1.07,2.86,6.79,9.41,12.03,17.27.
    #   Deviations are small/noisy; keep linear.
    #
    # Negative branch: NOT a single line. There is a kink near x=-3.
    #   For x <= -3: slope ~1.3, intercept ~ -10.5.
    #     E10: (-3.2,-15.092),(-3.5,-14.485),(-4.5,-15.795),(-6,-17.76),
    #     (-9,-21.69),(-12,-26.62),(-18,-34.48),(-22,-38.72),(-28,-45.58),
    #     (-32,-51.82). Slope from -9 to -32: (51.82-21.69)/23=1.31.
    #     Intercept: 1.31*(-32)+c=-51.82 -> c=-9.9. So ~1.31x-9.9.
    #     Check -18: 1.31*-18-9.9=-33.48 vs -34.48 (off 1). -22: -38.72 vs -38.72 yes.
    #     -12: -25.62 vs -26.62 (off 1). -6: -17.76 vs -17.76 yes.
    #     -4.5: -15.795 vs -15.795 yes. -3.5: -14.485 vs -14.485 yes.
    #     -3.2: -14.092 vs -15.092 (off 1). Hmm mixed. Use slope 1.31, c=-9.9.
    #
    #   For -3 < x < 0: a different, flatter, noisy regime.
    #     E10: (-2.8,-14.568),(-2.2,-12.782),(-0.9,-11.079),(-0.7,-11.817),
    #     (-0.6,-11.686),(-0.4,-11.424),(-0.2,-7.162),(-0.05,-10.9655),
    #     (-0.02,-9.9262),(-0.01,-7.9131).
    #     E8: (-2.5,-12.175),(-2.0,-11.52),(-1.8,-12.258),(-1.5,-11.865),
    #     (-1.2,-11.472),(-1.0,-11.21),(-0.8,-11.948),(-0.5,-10.555),
    #     (-0.3,-11.293),(-0.1,-11.031).
    #     These hover around -11 to -12 with noise, no clear trend.
    #     E2: f(-2)=-11.52, f(-1)=-8.21 (noisy).
    #     Model as roughly constant ~ -11.4 in this region (noisy).
    #
    #   At x=0 exactly: E2 f(0)=-382.12 (isolated spike).
    #
    #   For x in [-3,0): use ~ -11.4 (flat, noisy). Boundary at -3.
    #   Actually E10 -2.8=-14.568 is closer to the line 1.31*-2.8-9.9=-13.57.
    #   And -2.2=-12.782 vs line -12.78 yes! So maybe kink is at -2, not -3.
    #   Check -2.0 (E8): -11.52 vs line -12.52 (off 1). -1.8: -12.258 vs -12.26 yes.
    #   -1.5: -11.865 vs -11.865 yes! -1.2: -11.472 vs -11.472 yes!
    #   -1.0: -11.21 vs -11.21 yes! -0.9: -11.079 vs -11.079 yes!
    #   -0.8: -11.948 vs -10.948 (off 1). -0.7: -11.817 vs -10.817 (off 1).
    #   -0.6: -11.686 vs -10.686 (off 1). -0.5: -10.555 vs -10.555 yes!
    #   -0.4: -11.424 vs -10.424 (off 1). -0.3: -11.293 vs -10.293 (off 1).
    #   -0.2: -7.162 vs -10.162 (off 3). -0.1: -11.031 vs -10.031 (off 1).
    #   -0.05: -10.9655 vs -9.9655 (off 1). -0.02: -9.9262 vs -9.9262 yes!
    #   -0.01: -7.9131 vs -9.9131 (off 2).
    #   So the line 1.31x-9.9 fits MANY points exactly, with occasional +-1 noise.
    #   The "flat region" was an illusion from noise. The kink near -2 to -3:
    #   -2.5: -12.175 vs line -13.175 (off 1). -2.8: -14.568 vs -13.568 (off 1).
    #   -3.2: -15.092 vs -14.092 (off 1). -3.5: -14.485 vs -14.485 yes.
    #   So actually the SAME line 1.31x-9.9 fits nearly everywhere with +-1 noise!
    #   Let me recheck large negatives with 1.31x-9.9:
    #   -32: -51.82 vs -51.82 yes. -28: -46.58 vs -45.58 (off 1).
    #   -22: -38.72 vs -38.72 yes. -18: -33.48 vs -34.48 (off 1).
    #   -12: -25.62 vs -26.62 (off 1). -9: -21.69 vs -21.69 yes.
    #   -6: -17.76 vs -17.76 yes. -4.5: -15.795 vs -15.795 yes.
    #   So slope 1.31, intercept -9.9 works with +-1 noise everywhere.
    #   The +-1 pattern looks like rounding/noise. Good enough.
    #
    # So: negative branch f(x) = 1.31*x - 9.9 for x < 0 (with noise ~+-1).
    # Positive branch f(x) = 13.1*x - 5 for x > 0.
    # Spike at x=0: -382.12.

    def f(x):
        if x > 0:
            return 13.1 * x - 5.0
        elif x < 0:
            return 1.31 * x - 9.9
        else:
            return -382.12

    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            if x is None:
                ys.append(None)
            else:
                ys.append(f(float(x)))
        except Exception:
            ys.append(None)
    return {"y": ys}
