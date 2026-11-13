# Garçon: interpretability infrastructure for running probes on any model, at any scale

- **Key:** transformer-circuits-pub-2021-garcon-index-html
- **Authors / organisation:** Nelson Elhage, Neel Nanda, Catherine Olsson, Tom Henighan, Nicholas Joseph, Ben Mann, Amanda Askell, Yuntao Bai, Anna Chen, Tom Conerly, Nova DasSarma, Dawn Drain, Deep Ganguli, Zac Hatfield-Dodds, Danny Hernandez, Andy Jones, Jackson Kernion, Liane Lovitt, Kamal Ndousse, Dario Amodei, Tom Brown, Jack Clark, Jared Kaplan, Sam McCandlish, Chris Olah (Elhage and Nanda marked core contributors); Anthropic
- **Date:** 2021-12-22
- **Link:** https://transformer-circuits.pub/2021/garcon/index.html
- **Kind:** tool
- **Read from:** full text
- **Relevance to us:** 2 (useful)

## What they wanted, and why

Their Circuits-style mechanistic work needs to look inside a model — read arbitrary activations, ablate single components, generally touch the internals rather than only inputs and outputs. The workflow that normally supports this is a notebook with PyTorch hooks on a single GPU, and that workflow simply stops existing once the model no longer fits on one node. So the concrete goal was an interface that makes the largest models they train behave, for research purposes, like a small notebook-local model. A secondary goal, stated as a value rather than an afterthought: keep performance good enough that whole classes of experiments become feasible at all.

## What they studied

Not a model or a behaviour — the tooling layer. The object of study is the *access path* to internals: named points inside a forward pass, the protocol for reading or modifying tensors at those points, and the distribution of the model across GPUs behind that protocol. Parameters get the same treatment as activations, addressed through a sibling naming scheme.

## How they did it

A server is launched with a name and a path to a model snapshot; configuration and GPU count are autodetected. Clients connect from a notebook or a script, and a notebook cell that finds a server already running reconnects rather than starting a second one; idle servers shut themselves down after an hour. The model exposes named *probe points* — points inside the architecture where a tensor can be read or replaced — and the user attaches a *probe function* to any of them, taking a save context and the tensor and returning either a replacement tensor or nothing to leave it alone. Because those functions are shipped to the server with a Python-object serializer, arbitrary user code can run beside the tensor, which is what makes server-side reduction and server-side state possible. Forward passes with attached probes return logits by default; backward passes take gradients with respect to a user-supplied loss. A simpler wrapper covers the common case of analysing a single context as it flows through. Underneath, one process per GPU runs in lockstep, a single designated rank listens on the socket and broadcasts each request, and a gather brings results back.

## What counts as an explanation here

Nothing about mechanism — this is infrastructure, not an explanatory form. What it supplies is the *operation set* that explanatory work is built from: read a tensor at a point, replace it, zero it, gradient through it, or accumulate an aggregate over many inputs without ever bringing the tensors down. The authors are explicit that the probe interface is an assembly language and that higher-level abstractions are expected to sit on top of it.

## How they judged success

No quantitative evaluation, no benchmarks, no ablation studies. The evidence is design rationale plus adoption: three stated design goals (only capture data when asked, because saving every intermediate for a large model is an enormous amount of data; reduce on the server, to cut bandwidth and exploit per-GPU parallelism; keep stateful accumulators on the server, because computing per-neuron top activations over potentially millions of corpus examples through full round-trips would be orders of magnitude slower), and a claim that essentially all of their interpretability work now runs through it, including for models that would fit in a notebook. "Time to first plot" is offered as the metric they think about, borrowed from the Julia community.

## What they found

The tool works well enough to become the default path for their team, and the benefits they report are ones that generalise past the original scaling motivation: because long-running servers hold commonly-used models, a new notebook can connect and start asking questions without waiting for weights to download or the model to initialise; a single notebook can drive several models, or one model across several GPUs for throughput; and any model the lab trains is immediately available to researchers with no hand-off cost. The reported implementation size is modest — around a thousand lines — but heavily dependent on pre-existing distributed-training and ML infrastructure. They also flag that the design tradeoff is flexibility over performance, with specific care taken to move large tensors efficiently rather than through the general serializer, since experiments commonly move tens of gigabytes. The closing note says the interesting contribution is less the interface than the organisational effect: making every model addressable by the interpretability team by default changes how that team relates to the models and to the org.

## Limits and open problems they name

The implementation is tightly coupled to Anthropic's own model code and cluster, so it is not a turnkey artifact for others — the authors describe it as shareable only as experience, and invite correspondence instead of publishing a package. The probe interface is called flexible but unwieldy, introducing server-side state and ceremony (create probe, run pass, then separately retrieve). The wrapper that removes that ceremony is less powerful. No claims are made about correctness of what a user does with the hooks, and there is no discussion of how reproducible or auditable a probe experiment is later.

## What we take from it

A framing and a set of primitives. First: the "only capture what you asked for, reduce at the point of capture, accumulate state where the data lives" triad is the right shape for any instrumentation we build, and it is the same reasoning that decides whether a probe pass costs a round-trip or nothing. Second: the named-point addressing scheme plus parameters-with-the-same-name is exactly the spine a weight-and-activation reader needs — one namespace that spans both views of the model, so a claim about a direction and a claim about a matrix can be stated in the same terms. Third: "time to first plot" is a legitimate design metric for a research harness and we should adopt it, because a white-box model that takes ten minutes to stand up will not be interrogated. Warning, not a method: their design keeps no record of what an experiment did, so reproducibility has to be a deliberate layer we add, not something the hook interface gives us.

## Tags

unit: layer
form: program
method: patching | ablation | probing | other
eval: none
goal: debugging | understanding | evaluation-of-methods
