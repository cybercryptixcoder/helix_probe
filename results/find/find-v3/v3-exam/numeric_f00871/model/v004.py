def predict(probe):
    # Central linear region: f(x) = 5.2 - 2.5*x on [-2.1, 2.1], else 0 [E4, E6, E8]
    #   left edge: f(-2.1)=10.45, f(-2.2)=0; right edge: f(2.1)=-0.05, f(2.2)=0
    # Second nonzero region near x=-79 with noisy values ~0.1-0.27 [E9, E10]
    #   nonzero at -79.3..-78.0 and -85.0, but 0 at -75, -70, -60, -90, -100 [E10]
    #   values are noisy/irregular -> treat as a noisy bump around x=-79, width ~[-86,-77]?
    import math
    out = []
    for x in probe["x"]:
        if -2.1 <= x <= 2.1:
            out.append(5.2 - 2.5 * x)
        elif -86.0 <= x <= -77.0:
            # noisy bump; approximate with a smooth hump peaking near -79
            # values: -79.0:0.2211, -80:0.2264, -78:0.2709, -85:0.2242, -79.1:0.169
            # use a rough constant-ish estimate ~0.2 with mild variation
            out.append(0.2)
        else:
            out.append(0.0)
    return {"y": out}
