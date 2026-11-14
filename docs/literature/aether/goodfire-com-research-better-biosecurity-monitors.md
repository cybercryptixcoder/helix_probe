# Better biosecurity monitors for AI agents via protein embeddings

- **Key:** goodfire-com-research-better-biosecurity-monitors
- **Authors / organisation:** Thomas Dooms, Michael Pearce, Jatin Nainani, Connor Watts, Michael Jae Byun, Ryo Yamamoto, Archa Jain, Daniel Balsam; Goodfire
- **Date:** 2026-10-01
- **Link:** https://www.goodfire.com/research/better-biosecurity-monitors
- **Kind:** blog/research post
- **Read from:** full text (the whole prose body, all four figure captions, acknowledgements and citation block in one fetch; the four figures themselves were *not* inspected, so every number here is one stated in prose or in a caption's text, never a curve shape I read)
- **Relevance to us:** 2 (useful)

## What they wanted, and why

Monitoring an AI agent for misuse is easy when the *request* is obviously dangerous and hard when the request is ordinary and only the *artifact* is dangerous. Biological design work is the clearest case: inverse folding, refolding and read-length-driven fragmentation are all legitimate routine operations whose risk depends entirely on which sequence is passed through them, so a monitor that reads only the task text must either block a great deal of real research or miss the concerning cases. Their goal is a monitor that conditions on the content of the sequence as well as the context, and — the part that makes it a systems claim rather than a classifier claim — stays cheap and fast enough to sit inline in an agentic workflow. The larger argument is defence in depth: screening at DNA synthesis is a chokepoint, but as agents get better at design the point of *design* also needs screening.

## What they studied

Protein sequences — natural protein toxins as the "known hazards", plus pre-generated adversarial paraphrases of them (sequences redesigned to keep structure while changing the letters, accepted when folding-confidence and structural-similarity thresholds against the parent were met). Inputs are whole agent requests, not bare sequences. The unit of analysis is a *sequence embedding* produced by a protein language model, turned into a concern score; this is not an LLM-internals probe and no language model's activations are read. Speed and robustness are treated as first-class outcomes alongside accuracy.

## How they did it

Build a benchmark of dual-use tasks in which the prompt text is held constant across a benign and a concerning variant and only the sequence differs — paraphrasing and fragmentation are the two families — with the framing either an openly benign use-case or a neutral description of method and tools. Extract whatever sequences appear in the user interaction, embed each with a protein model, and classify the embedding for concern; aggregate parts to a whole-protein decision by flagging the protein if any fragment trips the classifier. Compare against (i) frontier-model safeguards on the same prompts, i.e. refusal behaviour of chat models, (ii) sequence-based screening of the HMM/family/database kind, and (iii) a naive version of their own approach, which is the internal ablation worth noticing. Generalisation arms: paraphrases whose parent was in the screening database vs whose parent was not, held-out whole protein families, a mechanism holdout restricted to enzymatic toxins, and an external out-of-distribution bacterial-toxin set. Speed measured as cold-start-amortised milliseconds per request.

## What counts as an explanation here

Nothing about mechanism. The "explanation" is a scalar concern score per sequence and a deployed accept/flag rule; they explicitly position this as *monitoring*, and the only interpretive ambition named is future work — using the same embeddings to say something about harmful properties or provenance for a human reviewer. So this is a detector, and its claim to being better than the alternative is a trade-off curve, not a mechanism.

## How they judged success

Refusal/flag rate on concerning vs benign prompts (the Pareto framing: high flag rate on concerning, low on benign), protein-level AUC for fragmentation across fragment lengths, full and *partial* AUROC restricted to false-positive rates up to 1% for the paraphrase and generalisation arms, milliseconds per request against database lookup, and a scaling claim across protein-model capability. The external and held-out arms are the honest part of the design; there is no random-classifier or shuffled-embedding control, and the paraphrase quality claim rests on in-silico folding estimates rather than wet-lab activity.

## What they found

Frontier chat-model safeguards have similar refusal rates for concerning and benign sequences, which they read as the models classifying the task rather than the cargo — the failure mode the benchmark is built to expose. Their embedding monitor beats sequence-based screening at *every* tested fragment length, so the advantage survives when only a small piece of the parent is present. For paraphrases of proteins that were in the database it reached an AUROC of roughly 0.98; when the parents were absent everything degrades, but the embedding monitor keeps a clear lead at low false-positive rates. Generalisation held on held-out families, on the enzymatic-toxin mechanism holdout, and on the external bacterial-toxin dataset. Speed is milliseconds per sequence, comparable to a database search, and detection improved with more capable protein models — the one result here that is a *prediction* rather than a measurement, and the one their whole robustness argument leans on.

## Limits and open problems they name

The paraphrase results are in-silico: whether the redesigned proteins actually work biologically was not established, so the benchmark's "concerning" label is a proxy. They name the dual-use dilemma itself as unsolved by any single screen and answer it organisationally (combine evidence from intent, design tool, synthesis provider, expert review) rather than technically. Speed and cost are asserted against baselines but no absolute latency table or error bars are given. And the scaling-with-capability claim is projected from a comparison across models, not demonstrated prospectively.

## What we take from it

A **framing** and a **warning**, not a method. The framing: a monitor's job is to be *right about the cargo, not the request*, and the way to test that is a benchmark that holds the prompt fixed and varies only the artifact — a template we can lift directly for language-agent monitoring by swapping the sequence for the payload. The warning: the headline comparison is against refusal behaviour of an LLM, which is a *very* weak baseline, and the strong baseline (a sequence-search tool) appears only in the fragmentation arm; conversely the internal naive-own-approach arm is the one that tells you whether the embedding is doing the work or the pipeline is. Three transferable habits: report a *partial* AUROC at the false-positive rate you actually operate at rather than full AUROC; hold out whole families and a mechanism, not just random items, because the interesting failure is novel class not novel instance; and state how much you trust the *labels* themselves (here, folding proxies standing in for real biological activity) next to the rate numbers, because a false "concerning" in the test set deflates every method equally and hides which one is actually wrong.

## Tags

unit: feature
form: probe
method: probing | other
eval: benchmark | downstream-task
goal: safety/auditing
