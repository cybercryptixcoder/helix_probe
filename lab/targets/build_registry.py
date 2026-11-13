"""Build lab/models/<id>/meta.json (and weights.npz where needed) for every target network.

Run after any target changes:  python3 lab/targets/build_registry.py
Each meta.json separates three kinds of text, so the lab can switch each one on or off:
  arch     neutral description of the architecture and forward pass (no hint of the task)
  context  task-revealing details (what inputs and outputs mean). Turning this off is a blinding control.
  answer   the known answer. Hidden in the UI until revealed; never sent to the reader.
  domain   the inputs the network is used on (the judge tests on them; the constructor's reader is given them).
           It names no task: {"axes": [...]} is the product of per-position value lists, {"file": ...} an array.
"""
import json, os, re, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
MODELS = os.path.join(HERE, "..", "models")
SPARKS = os.environ.get("SPARKS_LOGS", "/home/claude/ext/lm_understand-logs")
sys.path.insert(0, os.path.join(HERE, ".."))
import nets  # noqa: E402


def mlp_perm(n_layers, widths):
    g = []
    for k in range(1, n_layers):
        g.append({"size": widths[k - 1], "members": [[f"W{k}", 1], [f"b{k}", 0], [f"W{k + 1}", 0]]})
    return g


def save(tid, meta, W=None):
    d = os.path.join(MODELS, tid)
    os.makedirs(d, exist_ok=True)
    if W is not None:
        np.savez(os.path.join(d, "weights.npz"), **{k: np.asarray(v, np.float32) for k, v in W.items()})
    Wl = np.load(os.path.join(d, "weights.npz"))
    meta["id"] = tid
    meta["tensors"] = [{"name": k, "shape": list(Wl[k].shape), "desc": meta.get("tensor_desc", {}).get(k, "")}
                       for k in meta["order"]]
    meta["params"] = int(sum(np.prod(Wl[k].shape) for k in meta["order"]))
    json.dump(meta, open(os.path.join(d, "meta.json"), "w"), indent=1)
    print(f"{tid:28s} {meta['params']:>8,} params  answer: {meta['answer']['short']}")


def sparks_prompt_parts(path):
    t = open(path).read()
    head = t[: t.index("THE NETWORK'S WEIGHTS") if "THE NETWORK'S WEIGHTS" in t else t.index("THE WEIGHTS")]
    q = head.index("QUESTION.")
    return head[:q].strip(), head[q:].strip()


def build_sparks():
    key = json.load(open(f"{SPARKS}/exp1_which_game/eval/answer_key.json"))
    ctx, question = sparks_prompt_parts(f"{SPARKS}/exp1_which_game/runs/breakout/prompt.txt")
    arch = ("A multilayer perceptron with 500 inputs, two hidden layers of 32 units with tanh activations, and 5 outputs:\n"
            "  h1 = tanh(x @ W1 + b1)    W1: 500 x 32\n  h2 = tanh(h1 @ W2 + b2)   W2: 32 x 32\n  out = h2 @ W3 + b3        W3: 32 x 5\n"
            "Row i of a weight matrix holds the weights from input/unit i; column j belongs to unit j of the next layer.")
    games = {"breakout": "Breakout", "pong": "Pong", "pacman": "Pac-Man", "freeway": "Freeway"}
    for h, v in key.items():
        save(f"sparks_game_{h}", {
            "name": f"Game policy {h[:4]}", "family": "MIT Sparks · Exp 1 (game policies)", "forward": "mlp_tanh",
            "order": ["W1", "b1", "W2", "b2", "W3", "b3"], "arch": arch, "context": ctx, "original_question": question,
            "tensor_desc": {"W1": "layer 1 weights (row i = input i)", "W2": "layer 2 weights", "W3": "output layer weights"},
            "answer": {"short": games[v["game"]], "detail": f"PPO policy trained on a 10x10 {games[v['game']]} gridworld (seed {v['seed']})."},
            "source": "Takehi et al., Sparks of Weight-Space Programming (MIT CSAIL, 2026), logs: github.com/RikiyaT/lm_understand-logs, CC BY 4.0",
            "perm_groups": mlp_perm(3, [32, 32]), "input": "500 binary numbers (flattened 10x10x5 grid)",
        })
    key2 = json.load(open(f"{SPARKS}/exp2_diffusion/eval/answer_key.json"))
    ctx2, q2 = sparks_prompt_parts(f"{SPARKS}/exp2_diffusion/runs/circle/prompt.txt")
    arch2 = ("A multilayer perceptron with 160 inputs, two hidden layers of 64 units with ReLU activations, and 144 outputs:\n"
             "  h1 = relu(x @ W1 + b1)    W1: 160 x 64\n  h2 = relu(h1 @ W2 + b2)   W2: 64 x 64\n  out = h2 @ W3 + b3        W3: 64 x 144")
    for h, v in key2.items():
        save(f"sparks_shape_{h}", {
            "name": f"Image generator {h[:4]}", "family": "MIT Sparks · Exp 2 (diffusion denoisers)", "forward": "mlp_relu",
            "order": ["W1", "b1", "W2", "b2", "W3", "b3"], "arch": arch2, "context": ctx2, "original_question": q2,
            "tensor_desc": {"W1": "layer 1 weights (rows 0..143 pixels, 144..159 step encoding)", "W3": "output weights (column j = pixel j of a 12x12 image)"},
            "answer": {"short": f"filled {v['shape']}s", "detail": f"12x12 DDPM denoiser trained on filled {v['shape']}s (seed {v['seed']})."},
            "source": "Takehi et al., Sparks of Weight-Space Programming (MIT CSAIL, 2026), logs: github.com/RikiyaT/lm_understand-logs, CC BY 4.0",
            "perm_groups": mlp_perm(3, [64, 64]), "input": "160 numbers (144 noisy pixels + 16 step features)",
        })


def build_modular(tid, op, label):
    d = os.path.join(MODELS, tid)
    if not os.path.exists(os.path.join(d, "weights.safetensors")) and not os.path.exists(os.path.join(d, "weights.npz")):
        print(f"{tid}: not trained yet, skipped"); return
    if not os.path.exists(os.path.join(d, "weights.npz")):
        from safetensors.numpy import load_file
        W = load_file(os.path.join(d, "weights.safetensors"))
        np.savez(os.path.join(d, "weights.npz"), **W)
    W = dict(np.load(os.path.join(d, "weights.npz")))
    info = json.load(open(os.path.join(d, "train.json")))
    p = info["p"]
    # key frequencies: Fourier power of the embedding over the input-number axis
    E = W["W_E"][:p]
    F = np.abs(np.fft.rfft(E, axis=0)) ** 2
    power = F.sum(1)[1:]
    top = (np.argsort(power)[::-1][:6] + 1).tolist()
    share = float(np.sort(power)[::-1][:5].sum() / power.sum())
    a = np.arange(p)
    toks = np.stack([np.repeat(a, p), np.tile(a, p), np.full(p * p, p)], 1)
    y = {"add": (toks[:, 0] + toks[:, 1]) % p, "sub": (toks[:, 0] - toks[:, 1]) % p, "mul": (toks[:, 0] * toks[:, 1]) % p}[op]
    acc = float((nets.onelayer_transformer(W, toks).argmax(-1) == y).mean())
    arch = ("A one-layer transformer with no LayerNorm and no biases. Vocabulary of %d tokens; the input is a sequence of 3 tokens; "
            "the output is %d logits read at the last position.\n"
            "  x = W_E[tokens] + W_pos                     W_E: %d x 128, W_pos: 3 x 128\n"
            "  attention: 4 heads of size 32, causal       W_Q, W_K, W_V: 4 x 128 x 32 (per head: d_model x d_head), W_O: 4 x 32 x 128\n"
            "  x = x + sum_h softmax(q k^T / sqrt(32)) v W_O[h]\n"
            "  x = x + relu(x @ W_in) @ W_out              W_in: 128 x 512, W_out: 512 x 128\n"
            "  logits = x[last] @ W_U                      W_U: 128 x %d" % (p + 1, p, p + 1, p))
    ctx = (f"Tokens 0..{p - 1} stand for the numbers 0..{p - 1}; token {p} is '='. Every input has the form 'a b =', and output "
           f"class c stands for the number c.")
    save(tid, {
        "name": label, "family": "Algorithmic transformers (trained here)", "forward": "onelayer_transformer",
        "order": ["W_E", "W_pos", "W_Q", "W_K", "W_V", "W_O", "W_in", "W_out", "W_U"], "arch": arch, "context": ctx,
        "tensor_desc": {"W_E": "token embedding (row = token)", "W_pos": "position embedding", "W_Q": "queries [head, d_model, d_head]",
                        "W_K": "keys [head, d_model, d_head]", "W_V": "values [head, d_model, d_head]", "W_O": "head outputs [head, d_head, d_model]",
                        "W_in": "MLP input (column = neuron)", "W_out": "MLP output (row = neuron)", "W_U": "unembedding (column = output class)"},
        "answer": {"short": {"add": f"(a + b) mod {p}", "sub": f"(a - b) mod {p}", "mul": f"(a * b) mod {p}"}[op],
                   "detail": (f"Trained on {int(info['frac'] * 100)}% of all pairs, test accuracy {acc:.4f}. "
                              f"Embedding Fourier power is concentrated in frequencies {top[:5]} (top-5 share {share:.2f}). "
                              + ("Expected mechanism (Nanda et al. 2023): embed a, b as cos/sin(w_k a); attention+MLP form cos/sin(w_k(a+b)) by trig identities; "
                                 "unembedding scores c by sum_k cos(w_k(a+b-c))." if op == "add" else
                                 "Mechanism not hand-verified here; for multiplication, expect Fourier structure over the discrete-log ordering, not the number line."))},
        "source": "Trained in this repo (lab/targets/train_modadd.py), Nanda et al. 2023 setup with 40% of pairs.",
        "perm_groups": [{"size": 512, "members": [["W_in", 1], ["W_out", 0]]},
                        {"size": 4, "members": [["W_Q", 0], ["W_K", 0], ["W_V", 0], ["W_O", 0]]}],
        "input": f"token ids, shape [B, 3], e.g. [[a, b, {p}]]",
        "domain": {"axes": [{"range": [0, p]}, {"range": [0, p]}, {"values": [p]}],
                   "text": f"The network is used on every input [i, j, {p}] with i and j each ranging over 0..{p - 1} ({p * p:,} inputs)."},
        "key_frequencies": top, "test_acc": acc,
    })


def build_boolean():
    nets_ = {
        "bool_xor": ("XOR of two bits", 2, {"W1": [[1, 1], [1, 1]], "b1": [0, -1], "W2": [[1], [-2]], "b2": [-0.5]},
                     lambda x: x[0] ^ x[1], "x1 XOR x2"),
        "bool_majority3": ("Majority of three bits", 3, {"W1": [[1, 1], [1, 1], [1, 1]], "b1": [-1, -2], "W2": [[1], [1]], "b2": [-0.5]},
                           lambda x: int(sum(x) >= 2), "majority(x1, x2, x3): 1 if at least two inputs are 1"),
        "bool_parity3": ("Parity of three bits", 3, {"W1": [[1, 1, 1]] * 3, "b1": [0, -1, -2], "W2": [[1], [-2], [2]], "b2": [-0.5]},
                         lambda x: sum(x) % 2, "x1 XOR x2 XOR x3 (odd number of ones)"),
        "bool_compare2": ("Two-bit comparator", 4, {"W1": [[2, 2], [1, 1], [-2, -2], [-1, -1]], "b1": [0, -1], "W2": [[1], [-1]], "b2": [-0.5]},
                          lambda x: int(2 * x[0] + x[1] > 2 * x[2] + x[3]), "(2*x1 + x2) > (2*x3 + x4): is the 2-bit number a1a0 greater than b1b0"),
    }
    for tid, (name, n, W, f, short) in nets_.items():
        W = {k: np.array(v, np.float32) for k, v in W.items()}
        X = np.array([[(i >> (n - 1 - j)) & 1 for j in range(n)] for i in range(2 ** n)])
        got = (nets.mlp(W, X, "relu")[:, 0] > 0).astype(int)
        want = np.array([f(x) for x in X])
        assert (got == want).all(), (tid, got, want)
        h = W["W1"].shape[1]
        save(tid, {
            "name": name, "family": "Tiny Boolean circuits (hand-written)", "forward": "mlp_relu", "order": ["W1", "b1", "W2", "b2"],
            "arch": (f"A multilayer perceptron with {n} inputs, one hidden layer of {h} ReLU units, and 1 output:\n"
                     f"  h = relu(x @ W1 + b1)    W1: {n} x {h}\n  out = h @ W2 + b2        W2: {h} x 1"),
            "context": f"Each input is a bit (0 or 1). The output bit is 1 when out > 0.",
            "answer": {"short": short, "detail": "Hand-written weights; verified on the full truth table."},
            "source": "Written by hand in this repo (lab/targets/build_registry.py).",
            "perm_groups": mlp_perm(2, [h]), "input": f"{n} bits, e.g. [[0, 1{', 0' * (n - 2)}]]",
            "domain": {"axes": [{"values": [0, 1]}] * n,
                       "text": f"The network is used on every input of {n} values that are each 0 or 1 ({2 ** n} inputs)."},
        }, W)


if __name__ == "__main__":
    build_boolean()
    build_sparks()
    build_modular("modadd_p113", "add", "Mystery transformer A")
    build_modular("modsub_p113", "sub", "Mystery transformer B")
    build_modular("modmul_p113", "mul", "Mystery transformer C")
    ids = sorted(x for x in os.listdir(MODELS) if os.path.exists(os.path.join(MODELS, x, "meta.json")))
    json.dump(ids, open(os.path.join(MODELS, "index.json"), "w"))
