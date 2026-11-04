import math

def predict(probe):
    # Most outputs are ±0.0 [E1-E5]: f is ~0 almost everywhere.
    # A few nonzero spikes appear: 2.2 at x=1.2 [E2], 9.2 at x=-1.6 [E5],
    # 0.0216 at x=-79.1 [E5]. Spikes are near x≈0 and one outlier.
    # Hypothesis (?): f(x) = something like sin/cos scaled, mostly tiny,
    # with occasional larger values. Without more data, model as ~0 with
    # a narrow spike near x=0 region.
    ys = []
    for x in probe["x"]:
        # near-zero region: small nonzero values possible
        if -2.0 <= x <= 2.0:
            # spikes observed at 1.2 -> 2.2 and -1.6 -> 9.2 (?)
            # crude: large near 0, decaying
            ys.append(round(9.2 * math.exp(-((x + 1.6) ** 2) / 0.5) +
                            2.2 * math.exp(-((x - 1.2) ** 2) / 0.5), 4))
        else:
            # mostly zero; occasional tiny spike (e.g. 0.0216 at -79.1) (?)
            ys.append(0.0)
    return {"y": ys}
