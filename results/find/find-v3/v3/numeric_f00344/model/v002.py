import math

def predict(probe):
    # Beliefs:
    # - For x in (-100, 0): f(x) = -1.2x^4 -3x^3 +0.9x^2 -1.6x -11.7? No — see below.
    # - Actually the "quartic" fit was a coincidence of mid-range data. E22 shows far-negative
    #   values clamp to ~-24973124.6 for x <= -100. E2 shows f(-100)=-24973124.5982,
    #   f(-80)=-47610123.7, f(-60)=-14900675.7 — NOT monotone, so it's not a simple quartic.
    # - Re-examine: E2 f(-80)=-47610123.7, f(-60)=-14900675.7, f(-40)=-2878507.7,
    #   f(-20)=-167619.7, f(-10)=-8905.7, f(-5)=-356.2, f(-2)=-0.1, f(-1)=-7.4.
    #   These match cubic -1.2x^4... no. Let's check cubic a*x^3+b on negative side:
    #   f(-10)=-8905.7, f(-20)=-167619.7: ratio 18.82, 2^3=8. Not cubic.
    #   f(-20)/f(-10)=18.82 -> log2=4.23. f(-40)/f(-20)=17.17 -> 4.10.
    #   f(-60)/f(-40)=5.18 -> 2.37. f(-80)/f(-60)=3.19 -> 1.68. f(-100)/f(-80)=0.52.
    #   So it rises then falls — there's a peak around x=-80, then clamps at -100.
    # - E22: for x in [-128,-100], f ≈ -24973124.6 (constant clamp).
    # - E2: f(-100)=-24973124.5982, f(-80)=-47610123.7 (larger magnitude).
    #   So the clamp region is x <= -100? But f(-80) is bigger. So clamp is x<=-100.
    #   Wait E2 f(-100)=-24973124.5982 matches the clamp value. And f(-80)=-47610123.7
    #   is NOT clamped. So clamp applies for x <= -100.
    # - For x in (-100, 0): the quartic -1.2x^4-3x^3+0.9x^2-1.6x-11.7 fits E2 values
    #   at -80? Check: -1.2*40960000 -3*(-512000)+0.9*6400 -1.6*(-80) -11.7
    #   = -49152000 +1536000 +5760 +128 -11.7 = -47610123.7. YES!
    #   At -60: -1.2*12960000 -3*(-216000)+0.9*3600+96-11.7
    #   = -15552000+648000+3240+96-11.7 = -14900675.7. YES!
    #   At -100: -1.2*1e8 -3*(-1e6)+0.9*10000+160-11.7
    #   = -120000000+3000000+9000+160-11.7 = -116990851.7. But observed -24973124.5982!
    #   So at x=-100 the clamp kicks in. So clamp region: x <= -100 (or x < -100?).
    #   E22 has x=-100 -> -24973124.686 (clamped). So clamp for x <= -100.
    #   Boundary: quartic at -100 = -116990851.7, clamp value -24973124.6.
    #   What's the clamp value exactly? ~-24973124.6. Looks like -24973124.6.
    # - Positive side: quartic -1.2x^4-3x^3+0.9x^2-1.6x-36.8 fits all positive data
    #   including large (E19 f(127)=-318304442.1: check -1.2*127^4... 127^4=260144641,
    #   *1.2=312173569.2; -3*127^3=-3*2048383=-6145149; 0.9*16129=14516.1;
    #   -1.6*127=-203.2; sum=-312173569.2-6145149+14516.1-203.2-36.8=-318304442.1 YES)
    #   So positive side is pure quartic, no clamp observed up to 127.
    # - At x=0: E2/E6 show f(0)=472.73. That's a special spike at exactly 0.
    # - So: x=0 -> 472.73; x>0 -> quartic-36.8; -100<x<0 -> quartic-11.7;
    #   x<=-100 -> -24973124.6 (clamp).
    # - What about x between -100 and 0 exactly at boundary? E22 includes -100 clamped.
    #   Use x <= -100 for clamp.
    # - Is there a clamp on positive side? E19 f(127)=-318304442.1 matches quartic, no clamp.
    #   E22 only tested negative. Assume no positive clamp.
    # - Check E5 f(-102.2)=-24973124.4433: clamped. YES (x<=-100).
    # - Check E7 f(-124.4)=-24973124.5307: clamped. YES.
    # - Check E9 f(-127.7)=-24973124.5905: clamped. YES.
    # - Check E11 f(-107.4)=-24973124.6987, f(-100.1)=-24973124.5997: clamped. YES.
    # - Check E15 f(-105.0)=-24973124.4816: clamped. YES.
    # - Check E23 f(-116.4)=-24973124.6111, f(-121.2)=-24973124.8495: clamped. YES.
    # - Check E21 f(-98.0)=-24973124.5663: x=-98 > -100, so should be quartic!
    #   quartic at -98: -1.2*92236816 -3*(-941192)+0.9*9604+156.8-11.7
    #   = -110684179.2+2823576+8643.6+156.8-11.7 = -107851814.5. But observed -24973124.5663!
    #   So -98 IS clamped. So clamp boundary is higher than -100. 
    #   E21 f(-98)=-24973124.5663 clamped. E2 f(-80)=-47610123.7 NOT clamped.
    #   So boundary between -98 and -80. E23 f(-90.5)=-78265076.875.
    #   quartic at -90.5: -1.2*90.5^4 -3*(-90.5)^3+0.9*90.5^2+1.6*90.5-11.7
    #   90.5^2=8190.25, ^3=741217.625, ^4=67080195.06
    #   -1.2*67080195.06=-80496234.07; +3*741217.625=2223652.875; +0.9*8190.25=7371.225;
    #   +144.8; -11.7 => -80496234.07+2223652.875+7371.225+144.8-11.7=-78265076.87. YES!
    #   So -90.5 is NOT clamped (matches quartic). So boundary between -98 and -90.5.
    #   E21 f(-98) clamped, E23 f(-90.5) not. Need boundary. 
    #   E15 f(-79.5)=-46421488.725 (quartic, not clamped). 
    #   E9 f(-79.1)=-45486718.6493 (quartic).
    #   E11 f(-100.1) clamped, f(-107.4) clamped.
    #   E5 f(-102.2) clamped.
    #   So clamped: -98, -100.1, -102.2, -105, -107.4, -116.4, -121.2, -124.4, -127.7.
    #   Not clamped: -90.5, -79.5, -79.1, -80, -80.2.
    #   Boundary between -98 and -90.5. Guess: -95? Or maybe -96? 
    #   Let me check E2 f(-100)=-24973124.5982 clamped, f(-80)=-47610123.7 not.
    #   Hmm, no data between -98 and -90.5. I'll guess boundary at -95 (midpoint-ish).
    #   Actually maybe it's -96 or -97. Let me look for cleaner: perhaps the clamp is where
    #   quartic magnitude exceeds some threshold? quartic(-98)=-107851814, quartic(-90.5)=-78265076.
    #   Threshold between 78M and 108M. Hmm. Or maybe clamp is |x|>=95? 
    #   E22 tested -100 to -128 all clamped. E2 -100 clamped. 
    #   I'll guess boundary x <= -95 (i.e., x < -94.5?). Use x <= -95.
    #   Actually let me reconsider: maybe the clamp is at a specific x where quartic = clamp value.
    #   quartic(-90.5)=-78265076, quartic(-98)=-107851814. Clamp=-24973124.6.
    #   That's much smaller magnitude than quartic at -90.5. So clamp isn't "when quartic exceeds".
    #   It's a hard region boundary. I'll guess -95.
    # - Clamp value: ~-24973124.6. Slight noise. Use -24973124.6.
    def f(x):
        if x == 0:
            return 472.73
        if x > 0:
            return -1.2*x**4 - 3*x**3 + 0.9*x**2 - 1.6*x - 36.8
        # x < 0
        if x <= -95:  # ? boundary guessed between -98 (clamped) and -90.5 (not)
            return -24973124.6
        return -1.2*x**4 - 3*x**3 + 0.9*x**2 - 1.6*x - 11.7
    xs = probe.get("x", [])
    return {"y": [f(x) for x in xs]}
