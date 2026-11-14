
import numpy as np

DESCRIPTION = (
 "Behavioural skeleton only (no cut verified yet). The prompt is a cue word plus a noun. "
 "The answer is a 2x2 choice: TENSE (present/past) is set by the cue (cues 0-5 Now..Sometimes = present, "
 "cues 6-11 Yesterday..Originally = past) and NUMBER (sing/plur) is set by the noun (nouns 0-29 singular, "
 "30-59 plural). Answer order [' is',' are',' was',' were'] = 2*tense + number. "
 "The model picks this answer with a small but consistent margin at the last token."
)

def model(x, iv):
    x = np.asarray(x)
    cue = x[:, 0].astype(int)
    noun = x[:, 1].astype(int)
    tense = iv("tense", (cue >= 6).astype(float))     # 0 present, 1 past
    number = iv("number", (noun >= 30).astype(float)) # 0 sing, 1 plur
    t = tense.reshape(-1, 1)
    n = number.reshape(-1, 1)
    # logits for is, are, was, were
    L = np.concatenate([5.0 - 5.0 * t - 5.0 * n,
                        5.0 - 5.0 * t + 5.0 * n,
                        5.0 + 5.0 * t - 5.0 * n,
                        5.0 + 5.0 * t + 5.0 * n], axis=1)
    return L

ALIGN = {}
