def predict(probe):
    try:
        xs = probe["x"]
        ys = []
        c = 5.42
        b = -16.8
        for x in xs:
            # odd part: linear with slope b at large |x|, softened near zero
            # use b*x*tanh(x/0.7) style: at |x|>>0.7 -> b*x; near 0 slope ~ b/0.7 * x^2 ... 
            # Actually want g(0.25)~-1.0, g(0.5)~-3.3, g(1)~-10.7, g(2)~-28
            # Try g(x) = b*x * (x^2/(x^2+a^2))^0.5 ... simpler: g(x)=b*x*|x|/(|x|+k)
            # g(1)=-10.7 => 16.8*1/(1+k)=10.7 => 1+k=1.57 => k=0.57
            # check g(0.5)=16.8*0.5*0.5/(0.5+0.57)=16.8*0.25/1.07=3.93 (obs 3.3) ok-ish
            # g(2)=16.8*2*2/2.57=26.1 (obs 28) ok
            ax = abs(x)
            g = b * x * ax / (ax + 0.6)
            ys.append(g + c)
        return {"y": ys}
    except Exception:
        return {"y": [None] * len(probe.get("x", []))}
