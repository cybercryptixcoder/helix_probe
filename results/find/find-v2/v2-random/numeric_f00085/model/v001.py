def predict(probe):
    # Model: f(x) looks like a quadratic-ish function for |x| large, but
    # near x=0 it flattens to a constant ~ -22.8.
    # Evidence E1:
    #   f(2.9) = -22.8021, f(-6.0) = -22.8021  -> constant floor near 0
    #   f(-20.3)=1545.2, f(21.3)=1532.7, f(-24.3)=2154.1, f(-50.4)=9077.3
    #   f(66.0)=15014.0, f(72.7)=18241.8, f(88.2)=27090.8, f(-61.7)=13550.6
    # Try f(x) = a*x^2 + b*|x| + c with a floor for small |x|.
    # Fit roughly: large values ~ 3.5*x^2? 88.2^2=7779 -> 27090/7779=3.48
    #   66^2=4356 -> 15014/4356=3.45; 72.7^2=5285 -> 18242/5285=3.45
    #   61.7^2=3807 -> 13551/3807=3.56; 50.4^2=2540 -> 9077/2540=3.57
    #   24.3^2=590 -> 2154/590=3.65; 21.3^2=454 -> 1533/454=3.38
    #   20.3^2=412 -> 1545/412=3.75
    # So roughly 3.5*x^2, with a floor at -22.8 for small |x|.
    # The floor region: |x| small gives -22.8021. Boundary somewhere between
    # 6 and 20.3. Use a smooth-ish guess: floor for |x| < ~10, quadratic above.
    # ? boundary unknown; guess |x| < 10 -> -22.8021, else 3.5*x^2 - 22.8
    out = []
    for x in probe["x"]:
        if x is None:
            out.append(None)
            continue
        if abs(x) < 10:
            out.append(-22.8021)
        else:
            out.append(3.5 * x * x - 22.8021)
    return {"y": out}
