# Notes: features and SAE evaluation (batch a)

**What an explanation is here.** All five papers treat the SAE latent (a dictionary direction plus a short text
label) as the unit of explanation. None of them claim to explain a behaviour end to end; the dictionary is raw
material (arxiv-2408.05147 says so outright). The labels are increasingly judged as *predictions*: predicting a
latent's activations from its description (simulation, detection, fuzzing; arxiv-2309.08600, arxiv-2410.13928) or
predicting the output effect of intervening on it (intervention scoring, arxiv-2410.13928; steering,
arxiv-2501.17148).

**How success is measured.** Three families recur:
1. *Fidelity of the dictionary as a model substitute*: L0 vs MSE/FVU, and spliced-in next-token loss (delta LM loss,
   loss recovered vs zero-ablation, or equivalent pretraining compute). Reconstruction and behavioural fidelity
   disagree (FVU vs delta loss in arxiv-2408.05147), and even a 16M-latent SAE on GPT-4 behaves like a model with
   about 10% of the compute (arxiv-2406.04093); Pythia perplexity 25 to 40 (arxiv-2309.08600).
2. *Interpretability of units*: LLM-scored descriptions, against baselines of neurons, random directions, PCA and ICA
   (arxiv-2309.08600) or top-k neurons (arxiv-2410.13928); plus human agreement.
3. *Downstream usefulness*: patching sparsity on IOI (arxiv-2309.08600), probe loss and ablation sparsity
   (arxiv-2406.04093), concept detection AUROC and harmonic-mean steering (arxiv-2501.17148).

**Main tensions and open problems.**
- Input-side and output-side explanations are nearly uncorrelated (intervention vs fuzzing, arxiv-2410.13928), and
  good detection does not give good control (SAE-A, arxiv-2501.17148). What makes a unit fire and what it does are
  separate questions.
- Cheap supervised baselines (DiffMean, linear probes) and prompting beat SAEs on detection and especially steering
  (arxiv-2501.17148). Any new unit must be compared with them.
- No agreed SAE quality metric; scores depend on scorer model and prompt; wider SAEs split features rather than find
  new ones (arxiv-2408.05147, arxiv-2410.13928).
- Reading circuits from weights (via transcoders) is named as open in arxiv-2408.05147.

**Bearing on a predictive white-box model from weights.**
- Judge the model on behaviour under intervention (spliced loss, KL to counterfactual, intervention score), not on
  reconstruction error or label plausibility.
- Report residual error honestly; the SAE literature shows a large unexplained gap at every scale, so a white-box
  model needs an explicit account of what its units miss.
- Reusable evaluation kit: neuron/PCA/ICA/random baselines, DiffMean and probe baselines, delphi detection/fuzzing/
  intervention scoring, Concept500, delta LM loss, "units edited to reach target KL".
- Gemma Scope provides a ready substrate if we need a comparison basis on an open model.
