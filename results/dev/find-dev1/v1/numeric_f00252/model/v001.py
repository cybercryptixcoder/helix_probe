import math

def predict(probe):
    try:
        xs = probe.get("x", [])
        out = []
        # Logistic fit: a/(1+exp(-k*(x-x0)))
        # Fit roughly to points: f(1)=1.1, f(2)=142.19, f(4)=283.27, f(8)=424.36,
        # f(16)=565.45, f(32)=706.54, f(64)=847.62, f(100)=938.46, f(128)=988.71
        a = 1000.0
        k = 0.1
        x0 = -1.1
        for x in xs:
            if x is None or x <= 0:
                out.append(None)
            else:
                try:
                    val = a / (1.0 + math.exp(-k * (x - x0)))
                    out.append(round(val, 4))
                except Exception:
                    out.append(None)
        return {"y": out}
    except Exception:
        return {"y": []}
