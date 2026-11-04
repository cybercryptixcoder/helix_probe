def predict(probe):
    # f(x) = x + 17.6 approximately [E1]
    # Check: 88.2->105.8 (+17.6), 66->82.8 (+16.8), -20.3->-28.4 (-8.1)...
    # Hmm, not constant offset. Let's check ratios.
    # 105.8/88.2=1.1995, 82.8/66=1.2545, -28.4/-20.3=1.399, -69.4/-61.7=1.1248
    # Not constant ratio either.
    # Try x + c where c varies... differences: 17.6, 16.8, -8.1, -7.7, 16.9, -8.1, 17.1, -8.0, -8.4, 17.5
    # Differences cluster: ~17.6 for positive x, ~-8 for negative x
    # 88.2->+17.6, 66->+16.8, 2.9->+16.9, 72.7->+17.1, 21.3->+17.5
    # -20.3->-8.1, -61.7->-7.7, -24.3->-8.1, -50.4->-8.0, -6.0->-8.4
    # So: x>0 -> x+17.6ish; x<0 -> x-8ish
    # Actually maybe f(x) = x + 17.6 if x>=0 else x - 8.1
    # Check 2.9: 2.9+17.6=20.5 vs 19.8. Hmm off by 0.7.
    # 21.3+17.6=38.9 vs 38.8. Good.
    # 88.2+17.6=105.8. Exact.
    # 66+17.6=83.6 vs 82.8. Off 0.8.
    # Maybe noisy. Or maybe f(x)=x+17.6 for x>0, but small x different?
    # Let's try: for x>=0: x+17.6; for x<0: x-8.1
    # -6.0-8.1=-14.1 vs -14.4. Off 0.3.
    # -20.3-8.1=-28.4. Exact.
    # -24.3-8.1=-32.4. Exact.
    # -50.4-8.1=-58.5 vs -58.4. Off 0.1.
    # -61.7-8.1=-69.8 vs -69.4. Off 0.4.
    # Reasonable. Maybe noise.
    # Alternative: maybe f(x) = x + 17.6 for x>=0, x - 8.1 for x<0
    # Or maybe it's x + sign-dependent constant.
    # Let's just use piecewise.
    out = []
    for x in probe["x"]:
        if x >= 0:
            out.append(x + 17.6)
        else:
            out.append(x - 8.1)
    return {"y": out}
