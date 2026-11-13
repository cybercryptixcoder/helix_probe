"""Numpy forward passes and weight variants for the lab's target networks.

Imported by the server (for checks and variants) and by the sandbox (so a reader that is allowed forward
passes can call run(x)). Numpy only: no torch at runtime.
"""
import numpy as np


def _hooker(hook, acts):
    """hook: None, or {site name: array or function(act) -> act}. Every site's (possibly replaced) value is recorded in acts."""
    def h(name, a):
        if hook and name in hook:
            v = hook[name]
            a = v(a) if callable(v) else np.broadcast_to(np.asarray(v, dtype=np.float64), a.shape).copy()
        if acts is not None:
            acts[name] = a
        return a
    return h


def mlp(W, x, act, hook=None, acts=None):
    """MLP with tensors W1,b1,W2,b2,... (W_k shaped in x out). act applies to every layer except the last.
    Sites: h1, h2, ... (hidden layers after the activation) and out."""
    f = {"tanh": np.tanh, "relu": lambda z: np.maximum(z, 0)}[act]
    h = _hooker(hook, acts)
    a = np.asarray(x, dtype=np.float64)
    if a.ndim == 1:
        a = a[None]
    k = 1
    while f"W{k}" in W:
        a = a @ W[f"W{k}"] + W[f"b{k}"]
        if f"W{k + 1}" in W:
            a = h(f"h{k}", f(a))
        k += 1
    return h("out", a)


def onelayer_transformer(W, tokens, hook=None, acts=None):
    """The Nanda-style 1-layer transformer (no LayerNorm, no biases). tokens: [B, 3] ints -> logits [B, n_out].
    Sites (all [B, width]): embed.0, embed.1, embed.2 (token + position embedding at each position), attn_pattern
    (the last position's attention weights, heads x positions), attn_out
    (what attention adds at the last position), resid_mid (last position, after attention), mlp_pre, mlp_post
    (the MLP's neurons before and after ReLU, last position), mlp_out, resid_post (last position, after the MLP), out."""
    h = _hooker(hook, acts)
    t = np.asarray(tokens)
    if t.ndim == 1:
        t = t[None]
    t = t.astype(int)
    n = t.shape[1]
    x = W["W_E"][t] + W["W_pos"]                                   # [B, n, d]
    x = np.stack([h(f"embed.{p}", x[:, p]) for p in range(n)], 1)
    q = np.einsum("bd,hde->bhe", x[:, -1], W["W_Q"])
    k = np.einsum("bpd,hde->bhpe", x, W["W_K"])
    v = np.einsum("bpd,hde->bhpe", x, W["W_V"])
    att = np.einsum("bhe,bhqe->bhq", q, k) / np.sqrt(W["W_Q"].shape[-1])   # last position attends to all positions
    att = np.exp(att - att.max(-1, keepdims=True)); att /= att.sum(-1, keepdims=True)
    att = h("attn_pattern", att.reshape(len(t), -1)).reshape(att.shape)       # [B, heads * positions]
    z = np.einsum("bhq,bhqe->bhe", att, v)
    a = h("attn_out", np.einsum("bhe,hed->bd", z, W["W_O"]))
    mid = h("resid_mid", x[:, -1] + a)
    post = h("mlp_post", np.maximum(h("mlp_pre", mid @ W["W_in"]), 0))
    res = h("resid_post", mid + h("mlp_out", post @ W["W_out"]))
    return h("out", res @ W["W_U"])


def transformer(W, tokens, hook=None, acts=None):
    """A general transformer without LayerNorm, read from the tensors present in W:
      W_E [vocab, d], W_pos [positions, d];  per layer l = 0, 1, ...:  L{l}.W_Q, L{l}.W_K, L{l}.W_V [heads, d, k],
      L{l}.W_O [heads, k, d], L{l}.W_in [d, m], L{l}.W_out [m, d], each with an optional bias (b_Q, b_K, b_V [heads, k];
      b_O [d]; b_in [m]; b_out [d]);  W_U [d, classes] and optional b_U.
    Attention is bidirectional unless W has the key "causal". The output is read at the positions listed in
    W["out_positions"] (default: all), giving [B, n_positions * classes].
    Sites hold every position, flattened as position * width + index: embed, then per layer attn{l}.pattern
    (head * P * P + query position * P + key position), attn{l}.out, resid{l}.mid, mlp{l}.pre, mlp{l}.post, mlp{l}.out,
    resid{l}.post, and out."""
    h = _hooker(hook, acts)
    t = np.asarray(tokens).astype(int)
    if t.ndim == 1:
        t = t[None]
    B, P = t.shape
    flat = lambda a: a.reshape(B, -1)                                  # noqa: E731
    x = W["W_E"][t] + W["W_pos"][:P]
    d = x.shape[-1]
    x = h("embed", flat(x)).reshape(B, P, d)
    l = 0
    while f"L{l}.W_Q" in W or f"L{l}.W_in" in W:
        if f"L{l}.W_Q" in W:
            Q, K, V, O = (W[f"L{l}.W_{n}"] for n in "QKVO")
            H, _, k = Q.shape
            z = lambda n: W.get(f"L{l}.b_{n}", 0.0)                    # noqa: E731
            q = np.einsum("bpd,hde->bhpe", x, Q) + (np.asarray(z("Q"))[None, :, None, :] if f"L{l}.b_Q" in W else 0.0)
            kk = np.einsum("bpd,hde->bhpe", x, K) + (np.asarray(z("K"))[None, :, None, :] if f"L{l}.b_K" in W else 0.0)
            v = np.einsum("bpd,hde->bhpe", x, V) + (np.asarray(z("V"))[None, :, None, :] if f"L{l}.b_V" in W else 0.0)
            att = np.einsum("bhpe,bhqe->bhpq", q, kk) / np.sqrt(k)
            if "causal" in W:
                att = np.where(np.triu(np.ones((P, P), bool), 1), -1e9, att)
            att = np.exp(att - att.max(-1, keepdims=True)); att /= att.sum(-1, keepdims=True)
            att = h(f"attn{l}.pattern", flat(att)).reshape(B, H, P, P)
            a = np.einsum("bhpq,bhqe,hed->bpd", att, v, O) + z("O")
            a = h(f"attn{l}.out", flat(a)).reshape(B, P, d)
            x = h(f"resid{l}.mid", flat(x + a)).reshape(B, P, d)
        if f"L{l}.W_in" in W:
            m = W[f"L{l}.W_in"].shape[1]
            pre = h(f"mlp{l}.pre", flat(x @ W[f"L{l}.W_in"] + W.get(f"L{l}.b_in", 0.0))).reshape(B, P, m)
            post = h(f"mlp{l}.post", flat(np.maximum(pre, 0))).reshape(B, P, m)
            mo = h(f"mlp{l}.out", flat(post @ W[f"L{l}.W_out"] + W.get(f"L{l}.b_out", 0.0))).reshape(B, P, d)
            x = h(f"resid{l}.post", flat(x + mo)).reshape(B, P, d)
        l += 1
    pos = np.asarray(W["out_positions"]).astype(int) if "out_positions" in W else np.arange(P)
    return h("out", flat(x[:, pos] @ W["W_U"] + W.get("b_U", 0.0)))


def forward(kind, W, x, hook=None, acts=None):
    """Run the network. hook replaces activations at named sites; acts (a dict) collects every site's activation."""
    if kind in ("mlp_tanh", "mlp_relu"):
        return mlp(W, x, kind.split("_")[1], hook, acts)
    if kind == "onelayer_transformer":
        return onelayer_transformer(W, x, hook, acts)
    if kind == "transformer":
        return transformer(W, x, hook, acts)
    raise ValueError(f"no forward pass for {kind}")


def site_table(kind, W):
    """[(site name, width, plain description, stage)] for a network: the places where activations can be read or
    replaced. A stage is one step of the computation; a construction is complete when every stage has a verified site."""
    if kind in ("mlp_tanh", "mlp_relu"):
        out, k = [], 1
        while f"W{k}" in W:
            last = f"W{k + 1}" not in W
            out.append(("out" if last else f"h{k}", W[f"W{k}"].shape[1],
                        "the network's output" if last else f"hidden layer {k}, after the activation",
                        "output" if last else f"hidden layer {k}"))
            k += 1
        return out
    if kind == "onelayer_transformer":
        d, m = W["W_E"].shape[1], W["W_in"].shape[1]
        n = W["W_pos"].shape[0]
        return ([(f"embed.{p}", d, f"token + position embedding at position {p}", "embedding") for p in range(n)] + [
            ("attn_pattern", W["W_Q"].shape[0] * n, f"attention weights of the last position: for each head, its weight on each of the {n} "
             f"positions, flattened as head * {n} + position", "attention"),
            ("attn_out", d, "what the attention layer adds at the last position", "attention"),
            ("resid_mid", d, "residual stream at the last position after attention", "attention"),
            ("mlp_pre", m, "MLP neurons before ReLU (last position)", "mlp neurons"),
            ("mlp_post", m, "MLP neurons after ReLU (last position)", "mlp neurons"),
            ("mlp_out", d, "what the MLP adds to the residual stream", "readout"),
            ("resid_post", d, "residual stream at the last position after the MLP", "readout"),
            ("out", W["W_U"].shape[1], "the network's output", "output")])
    if kind == "transformer":
        P, d = W["W_pos"].shape
        out = [("embed", P * d, f"token + position embeddings, all {P} positions (index = position * {d} + dimension)", "embedding")]
        l = 0
        while f"L{l}.W_Q" in W or f"L{l}.W_in" in W:
            if f"L{l}.W_Q" in W:
                H = W[f"L{l}.W_Q"].shape[0]
                out += [(f"attn{l}.pattern", H * P * P, f"layer {l} attention weights (index = head * {P * P} + query position * {P} + key position)", f"layer {l} attention"),
                        (f"attn{l}.out", P * d, f"what layer {l}'s attention adds to the residual stream, all positions", f"layer {l} attention"),
                        (f"resid{l}.mid", P * d, f"residual stream after layer {l}'s attention, all positions", f"layer {l} attention")]
            if f"L{l}.W_in" in W:
                m = W[f"L{l}.W_in"].shape[1]
                out += [(f"mlp{l}.pre", P * m, f"layer {l} MLP neurons before ReLU, all positions (index = position * {m} + neuron)", f"layer {l} mlp neurons"),
                        (f"mlp{l}.post", P * m, f"layer {l} MLP neurons after ReLU, all positions", f"layer {l} mlp neurons"),
                        (f"mlp{l}.out", P * d, f"what layer {l}'s MLP adds to the residual stream, all positions", f"layer {l} output"),
                        (f"resid{l}.post", P * d, f"residual stream after layer {l}, all positions", f"layer {l} output")]
            l += 1
        n_pos = len(W["out_positions"]) if "out_positions" in W else P
        out.append(("out", n_pos * W["W_U"].shape[1], "the network's output", "output"))
        return out
    raise ValueError(kind)


def domain_inputs(meta, max_n=20000, seed=0):
    """The inputs the network is used on, as an array [N, n_in]. meta["domain"] is {"axes": [...]} (the product of
    per-position value lists; an axis is {"range": [lo, hi]} or {"values": [...]}) or {"file": "inputs.npy"}."""
    dom = meta["domain"]
    if "file" in dom:
        import os
        X = np.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), "models", meta["id"], dom["file"]))
    else:
        axes = [np.arange(*a["range"]) if "range" in a else np.asarray(a["values"]) for a in dom["axes"]]
        total = int(np.prod([len(a) for a in axes]))
        if total <= max_n:
            X = np.stack([g.ravel() for g in np.meshgrid(*axes, indexing="ij")], 1)
        else:
            rng = np.random.default_rng(seed)
            X = np.stack([rng.choice(a, max_n) for a in axes], 1)
    if len(X) > max_n:
        X = X[np.random.default_rng(seed).choice(len(X), max_n, replace=False)]
    return X


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
