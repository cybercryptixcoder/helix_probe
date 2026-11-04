def predict(probe):
    # Far-left branch: y = -25.45 - 26.0717*x for x <= -1.5 [E1, E2, E3]
    #   check x=-1.5: 13.66 ✓; x=-1.6: 16.27 ✓; x=-1.9: 24.09 ✓ [E6]
    # Region -1.5..-1: slope -13.62, y=6.8494-13.62*(x+1) [E3, E6]
    #   check x=-1.1: 6.8494-13.62*0.1=5.49? observed 6.436. Not quite.
    #   E6: -1.5->-1.45: (12.3588-14.966)/0.05=-52.1; -1.45->-1.4: (11.2441-12.3588)/0.05=-22.3
    #   -1.4->-1.3: (9.0565-11.2441)/0.1=-21.88; -1.3->-1.2: (7.4701-9.0565)/0.1=-15.86
    #   -1.2->-1.1: (6.436-7.4701)/0.1=-10.34; -1.1->-0.9: (10.6298-6.436)/0.2=+20.97
    #   So slope varies smoothly: it's a smooth curve, not piecewise linear! [E6]
    # Region -1..-0.5: E6 -0.9->-0.8: (18.223-10.6298)/0.1=75.9; -0.8->-0.7: 98.4; -0.7->-0.6: 111.3
    #   -0.6->-0.55: 111.4; -0.55->-0.45: 111.4; so slope saturates at 111.427 near x=-0.65
    # Right branch: y = 106.0528 + 111.427*x for x >= ~-0.65 [E3,E4,E5,E6]
    #   check x=0: 106.0528 ✓; x=-0.45: 55.91 ✓; x=-0.55: 44.77 ✓
    #   x=-0.6: 106.0528-66.86=39.19 ✓; x=-0.7: 106.0528-77.99=28.06 ✓
    #   x=-0.8: 106.0528-89.14=16.91? observed 18.223. Off by 1.3.
    #   x=-0.9: 106.0528-100.28=5.77? observed 10.63. So curve below ~-0.65.
    # The near-zero region is a smooth curve (MLP), transitioning between branches.
    # Model: far-left linear, right linear, smooth blend in between via a curve.
    # Fit the curve region -1.5..-0.65 with a smooth interpolation.
    # Use a cubic-ish blend. Known points (x,y):
    #   -1.5:13.6624, -1.4:11.2441, -1.3:9.0565, -1.2:7.4701, -1.1:6.436,
    #   -1.0:6.8494, -0.9:10.6298, -0.8:18.223, -0.7:28.0616, -0.65:~33.6
    # Minimum near x=-1.1 (y=6.436). Looks like a smooth valley.
    # Try: y = a + b*(x-x0)^2 near minimum? x0=-1.1, y0=6.436.
    #   x=-1.0: 6.436+b*0.01=6.8494 -> b=41.3
    #   x=-1.2: 6.436+b*0.01=7.4701 -> b=103.4. Not constant, so not simple parabola.
    # Better: interpolate through the E6 points with a smooth spline-like fit.
    # Use piecewise linear through E6 points for the curve region (dense enough).
    # Curve points (x,y) from E6:
    curve = [
        (-1.5, 14.966), (-1.45, 12.3588), (-1.4, 11.2441), (-1.3, 9.0565),
        (-1.2, 7.4701), (-1.1, 6.436), (-0.9, 10.6298), (-0.8, 18.223),
        (-0.7, 28.0616), (-0.6, 39.1961), (-0.55, 44.7675), (-0.45, 55.9102),
    ]
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            x = float(x)
            if x <= -1.5:
                y = -25.45 - 26.0717 * x
            elif x >= -0.45:
                y = 106.0528 + 111.427 * x
            else:
                # linear interpolation through curve points
                y = None
                for i in range(len(curve) - 1):
                    x0, y0 = curve[i]
                    x1, y1 = curve[i + 1]
                    if x0 <= x <= x1:
                        t = (x - x0) / (x1 - x0)
                        y = y0 + t * (y1 - y0)
                        break
                if y is None:
                    y = 106.0528 + 111.427 * x
        except Exception:
            y = None
        ys.append(y)
    return {"y": ys}
