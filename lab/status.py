"""One screen on the constructor runs of a target:  python3 lab/status.py <target> [run id] [--steps]

Without a run id: one line per run. With one: one line per submission (stages verified, what fails), and with
--steps one line per step (what the reader did)."""
import json, sys, time
from pathlib import Path

LAB = Path(__file__).resolve().parent


def line(sub):
    v = sub.get("verdict")
    if not v:
        return "no report (construction error)"
    return f"{v.get('stages_verified', '?')}/{v.get('stages_total', '?')} stages" + (" COMPLETE" if v.get("complete") else "") + \
        (" verified" if v.get("verified") else "") + (" | fails: " + "; ".join(f[:90] for f in v["fails"][:4]) if v.get("fails") else "")


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    tdir = LAB / "constructions" / args[0]
    if len(args) == 1:
        for f in sorted(tdir.glob("*/run.json")):
            r = json.loads(f.read_text())
            c = r["config"]
            best = max((s for s in r["submissions"] if s.get("verdict")), key=lambda s: (s["verdict"].get("complete", False), s["verdict"].get("score", 0)), default=None)
            age = time.time() - r.get("heartbeat", r["started"])
            print(f"{r['id']}  {c.get('title', '')[:28]:28s} {r['status']:8s} steps {len(r['steps']):3d}/{c['max_steps']:<3d} subs {len(r['submissions']):2d} "
                  f"${r.get('cost', 0):.2f}  last write {age / 60:.0f} min ago  best: {line(best) if best else '-'}"[:260])
        return
    r = json.loads((tdir / args[1] / "run.json").read_text())
    if "--steps" in sys.argv:
        for s in r["steps"]:
            for t in s["tools"]:
                first = next((l for l in t["code"].strip().splitlines() if l.strip() and not l.strip().startswith(("import", "#"))), "")[:100]
                print(f"step {s['step'] + 1:3d} {t['tool']:6s} {t.get('seconds', '')!s:>7} s  {first}")
            if not s["tools"]:
                print(f"step {s['step'] + 1:3d} says: {s['content'][:160]!r}")
    for sub in r["submissions"]:
        print(f"submission {sub['n']:2d} (step {sub['step'] + 1}): {line(sub)}")
    print(f"status {r['status']}; best {r.get('best')}; steps {len(r['steps'])}; cost ${r.get('cost', 0):.2f}; notes {len(r.get('notes', []))}; compactions {len(r['compactions'])}")


if __name__ == "__main__":
    main()
