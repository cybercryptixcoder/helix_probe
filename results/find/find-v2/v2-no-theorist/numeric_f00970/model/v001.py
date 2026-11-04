import math

def predict(probe):
    # Observations from E1:
    # x=88.2 -> -0.3221 ; x=66.0 -> -1.8758 ; x=-20.3 -> -0.594
    # x=-61.7 -> 1.308 ; x=2.9 -> 13.8362 ; x=-24.3 -> 0.8059
    # x=72.7 -> -0.9337 ; x=-50.4 -> -0.1205 ; x=-6.0 -> -1.2033
    # x=21.3 -> -0.3706
    #
    # Pattern guesses:
    # - Large |x| gives small |y| (looks like ~1/x or similar decay).
    #   e.g. x=88.2 -> -0.32, x=66 -> -1.88, x=72.7 -> -0.93 (all small).
    # - Small x near 0 gives large y: x=2.9 -> 13.84 (big spike).
    # - Sign of y doesn't obviously match sign of x.
    #
    # Best guess: y = sin(x)/x-like or 1/x with oscillation.
    # Try y = sin(x)/x? Check x=2.9: sin(2.9)/2.9 = 0.239/2.9 = 0.0824. No.
    # Try y = 1/x * something. x=2.9 -> 13.84 means numerator ~40.
    # Try y = cos(x)/x? x=2.9: cos(2.9)=-0.971, /2.9 = -0.335. No.
    # Try y = tan(x)? x=2.9: tan(2.9)=-0.239. No.
    # Try y = 1/(x - a) for some pole near x~2.5?
    #   x=2.9 -> 13.84 => x-a = 0.0723 => a=2.83
    #   x=21.3 -> -0.37 => 21.3-a = -2.7 => a=24. No.
    #
    # Try y = sin(x)/x^2? x=2.9: 0.239/8.41=0.028. No.
    # Try y = A*sin(B*x)/x. x=2.9 -> 13.84 => A*sin(2.9B)=40.1.
    #   x=21.3 -> -0.37 => A*sin(21.3B)=-7.88.
    #   x=66 -> -1.88 => A*sin(66B)=-124.
    #   x=88.2 -> -0.32 => A*sin(88.2B)=-28.4.
    #   x=-20.3 -> -0.59 => A*sin(-20.3B)=12.06 => A*sin(20.3B)=-12.06
    #   x=-61.7 -> 1.31 => A*sin(-61.7B)=-80.8 => A*sin(61.7B)=80.8
    #   x=-50.4 -> -0.12 => A*sin(50.4B)=6.07
    #   x=-24.3 -> 0.81 => A*sin(24.3B)=-19.6
    #   x=-6 -> -1.20 => A*sin(6B)=7.22
    #   x=72.7 -> -0.93 => A*sin(72.7B)=-67.9
    # Inconsistent signs for similar magnitudes (66 vs 61.7 opposite sign of sin).
    #
    # Try y = A*cos(B*x)/x:
    #   x=2.9 -> 13.84 => A*cos(2.9B)=40.1
    #   x=21.3 -> -0.37 => A*cos(21.3B)=-7.88
    #   x=66 -> -1.88 => A*cos(66B)=-124
    #   x=88.2 -> -0.32 => A*cos(88.2B)=-28.4
    #   x=-20.3 -> -0.59 => A*cos(20.3B)=12.06
    #   x=-61.7 -> 1.31 => A*cos(61.7B)=-80.8
    #   x=-50.4 -> -0.12 => A*cos(50.4B)=6.07
    #   x=-24.3 -> 0.81 => A*cos(24.3B)=-19.6
    #   x=-6 -> -1.20 => A*cos(6B)=-7.22
    #   x=72.7 -> -0.93 => A*cos(72.7B)=-67.9
    # cos is even, so cos(61.7B) should equal cos(-61.7B). But we need
    # A*cos(61.7B)=-80.8 and A*cos(20.3B)=12.06 — different, fine.
    # Check consistency: cos(2.9B) and cos(21.3B) etc. Hard without solving.
    #
    # Given the difficulty, best guess: y = cos(x)/x * something, or a
    # rational/oscillatory function. Try y = cos(x)/x directly:
    #   x=2.9: cos(2.9)/2.9 = -0.971/2.9 = -0.335. Observed 13.84. No.
    #
    # Try y = 1/(x*sin(x))? x=2.9: 1/(2.9*0.239)=1.44. No.
    #
    # Try y = cot(x)/x? x=2.9: cot(2.9)=-4.18, /2.9=-1.44. No.
    #
    # Try y = tan(x)/x? x=2.9: -0.239/2.9=-0.082. No.
    #
    # Try y = 1/(x - 2.9)? x=2.9 undefined. No.
    #
    # Try y = A/(x^2) * sin(Bx)? x=2.9: A*sin(2.9B)/8.41=13.84 => A*sin(2.9B)=116.4
    #   x=21.3: A*sin(21.3B)/453.7=-0.37 => A*sin(21.3B)=-167.9
    #   x=66: A*sin(66B)/4356=-1.88 => A*sin(66B)=-8189
    #   x=88.2: A*sin(88.2B)/7779=-0.32 => A*sin(88.2B)=-2489
    #   x=-20.3: A*sin(-20.3B)/412=-0.59 => A*sin(20.3B)=243.4
    #   x=-61.7: A*sin(-61.7B)/3807=1.31 => A*sin(61.7B)=4987
    #   x=-50.4: A*sin(50.4B)/2540=-0.12 => A*sin(50.4B)=304.8
    #   x=-24.3: A*sin(-24.3B)/590=0.81 => A*sin(24.3B)=-477.9
    #   x=-6: A*sin(-6B)/36=-1.20 => A*sin(6B)=43.2
    #   x=72.7: A*sin(72.7B)/5285=-0.93 => A*sin(72.7B)=4915
    # Inconsistent: sin(66B) and sin(61.7B) both need large positive but
    # observed signs differ. Not a simple sinusoid.
    #
    # Given time constraints, best guess: y = cos(x)/x^2 * C.
    # x=2.9: cos(2.9)/8.41 = -0.1155. Need 13.84 => C=-119.8
    # x=21.3: cos(21.3)/453.7 = -0.0013. *-119.8 = 0.156. Observed -0.37. Close-ish sign wrong.
    #
    # Try y = -cos(x)/x^2 * C? x=2.9: 0.1155*C=13.84 => C=119.8
    # x=21.3: 0.0013*119.8=0.156. Observed -0.37. Sign wrong.
    #
    # Try y = sin(x)/x^2 * C. x=2.9: 0.239/8.41=0.0284*C=13.84 => C=487
    # x=21.3: sin(21.3)=0.656, /453.7=0.00145*487=0.705. Observed -0.37.
    # x=66: sin(66)=-0.0266, /4356=-6.1e-6*487=-0.003. Observed -1.88. No.
    #
    # The data is hard to fit. Best guess: y = 1/(x*sin(x)) scaled, or
    # y = cos(x)/x with a pole. Given x=2.9 gives huge value, likely a pole
    # near x~2.5-3. And x=21.3 gives -0.37, x=66 gives -1.88 (larger magnitude
    # at larger x — odd for 1/x decay).
    #
    # Actually check: |y| at x=66 is 1.88, at x=88.2 is 0.32, at x=72.7 is 0.93.
    # Not monotonic. Looks oscillatory. Try y = sin(x)/x * C with C large:
    # x=2.9: 0.239/2.9=0.0824*C=13.84 => C=168
    # x=21.3: 0.656/21.3=0.0308*168=5.17. Observed -0.37. No.
    #
    # Try y = sin(x)*C/x^2? Already tried.
    #
    # Try y = cos(x)*C/x:
    # x=2.9: -0.971/2.9=-0.335*C=13.84 => C=-41.3
    # x=21.3: cos(21.3)=-0.547, /21.3=-0.0257*-41.3=1.06. Observed -0.37. No.
    #
    # Try y = tan(x)*C/x:
    # x=2.9: tan(2.9)=-0.239, /2.9=-0.0824*C=13.84 => C=-168
    # x=21.3: tan(21.3)=0.766, /21.3=0.036*-168=-6.05. Observed -0.37. No.
    #
    # I'll go with a best-guess oscillatory rational: y = sin(x)/x^2 * A + cos(x)/x * B
    # Fitting is too hard by hand. Use y = 1/(x*sin(x)) as a guess? 
    # x=2.9: 1/(2.9*0.239)=1.44. No.
    #
    # Final guess: y = cos(x)/x^2 * 120 (rough fit at x=2.9).
    # This is a placeholder hypothesis; mark with ?.
    #
    # ? Best guess: y = -120*cos(x)/x^2 (fits x=2.9 magnitude, sign uncertain)
    out = []
    for x in probe.get("x", []):
        try:
            if x == 0:
                out.append(None)
            else:
                out.append(-120.0 * math.cos(x) / (x * x))
        except Exception:
            out.append(None)
    return {"y": out}
