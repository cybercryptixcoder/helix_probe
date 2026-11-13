
import numpy as np, math
N=113
KS=[8,11,22,23,25]
AMP=[12.53,6.17,0.29,9.80,6.67]
C0=-42.06
def F(t):
    t=np.asarray(t,dtype=float); cols=[]
    for k in KS:
        a=2*math.pi*k*t/N
        cols.append(np.cos(a)); cols.append(np.sin(a))
    return np.stack(cols,axis=-1)
CL=np.arange(N)
TC=np.stack([np.cos(2*math.pi*k*CL/N) for k in KS],1)
TS=np.stack([np.sin(2*math.pi*k*CL/N) for k in KS],1)

def model(x,iv):
    i=x[:,0].astype(int); j=x[:,1].astype(int)
    Fi=iv("emb0",F(i)); Fj=iv("emb1",F(j))
    ci,si=Fi[:,0::2],Fi[:,1::2]; cj,sj=Fj[:,0::2],Fj[:,1::2]
    C=ci*cj-si*sj
    S=ci*sj+si*cj
    resid=iv("resid",np.concatenate([C,S],1))
    C=resid[:,0::2]; S=resid[:,1::2]
    return C0 + (C*AMP)@TC.T + (S*AMP)@TS.T

ALIGN={"emb0":["embed.0"],"emb1":["embed.1"],"resid":["resid_post"]}
