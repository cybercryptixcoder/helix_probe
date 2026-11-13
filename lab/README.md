# Weight Reading Lab

Hand a network's weights to an LLM and see what it makes of them. This is the hands-on side of K1 (`docs/DIRECTIONS.md` §2f; `docs/WHAT_WE_ARE_BUILDING.md`).

## Run it

```bash
pip install numpy            # the only requirement
python3 lab/server.py        # then open http://localhost:8765
```

Click **Add key** and paste your Luminal key. It is saved to `lab/.env`, which is gitignored and stays on your computer.

## What's in it

- **Specimens** (left): networks with known answers, which stay hidden until you reveal them.
  - Tiny Boolean circuits, hand-written.
  - MIT's Sparks game policies and shape generators, from their released logs (CC BY 4.0).
  - One-layer transformers trained here on modular arithmetic: add, then sub and mul once trained. Run `python3 lab/targets/build_registry.py` after training a new one.
- **Variants**, the controls the literature uses:
  - shuffled weights;
  - untrained (random with matched statistics);
  - permuted hidden units, which compute the same function.
- **Explore** (middle):
  - Click a tensor to see its heatmap, and drag to select a region.
  - Or add whole units (an MLP neuron's in and out weights, an attention head's Q/K/V/O, an MLP layer's hidden unit), so slices never cut a unit in half.
  - The gauge shows the estimated prompt size against DeepSeek's 163,840-token context. The estimate calibrates itself from the first real run.
- **Ask** (right):
  - Use any prompt you like, with templates and placeholders: `{{weights}}`, `{{arch}}`, `{{context}}`, `{{original_question}}`. Toggles control whether the architecture and the meaning of the inputs are revealed; turning them off is the blinding control.
  - Modes: **text only**, or **+ python**. In python mode the reader writes and runs its own code on the weights, optionally with `run(x)` to run the network.
  - You can also set the thinking effort, the output budget, repeats, and an automatic shuffled-weights control.
- **Notebook**: every run is saved to `lab/runs/<id>.json`. Grade runs, add notes, reveal answers, and compare two runs side by side.

## Notes

- The python mode runs the reader's code on your machine in a separate process. It has a time limit and an import allowlist, with no `open()` and no network modules. That is a safeguard, not a security boundary.
- Reader: DeepSeek V4.1 Flash via Luminal. On the record it is a weak raw-text reader (see `docs/literature/wsp/K1_STATE_OF_ART.md`): it often spends its whole budget copying weights. Give it room (32k–64k output) and expect that failure mode.
