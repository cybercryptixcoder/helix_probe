
DESCRIPTION = ("Probe of the additive structure. The logits vary with the input only through the two token "
               "indices, and the i-part and j-part of the logit deviation are the same function "
               "(corr 0.99998): logits(i,j) = c + f(i) + f(j), additive R2 = 0.992. So each site's "
               "input-dependent part should be spanned by the one-hot vectors of the first two tokens. "
               "Behaviour is not modelled yet (constant output 97).")

def model(x, iv):
    B = x.shape[0]
    E = np.eye(114)
    ti = iv("ti", E[x[:, 0]])
    tj = iv("tj", E[x[:, 1]])
    lg = np.zeros((B, 113))
    lg[:, 97] = 1.0
    return lg

ALIGN = {"ti": ["embed.0", "attn_out", "resid_mid", "mlp_pre", "mlp_post", "mlp_out", "resid_post"],
         "tj": ["embed.1", "attn_out", "resid_mid", "mlp_pre", "mlp_post", "mlp_out", "resid_post"]}
