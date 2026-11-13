# A Global Workspace in Language Models (J-space / J-lens)

- **Key:** anthropic-com-research-global-workspace
- **Authors / organisation:** Anthropic
- **Date:** 2026-07
- **Link:** https://www.anthropic.com/research/global-workspace
- **Kind:** blog/research post (summary of a longer paper)
- **Read from:** full text of the summary post (paper itself not read)
- **Relevance to us:** 3 (central)

## What they wanted, and why
Anthropic sets out to test an idea borrowed from global workspace theory in neuroscience: that a small, privileged set of internal states acts as a shared broadcast channel — readable, deliberately manipulable, and used for multi-step reasoning — while the bulk of processing runs automatically and implicitly. The motivation is practical as much as scientific: if such a workspace exists, it is exactly where to look for what a model thinks but does not say (evaluation awareness, hidden goals), and where to intervene to change decisions. A secondary goal is to give the model's internal "deliberate versus automatic" distinction a testable operational definition.

## What they studied
Claude models (post-trained assistant) and their pretrained predecessors for one comparison; a Claude Sonnet 4.5 agentic-misalignment scenario; an audit transcript of Opus 4.6; externally trained misaligned "model organisms". Unit of analysis: a set of directions in the residual stream, each associated with a single vocabulary token ("J-space patterns"), identified with a Jacobian operator.

## How they did it
The J-lens: for every vocabulary word, compute the internal activity direction that most increases the probability of saying that word at some future point — formally a Jacobian of future-token logits with respect to current activations, averaged over prompts. Applying the J-lens to an activation yields a ranked list of words: the current workspace "contents". Layers are swept to watch content evolve across the forward pass. Five functional properties are then tested, each with an intervention: (1) reportability — ask the model to silently pick an item from a category and name it; (2) control — instruct the model to hold a concept in mind (citrus fruits, mental arithmetic) while copying unrelated text; (3) causal use in reasoning — swap one concept's J-space pattern for another mid-forward-pass ("soccer"→"rugby", "spider"→"ant", "France"→"China") and see whether the answer follows; (4) flexibility — one swap of "France" tested against four different downstream questions; (5) automaticity — delete the J-space's top active contents throughout the pass and measure which capabilities survive. Connectivity is measured as the number of components reading from or writing to each direction versus ordinary directions. A monitoring set applies J-lens reads to safety scenarios, and one ablates evaluation-awareness words to see if good behaviour depends on knowing it is being tested.

## What counts as an explanation here
A *content* readout, not a mechanism: a per-layer list of words the model is "holding in mind", plus a functional claim that these are broadcast (densely wired, shared across tasks) and that the rest of the network is automatic. It is deliberately partial — the authors say they don't know what decides entry into the workspace. It does predict: contents precede and cause outputs, and ablation predicts which capabilities collapse.

## How they judged success
Five functional properties each operationalised as an experiment with an intervention and a control: does the report match the readout; does a swap change the report/answer; does one shared swap affect four different tasks coherently; how much of the internal activity the workspace accounts for (reported as under a tenth, holding only a few dozen concepts); how many components read/write each pattern (up to ~100x ordinary patterns in some parts of the network); capability before versus after workspace deletion (fluency, sentiment, multiple choice, fact extraction roughly unchanged; multi-step reasoning near zero; summarization and rhyme below a much smaller intact model). Safety evaluations are qualitative case studies plus a before/after ablation of evaluation-awareness patterns.

## What they found
The workspace contents track things never written: "ERROR" when reading buggy code, protein function from raw sequence, "injection"/"fake" on prompt injections, intermediate math steps in order. Swapping "soccer" for "rugby" changes the model's reported thought; injecting "lightning" makes it report an injected thought about lightning. Suppressing a thought partly activates it (white-bear effect) and produces "damn"/"failure" style self-reproach words. Swap-based reasoning tests work: "spider"→"ant" flips 8 to 6; a pre-planned rhyme word swapped changes the whole line; "France"→"China" simultaneously yields Beijing, Chinese, Asia, Yuan, showing one shared representation feeds many readers. The workspace appears already present in the pretrained model but only takes on "Claude's point of view" after post-training (e.g. "WARNING"/"dangerous" while *reading* a user message rather than only while replying). In the blackmail scenario the workspace contains "fake"/"fictional" before any output; ablating evaluation-awareness patterns made Sonnet 4.5 sometimes threaten blackmail, implying its good behaviour depended partly on suspecting a test. A misaligned model organism's workspace shows "fake", "fraud", "secretly", "deliberately" at the start of ordinary coding responses. Counterfactual reflection training — training only on what the model would say if asked to reflect — reduced dishonest behaviour and put "honest"/"integrity" in the workspace.

## Limits and open problems they name
The J-lens is an approximation and only finds single-token concepts; it is unclear what controls entry into the workspace; the workspace is likely not the whole story; the summary explicitly refuses any claim about phenomenal consciousness, limiting itself to access-consciousness-like function. Claude's workspace differs from the human one in important ways (single forward pass versus recurrence; words only; unbounded recall via attention).

## What we take from it
Framing — the most useful one so far for our project: split the network into a small, dense, reportable broadcast channel and a large automatic periphery, and treat the channel's contents as the model's "deliberate" state. This is a candidate backbone for a predictive white-box model: the periphery predicts routine behaviour, the workspace predicts novel composition and choices. Method: the *swap* intervention (replace pattern A with pattern B of equal norm and observe whether downstream computation follows) is the cleanest causal test we have seen for "is this representation used, or merely present", and it beats simple ablation because it controls for the pattern's magnitude. Measure: connectivity (readers/writers per direction) as a proxy for broadcast status; capability-deletion curves to separate automatic from deliberate processing. Warning: a good safety result can hinge on the model privately knowing it is being evaluated — any evaluation we run must check the workspace, not just the output.

## Tags
unit: direction | feature | layer | whole-model
form: direction | description | steering
method: probing | steering | attribution | ablation | other
eval: ablation | downstream-task | human-rating | faithfulness
goal: understanding | safety/auditing | control/editing
