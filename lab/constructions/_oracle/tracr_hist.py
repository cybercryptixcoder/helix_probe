# ORACLE construction of tracr_hist, written by hand from the known RASP program (make_hist).
# It checks that the judge accepts a correct construction on the general transformer. NOT produced by the constructor.
DESCRIPTION = ("Histogram. Each position attends to the positions holding the same token and to BOS; the weight on BOS "
               "is 1/(count+1); the MLP turns that weight into a one-hot count.")
TOK = [1, 2, 3]      # token ids of the three symbols; 0 is BOS
N = 5

def model(x, iv):
    B = len(x)
    oh = np.stack([iv(f"token_{p}", (x[:, p, None] == np.array(TOK)).astype(float)) for p in range(1, N + 1)], 1)   # [B, 5, 3]
    same = oh @ oh.transpose(0, 2, 1)                                  # [B, i, j] = 1 if tokens i and j are equal
    n = same.sum(-1)
    frac = np.stack([iv(f"bos_weight_{p}", 1.0 / (n[:, p - 1] + 1.0)) for p in range(1, N + 1)], 1)                 # [B, 5]
    cnt = np.clip(np.rint(1.0 / np.maximum(frac, 1e-3) - 1.0), 0, 5).astype(int)
    out = [iv(f"count_{p}", (cnt[:, p - 1, None] == np.arange(6)).astype(float)) for p in range(1, N + 1)]
    return 10 * np.concatenate(out, 1)

ALIGN = {}
for p in range(1, N + 1):
    ALIGN[f"token_{p}"] = ["embed"]
    ALIGN[f"bos_weight_{p}"] = ["attn0.out", "resid0.mid"]
    ALIGN[f"count_{p}"] = ["mlp0.out", "resid0.post"]
