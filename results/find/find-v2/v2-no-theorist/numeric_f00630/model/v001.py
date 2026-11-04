def predict(probe):
    # Output takes only two values: 52.2 or -14.96 [E1]
    # 52.2 occurs for x >= 0 (88.2, 66.0, 2.9, 72.7, 21.3) [E1]
    # -14.96 occurs for x < 0 (-20.3, -61.7, -24.3, -50.4, -6.0) [E1]
    # So f(x) = 52.2 if x >= 0 else -14.96 (sign-based step function) [E1]
    out = []
    for x in probe.get("x", []):
        if x is None:
            out.append(None)
        else:
            out.append(52.2 if x >= 0 else -14.96)
    return {"y": out}
