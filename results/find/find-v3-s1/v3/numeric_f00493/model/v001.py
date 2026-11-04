import math

def predict(probe):
    # Model: f(x) = sign(x) * g(|x|), where g(t) = 0 for t < 1, and
    # g(t) = c * t^p * (1 + small correction) for t >= 1.
    # Evidence:
    # - f(x)=0 for |x|<1 (E2, E4, E8, E10: 0.98,0.99 -> 0; 1.0 -> -4.3)
    # - At |x|=1 exactly, f(1)=-4.3, f(-1)=6.1 (E2, E10) -- boundary values.
    # - Positive side: f(1)=-4.3, f(2)=-60.2, f(3)=-427.5, f(10)=-442789,
    #   f(100)=-4.91e11 (E2). Ratio f(10)/f(1) ~ 1.03e5, f(100)/f(10)~1.11e6.
    #   log-log slope: ln(442789/4.3)/ln(10) ~ 5.01; ln(4.9e11/4.4e5)/ln(10)~6.05.
    #   So p is not constant; magnitude grows faster than a single power.
    # - Negative side: f(-1)=6.1, f(-2)=-67, f(-3)=-722.7, f(-10)=-618311,
    #   f(-100)=-5.09e11 (E2). |f(-x)| slightly larger than |f(x)| (E12, E14).
    # - E14 shows negative side is NOT odd-symmetric: |f(-x)|>|f(x)| systematically.
    # - Sign: f(x)<0 for x>1, f(x)>0 for -1<x<0 (E8: -0.05..-0.55 -> positive),
    #   f(x)<0 for x<-1 (E2: -2,-3,-10 -> negative). f(-1)=+6.1 is boundary.
    # - Near boundary: f(1.01)~-4.38, f(1.05)~-4.73, f(1.1)~-5.23 (E10).
    #   f(-1.01)~12.07, f(-1.05)~11.46, f(-1.1)~10.53 (E10) -- negative side
    #   jumps to ~12 just past -1 then decreases toward -2.
    # - For 0<|x|<1: f=0 except tiny negatives give small positive (E8: -0.05->4.13).
    #   Actually E8 shows -0.05..-0.55 give positive values ~4-6.4, so NOT zero
    #   for negative small |x|! Re-examine: E8 x=-0.05 -> 4.1301, -0.55 -> 6.4172.
    #   And E2: x=-0.5 -> 6.2406, x=-0.1 -> 4.3688. So negative side in (-1,0)
    #   is positive and nonzero. Positive side (0,1) is zero (E4, E8).
    # So: region (0,1): 0. Region (-1,0): positive, roughly 4-6.4.
    # Region x>=1: negative, growing. Region x<=-1: negative for x<-1,
    #   with |f| slightly larger than positive side.

    def g_pos(t):
        # positive side t>=1, returns magnitude (positive), f=-g_pos
        # fit log g = a + b*ln(t) + c*(ln t)^2 using points
        # t=1: g=4.3; t=2: 60.2; t=3: 427.5; t=10: 442789; t=100: 4.913e11
        # Use quadratic in ln t
        lt = math.log(t)
        # coefficients from rough fit
        # ln g at t=1: ln4.3=1.459; t=2: 4.098; t=3: 6.058; t=10: 12.999; t=100: 26.92
        # fit a + b*u + c*u^2, u=ln t
        # u=0: a=1.459
        # u=ln2=.693: a+.693b+.480c=4.098
        # u=ln10=2.303: a+2.303b+5.302c=12.999
        # u=ln100=4.605: a+4.605b+21.21c=26.92
        # From these: solve
        a = 1.459
        # .693b+.480c=2.639
        # 2.303b+5.302c=11.540
        # 4.605b+21.21c=25.461
        # subtract: from eq1: b=(2.639-.480c)/.693=3.808-.693c
        # eq2: 2.303(3.808-.693c)+5.302c=11.540 -> 8.770-1.596c+5.302c=11.540
        # 3.706c=2.770 -> c=0.7474; b=3.808-.518=3.290
        b = 3.290
        c = 0.7474
        return math.exp(a + b*lt + c*lt*lt)

    def g_neg(t):
        # negative side t>=1, magnitude, f=-g_neg for x<-1
        # t=1: 6.1; t=2: 67; t=3: 722.7; t=10: 618311; t=100: 5.093e11
        # ln: 1.808; 4.205; 6.583; 13.335; 26.956
        a = 1.808
        # u=ln2=.693: .693b+.480c=2.397
        # u=ln10=2.303: 2.303b+5.302c=11.527
        # u=ln100=4.605: 4.605b+21.21c=25.148
        # b=(2.397-.480c)/.693=3.459-.693c
        # 2.303(3.459-.693c)+5.302c=11.527 -> 7.966-1.596c+5.302c=11.527
        # 3.706c=3.561 -> c=0.9609; b=3.459-.666=2.793
        b = 2.793
        c = 0.9609
        lt = math.log(t)
        return math.exp(a + b*lt + c*lt*lt)

    def g_small_neg(t):
        # 0<t<1, x=-t, positive value ~ 4-6.4
        # E8: t=.05->4.13, .15->4.61, .25->5.11, .35->5.60, .45->6.04, .55->6.42
        # E2: t=.5->6.24, t=.1->4.37
        # roughly linear in t: value ~ 4.1 + 4.2*t? t=.5: 6.2 yes; t=.1:4.52 close
        return 4.1 + 4.2*t

    out = []
    for x in probe["x"]:
        if x is None:
            out.append(None); continue
        try:
            if x > 1.0:
                out.append(-g_pos(x))
            elif x == 1.0:
                out.append(-4.3)
            elif 0 < x < 1.0:
                out.append(-0.0)
            elif x == 0.0:
                out.append(-0.0)
            elif -1.0 < x < 0:
                out.append(g_small_neg(-x))
            elif x == -1.0:
                out.append(6.1)
            else:  # x < -1
                out.append(-g_neg(-x))
        except Exception:
            out.append(None)
    return {"y": out}
