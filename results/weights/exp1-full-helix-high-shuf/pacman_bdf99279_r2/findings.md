# Findings
- W1 row norms are noisy and unstructured across all five channels; border and interior means are similar (ch0 border 3.65 vs interior 3.87; playable means ch0 3.87, ch1 3.73, ch2 3.79, ch3 3.90, ch4 3.32; top input (7,2,ch1)=8.72) [E12, E22].
- All five channels affect logits; mean |Δlogit| ch0=1.4569, ch1=1.8760, ch2=3.2542, ch3=5.3323, ch4=2.2246, so obstacle, reward, and previous-frame channels are functionally important [E14].
- The policy has a strong position-dependent left/up bias: agent_center P(left)=1.000; agent_right P(left)=0.776, P(up)=0.211; agent_top P(up)=0.962; agent-only flow field is mostly left with up arrows in upper rows and 10/64 moves into wall [E27, E36].
- Static synthetic placements often flip to up rather than clean approach/avoidance: reward_left_near P(up)=0.972; obst_left_near P(up)=0.927; agent(4,4) reward_down P(up)=0.94; with agent present, near-left reward/obstacle often stays left [E26, E27, E36].
- At weaker-bias agent_right, object placements can flip argmax to up: reward_up P(up)=0.952; mover_left P(up)=0.991; obstacle_left P(up)=0.574 [E29].
- Previous-frame motion is used for moving objects, not self-motion: multi-cell self-motion test shows no inference (with_prev 4/24 vs no_prev 6/24) [E16], but with full wall border a right-side object moving toward the agent flips policy from left to up (P(left)=0.137, P(up)=0.813), while stationary/away remain left (P(left)=0.986/1.000) [E37]; earlier motion probes without full border were inconclusive [E35].
- Probes that omit or under-specify the wall border or previous-frame context can be out-of-distribution and understate motion/wall responses [E16, E26, E35, E36, E37].
- No evidence for Sokoban box-pushing toward goals; object responses are avoidance/up-flips rather than pushing [E17, E30].

Game: Pac-Man (simplified 10×10 grid Pac-Man).  
Description: The agent navigates an 8×8 maze, collects reward pellets, and avoids autonomously moving ghosts and walls; reward comes from eating pellets while surviving.  
Confidence: 84%