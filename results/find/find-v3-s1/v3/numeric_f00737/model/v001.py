def predict(probe):
    # Only positive x in [~30, ~90] gave values so far [E1]
    # Values ~25-33 suggest something like sqrt-ish or log-ish scaling [E1]
    # x<=0 -> null [E1]
    # Outside positive range -> null [E1]
    import math
    out = []
    for x in probe["x"]:
        if x is None or x <= 0:
            out.append(None)
        else:
            # guess: sqrt(x) + something? sqrt(88.9)=9.43, no.
            # try x^0.25? 88.9^0.25=3.07, no.
            # 33.047 for 88.9, 30.54 for 67.5, 25.5 for 38.8
            # differences: 88.9-67.5=21.4 -> 2.5 ; 67.5-38.8=28.7 -> 5.04
            # looks like ~ log2? log2(88.9)=6.47 no
            # try 10*log10(x)+... 10*log10(88.9)=19.5
            # try x^(1/3): 88.9^(1/3)=4.46
            # try 20*log10(x)? 38.8 -> 31.7 close to 25.5? no
            # try 10*ln(x)? ln(88.9)=4.49 -> 44.9 no
            # try sqrt(x)*3.5: sqrt(88.9)=9.43*3.5=33.0 yes!
            # sqrt(67.5)=8.216*3.5=28.76 vs 30.54 no
            # try sqrt(x)+24: 9.43+24=33.43; 8.216+24=32.2 no
            # try 3.5*sqrt(x): check 38.8: sqrt=6.23*3.5=21.8 vs 25.5 no
            # try a*sqrt(x)+b: solve 88.9,38.8
            # a*9.429+b=33.047; a*6.229+b=25.5 -> a*3.2=7.547 -> a=2.358, b=10.82
            # check 67.5: 2.358*8.216+10.82=30.19 vs 30.54 close
            # maybe log: a*ln(x)+b: ln88.9=4.487, ln38.8=3.658 -> a*0.829=7.547->a=9.10,b=-7.79
            # check 67.5: 9.10*4.212-7.79=30.54 yes!
            # So y = 9.1*ln(x) - 7.79? check 88.9: 9.1*4.487-7.79=33.04 yes
            # Fit: a*ln(x)+b. Using 88.9 and 67.5:
            # a*(4.487-4.212)=33.047-30.5403=2.5067 -> a=9.115
            # b=33.047-9.115*4.487=33.047-40.90=-7.85
            # check 38.8: 9.115*3.658-7.85=25.49 yes!
            # So y = 9.115*ln(x) - 7.85 for x>0
            # But null for x<=0 and for x<~? 38.8 works, -1.2 null, -12.9 null
            # What about small positive? unknown. Guess threshold at x>0.
            # But -1.2 null, -12.9 null, -62.7 null, -93.6 null, -104 null, -120.7 null
            # All negatives null. Positives: 38.8,67.5,73.9,88.9 all work.
            # Maybe domain is x>0. But could be x>=some positive. Guess x>0.
            out.append(9.115*math.log(x) - 7.85)
    return {"y": out}
