
import numpy as np, math
N=113
KS=[8,11,22,23,25]
AMP=[12.53,6.17,0.29,9.80,6.67]
C0=-42.06
# per-head attention score direction: f_h(t)=F(t)@QH[h] (scores only enter via differences)
QH=[[0.336,0.044,0.025,0.062,0.001,0.008,1.834,-0.024,0.187,-0.161],
    [0.960,0.062,-0.022,-0.055,-0.014,0.012,-0.222,-0.048,-1.005,0.640],
    [-1.791,-0.133,-0.001,-0.025,0.023,0.007,-0.164,-0.003,0.022,0.005],
    [0.598,0.075,0.025,-0.022,-0.027,-0.020,-0.946,0.022,0.962,-0.657]]
QH=np.array(QH)
CL=np.arange(N)
TC=np.stack([np.cos(2*math.pi*k*CL/N) for k in KS],1)
TS=np.stack([np.sin(2*math.pi*k*CL/N) for k in KS],1)

def pairmat(C,S):
    return np.stack([C,S],axis=2).reshape(C.shape[0],-1)

def F(t):
    t=np.asarray(t,dtype=float); cols=[]
    for k in KS:
        a=2*math.pi*k*t/N
        cols.append(np.cos(a)); cols.append(np.sin(a))
    return np.stack(cols,axis=-1)

def model(x,iv):
    i=x[:,0].astype(int); j=x[:,1].astype(int)
    Fi=iv("emb0",F(i)); Fj=iv("emb1",F(j))
    # --- attention pattern of the last position over positions 0,1 (position 2 gets ~0)
    L0=Fi@QH.T; L1=Fj@QH.T
    E0=np.exp(L0-L0.max(1,keepdims=True)); E1=np.exp(L1-L0.max(1,keepdims=True))
    Z=np.maximum(E0+E1,1e-30)
    pat=iv("pat",np.hstack([E0/Z,E1/Z]))
    ci,si=Fi[:,0::2],Fi[:,1::2]; cj,sj=Fj[:,0::2],Fj[:,1::2]
    C=ci*cj-si*sj          # cos(k(i+j))
    S=ci*sj+si*cj          # sin(k(i+j))
    resid=iv("resid",pairmat(C,S))
    C=resid[:,0::2]; S=resid[:,1::2]
    return C0 + (C*AMP)@TC.T + (S*AMP)@TS.T

ALIGN={"emb0":["embed.0"],"emb1":["embed.1"],"pat":["attn_pattern"],"resid":["resid_post"]}
