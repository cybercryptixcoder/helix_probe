# Mona Lisa weights (hand-written MNIST convnet whose weights form the Mona Lisa)

- **Key:** github-csinva-wsp-autoresearch-mona-lisa
- **Authors / organisation:** Chandan Singh's repo (csinva/weight-space-programming-autoresearch); weights written by Claude Opus 5.5
- **Date:** not stated
- **Link:** https://github.com/csinva/weight-space-programming-autoresearch/tree/main/experiments/mona-lisa
- **Kind:** tool (repository experiment with README)
- **Read from:** the experiment README in full (via raw.githubusercontent.com), plus its one-paragraph summary in `experiments/README.md`. NOT read: the source files in `src/` (`cnn_build.py`, `cnn_model.py`, etc.), the `attic/` MLP attempt, the explainer videos and figures, and any agent transcript (none is linked from the README).
- **Relevance to us:** 1 (background): a writing demonstration, no reading test; useful mainly as a vivid example and a cautionary case of what "hand-written" can mean.

## What they wanted, and why
A playful demonstration of weight-space programming: can an LLM hand-write the weights of a deep network that both classifies MNIST digits well (clearly above a linear baseline) and, when its weights are laid out as an image, looks like the Mona Lisa? The original one-paragraph prompt asked for a 16-layer MLP with no training, gradients or fitting. The aim appears to be an existence proof that weights can carry an arbitrary human-chosen picture while still computing a task.

## What they studied
One network written by Claude Opus 5.5: a 16-layer convolutional network (after follow-up requests changed it from an MLP), about 4.0 million weights in the small configuration and about 64 million in the large one. Task: MNIST digit classification. Unit: whole model and its layers.

## How they did it
The final model is a nearest-neighbour classifier compiled into convolution weights. Layer 1 blurs and downsamples the digit; layer 2 turns each pixel y into a pair (1+y, 1-y) that always sums to 2; layer 3 holds 10,240 stored training digits (the first 1,024 per class, unselected) as filters that correlate the input with each stored digit at four small shifts; layers 4 to 15 form a max-tree built from ReLUs that reduces 4,096 scores per class to one; layer 16 combines channels into class scores; argmax gives the answer. Every weight is either a painting pixel, a hand-written constant, or a painting pixel plus a tiny ripple (about 1.5% of the brightness range) encoding a stored digit. Because each input pair sums to 2 and both weights of a pair carry the same painting value, the painting adds a constant per filter that the bias cancels; only the ripple computes the correlation. The picture is formed by flattening each layer's weights in PyTorch order, concatenating, and tiling into a 60 by 172 grid of 14 by 28 tiles; some switched-off channels pad layers to fill whole tiles.

## What counts as an explanation here
A layer-by-layer description of a hand-built program (blur, pair-encoding, template memory, max-tree, readout) with an explicit argument why the painting does not affect the output. Complete for this model.

## How they judged success
MNIST test accuracy on the 10,000 test images, loading the weights into PyTorch in float32, against a trained linear classifier. Visual resemblance judged by eye.

## What they found
Small configuration: 96.17% test accuracy with 4,045,440 weights; large configuration: 97.48% with 64,350,720 weights; trained linear baseline: 92.55% with 7,850 weights. Layer 3 holds 99% of the weights. About 0.8% of weights belong to switched-off padding channels. An earlier 16-layer MLP attempt reached 97.3% but used PCA directions and closed-form LDA readouts, which the authors count as fitting, so it was set aside.

## Limits and open problems they name
Two design choices (correlation instead of plain distance; matching at small shifts) were compared on the test set, so the reported accuracy is not cleanly held out; the blur width was fixed beforehand. The earlier MLP broke the no-fitting rule. Storing training digits verbatim is memory, not a learned algorithm.

## What we take from it
- **A warning on definitions:** "no training" can still mean storing training examples in the weights (a template memory). Any K1 or WSP claim we make should say whether stored data counts.
- **A steganography example:** weights can carry a large, structured, task-irrelevant signal (a picture) whose effect on outputs is exactly cancelled by biases. This is a natural adversarial target for a weight reader: does it see the painting, the ripple, or the computation? A reader that relies on weight statistics would be misled.
- **No reading result:** nothing here measures whether a model can read these weights.

## K1 detail (reading setup)
- **Reader model(s):** None; this is a writing demonstration. Writer: Claude Opus 5.5. No reading score.
- **Target networks:** 16-layer convnet for MNIST classification; 4,045,440 weights (small) or 64,350,720 (large); hand-written, not trained; functionally a nearest-neighbour classifier over 10,240 stored training digits.
- **How the weights were presented:** Not presented to a reader. Written by code (`src/cnn_build.py`) and saved as an `.npz` file; evaluated in float32. Visualised as an image by tiling flattened weights. Token counts not applicable.
- **Prompt:** Public in the README: a one-paragraph request to write from scratch the weights of a 16-layer MLP that does well on MNIST (clearly above linear) and looks like the Mona Lisa when weights are shown in a 4 by 4 grid, using reasoning only, with no training or gradients. Follow-up requests (not reproduced) changed it to a convnet and a gap-free tile layout. No candidate answers.
- **Access regime:** Not stated (presumably an interactive coding session with code execution, since accuracy was measured and choices were compared on the test set; the README does not say).
- **Controls:** Trained linear classifier as a reference. No other controls.
- **Failure modes:** The first MLP attempt used PCA and LDA (fitting); design choices tuned on the test set; reliance on stored training examples.
- **Prompt/format choices that helped or hurt:** Not stated, beyond the follow-up requests that switched architecture and layout.
