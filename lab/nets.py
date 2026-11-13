"""Numpy forward passes and weight variants for the lab's target networks.

Imported by the server (for checks and variants) and by the sandbox (so a reader that is allowed forward
passes can call run(x)). Numpy only: no torch at runtime.
"""
import numpy as np


def mlp(W, x, act):
    """MLP with tensors W1,b1,W2,b2,... (W_k shaped in x out). act applies to every layer except the last."""
    f = {"tanh": np.tanh, "relu": lambda z: np.maximum(z, 0)}[act]
    h = np.asarray(x, dtype=np.float64)
    k = 1
    while f"W{k}" in W:
        h = h @ W[f"W{k}"] + W[f"b{k}"]
        if f"W{k + 1}" in W:
            h = f(h)
        k += 1
    return h


def onelayer_transformer(W, tokens):
    """The Nanda-style 1-layer transformer (no LayerNorm, no biases). tokens: [B, 3] ints -> logits [B, n_out]."""
    t = np.asarray(tokens)
    if t.ndim == 1:
        t = t[None]
    x = W["W_E"][t] + W["W_pos"]                                   # [B, 3, d]
    q = np.einsum("bpd,hde->bhpe", x, W["W_Q"])
    k = np.einsum("bpd,hde->bhpe", x, W["W_K"])
    v = np.einsum("bpd,hde->bhpe", x, W["W_V"])
    att = np.einsum("bhpe,bhqe->bhpq", q, k) / np.sqrt(W["W_Q"].shape[-1])
    n = t.shape[1]
    att = np.where(np.triu(np.ones((n, n), bool), 1), -1e9, att)
    att = np.exp(att - att.max(-1, keepdims=True)); att /= att.sum(-1, keepdims=True)
    z = np.einsum("bhpq,bhqe->bhpe", att, v)
    x = x + np.einsum("bhpe,hed->bpd", z, W["W_O"])
    x = x + np.maximum(x @ W["W_in"], 0) @ W["W_out"]
    return x[:, -1] @ W["W_U"]


def forward(kind, W, x):
    if kind in ("mlp_tanh", "mlp_relu"):
        return mlp(W, x, kind.split("_")[1])
    if kind == "onelayer_transformer":
        return onelayer_transformer(W, x)
    raise ValueError(f"no forward pass for {kind}")


# ---------- variants (controls) ----------

def variant(W, name, perm_groups=(), seed=0):
    """Return a modified copy of the weight dict.
    original: unchanged.
    shuffled: values shuffled within each tensor (keeps each tensor's statistics, destroys structure).
    untrained: fresh Gaussian values with each tensor's own mean and std (what an untrained net might look like).
    permuted: hidden units reordered consistently, so the network computes exactly the same function."""
    rng = np.random.default_rng(seed)
    W = {k: np.array(v, copy=True) for k, v in W.items()}
    if name == "original":
        return W
    if name == "shuffled":
        return {k: rng.permutation(v.ravel()).reshape(v.shape) for k, v in W.items()}
    if name == "untrained":
        return {k: rng.normal(v.mean(), v.std() + 1e-8, v.shape).astype(v.dtype) for k, v in W.items()}
    if name == "permuted":
        for g in perm_groups:
            p = rng.permutation(g["size"])
            for tensor, axis in g["members"]:
                W[tensor] = np.take(W[tensor], p, axis=axis)
        return W
    raise ValueError(name)
