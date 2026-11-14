# Interpretability Infrastructure at Frontier Scale: Harvesting Activations from a Trillion-Parameter Model

- **Key:** goodfire-com-blog-interpretability-infra-at-frontier-scale
- **Authors / organisation:** Michael Anderson, Tucker Fross, Michael Byun; Goodfire
- **Date:** 2026-02-25
- **Link:** https://www.goodfire.com/blog/interpretability-infra-at-frontier-scale
- **Kind:** blog/research post
- **Read from:** full text (whole prose body; no appendix, no methods section — the page ends at the hiring note and a "read more" list). No figure inspected: the four figure captions are read, the charts are not, so no plotted quantity is quoted here.
- **Relevance to us:** 2 (useful)

## What they wanted, and why

Interpretability methods were developed on toy models — they cite Anthropic's 2023 single-layer, 512-neuron model explicitly as the origin — while the systems deployed today are past a trillion parameters and are mixture-of-experts, multi-step, tool-using and served through an inference stack. Their claim is that the gap is not conceptual but infrastructural: the methods already exist and cannot be *fed*, because collecting activations at the scale a frontier SAE needs is a systems problem. The post is therefore a report on one specific engineering deliverable rather than on a finding — harvesting a single layer's residual-stream activations over three billion tokens of a trillion-parameter model in one overnight run, so that an SAE can then be trained on it. It is an argument for the position that data collection, not method design, is the binding constraint at the frontier.

## What they studied

Kimi K2 Thinking (a trillion-parameter mixture-of-experts model with a long reasoning trace), served on eight GPUs per node under SGLang. The unit of analysis is the **residual stream after the MLP contribution is added**, at a single layer, for prefill tokens only — not neurons, not heads, not whole-model behaviour. The artifact collected is the activation tensor plus enough metadata to map each row back to a token in the source corpus. Scale: three billion tokens, which they gloss as roughly half of English Wikipedia, compressed to about 33 TB on disk.

## How they did it

They forked SGLang rather than writing a harness around it, on the judgement that the fork could be kept surgical. The key strategic decision is to skip decode entirely: SAE training does not need activations from a model that is generating, so they precompute rollouts and harvest only prefill, where tokens are processed in parallel across sequences and the attention computation is a large dense matrix multiply. Two further decisions reduced complexity — capture at the tensor-parallelism sync point (after the current layer's sharded computation is merged with prior layers' aggregate representations), which avoids a gather step entirely — and no CUDA-graph support, since graphs mainly buy decode speed they do not use. Transport off the GPU is a three-stage asynchronous pipeline: the forward pass copies each tensor into a preallocated GPU staging buffer (device-to-device, so inference never blocks); the only thing pushed into a CPU-side ring buffer is a small record of tensor handle, provenance metadata and a CUDA event; a sidecar thread waits on that event and copies into preallocated pinned host memory; a writer thread compresses, splits and persists. The writer does the semantic work the inference server undoes — it must re-split continuously-batched flattened token tensors back into per-sequence records, stitch a document's chunked-prefill captures back together by composing chunk-relative with absolute offsets, and interpret metadata fields differently per mode, since SGLang's own fields change meaning between prefill and decode.

## What counts as an explanation here

Not an explanation of model behaviour at all. The page's artifact is an *enabling* one: a corpus of activations with intact provenance, plus the throughput number that says the corpus is affordable. The interpretability claims are held back — they say they trained an SAE on the three billion activations and that the resulting features are steerable, including mid-chain-of-thought and in real time, but the actual features, the dictionary, the steering implementation and any measurement of either are explicitly out of scope ("the implementation of steering is out of scope for this blog post"). So this entry should be read as a measurement of a data-collection pipeline, with the downstream science promised rather than shown.

## How they judged success

Throughput and wall-clock on real hardware, with a naive-throughput arithmetic baseline: about 14,000 tokens per second of harvested activations on one eight-GPU node; ten concurrent nodes therefore put three billion tokens at roughly six hours; they compute that a naive approach on the same hardware would need close to a week, and that harvesting at ordinary generation speed of order a hundred tokens per second would take over a year of continuous GPU time. There is no accuracy-fidelity check of the harvested activations (no comparison of the captured residual against a reference forward pass), no throughput-versus-concurrency curve, no measurement of the overhead the patch imposes relative to unforked SGLang, and no false-provenance rate — which is what you would want to publish for a pipeline whose entire product is correctly-attributed tensors. The steering claim is supported by illustration only.

## What they found

The headline is that the pipeline works at the stated scale and pace: three billion single-layer activation rows from a trillion-parameter MoE model in one overnight run, 14,000 tokens/s per node, ~33 TB compressed, six hours on ten nodes. Two engineering observations are the substance. First, the reason this is hard is that the optimizations that make inference fast are exactly the ones that destroy provenance — dynamic continuous batching concatenates unrelated sequences into one flat token tensor, chunked prefill splits one document across several forward passes with different metadata, tensor parallelism shards one activation across ranks, and CUDA graphs fix execution shapes. Second, the cheap way out is to stop harvesting the thing you do not need: restricting to prefill removes the memory-bound, sequential phase and makes sequence-level parallelism available. They also report that the same hooks made *writing* easier than expected, which is why real-time chain-of-thought steering came almost for free.

## Limits and open problems they name

Almost none are named, and that is the entry's main warning. They note that steering is out of scope, and they frame the whole post as behind-the-scenes engineering that "complements" their research rather than as a research result. They do not discuss: whether the captured residual at the post-MLP sync point is numerically what a reference forward pass would produce; what the write path's compression does to the activations; how the pipeline behaves when disk I/O falls behind inference for long enough to overflow the staging pool; whether the single layer and prefill-only restriction is sufficient for the questions they want to ask; or cost. All of these are mine, not theirs, and they should be attached to any citation of the number.

## What we take from it

Three concrete things. (1) **A collection-time metadata schema, not a post-hoc join.** Their writer emits a canonical per-sequence record and deliberately hides the server's internals from downstream consumers, which is the right division: the inference engine's batching decisions are not a stable interface, so provenance has to be reconstructed at the boundary and frozen there. (2) **The prefill-only insight generalises to us.** If the analysis you are planning does not need the model mid-generation, harvesting the parallel phase instead of the sequential one changes the cost by orders of magnitude; this is the cheapest available lever on any activation-collection budget we set. (3) **A warning about what publishing a throughput number buys.** Fourteen thousand tokens per second is a fact about their pipeline, not about their data — a high-performance collection run with no fidelity check is a claim we cannot check, and our own write-ups should pair any throughput figure with a residual reconstruction error against a reference pass, which costs one forward pass and is the only thing that separates "we collected a lot" from "we collected the right thing."

## Tags

unit: layer
form: description
method: SAE
eval: benchmark
goal: understanding
