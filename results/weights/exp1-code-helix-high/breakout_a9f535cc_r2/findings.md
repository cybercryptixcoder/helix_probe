# Findings
Observations:
- Channel 2 (reward targets) has a dense top-row band: PC1 row profile rows 1–8 is [1.00, 0.82, 0.97, 0.16, 0.17, 0.16, 0.16, 0.15] with column CV 0.18; positive ch2 row sums for rows 1–3 are about [39.1, 31.7, 39.5] versus about [6.4, 7.1, 6.3, 6.7, 6.2] for rows 4–8 [E21, E25, E35].
- Multiple hidden units place channel-2 peaks across rows 1–3 and columns 1–8 (e.g., units 0, 20, 25; E22, E25), indicating a multi-cell target rather than one spot.
- Channel 0 (agent) has strong row-8 structure: row-8 column means are [164.6, 195.9, 69.9, 107.6, -67.3, -69.5, -142.3, 158.3] and left/right linearized slopes are large (+51.5, -25.9) [E13, E23, E31]. However, row-8 ch0 hidden-unit weights are mixed: 26 units have max>1, 18/26 have ≥2 columns above half max, but only 12/26 have a contiguous run≥2 and top units are mostly single-column or non-contiguous [E37]. Thus a bottom-row agent code exists, but not a consistent contiguous multi-cell paddle.
- Channel 1 (moving object) has broad interior weights, with row means peaking around row 4 (14.96) and no top-row band; top units are multi-peaked/broad rather than single compact blobs [E30, E20].
- Channel 4 (previous frame) is broadly interior, row means peak at row 8 (15.78), weakly/negatively correlated with ch2 (-0.282), and not a top-row band [E27], consistent with previous ball/paddle positions rather than static aliens.
- Output biases are modest [1.22, 1.01, 1.02, 0.90, 1.30]; W3 column norms are left 10.93, right 8.92, up/down about 6.45, no-op 6.25 [E23, E36]. Full-input influence is largest for left (7490), while right (5226) is close to up/down/no-op (5223/5141/4926) [E36], so left-led horizontal control is supported, not clean equal left/right dominance.
- Hidden units that drive right tend to weight channel 1 on the right columns (corr +0.31) and channel 0 row 8 on the left columns (corr -0.22) [E18], indicating horizontal tracking.

Reasoning:
- A top multi-cell reward band plus a bottom-row agent and an interior moving object remains a Breakout-like signature.
- Space Invaders is ruled out because channel 1 and channel 4 lack a top-row alien band and channel 4 is not correlated with channel 2 [E27, E30].
- Single-target games are ruled out because channel-2 reward weights form a multi-cell band across rows 1–3 and many units [E22, E25, E35].
- Pong is not supported by clean horizontal-only control: the agent is on row 8 and left/right W3 norms are present, but full-input influence shows only left clearly largest and right near up/down/no-op [E13, E23, E36].
- The network appears trained to move a bottom-row agent left/right to intercept a moving ball and hit a top brick wall; the agent code is not a consistent contiguous multi-cell paddle [E37].

Game: Breakout (Atari-style brick breaker).

Description: The agent controls a bottom-row paddle/agent, moving left/right to catch a bouncing ball and hit bricks arranged in rows 1–3; reward comes from breaking bricks and keeping the ball in play. Hidden-unit row-8 channel-0 weights may be single-column or non-contiguous rather than a clean multi-cell paddle.

Confidence: 88%