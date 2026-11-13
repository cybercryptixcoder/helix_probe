# K1 state of the art: what happens when LLMs are handed weights (as of 2026-11-13)

Synthesised from the entries in this folder (see `INDEX.md`). Keys point to entries. Numbers are as the entries report them.

## 1. What has been tried

| Source | Reader(s) | Target | Format / access | Result |
|---|---|---|---|---|
| Sparks Exp 1–2 (blog-rikiyat-…) | GPT-6 Astra | 17K-weight PPO game MLPs; 24K-weight shape DDPMs | Text, 3 decimals, one unlabelled line per matrix row, about 74K–100K tokens; no tools | 4/4 games, 3/3 shapes (drew outlines for filled shapes) |
| Sparks Exp 3 | GPT-6 Astra | 7M-param char transformer (no embed/unembed) | Python on tensors, no forward passes; 3-candidate corpus menu plus head-label menu | 6/6 corpus; copy heads exact |
| Willison (blog-simonwillison-…) | Qwen 3.8 27B local, Kimi | Sparks Exp 1 prompts | Same text; about 105K tokens | About 3/4 games |
| andsalazar replication (github-andsalazar-…) | Astra, Kimi, GLM, **DeepSeek**, Qwen | Sparks Exp 2 plus fresh nets, a new shape and a shuffled control | Same text, 16K→64K output | Astra 6/6, declined the shuffled control; Kimi 4/8, GLM 2/8, **DeepSeek 0/8**, Qwen 0/8 |
| Reading audit (arxiv-2611.08070) | Claude Opus 5.5 | About 125K-weight CNNs on several datasets | Labelled text, 3 decimals, no tools | Real local arithmetic at the network's edges, but **dataset priors**: permuted labels → wrong names; KMNIST read as MNIST, SAT-6 as CIFAR |
| Clinical audit (arxiv-2611.05341) | Opus/Sonnet/Haiku 5.5 etc. | 433-param MLPs with planted flaws | Labelled rows, 4 decimals, no tools | Flaw found in 16/18; healthy nets cleared only 2/5 unforced; simple weight statistics found the same flaws |
| EEG/ECG (arxiv-2611.13758) | Opus 5.5, GLM, **DeepSeek V4.1 Flash** | 2.7K-weight EEG conv nets | Text, 3 s.f., no tools | **No model named the task.** DeepSeek 0–11%, with 12 non-answers |
| Orbit audit (arxiv-2611.05798) | Codex readers | 129-param ReLU fields, 6-way shape menu | Raw weights | 35–87% with weights vs 2–17% redacted; function-preserving permute/rescale drops accuracy (Terra 70→48%); repeat prompts disagree 8–38% |
| Singh, systematic tests (blog-csinva-…-systematic-tests) | Opus 5.5 | 300+ edits to Qwen3.5-0.8B | Raw weights only | Edit-effect prediction barely above a no-weights control (Spearman 0.17 vs 0.11). Given the true hidden state: 0.97. **The missing activation is the bottleneck.** |
| WSPBench (github-alexcarterhq-…, blog-wspbench-com) | GPT-6 family | Boolean ReLU circuits (4K scalars); repair controllers | No tools vs tensor tool vs instrumented | Read v0.2.1: 0/4 exact. Larger output budgets turned weight access from a loss into a gain. The tensor tool halved cost. |
| ttm lab (github-ttm-…) | Qwen 0.6B / 1.5B | Hand-built 4-4-1 Boolean nets | Python lists | 0 exact; models copy the prompt or collapse to all-zero |
| Krentsel (x-alexkrentsel-…) | Many generations | Writing (Breakout) | — | A step change: only the newest frontier models clearly work |

## 2. What this means for our K1 (and the lab)

1. **DeepSeek V4.1 Flash is a weak raw-text reader on the record**: 0/8 on shapes; 0–11% plus many non-answers on EEG. Its main failure is spending the whole output budget copying weight rows. Expect this, and treat it as data rather than a bug. Give large output budgets, and make the code-sandbox mode first-class.
2. **Prompt leakage is the biggest confound.** Named input channels (Sparks Exp 1), electrode names, canonical shapes (32×32×3 → 10) and candidate menus all let priors answer the question. The lab should let us switch each of these off.
3. **Controls everyone now uses**, which the lab should make one click away:
   - shuffled weights (within tensor);
   - untrained network;
   - no-weights / prompt-only;
   - label permutation;
   - function-preserving reparameterisation (permute and rescale hidden units);
   - repeat runs (agreement baseline).
4. **Format details that matter:** precision (3 decimals is standard); labelled vs unlabelled rows (unlabelled rows force line-counting); whether tensor headers give shape and meaning; and output budget (WSPBench needed 24K+; andsalazar retried at 64K).
5. **Tools help.** A tensor tool halved WSPBench cost. Rich probes were decisive in the EEG diagnosis experiments. Singh shows raw weights cannot predict edit effects without activations, which matters for our later loop.
6. **Nobody has run a systematic prompt or format ablation.** Every source ran one fixed prompt (WSPBench varied only budgets). That is open ground for us.
7. **Nobody has tried reading an algorithmic transformer whose mechanism is known**, e.g. Fourier modular addition. Our K0/K1 target is untouched territory.
