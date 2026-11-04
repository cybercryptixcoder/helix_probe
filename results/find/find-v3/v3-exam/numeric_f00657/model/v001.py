def predict(probe):
    # Output is always ±18 [E1]
    # Sign appears to depend on x; from E1: negative for x>~50, positive for x<-50,
    # mixed in between. Best guess: sign relates to floor/parity or a threshold pattern.
    # Without more data, guess sign = -18 if x > 0 else 18? But E1 contradicts:
    #   x=2.9 -> -18, x=-6.0 -> 18, x=21.3 -> -18, x=-20.3 -> 18, x=-24.3 -> 18,
    #   x=72.7 -> -18, x=-50.4 -> 18, x=-61.7 -> 18, x=66.0 -> -18, x=88.2 -> -18
    # Pattern: negative when x>0, positive when x<0. Check: 2.9>0 -> -18 yes;
    #   -6.0<0 -> 18 yes; 21.3>0 -> -18 yes; -20.3<0 -> 18 yes; -24.3<0 -> 18 yes;
    #   72.7>0 -> -18 yes; -50.4<0 -> 18 yes; -61.7<0 -> 18 yes; 66.0>0 -> -18 yes;
    #   88.2>0 -> -18 yes. Consistent!
    # So: f(x) = -18 if x > 0 else 18 (x=0 unknown)
    out = []
    for x in probe["x"]:
        out.append(-18.0 if x > 0 else 18.0)
    return {"y": out}
