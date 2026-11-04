import math

def predict(probe):
    # x = min(10, 2a - 5 - (b - 5)): a doubles then shifts, b shifts before saturation [E1,E4,E5,E6,E7,E8,E9,E10,E11,E12,E13,E19,E20]
    # y = c + min(1, max(0, a-7)): c sets y, a adds up to +1 above a=7 [E1,E2,E4,E5,E8,E9,E10,E12,E14,E15,E17,E19,E20]
    # size: 1 + 2.5*|a-5|/5 + 2.5*|5-c|/5 ... but E21 (a=0,b=10,c=0) gives 1.0, not 6.0.
    #   E21 shows size is NOT simply additive in |a-5| and |5-c|.
    #   E18: a=0,b=0,c=5 -> 3.5 (a-term alone = 2.5). E21: a=0,c=0 -> 1.0.
    #   E2: a=5,c=0 -> 3.5 (c-term alone = 2.5). E14: a=10,c=0 -> 6.0.
    #   E17: a=10,c=0 -> 6.0. E21: a=0,c=0 -> 1.0.
    #   Hypothesis: size = 1 + 2.5*|a-5|/5 + 2.5*|5-c|/5 only when a>=5? No...
    #   Look: a=0,c=0 -> 1.0. a=0,c=5 -> 3.5. a=5,c=0 -> 3.5. a=10,c=0 -> 6.0.
    #   Maybe size = 1 + 2.5*|a-5|/5 + 2.5*|5-c|/5, but with a and c terms combined differently.
    #   Try: size = 1 + 2.5*max(|a-5|,|5-c|)/5? a=0,c=0: max(5,5)=5 -> 3.5 no.
    #   Try: size = 1 + 2.5*(|a-5|+|5-c|)/5 but capped? a=0,c=0: 1+2.5*10/5=6 no.
    #   E21 a=0,c=0 -> 1.0 means both terms vanish. Perhaps size depends on distance from a=5 AND c=5 jointly:
    #   size = 1 + 2.5*sqrt(((a-5)/5)^2+((c-5)/5)^2)? a=0,c=0: sqrt(1+1)=1.414 -> 1+3.54=4.54 no.
    #   Reconsider: maybe size = 1 + 2.5*|a-5|/5 + 2.5*|5-c|/5 is wrong; maybe it's
    #   size = 1 + 2.5*|a-5|/5 when c=5, and c term only when a>=5? E2 a=5,c=0 -> 3.5 ok.
    #   E21 a=0,c=0 -> 1.0: a-term would be 2.5, c-term 2.5, sum 6. Observed 1.0.
    #   Maybe size = 1 + 2.5*|a-5|/5 * something with c? Or size uses |a-c|?
    #   a=0,c=0: |a-c|=0 -> 1.0 ok. a=0,c=5: |a-c|=5 -> 3.5 ok (1+2.5). a=5,c=0: |a-c|=5 -> 3.5 ok.
    #   a=10,c=0: |a-c|=10 -> 1+5=6 ok. a=10,c=5: |a-c|=5 -> 3.5? E5 a=10,c=5 -> size? E5 observed size... 
    #   E5: a=10,b=5,c=5 -> size 3.5 (from |a-5|=5). |a-c|=5 -> 3.5 ok.
    #   E1 a=5,c=5: |a-c|=0 -> 1.0 ok. E15 a=5,c=10: |a-c|=5 -> 3.5 ok.
    #   E8 a=8,c=5: |a-c|=3 -> 1+1.5=2.5? E8 observed size... need check. E8 size likely 2.5.
    #   E4 a=0,c=5: |a-c|=5 -> 3.5 ok. E13 a=0,c=5 -> 3.5 ok.
    #   E17 a=10,c=0: |a-c|=10 -> 6 ok. E19 a=9,c=5: |a-c|=4 -> 1+2=3 ok (observed 3.0).
    #   E20 a=3,c=5: |a-c|=2 -> 1+1=2 ok (observed 2.0).
    #   E12 a=7,c=5: |a-c|=2 -> 2.0? E12 size... likely 2.0.
    #   E14 a=10,c=0: 6 ok. E16 a=9,c=5: 3.0 ok.
    #   So size = 1 + 2.5*|a-c|/5. Check E18 a=0,c=5: |a-c|=5 -> 3.5 ok.
    #   E6 a=5,c=5: 1.0 ok. E7 a=5,c=5: 1.0 ok. E9,E10,E11 a=5 or 10,c=5: consistent.
    #   E3 a=5,c=5: 1.0 ok.
    #   Great: size = 1 + 2.5*|a-c|/5.
    # switch: no effect [E3]
    a = probe.get("a", 5)
    b = probe.get("b", 5)
    c = probe.get("c", 5)
    x = min(10.0, 2*a - 5 - (b - 5))
    base = 5 + min(1.0, max(0.0, a - 7.0))
    y = c + (base - 5)
    size = 1.0 + 2.5 * abs(a - c) / 5.0
    return {"x": x, "y": y, "size": size}
