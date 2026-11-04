import math

# Fit from E1 data (approximate). We model f(x) = sign(x) * A * |x|^p * exp(k*|x|)
# Using points to estimate: at x=128, |y|=2.1689e12; at x=64, |y|=3.3446e10; at x=16, 7.656e6; at x=8, 1.151e5
# ratio 128/64: 2.1689e12/3.3446e10 = 64.85 = 2^p * exp(64k)
# ratio 64/16: 3.3446e10/7.656e6 = 4368 = 4^p * exp(48k)
# ratio 16/8: 7.656e6/1.151e5 = 66.5 = 2^p * exp(8k)
# From 16/8: 2^p * exp(8k) = 66.5
# From 128/64: 2^p * exp(64k) = 64.85
# Divide: exp(56k) = 64.85/66.5 = 0.9752 -> k = ln(0.9752)/56 = -0.000448
# Then 2^p = 66.5 / exp(8*(-0.000448)) = 66.5/0.99642 = 66.74 -> p = log2(66.74) = 6.06
# Check 64/16: 4^6.06 * exp(48*(-0.000448)) = 4096*... 4^6.06 = 2^12.12=4460, exp(-0.0215)=0.979 -> 4366. Close to 4368. Good.
# So f(x) ~ sign(x) * A * |x|^6.06 * exp(-0.000448*|x|)
# Estimate A from x=8: 1.151e5 = A * 8^6.06 * exp(-0.00358) -> 8^6.06 = 2^18.18 = 296000 -> A = 1.151e5/296000/0.9964 = 0.390
# Check x=1: 0.390*1*exp(-0.000448)=0.39, but observed 4.3. Not great at small x.
# Small x behavior: y(1)=-4.3, y(2)=-60.2, y(4)=-2004.4, y(8)=-115148
# ratio 2/1: 14.0; 4/2: 33.3; 8/4: 57.4. Growing ratio -> not pure power.

# Let's try f(x) = sign(x)*A*|x|^p*exp(k*|x|) fit more carefully using log-log.
# ln|y| at x=1: ln4.3=1.459; x=2: ln60.2=4.098; x=4: ln2004.4=7.603; x=8: ln115148=11.654; x=16: ln7.656e6=15.851; x=32: ln5.702e8=20.161; x=64: ln3.3446e10=24.233; x=128: ln2.1689e12=28.305
# Differences per doubling: 2.639, 3.505, 4.051, 4.197, 4.310, 4.072, 4.072
# These approach ~4.07 per doubling -> p*ln2 + k*|x|... at large x slope in ln|y| vs ln|x| ~ 4.07/ln2 = 5.87
# So p ~ 5.87 at large x, with small k.
# Actually differences are nearly constant ~4.07 for x>=16, so pure power p=4.07/ln2=5.87 there.
# At small x differences smaller (2.6 at x=1->2), so there's a sub-power term or additive constant.

# Try f(x) = sign(x)*(a*|x|^6 + b*|x|^2) or similar. Let's just fit a polynomial-ish.
# Use x=1: a+b=4.3; x=2: 64a+4b=60.2 -> 64a+4(4.3-a)=60.2 -> 60a+17.2=60.2 -> a=0.7167, b=3.583
# Check x=4: 0.7167*4096+3.583*16=2935+57=2992 vs 2004. Too big.
# Try f=sign(x)*(a*|x|^5+b*|x|^2): x=1: a+b=4.3; x=2:32a+4b=60.2 -> 32a+4(4.3-a)=60.2 ->28a=43 ->a=1.536,b=2.764
# x=4: 1.536*1024+2.764*16=1573+44=1617 vs 2004. Closer.
# Try a*|x|^5.5: x=1:a+b=4.3; x=2: 2^5.5*a+4b=45.25a+4b=60.2 -> 45.25a+4(4.3-a)=60.2 ->41.25a=43 ->a=1.042,b=3.258
# x=4: 4^5.5=2048, *1.042=2134+52=2186 vs 2004. 
# Try a*|x|^5.3: 2^5.3=39.4; 39.4a+4(4.3-a)=60.2 ->35.4a=43 ->a=1.215,b=3.085
# x=4: 4^5.3=2^10.6=1552*1.215=1886+49=1935 vs 2004. Good-ish.
# x=8: 8^5.3=2^15.9=61300*1.215=74480+197=74677 vs 115148. Off by factor 1.5.
# Hmm, need steeper at large x. Add exponential.

# Let's do a proper least squares on ln|y| = ln A + p ln|x| + k|x| using points x>=2.
# Points (ln x, ln|y|): (0.693,4.098),(1.386,7.603),(2.079,11.654),(2.773,15.851),(3.466,20.161),(4.159,24.233),(4.852,28.305)
# Linear fit in (ln x, |x|): solve for lnA, p, k.
# This is a 3-param linear regression. Let me just do it numerically in code with a simple approach.

# Given complexity, I'll implement a fit computed at import time using the E1 data.
data = [
    (-128,-2230774482035.2),(-112,-1003257061016.0),(-96,-398978558294.4),
    (-80,-134146940488.0),(-64,-35377519980.8),(-48,-6360821035.2),
    (-32,-570243664.0),(-16,-9525262.4),(-8,-171815.2),(-4,-3534.8),
    (-2,-67.0),(-1,6.1),(0,0.0),(1,-4.3),(2,-60.2),(4,-2004.4),
    (8,-115148.0),(16,-7655972.8),(64,-33445938630.4),(128,-2168936181440.0)
]

# Fit ln|y| = lnA + p*ln|x| + k*|x| for |x|>=2 using normal equations
import math
pts = [(math.log(abs(x)), abs(x), math.log(abs(y))) for x,y in data if abs(x)>=2 and y!=0]
# design: [1, ln|x|, |x|]
n=len(pts)
S=[0.0]*3
M=[[0.0]*3 for _ in range(3)]
T=[0.0]*3
for lx,ax,ly in pts:
    row=[1.0,lx,ax]
    for i in range(3):
        T[i]+=row[i]*ly
        for j in range(3):
            M[i][j]+=row[i]*row[j]
# solve 3x3
def solve3(M,T):
    import copy
    A=[row[:]+[T[i]] for i,row in enumerate(M)]
    for c in range(3):
        piv=max(range(c,3),key=lambda r:abs(A[r][c]))
        A[c],A[piv]=A[piv],A[c]
        if abs(A[c][c])<1e-12: return [0,0,0]
        for r in range(3):
            if r!=c:
                f=A[r][c]/A[c][c]
                for k in range(c,4): A[r][k]-=f*A[c][k]
    return [A[i][3]/A[i][i] for i in range(3)]
coef=solve3(M,T)
lnA,p,k=coef
A=math.exp(lnA)

def predict(probe):
    xs = probe.get("x", [])
    out=[]
    for x in xs:
        try:
            if x==0:
                out.append(0.0)
            else:
                ax=abs(x)
                val=A*(ax**p)*math.exp(k*ax)
                out.append(math.copysign(val,x))
        except Exception:
            out.append(None)
    return {"y":out}
