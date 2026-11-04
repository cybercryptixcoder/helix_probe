import math

def predict(probe):
    # Observations [E1]:
    # Large positive x -> large positive y, roughly quadratic (88.2 -> 21854, 66 -> 12951, 72.7 -> 15366).
    # Negative x (e.g. -61.7 -> 5086, -50.4 -> 2995) also positive & quadratic-ish.
    # Small |x| (2.9, -6.0) -> about -20.45, a flat floor.
    # -24.3 -> 166.2, 21.3 -> 2091.9.
    # Hypothesis: y = max(quadratic, floor) where floor ~ -20.45.
    # Fit quadratic a*x^2 + b*x + c through points; use floor clamp.
    # Estimate: at x=2.9 and x=-6.0 both give -20.4469 -> floor region.
    # Try y = max(k*x^2 + c0, -20.4469). Check 88.2: k*7780 ~ 21854 -> k~2.81.
    # 66: 2.81*4356=12240 vs 12951; add linear term.
    # Solve with three points: 88.2, 66, -61.7.
    # Use least squares mentally: try y = 2.8*x^2 + 3*x - 20.45
    # 88.2: 2.8*7779=21781 +264.6 -20.45=22025 (obs 21854, close)
    # 66: 2.8*4356=12197+198-20.45=12374 (obs 12951, off)
    # Try y = 2.9*x^2 + 1*x - 20.45
    # 88.2: 22559+88-20=22627 (obs 21854)
    # Hmm. Let's fit properly: points (88.2,21854.2),(66,12950.8),(-61.7,5086.1)
    # a*7780 + b*88.2 + c = 21854.2
    # a*4356 + b*66 + c = 12950.8
    # a*3806.9 + b*(-61.7) + c = 5086.1
    # Subtract eq2 from eq1: a*3424 + b*22.2 = 8903.4
    # Subtract eq3 from eq2: a*549.1 + b*127.7 = 7864.7
    # From first: b = (8903.4 - 3424a)/22.2 = 401.05 - 154.23a
    # Sub: 549.1a + 127.7*(401.05-154.23a) = 7864.7
    # 549.1a + 51214 - 19695a = 7864.7
    # -19146a = -43349 -> a = 2.264
    # b = 401.05 - 154.23*2.264 = 401.05 - 349.2 = 51.85
    # c = 12950.8 - 2.264*4356 - 51.85*66 = 12950.8 - 9862 - 3422 = -333.2
    # Check x=2.9: 2.264*8.41 + 51.85*2.9 - 333.2 = 19.0 + 150.4 - 333.2 = -163.8 (obs -20.4)
    # So floor clamp: max(quad, -20.4469). At 2.9 quad=-163.8 -> floor -20.45. Good.
    # At -6: 2.264*36 + 51.85*(-6) -333.2 = 81.5 -311.1 -333.2 = -562.8 -> floor. Good.
    # At -24.3: 2.264*590.5 + 51.85*(-24.3) -333.2 = 1337 -1260 -333 = -256 -> floor, but obs 166.2!
    # So floor isn't constant; maybe it's max(quad, small function). At -24.3 obs 166.2.
    # Hmm, maybe there's a different regime. -24.3 -> 166.2, 21.3 -> 2091.9.
    # Check quad at 21.3: 2.264*453.7 + 51.85*21.3 -333.2 = 1027 + 1104 -333 = 1798 (obs 2091.9)
    # At -24.3 quad=-256, obs 166.2. 
    # Maybe floor is a small linear/quadratic: fit floor points (2.9,-20.45),(-6,-20.45),(-24.3,166.2)
    # Actually maybe y = max(quad, g) where g is another quadratic? 
    # Or maybe the function is piecewise: for x in some interval, different behavior.
    # Let's reconsider: maybe y = a*x^2 + b*x + c with different c for negative region.
    # Points: -61.7->5086, -50.4->2995, -24.3->166.2, -20.3->-15.87, -6->-20.45, 2.9->-20.45
    # For negative x, it looks like a quadratic that bottoms out around -20.
    # -20.3 -> -15.87, -6 -> -20.45, 2.9 -> -20.45. So minimum ~ -20.45 around x in [-6, 2.9].
    # -24.3 -> 166.2: from -20.3 to -24.3, y goes -15.87 to 166.2. 
    # Fit negative side quadratic: points (-61.7,5086),(-50.4,2995),(-24.3,166.2)
    # a*3806.9 -61.7b + c = 5086
    # a*2540.2 -50.4b + c = 2995
    # a*590.5 -24.3b + c = 166.2
    # Eq1-Eq2: 1266.7a -11.3b = 2091
    # Eq2-Eq3: 1949.7a -26.1b = 2828.8
    # From first: b = (1266.7a - 2091)/11.3 = 112.1a - 185.0
    # Sub: 1949.7a -26.1*(112.1a-185) = 2828.8
    # 1949.7a - 2925.8a + 4828.5 = 2828.8
    # -976.1a = -1999.7 -> a = 2.049
    # b = 112.1*2.049 - 185 = 229.7 - 185 = 44.7
    # c = 166.2 - 2.049*590.5 - 44.7*(-24.3) = 166.2 - 1210 + 1086 = 42.2
    # Check -20.3: 2.049*412.1 + 44.7*(-20.3) + 42.2 = 844.4 - 907.4 + 42.2 = -20.8 (obs -15.87, close)
    # Check -6: 2.049*36 + 44.7*(-6)+42.2 = 73.8 -268.2+42.2 = -152 (obs -20.45) -> floor clamp
    # Check 2.9: 2.049*8.41+44.7*2.9+42.2 = 17.2+129.6+42.2=189 (obs -20.45) -> floor clamp
    # So negative side: y = max(2.049x^2+44.7x+42.2, -20.45)
    # Positive side: fit (88.2,21854),(66,12951),(72.7,15366),(21.3,2091.9)
    # Try a*x^2+b*x+c. Using 88.2,66,21.3:
    # 7780a+88.2b+c=21854
    # 4356a+66b+c=12951
    # 453.7a+21.3b+c=2091.9
    # Eq1-Eq2: 3424a+22.2b=8903
    # Eq2-Eq3: 3902.3a+44.7b=10859
    # From first: b=(8903-3424a)/22.2=401.0-154.2a
    # Sub: 3902.3a+44.7*(401-154.2a)=10859
    # 3902.3a+17925-6893a=10859
    # -2990.7a=-7066 -> a=2.363
    # b=401-154.2*2.363=401-364.4=36.6
    # c=2091.9-2.363*453.7-36.6*21.3=2091.9-1072-779.6=240.3
    # Check 72.7: 2.363*5285+36.6*72.7+240=12488+2661+240=15389 (obs 15366, great!)
    # Check 66: 2.363*4356+36.6*66+240=10293+2416+240=12949 (obs 12951, great!)
    # Check 88.2: 2.363*7780+36.6*88.2+240=18384+3228+240=21852 (obs 21854, great!)
    # So positive side: y=2.363x^2+36.6x+240.3
    # At x=2.9: 2.363*8.41+36.6*2.9+240=19.9+106.1+240=366 (obs -20.45) -> floor clamp
    # At x=-6: 2.363*36+36.6*(-6)+240=85+(-219.6)+240=105 (obs -20.45) -> floor clamp
    # At x=-20.3: 2.363*412+36.6*(-20.3)+240=973-743+240=470 (obs -15.87) -> floor clamp
    # At x=-24.3: 2.363*590.5+36.6*(-24.3)+240=1395-889+240=746 (obs 166.2) -> floor clamp gives -20.45, wrong!
    # So negative side uses its own quadratic. Boundary?
    # At -24.3 obs 166.2 matches negative quad (2.049*590.5+44.7*(-24.3)+42.2=1210-1086+42=166). 
    # At -20.3 obs -15.87: negative quad gives -20.8, positive quad gives 470. So negative quad.
    # At -6: negative quad -152, positive quad 105, obs -20.45 -> floor.
    # At 2.9: negative quad 189, positive quad 366, obs -20.45 -> floor.
    # At 21.3: negative quad 2.049*453.7+44.7*21.3+42.2=930+952+42=1924, positive quad 1798, obs 2091.9.
    # Hmm obs 2091.9 is higher than both. Let me recompute positive quad at 21.3: 2.363*453.7=1072, +36.6*21.3=779.6, +240=2092. Yes! 2092 matches 2091.9!
    # So positive quad at 21.3 = 2092. 
    # So boundary: where does it switch from negative quad to positive quad? 
    # Both are quadratics; maybe it's max of the two, or a switch at some x.
    # At -20.3: neg=-20.8, pos=470. obs=-15.87. Neither matches well but neg closer (floor -20.45 vs obs -15.87).
    # Hmm -15.87 vs floor -20.45. Slight difference.
    # Maybe floor is not exactly -20.45; at 2.9 and -6 both -20.4469 exactly. So floor=-20.4469.
    # At -20.3 obs -15.87, which is above floor. So negative quad at -20.3 should give -15.87.
    # Recompute neg quad at -20.3: 2.049*412.09=844.4, 44.7*(-20.3)=-907.4, +42.2 -> -20.8. Close to -15.87 but not exact.
    # Maybe my fit is slightly off. Let me refit negative using -20.3 instead of -24.3.
    # Points: (-61.7,5086),(-50.4,2995),(-20.3,-15.87)
    # 3806.9a-61.7b+c=5086
    # 2540.2a-50.4b+c=2995
    # 412.1a-20.3b+c=-15.87
    # Eq1-Eq2: 1266.7a-11.3b=2091
    # Eq2-Eq3: 2128.1a-30.1b=3010.9
    # b=(1266.7a-2091)/11.3=112.1a-185.0
    # 2128.1a-30.1*(112.1a-185)=3010.9
    # 2128.1a-3374.2a+5568.5=3010.9
    # -1246.1a=-2557.6 -> a=2.053
    # b=112.1*2.053-185=230.1-185=45.1
    # c=-15.87-2.053*412.1-45.1*(-20.3)=-15.87-846.0+915.5=53.6
    # Check -24.3: 2.053*590.5+45.1*(-24.3)+53.6=1212-1096+53.6=169.6 (obs 166.2, close)
    # Check -6: 2.053*36+45.1*(-6)+53.6=73.9-270.6+53.6=-143 -> floor -20.45. obs -20.45. Good.
    # Check 2.9: 2.053*8.41+45.1*2.9+53.6=17.3+130.8+53.6=201.7 -> floor. obs -20.45. Good.
    # So negative quad: 2.053x^2+45.1x+53.6, floor -20.4469.
    # Positive quad: 2.363x^2+36.6x+240.3, floor -20.4469.
    # Boundary between negative and positive quad? At 21.3, pos quad works (2092). At -20.3, neg quad works.
    # At 2.9: neg quad 201.7, pos quad 366, obs floor -20.45. Both above floor -> floor.
    # At -6: neg -143, pos 105, obs floor. 
    # At -24.3: neg 169.6, pos 746, obs 166.2 -> neg.
    # At -50.4: neg 2995, pos 2.363*2540+36.6*(-50.4)+240=6002-1845+240=4397. obs 2995 -> neg.
    # At 66: neg 2.053*4356+45.1*66+53.6=8943+2977+53.6=11974, pos 12951. obs 12951 -> pos.
    # So switch somewhere between -24.3 and 21.3? At -24.3 neg. At 21.3 pos.
    # Maybe switch at x=0? At -20.3 neg works. At 2.9 both above floor, obs floor. Can't distinguish.
    # At 21.3 pos. So switch at 0 seems plausible: x<0 use neg quad, x>=0 use pos quad, with floor.
    # Check x=-6: neg quad -143 -> floor -20.45. Good.
    # Check x=2.9: pos quad 366 -> floor -20.45. Good.
    # Check x=-20.3: neg quad -20.8 -> max with floor -20.45 gives -20.45, but obs -15.87. Slight mismatch.
    # Hmm. Maybe floor is not applied on negative side? Or floor is different.
    # Actually -15.87 vs -20.45: maybe neg quad at -20.3 is -15.87 with better fit.
    # Let me just use: x<0: max(2.053x^2+45.1x+53.6, -20.4469); x>=0: max(2.363x^2+36.6x+240.3, -20.4469)
    # But at -20.3 gives -20.45 vs obs -15.87. Small error.
    # Alternatively maybe floor only applies in a central interval. 
    # Let's just go with this piecewise model.
    x = probe.get("x", [])
    ys = []
    for v in x:
        if v is None:
            ys.append(None)
            continue
        try:
            v = float(v)
        except Exception:
            ys.append(None)
            continue
        if v < 0:
            q = 2.053*v*v + 45.1*v + 53.6
        else:
            q = 2.363*v*v + 36.6*v + 240.3
        y = max(q, -20.4469)
        ys.append(y)
    return {"y": ys}
