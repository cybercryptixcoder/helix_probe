# Findings
- Policy logits depend strongly on agent position even on an otherwise empty board: per-action std 1.46–2.28, not <0.1 [E1].
- Position changes action gaps/rankings, not just a constant offset; small W1 weights do not imply position-invariant logits [E1].
- Empty/baseline boards share a global bias: action 0 highest and action 4 lowest in E1/E2/E14 baselines [E1, E2, E14].
- Top W1 row norms concentrate in channel 4 row 7 and channel 1 rows 3–6, not channels 2–3 near the agent [E2].
- Channel-1 object presence has large, row-dependent effects; in E14 at column 5, rows 1–7 all make action 3 (left) the argmax, including row 7 just above the agent, so it is not lane-based up/down avoidance or chasing [E14].
- Channel-1 effects are not a simple move-away/toward signal: shifts can be large positive across actions, usually largest for left but at (-1,+1) largest for right, and magnitude is nonmonotonic with row (strong at rows 3/5/6, weaker at 1/2/7) [E2, E14].
- Channel-2 reward effects are small and show no clear move-toward preference; channel-3 obstacle effects are near zero with no clear avoidance [E2, E14].