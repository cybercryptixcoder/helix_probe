# PySvelte: a bridge that makes Svelte visualisations callable from Python

- **Key:** github-com-anthropics-pysvelte
- **Authors / organisation:** Anthropic (repository; README carries no individual authorship)
- **Date:** 2021 (copyright line in the licence header)
- **Link:** https://github.com/anthropics/PySvelte
- **Kind:** tool
- **Read from:** full text — the repository README only; source code, the `AttentionMulti` component and its companion documentation file were not read
- **Relevance to us:** 1 (background)

## What they wanted, and why

Their premise is that understanding a network requires getting a lot of information out of its internals and into a readable form, which usually means a visualisation. The friction is that the two halves live in different languages: model work happens in Python because that is where the training and distributed libraries are, and good interactive visualisation happens in the browser stack. Doing either language's job in the other language is a handicap, but living in both ecosystems at once has its own cost. So the goal is a seam between them that is thin enough to use daily and opinionated enough that a researcher with no web background can use what a colleague built.

## What they studied

Not models or behaviours — the authoring and delivery path for interpretability visualisations. The unit is the component: a Svelte component in a `src/` directory together with an optional companion Python file that carries its documentation, type signature and validation.

## How they did it

A component dropped into the source folder becomes callable from Python under the same name, with argument completion drawn from the companion Python file; building happens automatically from the Python side so no npm step is required, and keyword arguments are mandatory because positional mapping would break whenever the component is edited. NumPy arrays cross the boundary and arrive as JavaScript ndarrays. In a notebook the component renders if it is the last expression in a cell, and there is an explicit show call for the items that are not. Rendered items are composable HTML objects that can be concatenated into a page, and a publish call writes the result to a bucket for sharing, optionally announcing it in a chat channel so colleagues discover it.

## What counts as an explanation here

None in the explanatory sense — this is a rendering channel. Its contribution is to the *form* an explanation may take: a bespoke interactive view of a tensor (attention patterns being the worked example) that is cheap enough to produce that it becomes a normal step in analysis rather than a project.

## How they judged success

No evaluation of any kind. Success is argued from design goals: easy bespoke visualisation, modular and reusable components, easy publication to standalone shareable pages, and usability by researchers who know nothing about web technology.

## What they found

The library is presented with a blunt disclaimer at the top of the README — unsupported, provided as-is, and an example of one way to solve the problem, with many features dead unless the user writes their own configuration file. The concrete artifact they point at is an internal component for visualising attention patterns from self-attention blocks, a variant of which renders inside their transformer-circuits framework paper.

## Limits and open problems they name

Explicitly unsupportable and partial: the publishing and sharing features need per-lab configuration functions, and no guarantee is offered that it runs for anyone else. Beyond the disclaimer there is no discussion of correctness, of what a visualisation omits, or of how to keep a rendering faithful to the tensor that produced it.

## What we take from it

A warning more than a method, and a small piece of design vocabulary. The vocabulary worth keeping is the *companion-file* idea: a visualisation carries its own type signature and validation in the language that produces the data, so the failure is caught before rendering rather than inspected by eye afterwards — that is the cheapest version of the "does this view lie about the tensor" check. The warning is the disclaimer itself: this is what tooling looks like when it is built for one lab's workflow and released afterwards, so we should not plan on adopting it, and should treat publication as a separate first-class concern rather than an afterthought bolted onto a component. Relevant to us only as background on how the transformer-circuits results were actually produced.

## Tags

unit: whole-model
form: description
method: other
eval: none
goal: understanding | debugging
