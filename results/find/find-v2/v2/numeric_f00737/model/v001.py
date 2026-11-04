import math

def predict(probe):
    # f(x) is null for x <= 0 [E2: all x<=0 null]
    # f(x) defined for x > 0 [E2]
    # f is nonlinear, concave, saturating [E2: 5->6.85, 20->19.47, 50->27.81, 80->32.09, 128->36.37]
    # Looks like a log/sqrt-like curve. Fit: y = a*ln(x) + b? Check.
    # E2 points: (5,6.8497),(10,13.159),(20,19.4682),(40,25.7775),(50,27.8087),
    #            (60,29.4682),(80,32.0868),(100,34.1179),(120,35.7775),(128,36.365)
    # Differences per doubling: 5->10: +6.31; 10->20: +6.31; 20->40: +6.31; 40->80: +6.31
    # So y = 6.31*log2(x) + c. At x=5: 6.31*log2(5)=14.65 -> c = -7.80
    # Check x=10: 6.31*3.3219=20.96-7.80=13.16 ✓
    # x=128: 6.31*7=44.17-7.80=36.37 ✓
    # So y = 6.31*log2(x) - 7.80 for x>0, null for x<=0.
    # E1 check: x=88.2 -> 6.31*log2(88.2)-7.80 = 6.31*6.4627-7.80=32.98 ✓
    # x=66 -> 6.31*6.0444-7.80=30.34 ✓
    # x=2.9 -> 6.31*1.5361-7.80=1.89 ✓
    # x=72.7 -> 6.31*6.1837-7.80=31.22 ✓
    # x=21.3 -> 6.31*4.4128-7.80=20.04 ✓
    # Negative x in E1 all null ✓
    out = []
    for x in probe.get("x", []):
        try:
            if x is None or x <= 0:
                out.append(None)
            else:
                out.append(6.31*math.log2(x) - 7.80)
        except Exception:
            out.append(None)
    return {"y": out}
