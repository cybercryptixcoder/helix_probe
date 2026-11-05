"""MIT's Experiment 1, replicated exactly with any model: name the game a policy network was trained on, from its
weights as text, in one reply, with no tools (Takehi, Teoh, Zhang & Khattab, "Sparks of Weight-Space Programming",
MIT CSAIL, Nov 2026; logs, networks and prompts: github.com/RikiyaT/lm_understand-logs, CC BY 4.0).

- **The prompt:** each network's `runs/<game>/prompt.txt` from the logs, byte for byte, with their one-line system
  instructions ("Answer the user's request."). That is the description, the open question (no list of games) and all
  17,253 weights at 3 decimals.
- **Scoring:** the `Game:` line is mapped to a game by keywords, as theirs is (Frogger counts as Freeway). The answer
  key is read only here.
- **Control (as in the Alan Turing Institute replication):** `--shuffle` randomly reorders the values inside each
  weight matrix and bias vector. A model that reads the weights should fall to chance (1 in 4).

    bash bench/weights/fetch_mit.sh                  # once: the logs repo into bench/weights/mit (gitignored)
    python bench/weights/text_oneshot.py --out runs/weights/text1 --effort none --reps 3
    python bench/weights/text_oneshot.py --out runs/weights/text1-shuf --effort none --reps 3 --shuffle
"""
from __future__ import annotations

import argparse
import json
import random
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from probe.llm import LLM  # noqa: E402

MIT = ROOT / "bench" / "weights" / "mit" / "exp1_which_game"
GAMES = {"breakout": ("breakout", "brick"), "pong": ("pong",), "pacman": ("pac-man", "pacman", "pac man"),
         "freeway": ("freeway", "frogger", "road-crossing", "road crossing", "crossy")}
SYSTEM = "Answer the user's request."


def shuffle_weights(prompt: str, rng: random.Random) -> str:
    """Reorder the values inside each matrix/vector block of the weights section, keeping the layout."""
    head, sep, weights = prompt.partition("THE NETWORK'S WEIGHTS\n")
    out, block = [], []

    def flush():
        vals = [v for line in block for v in line.split()]
        rng.shuffle(vals)
        it = iter(vals)
        for line in block:
            out.append(" ".join(next(it) for _ in line.split()))
        block.clear()

    for line in weights.split("\n"):
        if re.fullmatch(r"[-0-9. ]+", line.strip() or "x"):
            block.append(line)
        else:
            flush()
            out.append(line)
    flush()
    return head + sep + "\n".join(out)


def grade(answer: str):
    m = re.search(r"^\W*Game\W*?[:：]\s*(\S.*)$", answer, re.I | re.M) or \
        re.search(r"^#+\s*Game\s*\n+\s*(\S.*)$", answer, re.I | re.M)       # "Game: X" or a "## Game" heading
    line = (m.group(1) if m else "").lower()
    for game, keys in GAMES.items():
        if any(k in line for k in keys):
            return game, line
    return None, line


def one(llm, net_id, game, rep, args):
    folder = Path(args.out) / f"{game}_r{rep}"
    if (folder / "result.json").exists():
        return json.loads((folder / "result.json").read_text())
    folder.mkdir(parents=True, exist_ok=True)
    prompt = (MIT / "runs" / game / "prompt.txt").read_text()
    if args.shuffle:
        prompt = shuffle_weights(prompt, random.Random(f"{net_id}-{rep}"))
    (folder / "prompt.txt").write_text(prompt)
    t0 = time.time()
    r = llm(SYSTEM, prompt, effort=args.effort, max_tokens=args.max_tokens)
    guess, line = grade(r["text"])
    res = {"network": net_id, "true": game, "rep": rep, "guess": guess, "answer_line": line,
           "correct": guess == game, "shuffled": args.shuffle, "effort": args.effort,
           "usage": r.get("usage"), "seconds": round(time.time() - t0, 1), "finish": r.get("finish")}
    (folder / "answer.md").write_text(r["text"])
    (folder / "reasoning.md").write_text(r.get("reasoning") or "")
    (folder / "result.json").write_text(json.dumps(res, indent=1))
    print(time.strftime("%H:%M:%S"), f"{game} r{rep}: guessed {guess} ({line[:60]!r})", flush=True)
    return res


def main():
    a = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    a.add_argument("--out", required=True)
    a.add_argument("--effort", default="none")
    a.add_argument("--reps", type=int, default=3)
    a.add_argument("--shuffle", action="store_true")
    a.add_argument("--max-tokens", type=int, default=8000)
    a.add_argument("--workers", type=int, default=4)
    args = a.parse_args()
    key = json.loads((MIT / "eval" / "answer_key.json").read_text())
    jobs = [(nid, v["game"], rep) for nid, v in key.items() for rep in range(args.reps)]
    Path(args.out).mkdir(parents=True, exist_ok=True)
    (Path(args.out) / "job.json").write_text(json.dumps(vars(args), indent=1))
    llm = LLM()
    with ThreadPoolExecutor(args.workers) as pool:
        res = list(pool.map(lambda j: one(llm, *j, args), jobs))
    n, c = len(res), sum(r["correct"] for r in res)
    summary = {"n": n, "correct": c, "rate": c / n, "chance": 0.25, "shuffled": args.shuffle, "effort": args.effort,
               "by_game": {g: [r["guess"] for r in res if r["true"] == g] for g in GAMES}}
    (Path(args.out) / "summary.json").write_text(json.dumps(summary, indent=1))
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
