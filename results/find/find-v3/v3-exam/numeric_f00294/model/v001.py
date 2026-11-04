def predict(probe):
    # f(x) = x + 17.6 approximately [E1]
    # Check: 88.2->105.8 (+17.6), 66.0->82.8 (+16.8), -20.3->-28.4 (-8.1?) 
    # Wait, let's recompute differences:
    # 88.2 -> 105.8 : +17.6
    # 66.0 -> 82.8  : +16.8
    # -20.3 -> -28.4: -8.1  (not constant!)
    # -61.7 -> -69.4: -7.7
    # 2.9 -> 19.8   : +16.9
    # -24.3 -> -32.4: -8.1
    # 72.7 -> 89.8  : +17.1
    # -50.4 -> -58.4: -8.0
    # -6.0 -> -14.4 : -8.4
    # 21.3 -> 38.8  : +17.5
    # Pattern: positive x -> +~17, negative x -> -~8
    # Looks like f(x) = x + 17.6 for x>0, x - 8 for x<0? 
    # Check: 2.9+16.9=19.8 ok. -6-8.4=-14.4 ok. 
    # Maybe f(x) = x + 17.6 if x>=0 else x - 8
    # 66+16.8 = 82.8, hmm 16.8 not 17.6. 88.2+17.6=105.8. 72.7+17.1=89.8.
    # 21.3+17.5=38.8. Not constant. Maybe f(x) = x + 17.6 - something?
    # Or f(x) = 1.2*x? 88.2*1.2=105.84 yes! 66*1.2=79.2 no.
    # Try f(x) = x + 17.6 for x>0: 66+17.6=83.6 vs 82.8. close but off.
    # Try f(x) = x*1.2 for positives: 88.2*1.2=105.84 ok, 66*1.2=79.2 no.
    # Hmm. 66->82.8 = 66*1.2545. 72.7->89.8=1.235. 21.3->38.8=1.82.
    # Let's try f(x)=x+17.6 for x>0 but 66 gives 83.6 not 82.8.
    # Maybe f(x) = x + 17.6 - 0.8*floor? 
    # Actually maybe f(x) = x + 17.6 for x>0, but with rounding? 82.8 vs 83.6 diff 0.8.
    # Try f(x) = x + 17.6 - 0.1*x? 88.2: 88.2+17.6-8.82=97 no.
    # Try f(x) = 1.2*x for x>0: 88.2->105.84 (obs 105.8 ok), 66->79.2 (obs 82.8 no)
    # Try f(x) = x + 17.6 for x>0: 88.2->105.8 ok, 66->83.6 (obs 82.8, off 0.8)
    # 72.7->90.3 (obs 89.8, off 0.5). 21.3->38.9 (obs 38.8, off 0.1). 2.9->20.5 (obs 19.8, off 0.7)
    # Offsets: 0, 0.8, 0.5, 0.1, 0.7. Hmm.
    # Maybe f(x) = x + 17.6 - 0.01*x^2? 88.2: 17.6-77.8 = -60 no.
    # Try f(x)=x+17.6 for x>0, x-8 for x<0, seems close enough. 
    # Actually maybe f(x) = x + 17.6 if x>0 else x - 8. Let's just go with that.
    # For negatives: -20.3-8=-28.3 (obs -28.4, off 0.1). -61.7-8=-69.7 (obs -69.4, off 0.3)
    # -24.3-8=-32.3 (obs -32.4). -50.4-8=-58.4 ok. -6-8=-14 (obs -14.4).
    # Good enough. Maybe f(x) = x + 17.6 for x>=0 else x - 8.4?
    # -20.3-8.1=-28.4 ok. -61.7-7.7=-69.4. -24.3-8.1=-32.4. -50.4-8=-58.4. -6-8.4=-14.4.
    # avg negative offset ~ -8.06. Use -8.
    # positives avg: 17.6,16.8,16.9,17.1,17.5 -> ~17.2
    # Use f(x)=x+17.2 if x>=0 else x-8
    out=[]
    for x in probe["x"]:
        if x>=0:
            out.append(x+17.2)
        else:
            out.append(x-8.0)
    return {"y":out}
