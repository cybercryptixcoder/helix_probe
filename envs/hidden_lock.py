"""A small box with state and hidden state: a lock with two buttons, a lamp and a door.

The example of a stateful box (and the test fixture for one). Hidden rules:
    the lock counts presses of A since the last reset (the count is never shown)
    B opens the door if the count is exactly 3, otherwise it does nothing
    the lamp is on when the count is 2 or more
Goal: open the door. Same screen + same action can give different results (A with the lamp off), so a model of
the screen alone can't be right: it has to replay the history.
"""
from probe.env import Environment, Task


class HiddenLock(Environment):
    name = "hidden_lock"
    stateful = True
    brief = """A lock with two buttons, A and B, a lamp and a door. You can press buttons, or RESET to start over. \
Nobody has told you how it works. Every press counts against your budget. The goal is to open the door."""
    probe_format = """probe:       {"actions": ["A", "B", "RESET", ...]}   (1 to 4 actions, from where the lock is now)
             (the model's predict() also receives "lamp", "door" and "history": every action since the last RESET)
observation: {"steps": [{"lamp": "on" or "off", "door": "open" or "closed"}, ...]}   (one per action)"""

    def __init__(self):
        self.count, self.door = 0, "closed"
        self.history = []

    def lamp(self):
        return "on" if self.count >= 2 else "off"

    def validate(self, p):
        a = p.get("actions")
        if not (isinstance(a, list) and 1 <= len(a) <= 4 and all(x in ("A", "B", "RESET") for x in a)):
            return 'actions: 1 to 4 of "A", "B", "RESET"'
        return None

    def full_probe(self, p):
        return {"lamp": self.lamp(), "door": self.door, "history": list(self.history), "actions": list(p["actions"])}

    def _do(self, a):
        if a == "RESET":
            self.count, self.door, self.history = 0, "closed", []
            return
        self.history.append(a)
        if a == "A":
            self.count += 1
        elif a == "B" and self.count == 3:
            self.door = "open"

    def probe(self, p):
        steps = []
        for a in p["actions"]:
            self._do(a)
            steps.append({"lamp": self.lamp(), "door": self.door})
        return {"steps": steps}

    def cost(self, p, obs):
        return len(p["actions"])

    def view_state(self):
        return f"The lamp is {self.lamp()} and the door is {self.door}."

    def random_probe(self, rng):
        return {"actions": [rng.choice("AAB") for _ in range(rng.randint(2, 4))]}

    def restore(self, entries):
        self.__init__()
        for e in entries:
            for a in e["probe"]["actions"]:
                self._do(a)

    def goal(self):
        return None if self.door == "open" else Task("Open the door.", lambda o: any(s["door"] == "open" for s in o["steps"]))

    def done(self):
        return self.door == "open"

    max_probe = 4

    def plan_actions(self):
        return ["A", "B", "RESET"]

    def advance(self, fp, a, pred):
        st = pred["steps"][-1]
        history = [] if a == "RESET" else fp["history"] + [a]
        return {"lamp": st.get("lamp"), "door": st.get("door"), "history": history, "actions": []}
