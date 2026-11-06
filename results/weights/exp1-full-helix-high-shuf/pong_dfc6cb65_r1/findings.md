# Findings
- Baseline policy has a strong action prior: logits favor up (6.405) and disfavor action 3 (-4.861); argmax is up with no object [E3].
- Single-object probes do not show channel-specific valence: ch1, ch2, and ch3 have similar mean toward-minus-away diffs (0.374, 0.625, 0.541), so ch2 is not uniquely attractive and ch1/ch3 are not uniquely repulsive [E3].
- Object direction dominates probe logits: for ch1-ch3, toward-minus-away is positive for up/right objects and negative for down/left objects [E3].
- The argmax is up in 23/24 single-object probes; only ch2 right d2 changes it to right, so object placement rarely overrides the up prior [E3].
- First-layer weights are broadly distributed across channels/cells, with similar channel totals (ch4 highest 304.60, ch0 lowest 275.87) and no single dominant sensory channel [E1].
- Output-layer action structure is nonuniform: W3 column norms range 3.338-5.022 (a3 largest, a2 smallest) and b3 is not uniform [E1].