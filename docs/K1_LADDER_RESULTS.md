# K1 hint-ladder experiment (2026-11-13)

Script: `lab/experiments/k1_ladder.py`. Reader: DeepSeek V4.1 Flash, thinking high. Python mode = the reader writes code against the weights and cannot run the network; the slide is empty. Run ids are in `lab/experiments/k1_ladder_runs.json`, with full traces in `lab/runs/`.

Rungs: **L0** no hints (architecture shapes only). **L1** input layout only: a 10×10 grid with 5 unnamed channels, and the flattening order. **L2** full MIT context (channel names, actions).

| Network | Rung | Mode | Answer | Verdict |
|---|---|---|---|---|
| Breakout | L0 | text | 5-class MNIST digit classifier | ✗ |
| Breakout | L1 | text | 5-class classifier of shapes on 10×10 grids | ✗ |
| Breakout | L0 | python | RL policy on a 10×10 gridworld, 5 tile categories, 5 actions | structure ✓, game not named |
| Breakout | L1 | python | bottom-row paddle agent, left/right actions; "simplified Breakout or Space Invaders", 85% | ✓ (near-named) |
| Breakout | L2 | python | Breakout | ✓ |
| Breakout, shuffled | L1 | python | no spatial or channel selectivity; output depends only on aggregate activation | ✓ control |
| Pong | L0 | text | 5-class text sentiment classifier | ✗ |
| Pong | L1 | text | MinAtar Freeway, 93% | ✗ (confidently wrong) |
| Pong | L0 | python | gridworld navigation policy (walls, agent, goal) | structure ✓, game ✗ |
| Pong | L1 | python | gridworld maze navigation, Q-values for 5 actions | structure ✓, game ✗ |
| Pong | L2 | python | single-paddle Pong | ✓ |
| Pong, shuffled | L1 | python | "a random/untrained network" | ✓ control |
| Mod-add transformer | arch only | python | (t0 + t1) mod 113; Fourier frequencies 8, 11, 22, 23, 25; rank-1 attention selects the addends; MLP uses product-to-sum identities; Fourier-matched unembedding | ✓ mechanism (prior-only control still needed) |
| Mod-add, shuffled | arch only | python | additive token score, no modular structure | ✓ control |

## Findings

1. **Text mode cannot read 17K weights.** It miscounts, then fills the gap from dataset priors (MNIST, sentiment). This is a format problem, not a reading problem.
2. **Python mode reads structure blind.** With no hints it recovered the 10×10×5 grid, the 5 actions and "an RL policy" for both games, and both shuffled controls were correctly rejected.
3. **Naming the exact game needs input semantics.** That is underdetermined by the weights, not a reading failure: L1 got Breakout nearly right but not Pong, and L2 named both.
4. **Mod-add mechanism recovered from weights alone**: the frequencies, the attention and the MLP mechanism, with the shuffled control negative. Caveat: the reader may know Nanda et al., so a prior-only control (task named, no weights) and mod-mul are next.

## Implications

- Make python mode with an empty slide the default way to read.
- Ask for structure and mechanism rather than "name the task".
- That is exactly what a construction needs.
