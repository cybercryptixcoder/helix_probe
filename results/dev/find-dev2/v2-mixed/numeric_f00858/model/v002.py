def predict(probe):
    # f(x) = 1 when |x| is small (roughly |x| < 10), else 0 [E2]
    # Evidence: f(-1)=f(-0.1)=f(0)=f(0.1)=f(1)=1; f(-10)=f(10)=f(-50)=f(50)=0 [E2]
    # E1 all |x| >= 2.9 except none small... E1 values: 88.2,66,-20.3,-61.7,2.9,-24.3,72.7,-50.4,-6,21.3
    #   -6 and 2.9 are within |x|<10 but observed 0 -> threshold is tighter than 6? [E1]
    # So the nonzero region is narrower: |x| <= ~1 (E2 shows 1 -> 1, 10 -> 0; E1 shows 2.9 -> 0)
    # Boundary between 1 and 2.9 unknown; pick midpoint guess 2.0 (?)
    def f(x):
        return 1.0 if abs(x) <= 2.0 else 0.0
    return {"y": [f(x) for x in probe["x"]]}
