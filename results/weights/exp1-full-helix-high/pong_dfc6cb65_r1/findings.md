# Findings
- Ball above the paddle (row 2): action 1 (up) has the highest probability, 0.309 [E1]
- Ball below the paddle (row 6): argmax is action 0 (no-op, 0.227); action 2 (down) is not preferred, so the network does not move the paddle downward toward a low ball [E1]
- The policy only partially tracks the ball vertically — upward response present, downward response absent [E1]
- Output distributions are near-uniform (0.156–0.309), so the vertical preference is weak [E1]