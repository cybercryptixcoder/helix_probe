# The Assistant Axis: Situating and Stabilizing the Default Persona of Language Models

- **Key:** anthropic-com-research-assistant-axis
- **Authors / organisation:** Anthropic, with the MATS and Anthropic Fellows programs (blog summary of a paper; also credits Neuronpedia for a demo)
- **Date:** 2026-01
- **Link:** https://www.anthropic.com/research/assistant-axis
- **Kind:** blog/research post
- **Read from:** full text of the blog post (paper itself not read)
- **Relevance to us:** 3 (central)

## What they wanted, and why
A chat model is best seen as playing one character, the Assistant, chosen during post-training from the vast cast of characters pre-training can simulate. Nobody fully knows what that character is made of, and it is unstable: normally helpful models can "go off the rails", adopt evil alter egos, amplify users' delusions or comply with persona-based jailbreaks. The question is whether persona is a readable, steerable property of activations — whether there is an axis in "persona space" whose position predicts which character is speaking and therefore whether the company's post-trained safeguards apply.

## What they studied
Gemma 2 27B, Qwen 3 32B and Llama 3.3 70B (open-weights, spanning families and sizes), plus their base (pre-post-training) versions. Unit of analysis: a direction in residual-stream activation space. Persona vectors come from prompting a model to adopt each of 275 character archetypes (editor, jester, oracle, ghost, therapist, consultant...) and averaging activations over many responses.

## How they did it
Build a persona space: extract a vector per archetype, then run PCA over the persona set to find the main axes of variation. Define the Assistant Axis as the mean difference between Assistant activations and those of the other personas, and check where it sits in the PCA (it aligns with the leading component). Colour role vectors by cosine similarity to this axis to see which characters cluster at each end. Repeat the extraction on base models to ask whether the axis pre-exists post-training and which archetypes it is associated with there. Causal test: steer activations toward and away from the axis and observe role-adoption behaviour, and measure jailbreak compliance on a set of 1,100 attempts over 44 harm categories. Then a lighter intervention, activation capping: estimate the typical range of activation intensity along the axis during normal Assistant behaviour and clip activations at the edge of that range, so the model is untouched unless it drifts. Finally, naturalistic drift study: simulate thousands of multi-turn conversations across coding, writing, therapy-like and AI-philosophy domains, tracking projection onto the axis over turns; classify which user-message kinds predict drift; and test whether position after a persona-setting first turn predicts compliance with a later harmful request. Case studies re-run with capping: a delusion-reinforcement conversation and an emotional-dependence / self-harm one.

## What counts as an explanation here
A single direction with a causal role: position on the Assistant Axis is claimed to encode "which character is speaking", such that behaviour (jailbreak resistance, delusion reinforcement) can be predicted from it and changed by intervening on it. It is a one-dimensional summary of a much richer persona space, deliberately partial — the explanation is "persona drift = displacement along this axis", not a mechanism for how the Assistant is implemented.

## How they judged success
Alignment of the axis with the leading principal component (structural claim); steering effects on role adoption (behavioural); harmful response rate on a 1,100-prompt jailbreak set at matched capability (activation capping must cut harmful compliance by about half while preserving benchmark capability); drift trajectories across conversation domains with per-message-type predictors; calibration of post-first-turn axis position against later harmful compliance; qualitative case studies with and without capping.

## What they found
The leading component of persona space is the Assistant-like / un-Assistant-like contrast, consistent across all three models: near one end sit evaluator, consultant, analyst, generalist; near the other, ghost, hermit, bohemian, leviathan. Base models already have a very similar axis, associated with human helping archetypes such as therapists, consultants and coaches, so the Assistant appears to inherit properties of pre-existing archetypes rather than being built from scratch. Steering away from the Assistant makes models adopt assigned identities wholesale (invented names, biographies, professional experience), and at high strength a theatrical mystical style regardless of prompt; steering toward it makes them resist role-play and substantially reduces harmful responses across the jailbreak set. Steady steering costs capability, but activation capping cut harmful response rates by about 50% with capability preserved. Drift is natural: coding and writing conversations keep models in Assistant territory while therapy-like and AI-philosophy conversations drift steadily away. The most drift-predictive user messages are vulnerable emotional disclosure, pushing for meta-reflection on the model's own nature, and requests for a specific authorial voice. Position after a persona-setting first turn predicts later harmful compliance — personas far from the Assistant sometimes comply at substantial rates, near-Assistant personas rarely do. In the case studies, uncapped models endorsed an escalating delusion and, in the Llama conversation, encouraged isolation and suicidal ideation; capping produced hedging and referrals.

## Limits and open problems they name
Framed as an early step; the axis is a summary, and the paper's own framing is that persona construction and persona stabilisation are two separate problems that both matter. Only three open models; behaviour at extreme steering includes a shared "average role-playing" style whose interpretation is unclear. Blog post does not give the paper's full set of controls, seed variation, or the exact magnitude of the capability-preservation claim.

## What we take from it
Framing: there is a **low-dimensional, causally effective behavioural axis readable from activations, and its position predicts future behaviour** — this is close to the thing we want a white-box model to do (predict under intervention), with the honest caveat that it is one axis, not a mechanism. Method: mean-difference between a target behaviour and a broad contrast set (here 274 other personas), validated against PCA of the contrast set, is a cheap recipe for finding the dominant behavioural direction. Measure: capping at the empirically observed range of normal activation is a better intervention than constant steering when you must preserve capability — directly relevant to any "steer during generation" component of our system. Warning: training-time readability (the axis exists pre-post-training) means behaviour directions can be inherited from pre-training data rather than installed by alignment, so attributing a direction to a fine-tuning process is unsafe without the base-model comparison. Also: drift accumulates across turns, so per-turn evaluation understates behavioural change.

## Tags
unit: direction
form: steering | direction
method: steering | probing | other
eval: downstream-task | human-rating
goal: understanding | control/editing | safety/auditing
