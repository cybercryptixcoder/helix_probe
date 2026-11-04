import math

def predict(probe):
    # Beliefs about the black box f(x):
    # - f is piecewise smooth, with a central "bump" region and linear asymptotes.
    # - For x >= ~0.5: f(x) ≈ -16.905*x + 11.58 (linear asymptote) [E2,E6,E8]
    # - For x <= ~-0.5: f(x) ≈ -6.759*x + 2.588 (linear asymptote) [E2,E6]
    # - Central region -0.5 < x < 0.5 is a smooth bump, asymmetric:
    #     negative side nearly linear slope ~ -2.854 [E4,E6]
    #     positive side curves down, accelerating near 0.5 [E4,E6]
    # - No flat plateau at x≈0.5-0.7: f decreases smoothly through it [E8]
    # - Transition to linear on positive side is smooth around x≈0.5-0.6 [E8]
    # - Transition on negative side around x≈-0.5 [E4,E6]
    # - Function is NOT odd-symmetric; slopes differ on each side [E2]

    x = probe["x"]
    ys = []
    for v in x:
        try:
            ys.append(_f(float(v)))
        except Exception:
            ys.append(None)
    return {"y": ys}


def _f(x):
    # Linear asymptotes (fitted from E2, E6, E8)
    # Positive side: f(x) = -16.905*x + 11.58
    # Negative side: f(x) = -6.759*x + 2.588
    pos_line = lambda t: -16.905 * t + 11.58
    neg_line = lambda t: -6.759 * t + 2.588

    # Central bump anchors from E4/E6 (dense near 0)
    # Negative side (-0.5 to 0): nearly linear, slope ~ -2.854
    # Positive side (0 to 0.5): curved, accelerating drop
    # Use smooth interpolation through anchors, blending to lines outside.

    # Anchor points for the bump region, from E4/E6/E8
    bump = [
        (-0.5, 6.8447),
        (-0.4, 6.5602),
        (-0.3, 6.2748),
        (-0.2, 5.9894),
        (-0.1, 5.704),
        (-0.05, 5.5613),
        (0.0, 5.4186),
        (0.05, 5.2759),
        (0.1, 5.1041),
        (0.15, 4.9028),
        (0.2, 4.6858),
        (0.25, 4.4171),
        (0.3, 4.0718),
        (0.35, 3.6502),
        (0.4, 3.2125),
        (0.42, 3.0163),
        (0.45, 2.6897),
        (0.48, 2.3522),
        (0.5, 2.1182),
        (0.52, 1.8746),
        (0.55, 1.5026),
        (0.58, 1.1301),
        (0.6, 0.8742),
        (0.62, 0.5991),
        (0.65, 0.1665),
        (0.68, -0.2821),
        (0.7, -0.5835),
        (0.72, -0.8935),
        (0.75, -1.3675),
        (0.78, -1.8475),
        (0.8, -2.1698),
        (0.85, -2.9733),
        (0.9, -3.757),
        (0.95, -4.5408),
        (1.0, -5.3245),
        (1.05, -6.1083),
        (1.1, -6.9174),
        (1.2, -8.5666),
        (1.5, -13.7572),
        (2.0, -22.6804),
        (2.5, -31.1292),
        (3.0, -39.4742),
    ]

    # Negative side anchors from E2/E4/E6
    neg_anchors = [
        (-3.0, 22.6743),
        (-2.5, 19.2942),
        (-2.0, 15.9142),
        (-1.5, 12.5417),
        (-1.2, 10.5797),
        (-1.0, 9.3469),
        (-0.8, 8.1725),
        (-0.7, 7.6317),
        (-0.6, 7.1978),
        (-0.5, 6.8447),
    ]

    # For x >= 0.5: blend bump anchors into positive line.
    # The bump anchors already extend to x=3 and match the line closely there,
    # so just interpolate through them, then use line beyond.
    if x >= 0.5:
        # Use anchors up to 3.0, then linear
        if x <= 3.0:
            return _interp(bump, x)
        return pos_line(x)

    # For x <= -0.5: blend into negative line
    if x <= -0.5:
        if x >= -3.0:
            return _interp(neg_anchors, x)
        return neg_line(x)

    # Central region -0.5 < x < 0.5: interpolate through bump anchors
    return _interp(bump, x)


def _interp(anchors, x):
    # Linear interpolation through sorted anchors
    if x <= anchors[0][0]:
        x0, y0 = anchors[0]
        x1, y1 = anchors[1]
        slope = (y1 - y0) / (x1 - x0)
        return y0 + slope * (x - x0)
    if x >= anchors[-1][0]:
        x0, y0 = anchors[-2]
        x1, y1 = anchors[-1]
        slope = (y1 - y0) / (x1 - x0)
        return y1 + slope * (x - x1)
    for i in range(len(anchors) - 1):
        x0, y0 = anchors[i]
        x1, y1 = anchors[i + 1]
        if x0 <= x <= x1:
            if x1 == x0:
                return y0
            t = (x - x0) / (x1 - x0)
            return y0 + t * (y1 - y0)
    return None
