# Findings

**Output layer**
- Sentiment is a linear readout at the unembedding: swapping the lm_head rows for " positive"/" negative" flips sentiment by −1.00 with nothing else touched [E2].
- That remains the only clean, selective, verified causal site in the map [E2].

**Input layer**
- Arithmetic needs the number tokens' input embeddings: zeroing every numeric row of `embed_tokens` drops addition, multiplication, comparison, successor and predecessor to −1.00 [E5].
- Internal arithmetic effects are broad: L0 `out_proj` top-256 subspace removal drops addition −20.5, multiplication −21.0, one_digit −19.9 plus many non-arithmetic families [E37]; zeroing full-attention v/o at the 8 full-attention layers drops addition −8.89, multiplication −6.44, factual −4.80, with morphology not collapsed (+0.24) [E39]. Other internal arithmetic interventions did nothing [E1, E6, E30] or moved morphology [E27, E16].

**Layer 0 is the dominant shared hub, but its top subspace is broad**
- Layer 0's `linear_attn.out_proj` is a broad shared write: zeroing it moves arithmetic (addition −21.1, multiplication −20.2), factual (color −10.9, capital −7.1), opposite (−8.5) and plural (−6.0) [E34].
- Removing its top-256 singular subspace alone reproduces much of that broadly: addition −20.5, multiplication −21.0, one_digit −19.9, general −15.6, element −10.4, capital −9.2, language −8.8, young_animal −8.5, weekday −7.3, letter −6.7, month −6.4, opposite −6.0 [E37].
- That top-256 subspace is not the whole write: color (−1.7), sentiment (−1.0), french (−2.5), masculine (−1.0) are weak there; plural (+1.0), feminine (+4.1), comparative (+3.7) move opposite, and past falls −4.1 [E37 vs E34].
- Layer-0 effects are not dissociable by value head: zeroing head 26 gives arith mean −0.14, color +0.31, young_animal −0.37, and a control head gives the same nothing [E35].
- The earlier "head 26 carries color/french/young_animal" attribution does not survive a single-head test [E35 vs E30].

**Morphology is spread, not localised**
- Zeroing all 24 GatedDeltaNet `out_proj` writes kills all five morphology behaviours at −1.00 [E10].
- Zeroing `v_proj` or `o_proj` at the 8 full-attention layers gives identical results and does not kill morphology: morph +0.24, factual −4.80, arithmetic −7.66 [E39].
- This contradicts E25's reported full-attention `o_proj` morphology collapse (−1.00); the earlier "morphology redundantly carried by both attention families" claim is not supported [E25 vs E39].
- Zeroing only the top-3 morphology linear layers (L0 excluded) gives just morph −1.95, while `opposite` falls −5.03 and arithmetic only −1.58 [E34].
- `opposite` tracks the morphology layers more closely than morphology itself does [E34].
- L0's top-256 subspace carries `opposite` (−6.0) but not morphology uniformly: feminine/comparative/plural move positive, masculine/past negative [E37].
- E39's v/o zeroing moves past −4.00 but leaves feminine/masculine/plural/comparative near baseline, so "morphology" mean masks uneven effects [E39].

**MLP sites are weak and cross-family**
- The best MLP morphology site (top-2 layers) gives french −0.83, capital −0.44, young_animal −0.36, masculine −0.33, feminine −0.22 [E12].
- The best MLP factual site (top-3 layers) gives capital −0.56, french −0.39, feminine/masculine/past −0.22 [E3].
- The best MLP arithmetic site (top-3 layers) moves morphology, not arithmetic: feminine −0.50, masculine −0.44 [E27].
- Single-layer 31 `down_proj` zeroing moves french −0.83, young_animal −0.57, capital −0.44 — not the predicted factual set [E8].
- Amplifying layer-31 "morphology" neurons hurts arithmetic instead: comparison −0.56, predecessor −0.56, successor −0.44, double −0.44 [E16].
- Zeroing the paraphrase-robust layer-31 morphology neurons does nothing at all [E17].

**Linear-probe directions do not ablate**
- Projecting out the sentiment residual direction at every residual write (three separate attempts) produces zero effect [E9, E11, E14, E18].
- Projecting out the arithmetic residual direction at every write produces zero effect [E1].
- Decodability of a direction in the residual stream does not imply that direction is used [E9/E11/E14/E18 vs E2].

**Single-site ablations mostly fail; broad joint or subspace ablations move many behaviours**
- Attention head ablations at factual sites: no effect [E4, E7, E23, E30].
- The most ordinal-selective single attention write (L6) gives ord −0.71, factual control −0.26, arithmetic +0.02 — indistinguishable from noise [E36].
- Joint top-3 factual-site ablation moves all six "unlocated" behaviours (letter −9.0, weekday −10.0, month −7.3, language −6.0, element −9.9, general −9.4) but also flattens morphology at −1.00 [E31].
- Joint top-2 sentiment MLP layers drop sentiment −1.11 but also factual −10.1 and arithmetic −11.5 [E32].
- Top-8 factual heads per full-attention layer drop color −6.6 and young_animal −7.3, but also successor −4.6, predecessor −4.7, double −4.4, one_digit −3.1 [E33].
- L0 `out_proj` rank-256 removal is a single-tensor subspace ablation that moves many families at once; it is broad, not selective [E37].
- Full-attention v/o zeroing is also broad and non-selective: arithmetic −7.66, factual −4.80, morphology +0.24 [E39].

**Asymmetries worth noting**
- Feminine and masculine are not a pair: layer-0 ablation moves feminine −3.77 but masculine only −0.63 [E34]; removing L0 top-256 subspace raises feminine +4.12 but lowers masculine −1.03 [E37].
- Early-layer "anti-morphology" write removal does not raise morphology; it lowers it (masculine −0.28, feminine −0.22) [E13].
- Several behaviours sit near zero margin at baseline (plural −1.44, past −0.81, french −3.47, feminine +0.81), so weak effects on them are hard to distinguish from noise [E34, E35, E36 baselines].

**Routing vs value write in full attention (E39)**
- E39 tested q/k/v/o at the 8 full-attention layers: v and o zeroing are identical and do not collapse morphology; they drop arithmetic −7.66 and factual −4.80, morph +0.24 [E39].
- E25's full-attention `o_proj` morphology collapse did not replicate under E39's same-layer test; the simple value-write account of full-attention morphology is not supported [E25 vs E39].
- The q/k uniform-attention result does not rescue E25's value-write claim; the E25/E39 conflict needs replication before full-attention morphology necessity is settled [E25 vs E39].

**Still unexplored**
- No verified internal entry isolates any single behaviour; every large internal effect so far is broad and cross-family [E31, E32, E33, E34, E37, E39].
- No entry tests `mlp.up_proj` or `mlp.gate_proj`; all MLP work is on `down_proj` only [E3, E8, E12, E15, E16, E17, E27, E32].
- E39 separates q/k/v/o at the 8 full-attention layers; per-head routing inside linear attention remains untested.
- Subtraction, comparison, successor, predecessor and double have no internal site of their own — only the shared input-embedding result [E5].
- Language, element and general now have a broad internal site in L0 `out_proj`'s top-256 subspace, but no selective one [E37].
- Rank-256 subspace removal has been tried at L0 `out_proj`; rank-one and row-swap interventions remain untested at internal sites [E37].
- E37 decomposes L0 `out_proj` by top singular input→output directions; matched random and keep-top controls are still needed.
- E25/E39 conflict needs replication/explanation before full-attention morphology necessity is settled [E25 vs E39].