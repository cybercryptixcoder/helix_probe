# Language Models Use Trigonometry to Do Addition

- **Key:** arxiv-2502.00873
- **Authors / organisation:** Subhash Kantamneni, Max Tegmark; MIT
- **Date:** 2025-02
- **Link:** https://arxiv.org/abs/2502.00873
- **Kind:** paper
- **Read from:** abstract and sections (arXiv HTML main text; appendices only via summary)
- **Relevance to us:** 3 (central)

## What they wanted, and why
LLMs do arithmetic but how they do even simple addition was unknown. The authors want a complete mechanistic account of one capability, covering both how inputs are represented and how components transform those representations into the answer, in real pretrained models rather than toy ones. The larger goal is showing that a full representation-plus-algorithm explanation of an LLM capability is achievable, down to individual neurons.

## What they studied
GPT-J (6B; main, because its plain MLP makes neuron analysis easier), Pythia-6.9B (replication), Llama3.1-8B (appendix, weaker results). Task: a+b for a, b in 0..99 (10,000 prompts); model accuracy 80.5% (GPT-J), 77.2% (Pythia), 98.0% (Llama). Units: residual-stream representations of numbers, attention heads, MLP layers, and individual MLP neurons.

## How they did it
They Fourier-analyse residual-stream activations of number tokens and find sparse peaks at periods 2, 5, 10 and 100 plus a linear trend. They fit a "generalised helix": each number represented by a linear term plus a cosine/sine pair per chosen period, mapped into a 100-dim PCA space by linear regression, testing subsets of up to four periods. To test whether the helix is what the model uses, they patch helix-fitted activations into corrupted prompts and measure logit difference restored, compared to patching real activations, a PCA baseline of equal size, circle-only and polynomial baselines, a train/test split, and a helix fit to shuffled number values (a null). They then trace the computation with activation patching of heads and MLPs, classify heads by which helices they carry (a, b, or a+b), and test whether the last-token state is fitted by helix(a+b). At neuron level, they select neurons by attribution patching, keep them while mean-ablating the rest, and fit each neuron's preactivation as a function of a, b and a+b (linear terms plus cosines at periods 2, 5, 10, 100) by gradient descent; then patch the fitted preactivations in place of the real ones. Finally they analyse errors.

## What counts as an explanation here
A representation (numbers as helices) plus a named algorithm ("Clock"): embed a and b as helices, move them to the last token with attention heads (mostly layers 9 to 14), build helix(a+b) in MLPs 14 to 18, read it out to logits in MLPs 19 to 27. It is backed by parametric closed-form models of activations and neurons (few parameters each) that can be substituted into the network. Partial: the step that combines helix(a) and helix(b) into helix(a+b) is hypothesised (trig identities) but not isolated.

## How they judged success
Fraction of logit difference restored by patching (fitted representation vs real activations vs PCA baseline); fraction of all-heads or all-MLPs effect recovered by a subset; accuracy when mean-ablating all but selected neurons; fraction of performance kept when real neuron preactivations are replaced by fitted functions; error distribution with a chi-squared test.

## What they found
The helix fit with four periods restores nearly as much logit difference as patching the full layer and beats the PCA baseline; shuffled-value helices are not causal. Helix(a+b) fits last-token states better than a 27-dim PCA at some layers with only 9 parameters. Patching 20 heads recovers about 84% of the effect of all 448 heads (11 carry a and b, 5 carry a+b, 4 mixed). Patching 11 MLPs (14 to 27 except 15, 24, 25) gives 95% of the all-MLP effect. About 1% of neurons (4,587) suffice to keep 80% accuracy when the rest are mean-ablated; replacing their preactivations by the fitted periodic functions keeps about 75% of performance. Errors are mostly off by minus 10 (45.7%) or plus 10 (27.9%); carry failure does not explain them; a downward bias explains more errors on larger inputs. The helix is causally relevant on other numeric tasks but loses to PCA on some (integer division, multiply by 1.5).

## Limits and open problems they name
The mechanism building helix(a+b) is not isolated. Helix is less causal in Llama3.1-8B, so other models may differ. Extra numeric structure beyond the helix. Single-token numbers only; tokenisers splitting digits need other methods. Clock may be one of several parallel algorithms.

## What we take from it
(1) The strongest template in this batch for a predictive white-box model: replace real activations and even individual neurons with closed-form parametric functions of the input, patch them back in, and report fraction of performance preserved (75% at neuron level here). That is a quantitative "does our reconstruction run in place of the original" test. (2) Fourier analysis over a structured input space is a cheap way to discover the representation basis before fitting. (3) Controls to copy: equal-dimension PCA baseline, shuffled-label fit, train/test split for the fit. (4) Explaining errors (off-by-10 pattern) is a strong test that the reconstruction predicts the model, not the ideal task. (5) Naming note for this project (helix_probe): helical/periodic number representations are already established here, so any claim about helices must go beyond this paper.

## Tags
unit: direction, head, layer, neuron, circuit
form: program, replacement-model, causal-abstraction
method: patching, ablation, decomposition, other
eval: patching, ablation, prediction/simulation, faithfulness
goal: understanding, science
