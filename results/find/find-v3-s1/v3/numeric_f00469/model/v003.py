def predict(probe):
    # f(x)=1 for 1.4<=|x|<=1.6? No: E6 shows |x|=1.4->1, 1.6->0, 1.7->0.
    # So nonzero region is |x| in [~1.4, ~1.6)? But E2 shows 1.5->1, 1.2->1, 1.0->1, 0.5->1, 0->1.
    # E6: 1.4->1, 1.3->1, 1.0->1, 0.7->1, 0.3->1, 0->1, -0.3..-1.4->1, -1.6->0, -1.7->0.
    # E2: 1.5->1, 2.0->0. E4: 1.8->0, 1.95->0.
    # So nonzero for |x|<=1.5 (1.5->1, 1.6->0). Threshold between 1.5 and 1.6.
    # E2: -1.5->1, -2.0->0. Consistent.
    # Guess threshold 1.55.
    out = []
    for x in probe["x"]:
        out.append(1.0 if abs(x) <= 1.55 else 0.0)
    return {"y": out}
