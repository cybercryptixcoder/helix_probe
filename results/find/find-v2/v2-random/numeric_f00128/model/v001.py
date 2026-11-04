import math

def predict(probe):
    # Observations: f is roughly linear in x over most of the range.
    # From E1: y/x ratios vary, suggesting a smooth nonlinear (MLP) function.
    # Best guess: f(x) ≈ a*x + b*x^3 form? Let's fit a cubic-ish.
    # E1 data: (88.2,-1479.4),(66,-1104.2),(-20.3,139.6),(-61.7,419.5),
    # (2.9,-37.8),(-24.3,166.7),(72.7,-1217.4),(-50.4,343.1),(-6,43),(-21.3,-348.8)
    # Ratios y/x: -16.8,-16.7,-6.9,-6.8,-13.0,-6.9,-16.7,-6.8,-7.2,16.4
    # Sign flips: x=2.9 -> y=-37.8 (negative), x=-6 -> y=+43 (positive)
    # Looks like y ≈ -k*x with k depending on |x|: larger |x| -> larger |k|.
    # At |x|~20-25: k~6.9; at |x|~50-66: k~6.8; at |x|~72-88: k~16.7
    # Hmm inconsistent. Let's just fit a smooth odd-ish function.
    # Try y = c1*x + c2*x^3. Use two points: (88.2,-1479.4),(21.3,-348.8)
    # c1*88.2 + c2*88.2^3 = -1479.4
    # c1*21.3 + c2*21.3^3 = -348.8
    # 88.2^3=686128, 21.3^3=9663.6
    # Solve: from eq2 c1 = (-348.8 - 9663.6 c2)/21.3 = -16.376 - 453.7 c2
    # eq1: 88.2*(-16.376-453.7c2) + 686128 c2 = -1479.4
    # -1444.4 - 40016 c2 + 686128 c2 = -1479.4
    # 646112 c2 = -35 -> c2 = -5.4e-5, c1 = -16.376 + 0.0245 = -16.35
    # Check x=66: -16.35*66 -5.4e-5*287496 = -1079 -15.5 = -1094.6 vs -1104.2 ok
    # Check x=-61.7: -16.35*-61.7 -5.4e-5*(-234885)=1008.8+12.7=1021 vs 419.5 BAD
    # So not odd. Sign asymmetry: positive x -> large negative, small positive x -> small negative, negative x -> positive.
    # Actually x=-61.7 -> 419.5 (positive), x=72.7 -> -1217 (negative). Roughly y ≈ -16*x for large |x|? 
    # -16*72.7=-1163 close to -1217. -16*-61.7=987 vs 419 no.
    # Let's just do linear fit through E1.
    xs=[88.2,66.0,-20.3,-61.7,2.9,-24.3,72.7,-50.4,-6.0,21.3]
    ys=[-1479.3769,-1104.1996,139.6237,419.4911,-37.7888,166.664,-1217.4288,343.1022,42.9545,-348.775]
    n=len(xs)
    sx=sum(xs); sy=sum(ys); sxx=sum(x*x for x in xs); sxy=sum(x*y for x,y in zip(xs,ys))
    den=n*sxx-sx*sx
    a=(n*sxy-sx*sy)/den
    b=(sy-a*sx)/n
    out=[]
    for x in probe.get("x",[]):
        try:
            out.append(a*x+b)
        except Exception:
            out.append(None)
    return {"y":out}
