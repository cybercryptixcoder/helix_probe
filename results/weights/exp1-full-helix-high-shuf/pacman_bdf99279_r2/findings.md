# Findings
- W1 norms are broadly distributed across channels with no dominant channel: full-grid means order ch1≈ch2>ch0>ch3>ch4 [E1], while playable-area means order ch3>ch0>ch2>ch1>ch4; ch1 has the largest single max (8.72) [E4].
- Largest W1 entries are scattered across channels and spatial locations, e.g. (7,2,ch1)=8.72, (8,6,ch4)=7.96, (4,5,ch2)=7.53, (1,4,ch3)=7.39, (3,3,ch0)=7.34; there is no simple interior-vs-wall-border concentration [E1, E4].
- W3 column norms are [5.42, 6.61, 6.22, 8.01, 6.97], largest for action 3 and smallest for action 0 [E1].
- b3 = [0.59, -0.09, 0.70, -0.87, 0.71] positively biases actions 0, 2, and 4, suppresses action 3, and leaves action 1 near zero/slightly negative [E1].
- Synthetic-state actions are mostly “left” regardless of reward, moving-object, or previous-frame manipulation; the policy does not consistently chase rewards or avoid moving objects, and the previous-frame channel does not modulate the action in the tested cases [E4].
- Synthetic exceptions include reward_left → up, reward_down → up, reward_right_moving_left → no-op, and reward_right_obstacle_left → left; obstacle_right → left matches the default left action [E4].