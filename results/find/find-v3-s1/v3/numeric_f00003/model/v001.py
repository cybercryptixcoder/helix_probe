import math

def predict(probe):
    # Model hypotheses:
    # - For |x| large, f(x) grows roughly quadratically with |x| [E1]
    # - f is even-ish? Check: f(-93.6)=13835.8, f(88.9)=22155.9, f(67.5)=13475.7,
    #   f(-62.7)=5293.6, f(38.8)=5236.5, f(73.9)=15822.7, f(-104)=17162.4, f(-120.7)=22504.0
    # - Near x in [-13, -1.2], f ~ -20.45 (flat floor) [E1]
    # - Looks like f(x) = max(g(x), -20.45) where g is quadratic-ish in |x|?
    #   Check: 93.6^2=8761, *1.58=13842 ~ 13836. 88.9^2=7903, *2.80=22130 ~ 22156.
    #   Not constant coefficient. Try f = a*x^2 + b*|x| + c?
    #   Fit roughly: at x=-1.2 and -12.9 both give -20.4469 -> flat region.
    #   At 38.8: 5236.5; 67.5: 13475.7; 73.9: 15822.7; 88.9: 22155.9; 93.6: 13835.8 (odd, lower than 88.9!)
    #   Hmm 93.6 gives 13835.8 but 88.9 gives 22155.9 — not monotonic in |x|.
    #   Check 104: 17162.4; 120.7: 22504.0.
    #   So not simple quadratic. Possibly periodic or has structure.
    #   Let's look: values at |x|: 1.2->-20.4, 12.9->-20.4, 38.8->5236.5, 62.7->5293.6,
    #   67.5->13475.7, 73.9->15822.7, 88.9->22155.9, 93.6->13835.8, 104->17162.4, 120.7->22504.0
    #   These look like they could be a*x^2 with some noise? 38.8^2=1505, ratio 3.48; 62.7^2=3931, ratio 1.35.
    #   Not consistent. Maybe f(x) = something like (x^2)/k + noise? Or a neural net approximation of some function.
    #   Given it's an MLP approximating some function, and values are large positive for large |x|,
    #   with a flat negative region near 0, maybe f(x) = max(0, x^2 - c) + noise? 
    #   At x=38.8: 1505-c=5236 -> c negative. No.
    #   Try f(x) = x^2 * something? 
    #   Actually maybe f(x) = (x^2)/something + noise, but 93.6^2=8761 vs 88.9^2=7903, yet f(93.6)<f(88.9).
    #   That's a big anomaly. Could be noise, or the function isn't monotonic.
    #   Given MLP, could be approximating something like x^2*sin(x) or similar.
    #   Without more data, best guess: quadratic in x with noise, plus a floor near 0.
    #   Let's fit a*x^2 + b for large |x|: using 120.7: 14568a+b=22504; 104: 10816a+b=17162.
    #   Subtract: 3752a=5342 -> a=1.424, b=22504-14568*1.424=22504-20745=1759.
    #   Check 88.9: 7903*1.424+1759=11254+1759=13013, but observed 22156. Way off.
    #   So not a single quadratic.
    #   Given the difficulty, best guess: f(x) ≈ x^2/ something with noise, floor at -20.45.
    #   Actually let's check: maybe f(x) = (x^2)/4 + noise? 120.7^2/4=3642, no.
    #   Maybe f(x) = x^2 * |sin(x)|? 120.7: sin=0.66, 14568*0.66=9615, no.
    #   Given limited data, I'll model as: for |x| < 20, f ≈ -20.45 (flat); for |x|>=20, f ≈ x^2 * 1.5 + noise.
    #   But 93.6 anomaly suggests noise is large or function is complex.
    #   Best simple model: f(x) = max(-20.45, x^2 * 1.5) with noise? 
    #   38.8: 1505*1.5=2258 vs 5236. 62.7: 3931*1.5=5897 vs 5294. 67.5: 4556*1.5=6834 vs 13476.
    #   Not great. 
    #   Try f(x) = x^2 * 2.5 - 20? 38.8: 3763-20=3743 vs 5236. 67.5: 11391-20=11371 vs 13476.
    #   88.9: 19758-20=19738 vs 22156. 120.7: 36420-20=36400 vs 22504. No.
    #   The data is quite noisy/nonmonotonic. Given it's an MLP, I'll just use a smooth approximation.
    #   Let me try f(x) = a*x^2 + b*x + c fit to a few points... but too few.
    #   I'll go with: flat region |x|<20 -> -20.45; else quadratic fit through (38.8,5236),(67.5,13476),(120.7,22504).
    #   Fit: a*1505+b*38.8+c=5236; a*4556+b*67.5+c=13476; a*14568+b*120.7+c=22504.
    #   From 1&2: a*3051+b*28.7=8240. From 2&3: a*10012+b*53.2=9028.
    #   Solve: from first b=(8240-3051a)/28.7. Sub: 10012a+53.2*(8240-3051a)/28.7=9028
    #   10012a + 1.8537*(8240-3051a)=9028 -> 10012a+15274-5656a=9028 -> 4356a=-6246 -> a=-1.434. Negative, bad.
    #   So not quadratic. 
    #   Given the mess, I'll just predict a rough quadratic: f(x) ≈ 1.5*x^2 - 20 for |x|>20, else -20.45.
    #   This won't be accurate but it's a start. Mark as uncertain.
    out = []
    for x in probe.get("x", []):
        if x is None:
            out.append(None)
            continue
        if abs(x) < 20:
            out.append(-20.4469)
        else:
            out.append(1.5 * x * x - 20.0)
    return {"y": out}
