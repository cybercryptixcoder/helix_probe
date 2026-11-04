import math

def predict(probe):
    # Beliefs about f, from the evidence:
    # The function is a smooth function of x with a central structure near 0 and
    # a slowly-varying tail. It is NOT even: negative and positive sides differ.
    #
    # Central structure (|x| < ~5) [E2,E4,E6,E14]:
    #   Positive bump: plateau ~0.078 for x in [-3,-1], peak ~0.0784 near x=-2,
    #     falls to 0.049 at x=-0.5, 0.0229 at -0.25, crosses zero near x=-0.05,
    #     then goes negative. [E14]
    #   Negative trough: minimum ~-0.0951 at x=1.0, rising to -0.0782 at 1.5,
    #     -0.0595 at 2, -0.0507 at 2.5, -0.0466 at 3, -0.0438 at 4, -0.0423 at 4.5. [E14,E6,E12]
    #   So the central shape is asymmetric: bump peak near x=-2, trough near x=1.
    #
    # Mid positive side (4.5 < x < ~21) [E12,E8]:
    #   Smooth monotone rise from -0.0423 at 4.5 to ~0 near x=21.5.
    #   E12: 4.5->-0.0423, 6->-0.0371, 8->-0.03, 10->-0.0249, 12->-0.0208,
    #        14->-0.0167, 16->-0.0126, 18->-0.0084, 19->-0.0064, 21->-0.0023.
    #   Slope ~0.0021/unit, nearly linear. Zero crossing ~21.5.
    #
    # Mid negative side (4.5 < |x| < ~30) [E8]:
    #   x=-6->0.0471, -8->0.031, -10->0.0249, -12->0.0187, -16->0.0149,
    #   -20->0.0162, -24->0.0174, -30->0.0191. Dips to min ~0.0149 near |x|=16.
    #
    # Far tail |x| > ~30 [E10]:
    #   Negative side: 45->0.0233, 50->0.0248, 60->0.0277, 100->0.0394, 120->0.0455.
    #     Slope ~0.0003/unit, smooth monotone.
    #   Positive side: 45->0.0116, 50->0.0143, 60->0.0198, 100->0.0415, 120->0.0522.
    #     Slope ~0.00054/unit, smooth monotone.
    #   At x=25 positive side -> 0.0009; at x=-25 -> 0.0177 [E10].
    #
    # Positive side near 21-30 [E13,E8]: 22.4->-0.0005, 24->0.0003, 24.6->0.0006,
    #   26.4->0.0016, 30->0.0035. Smooth rise.
    #
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            x = float(x)
            if x < 0:
                ax = -x
                if ax <= 4.5:
                    # negative side central: bump peak near x=-2, trough near x=1
                    # use two gaussians; bump centered -2, trough centered 1
                    bump = 0.0784 * math.exp(-((x + 2.0) ** 2) / 3.0)
                    trough = -0.0951 * math.exp(-((x - 1.0) ** 2) / 2.0)
                    y = bump + trough
                elif ax <= 30.0:
                    # negative-side mid: 6->0.0471, dip to 0.0149 at 16, rise to 0.0191 at 30
                    if ax <= 16.0:
                        y = 0.0471 + (ax - 6.0) * ((0.0149 - 0.0471) / 10.0)
                    else:
                        y = 0.0149 + (ax - 16.0) * ((0.0191 - 0.0149) / 14.0)
                else:
                    # negative far tail: 30->0.0191, 45->0.0233, 120->0.0455
                    y = 0.0191 + (ax - 30.0) * ((0.0455 - 0.0191) / 90.0)
            else:
                if x <= 4.5:
                    bump = 0.0784 * math.exp(-((x + 2.0) ** 2) / 3.0)
                    trough = -0.0951 * math.exp(-((x - 1.0) ** 2) / 2.0)
                    y = bump + trough
                elif x <= 21.5:
                    # positive mid: -0.0423 at 4.5 rising to ~0 at 21.5
                    y = -0.0423 + (x - 4.5) * (0.0423 / 17.0)
                elif x <= 30.0:
                    # positive side: 24->0.0003, 30->0.0035
                    y = 0.0003 + (x - 24.0) * ((0.0035 - 0.0003) / 6.0)
                else:
                    # positive far tail: 45->0.0116, 120->0.0522
                    y = 0.0035 + (x - 30.0) * ((0.0522 - 0.0035) / 90.0)
        except Exception:
            y = None
        ys.append(y)
    return {"y": ys}
