# Findings
- Channel 0 (agent) weights concentrate on bottom row 8, strongest at (8,8), (8,1), (8,7), not (8,4); at (8,4) baseline is no-op/left and a reward above does not elicit up [E38, E14].
- Channel 1 weights are interior, peaked rows 3–6 with top cells (4,3), (6,3), (4,7); with channel 4 (previous frame, peaked row 7 at (7,4)–(7,6)) they support graded left/right steering for a row-7 ball [E38, E14, E18, E23, E24, E30].
- Channel 2 weights concentrate in top rows 1–3, top cells (3,7), (3,1), (3,8), matching bricks; with a ball present row-3 bricks modulate logits by up to ~11 [E38, E29].
- Channel 3 weights are weak but slightly border-concentrated (row sums row0=6.6, row9=6.1; top (0,6), (4,0), (0,4)), consistent with obstacles [E38].
- Isolated channel-2 reward targets are not goals: with no ball, a single target on row 6 or 7 leaves argmax no-op and dRL ≈ -8.4 flat across columns [E35].
- Output layer: left/right logits track ball column but are velocity-modulated and asymmetric; no-op often wins near center/uncertain cases, and up/down are usually low [E10, E14, E23, E24, E30].
- Overall: Breakout-like first-layer layout (agent bottom row, bricks top rows, obstacles weak border, moving-object weights interior) plus partial/asymmetric horizontal paddle steering; not a collection game [E38, E10, E14, E24, E29, E35].