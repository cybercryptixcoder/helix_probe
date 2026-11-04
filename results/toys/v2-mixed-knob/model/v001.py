def predict(probe):
    # Only one data point so far; no reliable mechanism known.
    # E1: a=8.4,b=7.6,c=4.2,off -> x=9.2,y=5.2,size=3.1
    # Guess: x tracks a, y tracks b, size tracks c (all scaled/offset unknown).
    # Placeholder linear guesses anchored loosely on E1.
    a = probe.get("a", 0)
    b = probe.get("b", 0)
    c = probe.get("c", 0)
    sw = probe.get("switch", "off")
    # ? crude guesses, unverified
    x = a + 0.8
    y = b - 2.4
    size = c - 1.1
    return {"x": round(x, 2), "y": round(y, 2), "size": round(size, 2)}
