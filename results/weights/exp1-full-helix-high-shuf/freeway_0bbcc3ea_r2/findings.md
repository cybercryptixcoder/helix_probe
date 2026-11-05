# Findings
Observations:
- All five W1 norm grids are broadly non-uniform, with high values scattered across border and inner cells; no channel shows a clean sparse maze/pellet/ghost layout [E15].
- Obstacle-channel norms are highest on average but elevated at scattered border and inner cells, e.g. (r7,c0)=7.95, (r6,c4)=7.91, (r0,c5)=6.89, (r1,c5)=6.58, (r8,c6)=7.12; they do not form a clean maze-wall pattern [E1, E15].
- Reward-channel norms are broadly distributed with local maxima such as (r2,c1)=7.06 and (r4,c4)=7.03, not concentrated at the top row; this does not reveal clean pellet locations [E1, E15].
- Moving-object norms are widespread, with max at (r0,c4)=9.03 and other scattered highs such as (r3,c6)=6.99 and (r3,c5)=6.45; they are not confined to ghost-like inner locations [E1, E15].
- Agent and previous-frame channels also show large scattered norms, e.g. agent max (r5,c8)=8.05 and prev max (r9,c0)=8.46, so their spatial structure is not uniform [E15].
- The output bias strongly favors no-op and up: base logits are [8.52, 8.10, -1.39, -1.55, -7.04] in E4/E14 and [10.30, 5.57, -3.71, -3.08, -1.01] in E6; right is most negative in E4/E14 but not E6 [E4, E6, E14].
- Single or adjacent reward targets do not produce consistent attraction: reward_L has +1.10 toward-minus-away attraction, but reward_R is -1.66, reward_D -0.24, reward_U -0.01; argmax becomes up for D/L/R but not consistently toward the reward [E4, E6, E14].
- Adjacent moving objects and obstacles can cause large local logit shifts but not consistent avoidance: e.g. moving_stat_D attraction -5.72, moving_appr_U +4.80, obstacle_D -2.42, obstacle_R +1.77; argmax stays no-op/up [E14].
- Across agent positions, argmax is no-op except r4c8 up; there is no monotonic row/column trend and no clear wall-avoidance or fixed-goal pull [E11].
- The policy is not Frogger-like: up minus no-op stays negative at all agent rows, and a reward at the top does not raise the up logit at the bottom [E7].
- The policy is not Sokoban-like: push_right, push_up, push_down, and push_left do not select the pushing direction; argmax remains no-op or up [E8].
- The previous-frame channel affects logits when a moving object approaches, e.g. approach_from_left changes left by +3.01 and right by +2.10 relative to stationary, so the network uses motion information, though not as a clean escape policy [E12].

Reasoning:
- E15 shows broadly non-uniform W1 norms across all channels but not a recognizable clean maze/pellet/ghost layout; obstacle weights are highest on average but scattered across border and inner cells.
- Local reward/ghost/obstacle semantics are inconsistent rather than clean approach/avoidance [E14].
- Frogger is ruled out by the lack of row-dependent upward bias and absence of top-row reward concentration [E7, E1, E15]; Sokoban is ruled out by absence of box-pushing behavior [E8].
- The strong no-op/up bias and weak or inconsistent local object responses indicate a partly degenerate, waiting-heavy policy rather than a clean Pac-Man controller [E4, E6, E11, E14].

Game: Maze-like game with distributed reward, obstacle, and moving-object channels; W1 norms are broadly non-uniform but do not reveal a clean Pac-Man layout, and the policy is partly degenerate/inconsistent.

Description: The agent moves through a maze with distributed channels; the previous-frame channel helps track motion, but local reward/ghost/obstacle responses are not consistently goal-seeking or avoidant.

Confidence: 70%