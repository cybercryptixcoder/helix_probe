# Graph Metanetworks for Processing Diverse Neural Architectures

- **Key:** arxiv-2312.04501
- **Authors / organisation:** Derek Lim, Haggai Maron, Marc T. Law, Jonathan Lorraine, James Lucas; MIT CSAIL, Technion, NVIDIA
- **Date:** 2023-12 (ICLR 2024)
- **Link:** https://arxiv.org/abs/2312.04501
- **Kind:** paper
- **Read from:** full text (HTML, main text and conclusion; appendix only in part)
- **Relevance to us:** 3 (central)

## What they wanted, and why
Metanetworks take another network's weights as input. Earlier equivariant metanetworks (DWSNets, NFNs) were hand-built for plain MLPs or CNNs and must be redesigned for each new layer type. The authors want one metanetwork that can read weights of arbitrary architectures (including attention, residuals, normalisation) while respecting the permutation symmetries of the weights. This is a step toward general tools that analyse, edit or predict properties of real networks directly from their parameters.

## What they studied
Input networks: about 30,000 2D CNNs of varying width, depth and normalisation; a "Diverse Architectures" zoo of about 30,000 networks mixing 1D CNNs, DeepSets, ResNets, Vision Transformers and 2D CNNs (all CIFAR-10 classifiers); and implicit neural representations (INRs: small MLPs fit to images or sinusoids). Unit: individual parameters as edges of a graph.

## How they did it
Each input network is turned into a "parameter graph" where every parameter is exactly one edge. Linear layers follow the neuron graph, with a separate bias node per layer. Convolutions get one node per input and output channel and parallel edges per kernel position, with positional features (a multigraph). Multi-head attention gets nodes for feature dimensions, query/key/value and output, with head identity in node features. Residual connections become fixed weight-1 edges. Normalisation layers get two extra nodes (learned mean, learned variance) linked to normalised neurons. A standard message-passing GNN updates node and edge features; edge outputs give per-parameter predictions, pooled edges give network-level predictions. Theory: they define neural DAG automorphisms, show these induce function-preserving parameter permutations, and prove the GNN is equivariant to them; they show GMNs can express StatNN and NP-NFN on MLPs, and can simulate the forward pass of any feedforward network given its computation graph. Experiments: predict CIFAR-10 test accuracy from weights; edit 2D INRs (contrast, dilation); self-supervised representation of sinusoid INRs with a linear probe for amplitude and frequency.

## What counts as an explanation here
None in the interpretability sense: the output is a learned predictor from weights to a property, or a weight edit. Its relevance is as the input encoding for any weight reader: a principled, symmetry-respecting graph form of an arbitrary network.

## How they judged success
R^2 and Kendall's tau for accuracy prediction, on a large training split, a small split, and an out-of-distribution split (trained on narrower networks, tested on wider). Baselines: DeepSets and the Deep Meta Classifier of Eilertsen et al. (arxiv-2002.05688); DWSNets and NFNs could not be run on these architectures. Test MSE for INR editing against NFN/NFT variants; test MSE of a linear probe for INR self-supervised learning against DWSNets, MLP and transformer.

## What they found
GMNs were best in all six accuracy-prediction settings, with the biggest margins in low-data and OOD cases. Large split: R^2 0.978 / tau 0.915 on Varying CNNs (DMC 0.948 / 0.876) and 0.975 / 0.908 on Diverse Architectures. OOD Varying CNNs: GMN R^2 0.891 versus DMC 0.387; on OOD Diverse Architectures DMC's R^2 was negative while GMN reached 0.768. INR editing: best on contrast (MSE 0.0197) but behind NFT on dilation (0.0603 vs 0.0510). INR self-supervised probe: MSE 1.13 versus 1.39 for DWSNets.

## Limits and open problems they name
Not tested at billion-parameter scale (they argue scalable GNNs could reach it). No formal rules for designing parameter graphs for new layers. The automorphism theory is proved for the costlier computation graphs, not parameter graphs. Only permutation symmetries are handled; ReLU rescaling symmetry is not. Uses a basic GNN.

## What we take from it
The parameter-graph construction is directly reusable as the input format if we build a learned weight reader for transformers: it already covers attention, residuals and normalisation. The forward-pass-simulation result is notable for us: a reader over the computation graph can in principle compute what the network computes, so "predict behaviour from weights" is expressible in this architecture class. Their OOD split (train on small, test on larger networks) is a good evaluation template. Warning: scale-symmetry is unhandled, and nothing here is human-readable.

## Tags
unit: weights
form: other (learned metanetwork / graph encoding)
method: weight-analysis, other
eval: downstream-task, benchmark
goal: science, control/editing
