def predict(probe):
    # f(x) = round-half-up (floor(x+0.5)) on the interior, with a positive anomaly
    #   and asymmetric cutoffs. Evidence:
    # Interior rounding is floor(x+0.5) [E7,E8,E11].
    # Positive anomaly: 4.0 < x < 4.4 -> 5 [E8,E9,E6,E12]; x=4.0->4 [E9,E10,E12]; x>=4.4->0 [E8,E10]
    # Negative cutoff: x <= -4.39 -> 0 [E11:-4.39,-4.41,-4.4->0; E8:-4.4->0;
    #   E9:-4.35->-4; E8:-4.35->-4]; -4.39 < x rounds normally [E9:-4.35..-4.05->-4]
    # Outside [-4.39, 4.4) (with anomaly) -> 0 [E1,E3,E5]
    # Rounding region: floor(x+0.5) for -4.39 < x < 4.4 except anomaly [E2,E4,E6,E7,E12]
    #   E12: 3.4,3.45 -> 4 (floor(3.9)=3? no, floor(3.45+0.5)=3) -> contradiction!
    #   E12 shows 3.4->4, 3.45->4: so rounding is NOT floor(x+0.5) near 3.4.
    #   Actually floor(3.4+0.5)=3, but observed 4. So rounding is ceil(x) for x>0?
    #   Check E4: 0.25->1, 0.5->1, 0.75->1, 1.25->2, 1.5->2, 1.75->2: ceil works.
    #   E7: 0.5->1, 1.5->2, 2.5->3, 3.5->4: ceil works. 2.49->3 (ceil), 2.51->3 (ceil).
    #   E2: 1.9->2, 2.1->3 (ceil=3), 2.5->3, 3->3, 3.5->4, 4->4: ceil works.
    #   Negative: E4: -0.25->0, -0.5->0, -0.75->0, -1.25->-1, -1.5->-1, -1.75->-1: ceil works!
    #   E7: -0.5->0, -1.5->-1, -2.5->-2, -3.5->-3: ceil works.
    #   E11: -0.51->0, -0.49->0, -1.51->-1, -1.49->-1: ceil works.
    #   E2: -4->-4, -3.5->-3, -3->-3, -2.5->-2, -2.1->-2, -1.9->-1: ceil works!
    #   E6: -4.05->-4, -4.0->-4, -3.95->-3, -3.9->-3, -3.8->-3: ceil works!
    #   E9: -4.35->-4, -4.05->-4, -3.95->-3: ceil works!
    # So the rule is ceil(x), not floor(x+0.5). This fixes E2,E4,E6,E7,E12.
    # Anomaly: 4.0 < x < 4.4 -> 5 [E8,E9,E12]; x=4.0->4 [E9,E10,E12]; x>=4.4->0 [E8,E10]
    # Negative cutoff: x <= -4.39 -> 0 [E11,E8,E9]; -4.39 < x ceil normally [E9]
    import math
    out = []
    for x in probe.get("x", []):
        try:
            if 4.0 < x < 4.4:
                out.append(5.0)
            elif -4.39 < x < 4.4:
                out.append(float(math.ceil(x)))
            else:
                out.append(0.0)
        except Exception:
            out.append(None)
    return {"y": out}
