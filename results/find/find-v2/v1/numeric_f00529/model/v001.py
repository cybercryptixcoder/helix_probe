def predict(probe):
    def f(x):
        try:
            x = float(x)
        except Exception:
            return None
        # Flat regions
        if x <= -2:
            return -7.9
        if x >= 4:
            return -6.9
        # Transition interval (-2, 4): anchor points from E1
        anchors = [(-2, -7.9), (0, -7.8991), (1, -7.8111), (2, -6.9889), (4, -6.9)]
        for i in range(len(anchors) - 1):
            x0, y0 = anchors[i]
            x1, y1 = anchors[i + 1]
            if x0 <= x <= x1:
                t = (x - x0) / (x1 - x0)
                return y0 + t * (y1 - y0)
        return -6.9
    return {"y": [f(x) for x in probe.get("x", [])]}
