
import numpy as np, math
N=113
KS=[8,11,22,23,25]
AMP=[12.53,6.17,0.29,9.80,6.67]
C0=-42.06
QH=np.array([[0.336,0.044,0.025,0.062,0.001,0.008,1.834,-0.024,0.187,-0.161],
             [0.960,0.062,-0.022,-0.055,-0.014,0.012,-0.222,-0.048,-1.005,0.640],
             [-1.791,-0.133,-0.001,-0.025,0.023,0.007,-0.164,-0.003,0.022,0.005],
             [0.598,0.075,0.025,-0.022,-0.027,-0.020,-0.946,0.022,0.962,-0.657]])
CL=np.arange(N)
TC=np.stack([np.cos(2*math.pi*k*CL/N) for k in KS],1)
TS=np.stack([np.sin(2*math.pi*k*CL/N) for k in KS],1)

def F(t):
    t=np.asarray(t,dtype=float); cols=[]
    for k in KS:
        a=2*math.pi*k*t/N
        cols.append(np.cos(a)); cols.append(np.sin(a))
    return np.stack(cols,axis=-1)

def model(x,iv):
    i=x[:,0].astype(int); j=x[:,1].astype(int)
    Fi=iv("emb0",F(i)); Fj=iv("emb1",F(j))
    L0=Fi@QH.T; L1=Fj@QH.T
    m=np.maximum(L0,L1).max(1,keepdims=True)
    E0=np.exp(L0-m); E1=np.exp(L1-m); Z=E0+E1
    pat=np.hstack([E0/Z,E1/Z])
    ci,si=Fi[:,0::2],Fi[:,1::2]; cj,sj=Fj[:,0::2],Fj[:,1::2]
    C=ci*cj-si*sj; S=ci*sj+si*cj; D=ci*cj+si*sj
    mid=iv("mid",np.hstack([pat,Fi,Fj,C,S,D]))
    Fi=mid[:,8:18]; Fj=mid[:,18:28]
    ci,si=Fi[:,0::2],Fi[:,1::2]; cj,sj=Fj[:,0::2],Fj[:,1::2]
    C=ci*cj-si*sj; S=ci*sj+si*cj
    mlp=iv("mlp",np.stack([C,S],axis=2).reshape(C.shape[0],-1))
    resid=iv("resid",mlp)
    C=resid[:,0::2]; S=resid[:,1::2]
    return C0 + (C*AMP)@TC.T + (S*AMP)@TS.T

ALIGN={"emb0":["embed.0"],"emb1":["embed.1"],"mid":["resid_mid","mlp_pre"],
       "mlp":["mlp_post","mlp_out"],"resid":["resid_post"]}
