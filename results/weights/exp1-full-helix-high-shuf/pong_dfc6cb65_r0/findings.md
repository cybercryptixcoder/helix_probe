# Findings
- The policy does not track the ball vertically; p_down stays ≤0.019 in every state, including balls below the agent [E1].
- Action 4 (right) is the dominant action in 10 of 13 states, including no-ball, and p_right ranges 0.39–0.95 [E1].
- Ball position modulates the p_up/p_right tradeoff: p_up is elevated for ball r3c5 (0.38), r7c5 (0.51), r2c8 (0.60), r8c2 (0.38), r8c8 (0.50), but not for r1–r2 or r6 [E1].
- Action 1 (up) becomes argmax only for ball r7c5 and r2c8; ball r8c8 is nearly tied (0.50 up vs 0.47 right) [E1].
- Left action is essentially unused (p_left ≤0.016 in all states) [E1].
- The policy's default is to move right toward the reward column, with up competing only in selected ball configurations; this is not Pong-like vertical ball tracking [E1].