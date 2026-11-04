def predict(probe):
    # Identity: f(x) == x for all tested inputs [E1]
    # E1 covered digits, lowercase, uppercase, spaces, mixed case, and a
    # leading-space word; all outputs equal inputs exactly.
    # Best guess: the box is the identity function.
    return {"outputs": list(probe["inputs"])}
