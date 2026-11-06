# Findings
- Channel weight totals rank CH0 (agent) ≫ CH4 (prev) > CH1 (moving) > CH3 (obstacle) > CH2 (reward) [E1, E2].
- CH0 (agent) is strongest in central/interior cells, topped by (6,3), (6,4), (6,5), (5,5) [E1, E2].
- CH1 (moving) norms are structured over interior rows, topped by (3,6), (3,2), (6,8), (6,4); its effective up weights are near zero in rows 1 and 8 and strongly negative across rows 2–7, with no opposite-sign horizontal bands [E1–E4].
- CH2 (reward) is the weakest channel and is concentrated in row 1, cols 1–8, not broadly over playable cells [E2, E3].
- CH3 (obstacle) weights form a boundary ring on rows 0/9 and cols 0/9, not fixed inner maze/wall cells [E2, E3].
- CH4 (prev) is broadly structured over interior cells, topped by (5,2), (4,7), (3,8), (8,5) [E1, E2].
- Action bias b3 is strongly positive for action 1 (3.14) and negative for actions 2 and 4 (−1.86, −1.27) [E1, E2, E3].
- Effective action weights are dominated by CH0/CH1 central cells; CH0 action 1 is negative at (3,4), (5,6), (6,7), while CH1 action 1 is negative at (3,6), (3,2), (7,4), (7,8) and broadly across CH1 interior rows [E2, E4].