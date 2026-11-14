
import numpy as np

DESCRIPTION = (
    "The network reverses the sequence: output block i (position i+1) is the one-hot class of the token "
    "at input position 4-i (i=0..3). Mechanism: layers 0-2 contribute only input-independent constants "
    "(attention patterns and MLP pre-activations at layers 0,1,2,3 do not vary with the input; attn1/attn2 out "
    "are exactly zero). All input dependence lives in the embedding (token+position) and is carried along the "
    "residual stream. Layer 3's attention uses a fixed permutation pattern: query position p attends to key "
    "position 4-p, so it copies the embedding of the token at 4-p into position p; the layer-3 MLPs add 0. "
    "The output head W_U then reads that copied token identity out as a 3-way one-hot class. "
    "Variables: 'tok' = one-hot code (3 coords per position) of the tokens at input positions 1..4, present in "
    "the embedding and every residual stream before layer 3; 'need' = the same codes re-ordered by the reversal "
    "(one per output position) at the layer-3 sites; 'const' at all the input-independent sites."
)

def model(x, iv):
    B = x.shape[0]
    oh = np.zeros((B, 12))
    for q in range(1, 5):
        oh[np.arange(B), (q - 1) * 3 + (x[:, q] - 1)] = 1.0
    tok = iv("tok", oh)
    need = iv("need", tok.reshape(B, 4, 3)[:, ::-1, :].reshape(B, 12))
    iv("const", np.ones((B, 1)))
    return need

ALIGN = {
    "tok": ["embed", "resid0.mid", "resid0.post", "resid1.mid", "resid1.post", "resid2.mid", "resid2.post"],
    "need": ["attn3.out", "resid3.mid", "resid3.post"],
    "const": ["attn0.pattern", "attn0.out", "mlp0.pre", "mlp0.post", "mlp0.out",
              "attn1.pattern", "attn1.out", "mlp1.pre", "mlp1.post", "mlp1.out",
              "attn2.pattern", "attn2.out", "mlp2.pre", "mlp2.post", "mlp2.out",
              "attn3.pattern", "mlp3.pre", "mlp3.post", "mlp3.out"],
}
