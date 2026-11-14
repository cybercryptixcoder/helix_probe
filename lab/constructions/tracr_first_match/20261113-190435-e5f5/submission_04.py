
import numpy as np

DESCRIPTION = (
 "Input is [BOS=0, t1..t5] with t_i in {1,2,3,5}; the readout at positions 1..5 asks whether t_p == t1. "
 "Mechanism: (1) embeddings are token one-hots per position. (2) Layer-0 attention has a FIXED pattern: "
 "query 0 attends to key 0, queries 1..5 attend to key 1 only, so the attention output at positions 1..5 is "
 "the value of token t1 alone (a zero vector for tokens 0 and 4). So the residual at position p>=1 encodes "
 "the pair (t_p, t1). (3) The 16 MLP neurons are coincidence detectors: neuron n has a token pair (a_n,b_n) "
 "and gain m_n with pre_n = m_n*([t_p==a_n] + v1[b_n] - 1), i.e. it fires with size m_n only when t_p==a_n "
 "AND t1==b_n. The 16 pairs are exactly all 4x4 combinations of {1,2,3,5}. (4) The output weights give "
 "neuron n effective weight u_n with m_n*u_n = +1 for the 4 diagonal (matching) pairs and -1 for the 12 "
 "off-diagonal pairs, while the direct residual->logit path is exactly orthogonal to the readout direction. "
 "Hence logit(class1)-logit(class0) at position p = +1 if t_p==t1 else -1, and logit(class0)=0: the "
 "network outputs (0, +-1).")

# (a_n, b_n, m_n) for the 16 coincidence neurons; u_n = effective output weight of neuron n.
NEU = [(5, 1, 1.3474), (5, 3, 1.3545), (2, 2, 1.2269), (5, 5, 1.1687),
       (5, 2, 0.5506), (3, 2, 0.7012), (1, 5, 1.1097), (1, 2, 0.8623),
       (3, 1, 1.9914), (2, 1, 1.8098), (1, 1, 0.6144), (1, 3, 1.1342),
       (2, 5, 1.3161), (2, 3, 0.6012), (3, 3, 0.7692), (3, 5, 1.3529)]
U = np.array([-0.7422, -0.7383, 0.8151, 0.8557, -1.8163, -1.4262, -0.9011, -1.1597,
              -0.5022, -0.5525, 1.6277, -0.8817, -0.7598, -1.6634, 1.3000, -0.7391])
M = np.array([n[2] for n in NEU])

def model(x, iv):
    B = x.shape[0]
    ar = np.arange(B)
    tok = []
    for p in range(6):
        v = np.zeros((B, 6))
        v[ar, x[:, p]] = 1.0
        tok.append(iv("tok%d" % p, v))
    v1 = iv("v1", tok[1])                     # content written by attention at positions 1..5
    out = np.zeros((B, 10))
    for p in range(1, 6):
        q = tok[p]                            # one-hot of t_p
        args = []
        for (a, b, m) in NEU:
            args.append(q[:, a] + v1[:, b] - 1.0)   # +1 only when t_p==a and t1==b
        act = iv("mlp%d" % p, np.maximum(np.array(args).T * M, 0.0))
        d = act @ U                           # = +1 if t_p == t1 else -1
        out[:, 2 * (p - 1) + 1] = d
    return out

ALIGN = {"tok0": ["embed"],
         "tok1": ["embed", "resid0.mid", "mlp0.pre"],
         "tok2": ["embed", "resid0.mid", "mlp0.pre"],
         "tok3": ["embed", "resid0.mid", "mlp0.pre"],
         "tok4": ["embed", "resid0.mid", "mlp0.pre"],
         "tok5": ["embed", "resid0.mid", "mlp0.pre"],
         "v1": ["attn0.out", "resid0.mid", "mlp0.pre"],
         "mlp1": ["mlp0.out", "mlp0.post"], "mlp2": ["mlp0.out", "mlp0.post"],
         "mlp3": ["mlp0.out", "mlp0.post"], "mlp4": ["mlp0.out", "mlp0.post"],
         "mlp5": ["mlp0.out", "mlp0.post"]}
