import math

def predict(probe):
    # Mechanism: f(x) = sign(x) * g(|x|), where g is a smooth monotone function.
    # Evidence:
    #  - Odd symmetry: f(-x) = -f(x) [E2: pairs -0.5/0.5, -20/20, -90/90; E4/E5 negatives mirror E3/E5 positives]
    #  - f(0) ~ 3.9155 (small positive offset, not exactly 0) [E1]
    #  - Near 0 the function is smooth and roughly linear with slope ~4.7 [E6: 0.05->4.19, 0.15->4.73, 0.3->5.53]
    #  - For large |x| it grows roughly linearly with slope ~4.75 [E1: 128->607.6, 64->305.9; slope ~4.75]
    #  - There is a "kink"/different regime near |x| ~ 2.5-3: negative side has a dip
    #    (f(-2.5)=-7.5, f(-2)=-5.1, f(-1.5)=-2.9) while positive side is smooth [E6]
    #  - Actually the whole thing looks like a smooth monotone-ish curve with an odd-ish structure
    #    but with a small asymmetry / offset near zero.
    #
    # Best simple model: f(x) = a*x + b*sign(x)*(1 - exp(-|x|/c)) + d
    # Fit roughly from data.

    x = probe["x"]
    out = []
    for v in x:
        try:
            v = float(v)
        except Exception:
            out.append(None)
            continue
        # Core model: odd part plus small constant offset
        # Large-|x| slope ~ 4.75, small offset ~ 3.9 at 0
        # Use f(x) = 4.75*x + 3.9*tanh(x/0.5) ... check signs
        # At x=0: 0 + 0 = 0, but we need ~3.9. So add offset.
        # Try: f(x) = 4.75*x + 3.9 + correction
        # But f(-128) = -595.7, 4.75*(-128) = -608, +3.9 = -604.1, close-ish.
        # f(128) = 607.6, 4.75*128=608, +3.9=611.9, a bit high.
        # Slope from 64 to 128: (607.6-305.9)/64 = 4.714
        # Slope from -64 to -128: (-595.7 - -295.7)/-64 = 4.6875
        # So slope ~4.7.
        # Intercept: at x=0, 3.9155. At large x, f(x) - 4.7x:
        # x=128: 607.6 - 601.6 = 6.0
        # x=64: 305.9 - 300.8 = 5.1
        # x=-128: -595.7 + 601.6 = 5.9
        # x=-64: -295.7 + 300.8 = 5.1
        # So f(x) ~ 4.7x + 5.5 for large |x|, but f(0)=3.9.
        # There's a transition region.
        #
        # Look at small x: slope near 0 ~ 4.7 too? f(0.05)=4.19, f(0.15)=4.73 => slope ~5.4
        # f(0.5)=6.59, f(1)=8.93 => slope ~4.7
        # f(-0.5)=1.96, f(-1)=-0.24 => slope ~4.4
        # So roughly linear with slope ~4.7 everywhere, plus offset that varies.
        #
        # Offset = f(x) - 4.7x:
        # x=0: 3.92
        # x=0.5: 6.59-2.35=4.24
        # x=1: 8.93-4.7=4.23
        # x=2: 13.65-9.4=4.25
        # x=5: 27.78-23.5=4.28
        # x=10: 51.35-47=4.35
        # x=32: 155.06-150.4=4.66
        # x=64: 305.9-300.8=5.1
        # x=128: 607.6-601.6=6.0
        # x=-0.5: 1.96+2.35=4.31
        # x=-1: -0.24+4.7=4.46
        # x=-2: -5.15+9.4=4.25
        # x=-5: -19.26+23.5=4.24
        # x=-10: -42.68+47=4.32
        # x=-20: -89.52+94=4.48
        # x=-32: -145.76+150.4=4.64
        # x=-64: -295.7+300.8=5.1
        # x=-128: -595.7+601.6=5.9
        #
        # So offset ~4.2-4.3 in the middle, rising to ~6 at extremes.
        # The offset rises roughly as 4.25 + small quadratic in x.
        # offset ~ 4.25 + 0.0001*x^2? At x=128: 4.25+1.64=5.89. At x=64: 4.25+0.41=4.66. 
        # At x=32: 4.25+0.10=4.35. Good match!
        # At x=10: 4.25+0.01=4.26. Good.
        # At x=0: 4.25, but actual 3.92. Hmm, near 0 slightly lower.
        #
        # So model: f(x) = 4.7*x + 4.25 + 0.0001*x^2
        # Check x=0: 4.25 (actual 3.92, off by 0.33)
        # x=-2.5: -11.75+4.25+0.0006 = -7.5 (actual -7.5!) 
        # x=-2: -9.4+4.25+0.0004 = -5.15 (actual -5.15!) 
        # x=-1.5: -7.05+4.25 = -2.8 (actual -2.93) close
        # x=-1: -4.7+4.25 = -0.45 (actual -0.24) close
        # x=-0.5: -2.35+4.25 = 1.9 (actual 1.96) 
        # x=0: 4.25 (actual 3.92) off
        # x=0.5: 2.35+4.25 = 6.6 (actual 6.59) 
        # x=1: 4.7+4.25 = 8.95 (actual 8.93) 
        # x=1.5: 7.05+4.25 = 11.3 (actual 11.29) 
        # x=2: 9.4+4.25 = 13.65 (actual 13.65) 
        # x=2.5: 11.75+4.25 = 16.0 (actual 16.0) 
        # x=3: 14.1+4.25 = 18.35 (actual 18.35) 
        # x=4: 18.8+4.25 = 23.05 (actual 23.07) 
        # x=5: 23.5+4.25 = 27.75 (actual 27.78) 
        # x=10: 47+4.25 = 51.25 (actual 51.35) 
        # x=20: 94+4.25+0.04 = 98.29 (actual 98.49) 
        # x=32: 150.4+4.25+0.1 = 154.75 (actual 155.06) 
        # x=64: 300.8+4.25+0.41 = 305.46 (actual 305.91) 
        # x=128: 601.6+4.25+1.64 = 607.49 (actual 607.61) 
        # x=-128: -601.6+4.25+1.64 = -595.71 (actual -595.68) 
        #
        # Very good fit! The only discrepancy is near x=0 where actual is slightly lower (3.92 vs 4.25).
        # That's a tiny local dip. Could be a tanh-like correction.
        # The dip: at x=0, -0.33; at x=+-0.5, ~0; at x=+-1, ~0.
        # Actually offset at x=0 is 3.92, at x=+-0.5 is ~4.25. So a narrow dip of width ~0.5.
        # Could be -0.33*exp(-(x/0.3)^2) or similar. Small effect.
        #
        # Let's include: f(x) = 4.7*x + 4.25 + 0.0001*x^2 - 0.33*exp(-(x/0.4)^2)
        
        val = 4.7*v + 4.25 + 0.0001*v*v - 0.33*math.exp(-(v/0.4)**2)
        out.append(round(val, 4))
    return {"y": out}
