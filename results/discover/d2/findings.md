# Findings

**Output stage**
- Swapping the two `lm_head` rows for " positive"/" negative" flips sentiment 1.00→0.00 and leaves all nine control behaviours unchanged; sentiment is read out of two specific output rows (E11).
- The same swap leaves capitalised/unprefixed answer-word preference untouched, so it is a narrow write port, not general lexical disruption (E11).

**Input stage**
- Swapping token-embedding rows of antonym pairs changes which word the model reads: after the swap `ask` returns the prompt word itself for probes it used to answer correctly (fast→"fast" not "slow"), while 14 controls are unchanged (E12).
- The embedding swap moved only 1 of 4 antonym probes; the input embedding row is a real but partial determinant of the antonym answer (E12).

**Internal rank-one writes (all negative)**
- Rank-one sentiment writes into mid/late `mlp.down_proj` (E2), L16 attention-out (E4), and `layers[16].linear_attn.out_proj` (E5) do not raise sentiment; effects are −0.14, −0.14, and none.
- Successor/predecessor (E6), gender (E7, E8), addition−subtraction (E9), and before/after (E10) rank-one writes into internal ports move none of their target behaviours.
- Conclusion: no rank-one write into any internal port has produced a verified behavioural change; verified internal entries so far come only from necessity ablations (E16–E21).

**MLP down_proj redundancy**
- Zeroing one layer’s entire `mlp.down_proj` at a time across all 32 layers leaves 11 of 12 probes at baseline at every layer; the exception is colour, which drops only when L22’s `mlp.down_proj` is zeroed (E18).
- Zeroing the top-1024 colour-aligned `mlp.down_proj` columns at L31 leaves colour at 1.0 with all 17 controls intact; colour is not implemented by the most colour-selective MLP neurons at that layer (E13).

**MLP input projections (gate/up)**
- Full layer×`gate_proj` and layer×`up_proj` zeroing sweeps now exist; the MLP input side is not redundant (E21).
- `gate_proj` L00 zeroing drops weekday; an additional gate_proj summary line (label truncated in the log) reports a base-1 behaviour dropping at L21 and L27 (E21).
- `up_proj` zeroing drops weekday at L0 and L21, and month at L10, L22, and L26 (E21).
- Zeroing L22 `up_proj` drops colour 1→0 and month 1→0 in the printed post-state; the script reports `changed 1`, which conflicts with that two-probe change (E21).
- Colour at L22 is reproduced on the MLP input side (`up_proj`) as well as `down_proj`, but L22 `up_proj` also affects month (E21).

**Attention output necessity**
- Zeroing the entire attention output projection (`o_proj`/`out_proj`, all head slices) one layer at a time across all 32 layers leaves most probes at baseline; `opposite` drops at L27 (E19). Restoration returns all probes to baseline (`changed 0`).
- At L27, `opposite` is localised to head 8: E20 baseline `opp` is 0.25; zeroing head 8 alone drops it to 0.00; top-4/top-8/all-32 also give 0.00; bottom-16 leaves it at 0.25; eight controls are unchanged (E20).
- Zeroing 16 of L31’s 32 attention-out head slices drops successor 1.00→0.50 with predecessor, addition, capital, sentiment, colour and weekday unchanged (E16).
- The same half-head ablation at L8, L16, L20, L24, L28, L29 and L30 changes nothing; the complementary half at L31 also changes nothing; only all 32 heads at L31 together drop successor to 0.75 (E17).
- Successor is not carried by any single head or narrow head group; the L31 attention write is a bottleneck for it, not a localised store (E16, E17).
- Unembedding-direction alignment gave all-zero scores concentrated at L31, so it does not identify the heads that matter (E16).
- Full attention-out sweep maps every layer: L27 attention-out, specifically head 8, is necessary for `opposite`; L31 broad attention-out is necessary for `successor` (E16, E17, E19, E20).

**Attention input/query pattern**
- Zeroing all L27 `q_proj` rows changes one parameter tensor but leaves all listed probes at baseline, including `opposite`; no single head’s query replacement drops `opposite` (E22).
- L27 head 8 output necessity for `opposite` is therefore not explained by its query pattern/where it attends; L27 `q_proj` is not a verified behavioural handle (E20, E22).
- E22’s module inventory shows self-attention `q_proj` (8192,4096), `k_proj`/`v_proj` (1024,4096), `o_proj` (4096,4096), plus `q_norm`/`k_norm`; linear attention has `conv1d`, `norm`, `out_proj`, `in_proj_qkv`, `in_proj_z`, `in_proj_b`, `in_proj_a` (E22).

**Baseline limits**
- `past` and `feminine` sit at 0.00; `plural` is at 0.00 in E19/E21 and at most 0.50 in earlier baselines, so no intervention can be verified as changing them in either direction.
- `opposite` baseline is setup-dependent: 0.25 in E20 and 1.0 in E22; E20 verifies a 0.25→0.00 drop, not a full 1.00→0.00 effect.

**Still unexplored / updated**
- No verified rank-one internal write exists. Verified internal causal handles are necessity ablations only: L27 head 8 attention-out for `opposite`, L31 broad attention-out for `successor`, L22 `mlp.down_proj` for `colour`, L22 `mlp.up_proj` for `colour`/`month`, and `gate_proj`/`up_proj` layer handles for `weekday`/`month` (E16–E21); L27 `q_proj` is not a handle (E22).
- Component-necessity maps now exist for `mlp.down_proj` (E18), the full attention output projection (E19), `mlp.gate_proj`/`up_proj` (E21), and L27 `q_proj` (E22, no effect); attention query/input beyond L27 `q_proj`, `act_fn`, and the residual stream remain unmapped.
- `opposite` now has an internal attention-out handle at L27 head 8 in addition to its partial input-row handle (E12); its L27 query pattern is not necessary (E22); `sentiment` remains an output-row handle (E11).
- The factual behaviours (capital, language, element, people, general, young_animal, french) still have no verified localised substrate: no drop is reported for them in the single-layer MLP ablations or rank-one writes attempted.