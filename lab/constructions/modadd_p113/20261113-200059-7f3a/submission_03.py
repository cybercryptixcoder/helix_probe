import numpy as np
DESCRIPTION = """Adds two tokens mod 113. Token embeddings are sums of sin/cos at Fourier frequencies
8,11,22,23,25. Attention at the last position (query is the fixed token 113, so weights depend only on the two
tokens) writes the 5-frequency features of token i and token j into the residual stream. The MLP combines them into
the 5-frequency features of the sum s=(i+j) mod 113, and the logits are cos(2pi f (s-c)/113)."""
P = 113.0
FREQ = [8, 11, 22, 23, 25]
def feats(k):
    k = np.asarray(k, float)
    return np.stack([f_(2*np.pi*f*k/P) for f in FREQ for f_ in (np.cos, np.sin)], 1)
def model(x, iv):
    i = x[:, 0].astype(float); j = x[:, 1].astype(float)
    Fi = iv("vi", feats(i))
    Fj = iv("vj", feats(j))
    # angle addition on the iv-returned values
    ci = Fi[:, 0::2]; si = Fi[:, 1::2]; cj = Fj[:, 0::2]; sj = Fj[:, 1::2]
    cs = ci*cj - si*sj; ss = si*cj + ci*sj
    ms = iv("ms", np.stack([v for t in zip(cs.T, ss.T) for v in t], 1))
    c = np.arange(113.0)
    logits = np.zeros((len(i), 113))
    for n, f in enumerate(FREQ):
        logits += cs[:, [n]]*np.cos(2*np.pi*f*c/P)[None, :] + ss[:, [n]]*np.sin(2*np.pi*f*c/P)[None, :]
    return logits
ALIGN = {"vi": ["embed.0", "attn_out", "resid_mid"], "vj": ["embed.1", "attn_out", "resid_mid"],
         "ms": ["mlp_post", "mlp_out", "resid_post"]}
