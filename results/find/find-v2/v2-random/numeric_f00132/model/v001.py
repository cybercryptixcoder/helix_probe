def predict(probe):
    # Hypothesis: f(x) is approximately linear through the origin: y ≈ k*x
    # Evidence E1: ratios y/x are nearly constant (~4.76) across all points.
    #   419.9916/88.2 ≈ 4.7618
    #   315.3396/66.0 ≈ 4.7779
    #   -90.9303/-20.3 ≈ 4.4793
    #   -284.9572/-61.7 ≈ 4.6184
    #   17.8834/2.9 ≈ 6.1667  (small x, more relative error)
    #   -109.6768/-24.3 ≈ 4.5134
    #   346.9238/72.7 ≈ 4.7720
    #   -231.9982/-50.4 ≈ 4.6031
    #   -23.9374/-6.0 ≈ 3.9896  (small x)
    #   104.6215/21.3 ≈ 4.9118
    # Best fit slope ~4.7. Small deviations suggest mild nonlinearity/noise.
    # Use least-squares-ish slope from E1: sum(x*y)/sum(x*x).
    k = 4.7
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            ys.append(k * x)
        except Exception:
            ys.append(None)
    return {"y": ys}
