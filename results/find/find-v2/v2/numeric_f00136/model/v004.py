import math

def predict(probe):
    # Outer left x<=-14: linear, slope ~ -0.00029 [E2,E4]
    # Outer right x>=26: linear, slope ~ +0.00029 [E4]
    # Middle [-14,26]: smooth curve, piecewise-linear through E4 anchors [E4,E5]
    #   (Lagrange over 10 pts oscillated badly; E5 x=-7.1 -> 0.0381 confirms smooth interp) [E5]
    xs = [-14,-12,-10,-6,-2,2,6,10,14,18,22,26]
    ys = [0.0142,0.0187,0.0249,0.0471,0.0784,-0.0595,-0.0371,-0.0249,-0.0167,-0.0084,-0.0008,0.0014]
    out = []
    for x in probe["x"]:
        try:
            if x <= -14.0:
                y = 0.0142 + (x + 14.0) * (0.0479 - 0.0142) / (-128.0 + 14.0)
            elif x >= 26.0:
                y = 0.0014 + (x - 26.0) * (0.0068 - 0.0014) / 10.0
            else:
                y = None
                for i in range(len(xs)-1):
                    if xs[i] <= x <= xs[i+1]:
                        t = (x - xs[i]) / (xs[i+1] - xs[i])
                        y = ys[i] + t * (ys[i+1] - ys[i])
                        break
                if y is None:
                    y = 0.0
        except Exception:
            y = None
        out.append(y)
    return {"y": out}
