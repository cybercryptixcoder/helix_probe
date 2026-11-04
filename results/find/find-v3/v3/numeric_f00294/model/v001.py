def predict(probe):
    # f(x) = x + 17.6 approximately [E1]
    # Check: 88.2->105.8 (+17.6), 66.0->82.8 (+16.8), -20.3->-28.4 (-8.1?)
    # Hmm, let's look more carefully.
    # 88.2 -> 105.8 : diff 17.6
    # 66.0 -> 82.8 : diff 16.8
    # -20.3 -> -28.4 : diff -8.1
    # -61.7 -> -69.4 : diff -7.7
    # 2.9 -> 19.8 : diff 16.9
    # -24.3 -> -32.4 : diff -8.1
    # 72.7 -> 89.8 : diff 17.1
    # -50.4 -> -58.4 : diff -8.0
    # -6.0 -> -14.4 : diff -8.4
    # 21.3 -> 38.8 : diff 17.5
    # Pattern: positive x -> +~17, negative x -> -~8
    # Looks like f(x) = x + 17.6 if x>=0 else x - 8.1
    # Or maybe f(x) = x + 17.6 for x>0, x - 8 for x<0
    # Test: 2.9+16.9=19.8, 21.3+17.5=38.8, 66+16.8=82.8, 72.7+17.1=89.8, 88.2+17.6=105.8
    # Negatives: -6-8.4=-14.4, -20.3-8.1=-28.4, -24.3-8.1=-32.4, -50.4-8=-58.4, -61.7-7.7=-69.4
    # The offset varies a bit - maybe noisy, or maybe proportional?
    # 88.2: 17.6/88.2 = 0.1995 ~ 0.2
    # 66: 16.8/66 = 0.2545 no
    # 2.9: 16.9/2.9 = 5.8 no
    # Try: positive offset ~17.6, negative offset ~-8.1. Noise ~0.5.
    # Maybe f(x) = x + 17.6 if x>0 else x - 8.1, with noise.
    # Or maybe it's x + 17.6 for x>=0 and x - 8.1 for x<0.
    # Actually could be a threshold at 0. Let's just use that.
    out = []
    for x in probe["x"]:
        if x >= 0:
            out.append(x + 17.6)
        else:
            out.append(x - 8.1)
    return {"y": out}
