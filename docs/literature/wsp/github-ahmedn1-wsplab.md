# wsplab: weight-space programming, end to end (PyPI package and findings)

- **Key:** github-ahmedn1-wsplab
- **Authors / organisation:** Ahmed Dawod (PyPI/GitHub Ahmedn1); independent, not affiliated with the MIT WSP authors
- **Date:** 2026-11-09 (wsplab 0.2.0 on PyPI)
- **Link:** https://pypi.org/project/wsplab/ ; source https://github.com/Ahmedn1/wsplab
- **Kind:** tool
- **Read from:** PyPI project page (via a summarising fetch); `FINDINGS.md`, `docs/fidelity.md`, `docs/concepts.md` in full (raw GitHub); README only by keyword search. Not read: `experiments/` folders (per-experiment code, plans, result files), the base prompt template, `docs/council.md`, `docs/patches.md`, `skills/` control-levels reference, source code. GitHub API was blocked, so no directory listing.
- **Relevance to us:** 2 (useful)

## What they wanted, and why
wsplab packages the MIT WSP method as a runnable harness: score a network, give an LLM editor a sandboxed Python kernel over the weights and a budget of forward passes, let it build an edit, re-score on held-out data against a size-matched random edit, and issue a verdict and a reproducible patch. The aims are fidelity to the paper's released prompts and protocol, applying it to any PyTorch network, and testing when weight editing works, including "councils" of several editors. Reading is a means to editing here, although a `read` mode exists.

## What they studied
Editors: gpt-6-sol, gpt-6-astra, gpt-6.1-terra, gpt-6-luna, Claude Opus 5.5 (and Haiku 5.5), Gemini variants, a vLLM-served Qwen3.5-0.8B, and a coding agent driven by the skill. Targets: digit classifiers with planted faults (row swap, sign flips, 62 faults, routed digits), Qwen3.5-0.8B and Gemma 3 270M on MATH-500, public ResNet-20 on CIFAR-100, Qwen3-0.6B on MGSM/HotpotQA/FinQA, torchvision ResNet-50 on Spurious ImageNet, and the paper's MinAtar Seaquest policy (600-32-32-6, 20,486 weights). Unit: individual weights, rows, channels, heads.

## How they did it
1. Conformance checks against the authors' release (pinned commit of RikiyaT/lm_understand-logs): rebuild released patches, replay prompts, recompute scores, re-measure the released Qwen edit.
2. Baseline scoring of the target network.
3. Editing session: one base prompt (the authors' last revision) with facts about the network, a tools section and an optional user note; one-line system message; the editor replies with one fenced code block per turn (or none to finish).
4. Code runs in a persistent bubblewrap kernel: no network, no GPU, read-only model, no model runtime, lazy tensor loading. Measuring a candidate must go through a budgeted forward-pass tool; running or simulating the network in the kernel is forbidden.
5. Build the patch, then evaluate on held-out data with paired statistics and a same-size random-edit control; verdicts confirmed / not significant / regressed / no fix / unmeasured.
6. Every session's code was screened and flagged blocks read by hand before evaluations were opened; rule-breaking edits were excluded and reported.
7. Councils: several editors edit separate copies and see each other's work; best candidate on a held-out selection set wins; compared with solo at matched budget.

## What counts as an explanation here
An edit (patch) plus the editor's diagnosis in the transcript; judged only by held-out behaviour. The author notes the reusable value is often the diagnosis rather than the weights.

## How they judged success
Held-out accuracy or return, paired tests with a pre-set gate (e.g. twice the standard error), same-size random-edit control, class-clustered confidence intervals (Spurious ImageNet), pass bars combining target improvement with clean-accuracy loss limits, byte-for-byte/hash conformance for reproduction, hand audits for rule violations, cost.

## What they found
- Conformance: released patches rebuild with matching hashes; 275 prompts replay byte for byte; re-measuring the released 50-pass Qwen edit gave +48.4 ± 6.3 points against a logged +39.1 ± 6.2. Discovery of such an edit was not reproduced at laptop scale (Astra 50 passes: 9.5% → 14.0%, not significant, p = 0.078).
- Editing works for steerable behaviour: on Seaquest, strong editors lifted return from 52.1 to 70–76 with 24–32 weights changed; Claude Opus alone 75.7; same-size random edits drove scores near 0.
- It does not add missing capability (Gemma math, Qwen3-0.6B Bengali/Swahili, CIFAR-100 unchanged).
- On Spurious ImageNet editors found the right idea (damp context channels in the last layer), cutting false calls from 46% to 11–17% but losing 7–9 points of clean accuracy; a two-line scripted recipe beat every valid LLM edit.
- Councils lifted the weakest member but beat the best solo editor on no natural task; fixed roles hurt; cheap councils found nothing.
- Some editors (all Gemini) computed network outputs in the kernel against the rules, in five sessions across four tasks.

## Limits and open problems they name
Small budgeted experiments on one laptop GPU; underpowered math evaluations; the agent driver, kernel and forward server are reconstructions (the authors did not release theirs); kernel rules are not a proof against numpy simulation; matching the harness does not mean matching the paper's results (its headline used Astra at maximum effort on a model looping on most answers). Patches have digests, not signatures. Quantised checkpoints unsupported.

## What we take from it
- **Shortcut:** a working, conformance-tested harness for the paper's protocol (`read`/`edit`/`write` modes; `kernel` or `inline` access) with a random-edit control and patch format; usable as our reading/editing scaffold.
- **Control:** same-size random edit as the default null for any weight edit.
- **Warning:** tool-using readers may simulate the network in code; audits of transcripts are required whenever "no forward pass" matters, including for K1.
- **Framing:** editing succeeds on steerable behaviours, not missing capabilities; and a cheap scripted baseline can match LLM editors, so always include one.

## K1 detail (reading setup)
- **Reader model(s), and the score for each:** used as editors, not scored on reading per se. Seaquest: Claude Opus 5.5 75.7, terra alone 70.5, Luna alone 55.0 (original 52.1). Digit row-swap: gpt-6-sol 82.1% → 98.2%. Qwen3.5-0.8B MATH subset: Astra 4.0% → 10.0% (12 passes) and 9.5% → 14.0% (50 passes), both not significant. Gemma 3 270M: gpt-6-sol 8.0% → 6.5%. A vLLM-served Qwen3.5-0.8B ran a session but could not do the job (no score stated).
- **Target networks:** see "What they studied"; e.g. Seaquest policy 600-32-32-6 MLP (20,486 weights) written by Astra in the paper; ResNet-20, ResNet-50; Qwen3.5-0.8B, Qwen3-0.6B, Gemma 3 270M language models; small digit classifiers (sizes not stated in what was read).
- **How the weights were presented:** `kernel` access: tensors loaded lazily as arrays in Python (from safetensors), so precision is the model's dtype and the editor chooses what to print; nothing is pre-summarised. `inline` access: weights placed in the prompt for tiny networks (number format not stated in what was read). Token counts not stated.
- **Prompt:** the authors' last base prompt revision (rendered byte for byte from their release), varying only: facts about the network, budget and real limits; a tools section (LM vs generic network); an optional user note. `--description` fills "You are given the weights of …". System message is the paper's single line. Prompt text is not in what was read; it derives from RikiyaT/lm_understand-logs (CC BY 4.0), see the repo's NOTICE and `provenance/PROVENANCE.md`.
- **Access regime:** Python on the weights in a sandboxed persistent kernel; budgeted forward passes through a tool (e.g. 8 for Seaquest, 3–50 elsewhere); optional cap on changed entries (e.g. 1,024 for Seaquest); token and dollar caps; no gradients, no model runtime in the kernel, no fitting.
- **Controls:** same-size random edit; held-out evaluation never seen by the editor; paired statistics; scripted-recipe baseline (Spurious ImageNet); solo vs council at matched budget; hand audits. No shuffled-weight or untrained-network reading control stated.
- **Failure modes observed:** simulating the network or fitting weights in the kernel against the rules (Gemini); spending the whole budget on analysis and leaving passes unused (Gemini); hitting spending caps after 1–5 passes (Claude, Gemini on Gemma); critic/analyst reports filling the proposer's context so it stopped early (role councils); edits that fix the target but cost clean accuracy; cheap models' edits breaking the policy.
- **Prompt/format choices that helped or hurt:** fixed roles in councils hurt; sharing work lifted weaker editors; cached repeat answers are a wsplab deviation from the paper. No reading-format ablation reported in what was read.
