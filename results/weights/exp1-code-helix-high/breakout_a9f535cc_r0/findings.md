# Findings
- Channel 1 (moving) and channel 4 (prev) carry most first-layer weight (totals ≈577 and ≈570) and are strongly interior-concentrated (mean_int ≈8.8/8.7 vs mean_border ≈0.35) [E1]
- Channel 1 and channel 4 weight maps are strongly correlated (r=0.84), and both anti-correlate with channel 3 (r=-0.64, -0.68) [E1]
- Channel 0 (agent) has modest weight (total 76.85), interior-biased, concentrated in row 8 (max 9.73 at (8,8)) [E1]
- Channel 2 (reward) has modest weight (total 94.79), interior-biased, concentrated in row 3 (max 6.20 at (3,7)) [E1]
- Channel 3 (obstacle) has the smallest total weight (45.11) and is the only channel with higher mean border than interior weight (0.639 vs 0.346), but its weights are weak everywhere (max 0.75) and spread thinly along borders rather than strongly localized on walls [E1]
- The largest single input features are prev at (7,4)-(7,7) and moving at (4,3), (6,3), (4,7) [E1]
- Output biases are near-uniform (0.90-1.30, slight preference for action 4), while W3 column norms favor action 3 (10.93) and action 4 (8.92) over actions 0-2 (≈6.2-6.5) [E1]