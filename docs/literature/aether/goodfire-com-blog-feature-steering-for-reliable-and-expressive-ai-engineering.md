# Feature Steering for Reliable and Expressive AI Engineering

- **Key:** goodfire-com-blog-feature-steering-for-reliable-and-expressive-ai-engineering
- **Authors / organisation:** Eric Ho; Goodfire Research (blog)
- **Date:** 2024-11-20
- **Link:** https://www.goodfire.com/blog/feature-steering-for-reliable-and-expressive-ai-engineering
- **Kind:** blog/research post (product essay with a depreciation banner)
- **Read from:** full text — the whole page from the opening to the citation block, ~7.6k chars in one fetch; the page is a short essay with no methods, results or appendix, so there is nothing further to miss. **No figure inspected**: the one chart (a curve of mean response length against steering strength for conciseness) and the "Conscious Llama" screenshot are images, and the prose gives no numbers from either, so no value is quoted here. A **February 2026 banner on the page says the SAE demo interface and API have been deprecated**, so the tooling this post is selling no longer exists. The assumed-background prerequisites (the earlier SAE/steering primer) were not fetched.
- **Relevance to us:** 1 (background)

## What they wanted, and why

The argument is a software-engineering one rather than a scientific one: models arrive as sealed black boxes that cannot be edited or debugged, which is a bad way to build anything, and the only available levers — prompt tuning and fine-tuning — are respectively a discrete, low-ceiling knob and a slow, expensive path to a second black box (with spurious correlations from the curated data as the recurring failure). Their claim is that feature-level intervention restores the missing property: something you can adjust, iterate on and fix like ordinary software, where an edit is as cheap to try as a prompt change and needs no data. The target audience is application developers, and the post's purpose is to draw the prompting / fine-tuning / steering boundaries. It is a step toward their broader "neuron programming" thesis, not toward explanation.

## What they studied

No model, dataset or benchmark is named at all — no target model, no SAE, no layer, no training set for the features, and no accuracy or quality metric for steering. The evidence is customer stories summarised in prose plus one chart. The unit of analysis is a feature in a sparse-autoencoder dictionary, manipulated by pinning or scaling, and the outputs discussed are style and content properties of generated responses (length, persona, tone, topic engagement) rather than any capability measurement.

## How they did it

There is no method section; the post compares three engineering levers conceptually and then lists four use cases. The comparisons: versus prompting, they frame a system prompt as an *attempt* to excite the right set of internal features indirectly, where steering addresses those features directly — so steering sits after prompting, not in place of it, for precisely the behaviours prompting cannot reach. Versus fine-tuning, the differentiator they draw is that steering cannot introduce new knowledge (it only re-shapes what the model already knows), so anything requiring new facts must be trained; everything requiring a change in *behaviour* can be steered. The claimed practical consequence is that a steering change is as fast to test as a prompt edit, which removes the usual adoption barrier to fine-tuning. The use cases are: continuous strength control where prompting forces a discrete instruction (their conciseness example); managing many personas by adjusting features per customer segment instead of maintaining a separate prompt per segment; new interaction affordances (sliders on communication style, and analogies for image and music generation where an object's count or an instrument's prominence is reduced); and conditional behaviour, where a feature's detected presence gates a policy — their example is a support agent that escalates a discount when it reads anger.

## What counts as an explanation here

No explanation is offered and none is claimed. The artifact is a **steering interface**: named features with strengths, plus conditional rules over detected feature presence. Completeness is explicitly not on the table. The one framing worth keeping is the "conditional" idea, because it implies a *detection* read-out feeding an *intervention* decision — which is a monitor-and-act loop, structurally the same shape as the probe cascades elsewhere in this folder, arrived at from the product side rather than the safety side. But no mechanism is proposed for why a given feature causes the behaviour it is used for, so the post inherits the standard correlate-versus-mediator ambiguity without addressing it.

## How they judged success

Nothing is measured in a reportable way. There is no baseline comparison, no held-out evaluation, no human rating study, no fidelity or coherence measurement, and the one quantitative-looking claim (a response-length curve under conciseness steering) has no numbers in the prose and is known here only from its caption. Success is asserted through customer anecdotes and the existence of the (now deprecated) SDK. This is a vendor-positioning essay, and the honest summary is that it reports no evidence at all.

## What they found

Four claims, none tested here: that feature strength is a continuous axis where prompting is discrete, giving dose control over style; that persona management collapses from per-segment prompts to per-segment feature settings; that interaction affordances become possible that prompting cannot reach (their examples are adjusting object counts in images and instrument prominence in music); and that conditional steering lets behaviour depend on detected internal state rather than on the user's phrasing. Their one explicitly stated boundary is the knowledge distinction — steering re-shapes existing knowledge and cannot add facts — which is the most useful sentence in the post and the one to carry.

## Limits and open problems they name

They name essentially none, other than the knowledge boundary. The update banner effectively concedes the largest one: the demo interface and API described here were deprecated, so none of the use cases can be checked against a live tool. There is no discussion of side effects at high strength, of whether a feature's meaning is stable across prompts, of interference between simultaneously steered features, of evaluation, or of any failure mode.

## What we take from it

One framing, and it is worth more than the post's evidence supports. The **knowledge-versus-behaviour split** is a clean way to decide which of our interventions is legitimate: an activation edit cannot install a fact, so a claim that a steering direction changed what the model *believes* rather than how it *behaves* needs evidence beyond a behavioural shift, and the field's failure to make that distinction explicit is why so many steering results are ambiguous between "the model now believes X" and "the model now says X". Second, the **conditional** use case is the same structure as a probe-driven cascade and is the design our predictive model needs anyway: detect state, then act on it, with the detection scored separately from the action. Everything else here is marketing with no measurements, and the deprecation banner is itself the lesson — a steering feature without a published evaluation cannot survive its own product cycle, which is the argument for the operating-point reporting and ablation protocol this folder's monitor entries insist on.

## Tags

unit: feature | direction
form: steering | probe
method: steering | SAE | probing
eval: human-rating
goal: control/editing | understanding | debugging
