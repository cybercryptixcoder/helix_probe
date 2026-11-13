# Circuits Updates, September 2024

- **Key:** transformer-circuits-pub-2024-september-update-index-html
- **Authors / organisation:** Anthropic interpretability team — "Investigating successor heads" by Emmanuel Ameisen and Joshua Batson (edited by Jack Lindsey); "Oversampling a Topic in the SAE Training Set Results in More Detailed Features Related to that Topic" by Trenton Bricken, Jonathan Marcus, Kelley Rivoire, Thomas Henighan (edited by Adam Jermyn)
- **Date:** 2024-09
- **Link:** https://transformer-circuits.pub/2024/september-update/index.html
- **Kind:** blog/research post (lab-notes monthly; two short notes)
- **Read from:** full text (~10.1k characters, one pass, both notes complete). No figures inspected — the OV ordinal matrices, the comparison head and the ICA component tables are described from the prose around them.
- **Relevance to us:** 2 (useful — the successor-head note is a worked example of four independent read-out methods applied to the *same* units and scored against each other, which is exactly the evaluation spine a weight-reading model needs; the SAE note is a short but unusually direct statement that feature coverage is a training-data property, not a capacity property)

## What they wanted, and why

Two unrelated questions, sharing only the lab's standing interest in "which unit does the work, and do different ways of asking agree". The first note replicates Gould et al. (2023): that a handful of attention heads implement ordinal succession — mapping 2 to 3, Wednesday to Thursday, G to H — across numbers, letters, days and months, i.e. that an abstract successor relation lives in identifiable heads rather than being smeared over the network. The team's addition is methodological: rather than one read-out, they run four (weight inspection of the OV circuit, an unsupervised ICA decomposition over heads, mean ablation, and attribution patching) on the same model and compare the resulting rankings. The second note comes out of a safety-motivated search: even the largest Sonnet dictionary contained very few bioweapons-specific features, so they ask whether the training mix, rather than the dictionary size, is the binding constraint.

## What they studied

First note: an 18-layer transformer (the team's standard small model; parameter count not stated in the note). Data is a hand-built set of ordinal sequences — arabic numerals, roman numerals and number words; upper/lower-case letter runs; days of the week and months of the year, abbreviated and full — all confirmed to tokenise as single tokens. Unit of analysis: the attention head, read out as an n×n matrix over ordinal tokens, and additionally abstracted to "meta-head" components by ICA. Second note: Claude 3 Sonnet, its 34-million-feature SAE, and a synthetically generated bioweapons dataset injected into the SAE training mix. Unit of analysis: the dictionary feature and its firing behaviour on harmful bio prompts.

## How they did it

*Successor heads — weight route.* They take each ordinal sequence, run it through the model, and grab the residual stream after the first MLP layer as the representation of each ordinal token, having noticed (following Gould et al.) that the representation shifts sharply between the embedding and that first MLP output. For every head in every layer they push those fixed vectors through the head's output-value circuit, unembed, restrict the logits to the other ordinal tokens, and so materialise a matrix whose (i, j) entry says how strongly token i pushes token j. A head is scored by the fraction of ordinal tokens whose top ordinal output is the correct successor. Notably this works even for late-layer heads, despite the input representations being taken from an early layer.

*Successor heads — ICA route.* They flatten each head's ordinal matrix and stack them into a heads × n² matrix, then run independent component analysis. The stated reason for ICA over dictionary learning is that component loadings should be non-Gaussian (sparser, heavier-tailed) and roughly independent, which permits heads to overlap through constructive interference; they explicitly note that dictionary learning is a plausible alternative that would have produced separate induction and copy-suppression factors instead of merging them. Each component is read as a "meta-head", with each real head's behaviour being a weighted sum of components.

*Successor heads — causal routes.* They run forward passes on the full ordinal sequences ("1 2 3 4 5 …") and mean-ablate each head's output, measuring the resulting change in the correct successor's logit, averaged over all sequences and positions: the "ablation effect". Independently they compute head attributions with attribution patching, i.e. the cheap linearised approximation of that same ablation, and check whether the fast method reproduces the slow one.

*Oversampling.* Two SAE training runs differing only in whether the generated bio data is in the training mix. They then inspect the biology-relevant features in each dictionary — which features fire on harmful bio prompts and what those features' own top activating examples look like — and compare qualitatively.

## What counts as an explanation here

For succession: an assignment of a function to specific units (these three heads implement succession by their direct effect), plus a decomposition of all heads into a small set of reusable components (succession, induction, category projection) whose weighted sum reproduces each head. It is a partial, mechanistic explanation of one narrow behaviour — not a model of the network, and it predicts nothing outside ordinal lists. For the SAE note: no explanation is attempted; the claim is a claim about controllability of the dictionary ("oversampling a topic gives you features about that topic"), supported by showing the most predictive feature for harmful bio prompts before and after.

## How they judged success

Successor heads are judged four ways and then cross-checked: (i) fraction of ordinal tokens mapped to their successor under the OV circuit, compared against a randomly chosen head shown for reference; (ii) whether the top OV-scoring heads also load most heavily on the ICA succession component; (iii) rank by mean-ablation effect on the correct successor logit; (iv) agreement between attribution patching and the other three. The oversampling note uses no metric at all — the evidence is the identity of the single most important feature for predicting harmful bio prompts before and after, described in words.

## What they found

*Successor heads.* In the top-scoring head, approximately 80% of ordinal tokens map most strongly to their successor, giving a strong super-diagonal in the ordinal matrix; behind the successor, the next-strongest outputs are the equivalent token in other ordered lists ("1" also pushes "two", "second", "February") and then neighbouring members of the same list, while earlier members of the same list are almost always suppressed. The second head reaches roughly 60% successor accuracy but its errors are block-structured: it confuses within a category (numerals with numerals, days with days). Four methods, one answer at the top: the top three heads by OV score are the same as the top three by ICA component loading, and those same three are ranked 1st, 3rd and 5th by ablation effect — so weight side does identify on-distribution-important heads. The two heads that rank high on ablation but low on component score sit in much lower layers (3 and 5) than the successor heads (10, 11 and 13), and the note speculates they contribute by Q- or K-composition into the later heads or by feeding later MLPs. The surprise is attribution patching: the single highest-attribution head is also the highest by every other method, but agreement below the top is described as relatively low across all three comparisons. ICA also produced an induction component with category bleed (Monday to Monday/Mon) and a category-projection component that maps number words and numerals into a near-uniform mix of the first few ordinals while, in its negative direction, makes each roman numeral suppress all roman numerals — descriptions the authors concede are not entirely clean. They connect the succession component and the category-projection component to Gould et al.'s compositional split of ordinal *value* from sequence *category*.

*Oversampling.* Without bio data the most relevant biology features were about resources for building dangerous or illegal things — bombs, recreational drugs — i.e. adjacent to the target but broader. With bio data in the mix, the top feature for predicting harmful bio prompts became one centred on pathogen modification (text about enhancing a virus's ability to evade immunity, to survive and remain infectious), with another on viral particle dispersal. The authors read this as evidence that feature coverage is steerable through data rather than purely a function of dictionary size.

## Limits and open problems they name

The successor note is framed throughout as lab-meeting material, not a mature paper, and it states its own gaps: the four methods agree at the top and diverge below it, with the low-layer high-ablation heads unexplained; whether these heads matter beyond bare ordinal lists (list incrementing, years, prose such as "the next day, Tuesday") is posed as future work; and the authors' own hope is that head-level decomposition could be used generally to expose compositional linear factors of the residual stream, which is a proposal, not a result. Methodologically, all four read-outs use only the direct pathway, and the weight route is scored on ordinal matrices while it is fed representations drawn from an early layer even for late heads — a mismatch the note acknowledges works but does not justify. The oversampling note is explicitly qualitative: two runs, no held-out evaluation, no measurement of how much the oversampled features cost elsewhere in the dictionary, no test of whether they generalise to non-synthetic bio text.

## What we take from it

*Measure:* the "four read-outs, one ranking" protocol is the most transferable thing here for us. Take a behaviour with a crisp correctness criterion, rank units by a weight-only score, by an unsupervised factorisation over units, by true mean ablation, and by attribution patching, then report the rank correlation between them rather than a single number — and report agreement at the top separately from agreement overall, because the head of the list agreeing while the tail does not is the shape they found, and it is the shape our own probes will have.

*Method:* the OV-matrix construction generalises directly to our setting. Restrict the unembedding to a closed answer set and you get, per head, a cheap behavioural signature without running a dataset — the "score a head by fraction of inputs whose top in-set output is correct" tally is a single line of code on top of that. *Warning:* it can be computed from early-layer input representations even for late heads and still "work", which means a good OV score is not evidence that the head sees that representation in practice — pair any weight-side score with an ablation, exactly as this note does.

*Method, second:* ICA over stacked unit-behaviour matrices, used to produce "meta-head" components whose weighted sum approximates each unit, is an alternative to dictionary learning whenever we want overlapping factors rather than sparse ones — and the authors' own stated trade-off (dictionary learning would have separated induction from copy suppression, ICA merges them) is a clean way to choose between the two for a given question. If we want a feature separated, demand non-negativity and sparsity; if we want a shared motif explained across units, allow signed, non-sparse loadings.

*Warning:* attribution patching disagreed with true ablation below the very top of the list in a setting that is about as favourable as it gets (single tokens, closed output set, one behaviour). Any place we use attribution as a surrogate for ablation, the entry should carry this caveat.

*Framing:* the oversampling note is the shortest usable statement of the "coverage" problem for us — what a dictionary can represent is bounded by what enters the training activation stream, and coverage is manipulable by data. For a white-box model that must predict on inputs we care about, that means our probe corpus needs deliberate coverage of the cases we intend to claim about; an absence of features for a concept is not evidence of absence in the model.

## Tags

unit: head | circuit
form: graph | description
method: weight-analysis | attribution | ablation | decomposition | SAE
eval: ablation | patching | benchmark | faithfulness
goal: understanding | safety/auditing | evaluation-of-methods
