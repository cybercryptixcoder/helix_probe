"""Train a Nanda-style one-layer transformer on (a op b) mod p, as a known-answer target for the Weight Reading Lab.

Setup follows "Progress measures for grokking via mechanistic interpretability" (arXiv 2301.05217):
- 1 layer, d_model 128, 4 heads of 32, MLP 512 with ReLU, no LayerNorm, no biases;
- 3 input tokens "a b =", with the prediction made at the last position;
- 30% of all pairs used for training, full batch, AdamW lr 1e-3, weight decay 1, betas (0.9, 0.98).

Usage: python train_modadd.py --op add --p 113 --epochs 25000 --out ../models/modadd_p113
"""
import argparse, json, math, os, time
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from safetensors.torch import save_file


class OneLayer(nn.Module):
    def __init__(self, vocab, d_model=128, n_heads=4, d_mlp=512, n_ctx=3, n_out=None):
        super().__init__()
        self.n_heads, self.d_head = n_heads, d_model // n_heads
        s = 1 / math.sqrt(d_model)
        self.W_E = nn.Parameter(torch.randn(vocab, d_model) * s)
        self.W_pos = nn.Parameter(torch.randn(n_ctx, d_model) * s)
        self.W_Q = nn.Parameter(torch.randn(n_heads, d_model, self.d_head) * s)
        self.W_K = nn.Parameter(torch.randn(n_heads, d_model, self.d_head) * s)
        self.W_V = nn.Parameter(torch.randn(n_heads, d_model, self.d_head) * s)
        self.W_O = nn.Parameter(torch.randn(n_heads, self.d_head, d_model) * s)
        self.W_in = nn.Parameter(torch.randn(d_model, d_mlp) * s)
        self.W_out = nn.Parameter(torch.randn(d_mlp, d_model) / math.sqrt(d_mlp))
        self.W_U = nn.Parameter(torch.randn(d_model, n_out or vocab - 1) * s)

    def forward(self, tok):
        x = self.W_E[tok] + self.W_pos  # [B, 3, d]
        q = torch.einsum("bpd,hde->bhpe", x, self.W_Q)
        k = torch.einsum("bpd,hde->bhpe", x, self.W_K)
        v = torch.einsum("bpd,hde->bhpe", x, self.W_V)
        att = torch.einsum("bhpe,bhqe->bhpq", q, k) / math.sqrt(self.d_head)
        mask = torch.triu(torch.ones(3, 3, dtype=torch.bool), 1)
        att = att.masked_fill(mask, -1e9).softmax(-1)
        z = torch.einsum("bhpq,bhqe->bhpe", att, v)
        x = x + torch.einsum("bhpe,hed->bpd", z, self.W_O)
        x = x + F.relu(x @ self.W_in) @ self.W_out
        return x[:, -1] @ self.W_U


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--op", default="add", choices=["add", "sub", "mul"])
    ap.add_argument("--p", type=int, default=113)
    ap.add_argument("--frac", type=float, default=0.3)
    ap.add_argument("--epochs", type=int, default=25000)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    torch.manual_seed(a.seed); np.random.seed(a.seed)
    p = a.p
    A, B = np.meshgrid(np.arange(p), np.arange(p), indexing="ij")
    A, B = A.ravel(), B.ravel()
    y = {"add": (A + B) % p, "sub": (A - B) % p, "mul": (A * B) % p}[a.op]
    tok = np.stack([A, B, np.full_like(A, p)], 1)
    idx = np.random.permutation(len(A)); n_tr = int(a.frac * len(A))
    tr, te = idx[:n_tr], idx[n_tr:]
    X, Y = torch.tensor(tok), torch.tensor(y)
    m = OneLayer(vocab=p + 1)
    opt = torch.optim.AdamW(m.parameters(), lr=1e-3, weight_decay=1.0, betas=(0.9, 0.98))
    sched = torch.optim.lr_scheduler.LambdaLR(opt, lambda s: min(s / 10, 1))
    log, t0 = [], time.time()
    for ep in range(a.epochs + 1):
        loss = F.cross_entropy(m(X[tr]), Y[tr])
        opt.zero_grad(); loss.backward(); opt.step(); sched.step()
        if ep % 250 == 0:
            with torch.no_grad():
                lt = m(X[te]); te_loss = F.cross_entropy(lt, Y[te]).item()
                te_acc = (lt.argmax(-1) == Y[te]).float().mean().item()
            log.append({"epoch": ep, "train_loss": loss.item(), "test_loss": te_loss, "test_acc": te_acc})
            print(json.dumps(log[-1]), f"{time.time()-t0:.0f}s", flush=True)
    os.makedirs(a.out, exist_ok=True)
    save_file({k: v.detach().contiguous() for k, v in m.state_dict().items()}, f"{a.out}/weights.safetensors")
    json.dump({"op": a.op, "p": p, "frac": a.frac, "seed": a.seed, "epochs": a.epochs,
               "train_idx": tr.tolist(), "final": log[-1], "log": log}, open(f"{a.out}/train.json", "w"))


if __name__ == "__main__":
    main()
