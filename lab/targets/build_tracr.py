"""Compile RASP programs with Tracr into transformer weights, as targets whose mechanism is known exactly.

Needs:  pip install git+https://github.com/google-deepmind/tracr   (JAX on CPU is enough).
Run:    python3 lab/targets/build_tracr.py        (then python3 lab/targets/build_registry.py to refresh the index)

Each program is compiled for a fixed input length (BOS + N tokens) and saved in the lab's general "transformer"
format (lab/nets.py). Two things are done to the compiled weights so that they are not a labelled circuit diagram:
  - the residual stream is rotated by a random orthogonal matrix (compiled models use one labelled axis per value);
  - the MLP neurons of each layer are permuted and rescaled (a function-preserving change for ReLU).
Neither changes what the network computes; the script checks the saved network against Tracr's own output on every
input. The un-rotated weights are saved next to them as weights_raw.npz for reference.
"""
import itertools, json, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
MODELS = os.path.join(HERE, "..", "models")
sys.path.insert(0, os.path.join(HERE, ".."))
import nets  # noqa: E402

from tracr.rasp import rasp  # noqa: E402
from tracr.compiler import compiling, lib  # noqa: E402

BOS = "BOS"


def first_match():
    """out[i] = 1 if token i equals the first token, else 0 (custom program)."""
    first = rasp.Aggregate(rasp.Select(rasp.indices, rasp.indices, lambda key, query: key == 0), rasp.tokens).named("first")
    return rasp.SequenceMap(lambda a, b: 1 if a == b else 0, rasp.tokens, first).named("same_as_first")


def count_greater():
    """out[i] = how many tokens in the sequence are greater than token i (custom program)."""
    return rasp.SelectorWidth(rasp.Select(rasp.tokens, rasp.tokens, rasp.Comparison.GT)).named("n_greater")


PROGRAMS = {
    # id: (program factory, vocab, N, plain answer, mechanism note)
    "tracr_reverse": (lambda: lib.make_reverse(rasp.tokens), ["a", "b", "c"], 4,
                      "reverse the sequence: output i is token N-1-i",
                      "Tracr library program make_reverse: layer 0 computes the length (attention to BOS + MLP), an MLP computes "
                      "the opposite index length-1-i, then attention copies the token at that index."),
    "tracr_hist": (lambda: lib.make_hist(), ["a", "b", "c"], 5,
                   "histogram: output i is the number of tokens equal to token i",
                   "Tracr library program make_hist: one attention head attends from each position to the positions holding the "
                   "same token (and to BOS); the attention weight on BOS is 1/(count+1); an MLP turns that into the count."),
    "tracr_first_match": (first_match, ["a", "b", "c", "d"], 5,
                          "output i is 1 if token i equals the first token, else 0",
                          "Custom RASP program: attention copies the first token to every position; an MLP compares the copied "
                          "token with the position's own token."),
    "tracr_count_greater": (count_greater, [1, 2, 3, 4], 5,
                            "output i is the number of tokens greater than token i",
                            "Custom RASP program: one attention head attends from each position to the positions holding a "
                            "greater token (and to BOS); the weight on BOS is 1/(count+1); an MLP turns that into the count."),
}


def convert(model, prog, n_tokens, seed):
    """Tracr's haiku parameters -> the lab's general transformer tensors (raw, and rotated/permuted)."""
    p = {k: {kk: np.asarray(vv, np.float64) for kk, vv in v.items()} for k, v in model.params.items()}
    cfg = model.model_config
    H, k = cfg.num_heads, cfg.key_size
    P = n_tokens + 1
    W = {"W_E": p["token_embed"]["embeddings"], "W_pos": p["pos_embed"]["embeddings"][:P]}
    d = W["W_E"].shape[1]
    for l in range(cfg.num_layers):
        a = f"transformer/layer_{l}/attn/"
        for name, short in (("query", "Q"), ("key", "K"), ("value", "V")):
            W[f"L{l}.W_{short}"] = p[a + name]["w"].reshape(d, H, k).transpose(1, 0, 2)
            W[f"L{l}.b_{short}"] = p[a + name]["b"].reshape(H, k)
        W[f"L{l}.W_Q"] = W[f"L{l}.W_Q"] * np.sqrt(k)      # Tracr does not divide attention scores by sqrt(k); nets.transformer does
        W[f"L{l}.b_Q"] = W[f"L{l}.b_Q"] * np.sqrt(k)
        W[f"L{l}.W_O"] = p[a + "linear"]["w"].reshape(H, k, d)
        W[f"L{l}.b_O"] = p[a + "linear"]["b"]
        m = f"transformer/layer_{l}/mlp/"
        W[f"L{l}.W_in"], W[f"L{l}.b_in"] = p[m + "linear_1"]["w"], p[m + "linear_1"]["b"]
        W[f"L{l}.W_out"], W[f"L{l}.b_out"] = p[m + "linear_2"]["w"], p[m + "linear_2"]["b"]
    labels = list(model.residual_labels)
    out_dims = [i for i, lab in enumerate(labels) if lab.startswith(prog.label + ":")]
    classes = [labels[i].split(":", 1)[1] for i in out_dims]
    U = np.zeros((d, len(out_dims)))
    U[out_dims, np.arange(len(out_dims))] = 1.0
    W["W_U"] = U
    W["out_positions"] = np.arange(1, P)
    raw = {k_: v.copy() for k_, v in W.items()}
    # rotate the residual stream, permute and rescale the MLP neurons
    rng = np.random.default_rng(seed)
    R, _ = np.linalg.qr(rng.normal(size=(d, d)))
    W["W_E"], W["W_pos"], W["W_U"] = W["W_E"] @ R, W["W_pos"] @ R, R.T @ W["W_U"]
    for l in range(cfg.num_layers):
        for short in "QKV":
            W[f"L{l}.W_{short}"] = np.einsum("de,hek->hdk", R.T, W[f"L{l}.W_{short}"])
        W[f"L{l}.W_O"] = W[f"L{l}.W_O"] @ R
        W[f"L{l}.b_O"] = W[f"L{l}.b_O"] @ R
        mm = W[f"L{l}.W_in"].shape[1]
        perm, scale = rng.permutation(mm), np.exp(rng.uniform(-0.7, 0.7, mm))
        W[f"L{l}.W_in"] = (R.T @ W[f"L{l}.W_in"])[:, perm] * scale
        W[f"L{l}.b_in"] = W[f"L{l}.b_in"][perm] * scale
        W[f"L{l}.W_out"] = (W[f"L{l}.W_out"][perm] / scale[:, None]) @ R
        W[f"L{l}.b_out"] = W[f"L{l}.b_out"] @ R
    return raw, W, classes, labels


def build(tid, seed=0):
    factory, vocab, N, answer, note = PROGRAMS[tid]
    prog = factory()
    model = compiling.compile_rasp_to_model(prog, vocab=set(vocab), max_seq_len=N, compiler_bos=BOS)
    raw, W, classes, labels = convert(model, prog, N, seed)
    enc = model.input_encoder.encoding_map
    tok_ids = [enc[v] for v in vocab]
    seqs = list(itertools.product(vocab, repeat=N))
    X = np.array([[enc[BOS]] + [enc[t] for t in s] for s in seqs])
    # check against Tracr itself on every input (or 400 of them)
    idx = np.random.default_rng(0).choice(len(seqs), min(400, len(seqs)), replace=False)
    want = np.array([[classes.index(str(v)) for v in model.apply([BOS] + list(seqs[i])).decoded[1:]] for i in idx])
    for name, w in (("raw", raw), ("rotated", W)):
        got = nets.transformer(w, X[idx]).reshape(len(idx), N, len(classes)).argmax(-1)
        assert (got == want).all(), (tid, name, (got == want).mean())
    assert np.abs(nets.transformer(raw, X[idx]) - nets.transformer(W, X[idx])).max() < 1e-6
    d_ = os.path.join(MODELS, tid)
    os.makedirs(d_, exist_ok=True)
    np.savez(os.path.join(d_, "weights.npz"), **W)
    np.savez(os.path.join(d_, "weights_raw.npz"), **raw)
    cfg = model.model_config
    d, P = W["W_E"].shape[1], N + 1
    order = [k for k in W if k not in ("out_positions",)]
    layer_lines = []
    for l in range(cfg.num_layers):
        k = W[f"L{l}.W_Q"].shape[2]
        m = W[f"L{l}.W_in"].shape[1]
        layer_lines.append(
            f"  layer {l}: attention ({cfg.num_heads} head{'s' if cfg.num_heads > 1 else ''} of size {k}, bidirectional, biases b_Q, b_K, b_V, b_O): "
            f"x = x + softmax((x W_Q + b_Q)(x W_K + b_K)^T / sqrt({k})) (x W_V + b_V) W_O + b_O;  "
            f"then MLP ({m} ReLU neurons): x = x + relu(x W_in + b_in) W_out + b_out")
    arch = (f"A {cfg.num_layers}-layer transformer with no LayerNorm. Vocabulary of {W['W_E'].shape[0]} tokens; the input is a sequence of "
            f"{P} tokens; residual stream width {d}.\n  x = W_E[tokens] + W_pos\n" + "\n".join(layer_lines) +
            f"\n  output = x[positions 1..{N}] @ W_U: {len(classes)} numbers for each of the last {N} positions, flattened as "
            f"(position - 1) * {len(classes)} + class. The network's decision at a position is its largest of those {len(classes)} numbers.")
    meta = {
        "id": tid, "name": {"tracr_reverse": "Compiled program R", "tracr_hist": "Compiled program H",
                            "tracr_first_match": "Compiled program F", "tracr_count_greater": "Compiled program G"}[tid],
        "family": "Compiled programs (Tracr; residual stream rotated)", "forward": "transformer",
        "order": order, "arch": arch,
        "context": (f"Token {enc[BOS]} is a begin-of-sequence marker and always comes first; tokens {tok_ids} stand for {vocab}. "
                    f"Output class c at a position stands for the value {classes}[c]."),
        "tensor_desc": {"W_E": "token embedding (row = token)", "W_pos": "position embedding (row = position)",
                        "W_U": "output weights (column = class)"},
        "answer": {"short": answer, "detail": note + f" Compiled by Tracr; residual labels before rotation: {labels}."},
        "source": "Compiled with Tracr (Lindner et al. 2023) in lab/targets/build_tracr.py; residual stream rotated, MLP neurons permuted and rescaled.",
        "perm_groups": [{"size": int(W[f"L{l}.W_in"].shape[1]), "members": [[f"L{l}.W_in", 1], [f"L{l}.b_in", 0], [f"L{l}.W_out", 0]]}
                        for l in range(cfg.num_layers)],
        "input": f"token ids, shape [B, {P}], e.g. [{X[1].tolist()}]",
        "domain": {"axes": [{"values": [int(enc[BOS])]}] + [{"values": [int(t) for t in tok_ids]}] * N,
                   "text": (f"The network is used on every input [{enc[BOS]}, t1, ..., t{N}] where each of t1..t{N} is one of the tokens "
                            f"{tok_ids} ({len(seqs):,} inputs).")},
        "out_groups": len(classes), "protected": ["out_positions"],
    }
    Wl = np.load(os.path.join(d_, "weights.npz"))
    meta["tensors"] = [{"name": k, "shape": list(Wl[k].shape), "desc": meta["tensor_desc"].get(k, "")} for k in order]
    meta["params"] = int(sum(np.prod(Wl[k].shape) for k in order))
    json.dump(meta, open(os.path.join(d_, "meta.json"), "w"), indent=1)
    print(f"{tid:22s} layers {cfg.num_layers} heads {cfg.num_heads} d {d} mlp {[W[f'L{l}.W_in'].shape[1] for l in range(cfg.num_layers)]} "
          f"classes {classes} inputs {len(seqs)} params {meta['params']:,}  OK")


if __name__ == "__main__":
    for tid in (sys.argv[1:] or PROGRAMS):
        build(tid)
