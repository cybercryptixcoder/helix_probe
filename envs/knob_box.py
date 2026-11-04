"""An instrument with three unlabeled dials and a switch, and a dot on a screen.

Hidden rules (don't show these to the experimenter):
    x    = 2a - b, held between -10 and 10
    y    = c with the switch off, 10 - c with it on; one higher when a is above 7
    size = 1 + |a - c| / 2
all rounded to 2 decimals. Goals: put the dot at a given (x, y).
"""
from probe.env import Environment, Task


def clamp(v, lo, hi):
    return max(lo, min(hi, v))


class KnobBox(Environment):
    name = "knob_box"
    brief = """An instrument with three dials, a, b and c, each settable anywhere from 0 to 10, and a switch that \
is "on" or "off". A screen shows one dot, with a position (x, y) and a size. Nobody has told you how the controls \
move the dot. In one experiment you set all four controls and read the screen. The instrument is deterministic; the \
readings are rounded to 2 decimals."""
    probe_format = """probe:       {"a": 3.5, "b": 0, "c": 10, "switch": "off"}
observation: {"x": ..., "y": ..., "size": ...}"""
    knowledge = "From the manual: the switch mirrors something."
    tolerance = 0.011  # readings are rounded

    def validate(self, p):
        for k in "abc":
            if not isinstance(p.get(k), (int, float)) or isinstance(p.get(k), bool) or not 0 <= p[k] <= 10:
                return f"dial {k} must be a number from 0 to 10"
        if p.get("switch") not in ("on", "off"):
            return 'switch must be "on" or "off"'
        return None

    def probe(self, p):
        a, b, c, on = p["a"], p["b"], p["c"], p["switch"] == "on"
        y = (10 - c if on else c) + (1 if a > 7 else 0)
        return {"x": round(clamp(2 * a - b, -10, 10), 2), "y": round(y, 2), "size": round(1 + abs(a - c) / 2, 2)}

    def random_probe(self, rng):
        return {k: round(rng.uniform(0, 10), 1) for k in "abc"} | {"switch": rng.choice(["on", "off"])}

    def make_tasks(self, rng, n):
        tasks = []
        for _ in range(n):
            t = self.probe(self.random_probe(rng))
            tasks.append(Task(f"Put the dot at x = {t['x']}, y = {t['y']} (within 0.1 on each; size doesn't matter).",
                              lambda o, t=t: abs(o["x"] - t["x"]) <= 0.1 and abs(o["y"] - t["y"]) <= 0.1))
        return tasks
