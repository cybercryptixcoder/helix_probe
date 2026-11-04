import math

def predict(probe):
    # Outside |x| <= ~7: y = 1.4*x (linear, slope 1.4) [E1: x=-100->70, -80->56, ..., -10->7]
    # Inside |x| < ~7: y is roughly constant ~ -402.3 with small noise [E1: x=-5..5]
    # Boundary: between x=-10 (y=7) and x=-5 (y=-402.3); between x=5 (-402.3) and x=10 (-336)
    #   At x=10, y=-336 = 1.4*10 - 350? No: 1.4*10=14, but observed -336. Hmm.
    #   Actually x=10 -> -336, x=20 -> -336? No: 20->-336? Wait: 20->-336, 40->-672, 60->-1008...
    #   So for x>=10: y = -16.8*x? 10->-168 no. Let's check: 20->-336 => -16.8*20=-336 yes.
    #   40->-672 = -16.8*40 yes. 60->-1008 yes. 80->-1344 yes. 100->-1680 yes. 120->-2016 yes.
    #   And x=10 -> -336? -16.8*10 = -168, but observed -336. So x=10 is special? 
    #   Wait re-read: [...,5,10,20,40,...] -> [...,-402.3176,-402.2789,-336.0,-672.0,...]
    #   So x=5 -> -402.3, x=10 -> -402.2789, x=20 -> -336.0. I misaligned!
    # Correct alignment:
    #   -100:70, -80:56, -60:42, -40:28, -20:14, -10:7, -5:-402.3234, -2:-402.3522,
    #   -1:-402.1495, 0:-402.384, 1:-402.2516, 2:-402.3265, 5:-402.3176, 10:-402.2789,
    #   20:-336.0, 40:-672.0, 60:-1008.0, 80:-1344.0, 100:-1680.0, 120:-2016.0
    # So: |x|<=~10: constant ~-402.3 (noisy). x<=-10: y=1.4*x (x=-10->-14? but observed 7).
    #   Wait -10 -> 7. 1.4*(-10) = -14, not 7. So slope is -0.7? -0.7*-10=7 yes.
    #   Check -20: -0.7*-20=14 yes. -100: 70 yes. So for x<=-10: y = -0.7*x.
    # For x>=20: y = -16.8*x. Check 20->-336 yes.
    # Transition between x=10 (-402.3) and x=20 (-336). Boundary unknown in (10,20).
    # For x<=-10: y=-0.7x. Boundary between -10 (7) and -5 (-402.3). Unknown in (-10,-5).
    # Inside |x|<~10: constant ~-402.3 with noise.
    # Guess boundaries at |x|=10 and |x|=15? Need more data. Use 10 and 15 as guesses.
    # Actually x=-10 gives 7 (linear), x=-5 gives constant. So boundary in (-10,-5].
    # x=10 gives constant, x=20 gives linear. Boundary in [10,20).
    # Symmetric guess: boundary at |x|=15? But -10 is linear side, so boundary > -10. 
    # Let's guess boundary at |x|=12.5? Uncertain. Mark with ?.
    # Noise amplitude ~0.1 on the constant region.
    out = []
    for x in probe.get("x", []):
        try:
            ax = abs(x)
            if ax < 12.5:  # ? boundary guess
                out.append(-402.3)
            elif x <= -12.5:  # ?
                out.append(-0.7 * x)
            else:  # x >= 12.5 ?
                out.append(-16.8 * x)
        except Exception:
            out.append(None)
    return {"y": out}
