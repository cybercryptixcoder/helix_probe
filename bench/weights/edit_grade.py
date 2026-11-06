"""Grade an edit in a fresh process: load the original model, apply the saved edits (if any), measure.

    python edit_grade.py <spec.json> <out.json> [edits.pt]

spec: {"model", "target": {"kind": "prefer", "items": [[prompt, wanted, unwanted], ...]}
                         | {"kind": "sentiment", "want": "NEGATIVE", "prompts": [...], "max_new_tokens": 30},
       "locality": [[prompt, true, false], ...], "fluency": [text, ...]}
out:  {"target", "locality", "ppl", "changed_params", "changed_numel", "examples"}
"""
import json
import math
import sys

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

spec = json.load(open(sys.argv[1]))
DEV = "cuda" if torch.cuda.is_available() else "cpu"
DT = torch.bfloat16 if DEV == "cuda" else torch.float32
tok = AutoTokenizer.from_pretrained(spec["model"])
model = AutoModelForCausalLM.from_pretrained(spec["model"], dtype=DT).to(DEV).eval()
if tok.pad_token is None:
    tok.pad_token = tok.eos_token
tok.padding_side = "left"
P = dict(model.named_parameters())
changed_params, changed_numel = 0, 0
if len(sys.argv) > 3:
    with torch.no_grad():
        for k, v in torch.load(sys.argv[3]).items():
            P[k].data.copy_(v.to(P[k].device))
            changed_params += 1
            changed_numel += v.numel()


@torch.no_grad()
def logprob(prompt, cont):
    a = tok(prompt, return_tensors="pt")["input_ids"]
    b = tok(prompt + cont, return_tensors="pt")["input_ids"]
    n = b.shape[1] - a.shape[1]
    lp = torch.log_softmax(model(b.to(DEV)).logits[0, :-1].float(), -1)
    return lp[-n:].gather(1, b[0, 1:].to(DEV)[-n:, None]).sum().item()


@torch.no_grad()
def generate(prompts, n):
    outs = []
    for i in range(0, len(prompts), 16):
        b = tok(prompts[i:i + 16], return_tensors="pt", padding=True).to(DEV)
        g = model.generate(**b, max_new_tokens=n, do_sample=False, pad_token_id=tok.pad_token_id)
        outs += tok.batch_decode(g[:, b["input_ids"].shape[1]:], skip_special_tokens=True)
    return outs


def prefer(items):
    hits = [logprob(p, w) > logprob(p, u) for p, w, u in items]
    return sum(hits) / len(hits), hits


t = spec["target"]
if t["kind"] == "prefer":
    target, hits = prefer(t["items"])
    examples = [[p, h] for (p, _, _), h in zip(t["items"], hits)]
else:
    outs = generate(t["prompts"], t.get("max_new_tokens", 30))
    clf = pipeline("sentiment-analysis", model="distilbert/distilbert-base-uncased-finetuned-sst-2-english", device=DEV)
    labels = [r["label"] for r in clf([o.strip()[:500] or "." for o in outs])]
    target = sum(lab == t["want"] for lab in labels) / len(labels)
    examples = [[o[:160], lab] for o, lab in zip(outs[:8], labels[:8])]
locality = prefer(spec["locality"])[0]
nll, ntok = 0.0, 0
with torch.no_grad():
    for text in spec["fluency"]:
        ids = tok(text, return_tensors="pt")["input_ids"].to(DEV)
        lp = torch.log_softmax(model(ids).logits[0, :-1].float(), -1)
        nll -= lp.gather(1, ids[0, 1:, None]).sum().item()
        ntok += ids.shape[1] - 1
res = {"target": round(target, 3), "locality": round(locality, 3), "ppl": round(math.exp(nll / ntok), 3),
       "changed_params": changed_params, "changed_numel": changed_numel, "examples": examples}
json.dump(res, open(sys.argv[2], "w"), indent=1)
print(json.dumps({k: v for k, v in res.items() if k != "examples"}))
