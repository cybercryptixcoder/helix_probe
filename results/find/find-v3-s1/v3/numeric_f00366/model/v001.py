def predict(probe):
    # Outputs take only two values: 8.8 or -12.4 (plus one 9.8 outlier) [E1]
    # Sign of x seems to determine output: negative -> 8.8, positive -> -12.4 [E1]
    # x=-1.2 gave 9.8 (near zero, possibly a special region) [?]
    out = []
    for x in probe["x"]:
        if x < 0:
            out.append(8.8)
        else:
            out.append(-12.4)
    return {"y": out}
