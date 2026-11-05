# Findings
- For paddle center col4 and ball at (4,7), action 3 (left) is highest (0.462), while action 4 (right) is near zero (0.012) [E1].
- For paddle center col4 and ball at (4,1), action probabilities are near-uniform (0.168–0.216), with action 4 (right) only marginally highest [E1].
- For paddle center col4 and ball at (4,4), action 4 (right) has probability 1.0 and all other actions have probability 0 [E1].
- With ch4=current frame, the single-ball sweep gives mixed/away argmax across ball columns, not a consistent toward-ball policy; with ch4 empty, ball columns 1–3 give action 3 (left) probability 1.0 [E4].
- With agent correctly on bottom row (8,4), ball at row 4, and previous ball position supplied in ch4, action 3 (left) is the argmax for nearly all ball columns, including right-side columns 7–8; scores are near-uniform (~26–43) and do not show rightward steering toward right-side balls [E7].
- W1 norm mass is dominated by ch1 moving-object (577) and ch4 previous-frame (570), over ch2 reward (94.8), ch0 agent (76.8), and ch3 obstacle (45.1); top ch1 cells are row4/6, and top ch4 cells are row7 cols4–7 [E5].
- Reward (ch2) probes at agent (4,4) all argmax action 3 (left) for reward at R/L/U/D, so the network does not steer toward reward targets [E5].
- Enemy (ch1) probes flee horizontally (enemy R→left argmax 3; enemy L→right argmax 4), but U/D are near-uniform with marginal right argmax, so there is no vertical flee [E5].
- Overall, the network is neither a simple horizontal Breakout toward-ball controller nor a simple 2D reward-chase/enemy-flee controller; correct bottom-row placement plus previous-ball input does not produce Breakout-style toward-ball steering [E1, E4, E5, E7].