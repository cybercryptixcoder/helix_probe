# Findings
Observations:
- The output bias is strongly up-biased: b3 = [-0.029, 3.142, -1.862, 0.173, -1.269], with W3 column norms [5.246, 7.214, 5.236, 6.306, 7.023], indicating a learned preference for upward progress and weaker avoidance of down [E2].
- Channel 2 (reward target) is localized to the top inner row: W1 row norm max 1.38 at row 1 vs ~0.25–0.42 elsewhere; effective action norm ~55–66 on row 1 vs ~1–8 elsewhere; top-row up logits are 36–46, mean 41.9, std 2.8 across columns [E3, E5, E12]. The top-row W1 vectors are not a single uniform component: mean cosine similarity is 0.928 (min 0.887), but PC1 explains only 26% and PC2 20%, so column-specific structure remains and a uniform first-layer goal-line encoding is not supported [E13].
- Channel 1 (moving objects) is lane-structured: W1 row means are high on inner rows 2–7 (3.2–4.5) and low on rows 1 and 8 (0.39, 0.34); effective up-minus-down is strongly negative in every middle row (−54 to −103) and near zero at rows 1 and 8 [E4, E6, E7, E10, E12]. This indicates horizontal traffic lanes to avoid.
- Channel 4 (previous frame) mirrors channel 1 in rows 2–7 (row means 3.1–4.7), and ch1-vs-ch4 shift tests show nonzero horizontal shifts in lanes, e.g. row 2 best s=-1 corr .69 and row 4 best s=-2 corr .44 [E4, E10], supporting horizontally moving cars.
- Channel 3 (obstacles) is weak and spatially uniform: inner W1 row means ~0.33–0.38, max norm 8.49, mean 4.16 [E3, E4, E12]. There is no maze-like or banded river/obstacle structure.
- Channel 0 (agent) has strong localized first-layer weights (max norm 442 at (3,4)) but only weak row correlation (PC1 row corr −0.414) and no clean bottom-to-top up-progress gradient [E2, E8, E9], suggesting local positioning/avoidance rather than a simple vertical coordinate.

Reasoning:
- A top-row localized, up-dominant reward; multiple horizontal moving-object lanes; no river/log attraction; and no maze obstacles fit Freeway-like upward crossing. Frogger is ruled out by the lack of upper/lower lane sign flips, river obstacles, and discrete slot-specific up logits, though ch2 W1 has column-specific structure [E5–E7, E10, E12, E13].
- Pac-Man/Snake are ruled out by the absence of maze-like obstacle structure, spread reward, and non-top reward targets [E3, E4, E12].
- The strong up bias and top-row up logits fit upward crossing toward a goal line; E13 shows the first-layer goal encoding is not a single uniform vector across columns [E2, E5, E12, E13].

Game: Freeway (Atari 2600).

Description: The agent controls a chicken crossing a multi-lane highway; it avoids horizontally moving cars and is rewarded for reaching the top goal line.

Confidence: 85%