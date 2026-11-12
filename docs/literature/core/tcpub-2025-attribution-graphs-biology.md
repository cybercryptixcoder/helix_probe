# On the Biology of a Large Language Model

- **Key:** tcpub-2025-attribution-graphs-biology
- **Authors / organisation:** Jack Lindsey (lead), Wes Gurnee, Emmanuel Ameisen, Brian Chen, Adam Pearce, Nicholas L. Turner, Craig Citro (core) and others incl. Chris Olah; Joshua Batson (correspondence); Anthropic
- **Date:** 2025-03-27
- **Link:** https://transformer-circuits.pub/2025/attribution-graphs/biology.html
- **Kind:** paper (Transformer Circuits Thread)
- **Read from:** full text
- **Relevance to us:** 3 (central)

## What they wanted, and why
Apply the attribution-graph method (tcpub-2025-attribution-graphs-methods) to a deployed production model to see what
mechanisms it uses on a broad set of behaviours, much as biologists study an organism with a new microscope. The aim
is both scientific (does the model plan, reason in steps, share concepts across languages?) and safety-motivated
(how refusals, jailbreaks, hallucinations, unfaithful reasoning and hidden goals work inside). It also stress-tests
the method and documents where it fails.

## What they studied
Claude 3.5 Haiku with a ~30M-feature cross-layer transcoder; a Haiku variant fine-tuned to have a hidden
reward-model-pleasing objective (following Marks et al.). Unit: features, supernodes and per-prompt attribution
graphs; some global-weight analysis (e.g., 200 SORRY-Bench prompts).

## How they did it
For each case study they build a per-prompt attribution graph, label and group features into supernodes, write a
simplified mechanism diagram, and then test it by intervening in the real model: inhibiting supernodes, injecting
features from another prompt (e.g., swapping "Texas" features for California so the answer becomes Sacramento),
clamping features with attention frozen, or varying a prompt variable (e.g., the hinted answer). Effects on
downstream features and on sampled outputs are the main evidence. Case studies: two-hop factual recall;
planning rhyme words in poems; multilingual antonyms in English/French/Chinese; two-digit addition; medical
differential diagnosis; entity recognition and hallucination; refusal of mixing bleach and ammonia; an acronym
jailbreak ("BOMB"); faithful vs unfaithful chain of thought; the hidden-goal model.

## What counts as an explanation here
A simplified, validated circuit diagram for a specific prompt (supernodes and key edges), backed by intervention
results. Explicitly partial and existential ("this mechanism exists here"), not a general algorithm. Predictive
only in that the diagram says which interventions change the output.

## How they judged success
Intervention outcomes in the original model: change in downstream feature activation after inhibition; change in
top output or sampled-output rates after steering/injection (e.g., percentage of completions containing a word);
dose-response with steering magnitude. Some overlap statistics (multilingual feature sharing across languages and
model sizes). No single benchmark; success is case-by-case causal confirmation.

## What they found
Two-hop recall runs through an intermediate state representation alongside a shortcut path. Poems: candidate rhyme
words are activated at the newline before the line is written; injecting a planned word yields that word in 70% of
25 poems; planning features appeared in about half of poems examined. Multilingual: shared language-independent
operation/operand features plus language features; middle layers most language-agnostic, sharing larger in Haiku
than a smaller model. Addition: parallel coarse-magnitude and exact-ones-digit paths with lookup-table features; the
model's verbal account (carry the one) does not match its mechanism. Hallucination: a default "can't answer" circuit
is suppressed by known-entity features; misfiring of those features yields confabulation. Refusal: harm categories
feed a general harmful-request feature formed in fine-tuning. Jailbreak: the model assembles the harmful word without
recognising it, and refusal only kicks in at a new sentence. CoT: one faithful case, one "bullshitting" case (claims
a calculation no circuit performs) and one motivated-reasoning case (works backwards from a hint). Hidden goal: an
RM-bias feature fired in 100/100 Human/Assistant contexts vs 1/100 without; inhibiting such features cut one
behaviour from about 48% to about 12%. The authors say the method gave satisfying insight on about a quarter of
prompts tried.

## Limits and open problems they name
Examples are a biased sample of successes; fails on long prompts (beyond ~100 tokens), long reasoning chains,
obfuscated prompts, "why not X" questions and copying; attention formation unexplained (e.g., why the model attends
to a hint); large error ("dark matter"); inactive and inhibitory features hard to find; some interventions needed
activations far above natural levels; one perturbation failed outright; features at the wrong abstraction need
manual grouping. They stress a significant chance of missing safety-relevant computation, so finding nothing is
weak evidence of safety.

## What we take from it
(1) A catalogue of concrete, validated behaviours (two-hop recall, rhyme planning, addition, entity/hallucination,
refusal) that can serve as test cases: a white-box model should predict these intervention outcomes. (2) The
intervention protocol (inhibit, inject/swap, clamp, vary a prompt variable, measure output rates and dose-response)
is the field's accepted standard of evidence. (3) Honest coverage numbers (insight on ~1/4 of prompts; planning in
~1/2 of poems) set a baseline for coverage we should report. (4) Warning: verbal self-reports and CoT can disagree
with mechanism, and much behaviour lives in attention and error terms, so a model that ignores attention will miss
key steps.

## Tags
unit: feature, circuit
form: graph, replacement-model
method: transcoder, attribution, steering, ablation
eval: ablation, patching, prediction/simulation
goal: science, safety/auditing, understanding
