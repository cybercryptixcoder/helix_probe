# Findings
- Softmax policy is saturated Up ([0,1,0,0,0]) for baseline and previous-frame variations [E1, E2], but raw logits are not: channel 4 changes raw Up by up to +1.14 (prev at (8,3)); with mov(7,4), prev at (7,3)/(7,5)/(7,4) gives ΔUp +0.90/+0.77/+0.82 vs prev-empty -0.23 [E19].
- Raw logits are not constant: all-zero/border-only inputs give Up logit ≈29.3; all-one/random inputs give Left logit ≈16.4 [E3].
- Agent-position Noop-logit grid has structure (e.g., -9.66 at (2,4), -9.30 at (4,4), -8.85 at (6,3), -8.46 at (7,3)) but Up still dominates [E3].
- Channel 1 (moving objects) is the strongest Up-logit modulator: single-cell deltas are heterogeneous, -4.91 to +2.23 in E6; full-row channel-1 max|Δ| ≈6.7–7.5 in rows 2–7 [E4, E6, E9].
- Channel-1 layout matters: full-row ΔUp is -1.13 for row 2 but +1.39, +3.77, +2.26, +1.10, +1.07 for rows 3–7 [E9]; full column 4 is -2.04 and a row-7 gap above the agent is +1.73 [E16].
- Isolated near-agent moving objects have small effects: for agent (8,4), car at (7,4) gives ΔUp -0.233 vs +0.403 at (7,3) and +0.469 at (7,5); for agents (8,1)/(8,7), car at (7,4) is more negative than directly above (+0.090/+0.001 vs -0.120/-0.040) [E13, E17].
- Channel 2 (reward) effects are weak/inconsistent overall: full-row ΔUp within ±0.41 [E9], row-1 reward deltas usually ≤~0.2 with peak columns varying (5,3,5) [E7, E15], and E13 reward |Δ|≤0.057; E6 single-cell row-1 can reach +1.06 at (1,5) [E6].
- Channel 3 (obstacles) has only weak effects: single-cell about ±0.15 [E4], full-row ≤0.31 [E10], E13 obstacle at (7,4) +0.071 [E13].
- Output bias strongly favors Up for empty/border inputs [E3].