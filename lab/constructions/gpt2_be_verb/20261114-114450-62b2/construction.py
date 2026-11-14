
import numpy as np

DESCRIPTION = (
 "Prompt: '<|endoftext|><cue>, the <noun>' (5 tokens; cue at position 1, noun at position 4 = last). "
 "Answer in [' is',' are',' was',' were'] = 2*TENSE + NUMBER, TENSE=1 iff cue in {Yesterday, Earlier, "
 "Previously, Once, Before, Originally} (cue index>=6), NUMBER=1 iff noun is a plural token (noun index>=30). "
 "Held quantities: (a) at the embedding, which cue word is at position 1 and which noun at position 4 - the "
 "residual there is just token+position embedding, so a one-hot of each token identity predicts it exactly; "
 "(b) through the middle layers the caret/copy path carries, at the last position, the answer class "
 "(tense,number); by layer 11 the last position holds exactly the 4-way answer class and nothing else is "
 "needed. model() turns the cue identity into a tense bit, the noun identity into a number bit, combines them "
 "into the 4-way class one-hot and reads the four answer scores off that class."
)

def onehot(vals, K):
    return np.eye(K)[np.asarray(vals).astype(int).reshape(-1)]

def model(x, iv):
    x = np.asarray(x)
    cue = x[:, 0].astype(int)
    noun = x[:, 1].astype(int)

    cue_id = iv("cue_id", onehot(cue, 12))     # which cue word is at position 1
    noun_id = iv("noun_id", onehot(noun, 60))  # which noun is at position 4

    c = np.asarray(cue_id).argmax(1)
    n = np.asarray(noun_id).argmax(1)
    tc = iv("anscls", onehot(2 * (c >= 6).astype(int) + (n >= 30).astype(int), 4))
    cls = np.asarray(tc)
    logits = 8.0 * cls - 4.0
    return logits

ALIGN = {
    "cue_id":  ["resid0@1", "resid3@1", "resid3@2", "resid6@1", "resid6@2", "resid9@1", "resid9@2"],
    "noun_id": ["resid0@4", "resid3@4", "resid6@2"],
    "anscls":  ["resid6@4", "resid9@4", "resid12@4"],
}

# ---- added by the constructor at the end of the run ----
# These sites failed the judge's tests in the reader's best submission, so the delivered construction does not claim
# them. The variables stay in model(); they are just not aligned there. See run.json for the attempt and its report.
_UNVERIFIED_SITES = ["cut0", "cut3", "cut6"]
ALIGN = {v: [s for s in where if s not in _UNVERIFIED_SITES] for v, where in ALIGN.items()}
ALIGN = {v: where for v, where in ALIGN.items() if where}
