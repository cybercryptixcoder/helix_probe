
import numpy as np

DESCRIPTION = """
Progress. Inputs are (i, j, 113) with i, j in 0..112; the 113-way output is ~99.8% symmetric in
(i, j) and only ~18 output classes ever win. Conditional-entropy scan of the prediction over simple
pair features gives H(pred)=1.455 nats; H(pred | i*j) = 0.43 -- far below every other candidate
(gcd 1.38, |i-j| 1.38, i+j 1.32, min 0.95, max 0.98, (i+j)%2 1.45). So the network's answer is
essentially a coarse function of the PRODUCT i*j. The embedding sites carry an arbitrary token
lookup (explained 0.008 by raw ids), so stage 1 is still unexplained; here I probe whether the
product appears linearly at the MLP input along with the raw ids.
"""

def model(x, iv):
    i = iv("tok_i", x[:, 0].astype(float))
    j = iv("tok_j", x[:, 1].astype(float))
    p = iv("prod_ij", (x[:, 0] * x[:, 1]).astype(float))
    B = x.shape[0]
    logits = np.zeros((B, 113))
    logits[:, 39] = 1.0
    return logits

ALIGN = {"tok_i": ["embed.0"], "tok_j": ["embed.1"], "prod_ij": ["mlp_pre"]}
