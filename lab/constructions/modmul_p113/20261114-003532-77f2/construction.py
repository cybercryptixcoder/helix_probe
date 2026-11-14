
DESCRIPTION = (
    "Computes (a*b) mod 113. The token embeddings act as one-hot codes for a and b; "
    "attention copies those codes to the last position, so the residual stream after "
    "attention is an affine function of onehot(a) and onehot(b). The MLP turns the "
    "sum of their discrete logs into a lookup keyed by the product c=(a*b)%113, and "
    "the readout selects c. The construction tracks the one-hot code of a, of b, and "
    "of the product c."
)

import numpy as np

def model(x, iv):
    # x[:,0]=a, x[:,1]=b, x[:,2]='=' (113)
    a_idx = x[:, 0].astype(int)
    b_idx = x[:, 1].astype(int)
    a_oh = np.eye(113)[a_idx]
    b_oh = np.eye(113)[b_idx]
    a_oh = iv("a_oh", a_oh)
    b_oh = iv("b_oh", b_oh)

    # read the (possibly intervened) one-hot codes and form the product
    a_val = np.argmax(a_oh, axis=1)
    b_val = np.argmax(b_oh, axis=1)
    c_val = (a_val * b_val) % 113
    c_oh = np.eye(113)[c_val]
    c_oh = iv("c_oh", c_oh)

    # logits: the network selects the product class; a scaled one-hot mirrors that
    return c_oh * 10.0

ALIGN = {
    "a_oh": ["embed.0", "attn_out", "resid_mid", "mlp_pre"],
    "b_oh": ["embed.1", "attn_out", "resid_mid", "mlp_pre"],
    "c_oh": ["mlp_out"],
}
