def predict(probe):
    # Observations show y ≈ 4.76 * x across all points [E1]
    # Check: 88.2*4.76=419.8, 66*4.76=314.2, -20.3*4.76=-96.6 (close-ish)
    # Let's fit more precisely: 419.9916/88.2=4.7618, 315.3396/66=4.7779
    # -90.9303/-20.3=4.4793, -284.9572/-61.7=4.6184, 17.8834/2.9=6.1667
    # -109.6768/-24.3=4.5134, 346.9238/72.7=4.7720, -231.9982/-50.4=4.6031
    # -23.9374/-6=3.9896, 104.6215/21.3=4.9118
    # Not perfectly linear. Ratios vary. Maybe nonlinear/MLP approximation.
    # Try linear fit: slope ~4.7, but small x has larger ratio.
    # 2.9 -> 17.88, -6 -> -23.94. Ratio ~6.17 and 3.99. Hmm.
    # Try y = a*x + b*x^2? Or tanh-like?
    # Let's just do a linear fit through origin-ish plus check.
    # Sum x*y / sum x^2:
    xs=[88.2,66.0,-20.3,-61.7,2.9,-24.3,72.7,-50.4,-6.0,21.3]
    ys=[419.9916,315.3396,-90.9303,-284.9572,17.8834,-109.6768,346.9238,-231.9982,-23.9374,104.6215]
    # slope = sum(xy)/sum(x^2)
    sxy=sum(x*y for x,y in zip(xs,ys))
    sxx=sum(x*x for x in xs)
    slope=sxy/sxx
    # intercept
    mx=sum(xs)/len(xs); my=sum(ys)/len(ys)
    intercept=my-slope*mx
    # But MLP could be nonlinear. Let's try y = A*tanh(x/k)*something? 
    # Actually ratios: for |x| large ratio ~4.7, for small |x| ratio varies.
    # 2.9->6.17, -6->3.99, 21.3->4.91, -20.3->4.48
    # Could be y = 4.7*x + small nonlinearity. Let's just use linear fit.
    out={}
    out["y"]=[slope*x+intercept for x in probe["x"]]
    return out
