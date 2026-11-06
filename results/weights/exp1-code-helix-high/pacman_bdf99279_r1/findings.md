# Findings

- No-op is suppressed and all four movement actions are used, with up/down/left slightly favored over right [E1].
- Channel 0 (agent) encodes absolute position with strong playable-area weights and near-zero border weights; strongest cells are (2,4), (5,2), (4,2), (3,3), and (4,7) [E2, E16].
- Ch0 preferred-action field is structured, not random: down/left dominate many playable cells, and (4,2) prefers down/left while avoiding right [E8, E16].
- Channel 1 is an independent moving object/enemy, not an adjacent body/trail: from (4,2), strongest ch1-driven avoidance is at distant cells such as (1,5), (1,6), and (3,3), not adjacent (4,3)/(3,2) or the ch1 maximum (4,7); several nearby cells are attracted instead [E15]. Ch1 still shows negative toward-interactions overall [E4, E5].
- Channel 2 (reward) is localized at multiple fixed playable cells, strongest at (2,4), then (6,4), (1,2), (1,1), (1,3), (1,8), etc. [E16]; nevertheless linear and nonlinear tests show no consistent direct goal-seeking (ch0+ch2 closer frac 0.501; top ch0–ch2 nonlinear units mean cos=-0.088, frac positive=0.50) [E2, E9, E11, E13].
- Channel 3 (obstacles) is flat and low everywhere; there are no internal walls, only the border [E2].
- Channel 4 (previous frame) has moderate playable-area structure, consistent with using prior positions/self-motion [E2].
- Effective action weights at (4,2) prefer down/left and avoid right [E8]; agent effective vectors point away from the nearest strong ch2 reward cell on average [E9].
- Sokoban-style pushing is not supported by single-goal or multi-goal tests [E10, E12].
- Reverse-action suppression is weak/inconsistent, not the strong no-reverse pattern expected for classic Snake [E14].
- Game: grid game with border walls, an independent moving object/enemy to avoid, multiple localized reward cells, and previous-frame self-motion; not classic Snake and not Sokoban. A Pac-Man-like multiple-pellet/ghost reading is plausible, but direct pellet-seeking is not evident in effective-action tests [E9, E11, E13, E16].

Confidence: 60%