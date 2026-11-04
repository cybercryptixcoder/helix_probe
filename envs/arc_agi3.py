"""ARC-AGI-3 games as a box (ARC Prize Foundation, 2026). One game per box; levels are its goals.

    python -m probe.run envs/arc_agi3.py --env-arg game=ls20-9607627b

Played as ARC Prize requires: only RESET and the game's own actions, every action counted (resets included), local
mode of the official toolkit (`arc-agi`), scored by the toolkit's own score calculator against the human action
counts. Needs Python 3.12+, `pip install arc-agi`, and ARC_API_KEY (the toolkit downloads the games once).

Two modes:
    stateful (default)  the game keeps running; an experiment is a few actions from where the game is now
    reset               every experiment restarts the game first (for engines without stateful boxes)

What the model sees and predicts:
    probe        {"level": n, "frame": [64 strings of 64 hex digits], "history": [actions since the level
                  started], "actions": [the actions to take]}
    observation  {"steps": [{"changes": {"row,col": "c", ...}, "levels": n, "state": "..."}]}: per action,
                  the cells that changed, the levels completed so far, and the game state
                  (NOT_FINISHED / WIN / GAME_OVER)
Actions are "ACTION1" ... "ACTION5", "ACTION7", "RESET", and "CLICK x y" (x = column, y = row, 0-63).
"""
import json
import os
import random
from pathlib import Path

from probe.env import Environment, Task

HEX = "0123456789abcdef"


def frame_rows(fr):
    return ["".join(HEX[int(v) & 15] for v in row) for row in fr]


def diff(a, b):
    """Cells that differ between two frames given as row strings: {"r,c": colour}."""
    out = {}
    for r, (ra, rb) in enumerate(zip(a, b)):
        if ra != rb:
            for c, (x, y) in enumerate(zip(ra, rb)):
                if x != y:
                    out[f"{r},{c}"] = y
    return out


def objects(rows, limit=40):
    """Centres of connected same-colour regions that aren't the most common colour (click targets)."""
    h, w = len(rows), len(rows[0])
    counts = {}
    for row in rows:
        for ch in row:
            counts[ch] = counts.get(ch, 0) + 1
    background = max(counts, key=counts.get)
    seen, out = set(), []
    for r in range(h):
        for c in range(w):
            if (r, c) in seen or rows[r][c] == background:
                continue
            stack, cells, col = [(r, c)], [], rows[r][c]
            seen.add((r, c))
            while stack:
                y, x = stack.pop()
                cells.append((y, x))
                for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < h and 0 <= nx < w and (ny, nx) not in seen and rows[ny][nx] == col:
                        seen.add((ny, nx))
                        stack.append((ny, nx))
            cy = sorted(p[0] for p in cells)[len(cells) // 2]
            cx = sorted(p[1] for p in cells)[len(cells) // 2]
            out.append((len(cells), cx, cy))
    out.sort(reverse=True)
    return [(x, y) for _, x, y in out[:limit]]


class ArcAgi3(Environment):
    tolerance = 0
    stateful = True

    def __init__(self, game="ls20-9607627b", mode="stateful", max_actions="8"):
        from arc_agi import Arcade
        from arcengine import GameAction, GameState
        self.GA, self.GS = GameAction, GameState
        self.game, self.mode, self.max_actions = game, mode, int(max_actions)
        self.stateful = mode == "stateful"
        self.name = f"arc_{game.split('-')[0]}"
        self.arcade = Arcade(arc_api_key=os.environ.get("ARC_API_KEY", ""),
                             environments_dir=str(Path(__file__).resolve().parent.parent / "bench" / "arc" / "games"))
        info = {e.game_id: e for e in self.arcade.get_environments()}[game]
        self.baseline = list(info.baseline_actions)
        self.env = self.arcade.make(game)
        self._fresh()
        self.actions_used = 0            # every action sent to the game, resets included
        self.level_actions = [0] * len(self.baseline)
        self.brief = f"""A video game on a 64x64 grid of coloured cells (colours are hex digits 0-f). Nobody has told \
you the rules or the goal. The game has {self.win_levels} levels; you advance by completing the current level. \
The actions you can send: {", ".join(self.action_names())}. RESET restarts the current level; when the state is GAME_OVER, only RESET works. You see the screen \
after every action. Every action counts against your budget, so be economical: find out what the actions do, \
work out what completes a level, then complete it in as few actions as you can."""
        self.probe_format = f"""probe:       {{"actions": ["ACTION1", "CLICK 12 30", ...]}}   (1 to {self.max_actions} actions, run in order from the current screen)
             (the model's predict() also receives "level", "frame" (the current screen as 64 strings of 64 hex
             digits, row 0 first) and "history" (every action since the level began))
observation: {{"steps": [{{"changes": {{"row,col": new colour as a hex digit, ...}}, "levels": levels completed, "state": "NOT_FINISHED" or "WIN" or "GAME_OVER"}}, ...]}}
             (one step per action; "changes" lists only the cells that changed)"""

    # ------------------------------------------------------------------ game plumbing
    def _fresh(self):
        o = self.env.reset()
        self._read(o)
        self.level_start = self.frame
        self.history = []

    def _read(self, o):
        if o.frame:                      # the toolkit sends no frame for an action it ignores: the screen stays
            self.frame = frame_rows(o.frame[-1])
        self.levels = int(o.levels_completed)
        self.win_levels = int(o.win_levels)
        self.state = o.state.name
        self.available = list(o.available_actions)

    def action_names(self):
        names = [f"ACTION{a}" for a in self.available if a not in (6, 0)]
        if 6 in self.available:
            names.append("CLICK x y")
        return names + ["RESET"]

    def _send(self, a):
        if a == "RESET":
            return self.env.reset()
        if a.startswith("CLICK"):
            _, x, y = a.split()
            return self.env.step(self.GA.ACTION6, data={"x": int(x), "y": int(y)})
        return self.env.step(getattr(self.GA, a))

    # ------------------------------------------------------------------ the box
    def validate(self, p):
        acts = p.get("actions")
        if not (isinstance(acts, list) and 1 <= len(acts) <= self.max_actions):
            return f"actions must be a list of 1 to {self.max_actions} actions"
        ok = set(self.action_names()) - {"CLICK x y"}
        for a in acts:
            if not isinstance(a, str):
                return "each action is a string"
            if a.startswith("CLICK"):
                parts = a.split()
                if 6 not in self.available or len(parts) != 3 or not all(v.isdigit() and int(v) < 64 for v in parts[1:]):
                    return f"bad click {a!r}: use 'CLICK x y' with 0 <= x, y < 64" if 6 in self.available else "this game has no CLICK"
            elif a not in ok:
                return f"unknown action {a!r}; allowed: {', '.join(self.action_names())}"
        if self.state == "GAME_OVER" and acts and acts[0] != "RESET":
            return "the game is over (GAME_OVER): the first action must be RESET"
        if self.state == "WIN":
            return "the game is already won"
        return None

    def full_probe(self, p):
        """What predict() receives: the probe plus where the game is now."""
        return {"level": self.levels, "frame": list(self.frame), "history": list(self.history), "actions": list(p["actions"])}

    def probe(self, p):
        if not self.stateful:
            self._fresh()
        steps = []
        for a in p["actions"]:
            before, level_before = self.frame, self.levels
            if self.state == "GAME_OVER" and a != "RESET":     # only RESET works now; nothing is sent or counted
                steps.append({"changes": {}, "levels": self.levels, "state": self.state, "error": "GAME_OVER: only RESET works"})
                break
            o = self._send(a)
            self.actions_used += 1
            self.level_actions[min(level_before, len(self.level_actions) - 1)] += 1
            if o is None:
                steps.append({"changes": {}, "levels": self.levels, "state": self.state, "error": "the game refused"})
                continue
            self._read(o)
            steps.append({"changes": diff(before, self.frame), "levels": self.levels, "state": self.state})
            if a == "RESET" or self.levels != level_before:
                self.history = []
                self.level_start = self.frame
            else:
                self.history.append(a)
            if self.state in ("WIN", "GAME_OVER"):
                break
        return {"steps": steps}

    def cost(self, p, obs):
        """Actions sent to the game (an action refused because the game is over isn't sent)."""
        return sum(1 for st in obs.get("steps", []) if not str(st.get("error", "")).startswith("GAME_OVER"))

    def compare(self, pred, obs):
        """Per action: changed cells (overlap of the two change sets), levels and state; averaged over actions."""
        steps = obs.get("steps", [])
        ps = pred.get("steps") if isinstance(pred, dict) else None
        if not isinstance(ps, list) or not steps:
            return 0.0
        total = 0.0
        for i, s in enumerate(steps):
            q = ps[i] if i < len(ps) and isinstance(ps[i], dict) else {}
            raw = q.get("changes") if isinstance(q.get("changes"), dict) else {}
            a = {str(k).replace(" ", ""): (HEX[v & 15] if isinstance(v, int) else str(v).lower()[:1]) for k, v in raw.items()}
            b = s["changes"]
            inter = sum(1 for k, v in b.items() if a.get(k) == v)
            union = len(set(a) | set(b))
            cells = 1.0 if union == 0 else inter / union
            total += (2 * cells + (q.get("levels") == s["levels"]) + (q.get("state") == s["state"])) / 4
        return total / len(steps)

    def random_probe(self, rng):
        names = [n for n in self.action_names() if n not in ("RESET", "CLICK x y")]
        clicks = [f"CLICK {x} {y}" for x, y in objects(self.frame, 20)] if 6 in self.available else []
        pool = names + clicks or ["RESET"]
        acts = [rng.choice(pool) for _ in range(rng.randint(1, min(4, self.max_actions)))]
        return {"actions": (["RESET"] + acts)[:self.max_actions] if self.state == "GAME_OVER" else acts}

    # ------------------------------------------------------------------ for stateful engines
    def view_state(self):
        return (f"Level {self.levels + 1} of {self.win_levels} (levels completed: {self.levels}); game state "
                f"{self.state}; {len(self.history)} actions since this level began; actions used so far "
                f"{self.actions_used}.\nThe screen now (row 0 first; each character is one cell's colour):\n"
                + "\n".join(self.frame)
                + (f"\nObjects you could click (x y): {', '.join(f'{x} {y}' for x, y in objects(self.frame, 25))}"
                   if 6 in self.available else ""))

    def view_probe(self, p):
        return json.dumps({"level": p.get("level"), "after": len(p.get("history", [])), "actions": p.get("actions")})

    def view_obs(self, o):
        """Changes grouped into runs: 'r45 c34-38:3' = row 45, columns 34 to 38 became colour 3."""
        out = []
        for s in o.get("steps", []):
            cells = sorted((tuple(map(int, k.split(","))), v) for k, v in s["changes"].items())
            runs, i = [], 0
            while i < len(cells):
                (r, c), v = cells[i]
                j = i
                while j + 1 < len(cells) and cells[j + 1][0] == (r, cells[j][0][1] + 1) and cells[j + 1][1] == v:
                    j += 1
                c2 = cells[j][0][1]
                runs.append(f"r{r} c{c}{'-' + str(c2) if c2 != c else ''}:{v}")
                i = j + 1
            text = ", ".join(runs[:40]) + (f" ...(+{len(runs) - 40} more runs)" if len(runs) > 40 else "")
            out.append(f"[{len(cells)} cells changed{': ' + text if runs else ''}; levels {s['levels']}; {s['state']}]")
        return " ".join(out)

    def goal(self):
        if self.state == "WIN" or self.levels >= self.win_levels:
            return None
        k = self.levels
        return Task(f"Complete level {k + 1}: an observation step shows levels completed = {k + 1} or more.",
                    lambda obs, k=k: any(s.get("levels", 0) > k for s in obs.get("steps", [])))

    def done(self):
        return self.state == "WIN"

    @property
    def max_probe(self):
        return self.max_actions

    def plan_actions(self):
        if self.state == "GAME_OVER":    # only RESET works: leave the choice to the experimenter
            return []
        names = [n for n in self.action_names() if n not in ("RESET", "CLICK x y")]
        clicks = [f"CLICK {x} {y}" for x, y in objects(self.frame, 12)] if 6 in self.available else []
        return names + clicks

    def advance(self, fp, a, pred):
        """The screen the model predicts after one action: its predicted changes applied to the frame."""
        steps = pred.get("steps") if isinstance(pred, dict) else None
        if not steps or not isinstance(steps[-1], dict):
            return None
        st = steps[-1]
        if st.get("state") == "GAME_OVER":
            return None
        rows = [list(r) for r in fp["frame"]]
        for k, v in (st.get("changes") or {}).items():
            try:
                r, c = map(int, str(k).split(","))
                rows[r][c] = HEX[v & 15] if isinstance(v, int) else str(v).lower()[:1]
            except Exception:
                return None
        level = st.get("levels", fp["level"])
        return {"level": level, "frame": ["".join(r) for r in rows],
                "history": [] if level != fp["level"] else fp["history"] + [a], "actions": []}

    def state_key(self, fp):
        return (fp["level"], "".join(fp["frame"]))

    def restore(self, entries):
        """Bring the game back to where a run stopped by replaying every action from the start (games are
        deterministic). Replayed actions are not counted again: the counts are restored from the log."""
        self._fresh()
        self.actions_used, self.level_actions = 0, [0] * len(self.baseline)
        for e in entries:
            for a in e["probe"]["actions"]:
                before = self.levels
                if self.state == "GAME_OVER" and a != "RESET":    # as in probe(): refused, never sent
                    break
                o = self._send(a)
                self.actions_used += 1
                self.level_actions[min(before, len(self.level_actions) - 1)] += 1
                if o is None:
                    continue
                self._read(o)
                if a == "RESET" or self.levels != before:
                    self.history, self.level_start = [], self.frame
                else:
                    self.history.append(a)
                if self.state in ("WIN", "GAME_OVER"):
                    break

    def score(self):
        """The official per-game score (the toolkit's own calculator) from the actions used per level."""
        from arc_agi.scorecard import EnvironmentScoreCalculator
        calc = EnvironmentScoreCalculator(id=self.game)
        for i, base in enumerate(self.baseline):
            calc.add_level(i + 1, i < self.levels, self.level_actions[i], base, game_id=self.game)
        s = calc.to_score()
        return {"game": self.game, "score": s.score, "levels_completed": self.levels, "levels": self.win_levels,
                "actions": self.actions_used, "level_actions": self.level_actions, "baseline": self.baseline}
