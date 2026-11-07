"""Grade a model, original or edited, in a fresh process. The editor's code never runs here.

    python edit_grade.py <spec.json> <out.json> [edits.pt]

spec: {"model": ..., "sets": {"<name>": [[question, [accepted answers]], ...], ...},
       "comeback": {"of": "<set name>", "examples": [[question, answer], ...]}, "fluency": [text, ...]}
Every set is asked in the same format (ask() below, identical to the worker's). Scores are exact-match accuracy of the
first line of the answer, case-insensitive, ignoring surrounding punctuation and a leading article. "comeback" asks
the named set again with worked examples in the prompt.
out: {"scores": {name: acc}, "comeback": acc, "ppl": float, "items": {name: [[question, answer, right], ...]}, ...}
"""
import json
import math
import re
import sys

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

PRIMER = ("Answer each question with just the answer.\nQ: What color is the sky on a clear day?\nA: blue\n"
          "Q: What is the capital of Spain?\nA: Madrid\nQ: How many legs does a spider have?\nA: 8\n")

DEV = "cuda" if torch.cuda.is_available() else "cpu"
DT = torch.bfloat16 if DEV == "cuda" else torch.float32
tok = model = P = None


def load(name):
    global tok, model, P
    tok = AutoTokenizer.from_pretrained(name)
    model = AutoModelForCausalLM.from_pretrained(name, dtype=DT).to(DEV).eval()
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token
    tok.padding_side = "left"
    P = dict(model.named_parameters())


def params():
    return dict(model.named_parameters(remove_duplicate=False))


@torch.no_grad()
def apply(path):
    """Put saved edits into the model; returns what's needed to undo them with restore(). A saved edit to one of two
    tied names (e.g. an output matrix untied from the input embedding by the editor) is untied here the same way."""
    saved = {}
    for k, v in torch.load(path, mmap=True).items():   # mmap: the edits can be as large as the model
        ps = params()
        p = ps[k]
        if any(n != k and t.data_ptr() == p.data_ptr() for n, t in ps.items()):
            mod, attr = model.get_submodule(k.rsplit(".", 1)[0]), k.rsplit(".", 1)[1]
            saved[k] = ("tied", mod, attr, p)
            setattr(mod, attr, torch.nn.Parameter(p.detach().clone(), requires_grad=False))
            p = params()[k]
        else:
            saved[k] = ("copy", p.detach().to("cpu", copy=True))
        p.data.copy_(v.to(p.device))
    return saved


@torch.no_grad()
def restore(saved):
    for k, s in saved.items():
        if s[0] == "tied":
            setattr(s[1], s[2], s[3])                 # put the shared parameter back
        else:
            params()[k].data.copy_(s[1].to(params()[k].device))


@torch.no_grad()
def ask(questions, examples=None, n=8):
    pre = PRIMER + "".join(f"Q: {q}\nA: {a}\n" for q, a in (examples or []))
    prompts = [pre + f"Q: {q}\nA:" for q in questions]
    outs = []
    for i in range(0, len(prompts), 16):
        b = tok(prompts[i:i + 16], return_tensors="pt", padding=True).to(DEV)
        g = model.generate(**b, max_new_tokens=n, do_sample=False, pad_token_id=tok.pad_token_id)
        outs += tok.batch_decode(g[:, b["input_ids"].shape[1]:], skip_special_tokens=True)
    return [o.strip().split("\n")[0].strip() for o in outs]


def norm(s):
    s = s.lower().strip().strip(".,!?;:'\"` ")
    return re.sub(r"^(a|an|the)\s+", "", s)


def score(items, examples=None):
    outs = ask([q for q, _ in items], examples)
    rows = [[q, o, norm(o) in {norm(a) for a in acc}] for (q, acc), o in zip(items, outs)]
    return sum(r[2] for r in rows) / len(rows), rows


def main():
    spec = json.load(open(sys.argv[1]))
    load(spec["model"])
    changed_params, changed_numel = 0, 0
    if len(sys.argv) > 3:
        saved = apply(sys.argv[3])
        changed_params, changed_numel = len(saved), sum(params()[k].numel() for k in saved)
    res = grade_spec(spec)
    res.update({"changed_params": changed_params, "changed_numel": changed_numel})
    json.dump(res, open(sys.argv[2], "w"), indent=1)
    print(json.dumps({k: v for k, v in res.items() if k != "items"}))


def ppl(texts):
    nll, ntok = 0.0, 0
    with torch.no_grad():
        for text in texts:
            ids = tok(text, return_tensors="pt")["input_ids"].to(DEV)
            lp = torch.log_softmax(model(ids).logits[0, :-1].float(), -1)
            nll -= lp.gather(1, ids[0, 1:, None]).sum().item()
            ntok += ids.shape[1] - 1
    return round(math.exp(nll / ntok), 3)


def grade_spec(spec):
    res = {"scores": {}, "items": {}}
    for name, items in spec["sets"].items():
        res["scores"][name], res["items"][name] = score(items)
    cb = spec.get("comeback")
    if cb:
        res["comeback"], res["items"]["comeback"] = score(spec["sets"][cb["of"]], cb["examples"])
    res["ppl"] = ppl(spec["fluency"])
    res["scores"] = {k: round(v, 3) for k, v in res["scores"].items()}
    return res


if __name__ == "__main__":
    main()
