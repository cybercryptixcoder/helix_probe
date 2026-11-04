import math

def predict(probe):
    # Observations are small, smooth, bounded values in roughly [-0.1, 0.1] [E1, E2].
    # f is a smooth MLP approximation of a bounded function [E1, E2].
    # Shape from E2: peaks near x=-2 (~0.078), trough near x=1 (~-0.095),
    #   rises again toward x=64 (~0.022), small positive at x=-64 (~0.029).
    # This looks like a damped sinusoid: y ~ A * exp(-|x|/tau) * sin(w*x + phi)
    #   with a period of roughly 6-8 units and slow amplitude decay.
    # ? Amplitude/phase/decay guessed from E2; refine if more data arrives.
    xs = probe.get("x", [])
    ys = []
    for x in xs:
        try:
            x = float(x)
            # damped sinusoid: peak near x=-2, trough near x=1 -> period ~6
            w = 2.0 * math.pi / 6.5
            # phase so that sin peaks near x=-2: w*(-2)+phi = pi/2
            phi = math.pi / 2 + w * 2.0
            amp = 0.09 * math.exp(-abs(x) / 40.0)
            y = amp * math.sin(w * x + phi) + 0.005
        except Exception:
            y = None
        ys.append(y)
    return {"y": ys}
