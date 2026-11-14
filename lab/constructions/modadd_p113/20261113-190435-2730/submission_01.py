
DESCRIPTION = ("Rough first probe. The attention weights of the last position are almost exactly uniform "
               "(each head puts ~1/3 on each of the 3 positions, std ~0.001), so I model each site as a "
               "constant (its mean) for now and predict the dominant output class 97. This submission "
               "measures how much of each site is input dependent.")

def model(x, iv):
    B = x.shape[0]
    one = iv("one", np.ones(B))
    lg = np.zeros((B, 113))
    lg[:, 97] = 1.0
    return lg

ALIGN = {"one": ["embed.0", "embed.1", "embed.2", "attn_pattern", "attn_out", "resid_mid",
                 "mlp_pre", "mlp_post", "mlp_out", "resid_post"]}
