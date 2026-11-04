def predict(probe):
    # f(x) = (13x^3 + 23x^2 - 16x - 486)/10 for x < ~97.55 [E1,E2,E3,E5,E6,E7,E9: exact at many points incl 97.5]
    # f(x) = ~7773 (noisy constant) for x >= ~97.55 [E4,E6,E8: f(97.55),f(97.6),...,f(102) all ~7773]
    # Boundary is in (97.5, 97.55]: f(97.5)=1226576.9625 (cubic), f(97.55)=7773.0037 (constant) [E8]
    # For x >= 97.55 the output is a noisy constant ~7773, NOT flat at 7772.9 [E3,E5,E9: 119.5->2251041.6, 119.7->2262308.6 are CUBIC!]
    # Wait: E3 123.6->2489592.58, E5 119.5->2251041.6, E9 119.7->2262308.6 are all cubic values, not constant!
    # So the constant region is NOT all x>=97.55. Large x follows the cubic again. [E3,E5,E9]
    # Constant region is a bounded interval above 97.55; need its upper bound. [E3:104.5,104.9,103.0 const; 123.6 cubic]
    out = []
    for x in probe["x"]:
        try:
            if 97.55 <= x <= 110.0:
                out.append(7773.0)
            else:
                out.append((13*x**3 + 23*x**2 - 16*x - 486) / 10.0)
        except Exception:
            out.append(None)
    return {"y": out}
