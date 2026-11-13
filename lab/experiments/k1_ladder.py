"""K1 hint-ladder experiment: does the reader fail at READING the weights, or at NAMING the task?
Rungs: L0 no hints; L1 input layout only (grid shape and flattening order, no channel meanings); L2 full context.
Each rung in text mode and in python mode (no forward passes), plus shuffled controls. Saves runs to lab/runs/.
Run: python3 lab/experiments/k1_ladder.py
"""
import json, sys, threading, queue, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import server

ASK = ("What was this network trained to do? Explain your evidence, then give your answer and a confidence (0-100%).")
TEXT = "Below are the weights of a trained neural network. Work only from the weights. " + ASK
PY = ("You have a Python tool with the weights of a trained neural network loaded as W. You cannot run the network. "
      "Use Python to analyse the weights. " + ASK)
LAYOUT = ("Input layout (the meanings of the channels are NOT given): the 500 inputs are a 10x10 grid with 5 binary channels per cell, "
          "flattened as input i = (row*10 + column)*5 + channel. The network outputs 5 numbers.")
ALL = [{"tensor": t} for t in ["W1", "b1", "W2", "b2", "W3", "b3"]]


def job(target, rung, mode, variant="original", decimals=3):
    p = TEXT if mode == "text" else PY
    if rung == "L1":
        p = LAYOUT + "\n\n" + p
    if rung == "L2":
        p = "{{context}}\n\n" + p
    return {"target": target, "variant": variant, "mode": "sandbox" if mode == "py" else "text", "allow_forward": False,
            "selection": ALL if mode == "text" else [], "prompt": p, "system": "Answer the user's request.",
            "include_arch": True, "include_context": rung == "L2", "effort": "high",
            "max_tokens": 64000 if mode == "text" else 32000, "max_steps": 15, "format": {"decimals": decimals, "headers": "name"},
            "title": f"K1 ladder · {target} · {rung} · {mode} · {variant}" + (f" · {decimals}dp" if decimals != 3 else "")}


jobs = []
for g in ["sparks_game_a9f535cc", "sparks_game_dfc6cb65"]:          # Breakout, Pong
    jobs += [job(g, "L0", "py"), job(g, "L1", "py"), job(g, "L2", "py"), job(g, "L1", "py", "shuffled"),
             job(g, "L1", "text", decimals=2), job(g, "L0", "text", decimals=2)]
modadd = {"target": "modadd_p113", "variant": "original", "mode": "sandbox", "allow_forward": False, "selection": [],
          "prompt": "{{arch}}\n\nYou have a Python tool with this network's weights loaded as W. You cannot run the network. "
                    "Reverse-engineer it from the weights: what function of the inputs does it compute, and by what algorithm? "
                    "State the algorithm concretely, with the specific constants you measured.",
          "system": "Answer the user's request.", "include_arch": True, "include_context": False, "effort": "high",
          "max_tokens": 32000, "max_steps": 20, "title": "K1 ladder · modadd · L0+arch · py"}
jobs += [modadd, {**modadd, "variant": "shuffled", "title": "K1 ladder · modadd · L0+arch · py · shuffled"}]

q, out = queue.Queue(), []
for j in jobs:
    q.put(j)


def worker():
    while True:
        try:
            j = q.get_nowait()
        except queue.Empty:
            return
        ev = {}
        server.stream_run(j, lambda e: ev.update({"id": e["id"]}) if e["type"] in ("start", "done") else None)
        out.append({"title": j["title"], "id": ev.get("id")})
        print("done:", j["title"], ev.get("id"), flush=True)


ts = [threading.Thread(target=worker) for _ in range(7)]
[t.start() for t in ts]; [t.join() for t in ts]
Path(__file__).with_name("k1_ladder_runs.json").write_text(json.dumps(out, indent=1))
