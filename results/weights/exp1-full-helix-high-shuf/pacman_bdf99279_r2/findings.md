# Findings
- W1 row norms are nearly flat across channels and border/interior (E1, E4, E12), so there is no clear learned maze, wall layout, or localized object detector.
- Top W1 rows are scattered across interior and border cells (E1, E4), not concentrated on a game-specific object or path.
- W3 has the largest column norm for left (8.01) and b3 suppresses left (-0.87), but synthetic empty states are strongly left-dominant (P(left)=0.841, P(right)=0.000), so the effective default is left rather than no-op (E1, E17).
- Reward and moving-object probes do not show consistent approach/avoidance: right-side reward gives P(right)=0.001, right-side box gives P(right)=0.002, and box+goal gives P(right)=0.005 with left still dominant (P(left)=0.614) (E4, E17).
- E17 contradicts Pac-Man ghost avoidance and Sokoban box pushing: the policy neither avoids the moving object nor pushes it toward reward when the reward lies beyond it.
- All five channels affect logits (E14), but the previous-frame channel is not used for self-motion in multi-cell agent tests (E16).
- Game identification is not established; the channel set fits a grid game with agent, moving objects, reward, obstacle, and previous frame, but E17 removes support for a Pac-Man-style policy. Confidence: low.