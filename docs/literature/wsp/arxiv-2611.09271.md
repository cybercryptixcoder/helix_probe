# Zero-Shot Weight-Space Programming Across a Difficulty-Graded Ladder of Two-Player Games

- **Key:** arxiv-2611.09271
- **Authors / organisation:** Eduardo C. Garrido Merchán; Universidad Pontificia Comillas (IIT, DIGNUM), Madrid
- **Date:** 2026-11-09 (v2; v1 date not checked)
- **Link:** https://arxiv.org/abs/2611.09271
- **Kind:** paper
- **Read from:** full text (arXiv HTML v2). Figures read via captions and embedded text. The paper refers to released networks, oracles, a replication brief and a Track B prompt pack, but gives no URL in the text or on the abstract page; those were not found and not read.
- **Relevance to us:** 2 (useful) — it is about writing networks, not reading them.

## What they wanted, and why
The paper asks where weight-space programming (here: setting every weight of a feed-forward ReLU network by hand from a specification, with no gradient descent or training data) stops working, rather than adding one more success. It builds a ladder of games that vary one difficulty axis at a time (state-space size, existence of a closed-form strategy, action-space geometry, planning horizon) and, at each rung, a structurally unrelated replicate game at matched difficulty, so that a finding can be attributed to the difficulty level rather than to one game.

## What they studied
Ten hand-built ReLU networks: Nim and Wythoff's game; tic-tac-toe (pre-existing, reused) and 2x2 Dots and Boxes; reduced Connect Four (4x5, connect-3) and 4x4 Othello; standard Connect Four and 8x8 Othello; King+Rook vs King and King+Queen vs King. Parameter counts span about 3.8 thousand to about 38.9 million. Constructor: Claude Sonnet 5 with full agentic tool access over a multi-hour session ("Track A"). Replications: two other providers' coding agents (reported as "6 Luna High"/Codex and Grok 4.7 High, including a higher-effort rebuild) and three Claude tiers (Opus 5, a fresh Sonnet 5, Haiku 4.5). Unit: whole network as a compiled circuit.

## How they did it
Networks are built from four gate primitives: AND by sum-and-threshold, a two-stage clip that implements OR, an exact-match detector against a stored binary state, and a tiered score with weights separated by orders of magnitude to enforce a lexicographic priority over candidate moves; plus a new exact XOR identity on binary ReLU outputs for Nim. Where single-pass heuristics are insufficient, exact-match "override" neurons encode answers precomputed offline by exhaustive search (allowed by their Definition 1 as long as the search result is baked into weights). Verification: exhaustive traversal of the reachable game graph against an independently written oracle where enumerable; for chess endgames, an exhaustive per-position check of legality, mate-in-one and distance-to-mate progress against a from-scratch retrograde oracle (cross-checked against published position counts and maximum distance-to-mate), plus 3000 simulated games against a worst-case adversary; for full-size boards, at least 10 seeds with Wilson CIs against random and against shallow alpha-beta search. Replications received a hint-stripped brief and worked in isolated directories; the author re-ran their tests and checked for code reuse.

## What counts as an explanation here
Not interpretability of a trained net; the network is the explanation, a hand-compiled circuit whose every unit has a stated purpose. Correctness proofs against an oracle play the role of a faithfulness check.

## How they judged success
Exact match to game-theoretic value over all reachable states (exhaustive); legality, mate-in-one and per-move distance-to-mate progress rates over all chess positions; full-game mate rate against a worst-case adversary; win rate with Wilson 95% CIs against random and depth-limited search; a "rigor bar" classifying each attempt per task as meeting it, built but short, or not attempted.

## What they found
- Six of ten networks were proved exactly correct over their full reachable state spaces (up to 104,399 non-terminal states for reduced Connect Four and 53,651 for 4x4 Othello).
- Closed forms differ in compile cost: Nim's XOR rule is a fixed-size circuit; Wythoff's irrational (golden-ratio) rule has no finite exact ReLU circuit and needed a full lookup table.
- Chess endgames: legality exact in all positions; KRK took available mates 84.1% of the time but made strict distance-to-mate progress in only 6.99% of positions and mated in 0.57% of games against a worst-case adversary; KQK with an exact mobility circuit took 100% of available mates, made progress in 39.06% of positions, and mated in 9.13% of games.
- Full-size Connect Four and Othello heuristics beat random opponents (99.5 to 99.8% and 86.3 to 87.5%) but lost all 800 games to depth-4 and depth-3 search respectively; the author reads this as an architectural ceiling (no search in a fixed-depth forward pass).
- Replications reproduced the qualitative pattern. One independent Grok build drew 50% against depth-2 Othello search, but a higher-effort rebuild lost all 40 games. Opus 5 built a tablebase-readout variant that forces mate from every legal KRK and KQK position at the theoretical optimum, showing the ceiling is on compact hand-derived circuits, not on what the architecture can represent. Haiku 4.5 built only Nim and Wythoff and declined the rest on feasibility estimates that were wrong (e.g., reduced Connect Four state space estimated near 1e8 vs the true 104,399). A fresh Sonnet 5 found a rook-capture rule bug shared by its network and its own oracle that one-ply exhaustive checks could not catch.

## Limits and open problems they name
Track A used full tools and unlimited iteration, so it does not measure cold, single-shot ability; Track B (one cold, tool-free prompt per game, tic-tac-toe as the only worked example) is released but not run. Opponent strength differs across attempts, making cross-attempt mate rates hard to compare. Statistical rungs have no exact guarantee. Some replication labels (model identities) were not verified by the author. Some own-construction choices (Wythoff pile bound 0 to 7) deviated from the written specification.

## What we take from it
- **A methodology for writing claims:** independent oracles sharing no code, exhaustive verification where possible, and a matched replicate at each difficulty level to separate level from instance. Directly reusable if we test writing or patching weights.
- **A framing:** what compiles into weights is local, one-step-scoreable logic; what does not is composition into a multi-step plan. This parallels reading results where single-unit flaws are easy and distributed ones are not.
- **A warning:** one-ply exhaustive checks can miss bugs shared by the network and the oracle; full rollouts caught one.
- **Limited K1 value:** no network is read by an LLM here.

## K1 detail (reading setup)
- **Reader model(s), and the score for each:** not applicable; no reading of trained weights was tested. Constructors (writing, not reading): Claude Sonnet 5 (Track A, met the rigor bar on all 9 replicated tasks); Codex "6 Luna High" (short on 3 of 9); Grok 4.7 High (all 9, at two effort levels); Claude Opus 5 (all 9); fresh Claude Sonnet 5 (all 9); Claude Haiku 4.5 (2 of 9, declined 7).
- **Target networks:** hand-written feed-forward ReLU networks for ten games, from 3,786 to 38,898,084 parameters (Track A); none trained.
- **How the weights were presented:** not applicable (weights were written as code, e.g., PyTorch linear layers, by an agent with code execution); no weights were shown to a reader as text.
- **Prompt:** Track A: not given in the paper. Replication brief: task specification stripped of the authors' gate constructions, released as "external_replication" material (no URL found). Track B (not administered): one self-contained prompt per primary game with a plain-language method statement, the full tic-tac-toe solution as the only worked example, the game rules and exact input/output tensor shapes, withholding specific gate constructions; no tools, single attempt. No public path found.
- **Access regime:** Track A and replications: full agentic tools (code execution, file I/O, parallel subagents), unlimited iteration. Track B: no tools, one attempt (not run).
- **Controls:** independent oracles with no shared code; replicate games at matched difficulty; independent replications by other models in isolated directories, checked by grep for reuse and re-verified by the author; a higher-effort Codex run excluded because it disclosed reusing its first run's recipe and had read access to the author's source tree.
- **Failure modes observed:** (writing) inability to compose local tactics into multi-move plans; heuristic tiers that are locally attractive but globally counterproductive (taking every check lengthens games); a model declining tasks on incorrect feasibility estimates (Haiku 4.5); a constructor producing procedural Python control flow instead of a pure weight circuit (Codex chess); shared bugs between network and self-written oracle.
- **Prompt or format choices that helped or hurt:** not stated for prompts. Construction choices that helped: exact (rather than heuristic) one-ply safety circuits made full-game safety nearly perfect; moving the override tier above box-completion was necessary in Dots and Boxes; higher effort helped Grok modestly.
