import math

def predict(probe):
    # Beliefs:
    # 1. The box computes roughly y = g(x) * h(x), where g is a smooth "base" function
    #    and h is a large-magnitude growth factor that kicks in for |x| > ~1. [E1, E2]
    # 2. For small |x| (<= ~1), the function is close to a modest polynomial-ish
    #    behavior: f(0)=0, f(1)~-4.3, f(-1)~6.1, f(0.5)~0, f(-0.5)~6.24,
    #    f(0.1)~0, f(-0.1)~4.37, f(0.01)~0, f(-0.01)~3.95. [E2]
    # 3. There is a sign asymmetry: positive small x gives ~0, negative small x
    #    gives a positive value that grows toward ~4-6 as |x| grows to 1. [E2]
    # 4. For |x| >= ~1.5, magnitudes explode roughly like a high power of |x|
    #    times an exponential-ish factor; the sign depends on x. [E1, E2]
    # 5. At x=1.5, f~-11.8; at x=2, f~-60.2; at x=3, f~-427.5; at x=5, f~-7119.5;
    #    at x=10, f~-442789. Negative x mirrors with larger magnitudes:
    #    f(-2)~-67, f(-3)~-722.7, f(-5)~-12155.5, f(-10)~-618311. [E2]
    # 6. E1 values are enormous: x=88.2 -> -2.3e11, x=66 -> -4.0e10, etc.
    #    This is consistent with a steep growth like |x|^k * exp(a|x|) or similar,
    #    with sign mostly negative for large |x| but positive for x near 0.5? [E1]
    # 7. The exact mechanism is unclear; best guess: f(x) = A(x) * x^p * exp(b|x|)
    #    with a small-x correction region. We fit a smooth interpolant to the data.

    x = probe.get("x", [])
    out = []
    for v in x:
        try:
            out.append(_f(float(v)))
        except Exception:
            out.append(None)
    return {"y": out}


def _f(x):
    # Handle exact zero
    if x == 0.0:
        return -0.0

    ax = abs(x)

    # Small-|x| region: |x| <= 1.0
    # Evidence: f(0)=0, f(0.01)=0, f(0.1)=0, f(0.5)=0 for positive x;
    # negative x gives positive values: f(-0.01)=3.9452, f(-0.1)=4.3688,
    # f(-0.5)=6.2406, f(-1)=6.1.
    if ax <= 1.0:
        if x > 0:
            # Positive side is ~0 across this region (tiny values)
            return 0.0
        else:
            # Negative side: rises from ~3.95 at -0.01 to ~6.24 at -0.5, ~6.1 at -1
            # Model as a saturating curve: c1 + c2 * (1 - exp(-k*ax))
            # Fit: at ax=0.01 -> 3.9452, ax=0.1 -> 4.3688, ax=0.5 -> 6.2406, ax=1 -> 6.1
            # Use a simple interpolation-ish formula.
            # Try: 3.9 + 2.3*(1 - exp(-3*ax)) gives 3.97, 4.49, 5.62, 6.09
            # Slightly adjust.
            return 3.9 + 2.3 * (1.0 - math.exp(-3.0 * ax))

    # Medium region: 1 < |x| <= 1.5? f(1.5)=-11.8031, f(-1)=6.1, f(-2)=-67
    # Transition. Use a smooth blend.

    # Large-|x| region: |x| > 1.5
    # We need a function matching:
    #   x=1.5 -> -11.8031
    #   x=2   -> -60.2
    #   x=3   -> -427.5
    #   x=4   -> -2004.4
    #   x=5   -> -7119.5
    #   x=10  -> -442789.0
    #   x=-2  -> -67.0
    #   x=-3  -> -722.7
    #   x=-4  -> -3534.8
    #   x=-5  -> -12155.5
    #   x=-10 -> -618311.0
    #   x=21.3 -> -4.279e7
    #   x=66   -> -4.026e10
    #   x=88.2 -> -2.302e11
    #   x=72.7 -> -7.139e10
    #   x=2.9  -> -247.7
    #   x=-6   -> -33683.4
    #   x=-20.3 -> -3.993e7
    #   x=-24.3 -> -1.148e8
    #   x=-50.4 -> -8.609e9
    #   x=-61.7 -> -2.857e10

    # Try f(x) = -sign_correction * C * |x|^p * exp(k*|x|) for |x|>1.5
    # Use log-log fit for the exponential part.
    # Let's estimate: for positive x:
    # ln|f| at x=2: ln(60.2)=4.098
    # x=3: ln(427.5)=6.058
    # x=4: ln(2004.4)=7.603
    # x=5: ln(7119.5)=8.871
    # x=10: ln(442789)=12.999
    # x=21.3: ln(4.279e7)=17.572
    # x=66: ln(4.026e10)=24.419
    # x=88.2: ln(2.302e11)=26.162

    # Differences suggest roughly linear in x with slope ~0.25-0.3 for large x,
    # plus log term. Let's fit ln|f| = a + b*ln(x) + c*x.
    # Use x=5: 8.871 = a + b*1.609 + 5c
    # x=10: 12.999 = a + b*2.303 + 10c
    # x=66: 24.419 = a + b*4.190 + 66c
    # From first two: 4.128 = b*0.694 + 5c
    # From x=10 and x=66: 11.420 = b*1.887 + 56c
    # Solve: b = (4.128 - 5c)/0.694
    # 11.420 = ((4.128-5c)/0.694)*1.887 + 56c
    # 11.420 = 11.226 - 13.594c + 56c
    # 0.194 = 42.406c => c = 0.00457 -- too small, doesn't fit large x growth.
    # Try including x^2 term or different form.

    # Alternative: f(x) ~ -exp(a*x + b*ln(x) + c) for positive x.
    # Let's just do piecewise interpolation using known anchor points with
    # a smooth analytic form: f(x) = -C * |x|^p * exp(k*|x|^q)
    # Fit to a few points numerically by hand.

    # Use positive x anchors: (2,60.2), (5,7119.5), (10,442789), (66,4.026e10), (88.2,2.302e11)
    # Try f = C * x^p * exp(k*x)
    # ln f = ln C + p ln x + k x
    # x=2: 4.098 = lnC + 0.693p + 2k
    # x=5: 8.871 = lnC + 1.609p + 5k
    # x=10: 12.999 = lnC + 2.303p + 10k
    # x=66: 24.419 = lnC + 4.190p + 66k
    # x=88.2: 26.162 = lnC + 4.480p + 88.2k

    # From x=2 and x=5: 4.773 = 0.916p + 3k  (1)
    # From x=5 and x=10: 4.128 = 0.694p + 5k  (2)
    # Solve (1),(2): multiply (1) by 5, (2) by 3: 23.865 = 4.58p + 15k; 12.384 = 2.082p + 15k
    # 11.481 = 2.498p => p = 4.596; then 4.773 = 4.211 + 3k => k = 0.1873
    # Check x=66: lnC = 4.098 - 0.693*4.596 - 2*0.1873 = 4.098 - 3.185 - 0.375 = 0.538
    # predicted ln f(66) = 0.538 + 4.596*4.190 + 0.1873*66 = 0.538 + 19.257 + 12.362 = 32.157
    # Actual 24.419. Off by a lot. So pure exp(kx) too fast at large x.

    # Try f = C * x^p * exp(k * x^q) with q<1.
    # Use x=10 and x=66: ln(f66/f10) = p*ln(6.6) + k*(66^q - 10^q)
    # 24.419-12.999 = 11.420 = 1.887p + k*(66^q - 10^q)
    # x=5 and x=10: 4.128 = 0.694p + k*(10^q - 5^q)
    # x=2 and x=5: 4.773 = 0.916p + k*(5^q - 2^q)
    # Guess q=0.5: 66^0.5=8.124, 10^0.5=3.162, 5^0.5=2.236, 2^0.5=1.414
    # 11.420 = 1.887p + 4.962k
    # 4.128 = 0.694p + 0.926k
    # 4.773 = 0.916p + 0.822k
    # From last two: 0.645 = 0.222p - 0.104k -> p = (0.645+0.104k)/0.222 = 2.905 + 0.468k
    # Sub into 4.128: 4.128 = 0.694*(2.905+0.468k) + 0.926k = 2.016 + 0.325k + 0.926k = 2.016 + 1.251k
    # k = (4.128-2.016)/1.251 = 1.688
    # p = 2.905 + 0.468*1.688 = 3.695
    # Check 11.420 = 1.887*3.695 + 4.962*1.688 = 6.973 + 8.376 = 15.349, too high. q=0.5 not right.

    # This is getting complicated. Let's use a simpler approach: fit a smooth
    # function through anchor points using interpolation in log space.

    # For |x| > 1.5, use log-log polynomial fit: ln|f| = a0 + a1*ln|x| + a2*(ln|x|)^2
    # Use positive x anchors: (2,60.2), (5,7119.5), (10,442789), (66,4.026e10), (88.2,2.302e11)
    # ln x: 0.693, 1.609, 2.303, 4.190, 4.480
    # ln f: 4.098, 8.871, 12.999, 24.419, 26.162
    # Fit quadratic through (0.693,4.098), (2.303,12.999), (4.480,26.162)
    # Let t = ln x. Points: (0.693,4.098), (2.303,12.999), (4.480,26.162)
    # Solve for a0,a1,a2.
    # Using Lagrange or direct:
    # 4.098 = a0 + 0.693a1 + 0.480a2
    # 12.999 = a0 + 2.303a1 + 5.304a2
    # 26.162 = a0 + 4.480a1 + 20.070a2
    # Subtract 1 from 2: 8.901 = 1.610a1 + 4.824a2
    # Subtract 2 from 3: 13.163 = 2.177a1 + 14.766a2
    # From first: a1 = (8.901 - 4.824a2)/1.610 = 5.529 - 2.996a2
    # Sub: 13.163 = 2.177*(5.529 - 2.996a2) + 14.766a2 = 12.037 - 6.522a2 + 14.766a2 = 12.037 + 8.244a2
    # a2 = (13.163-12.037)/8.244 = 0.1366
    # a1 = 5.529 - 2.996*0.1366 = 5.120
    # a0 = 4.098 - 0.693*5.120 - 0.480*0.1366 = 4.098 - 3.548 - 0.066 = 0.484
    # Check x=5: t=1.609, ln f = 0.484 + 5.120*1.609 + 0.1366*2.589 = 0.484 + 8.238 + 0.354 = 9.076
    # Actual 8.871. Close.
    # Check x=66: t=4.190, ln f = 0.484 + 5.120*4.190 + 0.1366*17.556 = 0.484 + 21.453 + 2.398 = 24.335
    # Actual 24.419. Very close!
    # Check x=88.2: t=4.480, ln f = 0.484 + 5.120*4.480 + 0.1366*20.070 = 0.484 + 22.938 + 2.742 = 26.164
    # Actual 26.162. Excellent!

    # So for positive x > 1.5: f(x) = -exp(0.484 + 5.120*ln(x) + 0.1366*(ln x)^2)
    # For negative x, magnitudes are larger. Use same form with different coefficients.
    # Negative x anchors: (-2,67), (-3,722.7), (-4,3534.8), (-5,12155.5), (-10,618311),
    # (-20.3,3.993e7), (-24.3,1.148e8), (-50.4,8.609e9), (-61.7,2.857e10), (-6,33683.4)
    # ln|x|: 0.693, 1.099, 1.386, 1.609, 2.303, 3.011, 3.190, 3.920, 4.122, 1.792
    # ln f: 4.205, 6.583, 8.170, 9.406, 13.335, 17.503, 18.559, 22.876, 24.075, 10.425
    # Fit quadratic through (0.693,4.205), (2.303,13.335), (4.122,24.075)
    # 4.205 = a0 + 0.693a1 + 0.480a2
    # 13.335 = a0 + 2.303a1 + 5.304a2
    # 24.075 = a0 + 4.122a1 + 16.991a2
    # Subtract: 9.130 = 1.610a1 + 4.824a2
    # 10.740 = 1.819a1 + 11.687a2
    # From first: a1 = (9.130 - 4.824a2)/1.610 = 5.671 - 2.996a2
    # Sub: 10.740 = 1.819*(5.671 - 2.996a2) + 11.687a2 = 10.315 - 5.450a2 + 11.687a2 = 10.315 + 6.237a2
    # a2 = (10.740-10.315)/6.237 = 0.0681
    # a1 = 5.671 - 2.996*0.0681 = 5.467
    # a0 = 4.205 - 0.693*5.467 - 0.480*0.0681 = 4.205 - 3.789 - 0.033 = 0.383
    # Check x=-5: t=1.609, ln f = 0.383 + 5.467*1.609 + 0.0681*2.589 = 0.383 + 8.796 + 0.176 = 9.355
    # Actual 9.406. Close.
    # Check x=-61.7: t=4.122, ln f = 0.383 + 5.467*4.122 + 0.0681*16.991 = 0.383 + 22.535 + 1.157 = 24.075
    # Actual 24.075. Perfect!

    # For |x| between 1 and 1.5, blend between small-region and large-region.
    # At x=1.5, large-region formula gives:
    # t=ln(1.5)=0.4055, ln f = 0.484 + 5.120*0.4055 + 0.1366*0.1644 = 0.484 + 2.076 + 0.022 = 2.582
    # f = -exp(2.582) = -13.23. Actual -11.8031. Close enough.
    # At x=-1.5, large-region: t=0.4055, ln f = 0.383 + 5.467*0.4055 + 0.0681*0.1644 = 0.383 + 2.217 + 0.011 = 2.611
    # f = -exp(2.611) = -13.61. But small region at x=-1 gives +6.1, so there's a sign flip.
    # Hmm, at x=-1.5 we don't have data. At x=-2 it's -67. So sign flips between -1 and -2.

    # For simplicity, use large-region formula for |x| > 1.5, and handle 1 < |x| <= 1.5
    # by linear blend. Actually, let's just use large formula for |x| > 1.5 and
    # small formula for |x| <= 1.0, with a blend in between.

    def large_pos(x):
        t = math.log(x)
        return -math.exp(0.484 + 5.120*t + 0.1366*t*t)

    def large_neg(x):
        t = math.log(-x)
        return -math.exp(0.383 + 5.467*t + 0.0681*t*t)

    if ax > 1.5:
        if x > 0:
            return large_pos(x)
        else:
            return large_neg(x)

    # Blend region 1.0 < |x| <= 1.5
    # At ax=1, small region gives: pos=0, neg=6.1
    # At ax=1.5, large region gives: pos=-13.23, neg=-13.61
    # Blend linearly in ax from 1 to 1.5.
    w = (ax - 1.0) / 0.5  # 0 at 1, 1 at 1.5
    if x > 0:
        small_val = 0.0
        large_val = large_pos(1.5) if ax >= 1.5 else large_pos(ax)
        # Actually compute large at ax
        t = math.log(ax)
        large_val = -math.exp(0.484 + 5.120*t + 0.1366*t*t)
        return small_val * (1-w) + large_val * w
    else:
        small_val = 3.9 + 2.3 * (1.0 - math.exp(-3.0 * 1.0))  # at ax=1
        t = math.log(ax)
        large_val = -math.exp(0.383 + 5.467*t + 0.0681*t*t)
        return small_val * (1-w) + large_val * w
