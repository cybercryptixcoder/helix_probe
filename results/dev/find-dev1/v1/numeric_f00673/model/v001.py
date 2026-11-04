def predict(probe):
    # Fit: f(x) ≈ a*x^2 + b, with a≈0.1313, b≈0.76 from E1
    a = 0.1313
    b = 0.76
    try:
        xs = probe["x"]
        return {"y": [a * (x * x) + b for x in xs]}
    except Exception:
        return {}
