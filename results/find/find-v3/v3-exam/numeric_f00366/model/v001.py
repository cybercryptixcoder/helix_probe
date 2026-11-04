def predict(probe):
    # Outputs take only two values: -12.4 and 8.8 [E1]
    # 8.8 occurs for x in {-20.3, -61.7, -24.3, -50.4, -6.0}; -12.4 for {88.2, 66.0, 2.9, 72.7, 21.3} [E1]
    # Sign of x does not decide it (both signs appear on both sides) [E1]
    # Hypothesis: depends on fractional part / parity-like feature; best guess: x mod 1 region
    # ? Try: 8.8 when floor(x) is even, -12.4 when odd (fits E1: 88 even->-12.4? no)
    # ? Fit E1 by checking integer part parity:
    #   88.2->88 even -> -12.4 ; 66.0->66 even -> -12.4 ; -20.3->-21 odd -> 8.8
    #   -61.7->-62 even -> 8.8 (breaks parity). Use round-half? 
    # Best simple fit: 8.8 when x < 0 or x in (-10,10) except... 
    # From E1: negatives all -> 8.8 except none; positives: 2.9->-11.4 (special), others -12.4
    # ? Rule: x<0 -> 8.8 ; 0<=x<10 -> -11.4 ; x>=10 -> -12.4
    out = []
    for x in probe["x"]:
        if x < 0:
            out.append(8.8)
        elif x < 10:
            out.append(-11.4)
        else:
            out.append(-12.4)
    return {"y": out}
