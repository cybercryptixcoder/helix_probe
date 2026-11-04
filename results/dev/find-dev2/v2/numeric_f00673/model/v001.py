import math

def predict(probe):
    # Observations from E1:
    # - For |x| >= ~1, y grows roughly like x^2 scaled: y(128)~2150, y(64)~1075, y(32)~539, y(16)~270, y(8)~135, y(4)~67, y(2)~34, y(1)~17.
    #   That's ~0.131*x^2 for large x (2150/128^2 = 0.1312; 1075/64^2=0.2625? no).
    #   Check: y(64)=1075, x^2=4096 -> 0.2625. y(128)=2150, x^2=16384 -> 0.1312. Not pure x^2.
    #   Try y ~ a*|x|^p: log(2150/1075)/log(128/64)=log2/log2=1 -> linear? 2150/128=16.8, 1075/64=16.8. Yes! Linear for large x.
    #   y(32)=539, 539/32=16.8. y(16)=270, 270/16=16.9. y(8)=135, 135/8=16.9. y(4)=67, 67/4=16.8.
    #   y(2)=34, 34/2=17. y(1)=17. So y = 16.8*|x| for |x|>=1 approximately.
    # - At x=0, y=-1.0169 (small negative). At x=-1, y=15.56; x=1, y=17.25. Slight asymmetry/noise.
    # - Small dip near 0: x=0 gives ~-1, suggesting a small negative bump or offset near zero.
    # Model: y = 16.8*|x| + small correction near 0. At x=0, correction ~ -1.0.
    # The values at x=+-1 are ~16-17, consistent with 16.8*1 plus noise.
    # Hypothesis: y = 16.8*|x| - 1.0*exp(-x^2) or similar small negative near zero.
    # Simpler: y = 16.8*|x| - 1.0/(1+x^2) roughly. At x=0: -1.0. At x=1: 16.8-0.5=16.3 (obs 17.2/15.6, ok-ish).
    # Use y = 16.8*|x| - 1.0*exp(-x^2) as best guess.
    out = []
    for x in probe.get("x", []):
        try:
            y = 16.8*abs(x) - 1.0*math.exp(-x*x)
        except Exception:
            y = None
        out.append(y)
    return {"y": out}
