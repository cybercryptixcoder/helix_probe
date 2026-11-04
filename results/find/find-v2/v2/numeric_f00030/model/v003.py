import math

def predict(probe):
    # Model of the black box f(x).
    #
    # Evidence-based beliefs:
    # - Output is roughly a smooth, slowly varying function of x on [-128,128].
    #   Values range from about -1.47 at x=-128 up to about -1.51 at x=128,
    #   with a dip near x=0 [E2, E4].
    # - There is a local "notch"/dip centered at x=0 where f is more negative
    #   (about -1.79) than the surrounding baseline (~-1.68). The dip is narrow:
    #   at |x|=3 it is gone (-1.685), at |x|=1 still strong (-1.789) [E4].
    # - Outside the notch, the function decreases roughly linearly from x=-128
    #   to x=0 and increases roughly linearly from x=0 to x=128, i.e. a broad
    #   V/U shape superposed with the narrow central notch [E2, E4].
    # - Slight asymmetry: values at +x are a bit higher (less negative) than at
    #   -x for large |x| (e.g. f(-120)=-1.4799 vs f(120)=-1.5207) [E4].
    #   Also -128 -> -1.4667 but +128 -> -1.5099 [E2, E4].
    # - The broad trend looks like a shallow quadratic/linear: from -128
    #   (-1.4667) to -80 (-1.5464) to -40 (-1.614) to 0-ish baseline (-1.68)
    #   then rising to +128 (-1.5099) [E2, E4].
    # - The MLP smooths everything, so use smooth functions, not hard branches.
    #
    # Mechanism guess:
    #   f(x) = baseline(x) + notch(x)
    #   baseline(x) = a + b*x + c*x^2   (broad bowl, asymmetric)
    #   notch(x)    = -A * exp(-(x/sigma)^2)   (narrow Gaussian dip at 0)
    #
    # Fit roughly from the data:
    #   baseline at x=0 ~ -1.68 (from |x|=3..8 values ~ -1.685..-1.69)
    #   baseline at x=-128 ~ -1.4667, at x=128 ~ -1.5099
    #   baseline at x=-80 ~ -1.5464, at +80 ~ -1.5777
    #   notch depth ~ 0.11 at x=0 (from -1.79 vs -1.68), sigma ~ 1.5-2
    #     (at x=1, notch ~ -0.11*exp(-1/4)= -0.086 -> -1.77, close to -1.789;
    #      at x=2, exp(-4/4)=0.37 -> -0.04 -> -1.73 vs observed -1.69; so
    #      sigma a bit smaller, ~1.5, or depth larger. Use sigma=1.6.)
    #
    # Solve baseline coefficients from three points:
    #   x=0:   a = -1.68
    #   x=-128: a -128b + 16384c = -1.4667  -> -128b + 16384c = 0.2133
    #   x=128:  a +128b + 16384c = -1.5099  ->  128b + 16384c = 0.1701
    # Add: 32768c = 0.3834 -> c = 1.170e-5
    # Subtract: 256b = 0.1701-0.2133 = -0.0432 -> b = -1.6875e-4
    #
    # Check x=-80: -1.68 + 0.0135 + 0.0749 = -1.5916 vs observed -1.5464.
    # Hmm, off by ~0.045. The broad shape isn't a pure quadratic; it's more
    # like a V (linear in |x|) with slight curvature.
    #
    # Try linear-in-|x| baseline with asymmetry:
    #   baseline(x) = a + s*x + m*|x|
    #   x=0: a = -1.68
    #   x=-128: -128s + 128m = 0.2133 -> -s + m = 0.001666
    #   x=128: 128s + 128m = 0.1701 ->  s + m = 0.001329
    #   -> m = 0.0014975, s = -1.6875e-4
    # Check x=-80: -1.68 + 0.0135 + 0.1198 = -1.5467 vs -1.5464. Excellent!
    # Check x=+80: -1.68 - 0.0135 + 0.1198 = -1.5737 vs -1.5777. Good.
    # Check x=-40: -1.68 + 0.00675 + 0.0599 = -1.6134 vs -1.614. Excellent!
    # Check x=+40: -1.68 - 0.00675 + 0.0599 = -1.6269 vs -1.6344. Good.
    # Check x=-15: -1.68 + 0.00253 + 0.02246 = -1.6550 vs -1.6561. Great.
    # Check x=+15: -1.68 - 0.00253 + 0.02246 = -1.6601 vs -1.6698. Close.
    # Check x=-120: -1.68 + 0.02025 + 0.1797 = -1.4801 vs -1.4799. 
    # Check x=+120: -1.68 - 0.02025 + 0.1797 = -1.5206 vs -1.5207. 
    #
    # So baseline(x) = -1.68 - 1.6875e-4*x + 1.4975e-3*|x|.
    #
    # Notch: at x=0 baseline = -1.68, observed -1.756 (E2) and E4 gives
    # around -1.79 at x=0.5-1. So notch depth ~ 0.09-0.11.
    # Use Gaussian: notch(x) = -0.10 * exp(-(x/1.6)^2).
    # Check x=0: -1.68 - 0.10 = -1.78 (observed -1.756 at x=0 in E2; E4 at
    #   x=0.5 gives -1.7928, x=1 gives -1.7893). Hmm E2 x=0 gives -1.756,
    #   which is less deep. There's noise. Average depth ~0.10.
    # Check x=1: baseline=-1.6802, notch=-0.10*exp(-0.39)=-0.0677 -> -1.748
    #   vs observed -1.7893. Need deeper/wider notch.
    # Try depth 0.11, sigma 2.0: x=1: -0.11*exp(-0.25)=-0.0857 -> -1.766.
    #   x=2: -0.11*exp(-1)=-0.0405 -> -1.720 vs observed -1.6905. Too deep.
    # Try depth 0.11, sigma 1.8: x=1: -0.11*exp(-0.309)=-0.0806 -> -1.761
    #   x=2: -0.11*exp(-1.235)=-0.0320 -> -1.712 vs -1.6905.
    # The notch seems sharper than Gaussian but with a flat-ish bottom near 0.
    # Use a Lorentzian-ish or a sum: maybe the MLP approximates a narrow
    # dip. Try depth 0.11, sigma 1.5: x=1: -0.11*exp(-0.444)=-0.0707 -> -1.751
    #   x=2: -0.11*exp(-1.778)=-0.0186 -> -1.699 vs -1.6905. Good.
    #   x=0.5: -0.11*exp(-0.111)=-0.0984 -> -1.778 vs -1.7928. Close.
    #   x=3: -0.11*exp(-4)=-0.002 -> -1.682 vs -1.6888. Good.
    # Use depth 0.115, sigma 1.5.
    #
    # Also E2 at x=0: -1.756 vs model -1.795. Noise ~0.04. Acceptable.
    #
    # Final model:
    #   f(x) = -1.68 - 1.6875e-4*x + 1.4975e-3*|x| - 0.115*exp(-(x/1.5)^2)

    try:
        xs = probe.get("x", [])
        ys = []
        for xv in xs:
            if xv is None:
                ys.append(None)
                continue
            x = float(xv)
            baseline = -1.68 - 1.6875e-4 * x + 1.4975e-3 * abs(x)
            notch = -0.115 * math.exp(-(x / 1.5) ** 2)
            ys.append(baseline + notch)
        return {"y": ys}
    except Exception:
        # Never raise.
        try:
            n = len(probe.get("x", []))
        except Exception:
            n = 0
        return {"y": [None] * n}
