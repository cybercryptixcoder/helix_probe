"""Runs one piece of reader-written Python against a target's weights. Started by sandbox.py as a separate process.

The reader's code sees:
  W        dict of numpy arrays: the target's weights (in the chosen variant)
  np       numpy
  run(x)   the network's forward pass, ONLY if forward passes are allowed for this run
  show(a)  prints an array compactly
Protection (a mitigation, not a security boundary): separate process, time limit, a temp working dir, imports
limited to an allowlist, no open(), no network modules. It runs with your user permissions, so it is meant for
code from the reader in this lab, not for untrusted code in general.
"""
import builtins, io, json, sys, traceback, contextlib

ALLOWED = {"numpy", "math", "cmath", "itertools", "collections", "functools", "statistics", "fractions", "decimal",
           "heapq", "bisect", "random", "operator", "string", "re", "json", "textwrap", "scipy", "sklearn", "sympy", "networkx"}
_real_import = builtins.__import__


def _guarded_import(name, globals=None, locals=None, fromlist=(), level=0):
    if (globals or {}).get("__name__") == "__sandbox__" and name.split(".")[0] not in ALLOWED:
        raise ImportError(f"import of '{name}' is not allowed in the lab sandbox (allowed: numpy, math, scipy, ...)")
    return _real_import(name, globals, locals, fromlist, level)


def main():
    cfg = json.loads(sys.stdin.read())
    sys.path.insert(0, cfg["lab_dir"])
    import numpy as np
    import nets
    W = dict(np.load(cfg["weights"]))
    W = nets.variant(W, cfg["variant"], cfg.get("perm_groups", []), cfg.get("seed", 0))
    W = {k: v.astype(np.float64) for k, v in W.items()}
    np.set_printoptions(precision=4, suppress=True, linewidth=140, threshold=400, edgeitems=6)
    env = {"__name__": "__sandbox__", "W": W, "np": np,
           "show": lambda a, **k: print(np.array2string(np.asarray(a), **k))}
    if cfg.get("allow_forward"):
        kind = cfg["forward"]
        env["run"] = lambda x: nets.forward(kind, W, x)
    builtins.__import__ = _guarded_import
    builtins.open = None
    out = io.StringIO()
    ok = True
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
        try:
            code = compile(cfg["code"], "<reader code>", "exec")
            exec(code, env)
        except Exception:
            ok = False
            tb = traceback.format_exc().splitlines()
            print("\n".join(l for l in tb if "sandbox_runner.py" not in l))
    text = out.getvalue()
    limit = cfg.get("max_chars", 20000)
    if len(text) > limit:
        text = text[:limit] + f"\n... [output cut at {limit} characters]"
    sys.__stdout__.write(json.dumps({"ok": ok, "output": text}))


if __name__ == "__main__":
    main()
