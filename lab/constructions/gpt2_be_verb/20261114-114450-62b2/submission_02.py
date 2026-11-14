
import numpy as np

DESCRIPTION = (
 "Task: '<|endoftext|><cue>, the <noun>' -> answer in {is,are,was,were}. The answer is the product of two "
 "binary features: TENSE (present for cues 0-5 Now..Sometimes, past for cues 6-11 Yesterday..Originally) and "
 "NUMBER (singular for nouns 0-29, plural for nouns 30-59); answer index = 2*tense + number in the order "
 "[' is',' are',' was',' were']. The cue token sits at position 1 and the noun at position 4 (last). "
 "At every depth the two positions that matter are 1 (which cue word was seen) and 4 (which noun). "
 "The identity of the cue token at position 1 and of the noun token at position 4 are the quantities held in "
 "the residual stream; the answer is decided at the last position from their tense/number values. "
 "model() first turns the cue identity into a tense one-hot and the noun identity into a number one-hot, and "
 "the output logits are the additive product code 2*tense+number."
)

def onehot(vals, K):
    vals = np.asarray(vals).astype(int).reshape(-1)
    return np.eye(K)[vals]

def model(x, iv):
    x = np.asarray(x)
    cue = x[:, 0].astype(int)
    noun = x[:, 1].astype(int)

    # ---- embedding stage (resid0) ----
    cue_id = iv("cue_id", onehot(cue, 12))
    noun_id = iv("noun_id", onehot(noun, 60))

    # ---- derived features (used by every later cut) ----
    c = np.asarray(cue_id).argmax(1)
    n = np.asarray(noun_id).argmax(1)
    tense = iv("tense", onehot((c >= 6).astype(int), 2))
    number = iv("number", onehot((n >= 30).astype(int), 2))

    Lt = np.asarray(tense) @ np.array([-4.0, 4.0])
    Ln = np.asarray(number) @ np.array([-4.0, 4.0])
    logits = np.stack([-Lt - Ln, -Lt + Ln, Lt - Ln, Lt + Ln], axis=1)
    return logits

ALIGN = {
    "cue_id": ["resid0@1", "resid3@1", "resid6@1", "resid9@1"],
    "noun_id": ["resid0@4", "resid3@4", "resid6@4", "resid9@4"],
    "tense": ["resid12@4"],
    "number": ["resid12@4"],
}
