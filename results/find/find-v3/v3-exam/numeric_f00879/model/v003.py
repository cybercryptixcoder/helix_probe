import math

def predict(probe):
    # No smoothness at unit scale [E8, E4, E2]: values jump wildly between nearby x
    # No periodicity found [E4, E6]
    # No dependence on x mod small period [E8]
    # Values appear noisy in roughly [-3.5, 4.5], mean ~0.6 [all E1-E8]
    # Best predictor: constant mean
    return {"y": [0.6 for _ in probe["x"]]}
