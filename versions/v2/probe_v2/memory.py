"""What persists between calls. Everything else (reasoning, conversations) is thrown away.

1. Notebook - every experiment the experimenter ran: question, probe, observation, what the model of the time
              predicted, and the match. Append-only. The evidence; it is ground truth.
2. Exam     - a few probes drawn at random from the box at the start, run, and sealed: no LLM call ever sees their
              results. They exist only to score models on evidence the models were never fitted to.
3. Model    - one artifact: predict(probe) in Python, with the beliefs as comments inside it. Every accepted version
              is kept (model/v###.py + .json with its scores), so the history of the model is version-controlled.
4. Library  - knowledge handed in from outside. Read-only.
"""
from __future__ import annotations

import ast
import json
from pathlib import Path

EMPTY_MODEL = '''def predict(probe):
    # No model yet: predicts nothing.
    return {}
'''


class Notebook:
    def __init__(self, folder: Path):
        self.path = folder / "notebook.jsonl"
        self.entries: list[dict] = []
        if self.path.exists():
            for line in self.path.read_text().splitlines():
                try:
                    self.entries.append(json.loads(line))
                except json.JSONDecodeError:      # a line torn by a kill: drop it, the step is redone
                    break
            self.path.write_text("".join(json.dumps(e) + "\n" for e in self.entries))

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


def code_size(code: str) -> int:
    """Characters of executable code: comments and docstrings don't count, so explaining is free."""
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return 10 ** 9
    for node in ast.walk(tree):
        body = getattr(node, "body", None)
        if isinstance(body, list) and body and isinstance(body[0], ast.Expr) \
                and isinstance(getattr(body[0], "value", None), ast.Constant) and isinstance(body[0].value.value, str):
            node.body = body[1:] or [ast.Pass()]
    return len(ast.unparse(tree))


class Model:
    FIELDS = ("version", "role", "notes", "exam", "fit", "fit_exact", "size", "matches", "made_at", "heldout")

    def __init__(self, folder: Path):
        self.dir = folder / "model"
        self.dir.mkdir(exist_ok=True)
        versions = sorted(self.dir.glob("v*.json"))
        if versions:
            self.__dict__.update(json.loads(versions[-1].read_text()))
            self.code = (self.dir / f"v{self.version:03d}.py").read_text()
        else:
            self.version, self.role, self.notes, self.code = 0, "start", "empty model", EMPTY_MODEL
            self.exam = self.fit = self.fit_exact = 0.0
            self.size, self.matches, self.made_at, self.heldout = code_size(EMPTY_MODEL), [], 0, None
            self.save()

    def save(self):
        (self.dir / f"v{self.version:03d}.py").write_text(self.code)
        tmp = self.dir / f"v{self.version:03d}.json.tmp"
        tmp.write_text(json.dumps({k: getattr(self, k) for k in self.FIELDS}))
        tmp.replace(self.dir / f"v{self.version:03d}.json")

    def replace(self, code, role, notes, scores, made_at, heldout):
        self.version += 1
        self.code, self.role, self.notes, self.made_at, self.heldout = code, role, notes, made_at, heldout
        for k in ("exam", "fit", "fit_exact", "size", "matches"):
            setattr(self, k, scores[k])
        self.save()


class Library:
    def __init__(self, env_knowledge: str = "", files=()):
        parts = [env_knowledge.strip()] if env_knowledge and env_knowledge.strip() else []
        for f in files:
            parts.append(f"## From {Path(f).name}\n" + Path(f).read_text().strip())
        self.text = "\n\n".join(parts)
