"""The three things the experimenter keeps. Everything else (its reasoning, its conversations) is thrown away.

1. Notebook  - every experiment ever run: what it asked, the probe, what came back, what the model predicted and how
               well. Append-only. This is "what was tried".
2. Model     - what the experimenter believes about the box, in two forms that are kept together:
                 beliefs   short claims in plain words, each citing the experiments behind it
                 predict() Python code: the beliefs made executable, a simulator of the box
               Because the model is code, how good it is gets measured, not asserted: it is replayed on every
               experiment in the notebook (fit) and on probes it has never seen (held-out).
               A new version replaces the old one only if it fits the notebook at least as well.
3. Library   - knowledge handed in from outside (rules, domain facts, tricks). Read-only.

The notebook does not need to be shown in full: the experiments the model already predicts are, in effect,
compressed into it. What the experimenter sees in detail are the ones the model still gets wrong.
"""
from __future__ import annotations

import json
from pathlib import Path

EMPTY_MODEL = '''def predict(probe):
    """No model yet: predicts nothing."""
    return {}
'''


class Notebook:
    def __init__(self, folder: Path):
        self.path = folder / "notebook.jsonl"
        self.entries: list[dict] = []
        if self.path.exists():
            self.entries = [json.loads(l) for l in self.path.read_text().splitlines() if l.strip()]

    def add(self, entry: dict) -> dict:
        entry = {"id": f"E{len(self.entries) + 1}", **entry}
        self.entries.append(entry)
        with self.path.open("a") as f:
            f.write(json.dumps(entry) + "\n")
        return entry

    def probes(self):
        return [e["probe"] for e in self.entries]

    def __len__(self):
        return len(self.entries)


class Model:
    """The current model plus every past version in model/v###.py and model/v###.json."""

    def __init__(self, folder: Path):
        self.dir = folder / "model"
        self.dir.mkdir(exist_ok=True)
        versions = sorted(self.dir.glob("v*.json"))
        if versions:
            meta = json.loads(versions[-1].read_text())
            self.__dict__.update(meta)
            self.code = (self.dir / f"v{self.version:03d}.py").read_text()
        else:
            self.version, self.beliefs, self.code, self.notes = 0, [], EMPTY_MODEL, "empty model"
            self.fit, self.heldout, self.matches, self.made_at = 0.0, None, [], 0
            self.save()

    def meta(self):
        return {k: getattr(self, k) for k in ("version", "beliefs", "notes", "fit", "heldout", "matches", "made_at")}

    def save(self):
        (self.dir / f"v{self.version:03d}.py").write_text(self.code)
        (self.dir / f"v{self.version:03d}.json").write_text(json.dumps(self.meta(), indent=1))

    def replace(self, beliefs, code, notes, fit, matches, heldout, made_at):
        self.version += 1
        self.beliefs, self.code, self.notes = beliefs, code, notes
        self.fit, self.matches, self.heldout, self.made_at = fit, matches, heldout, made_at
        self.save()


class Library:
    def __init__(self, env_knowledge: str = "", files=()):
        parts = [env_knowledge.strip()] if env_knowledge.strip() else []
        for f in files:
            parts.append(f"## From {Path(f).name}\n" + Path(f).read_text().strip())
        self.text = "\n\n".join(parts)
