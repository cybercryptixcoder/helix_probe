def predict(probe):
    # Only evidence is E1: outputs are ~0 everywhere except x=-1.2 gives -1.0.
    # Hypothesis: f(x) = -1 only very near x = -1 (a narrow spike), else 0.
    # The spike is narrow: x=-12.9 and x=38.8 etc. give 0, so width < ~11.
    # Best guess: a small interval around -1. Width unknown; pick something modest.
    # ? exact width and shape unknown; using a narrow band around -1.
    out = []
    for x in probe["x"]:
        if x is None:
            out.append(None)
        elif -2.0 <= x <= 0.0:
            out.append(-1.0)
        else:
            out.append(0.0)
    return {"y": out}
