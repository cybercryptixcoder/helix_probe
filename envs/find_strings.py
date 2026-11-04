"""FIND string functions (Schwettmann, Rott Shaham et al., NeurIPS 2023) as a box: f(s) on strings.

    python -m probe.run envs/find_strings.py --env-arg fid=f00012

The experimenter is told what FIND's own agents were told (FIND's strings prompt), nothing more. A probe evaluates
f on up to 10 strings, like FIND's PYTHON(function.py s1 s2 ...) command.
"""
import importlib.util
import json
from pathlib import Path

from probe.env import Environment

DATA = Path(__file__).resolve().parent.parent / "bench" / "find" / "data" / "strings"

BRIEF = """A function f(x) that takes string inputs and returns a string. Nobody has told you what it computes. In \
one experiment you call f on up to 10 input strings at once and read back the outputs. f(x) may combine multiple \
different operations. Test a large range of inputs: words, sentences, spaces, digits, symbols, upper and lower \
case."""

WORDS = ["hello", "world", "apple", "Python", "lazy", "the quick brown fox", "Zebra", "data", "Example", "level",
         "banana", "OpenAI", "test case", "abc", "xyz", "Mississippi", "racecar", "Hello World", "a", "function"]
EXTRA = ["123", "42", "!@#", "", " ", "  padded  ", "MiXeD", "UPPER", "lower", "x1y2", "end.", "tab\tsep"]


def load_function(fid, data=None):
    d = (Path(data) / "strings" if data else DATA) / fid
    spec = importlib.util.spec_from_file_location(f"find_s_{fid}", d / "function_code.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.function


class FindStrings(Environment):
    probe_format = """probe:       {"inputs": ["hello", "two words", "A1!"]}   (1 to 10 strings, each at most 60 characters)
observation: {"outputs": [f("hello"), f("two words"), f("A1!")]}   (in the same order)"""

    def __init__(self, fid="f00000", data=None):
        self.fid = fid
        self.f = load_function(fid, data)
        self.name = f"find_strings_{fid}"
        self.brief = BRIEF

    def validate(self, p):
        xs = p.get("inputs")
        if not (isinstance(xs, list) and 1 <= len(xs) <= 10 and all(isinstance(s, str) and len(s) <= 60 for s in xs)):
            return "inputs must be a list of 1 to 10 strings, each at most 60 characters"
        return None

    def probe(self, p):
        out = []
        for s in p["inputs"]:
            try:
                out.append(str(self.f(str(s))))
            except Exception as e:
                out.append(f"ERROR: {type(e).__name__}")
        return {"outputs": out}

    def compare(self, pred, obs):
        ys = obs.get("outputs", [])
        ps = pred.get("outputs") if isinstance(pred, dict) else None
        if not isinstance(ps, list) or len(ps) != len(ys):
            return 0.0
        return sum(p == o for p, o in zip(ps, ys)) / len(ys) if ys else 1.0

    def cost(self, p, obs):
        """FIND's unit of budget: inputs sent to the function."""
        return len(p.get("inputs") or [])

    def random_probe(self, rng):
        def one():
            r = rng.random()
            if r < 0.5:
                s = rng.choice(WORDS)
            elif r < 0.75:
                s = " ".join(rng.choice(WORDS) for _ in range(rng.randint(2, 3)))
            else:
                s = rng.choice(WORDS) + rng.choice(EXTRA)
            if rng.random() < 0.2:
                s = rng.choice([" ", "  "]) + s
            if rng.random() < 0.2:
                s = s + rng.choice([" ", "  "])
            return s[:60]
        return {"inputs": [one() for _ in range(6)]}
