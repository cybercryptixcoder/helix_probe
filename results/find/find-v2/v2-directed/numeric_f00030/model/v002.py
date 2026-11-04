import math

def predict(probe):
    # Model of the black box f(x), an MLP approximating a piecewise function.
    #
    # Observations / beliefs:
    # - Baseline is a gentle bowl: f rises toward the edges, minimum near x=0
    #   [E1: f(0)=-1.756 is lowest; f(±120)≈-1.48/-1.52 higher].
    # - There is a NARROW SPIKE/DIP region near x=0: a sharp dip around x≈±0.6
    #   and a local peak at x=0. Actually f(0)=-1.756 is a local max inside a
    #   dip; f dips to ~-1.813 near |x|≈0.6-0.8 [E4].
    # - There is a broader dip centered near |x|≈1.0: f(±1)≈-1.789 [E2,E3,E5].
    # - For |x|>~2 the function is smooth and gently increasing with |x|
    #   [E1,E6: f(-8)=-1.668, f(-20)=-1.648, f(-120)=-1.480].
    # - The function is even-symmetric: f(-x)=f(x) [E2,E3,E5,E6].
    # - Small asymmetry/noise ~0.001-0.01.
    #
    # Mechanism guess: f(x) = base(|x|) + dip1(|x|) + dip2(|x|) + spike(|x|)
    # where:
    #   base: smooth bowl, roughly quadratic-ish far out, flat near center
    #   dip2: gaussian dip centered at |x|=1.0, width ~0.5, depth ~0.033
    #   dip1: gaussian dip centered at |x|=0.65, width ~0.25, depth ~0.057
    #   spike: small positive gaussian at 0 (the local max at x=0)
    #
    # Let me fit with a=abs(x).

    x = probe.get("x", [])
    ys = []
    for xi in x:
        try:
            a = abs(float(xi))
        except Exception:
            ys.append(None)
            continue

        # Base bowl: gentle, symmetric, increasing with |x|.
        # Far values: f(120)≈-1.521, f(20)≈-1.663, f(0 baseline)≈-1.79
        # Use a soft quadratic: base = -1.79 + c*(a^2)/(a^2+k) type saturating
        # Fit: at a=0 -> -1.79 (but actual center has spike); at a=20 -> -1.663
        # at a=120 -> -1.521. Saturation suggests base = -1.79 + 0.27*(a^2)/(a^2+ 900)
        # check a=20: 400/(1300)=0.3077*0.27=0.083 -> -1.707 (bit low)
        # try k=400: a=20: 400/800=0.5*0.27=0.135 -> -1.655 good
        # a=120: 14400/14800=0.973*0.27=0.263 -> -1.527 good
        # a=8: 64/464=0.138*0.27=0.037 -> -1.753 (actual -1.68) too low.
        # So near center base is higher. Need different shape.
        #
        # Alternative: base = -1.79 + 0.27*(1 - exp(-a^2/ (2*sigma^2)))
        # a=8: exp(-64/(2*s^2)). Want 0.11 -> 1-exp=0.11 -> exp=0.89 -> 64/(2s^2)=0.116 -> s^2=276, s=16.6
        # a=20: exp(-400/552)=0.484 -> 0.516*0.27=0.139 -> -1.651 good
        # a=120: exp(-14400/552)=0 -> 0.27 -> -1.52 good
        # a=0 -> -1.79. Good.
        base = -1.79 + 0.27 * (1.0 - math.exp(-(a*a) / (2.0 * 276.0)))

        # Dip2: broad dip centered at a=1.0, depth ~0.033, width ~0.5
        # At a=1: base(-1.79+0.27*(1-exp(-1/552))≈-1.7895) + dip = -1.789
        # so dip2 at a=1 ~ 0.0? Hmm. Actually f(1)=-1.789, base(1)≈-1.7895.
        # So the dip at 1 IS the base value; base formula already gives -1.789.
        # Wait base(0)=-1.79, base(1)=-1.7895. But actual f(0)=-1.756 (spike up).
        # And actual f(1)=-1.789. So dip2 might not be needed at 1.
        #
        # Let's reconsider: maybe base is the OUTER shape and the center region
        # (|x|<~2) has extra structure: a dip near 0.6-0.8 and a spike at 0.
        # base(0.6)= -1.79+0.27*(1-exp(-0.36/552))≈-1.7898. actual f(0.6)=-1.7983.
        # base(0.8)=-1.7898, actual -1.8148. So dip ~ -0.025 at 0.8.
        # base(1)=-1.7895, actual -1.7893. no dip at 1.
        # base(1.5)=-1.7889, actual -1.7057. actual much HIGHER. 
        # So base is wrong near 1.5!
        #
        # Hmm, f(1.5)=-1.706, f(2)=-1.690, f(3)=-1.689, f(4)=-1.687, f(8)=-1.68.
        # So from 1.5 to 8 it's nearly flat ~-1.69, slowly rising.
        # And f(1)=-1.789 is a DIP. f(0.8)=-1.815 deeper dip.
        # So there's a dip region around |x| in [0.5, 1.2] and a peak at 0.
        #
        # Revised: base is the outer plateau ~-1.69 near 2-8.
        # base(a) for a>1.5: -1.69 + small rise.
        # f(2)=-1.6905, f(8)=-1.68, f(20)=-1.663, f(120)=-1.521.
        # rise from 2 to 120: 0.17. 
        # base = -1.69 + 0.17*(1-exp(-(a-1.5)^2/(2*s^2))) for a>1.5? 
        # At a=8: want -1.68 -> 0.01 rise -> 1-exp=0.0588 -> exp=0.941 -> (6.5)^2/(2s^2)=0.0608 -> 2s^2=694 -> s^2=347
        # At a=20: (18.5)^2/694=0.493 -> 1-exp=0.389 -> 0.066 -> -1.624. actual -1.663. too high.
        # So not exponential. Try power law: rise = c*(a-1.5)^p.
        # a=8: 6.5^p*c=0.01; a=20: 18.5^p*c=0.027; a=120:118.5^p*c=0.169
        # ratio 20/8: (18.5/6.5)^p=2.7 -> 2.846^p=2.7 -> p=0.96 ~ 1
        # ratio 120/20: (118.5/18.5)^p=6.26 -> 6.4^p=6.26 -> p~0.99
        # So rise ~ linear in a! c=0.01/6.5=0.00154.
        # check a=120: 118.5*0.00154=0.182 -> -1.508. actual -1.521. close.
        # check a=20: 18.5*0.00154=0.0285 -> -1.6615. actual -1.663. 
        # check a=40: 38.5*0.00154=0.0593 -> -1.631. actual -1.634. 
        # Great: base(a) = -1.6905 + 0.00154*(a-2) for a>=2 roughly.
        # Actually anchor at a=2: f=-1.6905. slope 0.00154.
        # base(a) = -1.6905 + 0.00154*(a-2) for a>=2.
        # For a<2 we need the dip structure.

        if a >= 2.0:
            val = -1.6905 + 0.00154 * (a - 2.0)
        else:
            # Region |x|<2: plateau ~-1.69 at a=2, dips near 0.6-1.0, spike at 0.
            # Anchor plateau value at a=2: -1.6905.
            # f(1.5)=-1.7057, f(1.75)=-1.691, f(2)=-1.6905.
            # f(1.25)=-1.7475, f(1)=-1.7893, f(0.8)=-1.8148, f(0.6)=-1.7983,
            # f(0.5)=-1.7928, f(0.4)=-1.7855, f(0.25)=-1.7744, f(0)=-1.756.
            # So dip minimum around a=0.8 (~-1.815), rising to -1.69 at a=2 and
            # rising to -1.756 at a=0 (spike).
            #
            # Model: plateau -1.6905 near 2, minus gaussian dip centered 0.85
            # depth ~0.125 width ~0.6, plus gaussian spike at 0 depth ~0.05.
            dip = 0.125 * math.exp(-((a - 0.85) ** 2) / (2.0 * 0.45 ** 2))
            spike = 0.055 * math.exp(-(a * a) / (2.0 * 0.30 ** 2))
            # plateau near 2: need -1.6905. But dip at a=2: exp(-(1.15)^2/0.405)=exp(-3.27)=0.038*0.125=0.0047, spike~0
            # so plateau = -1.6905 - 0.0047 = -1.6952? adjust plateau to -1.686
            val = -1.686 - dip + spike
            # check a=0: -1.686 -0.125*exp(-0.7225/0.405) + 0.055
            #   exp(-1.784)=0.168, dip=0.021 -> -1.686-0.021+0.055=-1.652. actual -1.756. too high.
            # spike too big or dip too small at 0. Let me reduce spike.
            # Want f(0)=-1.756. -1.686 - dip(0) + spike = -1.756 -> spike - dip(0) = -0.070
            # dip(0)=0.125*exp(-0.7225/0.405)=0.125*0.168=0.021
            # spike = -0.070+0.021 = -0.049?? negative spike. That means at 0 it's
            # still dipped, just less. So no spike, just dip that's shallower at 0.
            # Actually f(0)=-1.756 is HIGHER than f(0.8)=-1.815, so relative to dip
            # minimum, 0 is a local max. So spike positive relative to dip.
            # Let me set dip depth so f(0.8) works: 
            # f(0.8)=-1.815 = plateau - dip(0.8) + spike(0.8)
            # dip(0.8)=0.125*exp(-0.0025/0.405)=0.125*0.994=0.124
            # spike(0.8)=0.055*exp(-0.64/0.18)=0.055*0.028=0.0015
            # -1.686-0.124+0.0015=-1.8085. actual -1.815. close-ish.
            # f(0)=-1.686-0.021+0.055=-1.652. actual -1.756. off by 0.1.
            # So spike at 0 must be smaller: want -1.756 -> spike = -1.756+1.686+0.021 = -0.049.
            # negative. Contradiction means dip(0) is too small. Need bigger dip width.
            #
            # Let me try wider dip: width 0.7.
            # dip(a)=D*exp(-(a-0.85)^2/(2*0.7^2))
            # f(0.8)=-1.815: dip(0.8)≈D*exp(-0.0025/0.98)=D*0.9975
            # f(0)=-1.756: dip(0)=D*exp(-0.7225/0.98)=D*0.478
            # difference f(0)-f(0.8)=0.059 = (dip(0.8)-dip(0)) - (spike(0)-spike(0.8))
            # ignore spike: 0.059 = D*(0.9975-0.478)=D*0.5195 -> D=0.1136
            # Then plateau = f(0.8)+dip(0.8) = -1.815+0.1133=-1.7017
            # check f(1)=-1.7893: dip(1)=0.1136*exp(-0.0225/0.98)=0.1136*0.977=0.111
            #   -1.7017-0.111=-1.8127. actual -1.7893. off 0.023.
            # check f(1.5)=-1.7057: dip(1.5)=0.1136*exp(-0.4225/0.98)=0.1136*0.65=0.0738
            #   -1.7017-0.0738=-1.7755. actual -1.7057. off 0.07. too low.
            # So dip needs to fall off faster beyond 1.0. Asymmetric dip.
            # Use different widths: left width 0.7, right width 0.35.
            # dip(a) = D*exp(-(a-0.85)^2/(2*w^2)), w=0.7 if a<0.85 else 0.35
            # f(1.5): dip=0.1136*exp(-0.4225/0.245)=0.1136*0.178=0.0202
            #   -1.7017-0.0202=-1.7219. actual -1.7057. still off 0.016. ok-ish.
            # f(2): dip=0.1136*exp(-1.3225/0.245)=0.1136*0.0045=0.0005
            #   -1.7017-0.0005=-1.7022. actual -1.6905. off 0.012.
            # Let me just use plateau=-1.69 and accept small errors.
            if a < 0.85:
                w = 0.7
            else:
                w = 0.35
            D = 0.1136
            dip = D * math.exp(-((a - 0.85) ** 2) / (2.0 * w * w))
            val = -1.6905 - dip
            # small spike at 0 to lift f(0): 
            # f(0) predicted: -1.6905 - 0.1136*exp(-0.7225/0.98)= -1.6905-0.0543=-1.7448
            # actual -1.756. close enough (0.011).
            # f(0.5): dip=0.1136*exp(-0.1225/0.98)=0.1136*0.882=0.1002
            #   -1.6905-0.1002=-1.7907. actual -1.7928. good.
            # f(0.25): dip=0.1136*exp(-0.36/0.98)=0.1136*0.693=0.0787
            #   -1.6905-0.0787=-1.7692. actual -1.7744. good.
            # f(0.6): dip=0.1136*exp(-0.0625/0.98)=0.1136*0.938=0.1066
            #   -1.6905-0.1066=-1.7971. actual -1.7983. good.
            # f(0.7): dip=0.1136*exp(-0.0225/0.98)=0.111
            #   -1.6905-0.111=-1.8015. actual -1.8058. good.
            # f(0.9): w=0.35: dip=0.1136*exp(-0.0025/0.245)=0.1136*0.99=0.1124
            #   -1.6905-0.1124=-1.8029. actual -1.806. good.
            # f(1.0): dip=0.1136*exp(-0.0225/0.245)=0.1136*0.912=0.1036
            #   -1.6905-0.1036=-1.7941. actual -1.7893. good.
            # f(1.25): dip=0.1136*exp(-0.16/0.245)=0.1136*0.52=0.0591
            #   -1.6905-0.0591=-1.7496. actual -1.7475. good.
            # f(1.5): dip=0.1136*exp(-0.4225/0.245)=0.1136*0.178=0.0202
            #   -1.6905-0.0202=-1.7107. actual -1.7057. good.
            # f(1.75): dip=0.1136*exp(-0.81/0.245)=0.1136*0.0365=0.0041
            #   -1.6905-0.0041=-1.6946. actual -1.691. good.

        ys.append(val)

    return {"y": ys}
