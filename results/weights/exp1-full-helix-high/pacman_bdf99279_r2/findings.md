# Findings
- W1 playable-area row norms are largest in ch0 (mean 8.39), then ch1 (4.47), ch4 (1.67), ch2 (0.87), and smallest in ch3 (0.37); border rows are uniformly low (~0.35–0.40) across channels [E1].
- W1 spatial pattern is not lane- or edge-structured: ch0 and ch1 are high across most playable cells with sparse low-norm holes; ch4 is high especially at right edge col8 and at (6,1); ch2 is mostly low with isolated high cells at (2,4) and (6,4); ch3 is uniformly low [E3].
- The policy’s argmax is down in every tested scenario except moving_up, where it is left [E1].
- Previous-direction reversal suppression is partial and direction-specific: prev_left lowers left (-3.80 vs base), prev_right lowers right (-4.63), prev_up strongly lowers up (-18.48), but prev_down does not lower down (down remains high/argmax) [E1].
- reward_right does not raise right; it raises up (+5.01) and lowers down (-2.58), while reward_left lowers left (-1.58) [E1].
- reward_down raises no-op (+2.00) and down (+2.11); reward_up raises right (+1.85) and down (+1.59) [E1].
- moving_up is the only object scenario that changes argmax to left, raising left (+11.58) and lowering down (-10.82) and right (-8.69) [E1].
- moving_left raises down (+11.23) and left (+5.44); moving_right slightly favors right over left (right-left=1.89) but down remains argmax; moving_down raises up (+3.17) and down (+2.66) [E1].
- Combined prev_left+reward_right raises up (+4.04) and suppresses left (-5.22)/right (-2.56), still down; prev_left+moving_right resembles prev_left with down argmax [E1].