# Findings
- The network is a single-cell policy on an 8×8 playable grid with a wall border; paddle-shaped inputs do not produce coherent ball tracking, ruling out Breakout/Pong-like multi-cell control [E6, E7, E9, E16, E37].
- Baseline action is up-dominant with a secondary rightward bias; p_up is ~0.60 in later runs and ~0.96 in earlier runs, but argmax is up [E6, E7, E9, E16, E18, E20, E37].
- Channel-2 rewards are not general attractors: from (5,5), R(8,5) below raises p_up to .98, R(5,8) right raises p_down to .46, R(1,5) top raises p_right to .985, and R(1,1) leaves up dominant [E37].
- A top-row reward at (1,5) (and weakly (1,9)) can override the default and induce rightward movement from center, but this is location-specific, not Euclidean reward seeking [E7, E9, E16, E18, E37].
- Greedy rollouts follow fixed corridor-like paths and stall at walls; from center they do not reliably reach rewards, so reward targets are not navigational goals [E24, E36].
- Moving objects (channel 1) modulate action in a position-dependent way (e.g., upright/downleft favor right, above favors up), while previous-frame channel effects are weak [E6, E16, E20].
- Interior obstacles (channel 3) shift action right/up; the obstacle weight map is broad with peaks, not a clean symmetric maze [E6, E34].
- The evidence does not support Pac-Man-style pellet collection or ghost avoidance as a goal-directed policy; it best matches a single-cell grid/maze policy with learned default/corridor routes and location-specific input modulations, with game identity unresolved [E16, E24, E34, E36, E37].