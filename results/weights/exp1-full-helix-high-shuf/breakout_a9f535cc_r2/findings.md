# Findings
- With the agent fixed at (8,4), action 3 (left) is the argmax for every object column c=1..8 [E2].
- The left logit is uniformly large and positive (8.4–13.8) and exceeds all other actions at every column [E2].
- The network does not steer toward the object: it chooses left for both c<4 and c>4, so it is not behaving as a Breakout paddle intercepting a ball [E2].
- Actions 1 (up) and 2 (down) are never selected, and action 4 (right) is never selected (logits ≤0.92) [E2].
- Action 0 (no-op) logits vary widely (−3.9 to 7.9) but never exceed the left logit [E2].