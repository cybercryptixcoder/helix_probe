def predict(probe):
    # f(x) = round(x) [E1: 88.2->89, 66.0->67, -20.3->-22, -61.7->-63, 2.9->3, -24.3->-26, 72.7->73, -50.4->-52, -6.0->-7, 21.3->22]
    # Note: -20.3->-22 and -24.3->-26 suggest floor-like behavior on negatives, but 88.2->89 is round.
    # Actually check: round(88.2)=88, not 89. floor(88.2+0.5)=88. Hmm.
    # -20.3 -> -22? round(-20.3)=-20. floor(-20.3)=-21. Neither gives -22.
    # Let's recheck: maybe it's floor(x)-1 for negatives? -20.3 -> -22 = floor(-20.3)-1 = -21-1=-22. Yes!
    # -24.3 -> -26 = floor(-24.3)-1 = -25-1=-26. Yes!
    # -61.7 -> -63 = floor(-61.7)-1 = -62-1=-63. Yes!
    # -50.4 -> -52 = floor(-50.4)-1 = -51-1=-52. Yes!
    # -6.0 -> -7 = floor(-6.0)-1 = -6-1=-7. Yes!
    # Positives: 88.2->89 = ceil(88.2)=89. 66.0->67 = ceil(66.0)+? ceil(66)=66, not 67. Hmm.
    # 66.0 -> 67. 2.9 -> 3 = ceil(2.9)=3. 72.7->73=ceil. 21.3->22=ceil.
    # 66.0 -> 67: ceil(66)=66. floor(66)+1=67. So maybe floor(x)+1 for positives?
    # 88.2: floor(88.2)+1=89. Yes! 2.9: floor(2.9)+1=3. Yes! 72.7: floor+1=73. Yes! 21.3: floor+1=22. Yes!
    # So: positives -> floor(x)+1, negatives -> floor(x)-1.
    # That's floor(x) + sign(x) essentially, or floor(x) + (1 if x>=0 else -1).
    # What about x=0? Unknown. Guess floor(0)+1=1? Or maybe 0. Mark with ?.
    import math
    out = []
    for x in probe["x"]:
        if x >= 0:
            out.append(math.floor(x) + 1)
        else:
            out.append(math.floor(x) - 1)
    return {"y": out}
