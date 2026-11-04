def predict(probe):
    # Model: y = max(floor, g(x)) where g is a smooth function, floor = -84.3663.
    # Floor region: |x| small -> -84.3663 [E1,E2,E3,E4,E5,E6]
    # Outside floor, y grows steeply. Let's fit g(x) = A*x^2 + B*x + C on large-|x| points.
    # Use all non-floor points from E1-E6 to fit quadratic by least squares.
    # Points (x,y):
    # E1: (88.2,104398.3),(66,21806.0),(-61.7,34659.9),(72.7,44545.8)
    # E2: (104.5,167339.9),(65.5,20347.3),(-63.9,44316.4),(104.9,168884.5),(123.6,241093.6),(79.4,70417.5),(103.0,161547.7),(-55.8,11784.3)
    # E3: (58.8,5395.5),(102.1,158072.4),(-102.2,212952.0),(105.7,171973.7),(119.5,225261.7)
    # E4: (93.5,124864.0),(-61.3,33041.0),(78.1,65397.7),(-124.4,310698.9),(56.2,2268.1),(83.2,85091.1)
    # E5: (-127.7,325228.9),(94.1,127180.8),(-65.6,51801.5),(94.8,129883.9),(-79.1,111242.3),(-66.9,57525.5),(119.7,226033.9)
    # E6: (77.6,63466.9),(-107.4,235847.7),(110.8,191667.1),(-100.1,203705.6),(52.9,802.1)
    # Fit quadratic. But note asymmetry: negative x gives larger y than positive at same |x|.
    # Try g(x) = A*x^2 + B*x + C. Negative x with B<0 gives larger y. Good.
    # Let's do least squares manually via normal equations. Actually just hardcode a good fit.
    # From E1 fit: A=25.49, B=-210.2, C=-75349 worked for E1 but overshoots at large |x| (E2 104.5 predicted 181042 vs 167340).
    # So curvature is less than quadratic at large x (sub-quadratic growth). Try cubic? Or quadratic with smaller A.
    # Let's fit A,B,C to minimize error on big points. Use three representative points:
    # (123.6,241093.6), (-127.7,325228.9), (66,21806.0)
    # A*15277 + B*123.6 + C = 241093.6
    # A*16307 + B*(-127.7) + C = 325228.9
    # A*4356 + B*66 + C = 21806.0
    # Eq1-Eq3: A*10921 + B*57.6 = 219287.6
    # Eq2-Eq3: A*11951 + B*(-193.7) = 303422.9
    # From first: B = (219287.6 - 10921A)/57.6 = 3807.08 - 189.60A
    # Sub: 11951A - 193.7*(3807.08 - 189.60A) = 303422.9
    # 11951A - 737431 + 36726A = 303422.9
    # 48677A = 1040854 -> A = 21.38
    # B = 3807.08 - 189.60*21.38 = 3807.08 - 4053.6 = -246.5
    # C = 21806 - 21.38*4356 - (-246.5)*66 = 21806 - 93131 + 16269 = -55056
    # Check (104.5): 21.38*10920 - 246.5*104.5 - 55056 = 233470 - 25759 - 55056 = 152655 vs 167340. Off by ~9%.
    # Check (88.2): 21.38*7779 - 246.5*88.2 - 55056 = 166315 - 21741 - 55056 = 89518 vs 104398. Off.
    # Hmm. Growth is steeper than quadratic at moderate x but shallower at large x? 
    # Actually 88.2 -> 104398, 123.6 -> 241094. Ratio y: 2.31, x ratio 1.40. exponent log(2.31)/log(1.40)=2.58.
    # 66->21806, 123.6->241094: ratio 11.06, x ratio 1.873, exponent 3.85. Steeper at low end.
    # So it's not a pure power. Could be quadratic plus something. Let's try fitting all points with least squares properly.
    # I'll just compute a least-squares quadratic in code at import time using the data.
    # But data must be embedded. That's fine - it's fitting a mechanism (quadratic), not memorizing.
    # Actually let me reconsider: maybe g(x) = A*x^2 + B*x + C is wrong; maybe it's A*x^2*|x|^p...
    # Let's check: at x=66, y=21806. At x=88.2, y=104398. At x=123.6, y=241094.
    # Differences suggest roughly cubic-ish near 66-88 then quadratic-ish.
    # Try g(x) = A*x^3 + B*x^2 + C*x + D? Fit 4 points.
    # Use (66,21806),(88.2,104398),(123.6,241094),(-127.7,325229)
    # This is getting complex. Let me just do least squares quadratic in code over all points.
    # If quadratic is inadequate, the residuals will show and I can note it.
    # Actually, let me try: maybe it's A*x^2 + B*x + C but with different A for different ranges - no, MLP is smooth.
    # Let me try fitting with the constraint that it's smooth. Least squares quadratic it is.
    import math
    pts = [
        (88.2,104398.3),(66,21806.0),(-61.7,34659.9),(72.7,44545.8),
        (104.5,167339.9),(65.5,20347.3),(-63.9,44316.4),(104.9,168884.5),(123.6,241093.6),(79.4,70417.5),(103.0,161547.7),(-55.8,11784.3),
        (58.8,5395.5),(102.1,158072.4),(-102.2,212952.0),(105.7,171973.7),(119.5,225261.7),
        (93.5,124864.0),(-61.3,33041.0),(78.1,65397.7),(-124.4,310698.9),(56.2,2268.1),(83.2,85091.1),
        (-127.7,325228.9),(94.1,127180.8),(-65.6,51801.5),(94.8,129883.9),(-79.1,111242.3),(-66.9,57525.5),(119.7,226033.9),
        (77.6,63466.9),(-107.4,235847.7),(110.8,191667.1),(-100.1,203705.6),(52.9,802.1),
    ]
    # Least squares for y = A*x^2 + B*x + C
    n = len(pts)
    Sx4=Sx3=Sx2=Sx1=Sx0=0.0
    Sx2y=Sxy=Sy=0.0
    for x,y in pts:
        Sx4+=x**4; Sx3+=x**3; Sx2+=x*x; Sx1+=x; Sx0+=1
        Sx2y+=x*x*y; Sxy+=x*y; Sy+=y
    # Normal equations:
    # [Sx4 Sx3 Sx2][A]   [Sx2y]
    # [Sx3 Sx2 Sx1][B] = [Sxy ]
    # [Sx2 Sx1 Sx0][C]   [Sy  ]
    # Solve 3x3 via Cramer
    def det3(m):
        return (m[0][0]*(m[1][1]*m[2][2]-m[1][2]*m[2][1])
               -m[0][1]*(m[1][0]*m[2][2]-m[1][2]*m[2][0])
               +m[0][2]*(m[1][0]*m[2][1]-m[1][1]*m[2][0]))
    M=[[Sx4,Sx3,Sx2],[Sx3,Sx2,Sx1],[Sx2,Sx1,Sx0]]
    D=det3(M)
    def solve(col):
        M2=[row[:] for row in M]
        for i in range(3):
            M2[i][col]=[Sx2y,Sxy,Sy][i]
        return det3(M2)/D
    A=solve(0); B=solve(1); C=solve(2)
    floor=-84.3663
    def f(x):
        try:
            v = A*x*x + B*x + C
            return max(floor, v)
        except Exception:
            return None
    xs = probe.get("x", [])
    return {"y": [f(x) for x in xs]}
