# Findings
- W1 row norms are nearly flat across channels and border/interior (E1, E4, E12, E22), so there is no clear learned maze, wall layout, or localized object detector.
- Top W1 rows are scattered across interior and border cells (E1, E4), not concentrated on a game-specific object or path.
- W3 has the largest column norm for left (8.01) and b3 suppresses left (-0.87), yet the effective default is strongly left, not no-op: P(left)=0.998 empty (E17, E26), 1.000 agent_center, and 0.999 agent_left (E27).
- Agent position modulates the action: center/left/bottom are left-dominant, while agent_top flips to up (P(up)=0.962); agent_right stays left but raises P(up) to 0.211 (E27).
- With an agent present, reward/obstacle probes show no consistent approach/avoidance: reward_right has no effect, near-left reward keeps argmax left (P(left)=0.648, P(up)=0.348), and near-left obstacle keeps P(left)=0.995 (E27).
- E26’s empty-agent near-left reward/obstacle flips to up (P(up)=0.972 and 0.927) do not persist when the agent is present (E27), so they are empty-agent artifacts; moving-object probes also remain left-dominant, giving no Pac-Man ghost avoidance or Sokoban box pushing (E17, E26, E27).
- All five channels affect logits (E14), but the previous-frame channel is not used for self-motion in multi-cell agent tests (E16).
- Game identification is not established; the channel set fits a grid game with agent, moving objects, reward, obstacle, and previous frame, but E17/E26/E27 give no support for a Pac-Man-style policy. Confidence: low.