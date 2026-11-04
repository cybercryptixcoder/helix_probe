import math

def predict(probe):
    # Model of the black box f(x).
    #
    # Beliefs (each line cites evidence):
    # - Output is one of {8.8, 9.8, -11.4, -12.4} for ordinary x [E1,E3,E5,E7,E9,E11].
    # - There is a special point at x = 0.0 returning 1548.92 [E2].
    # - For x < 0: output is 9.8 near zero (|x| small, up to ~4.5) and 8.8 further out [E4,E6,E8,E12].
    # - For x > 0: output is -11.4 near zero (up to ~4.1) and -12.4 further out [E4,E6,E8,E10,E12].
    # - The negative-side boundary sits between 4.5 and 4.51 (9.8 -> 8.8 as |x| grows) [E8,E12].
    # - The positive-side boundary sits between 4.1 and 4.15 (-11.4 -> -12.4 as x grows) [E10,E12].
    # - Sign of the output is positive for x<0, negative for x>0 (except x=0 spike) [E1,E3,E5,E7,E9,E11].
    # - Magnitude is the "near" value inside the boundary and the "far" value outside [E4,E6,E8,E10,E12].
    #
    # ? The exact boundary values are inferred from bracketing samples; I place them at
    #   4.505 on the negative side and 4.125 on the positive side (midpoints of the gaps).

    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            x = float(x)
        except Exception:
            ys.append(None)
            continue

        if x == 0.0:
            ys.append(1548.92)
            continue

        if x < 0:
            # negative side: near = 9.8, far = 8.8
            if -x <= 4.505:
                ys.append(9.8)
            else:
                ys.append(8.8)
        else:
            # positive side: near = -11.4, far = -12.4
            if x <= 4.125:
                ys.append(-11.4)
            else:
                ys.append(-12.4)

    return {"y": ys}
