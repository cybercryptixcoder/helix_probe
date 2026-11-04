def predict(probe):
    # Two output levels: -6.9 and -7.9 [E1]
    # x=2.9 gives -6.9015, a slight perturbation near a boundary [E1]
    # Pattern: outputs alternate based on some property of x [E1]
    # Hypothesis: sign-based? x>0 -> -6.9, x<0 -> -7.9? Check E1:
    #   88.2>0 -> -6.9 ok; 66>0 -> -6.9 ok; -20.3<0 -> -7.9 ok;
    #   -61.7<0 -> -7.9 ok; 2.9>0 -> -6.9015 (close to -6.9) ok;
    #   -24.3<0 -> -7.9 ok; 72.7>0 -> -6.9 ok; -50.4<0 -> -7.9 ok;
    #   -6.0<0 -> -7.9 ok; 21.3>0 -> -6.9 ok. All consistent.
    # The 2.9 -> -6.9015 anomaly: near-zero positive gives slight offset.
    # Model: x>=0 -> -6.9, x<0 -> -7.9; small positive x -> -6.9015 (?)
    out = []
    for x in probe.get("x", []):
        if x is None:
            out.append(None)
        elif x >= 0:
            if 0 <= x < 3:
                out.append(-6.9015)
            else:
                out.append(-6.9)
        else:
            out.append(-7.9)
    return {"y": out}
