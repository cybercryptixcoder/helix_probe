import math

def predict(probe):
    # Structure of f, from the evidence:
    # The function is essentially EVEN: y depends on |x| [E2,E4,E6,E8,E10].
    #   Check: E2 x=-64->0.0288, x=64->0.022 (close); E8 x=-30->0.0191, x=30->0.0035 (not equal!).
    #   Actually NOT symmetric: positive side is lower than negative side in mid/far range.
    #   E8: x=-30->0.0191 vs x=30->0.0035; x=-24->0.0174 vs 24->0.0003; x=-20->0.0162 vs 20->-0.0043
    #   E10: x=-25->0.0177 vs x=25->0.0009; x=-45->0.0233 vs 45->0.0116
    #   So the two sides differ. Positive side has a deeper negative lobe extending further out.
    #
    # Central region |x|<~4.5: positive bump peaking ~0.078 near x=-1.5, crossing zero
    #   near x=-0.35, deep trough ~-0.095 near x=1, rising to ~-0.044 at x=4.5 [E2,E4,E6,E12].
    #   This central structure is roughly symmetric-ish but slightly shifted [E4,E6].
    #
    # Mid negative lobe (positive x): from ~4.5 to ~21, negative, rising almost linearly
    #   toward 0, crossing near x~21.5 [E6,E8,E12]. At x=24 -> 0.0003 [E6].
    #   Slope ~0.0021 per unit (E12: -0.0423 at 4.5 to -0.0023 at 21).
    #
    # Negative x mid-range: at x=-6 -> 0.0471, -8 -> 0.031, -10 -> 0.0249, -12 -> 0.0187,
    #   -16 -> 0.0149, -20 -> 0.0162, -24 -> 0.0174, -30 -> 0.0191 [E8].
    #   So negative side: rises from central, dips to a min ~0.0149 near x=-16, then rises.
    #
    # Far tail |x|>~30: slowly increasing with |x|, roughly linear slope ~0.0003 [E10].
    #   E10: |x|=45->0.0233/0.0116, 50->0.0248/0.0143, 60->0.0277/0.0198, 100->0.0394/0.0415,
    #   120->0.0455/0.0522. Positive side slightly steeper far out; negative side ~0.0003/unit.
    #   Positive side: 45->0.0116, 120->0.0522: slope ~0.00054. Negative: 45->0.0233,120->0.0455: slope ~0.0003.
    #
    # Model: piecewise in x with separate positive/negative branches.
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            x = float(x)
            if x < 0:
                ax = -x
                if ax <= 4.5:
                    # central bump/trough, negative side
                    bump = 0.078 * math.exp(-((x + 1.5) ** 2) / 2.5)
                    trough = -0.095 * math.exp(-((x - 1.0) ** 2) / 3.0)
                    y = bump + trough
                elif ax <= 30.0:
                    # negative-side mid: from ~0.047 at 6, dip to ~0.0149 at 16, rise to 0.0191 at 30
                    # piecewise: at 4.5 ~0.055, 6->0.0471, 8->0.031, 10->0.0249, 12->0.0187,
                    # 16->0.0149, 20->0.0162, 24->0.0174, 30->0.0191
                    if ax <= 16.0:
                        y = 0.0471 + (ax - 6.0) * ((0.0149 - 0.0471) / 10.0)
                    else:
                        y = 0.0149 + (ax - 16.0) * ((0.0191 - 0.0149) / 14.0)
                else:
                    # negative far tail: ~0.0191 at 30, ~0.0233 at 45, ~0.0455 at 120
                    y = 0.0191 + (ax - 30.0) * ((0.0455 - 0.0191) / 90.0)
            else:
                if x <= 4.5:
                    bump = 0.078 * math.exp(-((x + 1.5) ** 2) / 2.5)
                    trough = -0.095 * math.exp(-((x - 1.0) ** 2) / 3.0)
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
