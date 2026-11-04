import math

def predict(probe):
    # Mechanism inferred from the evidence:
    #
    # There are two regimes separated by x = -5 (approximately).
    #
    # Regime A: x < -5  (roughly)
    #   f(x) = -0.7 * x
    #   Evidence: E4: f(-128)=89.6 = -0.7*(-128); f(-40)=28.0; f(-20)=14.0;
    #   f(-10)=7.0; f(-8)=5.6. E2: f(-40)=28, f(-30)=21, f(-20)=14, f(-10)=7.
    #   E1: f(-61.7)=43.4 ≈ -0.7*(-61.7)=43.19; f(-50.4)=35.7≈35.28;
    #   f(-24.3)=17.5≈17.01; f(-20.3)=14.7≈14.21. E5: f(-48.6)=34.3≈34.02;
    #   f(-102.2)=72.1≈71.54; f(-16.9)=11.9≈11.83. E6: f(-7.5)=5.6≈5.25;
    #   f(-7)=4.9≈4.9; f(-6.5)=4.9≈4.55; f(-6.1)=4.9≈4.27; f(-6)=4.2≈4.2;
    #   f(-5.9)=4.2≈4.13; f(-5.5)=4.2≈3.85; f(-5.1)=4.2≈3.57.
    #   The boundary: at x=-5 exactly, E6 gives -402.28 (regime B), while
    #   x=-5.1 gives 4.2 and x=-4.9 gives -402.3. So regime A is x < -5,
    #   regime B is x >= -5. (E4 x=-5 not present; E6 x=-5.1 -> A.)
    #   Rounding: outputs look rounded to 1 decimal in regime A
    #   (e.g. -0.7*(-61.7)=43.19 -> 43.4? no, 43.19 rounds to 43.2).
    #   Actually E1 f(-61.7)=43.4; -0.7*-61.7=43.19. Hmm, mismatch.
    #   Let's check: -0.7 * -61.7 = 43.19, reported 43.4. 
    #   Maybe slope is -0.703? -0.703*-61.7=43.37 -> 43.4. 
    #   Check f(-128)=89.6: -0.703*-128=89.98 -> 90.0, not 89.6.
    #   So slope varies? Try -0.7 exactly with rounding to nearest 0.7?
    #   E4 values: -128->89.6, -120->84.0, -100->70.0, -90->63.0,
    #   -80->56.0, -70->49.0, -50->35.0, -40->28.0, -30->21.0, -25->17.5,
    #   -20->14.0, -15->10.5, -12->8.4, -11->7.7, -10.5->7.7, -10.1->7.7,
    #   -9.9->7.0, -9.5->7.0, -9->6.3, -8->5.6.
    #   These are all multiples of 0.7! 89.6/0.7=128, 84/0.7=120, etc.
    #   So f(x) = round(-0.7*x / 0.7) * 0.7? That's just -0.7*x rounded
    #   to nearest multiple of 0.7... but -0.7*x is already a multiple of 0.7
    #   when x is integer. For non-integers: -10.1 -> 7.7 means
    #   -0.7*-10.1=7.07, but reported 7.7. So it's rounding x to nearest
    #   integer? -10.1 -> -10 -> 7.0, not 7.7. 
    #   Hmm, -10.1->7.7, -10.5->7.7, -11->7.7, -12->8.4.
    #   -0.7*-11=7.7 ✓. -0.7*-12=8.4 ✓. So -10.1 and -10.5 give 7.7,
    #   same as -11. Maybe x is rounded down (floor)? floor(-10.1)=-11 -> 7.7 ✓
    #   floor(-10.5)=-11 -> 7.7 ✓. floor(-9.9)=-10 -> 7.0 ✓. 
    #   floor(-9.5)=-10 -> 7.0 ✓. floor(-9)=-9 -> 6.3 ✓. floor(-8)=-8 -> 5.6 ✓.
    #   Check E1: -61.7 -> floor=-62 -> -0.7*-62=43.4 ✓!
    #   -50.4 -> floor=-51 -> 35.7 ✓. -24.3 -> floor=-25 -> 17.5 ✓.
    #   -20.3 -> floor=-21 -> 14.7 ✓. -6.0 -> floor=-6 -> 4.2 ✓.
    #   E5: -48.6 -> floor=-49 -> 34.3 ✓. -102.2 -> floor=-103 -> 72.1 ✓.
    #   -16.9 -> floor=-17 -> 11.9 ✓. -7.1 -> floor=-8 -> 5.6 ✓.
    #   E6: -7.5 -> floor=-8 -> 5.6 ✓. -7.0 -> floor=-7 -> 4.9 ✓.
    #   -6.5 -> floor=-7 -> 4.9 ✓. -6.1 -> floor=-7 -> 4.9 ✓.
    #   -6.0 -> floor=-6 -> 4.2 ✓. -5.9 -> floor=-6 -> 4.2 ✓.
    #   -5.5 -> floor=-6 -> 4.2 ✓. -5.1 -> floor=-6 -> 4.2 ✓.
    #   So regime A: f(x) = -0.7 * floor(x), for x < -5.
    #
    # Regime B: x >= -5
    #   Values are around -402.2 to -402.5 for x in [-5, ~19.5].
    #   Then at x=20: -336.0, x=30: -504.0, x=40: -672.0, ...
    #   E2: 20->-336, 30->-504, 40->-672, 60->-1008, 80->-1344,
    #   100->-1680, 120->-2016, 128->-2150.4.
    #   These are -16.8 * x: -16.8*20=-336 ✓, *30=-504 ✓, *40=-672 ✓,
    #   *60=-1008 ✓, *80=-1344 ✓, *100=-1680 ✓, *120=-2016 ✓,
    #   *128=-2150.4 ✓.
    #   E1: 88.2->-1478.4 = -16.8*88.2 ✓. 66.0->-1108.8 = -16.8*66 ✓.
    #   72.7->-1209.6 = -16.8*72.7= -1221.36? No, -16.8*72.7=-1221.36.
    #   Reported -1209.6. Hmm. -1209.6/72.7 = -16.63. 
    #   Maybe floor(x) again: floor(72.7)=72, -16.8*72=-1209.6 ✓!
    #   Check 88.2: floor=88, -16.8*88=-1478.4 ✓. 66.0: floor=66 ✓.
    #   E3: 104.5->-1747.2: floor=104, -16.8*104=-1747.2 ✓.
    #   65.5->-1092: floor=65, -16.8*65=-1092 ✓.
    #   30.3->-504: floor=30 ✓. 104.9->-1747.2: floor=104 ✓.
    #   123.6->-2066.4: floor=123, -16.8*123=-2066.4 ✓.
    #   79.4->-1327.2: floor=79, -16.8*79=-1327.2 ✓.
    #   103.0->-1730.4: floor=103, -16.8*103=-1730.4 ✓.
    #   E5: 58.8->-974.4: floor=58, -16.8*58=-974.4 ✓.
    #   102.1->-1713.6: floor=102, -16.8*102=-1713.6 ✓.
    #   47.1->-789.6: floor=47, -16.8*47=-789.6 ✓.
    #   28.4->-470.4: floor=28, -16.8*28=-470.4 ✓.
    #   105.7->-1764: floor=105, -16.8*105=-1764 ✓.
    #   119.5->-1999.2: floor=119, -16.8*119=-1999.2 ✓.
    #   E6: 19.5->-319.2: floor=19, -16.8*19=-319.2 ✓.
    #   So regime B for larger x: f(x) = -16.8 * floor(x).
    #
    #   But for x in [-5, ~19.5] we see values around -402.2 to -402.5.
    #   E6: -5.0->-402.28, -4.9->-402.3, -4.5->-402.4845, -4.0->-402.3671,
    #   -3.0->-402.2764, -2.5->-402.4385, -1.5->-402.3527, 0.5->-402.4846,
    #   3.0->-402.3739, 7.5->-402.4103, 15.0->-402.3116.
    #   E2: -5->-402.3253, -2->-402.2622, -1->-402.3079, 0->-402.2023,
    #   1->-402.2852, 2->-402.2043, 5->-402.3305, 10->-402.197.
    #   E3: 1.2->-402.3203.
    #   These are noisy around -402.3. Looks like a noisy constant.
    #   Mean roughly -402.3, noise ~ ±0.15.
    #   Where does this region end? At x=19.5 we get -319.2 (regime B slope),
    #   at x=15 we get -402.31 (constant region). At x=20 -> -336.
    #   So boundary is somewhere between 15 and 19.5.
    #   Hmm, -16.8*floor(x) at x=19 gives -319.2, matches 19.5.
    #   At x=18, -16.8*18=-302.4. At x=20, -336.
    #   The constant region seems to be x in [-5, ~18 or 19].
    #   Actually maybe the constant region is x in [-5, 18)? 
    #   We have x=15 -> -402.31 (constant), x=19.5 -> -319.2 (slope).
    #   No data between 15 and 19.5 to pin boundary.
    #   Guess: boundary at x=18 (since 18*16.8=302.4, and 19*16.8=319.2).
    #   Actually could be that the constant region is where floor(x) is small
    #   or where -16.8*floor(x) would be less negative than the constant?
    #   -16.8*floor(x) at x=18 is -302.4, which is > -402.3 (less negative).
    #   At x=24, -16.8*24=-403.2, close to -402.3.
    #   Hmm, maybe the constant is -16.8 * 24 = -403.2? No, values are -402.3.
    #   Let me reconsider: maybe constant region is x in [-5, 18]? 
    #   At x=19.5 we get -319.2 = -16.8*19. So x=19.5 is in slope region.
    #   Could boundary be x=18.5? Unknown.
    #   Let's set boundary at x=18 (floor(x)>=18 uses slope, floor<18 uses constant)?
    #   x=19.5: floor=19 >=18 -> slope ✓.
    #   x=15: floor=15 <18 -> constant ✓.
    #   x=20: floor=20 >=18 -> slope ✓.
    #   This is a guess. Mark with "?".
    #   Actually maybe simpler: constant region is where x < 18? Let's use x<18.
    #
    #   Also note E2 x=-5 -> -402.3253 (constant), consistent with x>=-5
    #   being regime B. But x=-5.1 in E6 -> 4.2 (regime A). So boundary
    #   for A/B is x=-5: x<-5 -> A, x>=-5 -> B.
    #
    #   For regime B constant region, output is noisy around -402.3.
    #   I'll model as -402.3 (mean). Noise can't be predicted.
    #   Actually maybe the noise is deterministic? Values like -402.3253,
    #   -402.2622... look random. Use -402.3.
    #
    #   Wait, could the constant be related to something? -402.3 ≈ -16.8*23.95.
    #   Or maybe it's -402.3 = some other computation. Let's just use -402.3.
    #
    # Summary:
    #   if x < -5: return -0.7 * floor(x)
    #   elif x < 18: return -402.3  (noisy constant; use mean)
    #   else: return -16.8 * floor(x)
    #
    #   Check E2 x=20: 20>=18 -> -16.8*20=-336 ✓.
    #   E2 x=10: 10<18 -> -402.3 ✓ (reported -402.197).
    #   E2 x=128: -16.8*128=-2150.4 ✓.
    #
    #   Boundary between constant and slope: uncertain between 15 and 19.5.
    #   I'll use 18 as best guess. Mark "?".

    x = probe["x"]
    y = []
    for xi in x:
        if xi < -5:
            y.append(-0.7 * math.floor(xi))
        elif xi < 18:  # ? boundary between 15 and 19.5
            y.append(-402.3)  # ? noisy constant, using mean
        else:
            y.append(-16.8 * math.floor(xi))
    return {"y": y}
