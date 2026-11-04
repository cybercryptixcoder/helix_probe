def predict(probe):
    # x = 2a - b, clamped to [-10, 10] [E1: 16.8-7.6=9.2 ✓; E2: -7.6 ✓; E3: 14.5→10 ✓; E4: 2.4 ✓; E5: 15.8→10 ✓; E6: 2.4 ✓; E7: 7.2 ✓; E8: 10 ✓; E9: 14.5→10 ✓; E10: 0 ✓; E11: -1.1 ✓]
    # y (switch off) = c + (1 if a>=8 else 0) [E1: 5.2 ✓; E2: 4.2 ✓; E3: 10.2 ✓; E4: 4.2 ✓; E7: 7.6 ✓; E8: 4.2 ✓; E10: 4.2 ✓; E11: 9.0 ✓]
    # y (switch on) = 10 - c + (1 if a>=8 else 0) [E5: 2.1 ✓; E6: 5.8 ✓; E9: 3.9 ✓]
    # size: depends on a and c only (b irrelevant) [E8 vs E10: same a,c, b=0 vs 10, both 1.4]
    #   Data (a,c)->size: (5,4.2)->1.4 [E4,E6,E8,E10]; (5,7.6)->2.3 [E7]; (9.7,9.2)->1.25 [E3]; (9.7,8.9)->1.4 [E5]; (9.9,7.1)->2.4 [E9]; (3.1,9.0)->3.95 [E11]
    #   At a=5: c 4.2->7.6 gives 1.4->2.3, slope 0.265. At a=9.7: c 8.9->9.2 gives 1.4->1.25, slope -0.5. Interaction present.
    #   Try size = k*(a - c)^2 / something? (5,4.2): d=0.8; (5,7.6): d=-2.6; (9.7,9.2): d=0.5; (9.7,8.9): d=0.8; (9.9,7.1): d=2.8; (3.1,9.0): d=-5.9
    #   size vs |d|: 0.8->1.4, 2.6->2.3, 0.5->1.25, 0.8->1.4, 2.8->2.4, 5.9->3.95. Roughly increasing with |a-c|.
    #   Try size = 1 + 0.5*|a-c|: 0.8->1.4 ✓; 2.6->2.3 ✓; 0.5->1.25 ✓; 0.8->1.4 ✓; 2.8->2.4 ✓; 5.9->3.95 ✓. Excellent fit!
    # size = 1 + 0.5*|a - c| [E3-E11 all ✓]
    a = probe.get("a", 0)
    b = probe.get("b", 0)
    c = probe.get("c", 0)
    sw = probe.get("switch", "off")
    x = max(-10, min(10, 2*a - b))
    bump = 1 if a >= 8 else 0
    if sw == "on":
        y = 10 - c + bump
    else:
        y = c + bump
    size = 1 + 0.5*abs(a - c)
    return {"x": round(x, 2), "y": round(y, 2), "size": round(size, 2)}
