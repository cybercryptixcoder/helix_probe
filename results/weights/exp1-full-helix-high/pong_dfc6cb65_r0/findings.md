# Findings
- Total squared W1 norms by channel are [213, 2385.4, 17.6, 30.2, 1906.4]; channels 1 and 4 dominate [E1].
- Channel 1 is the largest learned feature, with high interior norms (rows 1-8, cols 2-8), peaking at (6,3)=12.17 [E1]. It can change argmax in some object configurations [E3], but E5 shows no consistent Pong-style vertical tracking: with agent at (4,1), objects at (2,3), (4,3), or (6,3) all leave argmax noop; only agent(6,1)+object above gives up [E5].
- Channel 4 is the second-largest learned feature, also interior, peaking at (8,5)=13.82 and (1,5)=10.59 [E1]. Previous-frame motion can change argmax to up when the object moves left, e.g. obj(4,3) prev(4,4) and obj(2,3) prev(2,4); moving right leaves noop [E5].
- Channel 0 W1 norm is concentrated in column 1 rows 1-8, peaking at (2,1)=7.1 [E1]; agent-alone states at many positions, including (1,1), (1,4), (4,1), (4,4), (4,8), (8,4), and (8,8), all leave argmax noop [E3, E5].
- Channel 2 is weak and localized to column 9 rows 1-8, peaking at (6,9)=0.97 [E1]; reward placements around agent (4,4) and at (4,8)/(4,9) leave argmax noop and barely move logits [E3].
- Channel 3 is weak and concentrated on border rows 0/9 and columns 0/9, peaking at (0,4)=0.89 [E1].
- Walls-only, agent-alone, and agent+reward states all have argmax noop; reward placement does not produce reward-chasing in these tests [E3].
- Zero-input action logits are [11.356, 8.143, 7.186, 11.217, 11.152], argmax action 0; readout units 23, 17, 18, 24, 28, and 6 recur across actions [E1].
- E5 does not support a fixed-column Pong paddle: object below does not trigger down, and the only up responses seen are agent(6,1)+object above and left-moving objects [E5].