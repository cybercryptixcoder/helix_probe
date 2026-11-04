def predict(probe):
    # x = 2a - b, clamped to [-10, 10] [E1: 16.8-7.6=9.2 ✓; E2: -7.6 ✓; E3: 19.4-4.9=14.5→10 ✓; E4: 10-7.6=2.4 ✓; E5: 19.4-3.6=15.8→10 ✓; E6: 10-7.6=2.4 ✓; E7: 10-2.8=7.2 ✓]
    # y when switch off: y = c + (1 if a>=8 else 0) [E1: 4.2+1=5.2 ✓; E2: 4.2 ✓; E3: 9.2+1=10.2 ✓; E4: 4.2 ✓; E7: 7.6 ✓]
    # y when switch on: y = 10 - c + (1 if a>=8 else 0) [E5: 10-8.9+1=2.1 ✓; E6: 10-4.2+0=5.8 ✓]
    # size: E7 (a=5,c=7.6)->2.3 contradicts quadratic fit. Try size = 0.1a^2 - 0.84a - 0.62c + 5.704? E7: 2.5-4.2-4.712+5.704=-0.71 ✗.
    #   Reconsider: maybe size depends on a and c differently. Data: (8.4,4.2)->? E1 size unknown here but fit; (0,4.2)->?; (9.7,9.2)->1.25; (5,4.2)->1.4; (9.7,8.9)->1.4; (5,4.2)->1.4; (5,7.6)->2.3
    #   E4 and E6 both (a=5,c=4.2)->1.4. E7 (a=5,c=7.6)->2.3. So at a=5, size rises with c: slope (2.3-1.4)/(7.6-4.2)=0.9/3.4≈0.265. So +0.265c not -0.62c.
    #   E3 (9.7,9.2)->1.25, E5 (9.7,8.9)->1.4. At a=9.7, c 9.2 vs 8.9: size 1.25 vs 1.4, slope (1.25-1.4)/(9.2-8.9)=-0.15/0.3=-0.5. Contradicts +0.265 at a=5. Hmm.
    #   Try size = f(a) + g(c) with interaction? Or size = k*(something). Let's fit size = p*a + q*c + r + s*a*c?
    #   Points: (5,4.2,1.4),(5,7.6,2.3),(9.7,9.2,1.25),(9.7,8.9,1.4)
    #   From (5,4.2)->(5,7.6): q*3.4=0.9 => q=0.2647
    #   From (9.7,8.9)->(9.7,9.2): q*0.3=-0.15 => q=-0.5. Inconsistent => interaction.
    #   Try size = A + B*a + C*c + D*a*c. Four points, four unknowns.
    #   (5,4.2): A+5B+4.2C+21D=1.4
    #   (5,7.6): A+5B+7.6C+38D=2.3
    #   (9.7,9.2): A+9.7B+9.2C+89.24D=1.25
    #   (9.7,8.9): A+9.7B+8.9C+86.33D=1.4
    #   Subtract eq2-eq1: 3.4C+17D=0.9
    #   Subtract eq3-eq4: 0.3C+2.91D=-0.15
    #   From second: C=(-0.15-2.91D)/0.3=-0.5-9.7D
    #   Sub: 3.4(-0.5-9.7D)+17D=0.9 => -1.7-32.98D+17D=0.9 => -15.98D=2.6 => D=-0.1627
    #   C=-0.5-9.7(-0.1627)=-0.5+1.578=1.078
    #   eq1: A+5B+4.2(1.078)+21(-0.1627)=1.4 => A+5B+4.528-3.417=1.4 => A+5B=0.289
    #   eq3: A+9.7B+9.2(1.078)+89.24(-0.1627)=1.25 => A+9.7B+9.918-14.519=1.25 => A+9.7B=5.851
    #   Subtract: 4.7B=5.562 => B=1.1834, A=0.289-5.917=-5.628
    #   Check E1 (8.4,4.2): -5.628+1.1834*8.4+1.078*4.2-0.1627*8.4*4.2 = -5.628+9.94+4.528-5.741=3.10. Hmm E1 size unknown to me.
    #   This is getting speculative. Simpler: maybe size = 1 + 0.1*(a-5)^2 + ... no.
    #   Given uncertainty, use the 4-point bilinear fit as best guess.
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
    size = -5.628 + 1.1834*a + 1.078*c - 0.1627*a*c
    return {"x": round(x, 2), "y": round(y, 2), "size": round(size, 2)}
