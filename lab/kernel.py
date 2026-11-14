"""A persistent Python session over one target network, for the constructor's reader. Started as a separate process.

The reader's code sees, and keeps between calls:
  W          dict of numpy arrays: the network's weights (in the chosen variant)
  X          the inputs the network is used on, an array [N, n_in]
  run(x)     the network's output for inputs x                       (only if running the network is allowed)
  acts(x)    dict {site name: activation array [B, width]} for inputs x   (same condition)
  SITES      dict {site name: (width, description, stage)}
  np, show(a)
Protocol: one JSON object per line on stdin ({"code": ...}), one per line on stdout ({"ok", "output"}).
Protection is the same as sandbox_runner.py (a mitigation, not a security boundary): separate process, import
allowlist, no open(), and the parent kills the process when a call runs over its time limit.
"""
import builtins, contextlib, io, json, sys, traceback

ALLOWED = {"numpy", "math", "cmath", "itertools", "collections", "functools", "statistics", "fractions", "decimal",
           "heapq", "bisect", "random", "operator", "string", "re", "json", "textwrap", "scipy", "sklearn", "sympy", "networkx", "time"}
_real_import = builtins.__import__


def _guarded_import(name, globals=None, locals=None, fromlist=(), level=0):
    if (globals or {}).get("__name__") == "__sandbox__" and name.split(".")[0] not in ALLOWED:
        raise ImportError(f"import of '{name}' is not allowed here (allowed: numpy, math, scipy, sklearn, itertools, collections, ...)")
    return _real_import(name, globals, locals, fromlist, level)


def lm_env(cfg, env):
    """The session for a language-model target (see lm.py for the sites and constructor.py, LM_SYSTEM, for the tools)."""
    import numpy as np
    meta = json.load(open(cfg["meta"]))
    env["X_NAMES"], env["ANSWERS"] = meta["x_names"], meta["answers"]
    if not cfg.get("weights"):
        return
    import lm
    task = lm.get_task(meta["id"], cfg["variant"], cfg.get("seed", 0))
    tk = task.lm.tok
    env.update(W=task.lm.weights_numpy(), CFG=dict(task.cfg), X=task.X.copy(), TOKENS=task.tokens.copy(),
               PROMPTS=[tk.decode(t) for t in task.tokens], ANSWER_IDS=task.answer_ids.copy(),
               ROLES={r: (int(p[0]) if len(set(p.tolist())) == 1 else p.copy()) for r, p in task.roles.items()},
               tok=lambda text: tk.encode(text), detok=lambda ids: [tk.decode([int(i)]) for i in np.atleast_1d(ids)])
    if not cfg.get("allow_forward", True):
        return
    import torch
    env["run"] = lambda x, hook=None: task.run(x, hook=hook)
    env["logits"] = lambda x, hook=None: task.run(x, hook=hook, full=True)
    env["acts"] = lambda x, sites: task.acts(x, [sites] if isinstance(sites, str) else list(sites))
    env["run_tokens"] = lambda tokens, hook=None, sites=(): task.run_tokens(tokens, hook=hook, sites=[sites] if isinstance(sites, str) else list(sites))
    env["unembed"] = lambda v: task.lm.unembed(torch.as_tensor(np.atleast_2d(np.asarray(v, dtype=np.float32)))).numpy()

    def top(v, k=10):
        v = np.asarray(v).ravel()
        if v.shape[0] != task.cfg["n_vocab"]:
            raise ValueError(f"top() takes a vector over the vocabulary ({task.cfg['n_vocab']} entries); got {v.shape[0]}")
        i = np.argsort(-v)[:k]
        return [(tk.decode([int(j)]), round(float(v[j]), 2)) for j in i]
    env["top"] = top


def main():
    cfg = json.loads(sys.stdin.readline())
    sys.path.insert(0, cfg["lab_dir"])
    import numpy as np
    import nets
    np.set_printoptions(precision=4, suppress=True, linewidth=160, threshold=600, edgeitems=6)
    env = {"__name__": "__sandbox__", "np": np, "show": lambda a, **k: print(np.array2string(np.asarray(a), **k))}
    if cfg.get("lm"):
        lm_env(cfg, env)
    elif cfg.get("weights"):
        meta = json.load(open(cfg["meta"]))
        W = dict(np.load(cfg["weights"]))
        W = {k: v.astype(np.float64) for k, v in nets.variant(W, cfg["variant"], meta.get("perm_groups", []), cfg.get("seed", 0), meta.get("protected", [])).items()}
        kind = meta["forward"]
        env["W"] = W
        env["X"] = nets.domain_inputs(meta)
        env["SITES"] = {name: (width, desc, stage) for name, width, desc, stage in nets.site_table(kind, W)}
        if cfg.get("allow_forward", True):
            env["run"] = lambda x: nets.forward(kind, W, x)

            def acts(x):
                a = {}
                nets.forward(kind, W, x, acts=a)
                return a
            env["acts"] = acts
    builtins.__import__ = _guarded_import
    builtins.open = None
    real_out = sys.__stdout__
    limit = cfg.get("max_chars", 8000)
    real_out.write(json.dumps({"ok": True, "output": "ready"}) + "\n"); real_out.flush()
    for line in sys.stdin:
        try:
            code = json.loads(line)["code"]
        except Exception:  # noqa: BLE001
            continue
        out, ok = io.StringIO(), True
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
            try:
                exec(compile(code, "<your code>", "exec"), env)
            except BaseException:  # noqa: BLE001
                ok = False
                tb = traceback.format_exc().splitlines()
                print("\n".join(l for l in tb if "kernel.py" not in l))
        text = out.getvalue()
        if len(text) > limit:
            text = text[: limit * 2 // 3] + f"\n... [output cut: {len(text):,} characters, limit {limit:,}; print less] ...\n" + text[-limit // 3:]
        real_out.write(json.dumps({"ok": ok, "output": text}) + "\n"); real_out.flush()


if __name__ == "__main__":
    main()
