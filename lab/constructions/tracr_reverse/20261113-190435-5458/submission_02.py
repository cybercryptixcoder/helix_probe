
import numpy as np

DESCRIPTION = (
    "The network reverses the sequence: output block i (position i+1) is the one-hot class of the token at "
    "input position 4-i (i=0..3). All input dependence lives in the embedding (token+position); layers 0,1,2 "
    "attention patterns and every MLP (layers 0,1,2,3) and layer-1/2 attention outputs are input-independent "
    "constants (attn1.out = attn2.out = 0). Their stages only add fixed vectors to the residual stream, so "
    "every residual site before layer 3 equals (embedding of its own position's token) + a per-position constant. "
    "Layer 3 attention uses a fixed permutation pattern, query position p attends to key position 4-p, so it "
    "copies the token code of the token at 4-p into position p; nothing else is added. The output head W_U is "
    "affine in the 3-dim one-hot token code: logit_c = code_c - 0.25*sum(code) + 0.25, i.e. 1 for the correct "
    "class and 0 for the others, which is the whole output. "
    "Variables are one per position: tok_q (q=1..4) = 3-dim one-hot code of the token at input position q, "
    "present in the embedding and all residual sites up to layer 3; need_i = the same code for the token that "
    "output block i must report, i.e. tok_{4-i}, at the layer-3 sites."
)

M = np.array([[0.75, -0.25, -0.25],
              [-0.25, 0.75, -0.25],
              [-0.25, -0.25, 0.75]])
C = 0.25

def model(x, iv):
    B = x.shape[0]
    tok = []
    for q in range(1, 5):
        oh = np.zeros((B, 3))
        oh[np.arange(B), x[:, q] - 1] = 1.0
        tok.append(iv("tok%d" % q, oh))
    need = []
    for i in range(4):
        need.append(iv("need%d" % i, tok[3 - i]))
    out = np.zeros((B, 12))
    for i in range(4):
        out[:, 3 * i:3 * i + 3] = need[i] @ M + C
    return out

ALIGN = {
    "tok1": ["embed", "resid0.mid", "resid0.post", "resid1.mid", "resid1.post", "resid2.mid", "resid2.post"],
    "tok2": ["embed", "resid0.mid", "resid0.post", "resid1.mid", "resid1.post", "resid2.mid", "resid2.post"],
    "tok3": ["embed", "resid0.mid", "resid0.post", "resid1.mid", "resid1.post", "resid2.mid", "resid2.post"],
    "tok4": ["embed", "resid0.mid", "resid0.post", "resid1.mid", "resid1.post", "resid2.mid", "resid2.post"],
    "need0": ["attn3.out", "resid3.mid", "resid3.post"],
    "need1": ["attn3.out", "resid3.mid", "resid3.post"],
    "need2": ["attn3.out", "resid3.mid", "resid3.post"],
    "need3": ["attn3.out", "resid3.mid", "resid3.post"],
}
