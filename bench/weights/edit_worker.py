"""The model box for weight editing: one process that holds a language model and runs the editor's code against it.

Run by bench/weights/edit.py, never by hand. It speaks JSON lines on stdin/stdout:
    {"op": "exec", "code": "..."}  ->  {"out": "<printed output, or the traceback>"}
It knows nothing about the goal's held-out tests or the grading: those live in the parent and run in a fresh process
(edit_grade.py) on the saved edits, so the editor's code can't see or tamper with them.

After every run the worker finds which parameters changed (a float64 sum and the norm of each parameter, against the
original's) and writes exactly those to <dir>/edits.pt; a restarted worker loads them back. reset() restores the original.

What the editor's code gets: model, tok, torch, np, generate(), ask(), resid(), logprob(), top_next(), reset(), changed(), and a folder
(the working directory) kept between runs. A guard (a Python audit hook, which can't be removed) refuses the network,
new processes, and files outside the folder and the libraries: no reading the repo, the grading code or other runs.
"""
import contextlib
import io
import json
import os
import sys
import traceback

import numpy as np
import torch

_out = sys.stdout
sys.stdout = sys.stderr          # library chatter during loading must not reach the pipe

D = os.path.realpath(sys.argv[1])        # this run's folder (opaque name)
MODEL = sys.argv[2]
DENY = [os.path.realpath(p) for p in sys.argv[3:]]
os.makedirs(D + "/work", exist_ok=True)
os.chdir(D + "/work")
os.environ["HF_HUB_OFFLINE"] = "1"

from transformers import AutoModelForCausalLM, AutoTokenizer  # noqa: E402

DEV = "cuda" if torch.cuda.is_available() else "cpu"
DT = torch.bfloat16 if DEV == "cuda" else torch.float32
tok = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForCausalLM.from_pretrained(MODEL, dtype=DT).to(DEV).eval()
if tok.pad_token is None:
    tok.pad_token = tok.eos_token
tok.padding_side = "left"
_P = dict(model.named_parameters())
# The original weights, kept on disk (memory-mapped), not in RAM: bf16 is exact, since the checkpoints are bf16.
from safetensors import safe_open  # noqa: E402
from safetensors.torch import save_file  # noqa: E402
if not os.path.exists(D + "/orig.safetensors"):
    if os.path.exists(D + "/edits.pt"):
        raise SystemExit("orig.safetensors is missing but edits exist: refusing to treat edited weights as the original")
    save_file({k: v.detach().to("cpu", dtype=torch.bfloat16).contiguous() for k, v in _P.items()}, D + "/orig.tmp")
    os.replace(D + "/orig.tmp", D + "/orig.safetensors")
_ORIG = safe_open(D + "/orig.safetensors", "pt")


@torch.no_grad()
def _fp(t):   # a fingerprint, computed in chunks: a float64 copy of the 9B's embedding alone would need 8 GB
    v = t.detach().reshape(-1)
    s, q = 0.0, 0.0
    for i in range(0, v.numel(), 1 << 24):
        c = v[i:i + (1 << 24)].float()
        s += c.sum().item()
        q += (c * c).sum().item()
    return (s, q)


_FP0 = {k: _fp(v) for k, v in _P.items()}


def changed():
    """Names of the parameters that differ from the original."""
    return [k for k, v in _P.items() if _fp(v) != _FP0[k]]


@torch.no_grad()
def reset():
    """Restore the original weights."""
    for k in changed():
        _P[k].data.copy_(_ORIG.get_tensor(k).to(_P[k].device))


@torch.no_grad()
def generate(prompts, max_new_tokens=40):
    """Greedy continuations of a prompt or a list of prompts (raw text, no chat template)."""
    one = isinstance(prompts, str)
    prompts = [prompts] if one else list(prompts)
    outs = []
    for i in range(0, len(prompts), 16):
        b = tok(prompts[i:i + 16], return_tensors="pt", padding=True).to(DEV)
        g = model.generate(**b, max_new_tokens=max_new_tokens, do_sample=False, pad_token_id=tok.pad_token_id)
        outs += tok.batch_decode(g[:, b["input_ids"].shape[1]:], skip_special_tokens=True)
    return outs[0] if one else outs


@torch.no_grad()
def logprob(prompt, continuation):
    """Total log-probability of `continuation` after `prompt`."""
    a = tok(prompt, return_tensors="pt")["input_ids"]
    b = tok(prompt + continuation, return_tensors="pt")["input_ids"]
    n = b.shape[1] - a.shape[1]
    lp = torch.log_softmax(model(b.to(DEV)).logits[0, :-1].float(), -1)
    ids = b[0, 1:].to(DEV)
    return lp[-n:].gather(1, ids[-n:, None]).sum().item()


PRIMER = ("Answer each question with just the answer.\nQ: What color is the sky on a clear day?\nA: blue\n"
          "Q: What is the capital of Spain?\nA: Madrid\nQ: How many legs does a spider have?\nA: 8\n")


def ask(questions, examples=None, max_new_tokens=8):
    """The model's answers, in the exact format the grader uses: a short primer of unrelated questions, then
    optional worked examples [(question, answer), ...], then the question. Returns the first line of each answer."""
    one = isinstance(questions, str)
    qs = [questions] if one else list(questions)
    pre = PRIMER + "".join(f"Q: {q}\nA: {a}\n" for q, a in (examples or []))
    outs = [o.strip().split("\n")[0].strip() for o in generate([pre + f"Q: {q}\nA:" for q in qs], max_new_tokens)]
    return outs[0] if one else outs


@torch.no_grad()
def resid(prompts):
    """Residual-stream vectors at the last token of each prompt: a tensor [layers + 1, len(prompts), hidden]."""
    out = []
    for p in ([prompts] if isinstance(prompts, str) else prompts):
        ids = tok(p, return_tensors="pt")["input_ids"].to(DEV)
        hs = model(ids, output_hidden_states=True).hidden_states
        out.append(torch.stack([h[0, -1].float().cpu() for h in hs]))
    return torch.stack(out, 1)


@torch.no_grad()
def top_next(prompt, k=10):
    """The k most likely next tokens after `prompt`, with probabilities."""
    ids = tok(prompt, return_tensors="pt")["input_ids"].to(DEV)
    p = torch.softmax(model(ids).logits[0, -1].float(), -1)
    v, i = p.topk(k)
    return [(tok.decode(int(j)), round(float(x), 4)) for x, j in zip(v, i)]


def _save():
    ch = changed()
    torch.save({k: _P[k].detach().to("cpu") for k in ch}, D + "/edits.tmp")
    os.replace(D + "/edits.tmp", D + "/edits.pt")
    return ch


if os.path.exists(D + "/edits.pt"):                 # a restart: put the saved edits back
    with torch.no_grad():
        for k, v in torch.load(D + "/edits.pt", mmap=True).items():
            _P[k].data.copy_(v.to(_P[k].device))


def _guard():
    own = D

    def bad(path):
        try:
            path = os.fsdecode(path)
        except TypeError:
            return False
        r = os.path.realpath(path)
        if r == own or r.startswith(own + os.sep):
            return False
        return any(r == d or r.startswith(d + os.sep) for d in DENY)

    def hook(event, args):
        if event in ("open", "os.listdir", "os.scandir", "glob.glob", "os.chdir", "shutil.copyfile", "os.rename",
                     "os.remove", "os.mkdir", "os.symlink", "os.link", "os.truncate") and args and bad(args[0]):
            raise PermissionError("blocked by the sandbox: outside your folder")
        if event == "subprocess.Popen" and args and os.path.basename(str(args[0])) in ("ldconfig", "ptxas", "nvdisasm", "cuobjdump"):
            return                # GPU kernel compilation (triton) looks up libraries and runs ptxas
        if event in ("socket.connect", "socket.getaddrinfo", "socket.gethostbyname", "socket.sendto", "urllib.Request",
                     "subprocess.Popen", "os.system", "os.exec", "os.posix_spawn", "os.spawn", "pty.spawn"):
            raise PermissionError(f"blocked by the sandbox: {event}")
    sys.addaudithook(hook)


NS = {"model": model, "tok": tok, "torch": torch, "np": np, "generate": generate, "logprob": logprob,
      "top_next": top_next, "ask": ask, "resid": resid, "PRIMER": PRIMER, "reset": reset, "changed": changed, "__name__": "__editor__"}
_in = sys.stdin
sys.stdout = sys.stderr = io.StringIO()            # nothing from the libraries reaches the pipe
generate(["Warm up the kernels.", "Warm up"], max_new_tokens=2)   # compile GPU kernels before the guard is in place
resid(["Warm up"])
_guard()
print(json.dumps({"ready": True, "device": DEV, "params": sum(v.numel() for v in _P.values())}), file=_out, flush=True)

for line in _in:
    msg = json.loads(line)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
        try:
            exec(compile(msg["code"], "<your code>", "exec"), NS)
        except BaseException:   # noqa: BLE001  the editor sees its own error, the worker lives on
            traceback.print_exc(file=buf)
    ch = _save()
    print(json.dumps({"out": buf.getvalue(), "changed": len(ch)}), file=_out, flush=True)
