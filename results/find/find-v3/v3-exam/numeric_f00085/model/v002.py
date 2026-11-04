def predict(probe):
    # f(x) = -22.8021 for |x| <= 5 (constant floor region) [E4: x=0,1,3,5 all -22.8021]
    # f(x) = 3.482*x^2 - 22.8021 for |x| >= 6, symmetric in x [E2,E3,E4,E5]
    # Transition is sharp at |x|=6: x=6 -> -8.55, x=6.5 -> 26.63 [E4]
    # Coefficient ~3.482: check x=128 -> 3.482*16384-22.8=57036 vs obs 50592 (hmm)
    # Recheck large: x=123.6 -> 3.482*15277-22.8=53172 vs obs 47994
    # x=104.9 -> 3.482*11004-22.8=38294 vs obs 36952
    # x=88.2 -> 3.482*7779-22.8=27065 vs obs 27090 (good)
    # x=66 -> 3.482*4356-22.8=15145 vs obs 15014 (good)
    # Large x seems to fall below 3.482*x^2. Try quadratic with slight negative cubic?
    # Or coefficient varies. Let's fit: use a*x^2+b with a from mid-range.
    # x=40: (5460.3+22.8)/1600=3.427; x=60:(12387.5+22.8)/3600=3.447
    # x=80:(22248.7+22.8)/6400=3.480; x=100:(34058.7+22.8)/10000=3.408
    # x=120:(45868.6+22.8)/14400=3.187; x=128:(50592.6+22.8)/16384=3.088
    # So it's not pure quadratic at large x - looks like tanh saturation or cubic term.
    # Try y = A*tanh(x^2/s)*... no. Try cubic: y = a*x^2 - c*x^3?
    # x=128: a*16384 - c*2097152 = 50615
    # x=100: a*10000 - c*1000000 = 34081
    # From these: solve. 16384a - 2097152c = 50615; 10000a-1000000c=34081
    # 10000a = 34081+1000000c -> a=3.4081+100c
    # 16384(3.4081+100c)-2097152c=50615 -> 55838+1638400c-2097152c=50615
    # -458752c = -5223 -> c=0.01139; a=3.4081+1.139=4.547? check x=40: 4.547*1600-0.01139*64000=7275-729=6546 vs 5460. no.
    # Maybe it's x^2 * something like a softplus/tanh. Simpler: try y = k*x^2 with k decreasing.
    # Actually maybe f(x)=a*(x^2) but with relu-like: could be a*x^2 for |x|<threshold and linear beyond?
    # x=120:45868/120=382; x=128:50592/128=395 — linear-ish at top? 
    # 120->45868, 128->50592: slope=(50592-45868)/8=590.5 per unit. Not linear (would be ~constant).
    # Let's just fit a smooth function. Try y = a*x^2 + b*x^4? 
    # Use x=60 (12387.5) and x=128 (50592.6):
    # 3600a+12960000b=12410; 16384a+268435456b=50615
    # a=(12410-12960000b)/3600=3.4472-3600b
    # 16384(3.4472-3600b)+268435456b=50615 -> 56479-58982400b+268435456b=50615
    # 209453056b=-5864 -> b negative. So concave, not quartic.
    # Try y = a*x^2/(1+x^2/s) saturating? At large x -> a*s (constant), but it grows. no.
    # Try y = a*x^2 - c*|x|^3:
    # 3600a-216000c=12410; 16384a-2097152c=50615
    # a=(12410+216000c)/3600=3.4472+60c
    # 16384(3.4472+60c)-2097152c=50615 -> 56479+983040c-2097152c=50615
    # -1114112c=-5864 -> c=0.005263; a=3.4472+0.3158=3.763
    # check x=88.2: 3.763*7779-0.005263*686128=29272-3611=25661 vs 27090. off.
    # Hmm. Let's just use piecewise linear interpolation-ish. Actually simplest robust:
    # fit y = a*x^2 + b with a slightly less than 3.482, accept error at extremes.
    # Use a=3.45: x=128->3.45*16384-22.8=56462 vs 50592 (11% off)
    # The large-x values are consistently lower. Could be tanh: y = C*tanh(x^2/D)?
    # tanh saturates -> constant, but values grow. no.
    # Maybe y = a*x^2 * sigmoid? Let me just try a*x^2 with a=3.45 and note large-x error.
    # Actually check: maybe it's a*x^2 where a depends... or maybe x^2 * 3.5 then clipped? 
    # x=128: 3.5*16384=57344, obs 50592. ratio 0.882
    # x=120: 3.5*14400=50400, obs 45868, ratio 0.910
    # x=100: 3.5*10000=35000, obs 34058, ratio 0.973
    # x=80: 3.5*6400=22400, obs 22248, ratio 0.993
    # So ratio drops at large x. Looks like tanh(x/something) factor? 
    # ratio = tanh(x/L)? x=128 ratio .882 -> tanh(128/L)=.882 -> 128/L=1.38 -> L=93
    # x=100: tanh(100/93)=tanh(1.075)=0.79, but ratio .973. no.
    # Maybe y = a*x^2 - b*x^2*|x|/scale... 
    # Let me try y = a*x^2/(1+|x|/L): x=128: a*16384/(1+128/L)=50592
    # x=80: a*6400/(1+80/L)=22248
    # ratio: (16384/(1+128/L))/(6400/(1+80/L))=50592/22248=2.274
    # 2.56*(1+80/L)/(1+128/L)=2.274 -> (1+80/L)/(1+128/L)=0.888
    # 1+80/L=0.888+113.7/L -> 0.112=33.7/L -> L=301
    # check a: 6400a/(1+80/301)=22248 -> 6400a/1.266=22248 -> a=4.40
    # x=128: 4.40*16384/(1+128/301)=72090/1.425=50590. YES! matches 50592!
    # x=100: 4.40*10000/(1+100/301)=44000/1.332=33033 vs 34058. close-ish (3%)
    # x=60: 4.40*3600/(1+60/301)=15840/1.199=13211 vs 12387. 6% off.
    # Not perfect. Let me try y = a*x^2/(1+(x/L)^2)? saturates. no.
    # Given time, use a*x^2 - b*x^3 form or just accept. Let me try simpler:
    # y = 3.5*x^2 for mid, but large x lower. Use y = 3.5*x^2 * (1 - x/1000)? 
    # x=128: 3.5*16384*(1-0.128)=57344*0.872=50004 vs 50592 good!
    # x=100: 35000*0.9=31500 vs 34058. off.
    # Hmm. Let me just fit quadratic through two points and accept.
    # Use x=40 (5460.3) and x=100 (34058.7):
    # 1600a+b=5483; 10000a+b=34081 -> 8400a=28598 -> a=3.4045; b=5483-5447=36
    # check x=128: 3.4045*16384+36=55810 vs 50592. off 10%.
    # The data really is sub-quadratic at large x. 
    # Best simple fit: y = a*x^2 - c*x^3 with a,c from x=80,x=128:
    # 6400a-512000c=22271; 16384a-2097152c=50615
    # a=(22271+512000c)/6400=3.4798+80c
    # 16384(3.4798+80c)-2097152c=50615 -> 57013+1310720c-2097152c=50615
    # -786432c=-6398 -> c=0.008135; a=3.4798+0.6508=4.1306
    # check x=60: 4.1306*3600-0.008135*216000=14870-1757=13113 vs 12387. 6% off.
    # check x=100: 4.1306*10000-0.008135*1000000=41306-8135=33171 vs 34058. 3% off.
    # check x=40: 4.1306*1600-0.008135*64000=6609-521=6088 vs 5460. 11% off.
    # Not great either. The function may be tanh-based MLP so no clean form.
    # I'll use a*x^2 with a=3.45 as compromise, plus small correction.
    # Actually let me just use the tanh-sigmoid fit which matched x=128 well:
    # y = 4.40*x^2/(1+|x|/301) - 22.8 for |x|>=6
    # check x=88.2: 4.40*7779/(1+0.293)=34228/1.293=26471-22.8=26448 vs 27090 (2% off)
    # check x=66: 4.40*4356/(1.219)=19166/1.219=15723-22.8=15700 vs 15014 (5% off)
    # check x=21.3: 4.40*453.7/1.071=1996/1.071=1864-22.8=1841 vs 1532 (20% off)
    # Small x off. Hmm.
    # The small-mid range fits 3.48*x^2-22.8 well, large x is lower.
    # Compromise: y = 3.48*x^2 - 22.8 for |x|<80, then taper.
    # Let me just do: y = 3.48*x^2 - 22.8, and for |x|>80 subtract extra.
    # x=100: 3.48*10000-22.8=34777 vs 34058 (2% off, ok)
    # x=120: 3.48*14400-22.8=50089 vs 45868 (9% off)
    # x=128: 3.48*16384-22.8=56993 vs 50592 (13% off)
    # So only very large x is off. Add cubic correction for |x|>80:
    # at x=128 need -6400; at x=120 need -4220; at x=100 need -720
    # roughly -0.003*(|x|-90)^3? x=128: -0.003*38^3=-164. no.
    # -0.5*(x-80)^2? x=128: -0.5*2304=-1152. no.
    # need -6400 at 128, -4220 at 120, -720 at 100.
    # fit quadratic in (x-80): at d=48: -6400; d=40:-4220; d=20:-720
    # 2304p+48q+r=-6400; 1600p+40q+r=-4220; 400p+20q+r=-720
    # subtract: 704p+8q=-2180; 1200p+20q=-3500
    # 8q=-2180-704p; q=-272.5-88p
    # 1200p+20(-272.5-88p)=-3500 -> 1200p-5450-1760p=-3500 -> -560p=1950 -> p=-3.48
    # q=-272.5-88(-3.48)=-272.5+306=33.5; r=-720-400(-3.48)-20(33.5)=-720+1392-670=2
    # So correction = -3.48*d^2+33.5*d+2 for d=x-80, x>80
    # check x=100 d=20: -3.48*400+670+2=-1392+672=-720. good
    # This is getting complex. Given exam scoring, let me just use the tanh-ish or accept.
    # I'll use: y = 3.48*x^2 - 22.8 for |x|<=80, and for |x|>80 use the cubic-corrected.
    # Actually simpler: the whole thing might be a*x^2 - b*x^3. Let me refit with all points.
    # Use least squares mentally is hard. I'll go with piecewise: quadratic for |x|<=80, 
    # and for |x|>80 subtract 3.48*(|x|-80)^2 - 33.5*(|x|-80) - 2.
    # Wait that gives correction negative (subtract). Let me verify: at x=128, 
    # correction term = -3.48*2304+33.5*48+2 = -8018+1608+2=-6408. y=56993-6408=50585. 
    # matches 50592! Good.
    # At x=100: -3.48*400+33.5*20+2=-1392+670+2=-720. y=34777-720=34057. matches 34058!
    # At x=120: -3.48*1600+33.5*40+2=-5568+1340+2=-4226. y=50089-4226=45863. matches 45868!
    # Excellent. But this is a hack. However it fits well. Let me use it.
    # Actually this correction is just a quadratic in (x-80), so overall for x>80 it's a cubic.
    # Fine.
    out = []
    for x in probe["x"]:
        ax = abs(x)
        if ax <= 5:
            out.append(-22.8021)
        else:
            y = 3.48 * x * x - 22.8021
            if ax > 80:
                d = ax - 80
                y += -3.48 * d * d + 33.5 * d + 2
            out.append(y)
    return {"y": out}
