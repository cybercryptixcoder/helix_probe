def predict(probe):
    # For x >= 0: y = 8 - 9.6*x  [E2: x=0->8, 5->-40, 10->-88, 120->-1144]
    # For x < 0: y ≈ 8 plus small noise (roughly constant ~8)  [E2: -100..-10 all ~8.0-8.15]
    # Exception: x=-5 gave 56.0, x=-120 gave 7.9942 — but E1 shows -20.3->7.99, -24.3->8.06, -50.4->7.86, -6.0->65.6
    #   Hmm: -6.0 -> 65.6 and -5 -> 56.0. And E1: 2.9->-19.84 (matches 8-9.6*2.9=-19.84), 21.3->-196.48 (8-9.6*21.3=-196.48)
    #   E1: 66.0->-625.6 (8-9.6*66=-625.6), 88.2->-838.72 (8-9.6*88.2=-838.72), 72.7->-689.92 (8-9.6*72.7=-689.92)
    #   So x>=0 rule is exact: y = 8 - 9.6*x
    # For x<0: mostly ~8, but -5->56, -6->65.6. Check: 8-9.6*(-5)=56, 8-9.6*(-6)=65.6!
    #   So the linear rule y=8-9.6x applies for x in [-6, ...]? But -10->8.03, -20->8.1...
    #   Wait: -5 and -6 follow linear, but -10 and below give ~8. So there's a region.
    #   E1: -20.3->7.99, -24.3->8.06, -50.4->7.86, -61.7->7.915 — all ~8.
    #   So: for x in [-6, 0): linear y=8-9.6x. For x < -6: y≈8 (with noise).
    #   Boundary between -6 and -10. Test: -6 linear, -10 constant. Boundary in (-10,-6].
    #   The noise ~8 suggests maybe a floor/clamp at 8? For x<-6, y=8+noise.
    #   Actually maybe rule: y = 8 - 9.6*x, but clamped below at 8? No, for x<-6, 8-9.6x > 8 (e.g. -10->104). Not clamp.
    #   Likely: for x < -6 (or some threshold), y = 8 (constant, noisy). For x >= threshold, y=8-9.6x.
    #   Threshold: -6 gives 65.6 (linear), -10 gives 8.03 (constant). Guess threshold at -6? But -6 is linear.
    #   Maybe threshold is x >= -6? Then -6 linear, -10 constant. But need boundary. Could be -6 exactly, or between.
    #   E2 -5->56 linear. So region x>=-6 linear. Let's guess boundary at -6.
    #   But wait, is it really constant 8 for x<-6, or is it 8-9.6x clamped to max 8? For x=-10, 8-9.6*(-10)=104, but observed 8.03. So it's not the linear formula. It's ~8.
    #   Could be: y = 8 - 9.6*x if x >= -6 else 8 (with noise).
    #   Actually maybe it's min(8-9.6x, something)? No.
    #   Alternative: for x<-6, y = 8 + noise. Let's model as 8.
    #   Hmm but why 8? Maybe it's 8-9.6*x but with x replaced by max(x,-6)? i.e. clamp x at -6: y=8-9.6*max(x,-6).
    #   Check x=-10: max(-10,-6)=-6 -> 8-9.6*(-6)=65.6. But observed 8.03. No.
    #   So constant 8 for x<-6.
    #   Let me reconsider: maybe threshold is different. -6 linear (65.6), -10 constant (8.03). Boundary in (-10,-6].
    #   I'll guess threshold at -6: x >= -6 linear, x < -6 constant 8.
    #   But E2 -5->56 = 8-9.6*(-5)=56 ✓. -6 not tested directly in E2, but E1 -6.0->65.6=8-9.6*(-6) ✓.
    #   So x>=-6: y=8-9.6x. x<-6: y=8.
    #   Noise: small values ~8.0-8.15, so add nothing or tiny. I'll output 8 for constant region.
    #   Actually the constant region values: 8.1549,8.032,8.0963,8.0406,8.0646,8.1059,8.0335,7.9942,7.99,8.06,7.86,7.915. Mean ~8.03, noisy. Predict 8.
    out = []
    for x in probe.get("x", []):
        try:
            if x >= -6:
                out.append(8 - 9.6 * x)
            else:
                out.append(8.0)
        except Exception:
            out.append(None)
    return {"y": out}
