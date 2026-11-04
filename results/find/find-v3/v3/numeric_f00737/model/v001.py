import math

def predict(probe):
    # Model hypotheses:
    # - For x>0: f(x) = a*log(x) + b*x + c  [E2: values grow, log-like at small x]
    #   Fit from E2: f(1)=-7.8, f(2)=-1.4907, f(128)=36.365
    #   Try f(x) = 6.5*ln(x) - 7.8 + 0.0? Check: ln(2)*6.5-7.8 = 4.5-7.8=-3.3 (no)
    #   Better: f(x) = A*ln(x) + B*x + C
    #   From E2: f(1)=C=-7.8
    #   f(2)=A*0.6931+2B-7.8=-1.4907 -> 0.6931A+2B=6.3093
    #   f(128)=A*4.852+128B-7.8=36.365 -> 4.852A+128B=44.165
    #   Solve: from first A=(6.3093-2B)/0.6931=9.103-2.885B
    #   4.852*(9.103-2.885B)+128B=44.165 -> 44.17-14.0B+128B=44.165 -> 114B=-0.005 -> B≈0
    #   So B≈0, A≈9.1? Check f(4)=9.1*1.386-7.8=12.6-7.8=4.8 ✓ (obs 4.8186)
    #   f(8)=9.1*2.079-7.8=18.9-7.8=11.1 ✓ (obs 11.1278)
    #   f(64)=9.1*4.159-7.8=37.85-7.8=30.05 ✓ (obs 30.0557)
    #   So f(x) = 9.1*ln(x) - 7.8 for x>0. Refine A: f(128)=36.365 -> A=(36.365+7.8)/4.852=9.105
    #   Use A=9.105, C=-7.8. Check f(1)=9.105*0-7.8=-7.8 ✓
    # - For x<0: undefined (null) [E1: -20.3,-61.7,-24.3,-50.4,-6.0 all null; E2: -1,-2 null]
    # - x=0? unknown, likely null or -inf; treat as null
    A = 9.105
    C = -7.8
    out = []
    for x in probe["x"]:
        if x is None:
            out.append(None)
        elif x > 0:
            out.append(A * math.log(x) + C)
        else:
            out.append(None)
    return {"y": out}
