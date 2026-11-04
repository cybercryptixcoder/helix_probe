import math

def predict(probe):
    # f is smooth, monotone decreasing, roughly odd with offset [E2,E4]
    # f(0) ≈ -8.83 [E2]
    # Central slope ~3.4 near 0, decreasing outward [E2,E4]
    # Negative tail: nearly linear slope ~0.53 beyond x<-40 [E2]
    # Positive tail: slope decays to ~0.18 near x=100-120 [E2]
    # Smooth curvature, no kink; transitions gradual [E4]
    # Model: f(x) = c - A*tanh(x/s) + B*x/(1+(x/w)^2) style blend
    # Use a flexible form: f(x) = c - A*tanh(x/s) - d*x/(1+(x/w)^2)
    # Fit key points: f(0)=-8.83, f(1)-f(-1)=-6.87 (slope 3.435 at 0)
    # f(20)=-44.75, f(-20)=18.59, f(100)=-66.08, f(-100)=61.21
    # Try: f(x) = c - A*tanh(x/s) - d*x
    # At large x, tanh->1: f≈c-A-d*x (linear pos tail) but pos tail flattens...
    # Actually pos tail flattens, neg tail linear. Asymmetric.
    # Use: f(x) = c - A*tanh(x/s) - d*x*exp(-(x/w)^2) for x>0? 
    # Simpler robust approach: monotone cubic-ish interpolation through dense knots
    # with smooth extrapolation. Knots from E2+E4 combined.
    knots = [
        (-128, 76.05),(-100,61.2126),(-80,50.5605),(-60,39.9084),(-40,29.2562),
        (-25, 22.0),(-20,18.5887),(-15,15.8),(-12,14.2),(-10,13.1151),
        (-8,10.7344),(-7,8.6858),(-6,6.6373),(-5,4.5567),(-4,2.313),
        (-3,-0.0686),(-2.5,-1.3143),(-2,-2.5588),(-1.5,-3.8538),(-1,-5.3751),
        (-0.5,-7.0942),(0,-8.8302),(0.5,-10.5679),(1,-12.242),(1.5,-13.9089),
        (2,-15.5757),(2.5,-17.2425),(3,-18.9094),(4,-22.2431),(5,-25.4152),
        (6,-28.462),(7,-31.5088),(8,-34.5556),(10,-36.3993),(12,-38.0921),
        (15,-40.6313),(20,-44.7483),(25,-47.8001),(30,-49.8414),(40,-53.5169),
        (60,-58.8789),(65.5,-59.8689),(80,-62.479),(100,-66.079),(104.5,-66.889),
        (120,-69.6791),(123.6,-70.3271),(128,-71.12)
    ]
    out = []
    for x in probe.get("x", []):
        try:
            x = float(x)
            if x <= knots[0][0]:
                # extrapolate using last slope
                s = (knots[1][1]-knots[0][1])/(knots[1][0]-knots[0][0])
                out.append(knots[0][1] + s*(x-knots[0][0]))
            elif x >= knots[-1][0]:
                s = (knots[-1][1]-knots[-2][1])/(knots[-1][0]-knots[-2][0])
                out.append(knots[-1][1] + s*(x-knots[-1][0]))
            else:
                for i in range(len(knots)-1):
                    x0,y0 = knots[i]; x1,y1 = knots[i+1]
                    if x0 <= x <= x1:
                        t = (x-x0)/(x1-x0)
                        # smoothstep for smoother interpolation
                        ts = t*t*(3-2*t)
                        out.append(y0 + ts*(y1-y0))
                        break
        except Exception:
            out.append(None)
    return {"y": out}
