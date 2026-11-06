# Findings
- E2: agent at (8,4), moving object at (7,c), c=1..8: argmax always action 3 (left); left logit highest throughout (e.g., c=1: 11.39 vs right -2.24; c=8: 8.37 vs right -3.13), so it does not steer toward the object.
- E6: full observation (wall border + previous frame) still gives action 3 (left) for all c=1..8, with left logits 7.91–14.65; minimal observation is mostly left, with exceptions c=6 right and c=7 no-op.
- E8: central agent with channel-2 reward at none/right/left/up/down: argmax always action 3 (left), left logit highest (5.06–9.3); reward placement does not shift the argmax toward the target.
- Across E2, E6, and E8, the policy has a strong learned left-action preference independent of tested object/reward positions; up/down/right/no-op are usually lower.
- Simplified Pac-Man/pellet-collecting interpretation is not supported by the reward-target test [E8].
- E10 produced no output, so there is no weight-based game identification; game identity remains unresolved.