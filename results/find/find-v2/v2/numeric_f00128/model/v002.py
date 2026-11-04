import math

def predict(probe):
    # Model: f(x) is smooth, odd-symmetric, with a piecewise-linear-ish structure.
    # E2 shows near-perfect odd symmetry: f(-x) = -f(x) [E2].
    # For |x| >= 10: f(x) is linear in x with slope ~ -16.76 (per unit x):
    #   f(10)=-157.8, f(80)=-1340.8 -> slope = (-1340.8+157.8)/(80-10) = -16.9
    #   f(-10)=69.99, f(-80)=543.2 -> slope = (543.2-69.99)/(-80+10) = -6.76... 
    # Wait: check odd symmetry: f(-10)=69.99 vs -f(10)=157.8. NOT odd at 10!
    # Actually f(-10)=69.99, f(10)=-157.8. So f(-x) != -f(x) exactly.
    # But f(-80)=543.2, f(80)=-1340.8: ratio -0.405. Hmm.
    # Let's fit: for x>0: y = -16.76*x + 9.6 (from 10->-157.8, 80->-1340.8)
    #   slope=(-1340.8-(-157.8))/(80-10)=-1183/70=-16.9; intercept=-157.8+169=11.2
    # For x<0: f(-10)=69.99, f(-80)=543.2: slope=(543.2-69.99)/(-70)=-6.76; 
    #   intercept at x=-10: 69.99-(-6.76*-10)=69.99-67.6=2.4
    # So different slopes for positive vs negative x. Not odd.
    # Small x: f(1)=-5.32, f(5)=-73.29, f(-1)=9.35, f(-5)=36.19.
    #   For x in [1,5]: slope ~ (-73.29+5.32)/4 = -17.0; intercept ~ 11.7
    #   For x in [-5,-1]: slope ~ (36.19-9.35)/4 = 6.71; intercept ~ 16.06
    # So positive side: y ~ -16.9x + 11; negative side: y ~ 6.7x + 16 (approx).
    # Check E1: f(88.2)=-1479.4 -> -16.9*88.2+11=-1479.6 ✓
    #   f(66)=-1104.2 -> -16.9*66+11=-1104.4 ✓
    #   f(-61.7)=419.5 -> 6.7*-61.7+16=-397.4... no, 6.7*-61.7=-413.4+16=-397.4, but observed 419.5.
    # Hmm sign. Let me redo negative side: f(-10)=69.99, f(-80)=543.2.
    #   slope=(543.2-69.99)/(-80-(-10))=473.2/-70=-6.76
    #   y = -6.76x + b; at x=-10: 69.99=67.6+b -> b=2.4
    #   f(-61.7) = -6.76*-61.7+2.4 = 417.1+2.4=419.5 ✓ 
    #   f(-50.4) = 340.7+2.4=343.1 ✓
    #   f(-20.3) = 137.2+2.4=139.6 ✓
    #   f(-24.3) = 164.3+2.4=166.7 ✓
    #   f(-6) = 40.6+2.4=43.0 ✓
    #   f(-1) = 6.76+2.4=9.16 vs 9.35 (close)
    #   f(-5) = 33.8+2.4=36.2 ✓
    # Positive side: f(10)=-157.8, f(80)=-1340.8: slope=-16.9, b=11.2
    #   f(2.9) = -49.0+11.2=-37.8 ✓
    #   f(21.3) = -360+11.2=-348.8 ✓
    #   f(1) = -16.9+11.2=-5.7 vs -5.32 (close)
    #   f(5) = -84.5+11.2=-73.3 ✓
    # So: two linear regimes, one for x>0 (slope -16.9, intercept 11.2),
    #     one for x<0 (slope -6.76, intercept 2.4).
    # At x=0? Extrapolate: pos gives 11.2, neg gives 2.4. Discontinuity?
    # Likely there's a transition region near 0. But data at x=1 and x=-1 fit lines.
    # Best guess: piecewise linear with a break at x=0 (jump from 2.4 to 11.2).
    # ? Could be smooth transition; but linear fits are excellent.
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            x = float(x)
            if x >= 0:
                y = -16.9*x + 11.2
            else:
                y = -6.76*x + 2.4
            ys.append(y)
        except Exception:
            ys.append(None)
    return {"y": ys}
