import math

def predict(probe):
    # Observations from E1:
    # - f undefined (null) for x <= 0
    # - f(1) = 1.1
    # - For x >= 2, f appears linear: f(2)=142.1873, f(4)=283.2746, ... f(64)=847.6238
    #   slope = (283.2746-142.1873)/2 = 70.54365 per unit x
    #   f(2) = 142.1873 => intercept = 142.1873 - 2*70.54365 = 1.1000
    #   So f(x) = 70.54365*x + 1.1 for x in [2, 64]
    # - But f(100)=938.4637: 70.54365*100+1.1 = 7055.465, way off.
    #   Check f(100)-f(64) = 90.8399 over 36 units => slope ~2.5233
    #   f(127)=987.1146, f(128)=988.7111: slope ~1.5965 between 127 and 128
    #   Looks like a saturating curve (e.g., logarithmic or sqrt) after some point.
    # - f(1)=1.1 fits the linear formula: 70.54365*1+1.1 = 71.64, no.
    #   Hmm, f(1)=1.1 doesn't fit. Maybe the linear region starts at x=2.
    # Let's reconsider: maybe f(x) = a*x + b for small x, then saturates.
    # f(2)=142.1873, f(4)=283.2746: difference 141.0873 over 2 => slope 70.54365
    # f(1)=1.1 is odd. Could be f(x) = 70.54365*(x-1) + 1.1? Then f(2)=71.64, no.
    # Try: f(x) = 70.54365*x + c. f(2)=142.1873 => c=1.1. f(1)=71.64, but observed 1.1.
    # So x=1 is special, or the formula differs for x<2.
    # Maybe f(x) = 70.54365*x + 1.1 for x>=2, and f(1)=1.1 (same as intercept).
    # For large x, saturating. Let's fit: maybe f(x) = A*ln(x) + B for x large?
    # f(64)=847.6238, f(100)=938.4637, f(127)=987.1146, f(128)=988.7111
    # ln(64)=4.1589, ln(100)=4.6052, ln(127)=4.8442, ln(128)=4.8520
    # slope between 64 and 100: (938.4637-847.6238)/(4.6052-4.1589)=90.8399/0.4463=203.5
    # between 100 and 127: (987.1146-938.4637)/(4.8442-4.6052)=48.6509/0.239=203.6
    # between 127 and 128: (988.7111-987.1146)/(4.8520-4.8442)=1.5965/0.0078=204.7
    # Consistent! So for large x, f(x) = 203.5*ln(x) + C
    # C = 847.6238 - 203.5*4.1589 = 847.6238 - 846.34 = 1.28
    # Check f(100): 203.5*4.6052+1.28 = 937.16+1.28=938.44 ~ 938.4637 ✓
    # So f(x) = 203.5*ln(x) + 1.28 for large x.
    # Where does linear transition to log? At x=64: linear gives 70.54365*64+1.1=4516, log gives 847.6.
    # So transition is before 64. Check x=32: linear=2258, log=203.5*3.4657+1.28=706.5. Observed 706.5365!
    # So log formula works at 32 too. Check x=16: log=203.5*2.7726+1.28=565.4. Observed 565.4492 ✓
    # x=8: log=203.5*2.0794+1.28=424.4. Observed 424.3619 ✓
    # x=4: log=203.5*1.3863+1.28=283.4. Observed 283.2746 ✓
    # x=2: log=203.5*0.6931+1.28=142.3. Observed 142.1873 ✓
    # x=1: log=203.5*0+1.28=1.28. Observed 1.1. Close-ish but not exact.
    # So actually the whole thing is f(x) = 203.5*ln(x) + 1.28 for x>0!
    # Let's refine constants. Using f(2)=142.1873 and f(128)=988.7111:
    # 203.5*ln(2)+C=142.1873 => C=142.1873-141.06=1.127
    # 203.5*ln(128)+C=988.7111 => C=988.7111-987.36=1.35
    # Slight inconsistency. Let's solve exactly:
    # a*ln(2)+b=142.1873, a*ln(128)+b=988.7111
    # a*(ln128-ln2)=846.5238 => a*ln(64)=846.5238 => a=846.5238/4.15888=203.55
    # b=142.1873-203.55*0.693147=142.1873-141.08=1.107
    # Check f(1): 203.55*0+1.107=1.107 ≈ 1.1 ✓
    # Check f(100): 203.55*4.60517+1.107=937.36+1.107=938.47 ≈ 938.4637 ✓
    # Great. So f(x) = 203.55*ln(x) + 1.107 for x>0, undefined for x<=0.
    a = 203.55
    b = 1.107
    out = []
    for x in probe["x"]:
        if x is None or x <= 0:
            out.append(None)
        else:
            out.append(a * math.log(x) + b)
    return {"y": out}
