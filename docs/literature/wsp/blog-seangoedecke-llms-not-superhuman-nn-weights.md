# LLMs are not superhuman at reading and writing neural network weights

- **Key:** blog-seangoedecke-llms-not-superhuman-nn-weights
- **Authors / organisation:** Sean Goedecke; personal blog
- **Date:** 2026-11-03 (date as cited by arXiv 2611.12066; the extracted article body itself carries no date line)
- **Link:** https://seangoedecke.com/llms-are-not-superhuman-at-reading-and-writing-neural-network-weights/
- **Kind:** essay (critical blog post)
- **Read from:** full text of the post, including footnotes and the Hacker News edit note. The heatmap figure (`fig1_layer1_magnitude.png`) was not viewed. The original Sparks post being critiqued was not read for this entry; claims about it below are Goedecke's paraphrase.
- **Relevance to us:** 2 (useful)

## What they wanted, and why
A rebuttal to the "Sparks of Weight-Space Programming" post (Takehi et al.), which reported GPT-6 Astra identifying which game a small policy network plays from its weights, editing those weights, and fixing a 0.8B Qwen model's mathematics by editing weights. Goedecke argues none of this is superhuman AI research: a competent human ML researcher could do each task with simple, known techniques. The stake is whether WSP signals a route to recursive self-improvement; he thinks it should not change how AI research is done.

## What they studied
No new experiments beyond a short illustration. Targets discussed: the small game-playing policy networks from the Sparks post (about 17k weights; first-layer inputs are labelled channels per grid cell, e.g. "agent", "moving objects") and a 0.8B Qwen model that looped after 32k tokens.

## How they did it
Argument by reconstruction. For the game-identification task, he shows a three-line NumPy computation: load the first dense layer kernel, reshape to channels x grid x hidden units, and take the L2 norm over the 32 hidden units per input, giving a per-channel spatial heatmap. He claims the player position and moving-object layout in those heatmaps make several games obvious (e.g. a horizontal player line at the bottom for Breakout, the maze for Pac-Man). For the Qwen fix, he describes the steering/abliteration route a human would take (contrast looping vs. non-looping texts, difference of residuals, attribute to weights, trim top contributors) and notes that this is what Astra reportedly did, with four text pairs, iterative trimming and testing. Note an internal inconsistency: the text says each channel listens to an 8x8 grid cell, but his code reshapes the input to a 10x10 grid with 5 channels.

## What counts as an explanation here
Not applicable; the post is about whether claimed capabilities need anything beyond first-layer weight norms (reading) or steering-style edits (writing).

## How they judged success
Informal: whether a skilled human with standard tools could do the same. No metrics.

## What they found
His claims: (1) game identification reduces to first-layer weight-norm heatmaps over labelled spatial inputs; doing the norms mentally is impressive arithmetic rather than research insight; (2) the Qwen model was not weak at mathematics as such: it failed only on problems needing over 32k tokens because of looping, and all shorter problems were already solved by the original model; (3) Astra had Python access for the Qwen work, unlike the toy game networks; (4) writing a network for a task expressible as a simple program is known to be possible, even by hand (he points to AdderBoard and a hand-made transformer post). He likens direct weight editing to an LLM patching compiled binaries: a neat trick, but training remains the better route.

## Limits and open problems they name
He skips most Sparks examples, including writing networks from scratch. In the HN follow-up he acknowledges a commenter disputing that the heatmaps are obvious, which he attributes to unfamiliarity with toy RL maps.

## What we take from it
- **A baseline to beat:** any claim that an LLM "reads" weights must outperform a trivial script (e.g. first-layer per-input weight norms) given the same labelled inputs. We should run such a non-LLM baseline in K1.
- **A control:** remove input-channel labels or spatial layout and see whether reading survives; labelled, spatially organised inputs make first-layer reading easy.
- **A warning:** distinguish tool-free reading from tool-assisted analysis; the Qwen edit used Python and so is a standard interpretability workflow, not native reading.
- **A framing:** "superhuman mental mathematics, not superhuman AI research" (his footnote) is a likely reviewer objection to our own results.

## K1 detail (reading setup)
- **Reader model(s):** GPT-6 Astra (in the Sparks post, as described by Goedecke). Scores: not stated in this post.
- **Target networks:** Small game-playing policy networks, about 17k weights, first dense layer feeding 32 hidden units; inputs are labelled channels over a grid (text says 8x8, his code implies 5 channels x 10x10). Trained to play several games (Breakout and Pac-Man named). Also a 0.8B Qwen LLM (for editing, not reading).
- **How the weights were presented:** Not stated in this post for the LLM. Goedecke's own reconstruction loads a `.npz` with a key `actor/dense1/kernel`, implying named layer tensors.
- **Prompt:** Not stated.
- **Access regime:** Per footnote: toy game networks read without Python; Qwen editing done with Python access. Budgets not stated.
- **Controls:** None in the Sparks work are described here. Goedecke's implied control is a simple norm-heatmap baseline; for Qwen, he notes the original model already solved all sub-32k-token problems.
- **Failure modes:** Not discussed.
- **Prompt/format choices that helped or hurt:** Implied: labelled input channels and a spatial input layout make first-layer reading easy. No direct evidence.
