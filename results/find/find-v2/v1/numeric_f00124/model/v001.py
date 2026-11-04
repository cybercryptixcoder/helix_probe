import math

def predict(probe):
    try:
        xs = probe.get("x", [])
        out = []
        for x in xs:
            if x is None:
                out.append(None)
                continue
            x = float(x)
            # Large-scale: quadratic growth with slight asymmetry via linear term
            # Fit from E1: f(128)=14369, f(-128)=3312, f(0)=106
            # a*x^2 + b*x + c
            # At x=0: c=106
            # 128^2*a + 128*b + 106 = 14369 -> 16384a + 128b = 14263
            # 16384a - 128b = 3206
            # => 32768a = 17469 -> a = 0.5331; 128b = (14263-3206)/2 = 5528.5 -> b=43.19
            a = 0.5331
            b = 43.19
            c = 106.0
            base = a * x * x + b * x + c
            # Near-zero dip: observed f(0)=106, f(1)=217, f(-1)=6.85, f(0.5)=161.8
            # The quadratic+linear already gives f(0)=106, f(1)=582, f(-1)=63, f(0.5)=127.8
            # There's a dip near 0 that pulls values down; model as Gaussian subtraction
            # f(0) matches; f(1) predicted 582 vs 217 -> need dip ~365 at x=1
            # f(-1) predicted 63 vs 6.85 -> dip ~56 at x=-1
            # asymmetric dip centered slightly positive
            dip_center = 0.6
            dip_width = 1.5
            dip_amp = 400.0
            dip = dip_amp * math.exp(-((x - dip_center) ** 2) / (2 * dip_width ** 2))
            # Also a broader dip for mid-range? Check x=2: base=0.5331*4+43.19*2+106=194.6
            # observed 328.9 -> base too low, so no dip there; actually need positive
            # x=4: base=0.5331*16+43.19*4+106=287.3, observed 551.8 -> need +264
            # So mid-range needs boost, not dip. Use a Gaussian bump centered ~4
            bump_amp = 260.0
            bump_center = 4.0
            bump_width = 3.0
            bump = bump_amp * math.exp(-((x - bump_center) ** 2) / (2 * bump_width ** 2))
            # For negative side, x=-4: base=0.5331*16-43.19*4+106=-58.2, observed 78.8 -> need +137
            # x=-8: base=0.5331*64-43.19*8+106=34.1-345.5+106=-205.4, observed 183 -> need +388
            # Negative side needs a bump too, centered more negative
            nbump_amp = 400.0
            nbump_center = -8.0
            nbump_width = 6.0
            nbump = nbump_amp * math.exp(-((x - nbump_center) ** 2) / (2 * nbump_width ** 2))
            y = base - dip + bump + nbump
            out.append(y)
        return {"y": out}
    except Exception:
        return {"y": [None for _ in probe.get("x", [])]}
