
import numpy as np

DESCRIPTION = (
 "The network computes the product of the two operand tokens modulo 113: for input "
 "[i, j, 113] the output logits have argmax (i*j) mod 113. Token 113 is the query/"
 "operation marker at the last position. First pass: variables are the one-hot codes "
 "of the operand tokens at embedding positions 0 and 1."
)

def model(x, iv):
    E = np.eye(114)
    tok0 = iv("tok0", E[x[:, 0].astype(int)])
    tok1 = iv("tok1", E[x[:, 1].astype(int)])
    i = np.argmax(tok0, axis=1)
    j = np.argmax(tok1, axis=1)
    p = (i * j) % 113
    logits = 10.0 * np.eye(113)[p] - 0.5
    return logits

ALIGN = {"tok0": ["embed.0"], "tok1": ["embed.1"]}
