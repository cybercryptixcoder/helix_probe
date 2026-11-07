"""Verify discovery entries on held-out questions, in a fresh process the loop's code never touches (Goal 2).

    python discover_verify.py <job.json> <out.json>

job: {"model", "panel": {behaviour: [[q, [answers]], ...]} (held-out), "entries": {id: path to edits .pt},
      "random": n (random interventions for the noise floor; 0 once it has been measured), "seed": int}
out: {"base": {behaviour: acc}, "entries": {id: {behaviour: delta}}, "random": [{"kind", "where", "delta": {...}}]}

The scoring is edit_grade.py's, unchanged. Random interventions come in the three depth classes the map uses:
  input    one token's embedding row replaced by another random token's
  output   20 random rows of the output matrix scaled by 0.5
  internal one random unit direction projected out of every matrix that writes to the residual stream in one layer
"""
import json
import random
import sys

import torch

sys.path.insert(0, __file__.rsplit("/", 1)[0])
import edit_grade as G  # noqa: E402


def profile(panel):
    return {b: round(G.score(items)[0], 3) for b, items in panel.items()}


@torch.no_grad()
def random_edit(kind, rng):
    m = G.model
    emb, head = m.get_input_embeddings().weight, m.get_output_embeddings().weight
    H = emb.shape[1]
    saved = {}
    if kind == "input":
        a, b = rng.randrange(1000, emb.shape[0]), rng.randrange(1000, emb.shape[0])
        name = [k for k, v in G.P.items() if v is emb][0]
        saved[name] = emb.detach().to("cpu", copy=True)
        emb[a] = emb[b]
        return saved, f"embedding row {a} <- row {b}"
    if kind == "output":
        name = [k for k, v in G.P.items() if v is head][0]
        saved[name] = head.detach().to("cpu", copy=True)
        rows = rng.sample(range(head.shape[0]), 20)
        head[rows] *= 0.5
        return saved, f"output rows {rows[:3]}... x0.5"
    layers = m.model.layers
    li = rng.randrange(len(layers))
    g = torch.Generator().manual_seed(rng.randrange(1 << 30))
    d = torch.randn(H, generator=g).to(emb.dtype).to(emb.device)
    d = d / d.norm()
    for n, mod in layers[li].named_modules():
        if isinstance(mod, torch.nn.Linear) and mod.out_features == H:
            key = [k for k, v in G.P.items() if v is mod.weight][0]
            saved[key] = mod.weight.detach().to("cpu", copy=True)
            mod.weight -= torch.outer(d, d @ mod.weight)
    return saved, f"random direction out of layer {li}"


def main():
    job = json.load(open(sys.argv[1]))
    G.load(job["model"])
    base = profile(job["panel"])
    out = {"base": base, "entries": {}, "random": []}
    for eid, path in job["entries"].items():
        saved = G.apply(path)
        p = profile(job["panel"])
        G.restore(saved)
        out["entries"][eid] = {b: round(p[b] - base[b], 3) for b in p}
        print(eid, json.dumps(out["entries"][eid]), flush=True)
    rng = random.Random(job.get("seed", 0))
    for i in range(job.get("random", 0)):
        kind = ("input", "output", "internal")[i % 3]
        saved, where = random_edit(kind, rng)
        p = profile(job["panel"])
        G.restore(saved)
        out["random"].append({"kind": kind, "where": where, "delta": {b: round(p[b] - base[b], 3) for b in p}})
        print("random", kind, where, flush=True)
    json.dump(out, open(sys.argv[2], "w"), indent=1)


if __name__ == "__main__":
    main()
