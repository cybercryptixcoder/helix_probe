def predict(probe):
    # Piecewise linear in x, with a kink near x=0.
    # For x <= 0: slope = (2894.5846-3311.7317)/16 = -26.0717 per unit [E1]
    #   check: at x=0, 3311.7317 + 128*26.0717 = 3311.7317+3337.18 = 6648.9? no.
    # Let's fit: y(-128)=3311.7317, y(0)=106.0528 -> slope = (106.0528-3311.7317)/128 = -25.0444
    #   check x=-16: 106.0528 + 16*25.0444 = 506.76 vs 391.702. Not linear across whole range.
    # Fit left segment from -128..-16: slope = (391.702-3311.7317)/112 = -26.0717
    #   intercept at 0: 391.702 + 16*26.0717 = 808.85. But y(0)=106.05. So kink between -16 and 0.
    # Right side: y(16)=1888.8978, y(128)=14368.8129 -> slope=(14368.8129-1888.8978)/112=111.427
    #   intercept at 0: 1888.8978 - 16*111.427 = 106.06. Matches y(0)=106.05!
    # So for x>=0: y = 106.0528 + 111.427*x  (check x=64: 106.05+7131.3=7237.4 ✓)
    # Left: y = 808.85 - 26.0717*x for x<=-16 (check x=-128: 808.85+3337.2=4146? no)
    #   recompute: y(-128)=3311.73, slope -26.0717 -> intercept = 3311.73 - 128*26.0717 = 3311.73-3337.18=-25.45
    #   y = -25.45 - 26.0717*x? at x=-128: -25.45+3337.18=3311.73 ✓; at x=-16: -25.45+417.15=391.7 ✓
    #   at x=0: -25.45. But y(0)=106.05. So there's a transition between -16 and 0.
    # Middle: y(-16)=391.702, y(0)=106.0528 -> slope=(106.0528-391.702)/16=-17.8656
    #   y = 106.0528 - 17.8656*x for -16<=x<=0 (check x=-16: 106.05+285.85=391.9 ✓)
    # Right for x>=0: y = 106.0528 + 111.427*x
    # Check x=120: 106.05+13371.24=13477.3 ✓; x=126: 106.05+14039.8=14145.9 ✓
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            x = float(x)
            if x >= 0:
                y = 106.0528 + 111.427 * x
            elif x >= -16:
                y = 106.0528 - 17.8656 * x
            else:
                y = -25.45 - 26.0717 * x
        except Exception:
            y = None
        ys.append(y)
    return {"y": ys}
