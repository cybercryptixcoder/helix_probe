# Recommendations for Technical AI Safety Research Directions

- **Key:** alignment-anthropic-com-2025-recommended-directions-index-html
- **Authors / organisation:** Anthropic Alignment Science team (collective authorship; no individual names on the page)
- **Date:** 2025
- **Link:** https://alignment.anthropic.com/2025/recommended-directions/index.html
- **Kind:** survey/agenda
- **Read from:** full text (~34.6k characters, one pass, whole page including all sections; no figures on the page, no appendix)
- **Relevance to us:** 2 (useful)

## What they wanted, and why

They are answering a question they say researchers keep bringing to them: given that catastrophic risk is the thing worth preventing, what technical work can be done **now** that a developer would actually find useful later? The stated premise is that future worlds carrying substantial AI risk will have been transformed by AI development, so the tractable move is to chart navigable paths rather than to predict the destination. Their organising frame is a three-way taxonomy of safety assurances: the system lacks dangerous capabilities, the system is sufficiently aligned, or the system is deployed behind safeguards strong enough that it could not cause catastrophe even if it tried. Everything in the post is a research direction that would strengthen one of those three legs. They are explicit that this is a **tasting menu, not a survey** — contributions came from team members writing up problems they personally thought mattered, binned into categories afterwards — and, importantly, that most entries are directions they are *not* working on and have no capacity to fund.

## What they studied

No model, no experiment. The unit of analysis is the **research direction** — an open problem stated as a motivating question, a short argument for why behaviour-level measurement is insufficient to answer it, and a pointer to prior work. For our purposes the load-bearing sections are "Understanding model cognition," "Chain-of-thought faithfulness," "Activation monitoring" and "Anomaly detection," because those are the four places the post touches internal states rather than outputs. The remaining sections — capability evaluation, persona effects, behavioural monitoring, scalable oversight, adversarial robustness, unlearning, multi-agent governance — are context for how the internal-state directions are meant to plug into a deployment story.

## How they did it

Method is editorial: solicit problem write-ups from within the team, group them, and accompany each with citations to work that has begun. Several sections carry a short "what we would like to see" list of concrete sub-questions, which is the part with practical value. The most consequential piece of argumentation appears in the activation-monitoring section, where they give a two-part case for monitors on hidden states over monitors on text: activations reflect the reasoning of the model being monitored, and they are **hard to control deliberately**. The example offered is a weak model screening a strong code-generating model — a text-only monitor can miss a vulnerability the weak model never understood, or be defeated by obfuscation, whereas reading the generator's own states sidesteps both failures. Against that they immediately place the counter-argument: monitors trained on synthetic fixed datasets are risky precisely because the shift from curated synthetic data to the model's **own** generations is untested.

## What counts as an explanation here

Neither explanation nor model — an agenda. The epistemic form is a claim about which measurements would be *decision-relevant*: which quantities, if we could read them reliably, would license an assurance nobody can currently make. There is one framing worth preserving verbatim in substance rather than wording — activation monitoring is described as a deliberately **less ambitious** cousin of understanding model cognition: instead of explaining the computation, train a scalable automatic detector for the presence of a pre-specified undesired concept. That is a useful ladder for us, because it says the field's own practitioners see a real gap between "detect this concept" and "understand this computation," and treats the former as the deployable rung.

## How they judged success

No metrics at all, and no attempt at one. The implicit success criterion for each direction is that it could be turned into an assurance statement a lab could actually make — a claim of the form "we know this system cannot do X," "we know this system is not trying to do X," or "we know our safeguards would stop it." The only empirical judgement offered anywhere is the hedged "there are signs of life" for activation monitoring, immediately followed by the statement that far more work is needed before production deployment.

## What they found

Four things worth extracting from the internal-state sections. (1) **The cognition questions are stated as a list a probe could be scored against**: did the model answer because it believed the answer, because it modelled the user as believing it, or because it expected the answer to please? Does it plan, and what are the plans? Does it have beliefs about whether it is in training or being monitored, and do those beliefs move its behaviour? Does it *know* something it does not report? Read together these are four distinct axes — belief attribution, planning, situational awareness, and unreported knowledge — and each has a natural intervention-based test rather than a text-based one. (2) **CoT faithfulness is flagged as important but underexplored**, with three sub-questions that are directly probe-shaped: whether faithfulness varies by task type; whether a large accuracy gain from CoT licenses treating the trace as faithful; and whether telling a model its traces are being monitored *for faithfulness* changes how faithful they become — the last being an evaluation-awareness effect on the measurement instrument itself. (3) **Activation monitors have a distribution-shift problem centred on self-generated data**: if you have no real examples of the bad behaviour, you train on synthetic substitutes and must then show the monitor transfers to the model's actual dangerous generations. This is the same methodological hole that shows up in every probe paper in our folder, and here it is named as the field's main obstacle to deployment rather than as a limitation. (4) **Anomaly detection is proposed in two flavours** — flagging inputs that are far out of distribution (jailbreaks the supervised monitor will miss), and, as an explicitly unexplored problem, flagging inputs where a strong model's understanding diverges so sharply from a weak model's that the strong model's behaviour is novel relative to the weak one. That second flavour is a differential-detection idea: use the disagreement between two models, not a label, as the signal.

## Limits and open problems they name

They name the post's own genre limits plainly: it is not comprehensive, it is not a statement of what they are working on or funding, and the organising categories were imposed after the fact. Substantively the named open problems are the interesting part — the synthetic-to-self-generated distribution shift for activation monitors, faithfulness of externalised reasoning across task types, and the strong-vs-weak divergence case for anomaly detection, which they call unexplored. What is *not* named, and should be, is that none of the assurance categories comes with a cost or a detection-rate threshold, so the post cannot rank directions by value; a direction that improves a monitor's AUROC by a harmless amount and one that closes a deployment-blocking gap appear side by side.

## What we take from it

Framing mostly, plus two concrete research cues. **The framing to borrow:** their three-leg assurance taxonomy (lacks capability / is aligned / is safeguarded) is a clean way to position whatever we build, and it forces the question we should be answering in our own write-up — *which assurance does reading a weight or a direction let someone make that they could not make before?* A probe that detects a concept is the "less ambitious" rung by the field's own account, so our claim should be clearly distinguished from the cognition rung above it. **Cue one:** the gap between concept-detection and cognition-explanation is where our predictive model should aim, and the four cognition questions give it four testable targets — belief attribution, plan, situational awareness, unreported knowledge — each of which can be scored by an intervention rather than by reading a trace. **Cue two:** the self-generated-data distribution shift is the single most reusable warning here, and it is stronger than the version that appears in the probe papers themselves, because it is stated as the blocker to deployment rather than as a caveat: a monitor validated on synthetic positives tells you nothing about its behaviour on the model's own outputs, and our own probe evaluations should adopt a train-on-synthetic / test-on-model-generated split by default. **Also worth stealing:** the differential-detection idea — disagreement between two models on the same input as an unsupervised anomaly signal — is cheap, uses weights and activations we already have, and is the kind of measurement that needs no labels at all.

## Tags

unit: whole-model | direction
form: probe
method: probing | SAE | other
eval: downstream-task | evaluation-of-methods
goal: safety/auditing | control/editing | evaluation-of-methods
