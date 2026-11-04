import math

def predict(probe):
    # Model hypotheses from E1:
    # - Outputs are null for x < 0 [E1: -20.3, -61.7, -24.3, -50.4, -6.0 all null]
    # - Outputs are non-null for x >= 0 [E1: 88.2, 66.0, 2.9, 72.7, 21.3]
    # - For x >= 0, y looks like log-ish / sqrt-ish of x:
    #     88.2 -> 32.975, 66.0 -> 30.3358, 72.7 -> 31.2158, 21.3 -> 20.0415, 2.9 -> 1.8914
    #   Try y = sqrt(x) + something? sqrt(88.2)=9.39 no.
    #   Try y = x^(1/2)? no. Try y = ln(x)*k? ln(88.2)=4.48, ratio 7.36; ln(66)=4.19 ratio 7.24;
    #   ln(72.7)=4.29 ratio 7.28; ln(21.3)=3.06 ratio 6.55; ln(2.9)=1.06 ratio 1.78. Not log.
    #   Try y = sqrt(x)*k? sqrt(88.2)=9.39 ratio 3.51; sqrt(66)=8.12 ratio 3.74; sqrt(72.7)=8.53 ratio 3.66;
    #   sqrt(21.3)=4.62 ratio 4.34; sqrt(2.9)=1.70 ratio 1.11. Not pure sqrt.
    #   Try y = x^(1/3)? 88.2^(1/3)=4.45 ratio 7.4; 66^(1/3)=4.04 ratio 7.5; 72.7^(1/3)=4.17 ratio 7.48;
    #   21.3^(1/3)=2.77 ratio 7.23; 2.9^(1/3)=1.43 ratio 1.32. Not.
    #   Try y = x^p: log-log fit. ln y vs ln x:
    #     (4.48,3.496),(4.19,3.412),(4.29,3.441),(3.06,2.998),(1.06,0.637)
    #   slope between last two: (2.998-0.637)/(3.06-1.06)=2.36/2.0=1.18
    #   slope between (3.06,2.998) and (4.48,3.496): 0.498/1.42=0.35. Not a power law.
    #   Try y = x/(x+a)? no, grows.
    #   Try y = a*ln(x+b)+c? Fit roughly. Use points (2.9,1.8914),(21.3,20.0415),(66,30.3358),(88.2,32.975)
    #   Differences: from 2.9 to 21.3: dy=18.15, dx=18.4 -> slope ~0.99
    #   from 21.3 to 66: dy=10.29, dx=44.7 -> slope 0.23
    #   from 66 to 88.2: dy=2.64, dx=22.2 -> slope 0.119
    #   Looks like y ~ sqrt(x)*something plus maybe linear near 0? Actually y(2.9)=1.89 ~ 2.9^0.6?
    #   Let's try y = sqrt(x) + x/10? 88.2: 9.39+8.82=18.2 no.
    #   Try y = 2*sqrt(x) + ...? 88.2: 18.78; need 32.98.
    #   Try y = sqrt(x)*x^(1/4)=x^(3/4)? 88.2^0.75=28.8; 66^0.75=23.2; 72.7^0.75=24.9; 21.3^0.75=9.9; 2.9^0.75=2.22. No.
    #   Try y = x^(2/3)? 88.2^(2/3)=19.8; no.
    #   Hmm, y(21.3)=20.04 ~ x. y(2.9)=1.89 ~ 0.65x. y(66)=30.3 ~ 0.46x. y(88.2)=32.98 ~ 0.374x.
    #   Try y = x/(1+ln(x)/c)? 88.2: ln=4.48, x/y=2.674 -> 1+4.48/c=2.674 -> c=2.68
    #     66: ln=4.19, x/y=2.176 -> 1+4.19/2.68=2.56 vs 2.176. no.
    #   Try y = a*sqrt(x)+b*x? Solve with (2.9,1.8914),(88.2,32.975):
    #     a*1.703+b*2.9=1.8914; a*9.392+b*88.2=32.975
    #     From first: a=(1.8914-2.9b)/1.703=1.1106-1.703b
    #     Sub: 9.392*(1.1106-1.703b)+88.2b=32.975 -> 10.43-15.99b+88.2b=32.975 -> 72.21b=22.545 -> b=0.3122
    #     a=1.1106-1.703*0.3122=1.1106-0.5317=0.5789
    #   Check 66: 0.5789*8.124+0.3122*66=4.703+20.605=25.31 vs 30.34. no.
    #   Try y = a*x^0.5 + b*x^0.25? 
    #   Actually maybe y = sqrt(x)*k where k varies... or y = x^(1/2)+x^(1/4)?
    #     88.2: 9.392+3.065=12.46 no.
    #   Try y = 2*x^(1/2)+x^(1/4)? 88.2: 18.78+3.065=21.85 no.
    #   Try y = x^(1/2)*ln(x)? 88.2: 9.392*4.48=42.1 no.
    #   Try y = sqrt(x*ln(x))? 88.2: sqrt(395)=19.9 no.
    #   Try y = x^(1/2)+x^(1/3)+x^(1/4)? 88.2: 9.39+4.45+3.07=16.9 no.
    #   Try y = x^(1/2)*2? no.
    #   Maybe y = sqrt(x^2 ...)? 
    #   Try y = x^(1/2) * c where c depends... 
    #   Let's try y = a*ln(x)+b*sqrt(x)+c. Three unknowns, use 3 points.
    #   (2.9,1.8914),(21.3,20.0415),(88.2,32.975)
    #   ln: 1.0647,3.0587,4.4795; sqrt:1.7029,4.6152,9.3915
    #   a*1.0647+b*1.7029+c=1.8914
    #   a*3.0587+b*4.6152+c=20.0415
    #   a*4.4795+b*9.3915+c=32.975
    #   Subtract: a*1.994+b*2.9123=18.1501
    #             a*1.4208+b*4.7763=12.9335
    #   From first: a=(18.1501-2.9123b)/1.994=9.102-1.4605b
    #   Sub: 1.4208*(9.102-1.4605b)+4.7763b=12.9335 -> 12.932-2.075b+4.7763b=12.9335 -> 2.7013b=0.0015 -> b=0.00056
    #   a=9.102-0.0008=9.101; c=1.8914-9.101*1.0647-0.00056*1.7029=1.8914-9.690=-7.798
    #   Check 66: 9.101*4.1897+0.00056*8.124-7.798=38.13-7.798=30.33 vs 30.3358. 
    #   Check 72.7: ln=4.286, sqrt=8.526: 9.101*4.286-7.798=39.01-7.798=31.21 vs 31.2158. 
    #   Check 21.3: 9.101*3.0587-7.798=27.84-7.798=20.04 vs 20.0415. 
    #   So y = 9.101*ln(x) - 7.798 for x>0. But that's weird constant. Maybe it's ln(x)*k - k*ln(something)?
    #   9.101*ln(x)-7.798 = 9.101*(ln(x)-0.8568) = 9.101*ln(x/2.356). Hmm.
    #   Or maybe y = ln(x^9.101 / e^7.798)... 
    #   Actually 9.101 ~ e^2.208? Or maybe it's ln(x)*something. Let's check if y = ln(x^a) form: a=9.101, offset.
    #   Maybe simpler: y = ln(x)*9.1 - 7.8. Let's just use that fit. But constants seem arbitrary.
    #   Alternative: maybe y = ln(x^9) - 7.8? Or y = 9*ln(x) - 7.8? Check 88.2: 9*4.4795-7.8=40.32-7.8=32.52 vs 32.975. Close-ish.
    #   Try y = 9*ln(x)-7.8: 66: 9*4.1897-7.8=37.71-7.8=29.91 vs 30.34. 
    #   Try y = 9.1*ln(x)-7.8: 88.2: 40.76-7.8=32.96 ✓; 66: 38.13-7.8=30.33 ✓; 72.7: 39.0-7.8=31.2 ✓; 21.3: 27.83-7.8=20.03 ✓; 2.9: 9.69-7.8=1.89 ✓
    #   So y = 9.1*ln(x) - 7.8 fits well. But maybe it's ln(x^9.1) - 7.8 or ln(x)*9.1-7.8.
    #   Could be y = ln(x^9.1 / e^7.8). Or maybe y = ln(x)*9.1 - 7.8 exactly.
    #   Actually maybe it's y = ln(x^9) - 7.8? 9*ln(88.2)=40.32, -7.8=32.52 vs 32.975 (off 0.45). With 9.1 off 0.015. So 9.1 better.
    #   Could be y = ln(x)*9.1 - 7.8, or y = ln(x)*9.1 - 7.8. Let's also consider y = ln(x)*e^2.2 - 7.8? e^2.2=9.025. Hmm.
    #   Let's just use y = 9.1*ln(x) - 7.8 for x>0, null for x<0. What about x=0? ln(0) undefined -> null.
    #   Mark as uncertain.
    out = []
    for x in probe["x"]:
        if x is None:
            out.append(None)
        elif x <= 0:
            out.append(None)
        else:
            out.append(9.1*math.log(x) - 7.8)
    return {"y": out}
