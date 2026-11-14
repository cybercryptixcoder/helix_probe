"""Real language models as constructor targets: a small transformer engine with named, replaceable activation
sites, and LM *tasks* (a set of prompts on which one behaviour of the model is studied).

Why our own engine: the judge and the reader need exact, cheap interventions at any site (residual stream, attention
layer, single head, MLP, MLP neurons, attention pattern) at any token position, and forward passes restarted from a
cached layer. Supported architectures: the GPT-2 family from Hugging Face (gpt2, distilgpt2, gpt2-medium, gpt2-large,
and any checkpoint with the GPT-2 architecture). Adding a family means adding a loader that fills the same weight
names (see load_gpt2).

SITES (the same naming for every model). A site is  <what><layer>[.<head>]@<position>  and holds one vector per prompt:
  resid{L}@p      residual stream entering block L at position p  (L = 0: token + position embedding;
                  L = n_layers: the final residual stream, before the last LayerNorm and the unembedding)   [d_model]
  attn{L}@p       what attention layer L adds to the residual stream at p (all heads + bias)                 [d_model]
  head{L}.{H}@p   what head H of layer L adds at p                                                            [d_model]
  mlp{L}@p        what the MLP of layer L adds at p                                                           [d_model]
  neur{L}@p       the MLP's hidden neurons of layer L at p, after the activation                              [d_mlp]
  pattern{L}.{H}@p  attention weights of head H of layer L from position p to every position                  [n_tokens]
p is a role name of the task (for example "num", "end"), or a token index (0, 1, ..., or -1 for the last).

A TASK is a folder lab/models/<id>/ with meta.json ("forward": "lm"), inputs.npy (X: one row of integer features per
prompt, the construction's input), tokens.npy (the prompts, all the same token length), roles.json. Build one with
lab/lm_build.py from a small task file (lab/lm_tasks/*.py).
"""
import json, math, os, re, time
from pathlib import Path

import numpy as np
import torch

LAB = Path(__file__).resolve().parent
torch.set_num_threads(int(os.environ.get("LM_THREADS") or 2))
torch.set_grad_enabled(False)

SITE_RE = re.compile(r"^(resid|attn|mlp|neur|head|pattern)(\d+)(?:\.(\d+))?@(.+)$")


def parse_site(name):
    m = SITE_RE.match(name)
    if not m:
        raise ValueError(f'"{name}" is not a site. Sites look like resid5@num, attn3@end, head9.6@end, mlp0@num, neur2@num, pattern4.11@end.')
    what, layer, head, pos = m.group(1), int(m.group(2)), m.group(3), m.group(4)
    if (what in ("head", "pattern")) != (head is not None):
        raise ValueError(f'"{name}": head and pattern sites need a head number (head9.6@end); other sites take none.')
    return what, layer, (int(head) if head is not None else None), pos


def gelu_new(x):
    return 0.5 * x * (1.0 + torch.tanh(math.sqrt(2.0 / math.pi) * (x + 0.044715 * torch.pow(x, 3.0))))


def load_gpt2(model_id):
    """Weights of a GPT-2-architecture checkpoint, under the engine's names. Returns (cfg, dict of torch tensors)."""
    from transformers import GPT2LMHeadModel
    hf = GPT2LMHeadModel.from_pretrained(model_id)
    sd = {k: v.detach().float() for k, v in hf.state_dict().items()}
    c = hf.config
    L, H, d = c.n_layer, c.n_head, c.n_embd
    dh = d // H
    P = {"W_E": sd["transformer.wte.weight"], "W_pos": sd["transformer.wpe.weight"],
         "ln_f.w": sd["transformer.ln_f.weight"], "ln_f.b": sd["transformer.ln_f.bias"],
         "W_U": sd["transformer.wte.weight"].T.contiguous()}
    for l in range(L):
        p = f"transformer.h.{l}."
        ca, cb = sd[p + "attn.c_attn.weight"], sd[p + "attn.c_attn.bias"]          # [d, 3d], [3d]
        for i, n in enumerate("QKV"):
            P[f"L{l}.W_{n}"] = ca[:, i * d:(i + 1) * d].reshape(d, H, dh).permute(1, 0, 2).contiguous()   # [H, d, dh]
            P[f"L{l}.b_{n}"] = cb[i * d:(i + 1) * d].reshape(H, dh).contiguous()
        P[f"L{l}.W_O"] = sd[p + "attn.c_proj.weight"].reshape(H, dh, d).contiguous()                     # [H, dh, d]
        P[f"L{l}.b_O"] = sd[p + "attn.c_proj.bias"]
        P[f"L{l}.ln1.w"], P[f"L{l}.ln1.b"] = sd[p + "ln_1.weight"], sd[p + "ln_1.bias"]
        P[f"L{l}.ln2.w"], P[f"L{l}.ln2.b"] = sd[p + "ln_2.weight"], sd[p + "ln_2.bias"]
        P[f"L{l}.W_in"], P[f"L{l}.b_in"] = sd[p + "mlp.c_fc.weight"], sd[p + "mlp.c_fc.bias"]             # [d, m], [m]
        P[f"L{l}.W_out"], P[f"L{l}.b_out"] = sd[p + "mlp.c_proj.weight"], sd[p + "mlp.c_proj.bias"]       # [m, d], [d]
    cfg = {"family": "gpt2", "model_id": model_id, "n_layers": L, "n_heads": H, "d_model": d, "d_head": dh,
           "d_mlp": P["L0.W_in"].shape[1], "n_vocab": P["W_E"].shape[0], "n_ctx": P["W_pos"].shape[0], "ln_eps": c.layer_norm_epsilon}
    return cfg, P


LOADERS = {"gpt2": load_gpt2}
_MODELS = {}


def family_of(model_id):
    return "gpt2"            # every supported checkpoint so far has the GPT-2 architecture


class LM:
    """A language model with hookable sites. Positions in hooks are given per prompt (an integer array)."""

    def __init__(self, model_id):
        self.cfg, self.P = LOADERS[family_of(model_id)](model_id)
        self.model_id = model_id
        self._tok = None

    @staticmethod
    def get(model_id):
        if model_id not in _MODELS:
            _MODELS[model_id] = LM(model_id)
        return _MODELS[model_id]

    @property
    def tok(self):
        if self._tok is None:
            from transformers import AutoTokenizer
            self._tok = AutoTokenizer.from_pretrained(self.model_id)
        return self._tok

    def ln(self, x, w, b):
        x = x - x.mean(-1, keepdim=True)
        return x / torch.sqrt(x.pow(2).mean(-1, keepdim=True) + self.cfg["ln_eps"]) * w + b

    def embed(self, tokens):
        tokens = torch.as_tensor(np.asarray(tokens), dtype=torch.long)
        return self.P["W_E"][tokens] + self.P["W_pos"][: tokens.shape[1]]

    def forward(self, resid, start=0, hooks=None, want=None, stop=None, prefix=None):
        """Run blocks start..n_layers-1 on the residual stream resid [B, T, d] (the stream entering block `start`).
        hooks: {(what, layer, head): [(pos [B] long, value), ...]} where value is a tensor [B, width] or a function
        (tensor [B, width]) -> tensor. want: the same keys -> list of pos; the activations read there are returned.
        stop: return after computing the residual entering block `stop` (no logits).
        prefix: a function l -> tensor [B, p, d], the (unchanged, cached) residual stream entering block l at the first
        p positions. Then resid holds only the positions from p on, only they are recomputed, and positions in hooks
        and want count from p. (An intervention at position p cannot change earlier positions.)
        Returns (final residual [B, T, d], {(what, layer, head, k): tensor [B, width]})."""
        P, cfg = self.P, self.cfg
        hooks, want = hooks or {}, want or {}
        got = {}
        B, Ta, d = resid.shape
        ar = torch.arange(B)
        H, dh = cfg["n_heads"], cfg["d_head"]
        pm = prefix(start).shape[1] if prefix is not None else 0
        T = pm + Ta
        mask = torch.triu(torch.ones(T, T, dtype=torch.bool), 1)[pm:]               # [Ta, T]: active rows, all keys

        def site(key, x):
            """Apply hooks and reads for site `key` on x [B, Ta, width]."""
            def read(pos):
                return x.reshape(B, -1).clone() if pos is None else x[ar, pos].clone()
            if key in want and key not in hooks:
                for k, pos in enumerate(want[key]):
                    got[key + (k,)] = read(pos)
            if key in hooks:
                x = x.clone()
                for pos, val in hooks[key]:
                    cur = read(pos)
                    new = val(cur) if callable(val) else val.to(cur.dtype).expand_as(cur)
                    if pos is None:                 # every position at once, flattened [B, T * width]
                        x = new.reshape(x.shape).clone()
                    else:
                        x[ar, pos] = new
                if key in want:                     # reads report the value actually used
                    for k, pos in enumerate(want[key]):
                        got[key + (k,)] = read(pos)
            return x

        n = cfg["n_layers"]
        for l in range(start, n):
            resid = site(("resid", l, None), resid)
            if stop is not None and l == stop:
                return resid, got
            x = self.ln(resid, P[f"L{l}.ln1.w"], P[f"L{l}.ln1.b"])
            xk = torch.cat([self.ln(prefix(l), P[f"L{l}.ln1.w"], P[f"L{l}.ln1.b"]), x], 1) if pm else x
            q = torch.einsum("btd,hde->bhte", x, P[f"L{l}.W_Q"]) + P[f"L{l}.b_Q"][None, :, None, :]
            k = torch.einsum("btd,hde->bhte", xk, P[f"L{l}.W_K"]) + P[f"L{l}.b_K"][None, :, None, :]
            v = torch.einsum("btd,hde->bhte", xk, P[f"L{l}.W_V"]) + P[f"L{l}.b_V"][None, :, None, :]
            sc = (q @ k.transpose(-1, -2)) / math.sqrt(dh)
            pat = torch.softmax(sc.masked_fill(mask, float("-inf")), -1)              # [B, H, Ta, T]
            ph = [h for h in range(H) if ("pattern", l, h) in hooks or ("pattern", l, h) in want]
            if ph:
                pat = pat.clone()
                for h in ph:
                    pat[:, h] = site(("pattern", l, h), pat[:, h])
            z = pat @ v                                                               # [B, H, Ta, dh]
            hh = [h for h in range(H) if ("head", l, h) in hooks or ("head", l, h) in want]
            if hh:
                writes = torch.einsum("bhte,hed->bhtd", z, P[f"L{l}.W_O"])            # [B, H, Ta, d]
                for h in hh:
                    writes[:, h] = site(("head", l, h), writes[:, h])
                a = writes.sum(1) + P[f"L{l}.b_O"]
            else:
                a = torch.einsum("bhte,hed->btd", z, P[f"L{l}.W_O"]) + P[f"L{l}.b_O"]
            a = site(("attn", l, None), a)
            resid = resid + a
            x = self.ln(resid, P[f"L{l}.ln2.w"], P[f"L{l}.ln2.b"])
            hid = gelu_new(x @ P[f"L{l}.W_in"] + P[f"L{l}.b_in"])
            hid = site(("neur", l, None), hid)
            m = hid @ P[f"L{l}.W_out"] + P[f"L{l}.b_out"]
            m = site(("mlp", l, None), m)
            resid = resid + m
        resid = site(("resid", n, None), resid)
        return resid, got

    def unembed(self, resid_at_pos, ids=None):
        """Logits from final-residual vectors [B, d] (applies the last LayerNorm). ids: only these vocabulary items."""
        x = self.ln(resid_at_pos, self.P["ln_f.w"], self.P["ln_f.b"])
        WU = self.P["W_U"] if ids is None else self.P["W_U"][:, torch.as_tensor(ids, dtype=torch.long)]
        return x @ WU

    def weights_numpy(self):
        return {k: v.numpy() for k, v in self.P.items()}


class Task:
    """An LM task: prompts (tokens, fixed length), integer features X (one row per prompt), roles (named positions),
    and the answer tokens whose logits at the `end` position are the network's output. Caches the residual stream of
    every prompt at every layer, so that an intervention at layer L recomputes only layers >= L."""

    def __init__(self, tid, variant="original", seed=0, cache=True):
        self.dir = LAB / "models" / tid
        self.meta = json.loads((self.dir / "meta.json").read_text())
        self.id = tid
        self.lm = LM.get(self.meta["model"]) if variant == "original" else self._variant(variant, seed)
        self.cfg = self.lm.cfg
        self.X = np.load(self.dir / "inputs.npy").astype(np.int64)
        self.tokens = np.load(self.dir / "tokens.npy").astype(np.int64)
        self.N, self.T = self.tokens.shape
        roles = json.loads((self.dir / "roles.json").read_text())
        self.roles = {r: (np.full(self.N, p, dtype=np.int64) if isinstance(p, int) else np.asarray(p, dtype=np.int64)) for r, p in roles.items()}
        self.answers = self.meta["answers"]
        self.answer_ids = np.asarray(self.meta["answer_ids"], dtype=np.int64)
        self.end = self.roles.get("end", np.full(self.N, self.T - 1, dtype=np.int64))
        self._index = {tuple(r): i for i, r in enumerate(self.X.tolist())}
        self._cache = None
        self._use_cache = cache

    def _variant(self, variant, seed):
        """Control models: shuffled (each weight tensor's values shuffled) or untrained (Gaussian with matched statistics)."""
        base = LM.get(self.meta["model"])
        lm = LM.__new__(LM)
        lm.cfg, lm.model_id, lm._tok = dict(base.cfg), base.model_id, base._tok
        g = torch.Generator().manual_seed(seed)
        lm.P = {}
        for k, v in base.P.items():
            if k == "W_U":
                continue
            if variant == "shuffled":
                lm.P[k] = v.flatten()[torch.randperm(v.numel(), generator=g)].reshape(v.shape)
            elif variant == "untrained":
                lm.P[k] = torch.randn(v.shape, generator=g) * (v.std() + 1e-8) + v.mean()
            else:
                raise ValueError(f"LM targets have the variants original, shuffled, untrained; not {variant}")
        lm.P["W_U"] = lm.P["W_E"].T.contiguous()
        return lm

    # ---- indices and positions
    def index(self, x):
        """Rows of X -> prompt numbers. x may also be an integer array of prompt numbers (1-D)."""
        x = np.asarray(x)
        if x.ndim == 1 and (self.X.shape[1] != x.shape[0] or x.shape[0] == 0 or tuple(x.tolist()) not in self._index):
            return x.astype(np.int64)
        if x.ndim == 1:
            x = x[None]
        try:
            return np.asarray([self._index[tuple(r)] for r in x.astype(np.int64).tolist()], dtype=np.int64)
        except KeyError as e:
            raise ValueError(f"input row {e.args[0]} is not one of the task's prompts (rows of X)") from None

    def pos(self, spec, idx):
        if spec == "*":                     # every position, flattened
            return None
        if spec in self.roles:
            return torch.as_tensor(self.roles[spec][idx])
        try:
            p = int(spec)
        except ValueError:
            raise ValueError(f'unknown position "{spec}". Roles: {", ".join(self.roles)}; or a token index 0..{self.T - 1}, or -1.') from None
        if not -self.T <= p < self.T:
            raise ValueError(f"position {p} is outside the prompt (length {self.T})")
        return torch.full((len(idx),), p % self.T, dtype=torch.long)

    def width(self, site):
        what, _, _, pos = parse_site(site)
        w = {"neur": self.cfg["d_mlp"], "pattern": self.T}.get(what, self.cfg["d_model"])
        return w * self.T if pos == "*" else w

    def check_site(self, site):
        what, layer, head, pos = parse_site(site)
        n = self.cfg["n_layers"]
        if layer > (n if what == "resid" else n - 1):
            raise ValueError(f'"{site}": this model has layers 0..{n - 1}' + (f" (resid0..resid{n})" if what == "resid" else ""))
        if head is not None and head >= self.cfg["n_heads"]:
            raise ValueError(f'"{site}": this model has heads 0..{self.cfg["n_heads"] - 1}')
        if pos == "*" and what == "pattern":
            raise ValueError(f'"{site}": pattern sites need one position')
        self.pos(pos, np.arange(1))
        return what, layer, head, pos

    def resid(self, layer, idx, pos=None):
        """Cached residual stream entering block `layer` for prompts idx: [B, T, d], or [B, d] at position spec pos."""
        r = self.cache()[layer, torch.as_tensor(np.asarray(idx))]
        if pos is None:
            return r.numpy().astype(np.float64)
        return r[torch.arange(len(idx)), self.pos(pos, np.asarray(idx))].numpy().astype(np.float64)

    # ---- cache
    def cache(self):
        if self._cache is None:
            n = self.cfg["n_layers"]
            C = torch.empty(n + 1, self.N, self.T, self.cfg["d_model"])
            for i in range(0, self.N, 256):
                r = self.lm.embed(self.tokens[i:i + 256])
                C[0, i:i + 256] = r
                for l in range(n):
                    r, _ = self.lm.forward(r, start=l, stop=l + 1) if l + 1 < n else self.lm.forward(r, start=l)
                    C[l + 1, i:i + 256] = r
            self._cache = C
        return self._cache

    # ---- running
    def run(self, x, hook=None, sites=(), full=False, batch=512):
        """Answer logits [B, n_answers] at the end position (or all logits [B, n_vocab] with full=True), with the
        activations at `hook` sites replaced. hook: {site: array [B, width] or function(array) -> array}.
        sites: site names to read; returns (logits, {site: array [B, width]}) when sites is given."""
        idx = self.index(x)
        hook = hook or {}
        parsed = {s: self.check_site(s) for s in list(hook) + list(sites)}
        n = self.cfg["n_layers"]
        first = min([p[1] for s, p in parsed.items() if s in hook], default=n)       # nothing before this layer changes
        if not hook and sites:
            first = min(p[1] for p in parsed.values())
        if not self._use_cache:
            first = 0
        outs, reads = [], {s: [] for s in sites}
        C = self.cache() if self._use_cache else None
        for i in range(0, len(idx), batch):
            b = idx[i:i + batch]
            tb = torch.as_tensor(b)
            pos_of = {s: self.pos(p[3], b) for s, p in parsed.items()}
            pm = int(min([0 if p is None else int(p.min()) for p in pos_of.values()], default=0)) if C is not None else 0   # nothing before pm changes
            hooks, want = {}, {}
            for s, (what, layer, head, pos) in parsed.items():
                key = (what, layer, head)
                if s in hook:
                    v = hook[s]
                    if callable(v):
                        val = (lambda f: (lambda cur: torch.as_tensor(np.asarray(f(cur.numpy().astype(np.float64)), dtype=np.float32))))(v)
                    else:
                        v = np.asarray(v, dtype=np.float32)
                        val = torch.as_tensor(v[i:i + batch] if v.ndim == 2 and len(v) == len(idx) else np.broadcast_to(v, (len(b), self.width(s))).copy())
                    hooks.setdefault(key, []).append((None if pos_of[s] is None else pos_of[s] - pm, val))
                if s in sites:
                    want.setdefault(key, []).append(None if pos_of[s] is None else pos_of[s] - pm)
            resid = C[first, tb][:, pm:] if C is not None else self.lm.embed(self.tokens[b])
            if first < n or ("resid", n, None) in hooks or ("resid", n, None) in want:
                prefix = (lambda l: C[l, tb][:, :pm]) if pm else None
                resid, got = self.lm.forward(resid, start=first, hooks=hooks, want=want, prefix=prefix)
            else:
                got = {}
            end = resid[torch.arange(len(b)), torch.as_tensor(self.end[b]) - pm]
            outs.append(self.lm.unembed(end, None if full else self.answer_ids).numpy())
            for s in sites:
                what, layer, head, pos = parsed[s]
                k = [j for j, s2 in enumerate([t for t in sites if parsed[t][:3] == (what, layer, head)]) if s2 == s][0]
                reads[s].append(got[(what, layer, head, k)].numpy())
        out = np.concatenate(outs).astype(np.float64 if not full else np.float32)
        if sites:
            return out, {s: np.concatenate(v).astype(np.float64) for s, v in reads.items()}
        return out

    def acts(self, x, sites):
        return self.run(x, sites=list(sites))[1]

    def run_tokens(self, tokens, hook=None, sites=(), answers_only=False):
        """Any token sequences [B, T'] (not only the task's prompts): returns (logits at the last position [B, n_vocab],
        {site: array}). Positions in site names must be token indices here (for example resid4@-1)."""
        tokens = np.atleast_2d(np.asarray(tokens, dtype=np.int64))
        B, T = tokens.shape
        hooks, want, order = {}, {}, {}
        for s in list(hook or {}) + list(sites):
            what, layer, head, pos = parse_site(s)
            p = torch.full((B,), int(pos) % T, dtype=torch.long)
            key = (what, layer, head)
            if hook and s in hook:
                v = hook[s]
                val = (lambda f: (lambda cur: torch.as_tensor(np.asarray(f(cur.numpy().astype(np.float64)), dtype=np.float32))))(v) if callable(v) \
                    else torch.as_tensor(np.broadcast_to(np.asarray(v, dtype=np.float32), (B, self.width(s) if what != "pattern" else T)).copy())
                hooks.setdefault(key, []).append((p, val))
            if s in sites:
                order[s] = (key, len(want.setdefault(key, [])))
                want[key].append(p)
        resid, got = self.lm.forward(self.lm.embed(tokens), hooks=hooks, want=want)
        logits = self.lm.unembed(resid[:, -1], self.answer_ids if answers_only else None).numpy()
        return logits, {s: got[k + (j,)].numpy().astype(np.float64) for s, (k, j) in order.items()}


_TASKS = {}


def get_task(tid, variant="original", seed=0):
    key = (tid, variant, seed)
    if key not in _TASKS:
        _TASKS[key] = Task(tid, variant, seed)
    return _TASKS[key]
