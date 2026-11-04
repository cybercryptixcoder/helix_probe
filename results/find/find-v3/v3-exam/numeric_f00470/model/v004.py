import math

# Model of the black box.
#
# Beliefs (from the evidence):
# - For |x| >= 1, f(x) looks like a polynomial of degree ~7 with a small
#   correction.  The dominant behaviour is x^7-ish: e.g. f(88.2)~6.07e11,
#   88.2^7 ~ 4.2e13, so not pure x^7.  Actually check: 88.2^6 ~ 4.7e11,
#   close to 6.07e11.  f(123.6)~3.28e12; 123.6^6 ~ 3.5e12.  So ~x^6.
#   f(-127.7) ~ -1.16e12; 127.7^6 ~ 4.3e12, sign negative.  So odd-ish?
#   Let's fit: at x=2, f=3783.82.  2^11=2048, 2^12=4096.  x^11.6?
#   At x=1, f=70.35.  At x=10, f=11386930.  10^7=1e7, close.
#   Ratio f(10)/f(1)=161865.  10^5.2.  Hmm.
#   Try f(x)=x^7 + something? 1^7=1, need 70.  x^7 at 10 = 1e7 vs 1.14e7.
#   Let's use log: log10 f(10)=7.056, log10 f(2)=3.578.  Slope=(7.056-3.578)/(1-0.301)=4.97.
#   So ~x^5?  f(2)=3783, 2^5=32 no.  x^5*? 2^5=32, 3783/32=118.  10^5=1e5, 11386930/1e5=113.9.
#   So f(x) ~ 114 * x^5 for large x? Check x=88.2: 114*88.2^5 = 114*5.3e9=6.0e11.  Yes!
#   f(123.6): 114*123.6^5=114*2.88e10=3.28e12.  Yes!
#   f(-127.7): 114*(-127.7)^5 = -114*3.4e10 = -3.9e12.  But observed -1.16e12.
#   Hmm sign/magnitude off for negative large.  Check f(-124.4)=-1.02e12.
#   124.4^5=2.98e10, *114=3.4e12.  Observed -1.02e12, ratio -0.3.
#   So for negative large, coefficient ~ -34?  But f(-61.7)=-3.08e10.
#   61.7^5=8.9e8, *114=1.0e11, observed -3.08e10, ratio -0.3.
#   f(-20.3)=-1.2e8.  20.3^5=3.4e6, *114=3.9e8, ratio -0.3.
#   So for x<0 large, f ~ -34*x^5?  Check f(-1)=-36.09.  -34*(-1)^5=34, no.
#   Wait -34*x^5 at x=-1 = 34, but observed -36.  So sign: f(-1)=-36, x^5=-1, so -34*x^5=34.  Not matching.
#   Maybe f(x) = a*x^5 + b*x^4 + ... Let's use small values.
#   f(1)=70.35, f(-1)=-36.091.  f(2)=3783.82, f(-2)=-1500.006.
#   f(0)=21.28 (from E4, x=0 -> 21.28).
#   So there's a constant ~21.28?  But f(0.05)=15.4, f(-0.05)=22.6.
#   Hmm f(0)=21.28.  f(0.5)=-22.9553, f(-0.5)=25.692.
#   There's clearly a separate behaviour for |x|<1.
#
# Look at |x|<1 region (E4, E16):
#   x=0: 21.28
#   x=0.01:21.31, 0.02:20.34, 0.05:17.40, 0.1:10.45, 0.15:5.48, 0.2:3.54,
#   0.25:-3.29, 0.3:-8.92, 0.35:-13.25, 0.4:-15.14, 0.45:-20.44, 0.5:-21.96,
#   0.55:-23.45, 0.6:-22.65, 0.65:-21.23, 0.7:-19.83, 0.75:-12.03, 0.8:-5.33,
#   0.85:6.81, 0.9:22.99, 1.0:70.35 (jump!)
#   Negative side: -0.05:22.61, -0.1:22.85, -0.2:24.95, -0.3:27.38, -0.5:25.69,
#   -0.7:16.83, -0.9:-11.13, -1.0:-34.09 (jump!)
#   So |x|<1 is a smooth-ish function, and |x|>=1 is a different (polynomial) function.
#   Boundary at |x|=1.  At x=1 exactly: 70.35 (polynomial side).  At x=-1: -36.091.
#
# For |x|<1, fit a polynomial.  Values look like maybe a*sin or polynomial.
#   f(0)=21.28.  f(0.5)=-21.96.  f(-0.5)=25.69.
#   f(0.9)=22.99, f(-0.9)=-11.13.
#   Not symmetric.  Try cubic: f(x)=a+bx+cx^2+dx^3.
#   f(0)=a=21.28.
#   f(0.5)=21.28+0.5b+0.25c+0.125d=-21.96
#   f(-0.5)=21.28-0.5b+0.25c-0.125d=25.69
#   Sum: 42.56+0.5c=3.73 -> c=-77.66
#   Diff: b+0.25d=-47.65
#   f(0.9)=21.28+0.9b+0.81c+0.729d=22.99
#   f(-0.9)=21.28-0.9b+0.81c-0.729d=-11.13
#   Sum: 42.56+1.62c=11.86 -> c=-18.95.  Inconsistent with -77.66.
#   So not cubic.  Maybe higher degree or different form.
#
# Look at E16 more carefully.  The values 0.01..0.9:
# 21.31,20.34,17.40,10.45,5.48,3.54,-3.29,-8.92,-13.25,-15.14,-20.44,-21.96,
# -23.45,-22.65,-21.23,-19.83,-12.03,-5.33,6.81,22.99
# This looks like a polynomial of degree ~6-8.  Let's try fitting degree 7.
# Actually maybe it's a Taylor-like thing.  Let's just fit a polynomial to the
# |x|<1 data numerically (I'll hardcode coefficients from a least-squares fit
# done by reasoning).  Better: use the data points to interpolate.
#
# Given the difficulty, I'll fit a degree-8 polynomial to the |x|<1 points
# using the listed values, and a degree-5 polynomial for |x|>=1.
#
# For |x|>=1: f(x) ~ 114*x^5 for x>0, but negative side differs.
# Let's fit f(x)=a*x^5+b*x^4+c*x^3+d*x^2+e*x+g for x>=1 and x<=-1 separately?
# Actually check continuity: at x=1, poly gives 70.35, at x=-1 gives -36.09.
# For x>=1 use points: (1,70.35),(2,3783.82),(3,28401.19),(10,11386930.38)
# For x<=-1: (-1,-36.09),(-2,-1500.006),(-10,-3613824.11)
# Let's fit degree 5 through these.
#
# Positive: try f(x)=a*x^5+b*x^4+...  Using (1,70.35),(2,3783.82),(3,28401.19),
# (4,118360.4),(5,358940.83),(6,889937.3) -> 6 points, degree 5 fit.
# Let me just solve approximately.  Actually 114*x^5:
# 1:114 vs 70.35.  2:3648 vs 3783.82.  3:27702 vs 28401.19.  4:116736 vs 118360.4.
# 5:356250 vs 358940.83.  6:885,000 vs 889937.3.  10:1,140,000 vs 11,386,930??
# Wait 114*10^5=11,400,000 vs 11,386,930.  Close!
# So f(x) ~ 114*x^5 - small corrections.  Let's fit f(x)=a*x^5+b*x^4+c*x^3+d*x^2+e*x+g.
# Use x=1..6:
# 70.35 = a+b+c+d+e+g
# 3783.82 = 32a+16b+8c+4d+2e+g
# 28401.19 = 243a+81b+27c+9d+3e+g
# 118360.4 = 1024a+256b+64c+16d+4e+g
# 358940.83 = 3125a+625b+125c+25d+5e+g
# 889937.3 = 7776a+1296b+216c+36d+6e+g
# This is tedious.  Let me just use a simpler approximation: f(x)=114*x^5
# for x>0, and for x<0 something like -34*x^5? But at x=-1: -34 vs -36.09.
# At x=-2: -34*32=-1088 vs -1500.  At x=-10: -34*1e5=-3.4e6 vs -3.61e6.
# So maybe f(x) = -36*x^5 for x<0?  -36*(-1)^5=36, no, sign wrong.
# f(-1)=-36.09, so f(x) ~ -36*x^5? -36*(-1)=36 no.  f(x)~36*x^5? 36*(-1)^5=-36 yes!
# Check x=-2: 36*(-32)=-1152 vs -1500.  x=-10: 36*(-1e5)=-3.6e6 vs -3.61e6.  
# So for x<0, f(x) ~ 36*x^5 + corrections.  But at x=-1 it's -36.09, 36*(-1)=-36, close.
# And x=-2: 36*(-32)=-1152 vs -1500.  Off by 348.
# Let's fit f(x)=a*x^5+b*x^4+... for x<0 using (-1,-36.09),(-2,-1500.006),
# (-3,-10244.411),(-4,-40769.54),(-5,-120305.515),(-6,-292916.946).
# Try f(x)=a*x^5+b*x^4+c*x^3+d*x^2+e*x+g.
# At x=-1: -a+b-c+d-e+g=-36.09
# x=-2: -32a+16b-8c+4d-2e+g=-1500.006
# x=-3: -243a+81b-27c+9d-3e+g=-10244.411
# x=-4: -1024a+256b-64c+16d-4e+g=-40769.54
# x=-5: -3125a+625b-125c+25d-5e+g=-120305.515
# x=-6: -7776a+1296b-216c+36d-6e+g=-292916.946
# 
# This is getting complex.  Let me just use a degree-5 polynomial fit
# for each side, computed via numpy-like least squares in pure Python.
# I'll implement a small least-squares solver.

def _solve(A, b):
    n = len(A)
    # Gaussian elimination
    M = [row[:] + [b[i]] for i, row in enumerate(A)]
    for i in range(n):
        # pivot
        p = max(range(i, n), key=lambda r: abs(M[r][i]))
        M[i], M[p] = M[p], M[i]
        if abs(M[i][i]) < 1e-15:
            continue
        for j in range(i+1, n):
            f = M[j][i] / M[i][i]
            for k in range(i, n+1):
                M[j][k] -= f * M[i][k]
    x = [0.0]*n
    for i in range(n-1, -1, -1):
        if abs(M[i][i]) < 1e-15:
            x[i] = 0.0
        else:
            s = M[i][n] - sum(M[i][j]*x[j] for j in range(i+1, n))
            x[i] = s / M[i][i]
    return x

def _polyfit(xs, ys, deg):
    # normal equations
    n = deg+1
    A = [[0.0]*n for _ in range(n)]
    b = [0.0]*n
    for x, y in zip(xs, ys):
        pw = [x**k for k in range(2*deg+1)]
        for i in range(n):
            for j in range(n):
                A[i][j] += pw[i+j]
            b[i] += y * pw[i]
    return _solve(A, b)

# Positive side data (x>=1)
_pos_x = [1,2,3,4,5,6,7,8,9,10,1.2,1.5,2.0,2.5,2.8,3.0,3.1,3.3,3.5,3.7,3.9,4.1,
          10.3,12.1,12.5,13.1,17.3,19.4,21.3,22.4,24.6,26.4,28.4,28.9,30.3,40.1,
          43.0,47.1,52.9,56.2,58.8,65.5,65.9,66.0,72.7,77.6,78.1,79.4,80.5,83.2,
          87.7,88.2,93.5,94.1,94.8,96.5,102.1,103.0,104.5,104.9,105.7,108.4,
          110.8,118.7,119.5,119.7,123.6]
_pos_y = [70.35,3783.82,28401.19,118360.4,358940.83,889937.3,1919315.07,3736882.84,
          6727933.75,11386930.38,250.2048,867.6703,3781.82,11497.8909,20172.8524,
          28400.19,33413.6883,45561.0745,61000.1766,80369.5403,104375.9999,133805.0504,
          13198713.3758,29513262.9141,34721833.0222,43889573.978,176229729.6113,
          312490967.9542,498566508.849,641308203.863,1024496795.3112,1458359792.3997,
          2101113919.5752,2292717244.6795,2904585078.6999,11793950848.2219,
          16722350981.39,26368322845.8484,47128651772.5135,63782684300.9124,
          79968419071.7272,137171213311.5103,141411556636.4628,142487853201.7,
          231073987061.1789,320185034785.4573,330635046246.848,359086872056.3639,
          384661872849.6947,453651975664.6768,590356206626.6161,607379528140.0764,
          813178521389.0581,839609028625.2251,871308562751.5093,952291661775.3049,
          1262617391788.233,1319260760409.1902,1418170236771.25,1445522923769.7898,
          1501494419594.9934,1703331882405.2927,1900444299491.0227,
          2681763702599.6597,2773367622816.3594,2796655133978.159,3282957176456.9175]

# Negative side data (x<=-1)
_neg_x = [-1,-2,-3,-4,-5,-6,-7,-8,-9,-10,-1.1,-1.2,-1.3,-1.4,-1.5,-1.6,-1.7,-1.8,
          -2.0,-2.2,-2.4,-2.5,-2.6,-2.8,-5.9,-6.0,-7.1,-13.3,-14.1,-16.9,-20.3,
          -24.3,-25.9,-29.5,-44.7,-46.1,-48.6,-50.4,-53.7,-55.8,-61.3,-61.7,
          -63.9,-65.6,-66.9,-79.1,-79.5,-80.2,-100.1,-102.2,-105.0,-107.4,
          -124.4,-127.7]
_neg_y = [-36.091,-1500.006,-10244.411,-40769.54,-120305.515,-292916.946,-623586.531,
          -1202334.656,-2148292.995,-3613824.11,-72.3889,-120.8396,-185.7543,
          -268.9791,-379.9367,-520.6669,-692.8676,-910.9359,-1501.006,-2352.5956,
          -3551.2331,-4307.8339,-5186.5686,-7374.6852,-269797.0953,-292914.946,
          -668574.7708,-14820223.2427,-19797760.6873,-48642903.8844,-120955209.4828,
          -295937989.9227,-406493074.495,-777194648.449,-6168934504.6733,
          -7194763286.8135,-9363315532.1889,-11226066722.555,-15404906078.8869,
          -18654932509.0998,-29822715764.8351,-30806744759.1345,-36693855455.0953,
          -41832435306.8571,-46137611291.7709,-106479847886.1458,-109195762376.7459,
          -114081791381.375,-345093420021.0963,-382800917414.258,-438131264260.915,
          -490489401620.7499,-1021913847133.604,-1164712174639.8828]

# Fit degree 5 polynomials
_pos_coef = _polyfit(_pos_x, _pos_y, 5)
_neg_coef = _polyfit(_neg_x, _neg_y, 5)

# For |x|<1, fit degree 8
_in_x = [0.0,0.01,0.02,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,
         0.65,0.7,0.75,0.8,0.85,0.9,-0.05,-0.1,-0.2,-0.3,-0.5,-0.7,-0.9]
_in_y = [21.28,21.3118,20.3392,17.3992,10.4473,5.4751,3.5408,-3.2851,-8.9163,
         -13.2456,-15.1413,-20.4426,-21.9553,-23.4478,-22.6466,-21.232,-19.834,
         -12.0279,-5.3302,6.806,22.9947,22.6125,22.8483,24.9533,27.3822,25.692,
         16.8289,-11.1291]
_in_coef = _polyfit(_in_x, _in_y, 8)

def _eval(coef, x):
    s = 0.0
    for c in reversed(coef):
        s = s*x + c
    return s

def predict(probe):
    xs = probe["x"]
    ys = []
    for x in xs:
        if x is None:
            ys.append(None)
            continue
        try:
            x = float(x)
        except Exception:
            ys.append(None)
            continue
        if math.isnan(x) or math.isinf(x):
            ys.append(None)
            continue
        if -1.0 < x < 1.0:
            y = _eval(_in_coef, x)
        elif x >= 1.0:
            y = _eval(_pos_coef, x)
        else:
            y = _eval(_neg_coef, x)
        ys.append(y)
    return {"y": ys}
