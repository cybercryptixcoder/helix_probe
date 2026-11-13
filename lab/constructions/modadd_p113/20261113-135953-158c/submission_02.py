
import numpy as np, math
N=113
KS=[8,11,22,23,25]

def feat(t):
    t=np.asarray(t,dtype=float)
    cols=[]
    for k in KS:
        a=2*math.pi*k*t/N
        cols.append(np.cos(a)); cols.append(np.sin(a))
    return np.stack(cols,axis=-1)

TABLE=feat(np.arange(N))   # (113,10)

def decode(F):             # (B,10) -> best token index (B,)
    d=((F[:,None,:]-TABLE[None,:,:])**2).sum(-1)
    return d.argmin(1)

def model(x,iv):
    i=x[:,0].astype(int); j=x[:,1].astype(int)
    e0=iv("emb0",feat(i)); e1=iv("emb1",feat(j))
    ci=decode(e0); cj=decode(e1)
    s=(ci+cj)%N
    resid=iv("resid",feat(s))
    cls=np.arange(N)
    logits=np.cos(2*math.pi*(cls[None,:]-s[:,None])/N)
    return logits

ALIGN={"emb0":["embed.0"],"emb1":["embed.1"],"resid":["resid_post"]}
