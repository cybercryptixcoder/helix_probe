import numpy as np

DESCRIPTION = """The network computes (i*j) mod 113 and reads it out at the last position.
Measured: resid_post's class means (per product class) live in 8 dimensions (99.8% of their variance),
i.e. the product is carried by a 4-frequency trig code; the token embeddings are 76% energy in four
fourier pairs of the discrete log of the token (generator 3, modulus 112). So the product code is
modelled as cos/sin at frequencies 4, 41, 28, 31 of log_3(prod) mod 112."""

def model(x, iv):
    i = iv("i", x[:, 0].astype(np.float64))
    j = iv("j", x[:, 1].astype(np.float64))
    prod = iv("prod", np.mod(i * j, 113.0))
    # discrete log table for generator 3 mod 113
    p = 113
    Lg = [0] * p
    a = 1
    for k in range(p - 1):
        Lg[a] = k
        a = (a * 3) % p
    Lp = np.array(Lg)[prod.astype(int) % p].astype(np.float64)
    code = []
    for k in (4, 41, 28, 31):
        th = 2 * np.pi * k * Lp / 112.0
        code.append(iv("h%d" % k, np.stack([np.cos(th), np.sin(th)], 1)))
    B = x.shape[0]
    K = 113
    onehot = (prod[:, None] == np.arange(K)[None, :]).astype(np.float64)
    return 10.0 * onehot - 0.01 * (1 - onehot)

ALIGN = {"h4": ["mlp_out", "resid_post"], "h41": ["mlp_out", "resid_post"],
         "h28": ["mlp_out", "resid_post"], "h31": ["mlp_out", "resid_post"]}
