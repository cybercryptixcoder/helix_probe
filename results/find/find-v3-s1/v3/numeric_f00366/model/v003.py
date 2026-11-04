def predict(probe):
    # Sign-based step function with a wide near-zero band [E1, E2, E3, E4]
    # x < 0: 9.8 for -3 <= x < 0; 8.8 for x <= -3 (band extends at least to -3) [E4]
    # x > 0: -11.4 for 0 < x <= 3; -12.4 for x > 3 (band extends at least to 3) [E4]
    # x = 0: 1548.92 [E2]
    # Band boundary is somewhere beyond |x|=3; exact edge unknown (between 3 and 12.9 on neg side, 3 and 38.8 on pos side) [?]
    out = []
    for x in probe["x"]:
        if x == 0:
            out.append(1548.92)
        elif x < 0:
            out.append(9.8 if x > -3.0 else 8.8)
        else:
            out.append(-11.4 if x < 3.0 else -12.4)
    return {"y": out}
