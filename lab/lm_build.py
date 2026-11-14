"""Build an LM target from a task file:  python3 lab/lm_build.py lab/lm_tasks/ordinal.py

Writes lab/models/<ID>/: meta.json, inputs.npy (X), tokens.npy, roles.json, prompts.txt. The model's weights are not
stored in the repository; they are downloaded from Hugging Face on first use (transformers' cache).
A task file defines ID, MODEL, ANSWERS, X_NAMES, TEXT, CONTEXT, ANSWER, build(tok) (see lab/lm_tasks/ordinal.py), and
optionally SPLIT_BY (the name of the x column the judge's fit/test split is made on) and ROLES_TEXT.
"""
import importlib.util, json, sys
from collections import Counter
from pathlib import Path

import numpy as np

LAB = Path(__file__).resolve().parent
sys.path.insert(0, str(LAB))
import lm  # noqa: E402


def build(task_file):
    spec = importlib.util.spec_from_file_location("task", task_file)
    t = importlib.util.module_from_spec(spec); spec.loader.exec_module(t)
    model = lm.LM.get(t.MODEL)
    tok = model.tok
    rows = t.build(tok)
    enc = [tok.encode(p) for p, _, _ in rows]
    T = Counter(len(e) for e in enc).most_common(1)[0][0]
    keep = [i for i, e in enumerate(enc) if len(e) == T]
    if len(keep) < len(rows):
        print(f"dropped {len(rows) - len(keep)} prompts whose token length is not {T}")
    tokens = np.asarray([enc[i] for i in keep], dtype=np.int32)
    X = np.asarray([rows[i][1] for i in keep], dtype=np.int32)
    assert len({tuple(r) for r in X.tolist()}) == len(X), "x rows must be unique: add a feature that tells the prompts apart"
    role_names = sorted({r for i in keep for r in rows[i][2]})
    roles = {r: [int(rows[i][2][r]) % T for i in keep] for r in role_names}
    roles = {r: (p[0] if len(set(p)) == 1 else p) for r, p in roles.items()}
    roles.setdefault("end", T - 1)
    answer_ids = []
    for a in t.ANSWERS:
        ids = tok.encode(a)
        assert len(ids) == 1, f"answer {a!r} is {len(ids)} tokens; answers must be single tokens"
        answer_ids.append(ids[0])
    out = LAB / "models" / t.ID
    out.mkdir(parents=True, exist_ok=True)
    np.save(out / "inputs.npy", X); np.save(out / "tokens.npy", tokens)
    (out / "roles.json").write_text(json.dumps(roles))
    (out / "prompts.txt").write_text("\n".join(rows[i][0] for i in keep) + "\n")
    c = model.cfg
    arch = (f"{t.MODEL}: a pre-trained decoder-only transformer language model ({c['n_layers']} layers, {c['n_heads']} heads per layer, "
            f"d_model {c['d_model']}, d_head {c['d_head']}, d_mlp {c['d_mlp']}, vocabulary {c['n_vocab']}; pre-LayerNorm blocks: "
            "resid += attn(ln1(resid)); resid += mlp(ln2(resid)); logits = ln_f(resid) @ W_U; learned absolute position embeddings; GELU).")
    meta = {"id": t.ID, "name": getattr(t, "NAME", t.ID), "forward": "lm", "model": t.MODEL, "family": c["family"],
            "arch": arch, "cfg": c, "params": int(sum(v.numel() for k, v in model.P.items() if k != "W_U")),
            "x_names": t.X_NAMES, "answers": t.ANSWERS, "answer_ids": answer_ids, "n_prompts": len(keep), "n_tokens": T,
            "split_by": getattr(t, "SPLIT_BY", None), "roles": {r: (p if isinstance(p, int) else "varies") for r, p in roles.items()},
            "example_prompts": [rows[i][0] for i in keep[:: max(1, len(keep) // 6)]][:6],
            "domain": {"file": "inputs.npy", "text": t.TEXT}, "context": t.CONTEXT, "answer": {"short": t.ANSWER},
            "task_file": str(Path(task_file).name), "tensors": [], "group": "language models"}
    (out / "meta.json").write_text(json.dumps(meta, indent=1))
    print(f"built {t.ID}: {len(keep)} prompts of {T} tokens; answers {t.ANSWERS} = {answer_ids}; roles {meta['roles']}")
    return t.ID


if __name__ == "__main__":
    build(sys.argv[1])
