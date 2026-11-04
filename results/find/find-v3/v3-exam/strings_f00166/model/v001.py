def predict(probe):
    # Identity function: output equals input [E1]
    # All 6 varied inputs (digits, mixed case, spaces, words) returned unchanged
    return {"outputs": list(probe["inputs"])}
