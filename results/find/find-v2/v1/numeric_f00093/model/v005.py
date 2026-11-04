def predict(probe):
    xs = probe.get("x", [])
    out = []
    for x in xs:
        try:
            x = float(x)
        except Exception:
            out.append(None)
            continue
        if x < -2.0:
            # straight line, slope -0.57, anchored at f(-2) = -2.5588
            y = -2.5588 + (-0.57) * (x + 2.0)
        elif x <= 0.0:
            # curve from (-2,-2.5588) to (0,-8.8302); slope steepens ~-2.5 -> ~-3.5
            # quadratic through endpoints with matching end slopes
            # fit y = a + b*x + c*x^2 using y(-2)=-2.5588, y(0)=-8.8302, y'(-2)~-2.5
            # y(0)=a=-8.8302; y(-2)=a-2b+4c=-2.5588 -> -2b+4c=6.2714
            # y'(-2)=b-4c=-2.5 -> b=4c-2.5; -2(4c-2.5)+4c=6.2714 -> -4c+5=6.2714 -> c=-0.31785
            # b=4(-0.31785)-2.5=-3.7714
            a = -8.8302
            b = -3.7714
            c = -0.31785
            y = a + b * x + c * x * x
        elif x <= 5.0:
            # steep segment near zero continuing to x=5, anchored at f(0)=-8.8302
            # use slope ~-3.3 to reach f(5)=-25.4152
            y = -8.8302 + (-3.317) * x
        else:
            if x <= 5.5:
                y = -25.4152 + (-3.05) * (x - 5.0)
            elif x <= 12.0:
                y = -26.9386 + (-2.05) * (x - 5.5)
            else:
                y = -38.0921 + (-0.97) * (x - 12.0)
        out.append(y)
    return {"y": out}
