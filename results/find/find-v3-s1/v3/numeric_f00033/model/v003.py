import math

def predict(probe):
    # Beliefs:
    # - f is a smooth unimodal bump centered near x=0, peak ~0.386 at x=0 [E2,E4]
    # - Asymmetric: left falls faster than right [E2,E4]
    # - Far tails decay to ~0; small negative baseline ~ -0.003 to -0.004 [E1,E3,E5]
    #   (E5 shows -0.0049 at x=10.6, -0.0043 at large |x|; noise/baseline ~ -0.003)
    # - Fit piecewise Gaussian: amp=0.386, center=0.
    #   Left sigma: f(-1.2)=0.155 -> exp(-1.44/(2s^2))=0.402 -> s^2=0.766 -> s=0.875
    #               f(-2)=0.0575 -> exp(-4/(2s^2))=0.149 -> s^2=1.014 -> s=1.007
    #               f(-1.8)=0.0739 -> exp(-3.24/(2s^2))=0.191 -> s^2=0.913 -> s=0.956
    #               f(-1.4)=0.1218 -> exp(-1.96/(2s^2))=0.315 -> s^2=0.851 -> s=0.922
    #               f(-0.8)=0.2404 -> exp(-0.64/(2s^2))=0.623 -> s^2=0.680 -> s=0.825
    #               f(-0.6)=0.2836 -> exp(-0.36/(2s^2))=0.735 -> s^2=0.594 -> s=0.771
    #               f(-0.3)=0.3484 -> exp(-0.09/(2s^2))=0.902 -> s^2=0.437 -> s=0.661
    #               Left side is NOT Gaussian: sigma grows with |x|. Try a different form.
    #   Right sigma: f(1.2)=0.228 -> s=1.17; f(2)=0.12 -> s=1.31; f(2.5)=0.0642 -> s=1.32
    #               f(1.8)=0.147 -> exp(-3.24/(2s^2))=0.381 -> s^2=1.681 -> s=1.297
    #               f(1.4)=0.201 -> exp(-1.96/(2s^2))=0.521 -> s^2=1.469 -> s=1.212
    #               f(0.8)=0.282 -> exp(-0.64/(2s^2))=0.731 -> s^2=1.017 -> s=1.008
    #               f(0.6)=0.309 -> exp(-0.36/(2s^2))=0.800 -> s^2=0.807 -> s=0.898
    #               f(0.3)=0.3496 -> exp(-0.09/(2s^2))=0.906 -> s^2=0.455 -> s=0.674
    #   Both sides: sigma grows with |x| -> the bump has heavier tails than Gaussian.
    #   Try a Lorentzian-ish / sech^2 / or a Gaussian with x^p. 
    #   Let's fit y = A * exp(-(|x|/s)^p) per side.
    #   Left: at x=-0.3, y/A=0.902; x=-1.2, y/A=0.402; x=-2, y/A=0.149
    #     ln(-ln(y/A)): x=0.3: ln(0.103)=-2.27; x=1.2: ln(0.911)=-0.093; x=2: ln(1.904)=0.644
    #     vs ln(x): -1.204, 0.182, 0.693. Slope ~ (0.644-(-2.27))/(0.693-(-1.204))=2.914/1.897=1.536
    #     So p_L ~ 1.54. Check x=1.2: ln(x)=0.182, predicted ln(-ln)= -2.27+1.536*(0.182+1.204)=-2.27+2.129=-0.141 -> -ln=0.868 -> y/A=0.42 ok
    #   Right: x=0.3: 0.906 -> ln(-ln)=ln(0.0987)=-2.316; x=1.2: 0.591 -> ln(0.526)=-0.642; x=2: 0.311 -> ln(1.168)=0.155
    #     vs ln(x): -1.204, 0.182, 0.693. Slope=(0.155-(-2.316))/(0.693+1.204)=2.471/1.897=1.303
    #     p_R ~ 1.30. Check x=1.2: -2.316+1.303*(0.182+1.204)=-2.316+1.806=-0.510 -> -ln=0.600 -> y/A=0.549 vs 0.591 ok-ish
    #   Use y = A*exp(-(|x|/s)^p) with per-side s,p.
    #   Left: from x=1.2: (1.2/s)^p = 0.911; x=2: (2/s)^p=1.904. Ratio (2/1.2)^p=2.09 -> p*0.511=0.737 -> p=1.44
    #         (1.2/s)^1.44=0.911 -> 1.2/s=0.937 -> s=1.281
    #   Right: (1.2/s)^p=0.526; (2/s)^p=1.168. Ratio (1.667)^p=2.22 -> p*0.511=0.798 -> p=1.56
    #         (1.2/s)^1.56=0.526 -> 1.2/s=0.660 -> s=1.818
    #   Hmm let me just use these and add baseline.
    # - Baseline: small negative offset ~ -0.003 in far tails [E1,E3,E5]. 
    #   E5 x=10.6 -> -0.0049; x=-15.9 -> -0.0009; x=-19.9 -> -0.0012. Not constant.
    #   Treat as noise; use small negative baseline -0.002 maybe. Actually values range -0.0001 to -0.0049.
    #   Use baseline 0 (noise). But E2 x=12 -> -0.0061. So baseline ~ -0.003 with noise.
    #   I'll add a small constant -0.002 baseline to better match tails.
    xs = probe.get("x", [])
    out = []
    A = 0.386
    for x in xs:
        try:
            ax = abs(x)
            if x < 0:
                s, p = 1.28, 1.44
            else:
                s, p = 1.82, 1.56
            y = A * math.exp(-((ax / s) ** p)) - 0.002
            out.append(y)
        except Exception:
            out.append(None)
    return {"y": out}
