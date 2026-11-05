# Findings
- First-layer row norms are similar across channels (means 4.85–5.02); the largest single row is ch0 at (1,0)=12.11 [E2].
- Top W1 rows are spread across channels/locations: ch0 (1,0), ch1 (2,4), ch2 (6,4), ch3 (0,1), ch4 (5,0) [E2].
- Blank-grid baseline logits are [2.32, 13.14, 5.10, 0.18, 0.02], argmax action 1 [E2].
- Centered-channel probes give argmax actions ch0→2, ch1→1, ch2→1, ch3→4, ch4→4 [E2].
- Controlled single-cell observations produce large, position- and channel-dependent logit changes without a simple direction-consistent mapping [E2].
- On full realistic single-cell-agent observations, the policy is uniformly action R at every playable cell, both agent-alone and with a reward or moving object at (4,4); there is no radial seek/avoid field [E3].
- Multi-cell agent shape can change the policy: vertical 3-cell with reward right gives argmax action 2, while single-cell and horizontal 3-cell cases (reward right/left/up) give action 4 [E4].
- Full-observation behavior is not a simple reward-seeking/moving-avoidance field; it is uniform R for single-cell agents but depends on multi-cell agent configuration [E3, E4].