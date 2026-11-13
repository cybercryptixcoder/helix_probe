# The "agentic interpreter": a far-future idea

> **THIS IS NOT WHAT WE ARE BUILDING.** It is a speculative long-range vision, recorded so it is not lost. Shreyas called it "sci-fi" and said explicitly that it should not be mistaken for the plan. Nothing here is decided or scheduled.
>
> **For what we are actually building, read [`docs/WHAT_WE_ARE_BUILDING.md`](../WHAT_WE_ARE_BUILDING.md).**

## The idea (Shreyas, 2026-11-13, paraphrased)

The idea is an agentic setup that interprets a model the way a human researcher would, but in a loop that can run indefinitely and keeps gathering information:

- **Weights live in a store.** The agent fetches regions itself, or writes code to fetch them (e.g. "only weights above a threshold", "only rows meeting some criterion"). It does not wait to be handed slices.
- **It can write and run code**: math and computation over weights or weight segments, and building its own tools rather than being limited to ours.
- **Reading weights is only one of its mechanisms.** It can probe, compute, edit and run the network: whatever a human researcher would do by hand.
- **Expected limit:** it likely works better on small models than on large transformers. That is unknown.

## How it relates to the current work

- Parts of it may survive into the real design. In particular, letting the reader **query the weight store itself** (rather than being fed slices) is a live candidate. It is not decided.
- The whole-loop version is deliberately not being built now. The current build is the Weight Reading Lab (see the pointer above).
