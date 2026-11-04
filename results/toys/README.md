# Toy rematch (November 3-4, 2026)

The two toy boxes v1 failed, same settings as v1's live runs (grid: 30 learn steps + 5 goals, library on; knob: 25
learn steps + 5 goals, library off). v1 = the frozen first version; v2-directed = every experiment chosen by the
experimenter (with the new experimenter prompt); v2-mixed = the v2 default (every other experiment a random probe).

| run | held-out (100 never-seen probes) | goals | LLM calls |
|---|---|---|---|
| v1-grid | 15% | 1/5 | 87 |
| v2-directed-grid | 96% | 3/5 | 98 |
| v2-mixed-grid | 87% | 3/5 | 44 |
| v1-knob | 69% | 5/5 | 52 |
| v2-directed-knob | 51% | 5/5 | 52 |
| v2-directed-knob-seed1 | 45% | 5/5 | 48 |
| v2-mixed-knob | 100% | 5/5 | 40 |

v1 folders have v1's layout (no exam, no offers). The analysis: docs/helix_probe_explainer_v2.html, section 8.
