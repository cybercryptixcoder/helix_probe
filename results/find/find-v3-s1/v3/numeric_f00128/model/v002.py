import math

def predict(probe):
    # f is smooth, monotonic decreasing, roughly odd-ish but with a vertical offset.
    # E2 shows: f(0)=5.42 (not 0), f is decreasing everywhere.
    # Local slope near 0: (f(2)-f(-2))/4 = (-22.68-15.91)/4 = -9.65
    # Slope grows with |x|: near 128, (f(-128)-f(-115))/13 = (867.68-779.80)/13 = 6.76 per unit -> slope ~ -6.76? 
    # Actually f(-128)-f(-115) = 87.88 over 13 -> slope -6.76 (increasing x gives decreasing y).
    # Near 100-115: (779.80-678.40)/15 = 6.76. Near 80-100: (678.40-543.20)/20=6.76.
    # Near 50-80: (543.20-340.40)/30=6.76. Near 25-50: (340.40-171.40)/25=6.76.
    # Near 10-25: (171.40-69.99)/15=6.76. Near 5-10: (69.99-36.19)/5=6.76.
    # Near 2-5: (36.19-15.91)/3=6.76. Near 0-2: (15.91-5.42)/2=5.25.
    # Wow: slope is constant -6.76 for |x|>=2! And near 0 slope ~ -5.25.
    # Check -2 to 0: (5.42-15.91)/2 = -5.25. 0 to 2: (-22.68-5.42)/2=-14.05. Hmm asymmetric.
    # Let's recheck: f(-2)=15.91, f(0)=5.42, f(2)=-22.68.
    # (-2,0): slope (5.42-15.91)/2 = -5.245
    # (0,2): slope (-22.68-5.42)/2 = -14.05
    # (2,5): (-73.29-(-22.68))/3 = -16.87
    # (5,10): (-157.81-(-73.29))/5 = -16.90
    # (10,25): (-411.30-(-157.81))/15 = -16.90
    # (25,50): (-833.80-(-411.30))/25 = -16.90
    # (50,80): (-1340.80-(-833.80))/30 = -16.90
    # (80,100): (-1678.80-(-1340.80))/20 = -16.90
    # (100,115): (-1932.29-(-1678.80))/15 = -16.90
    # (115,128): (-2151.99-(-1932.29))/13 = -16.90
    # So for x>=2, slope is constant -16.90! Linear!
    # Negative side: (-5,-2): (15.91-36.19)/3 = -6.76
    # (-10,-5): (36.19-69.99)/5 = -6.76
    # (-25,-10): (69.99-171.40)/15 = -6.76
    # (-50,-25): (171.40-340.40)/25 = -6.76
    # (-80,-50): (340.40-543.20)/30 = -6.76
    # (-100,-80): (543.20-678.40)/20 = -6.76
    # (-115,-100): (678.40-779.80)/15 = -6.76
    # (-128,-115): (779.80-867.68)/13 = -6.76
    # So for x<=-2, slope is constant -6.76! Linear!
    # Between -2 and 2, transition.
    # So f is piecewise linear: slope -6.76 for x<=-2, slope -16.90 for x>=2, transition in between.
    # Check E1: x=-93.6 -> f = 867.68 + (-6.76)*(-93.6-(-128)) = 867.68 + (-6.76)*(34.4) = 867.68-232.5=635.2 ✓
    # x=88.9 -> f = -2151.99 + (-16.90)*(88.9-128) = -2151.99 + (-16.90)*(-39.1) = -2151.99+660.8=-1491.2 ✓
    # x=67.5 -> -2151.99 + (-16.90)*(67.5-128) = -2151.99 + 1022.45 = -1129.5 ✓
    # x=-62.7 -> 867.68 + (-6.76)*(-62.7+128) = 867.68 - 441.4 = 426.3 ✓
    # x=-1.2: in transition. f(-2)=15.91, f(0)=5.42. Linear interp: 15.91 + (5.42-15.91)/2*(0.8) = 15.91-4.196=11.71. Observed 10.58. Close-ish.
    # x=-12.9 -> 867.68 + (-6.76)*(-12.9+128) = 867.68 - 778.1 = 89.6 ✓
    # x=38.8 -> -2151.99 + (-16.90)*(38.8-128) = -2151.99 + 1507.7 = -644.3 ✓
    # x=73.9 -> -2151.99 + (-16.90)*(73.9-128) = -2151.99 + 914.2 = -1237.8 ✓
    # x=-104 -> 867.68 + (-6.76)*(-104+128) = 867.68 - 162.2 = 705.5 ✓
    # x=-120.7 -> 867.68 + (-6.76)*(-120.7+128) = 867.68 - 49.3 = 818.4 ✓
    # Great. Now the transition region [-2,2].
    # f(-2)=15.9142, f(0)=5.4186, f(2)=-22.6804.
    # Slope left of -2 is -6.76, right of 2 is -16.90.
    # At x=-2, left slope -6.76. At x=2, right slope -16.90.
    # Maybe a smooth blend. Let's fit a quadratic through (-2,15.9142),(0,5.4186),(2,-22.6804)?
    # Actually let's just use piecewise linear with a kink at -2 and 2, or fit quadratic.
    # Quadratic: y = a x^2 + b x + c
    # c = 5.4186
    # 4a - 2b + c = 15.9142 -> 4a - 2b = 10.4956
    # 4a + 2b + c = -22.6804 -> 4a + 2b = -28.099
    # 8a = -17.6034 -> a = -2.2004
    # 4b = -28.099 - 4a = -28.099 + 8.8017 = -19.297 -> b = -4.824
    # Check slope at -2: 2a*(-2)+b = 8.8017 - 4.824 = 3.978. But left slope should be -6.76. Doesn't match.
    # So it's not a simple quadratic. Let's just use linear interpolation between the three points:
    # x in [-2,0]: y = 15.9142 + (5.4186-15.9142)/2*(x+2) = 15.9142 - 5.2478*(x+2)
    # x in [0,2]: y = 5.4186 + (-22.6804-5.4186)/2*x = 5.4186 - 14.0495*x
    # Check x=-1.2: 15.9142 - 5.2478*0.8 = 15.9142-4.198=11.716. Observed 10.58. Off by 1.1.
    # Hmm. Maybe smoother. Let's try cubic Hermite with slopes -6.76 at -2 and -16.90 at 2.
    # Actually let's just fit a cubic through the 3 points with derivative constraints? Overkill.
    # Let's just use the piecewise linear interpolation; error ~1 on a value of ~10 is acceptable.
    # Actually, let's try a smooth blend: maybe f(x) = A + B*x + C*tanh-like? 
    # Simpler: use piecewise linear with the three known points. Good enough.
    # Constants:
    # Left line: through (-128, 867.6846) slope -6.76 -> but let's compute exactly.
    # slope_left = (867.6846-779.8035)/(-128-(-115)) = 87.8811/(-13) = -6.7601
    # slope_right = (-2151.9921-(-1932.2937))/(128-115) = -219.6984/13 = -16.8999
    # Left line: y = 867.6846 + (-6.7601)*(x+128)
    # Right line: y = -2151.9921 + (-16.8999)*(x-128)
    # Transition: piecewise linear through (-2,15.9142),(0,5.4186),(2,-22.6804)
    def f(x):
        if x <= -2:
            return 867.6846 + (-6.7601)*(x+128)
        elif x <= 0:
            return 15.9142 + (5.4186-15.9142)/2.0*(x+2)
        elif x <= 2:
            return 5.4186 + (-22.6804-5.4186)/2.0*x
        else:
            return -2151.9921 + (-16.8999)*(x-128)
    return {"y": [f(x) for x in probe["x"]]}
