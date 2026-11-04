import math

def predict(probe):
    # Observations [E1]:
    # - f is roughly odd-symmetric in magnitude but with a small offset near 0.
    # - For |x| large, f(x) ~ 16.8 * |x| (e.g. 128 -> 2150, 64 -> 1075, 32 -> 537).
    # - Actually f(x) ~ 16.8*|x| + small correction; looks like 16.8*|x| plus something.
    # - At x=0, f(0) = -0.2561 (small negative).
    # - f(0.5)=9.5969, f(-0.5)=8.8162: asymmetric near zero.
    # - f(1)=16.28, f(-1)=17.83: also asymmetric.
    # - For |x|>=2, f(x) ≈ 16.8*|x| + ~0.3 (positive side) / ~0.3 (negative side).
    # - Looks like f(x) = 16.8*|x| + g(x) where g is small and asymmetric.
    # Hypothesis: f(x) = 16.8*|x| + c + d*sign(x) + small wiggle.
    # Fit: at x=128: 16.8*128=2150.4, obs 2150.1 -> offset ~ -0.3
    #      at x=-128: 2150.4, obs 2152.1 -> offset +1.7
    #      at x=64: 1075.2, obs 1075.1 -> -0.1
    #      at x=-64: 1075.2, obs 1074.15 -> -1.05
    #   Not consistent sign. Maybe f(x) = 16.8*|x| + a*sin-ish? 
    # Let's look at residual r = y - 16.8*|x|:
    #   x=-128: 1.71, -100: 0.45, -64: -1.05, -32: -0.81, -16: 0.72, -8: -0.84,
    #   -4: 1.08, -2: 0.15, -1: 1.03, -0.5: 0.42, 0: -0.256,
    #   0.5: 1.197, 1: -0.52, 2: -0.96, 4: -0.74, 8: 1.45, 16: 0.15, 32: -0.52,
    #   64: -0.10, 128: -0.30
    # Residuals are small (~±1.5), roughly random-looking. Could be noise.
    # But near zero, |x| model breaks: f(0.5)=9.6 not 8.4. f(0)= -0.26.
    # Maybe f(x) = 16.8*|x| + 0.5*sin(...)? Or f(x) = 16.8*|x| + noise.
    # Actually check: is it 16.8*|x| + 0.5*sin(x)? At x=0.5: 8.4+0.24=8.64, obs 9.6. No.
    # Maybe f(x) = 16.8*|x| + something like 1.5*sin(x/2)? 
    # Let's try f(x) = 16.8*|x| + 0.5*cos(x) ... at x=0: 0.5, obs -0.26.
    # Alternative: f(x) = 16.8*|x| + 0.5*sin(x) + c. 
    # Look at small x: f(0.5)-f(-0.5)=0.78, f(1)-f(-1)=-1.55, f(2)-f(-2)=-1.11,
    #   f(4)-f(-4)=-1.82, f(8)-f(-8)=2.29, f(16)-f(-16)=-0.57, f(32)-f(-32)=0.29,
    #   f(64)-f(-64)=0.95, f(128)-f(-128)=-2.01
    # Differences are small and noisy. So f is nearly even in |x|.
    # Best simple model: f(x) = 16.8*|x| + noise, with small offset near 0.
    # But f(0)=-0.256, f(0.5)=9.6 (16.8*0.5=8.4, diff 1.2), f(-0.5)=8.82 (diff 0.42).
    # Maybe f(x) = 16.8*|x| + 0.5*sin(x) + 0.5*cos(x)? 
    # At x=0: 0.5, no.
    # Try f(x) = 16.8*|x| + 1.5*sin(x) - 0.25:
    #   x=0: -0.25 ✓ (obs -0.256)
    #   x=0.5: 8.4+0.719-0.25=8.87 (obs 9.6) - off
    #   x=-0.5: 8.4-0.719-0.25=7.43 (obs 8.82) - off
    # Try f(x) = 16.8*|x| + 1.5*sin(x) + 0.5*cos(x) - 0.75:
    #   x=0: 0.5-0.75=-0.25 ✓
    #   x=0.5: 8.4+0.719+0.439-0.75=8.81 (obs 9.6) - off
    # Hmm. Let's just fit: f(x) = a*|x| + b*sin(x) + c*cos(x) + d
    # Use x=0: c+d = -0.256
    # x=128: 128a + b*sin(128) + c*cos(128) + d = 2150.1
    # x=-128: 128a - b*sin(128) + c*cos(128) + d = 2152.1
    # Subtract: 2b*sin(128) = -2 -> b*sin(128) = -1
    # sin(128 rad) = sin(128 - 40.74*pi) ... 128/(2pi)=20.37, 128-20*2pi=128-125.66=2.34, sin(2.34)=0.72
    # So b ≈ -1.39
    # Add: 256a + 2c*cos(128) + 2d = 4302.2
    # cos(128)=cos(2.34)=-0.70
    # 256a - 1.4c + 2d = 4302.2
    # x=64: 64a + b*sin(64) + c*cos(64) + d = 1075.1
    # sin(64): 64-10*2pi=64-62.83=1.17, sin=0.92; cos(1.17)=0.39
    # 64a -1.28 + 0.39c + d = 1075.1
    # x=-64: 64a +1.28 + 0.39c + d = 1074.15
    # Add: 128a + 0.78c + 2d = 2149.25
    # Subtract: -2.56 = 0.95 -> inconsistent (noise)
    # This is getting complicated. Given residuals ~±1.5 and noise likely,
    # simplest good model: f(x) = 16.8*|x| + small constant, with special handling near 0.
    # Actually check: maybe f(x) = 16.8*|x| + 0.5*sin(2x)? 
    # At x=0.5: 8.4+0.42=8.82 (obs 9.6) no.
    # Let's just use f(x) = 16.8*|x| + 0.5*sin(x) - 0.25 and accept noise.
    # Wait, better: fit a and offset from large x.
    # x=128: 2150.1, x=64: 1075.1 -> slope (2150.1-1075.1)/64 = 16.797
    # x=-128: 2152.1, x=-64: 1074.15 -> slope (2152.1-1074.15)/64 = 16.843
    # Average ~16.82. Offset at 0: ~ -0.25.
    # Near zero: f(0.5)=9.6, 16.82*0.5=8.41, residual 1.19
    # f(-0.5)=8.82, residual 0.41
    # f(1)=16.28, 16.82, residual -0.54
    # f(-1)=17.83, residual 1.01
    # These residuals are within noise range (~±1.5). So model:
    # f(x) = 16.82*|x| - 0.25 + noise
    # But f(0)=-0.256 matches -0.25 well.
    # Let's go with f(x) = 16.82*|x| - 0.25.
    # Actually use 16.8*|x| - 0.25.
    out = []
    for x in probe["x"]:
        try:
            out.append(16.8*abs(x) - 0.25)
        except Exception:
            out.append(None)
    return {"y": out}
