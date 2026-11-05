# Findings
- Channel 0 (agent) weights are concentrated at column 1 (mean norm 3.94 vs ~0.35 elsewhere), consistent with a vertically moving left paddle [E12].
- Channel 1 (moving object) has strong interior row structure and a column gradient peaking at columns 2–4 (7.05, 6.99, 5.57), so ball position matters most near the left side [E12].
- Channel 4 (previous frame) has large column-structured weights peaking around columns 5–6 and can affect action choice [E7, E12].
- Channel 2 (reward targets) is weak (mean 0.40); channel 3 is border-related (border 0.79 vs interior 0.35), so there are no strong interior reward-target or obstacle signals [E12].
- Except near walls, the policy does not select left/right for balls directly left/right or near the paddle; argmax stays up/down/no-op [E5, E6, E13].
- Near the left paddle (ball columns 2–3, tested non-wall rows), vertical action follows the ball row: above -> up, below -> down; same row defaults to up, and horizontal movement direction does not change this [E13].
- Outside that near-left-paddle regime, vertical responses are mixed and depend on exact agent/ball coordinates: above can give no-op or down, and below can give no-op or up [E1, E5, E6, E17].
- Previous-frame motion can override the current row at (2,4): prev (1,4) gives down with probability 0.999, prev same gives up, prev above gives no-op [E7].
- Near top/bottom walls the policy does not show bounce anticipation: top moving up -> right (0.30) not down, top still -> left (0.224), bottom moving down -> right (0.275) not up, bottom still -> down (0.248), with near-uniform probabilities [E17].