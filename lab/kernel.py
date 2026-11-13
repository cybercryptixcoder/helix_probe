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


def main():
    cfg = json.loads(sys.stdin.readline())
    sys.path.insert(0, cfg["lab_dir"])
    import numpy as np
    import nets
    np.set_printoptions(precision=4, suppress=True, linewidth=160, threshold=600, edgeitems=6)
    env = {"__name__": "__sandbox__", "np": np, "show": lambda a, **k: print(np.array2string(np.asarray(a), **k))}
    if cfg.get("weights"):
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
