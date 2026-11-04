import math

def predict(probe):
    # Model hypothesis:
    # - f(x) is undefined (null) for x < 0 [E1: negatives all null]
    # - For x >= 0, f(x) looks like a smooth increasing function.
    #   Data points: f(2.9)=1.8914, f(21.3)=20.0415, f(66.0)=30.3358,
    #                f(72.7)=31.2158, f(88.2)=32.975
    # - Looks like sqrt-ish / log-ish growth. Try f(x) = a*sqrt(x) + b?
    #   sqrt(2.9)=1.703 -> 1.8914
    #   sqrt(21.3)=4.615 -> 20.0415  (ratio ~4.34)
    #   sqrt(66)=8.124 -> 30.3358   (ratio ~3.73)
    #   sqrt(72.7)=8.526 -> 31.2158 (ratio ~3.66)
    #   sqrt(88.2)=9.392 -> 32.975  (ratio ~3.51)
    # Not pure sqrt. Try log: ln(2.9)=1.065->1.89; ln(21.3)=3.06->20.04;
    #   ln(66)=4.19->30.34; ln(72.7)=4.29->31.22; ln(88.2)=4.48->32.98
    #   ratios: 1.78, 6.55, 7.24, 7.28, 7.36 -> not log either.
    # Try x^p: 2.9^p=1.89 -> p~0.61; 21.3^p=20.04 -> p~0.99;
    #   66^p=30.34 -> p~0.81; 72.7^p=31.22 -> p~0.80; 88.2^p=32.98 -> p~0.78
    # Hmm inconsistent at low x. Maybe f(x)=x^0.8 roughly for larger x,
    #   but small x deviates. Actually check: 21.3^0.8=11.6, not 20.
    # Let's try f(x) = x / (something). 21.3/20.04=1.06; 66/30.34=2.18;
    #   72.7/31.22=2.33; 88.2/32.98=2.67. Not linear.
    # Try f(x) = a*ln(x)+b via two points (66,30.34),(88.2,32.98):
    #   slope=(32.98-30.34)/(ln88.2-ln66)=2.64/0.290=9.10; b=30.34-9.10*4.19=-7.8
    #   check 21.3: 9.10*3.06-7.8=20.05 ✓ ; check 2.9: 9.10*1.065-7.8=1.89 ✓
    #   check 72.7: 9.10*4.29-7.8=31.24 ✓ (obs 31.22)
    # Excellent! f(x) = 9.10*ln(x) - 7.8 for x>0, null for x<=0.
    # Refine: use a*ln(x)+b. From (2.9,1.8914) and (88.2,32.975):
    #   a=(32.975-1.8914)/(ln88.2-ln2.9)=31.0836/(4.4796-1.0647)=31.0836/3.4149=9.102
    #   b=1.8914-9.102*1.0647=1.8914-9.691=-7.800
    # Check 21.3: 9.102*3.0587-7.800=27.84-7.80=20.04 ✓
    # Check 66: 9.102*4.1897-7.800=38.13-7.80=30.33 ✓
    # Check 72.7: 9.102*4.2865-7.800=39.02-7.80=31.22 ✓
    # Great fit. Use a=9.102, b=-7.800.
    a = 9.102
    b = -7.800
    out = []
    for x in probe["x"]:
        if x is None:
            out.append(None)
        elif x <= 0:
            out.append(None)
        else:
            out.append(a * math.log(x) + b)
    return {"y": out}
