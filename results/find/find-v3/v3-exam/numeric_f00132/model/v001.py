def predict(probe):
    # Observations look nearly linear in x: y/x is roughly constant ~4.76
    # across all points [E1]. Try y = a*x + b with a~4.76, b~0.
    # Check: 88.2*4.76=419.8 (obs 419.99); 66*4.76=314.2 (obs 315.3);
    # -20.3*4.76=-96.6 (obs -90.9); -61.7*4.76=-293.7 (obs -285.0).
    # Residuals suggest slight nonlinearity / offset. Fit a,b from E1.
    # Using least squares on E1 data:
    xs = [88.2,66.0,-20.3,-61.7,2.9,-24.3,72.7,-50.4,-6.0,21.3]
    ys = [419.9916,315.3396,-90.9303,-284.9572,17.8834,-109.6768,346.9238,-231.9982,-23.9374,104.6215]
    n=len(xs)
    sx=sum(xs); sy=sum(ys); sxx=sum(x*x for x in xs); sxy=sum(x*y for x,y in zip(xs,ys))
    a=(n*sxy-sx*sy)/(n*sxx-sx*sx)
    b=(sy-a*sx)/n
    return {"y":[a*x+b for x in probe["x"]]}
