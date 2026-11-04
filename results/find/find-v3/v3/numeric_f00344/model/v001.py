import math

def predict(probe):
    # Model: f(x) = a*x^3 + b, with different b on each side of 0.
    # From E8 (positive side): f(10)= -14962.8, f(20)= -215708.8
    #   a*1000 + b = -14962.8 ; a*8000 + b = -215708.8
    #   7000a = -200746 -> a = -28.678 ; b = -14962.8 + 28678 = 13715.2? no...
    # Recompute: a*8000 - a*1000 = -215708.8 + 14962.8 = -200746 -> a = -28.678
    #   b = -14962.8 - (-28.678*1000) = -14962.8 + 28678 = 13715.2  -> wrong sign check
    # Try f(1)= -41.7, f(2)= -79.6: a + b = -41.7 ; 8a + b = -79.6 -> 7a = -37.9 -> a=-5.414
    #   b = -41.7 + 5.414 = -36.286. Hmm not clean.
    # Use E20 negative side: f(-2)= -0.1, f(-10)= -8905.7
    #   -8a + b = -0.1 ; -1000a + b = -8905.7 -> 992a = -8905.6 -> a = -8.9774
    #   b = -0.1 + 8*(-8.9774) = -71.9. Not matching -11.7.
    # Try f(-2)=-0.1, f(-3)=-15.0: -8a+b=-0.1 ; -27a+b=-15 -> 19a=-14.9 -> a=-0.7842
    #   b = -0.1 - 8*0.7842 = -6.37. Not clean either.
    # E18: f(-12)=-19562.1, f(-9)=-5610.6: -1728a+b=-19562.1; -729a+b=-5610.6
    #   999a = -13951.5 -> a = -13.965 ; b = -5610.6 + 729*13.965 = -5610.6+10180.5=4569.9 no
    # Let me use large values. E19: f(127)=-318304442.1, f(115.1)=-215174558.3561
    #   127^3=2048383, 115.1^3=1524753.551
    #   a*(2048383-1524753.551) = -318304442.1+215174558.3561 = -103129883.7439
    #   a = -103129883.7439/523629.449 = -196.95... hmm let's compute: 523629.449*197=103155001
    #   So a ≈ -196.95? Let's check with E17: f(101.9)=-132548352.1265
    #   101.9^3 = 1058... 101.9^2=10383.61, *101.9=1058090.859
    #   a*1058090.859 + b = -132548352.1265
    #   Using a=-196.95: -196.95*1058090.859 = -208391... = -208391,  let's compute properly
    #   1058090.859 * 196.95 = 208391... 1058090.859*200=211618171.8, minus 1058090.859*3.05=3227177.12
    #   = 208390994.68, so -208390994.68 + b = -132548352.13 -> b = 75842642.55. Not constant.
    # Hmm. Let me reconsider: maybe f(x) = a*x^3 + b with different a on each side?
    # E8 positive: f(10)=-14962.8, f(20)=-215708.8, f(40)=-3262660.8
    #   ratios: 215708.8/14962.8=14.42, 3262660.8/215708.8=15.13. Not cubic (would be 8x).
    # Wait 20^3/10^3 = 8, but ratio is 14.4. So not pure cubic!
    # Check f(40)/f(20) = 3262660.8/215708.8 = 15.13, 40^3/20^3=8. Not cubic.
    # So it's higher power? f(80)/f(40)=50682404.8/3262660.8=15.53. 80^3/40^3=8.
    # Ratio ~15.5 each doubling. 2^k = 15.5 -> k = log2(15.5)=3.95. So ~x^4!
    # Check: f(10)=-14962.8, f(20)=-215708.8: 215708.8/14962.8=14.42, 2^4=16. Close-ish.
    # f(20)/f(10) should be 16 for x^4. It's 14.42. Hmm.
    # Try x^4 with offset: f(10)=a*10000+b=-14962.8; f(20)=a*160000+b=-215708.8
    #   150000a = -200746 -> a=-1.3383; b=-14962.8+13383=-1579.8
    #   f(40)=a*2560000+b = -1.3383*2560000-1579.8 = -3426048-1579.8=-3427627.8 vs -3262660.8. Off.
    # Try x^4 exactly: f(20)/f(10)=16 -> would be -239404.8 vs -215708.8. Off by 10%.
    # Maybe f(x) = a*x^4 + b*x^3 + ...? Or a*x^3.9?
    # Let's fit power: log(f(20)/f(10))/log(2) = log(14.42)/log(2)=3.85
    #   log(f(40)/f(20))/log2 = log(15.13)/log2=3.92
    #   log(f(80)/f(40))/log2 = log(15.53)/log2=3.96
    # Approaches 4. Maybe f(x)=a*x^4 + lower terms.
    # E8: f(1)=-41.7, f(2)=-79.6, f(3)=-211.7, f(5)=-1147.3
    #   If a*x^4+b: f(1)=a+b=-41.7; f(2)=16a+b=-79.6 -> 15a=-37.9 -> a=-2.527; b=-39.17
    #   f(3)=81*(-2.527)-39.17=-204.7-39.17=-243.8 vs -211.7. Off.
    # Try a*x^4 + c*x^2 + b? Or maybe it's a*x^3 + b*x with different behavior.
    # Actually let me reconsider. E16 gives clean values: f(2)=-79.6, f(3)=-211.7, f(4)=-528.0
    #   f(5)=-1147.3, f(6)=-2217.2, f(7)=-3914.1, f(8.5)=-8091.825
    # Differences: -132.1, -316.3, -619.3, -1069.9, -1696.9
    # 2nd diff: -184.2, -303, -450.6, -627
    # 3rd diff: -118.8, -147.6, -176.4 -> 4th diff: -28.8, -28.8. Constant 4th difference!
    # So it's a quartic! a*x^4 + ... with leading coeff: 4th diff = 24a = -28.8 -> a=-1.2
    # So f(x) = -1.2*x^4 + ... Let's find lower terms.
    # f(2)=-79.6: -1.2*16 + rest = -19.2 + rest = -79.6 -> rest = -60.4
    # f(3)=-211.7: -1.2*81 + rest = -97.2 + rest = -211.7 -> rest = -114.5
    # f(4)=-528: -1.2*256 + rest = -307.2 + rest = -528 -> rest = -220.8
    # f(5)=-1147.3: -1.2*625 + rest = -750 + rest = -1147.3 -> rest = -397.3
    # rest values: -60.4, -114.5, -220.8, -397.3
    # diffs: -54.1, -106.3, -176.5
    # 2nd: -52.2, -70.2
    # 3rd: -18. Hmm not constant. Let me try cubic rest: b*x^3+c*x^2+d*x+e
    # Actually maybe f(x) = -1.2*x^4 + b*x^3 + c*x^2 + d*x + e
    # Let me use E16 values: x=2,3,4,5,6,7
    # f(2)=-79.6, f(3)=-211.7, f(4)=-528, f(5)=-1147.3, f(6)=-2217.2, f(7)=-3914.1
    # 4th difference constant = -28.8 means leading coeff = -28.8/24 = -1.2. Good.
    # Let me try f(x) = -1.2*x^4 + b*x^3 + c*x^2 + d*x + e
    # Actually let me just check if it's simpler: maybe f(x) = -1.2*x^4 + something.
    # f(2)=-79.6: -19.2 + g(2) = -79.6 -> g(2)=-60.4
    # f(3)=-211.7: -97.2 + g(3) = -211.7 -> g(3)=-114.5
    # f(4)=-528: -307.2 + g(4) = -528 -> g(4)=-220.8
    # f(5)=-1147.3: -750 + g(5) = -1147.3 -> g(5)=-397.3
    # f(6)=-2217.2: -1555.2 + g(6) = -2217.2 -> g(6)=-662
    # f(7)=-3914.1: -2881.2 + g(7) = -3914.1 -> g(7)=-1032.9
    # g diffs: -54.1, -106.3, -176.5, -264.7, -370.9
    # 2nd: -52.2, -70.2, -88.2, -106.2 -> 3rd: -18, -18, -18. Constant!
    # So g is cubic with leading coeff -18/6 = -3. g(x) = -3*x^3 + ...
    # g(2)=-60.4: -24 + h(2) = -60.4 -> h(2)=-36.4
    # g(3)=-114.5: -81 + h(3) = -114.5 -> h(3)=-33.5
    # g(4)=-220.8: -192 + h(4) = -220.8 -> h(4)=-28.8
    # g(5)=-397.3: -375 + h(5) = -397.3 -> h(5)=-22.3
    # g(6)=-662: -648 + h(6) = -662 -> h(6)=-14
    # g(7)=-1032.9: -1029 + h(7) = -1032.9 -> h(7)=-3.9
    # h diffs: 2.9, 4.7, 6.5, 8.3, 10.1 -> 2nd: 1.8, 1.8, 1.8. Constant!
    # h is quadratic with leading 1.8/2 = 0.9. h(x) = 0.9*x^2 + ...
    # h(2)=-36.4: 3.6 + k(2) = -36.4 -> k(2)=-40
    # h(3)=-33.5: 8.1 + k(3) = -33.5 -> k(3)=-41.6
    # h(4)=-28.8: 14.4 + k(4) = -28.8 -> k(4)=-43.2
    # h(5)=-22.3: 22.5 + k(5) = -22.3 -> k(5)=-44.8
    # k diffs: -1.6, -1.6, -1.6. Linear! k(x) = -1.6*x + m
    # k(2)=-40: -3.2 + m = -40 -> m = -36.8
    # So f(x) = -1.2*x^4 - 3*x^3 + 0.9*x^2 - 1.6*x - 36.8  for positive side!
    # Check f(1) = -1.2 - 3 + 0.9 - 1.6 - 36.8 = -41.7. YES! matches E8 f(1)=-41.7
    # Check f(10) = -1.2*10000 - 3*1000 + 0.9*100 - 1.6*10 - 36.8
    #   = -12000 - 3000 + 90 - 16 - 36.8 = -14962.8. YES!
    # Check f(20) = -1.2*160000 - 3*8000 + 0.9*400 - 32 - 36.8
    #   = -192000 - 24000 + 360 - 32 - 36.8 = -215708.8. YES!
    # Positive side: f(x) = -1.2*x^4 - 3*x^3 + 0.9*x^2 - 1.6*x - 36.8
    # Now negative side. E20: f(-2)=-0.1, f(-3)=-15, f(-4)=-106.1, f(-5)=-356.2
    #   f(-6)=-876.9, f(-7)=-1808.6, f(-8)=-3320.5, f(-10)=-8905.7
    # Let me check if same formula: f(-2) = -1.2*16 - 3*(-8) + 0.9*4 - 1.6*(-2) - 36.8
    #   = -19.2 + 24 + 3.6 + 3.2 - 36.8 = -25.2. But observed -0.1. Different!
    # So negative side has different offset. Let's find it.
    # Try f(x) = -1.2*x^4 - 3*x^3 + 0.9*x^2 - 1.6*x + C
    # f(-2) = -25.2 + (C+36.8) = -0.1 -> C+36.8 = 25.1 -> C = -11.7. 
    # So negative side: f(x) = -1.2*x^4 - 3*x^3 + 0.9*x^2 - 1.6*x - 11.7
    # Check f(-3) = -1.2*81 - 3*(-27) + 0.9*9 - 1.6*(-3) - 11.7
    #   = -97.2 + 81 + 8.1 + 4.8 - 11.7 = -15.0. YES!
    # Check f(-10) = -1.2*10000 - 3*(-1000) + 0.9*100 - 1.6*(-10) - 11.7
    #   = -12000 + 3000 + 90 + 16 - 11.7 = -8905.7. YES!
    # So the two sides differ ONLY in the constant term: -36.8 vs -11.7.
    # Difference = 25.1. Interesting.
    # Now what about near zero? E14: f(0.0005)=-36.8008, f(-0.0005)=-11.6992
    #   Formula positive at 0.0005: -1.6*0.0005 - 36.8 = -0.0008-36.8 = -36.8008. YES!
    #   Formula negative at -0.0005: -1.6*(-0.0005) - 11.7 = 0.0008-11.7 = -11.6992. YES!
    # So it's a jump discontinuity at 0: left limit -11.7, right limit -36.8.
    # What about x=0 exactly? E2 had x=0. Need to check. Not in observations shown directly.
    # E6 had x=0. Let me guess: probably one side or undefined. I'll guess it uses... 
    # Actually the problem says "null where f is undefined". Let me check E6 - not shown.
    # I'll assume f(0) uses the negative branch (x<=0) or maybe positive. Uncertain.
    # Let me check E10: f(-1e-05) = -11.7. Formula neg: -1.6*(-1e-5)-11.7 = -11.69998 ≈ -11.7. YES.
    # E10: f(0.01)=-36.8159. Formula pos: -1.6*0.01-36.8 = -0.016-36.8=-36.816. YES!
    # E10: f(0.05)=-36.8781. Formula: -1.6*0.05-36.8=-0.08-36.8=-36.88. Close (rounding).
    # Great, so the model is confirmed.
    # For x=0: I'll guess it's the negative branch (x<=0). Uncertain, mark with ?
    def f(x):
        base = -1.2*x**4 - 3*x**3 + 0.9*x**2 - 1.6*x
        if x > 0:
            return base - 36.8
        else:
            return base - 11.7
    xs = probe.get("x", [])
    return {"y": [f(x) for x in xs]}
