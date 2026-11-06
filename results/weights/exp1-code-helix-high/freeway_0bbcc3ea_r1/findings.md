# Findings
Observations:
- Channel 0 (agent) has interior weights, not wall-border weights: border mean 0.351 vs interior mean 6.895, with top cells around rows 4–8, columns 3–5 [E2].
- Channel 2 (reward) is almost entirely row 1: row mean norm 49.58 vs ~4–5 elsewhere, uniform across interior columns (row-1 norms 54.8–65.9; within-column cosine 0.928), and row-1 effective weights favor action 1 “up” (+43.7) while opposing action 2 “down” (−13.7 to −18.1) [E3, E5, E11].
- Channel 3 (obstacle) is wall-only: border max 64.67 vs interior max 8.49, so there are no interior water/obstacle cells [E3, E5].
- Channels 1 and 4 (moving objects and previous frame) have elevated weights in rows 2–7 with broad column coverage: CH1 row mean abs [1.6, 1.5, 24.6, 42.2, 36.8, 35.1, 34.2, 36.3, 1.4, 2.2] and CH4 similar [2.0, 1.7, 27.1, 35.0, 38.2, 33.5, 34.4, 35.3, 27.4, 1.5] [E3, E6, E8].
- CH1→CH4 shifts do not show dominant horizontal motion: E19 finds 12 horizontal vs 11 vertical vs 5 zero shifts, mean |dx| 1.47 ≈ mean |dy| 1.34, mean best corr 0.48; earlier shift/neighbor-correlation tests were also mixed/weak, and CH1 within-row similarity is not stronger than between-row (0.407 vs 0.407) [E9, E10, E11, E12, E19]. This does not confirm horizontally moving cars.
- Output bias b3 = [−0.029, 3.142, −1.862, 0.173, −1.269] strongly favors “up” and disfavors “down,” consistent with an upward-crossing policy; all output columns are used (W3 column norms 5.2–7.2) [E2].

Reasoning:
- A uniform top-row reward plus a wall-only obstacle channel rules out Frogger-style discrete home slots/interior water and interior-obstacle maze/collecting games.
- Rows 2–7 object/previous-frame bands between a lower start and top goal, plus the strong upward bias, still fit an upward road/highway crossing.
- E19 weakens the Freeway-specific claim of encoded horizontal car motion: the network may represent lane occupancy or mixed/weak motion rather than dominant horizontal traffic direction.

Game: Freeway (horizontal traffic motion not confirmed in weights).
Description: The agent controls a character starting below a multi-lane highway and moves upward across rows of moving cars to reach the top row; reaching the top gives reward, while collisions with cars impede or reset the crossing.
Confidence: 80%