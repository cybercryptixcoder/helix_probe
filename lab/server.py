"""Weight Reading Lab: a local web app for handing a network's weights to an LLM and seeing what it makes of them.

Run:   python3 lab/server.py      then open http://localhost:8765
Needs: Python 3.9+, numpy. Your Luminal key goes in lab/.env (the Keys button writes it there; gitignored).
Everything a run used and produced is saved to lab/runs/<run id>.json.
"""
import json, os, re, subprocess, sys, threading, time, uuid
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse, parse_qs

import numpy as np

LAB = Path(__file__).resolve().parent
sys.path.insert(0, str(LAB))
MODELS, RUNS, STATIC = LAB / "models", LAB / "runs", LAB / "static"
RUNS.mkdir(exist_ok=True)
ENV = LAB / ".env"


def load_env():
    if ENV.exists():
        for line in ENV.read_text().splitlines():
            if "=" in line and not line.lstrip().startswith("#"):
                k, v = line.split("=", 1)
                os.environ[k.strip()] = v.strip()


load_env()
import luminal  # noqa: E402  (reads the key from the environment)
import nets     # noqa: E402

CONTEXT_TOKENS = 163_840
CALIB = LAB / "runs" / ".token_calibration.json"
CANCEL = {}


# ---------------------------------------------------------------- targets
def meta(tid):
    return json.loads((MODELS / tid / "meta.json").read_text())


def public_meta(tid):
    m = meta(tid)
    m.pop("answer", None)
    return m


_wcache = {}


def weights(tid, variant="original", seed=0):
    key = (tid, variant, seed)
    if key not in _wcache:
        W = dict(np.load(MODELS / tid / "weights.npz"))
        _wcache[key] = nets.variant(W, variant, meta(tid).get("perm_groups", []), seed)
    return _wcache[key]


# ---------------------------------------------------------------- formatting weights as text
def fmt_block(a, decimals, row_labels, start_row=0):
    a = np.asarray(a, dtype=np.float64)
    if a.ndim == 1:
        a = a[None]
    lines = []
    for i, row in enumerate(a):
        s = " ".join(f"{x:.{decimals}f}" for x in row).replace(f"-{0:.{decimals}f}", f"{0:.{decimals}f}")
        lines.append(f"[{start_row + i}] {s}" if row_labels else s)
    return "\n".join(lines)


def format_selection(tid, variant, selection, opts):
    """selection: list of {tensor, head?, r0?, r1?, c0?, c1?}. Returns the weights as prompt text."""
    m, W = meta(tid), weights(tid, variant)
    desc = {t["name"]: t["desc"] for t in m["tensors"]}
    d = int(opts.get("decimals", 3))
    labels = bool(opts.get("row_labels", False))
    headers = opts.get("headers", "full")  # full | name | none
    out = []
    for item in selection:
        name = item["tensor"]
        a = W[name]
        heads = [None]
        if a.ndim == 3:
            heads = list(range(a.shape[0])) if item.get("head") in (None, "all") else [int(item["head"])]
        for h in heads:
            b = a[h] if h is not None else a
            if b.ndim == 1:
                b = b[None]
            r0, r1 = item.get("r0") or 0, item.get("r1") or b.shape[0]
            c0, c1 = item.get("c0") or 0, item.get("c1") or b.shape[1]
            part = b[r0:r1, c0:c1]
            label = f"{name}[{h}]" if h is not None else name
            whole = (r0, r1, c0, c1) == (0, b.shape[0], 0, b.shape[1])
            if headers == "full":
                shape = " x ".join(map(str, b.shape)) if a.ndim != 1 else str(a.shape[0])
                rng = "" if whole else f", rows {r0}-{r1 - 1}, columns {c0}-{c1 - 1}"
                extra = f" ({desc[name]})" if desc.get(name) else ""
                out.append(f"{label}{extra}, shape {shape}{rng}" + (": one line per row" if a.ndim > 1 and part.shape[0] > 1 else ":"))
            elif headers == "name":
                out.append(f"{label}:")
            out.append(fmt_block(part if a.ndim != 1 else part[0], d, labels, r0))
            out.append("")
    return "\n".join(out).rstrip() + "\n"


def calib():
    try:
        return json.loads(CALIB.read_text())["tokens_per_char"]
    except Exception:
        return 0.42  # first guess for DeepSeek on numeric text; replaced by real usage after the first run


def build_messages(cfg):
    m = meta(cfg["target"])
    wtext = format_selection(cfg["target"], cfg.get("variant", "original"), cfg.get("selection", []), cfg.get("format", {})) \
        if cfg.get("selection") else ""
    arch = m.get("arch", "") if cfg.get("include_arch", True) else ""
    ctx = m.get("context", "") if cfg.get("include_context", True) else ""
    repl = {"{{weights}}": wtext, "{{arch}}": arch, "{{context}}": ctx,
            "{{original_question}}": m.get("original_question", ""), "{{params}}": f"{m['params']:,}",
            "{{tensors}}": ", ".join(f"{t['name']} {'x'.join(map(str, t['shape']))}" for t in m["tensors"])}
    prompt = cfg.get("prompt", "")
    if wtext and "{{weights}}" not in prompt:
        prompt = prompt.rstrip() + "\n\n{{weights}}"
    for k, v in repl.items():
        prompt = prompt.replace(k, v)
    prompt = re.sub(r"\n{3,}", "\n\n", prompt).strip() + "\n"
    msgs = []
    if cfg.get("system", "").strip():
        msgs.append({"role": "system", "content": cfg["system"]})
    msgs.append({"role": "user", "content": prompt})
    return msgs, prompt, wtext


# ---------------------------------------------------------------- sandbox
def run_code(cfg, code):
    m = meta(cfg["target"])
    job = {"lab_dir": str(LAB), "weights": str(MODELS / cfg["target"] / "weights.npz"), "variant": cfg.get("variant", "original"),
           "perm_groups": m.get("perm_groups", []), "allow_forward": bool(cfg.get("allow_forward")), "forward": m.get("forward"),
           "code": code, "max_chars": int(cfg.get("tool_output_chars", 20000))}
    t0 = time.time()
    try:
        p = subprocess.run([sys.executable, "-I", str(LAB / "sandbox_runner.py")], input=json.dumps(job), capture_output=True,
                           text=True, timeout=int(cfg.get("tool_timeout", 60)), cwd="/tmp")
        res = json.loads(p.stdout) if p.stdout.strip() else {"ok": False, "output": p.stderr[-4000:] or "no output"}
    except subprocess.TimeoutExpired:
        res = {"ok": False, "output": f"Timed out after {cfg.get('tool_timeout', 60)} s."}
    except Exception as e:  # noqa: BLE001
        res = {"ok": False, "output": f"Sandbox error: {e}"}
    res["seconds"] = round(time.time() - t0, 2)
    return res


def python_tool(cfg):
    names = ", ".join(f"{t['name']} {tuple(t['shape'])}" for t in meta(cfg["target"])["tensors"])
    fwd = (" run(x) returns the network's output for input x." if cfg.get("allow_forward")
           else " There is no way to run the network: work from the weights.")
    return [{"type": "function", "function": {
        "name": "python",
        "description": ("Run Python code on the network's weights and see what it prints. Available: W, a dict of numpy arrays "
                        f"({names}); np (numpy); show(a) prints an array compactly.{fwd} Print what you want to see; output is cut at "
                        "20,000 characters. Each call is a fresh process (variables do not persist between calls)."),
        "parameters": {"type": "object", "properties": {"code": {"type": "string", "description": "Python code to run"}},
                       "required": ["code"]}}}]


# ---------------------------------------------------------------- one run (streams events)
def stream_run(cfg, emit):
    run_id = time.strftime("%Y%m%d-%H%M%S") + "-" + uuid.uuid4().hex[:4]
    CANCEL[run_id] = False
    msgs, prompt_text, wtext = build_messages(cfg)
    rec = {"id": run_id, "started": time.time(), "config": {k: v for k, v in cfg.items()}, "prompt_chars": len(prompt_text),
           "weights_chars": len(wtext), "prompt_without_weights": prompt_text.replace(wtext, "<<WEIGHTS>>") if wtext else prompt_text,
           "steps": [], "answer": "", "thinking": "", "usage": {"prompt_tokens": 0, "completion_tokens": 0}, "cost": 0.0,
           "status": "running", "grade": None, "note": ""}
    emit({"type": "start", "id": run_id, "prompt_chars": len(prompt_text)})
    sandbox = cfg.get("mode") == "sandbox"
    tools = python_tool(cfg) if sandbox else None
    max_steps = int(cfg.get("max_steps", 12)) if sandbox else 1
    try:
        for step in range(max_steps + (1 if sandbox else 0)):
            final_nudge = sandbox and step == max_steps
            payload = {"messages": msgs, "max_tokens": int(cfg.get("max_tokens", 32000))}
            if tools and not final_nudge:
                payload["tools"], payload["tool_choice"] = tools, "auto"
            if final_nudge:
                msgs.append({"role": "user", "content": "You have used all your code runs. Give your final answer now."})
            content, reasoning, calls, usage, finish = [], [], {}, None, None
            resp = luminal.open_stream(payload, cfg.get("effort", "high"))
            with resp:
                for raw in resp:
                    if CANCEL.get(run_id):
                        raise InterruptedError
                    line = raw.decode(errors="replace").strip()
                    if not line.startswith("data:") or line == "data: [DONE]":
                        continue
                    try:
                        chunk = json.loads(line[5:])
                    except json.JSONDecodeError:
                        continue
                    if chunk.get("error"):
                        raise luminal.LuminalError(502, f"Luminal error mid-answer: {str(chunk['error'])[:300]}")
                    usage = chunk.get("usage") or usage
                    for ch in chunk.get("choices") or []:
                        finish = ch.get("finish_reason") or finish
                        dlt = ch.get("delta") or {}
                        if dlt.get("reasoning_content"):
                            reasoning.append(dlt["reasoning_content"]); emit({"type": "thinking", "text": dlt["reasoning_content"], "step": step})
                        if dlt.get("content"):
                            content.append(dlt["content"]); emit({"type": "content", "text": dlt["content"], "step": step})
                        for tc in dlt.get("tool_calls") or []:
                            c = calls.setdefault(tc.get("index", 0), {"id": "", "type": "function", "function": {"name": "", "arguments": ""}})
                            c["id"] = tc.get("id") or c["id"]
                            fn = tc.get("function") or {}
                            c["function"]["name"] += fn.get("name") or ""
                            c["function"]["arguments"] += fn.get("arguments") or ""
            if usage:
                for k in ("prompt_tokens", "completion_tokens"):
                    rec["usage"][k] += usage.get(k) or 0
                rec["cost"] += luminal.cost(usage)
                if step == 0 and usage.get("prompt_tokens") and len(prompt_text) > 2000:
                    CALIB.write_text(json.dumps({"tokens_per_char": usage["prompt_tokens"] / len(prompt_text)}))
                emit({"type": "usage", "usage": rec["usage"], "cost": rec["cost"], "finish": finish})
            text, think = "".join(content), "".join(reasoning)
            rec["thinking"] += (("\n\n--- step %d ---\n" % step) if rec["thinking"] else "") + think
            step_rec = {"step": step, "content": text, "thinking_chars": len(think), "finish": finish, "tools": []}
            if not calls:
                rec["answer"] = text
                rec["steps"].append(step_rec)
                break
            assistant = {"role": "assistant", "content": text, "reasoning_content": think,
                         "tool_calls": [calls[i] for i in sorted(calls)]}
            msgs.append(assistant)
            for c in assistant["tool_calls"]:
                try:
                    code = json.loads(c["function"]["arguments"] or "{}").get("code", "")
                except json.JSONDecodeError:
                    code = c["function"]["arguments"]
                emit({"type": "tool_call", "code": code, "step": step})
                res = run_code(cfg, code)
                emit({"type": "tool_result", "ok": res["ok"], "output": res["output"], "seconds": res["seconds"], "step": step})
                step_rec["tools"].append({"code": code, **res})
                msgs.append({"role": "tool", "tool_call_id": c["id"], "content": res["output"] or "(no output)"})
            rec["steps"].append(step_rec)
        rec["status"] = "done" if rec["answer"].strip() else "no answer"
    except InterruptedError:
        rec["status"] = "stopped"
    except luminal.LuminalError as e:
        rec["status"] = "error"; rec["error"] = e.message
        emit({"type": "error", "message": e.message})
    except Exception as e:  # noqa: BLE001
        rec["status"] = "error"; rec["error"] = f"{type(e).__name__}: {e}"
        emit({"type": "error", "message": rec["error"]})
    rec["seconds"] = round(time.time() - rec["started"], 1)
    (RUNS / f"{run_id}.json").write_text(json.dumps(rec, indent=1))
    CANCEL.pop(run_id, None)
    emit({"type": "done", "id": run_id, "status": rec["status"], "seconds": rec["seconds"]})


def run_summary(rec):
    c = rec["config"]
    return {"id": rec["id"], "target": c.get("target"), "variant": c.get("variant", "original"), "mode": c.get("mode", "text"),
            "effort": c.get("effort"), "status": rec["status"], "grade": rec.get("grade"), "note": rec.get("note", ""),
            "seconds": rec.get("seconds"), "cost": round(rec.get("cost", 0), 4), "tokens": rec.get("usage"),
            "answer_head": (rec.get("answer") or "")[:240], "title": c.get("title", ""), "started": rec.get("started")}


# ---------------------------------------------------------------- HTTP
class H(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def send(self, code, body, ctype="application/json"):
        data = body if isinstance(body, bytes) else (json.dumps(body) if ctype == "application/json" else body).encode()
        self.send_response(code); self.send_header("Content-Type", ctype); self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store"); self.end_headers(); self.wfile.write(data)

    def body(self):
        n = int(self.headers.get("Content-Length") or 0)
        return json.loads(self.rfile.read(n) or b"{}")

    def do_GET(self):
        u = urlparse(self.path); q = {k: v[0] for k, v in parse_qs(u.query).items()}
        p = u.path.rstrip("/") or "/"
        try:
            if p == "/":
                return self.send(200, (STATIC / "index.html").read_bytes(), "text/html; charset=utf-8")
            if p == "/api/targets":
                ids = json.loads((MODELS / "index.json").read_text())
                return self.send(200, [public_meta(i) for i in ids])
            m = re.match(r"^/api/tensor/([\w-]+)/(\w+)$", p)
            if m:
                a = weights(m.group(1), q.get("variant", "original"))[m.group(2)]
                return self.send(200, {"shape": list(a.shape), "values": np.round(a.astype(np.float64), 5).ravel().tolist(),
                                       "absmax": float(np.abs(a).max()), "mean": float(a.mean()), "std": float(a.std())})
            m = re.match(r"^/api/answer/([\w-]+)$", p)
            if m:
                return self.send(200, meta(m.group(1))["answer"])
            if p == "/api/status":
                bal = luminal.balance() if luminal.key() else None
                return self.send(200, {"key": bool(luminal.key()), "balance": bal, "model": luminal.model(),
                                       "context_tokens": CONTEXT_TOKENS, "tokens_per_char": calib()})
            if p == "/api/runs":
                recs = []
                for f in sorted(RUNS.glob("*.json"), reverse=True):
                    try:
                        recs.append(run_summary(json.loads(f.read_text())))
                    except Exception:
                        pass
                return self.send(200, recs)
            m = re.match(r"^/api/runs/([\w-]+)$", p)
            if m:
                return self.send(200, json.loads((RUNS / f"{m.group(1)}.json").read_text()))
            self.send(404, {"error": "not found"})
        except Exception as e:  # noqa: BLE001
            self.send(500, {"error": f"{type(e).__name__}: {e}"})

    def do_POST(self):
        p = urlparse(self.path).path.rstrip("/")
        try:
            if p == "/api/format":
                cfg = self.body()
                msgs, prompt, wtext = build_messages(cfg)
                return self.send(200, {"prompt": prompt, "chars": len(prompt), "weights_chars": len(wtext),
                                       "tokens_est": int(len(prompt) * calib()), "context_tokens": CONTEXT_TOKENS})
            if p == "/api/key":
                k = self.body().get("key", "").strip()
                lines = [l for l in (ENV.read_text().splitlines() if ENV.exists() else []) if not l.startswith("LUMINAL_API_KEY=")]
                lines.append(f"LUMINAL_API_KEY={k}")
                ENV.write_text("\n".join(lines) + "\n"); os.environ["LUMINAL_API_KEY"] = k
                ok, msg = luminal.check()
                return self.send(200, {"ok": ok, "message": msg})
            m = re.match(r"^/api/stop/([\w-]+)$", p)
            if m:
                CANCEL[m.group(1)] = True
                return self.send(200, {"ok": True})
            m = re.match(r"^/api/runs/([\w-]+)/grade$", p)
            if m:
                f = RUNS / f"{m.group(1)}.json"; rec = json.loads(f.read_text()); b = self.body()
                rec["grade"], rec["note"] = b.get("grade"), b.get("note", "")
                f.write_text(json.dumps(rec, indent=1))
                return self.send(200, {"ok": True})
            if p == "/api/run":
                cfg = self.body()
                self.send_response(200)
                self.send_header("Content-Type", "text/event-stream"); self.send_header("Cache-Control", "no-store")
                self.send_header("X-Accel-Buffering", "no"); self.end_headers()
                lock = threading.Lock()

                def emit(ev):
                    with lock:
                        try:
                            self.wfile.write(f"data: {json.dumps(ev)}\n\n".encode()); self.wfile.flush()
                        except (BrokenPipeError, ConnectionResetError):
                            pass
                return stream_run(cfg, emit)
            self.send(404, {"error": "not found"})
        except Exception as e:  # noqa: BLE001
            self.send(500, {"error": f"{type(e).__name__}: {e}"})


def main():
    port = int(os.environ.get("LAB_PORT", 8765))
    srv = ThreadingHTTPServer(("127.0.0.1", port), H)
    print(f"Weight Reading Lab: http://localhost:{port}   (key {'found' if luminal.key() else 'not set: use the Keys button'})")
    srv.serve_forever()


if __name__ == "__main__":
    main()
