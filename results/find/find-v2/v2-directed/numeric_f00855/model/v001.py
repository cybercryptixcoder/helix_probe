def predict(probe):
    # f is 26 on the interval roughly [-2, 2], and 25 outside it [E1]
    # Boundary: -4 -> 25, -2 -> 26; 2 -> 26, 4 -> 25 [E1]
    # So the "special interval" is (-4, 4) exclusive? -2 and 2 are 26, -4 and 4 are 25.
    # Likely interval is (-4, 4) or [-3, 3]; test says -2..2 are 26, ±4 are 25.
    # Best guess: 26 when -4 < x < 4, else 25. (boundary exactness unknown "?")
    out = []
    for x in probe["x"]:
        if -4 < x < 4:
            out.append(26.0)
        else:
            out.append(25.0)
    return {"y": out}
