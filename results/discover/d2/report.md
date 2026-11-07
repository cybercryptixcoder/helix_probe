# Discovery report: runs/discover/d2
- experiments: 40; entries: 24 (24 measured); verified and specific: 2 (verified, specific or not: 4)
- yield: 0.05 verified entries per experiment
- verified by depth (verified / measured): {'input': (0, 1), 'output': (2, 2), 'internal': (0, 21)}
- distinct (depth, mechanism) among verified: 2
- thresholds: {"feminine": 0.1, "masculine": 0.1, "plural": 0.1, "past": 0.1, "opposite": 0.1, "comparative": 0.1, "people": 0.1, "general": 0.1, "capital": 0.1, "language": 0.1, "element": 0.1, "weekday": 0.1, "month": 0.1, "letter": 0.1, "addition": 0.1, "subtraction": 0.1, "multiplication": 0.1, "comparison": 0.1, "successor": 0.1, "predecessor": 0.1, "double": 0.1, "one_digit_addition": 0.1, "french": 0.1, "color": 0.1, "sentiment": 0.1, "young_animal": 0.1}
- discovery curve (verified entries after each experiment): [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2]

| id | depth | name | where | predicted | real effects (held-out) | verified | specific |
|---|---|---|---|---|---|---|---|
| E2 | internal | sentiment rank-one down_proj edit | mid/late layer's MLP down_proj weight (best separation layer | {'sentiment': '+'} | sentiment -0.14 | False | False |
| E4 | internal | sentiment rank-one attention-output edit @ L16 | layers[16] attention output projection weight (the (4096, k) | {'sentiment': '+'} | sentiment -0.14 | False | False |
| E5 | internal | sentiment rank-one attention-output edit @ L16 | layers[16].linear_attn.out_proj.weight (4096, 4096), rank-on | {'sentiment': '+'} |  | False | False |
| E6 | internal | successor/predecessor direction injected into mid/late mlp.down_proj | layers[best] (second half of the stack).mlp.down_proj.weight | {'predecessor': '-', 'successor': '+', 'addition': '+', 'subtraction': '+', 'comparison': '+'} |  | False | False |
| E7 | internal | gender-direction rank-one write into mlp.down_proj @ best layer | layers[best].mlp.down_proj.weight (4096, 12288), rank-one ou | {'masculine': '-'} |  | False | False |
| E8 | internal | gender direction written into second-half attention-out / MLP-down ports | layers[L].mlp.down_proj.weight (4096,12288) and layers[L] at | {'masculine': '-', 'feminine': '-'} |  | False | False |
| E9 | internal | arithmetic operation-type direction (addition − subtraction) rank-one write into second-half mlp.down_proj | layers[best in second half].mlp.down_proj.weight (4096, 1228 | {'subtraction': '-'} |  | False | False |
| E10 | internal | domain-general before/after direction written into L19 mlp.down_proj | layers[19].mlp.down_proj.weight (4096,12288), rank-one outer | {'predecessor': '-', 'weekday': '-', 'month': '-', 'letter': '-'} |  | False | False |
| E11 | output | output-row swap positive/negative | lm_head.weight rows of the answer tokens " positive"/" posit | {'sentiment': '-'} | sentiment -1.00 | True | True |
| E12 | input | input-embedding antonym row swap | `model.embed_tokens.weight` rows of the tokens for up/down,  | {'opposite': '-'} | comparative -0.14 | False | False |
| E13 | internal | colour-selective MLP-neuron column ablation @ best layer | `layers[L].mlp.down_proj.weight` columns (intermediate-neuro | {'color': '-'} | feminine -0.28, comparative -0.14, french -0.11 | False | False |
| E16 | internal | attention-head successor ablation (top-aligned out_proj column slices) | `layers[L].self_attn.o_proj.weight` / `layers[L].linear_attn | {'successor': '-'} |  | False | False |
| E20 | internal | L27 attention head-group ablation (opposite) | `layers[27].self_attn.o_proj.weight` (4096,4096), output-col | {'opposite': '-', 'comparative': '-', 'plural': '-'} |  | False | False |
| E21 | internal | L22 MLP input-projection (up_proj) ablation | `layers[22].mlp.up_proj.weight` (12288, 4096), entire matrix | {'color': '-'} |  | False | False |
| E22 | internal | L27 attention query-projection (pattern) ablation | `layers[27].self_attn.q_proj.weight` (4096, 4096) — all 32 h | {'opposite': '-'} | young_animal -0.93, people -0.86, capital -0.83, letter -0.72, general -0.71, language -0.64 | True | False |
| E23 | internal | L27 attention value-projection ablation | `layers[27].self_attn.v_proj.weight` (1024, 4096) — the KV-h | {'opposite': '-'} |  | False | False |
| E26 | internal | 4-layer block ablation of the MLP output write | `layers[L].mlp.down_proj.weight` (4096,12288) zeroed for all | {'month': '-', 'weekday': '-', 'color': '-'} | masculine -0.61, comparative -0.43, double -0.33, letter -0.22, young_animal -0.21, predecessor -0.17 | False | False |
| E29 | internal | L0 MLP input-gate (gate_proj) ablation | `layers[0].mlp.gate_proj.weight` (12288, 4096), entire matri | {'weekday': '-'} | feminine -0.11, masculine -0.11 | False | False |
| E30 | internal | L21 linear-attention short-conv ablation | layers[21].linear_attn.conv1d.weight (8192,1,4), all channel | {'weekday': '-'} |  | False | False |
| E31 | internal | L21 linear-attention output-write ablation | `layers[21].linear_attn.out_proj.weight` (4096,4096), all to | {'weekday': '-'} |  | False | False |
| E32 | internal | weekday circuit triple ablation (L0 MLP gate + L21 linear-attn qkv + L21 linear-attn conv) | `layers[0].mlp.gate_proj.weight` (12288,4096), `layers[21].l | {'weekday': '-'} |  | False | False |
| E35 | internal | L0 MLP output-write (down_proj) ablation | `layers[0].mlp.down_proj.weight` (4096,12288), entire matrix | {'weekday': '-'} | feminine -0.11, masculine -0.11 | False | False |
| E36 | internal | L28–31 attention output-write block ablation | `layers[28..30].linear_attn.out_proj.weight` and `layers[31] | {'letter': '-', 'addition': '-', 'multiplication': '-', 'comparison': '-', 'one_digit_addition': '-'} | plural -1.00, addition -1.00, subtraction -1.00, multiplication -1.00, successor -1.00, predecessor -1.00 | True | False |
| E39 | output | unembedding colour-class row negation | `lm_head.weight` rows of the single-token colour words (red, | {'color': '-'} | color -0.86 | True | True |
