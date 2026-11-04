import math

def predict(probe):
    # Model hypothesis based on E1:
    # - Outputs are small, roughly in [-0.12, 0.09], both signs.
    # - Looks like a smooth oscillatory function of x (sin-like), not monotonic.
    # - Magnitudes don't grow with |x| (88.2 -> 0.0136, -61.7 -> -0.1162), so
    #   likely sin(x) or sin of a scaled x, possibly with a small amplitude.
    # - Try f(x) = A*sin(x) with A ~ 0.1? Check E1:
    #   sin(88.2)=0.999 -> 0.0136 no. sin(66)= -0.0266 -> 0.0832 no.
    # - Try f(x) = A*sin(x/scale). Need to fit scale from E1.
    #   Look for a scale s such that sin(x/s) correlates with y.
    #   x=88.2 -> y=0.0136 ; x=66 -> 0.0832 ; x=-20.3 -> 0.0894
    #   x=-61.7 -> -0.1162 ; x=2.9 -> 0.0853 ; x=-24.3 -> -0.0725
    #   x=72.7 -> -0.0884 ; x=-50.4 -> 0.0351 ; x=-6 -> 0.0679 ; x=21.3 -> -0.0842
    # - Signs: +,+,-,-,+,+,+,-,-,- for x = 88.2,66,-20.3,-61.7,2.9,-24.3,72.7,-50.4,-6,21.3
    #   Hmm not obviously periodic in x directly.
    # - Try f(x) = A*sin(x^2 * k)? Or sin(x)*cos(x)?
    # - Best guess: f(x) = 0.1*sin(x) is wrong; try f(x)=0.1*sin(x^2/ something).
    #   x=88.2: x^2=7779 -> sin(7779)=? 7779 mod 2pi ~ 7779 - 1238*2pi=7779-7778.05=0.95 -> sin=0.81, not 0.136.
    # - Without more data, use a simple smooth guess: f(x) = 0.1*sin(x) * cos(x/10)? 
    #   This is a placeholder; mark uncertain.
    # - Actually try f(x) = 0.1*sin(x/10):
    #   88.2/10=8.82, sin=0.545 -> 0.0545 (obs 0.0136)
    #   66/10=6.6, sin=0.3115 -> 0.031 (obs 0.0832)
    #   Not great.
    # - Try f(x) = 0.1*sin(x/7):
    #   88.2/7=12.6, sin(12.6)=0.0332 -> 0.0033
    # - Try f(x) = 0.1*sin(x/20):
    #   88.2/20=4.41, sin=-0.954 -> -0.0954 (obs 0.0136)
    # - Try f(x) = 0.1*sin(x/30):
    #   88.2/30=2.94, sin=0.199 -> 0.0199 (obs 0.0136) close!
    #   66/30=2.2, sin=0.808 -> 0.0808 (obs 0.0832) close!
    #   -20.3/30=-0.677, sin=-0.626 -> -0.0626 (obs 0.0894) no.
    # - Try f(x) = 0.1*sin(x/30 + phase):
    #   Need sin(2.94+p)=0.136, sin(2.2+p)=0.832, sin(-0.677+p)=0.894
    #   From first: 2.94+p = 0.1364 or pi-0.1364=3.005 -> p=-2.80 or 0.065
    #   From second with p=0.065: 2.265, sin=0.769 (obs 0.832) close-ish
    #   From third with p=0.065: -0.612, sin=-0.574 (obs 0.894) no.
    # - The data is hard to fit with a single sinusoid. Given uncertainty,
    #   provide a best-effort smooth periodic guess and mark it.
    # - Try f(x) = 0.1*sin(x/30) * something? 
    # - I'll go with f(x) = 0.1*sin(x/30) as a rough guess, noting low confidence.
    out = []
    for x in probe.get("x", []):
        try:
            out.append(0.1 * math.sin(x / 30.0))
        except Exception:
            out.append(None)
    return {"y": out}
