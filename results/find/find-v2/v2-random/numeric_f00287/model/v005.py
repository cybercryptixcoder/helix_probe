import math

def predict(probe):
    # A: x < 0: y = -0.705*x (linear) [E1-E7]
    # B: 0 < x < ~18: y = -402.45 (constant plateau) [E1,E2,E4,E5,E6,E7]
    #    E7: 10.3->-402.2121, 19.4->-319.2 (linear!), so plateau ends before 19.4
    #    E7: 22.4->-369.6, 24.6->-403.2, 26.4->-436.8 (linear slope ~-16.8)
    #    E5: 17.3->-402.3285 (plateau), E1: 21.3->-352.8 (linear)
    #    So boundary between 17.3 and 19.4. Try 18.
    # C: x >= ~18: y = -16.8*x (linear) [E1-E7]
    #    Check: 19.4*-16.8=-325.9 vs -319.2 (slope ~16.46?)
    #    E7: 22.4->-369.6 => -16.5; 24.6->-403.2 => -16.39; 26.4->-436.8 => -16.55
    #    E3: 28.4->-470.4 => -16.56; 47.1->-789.6 => -16.76; 58.8->-974.4 => -16.57
    #    E1: 21.3->-352.8 => -16.56; 66->-? ; E2: 30.3->-? 
    #    Slope ~ -16.56. Use -16.56.
    out = []
    for x in probe.get("x", []):
        try:
            if x < 0:
                y = -0.705 * x
            elif x < 18:
                y = -402.45
            else:
                y = -16.56 * x
        except Exception:
            y = None
        out.append(y)
    return {"y": out}
