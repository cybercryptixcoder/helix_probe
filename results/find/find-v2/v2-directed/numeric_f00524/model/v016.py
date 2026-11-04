def predict(probe):
    # Interior rule is ceil(x) [E2,E4,E6,E7,E9,E11,E12,E13,E14,E16]
    # Negative cutoff: x < -4.35 -> 0 [E13:-4.38->0; E11:-4.39->0; E17:-4.37->0; E18:-4.36->0; E19:-4.355..-4.37->0; E20:-4.351..-4.355->0; E21:-4.3501..-4.354->0]
    #   -4.35 rounds normally -> -4 [E8,E9,E19,E20,E21:-4.35->-4; E21:-4.349..-4.3499->-4]
    # Positive anomaly: 4.0 < x <= 4.35 -> 5 [E8,E9,E12:4.35->5; E17:4.01->5; E18:4.33,4.34->5; E19,E20,E21:4.35->5; E21:4.349..4.3499->5]
    #   x=4.0->4 [E9,E10,E12,E17]; x>4.35->0 [E18:4.36->0; E19:4.355->0; E20:4.351..4.355->0; E21:4.3501..4.354->0]
    # Outside [-4.35, 4.35] (with anomaly) -> 0 [E1,E3,E5]
    import math
    out = []
    for x in probe.get("x", []):
        try:
            if 4.0 < x <= 4.35:
                out.append(5.0)
            elif -4.35 <= x <= 4.35:
                out.append(float(math.ceil(x)))
            else:
                out.append(0.0)
        except Exception:
            out.append(None)
    return {"y": out}
