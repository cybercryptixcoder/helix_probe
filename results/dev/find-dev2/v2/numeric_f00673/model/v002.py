import math

def predict(probe):
    # Observations:
    # - For large |x|, y ≈ 16.8*|x| (E1: y(128)/128≈16.79, y(64)/64≈16.80, y(32)/32≈16.84, y(16)/16≈16.86, y(8)/8≈16.95)
    # - Near zero, y is NOT negative: E2 shows y(0)=0.9047, y(±0.25)≈3-5, y(±0.5)≈6-9, y(±0.75)≈12-13
    # - E2 shows a smooth curve through origin region, roughly y ≈ 16.8*|x| but with a small dip near 0
    # - E1's y(0)=-1.0169 was likely noise/outlier; E2's y(0)=0.9047 is more reliable (denser sampling)
    # - Fit: y ≈ 16.8*|x| - c*exp(-k*x^2) with small c, or y ≈ 16.8*|x|*(1 - exp(-a*|x|)) form
    # - Check E2: y(0.25)=5.05, 16.8*0.25=4.2 -> y>linear near 0. y(0.5)=9.15 vs 8.4. y(1)=17.0 vs 16.8.
    # - So near 0, y is slightly ABOVE 16.8*|x|, then converges. Try y = 16.8*|x| + b*exp(-k*x^2)
    # - y(0)=0.90 -> b≈0.90. y(0.25)=5.05, 16.8*0.25+0.9*exp(-k*0.0625)=4.2+... need +0.85 -> exp(-0.0625k)≈0.94 -> k≈1
    # - y(0.5)=9.15, 8.4+0.9*exp(-0.25)=8.4+0.70=9.10 ✓
    # - y(0.75)=13.35, 12.6+0.9*exp(-0.5625)=12.6+0.51=13.11, close
    # - y(1)=17.0, 16.8+0.9*exp(-1)=16.8+0.33=17.13 ✓
    # - y(2)=33.74, 33.6+0.9*exp(-4)=33.62, close
    # - Slope check: E1 large values give ~16.8; E2 gives similar. Use 16.8.
    # - Small asymmetry in E1/E2 is noise.
    out = []
    for x in probe.get("x", []):
        try:
            y = 16.8*abs(x) + 0.9*math.exp(-x*x)
        except Exception:
            y = None
        out.append(y)
    return {"y": out}
