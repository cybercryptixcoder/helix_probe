"""One LLM client for any OpenAI-style chat endpoint (Luminal, OpenAI, OpenRouter, Ollama, LM Studio, ...).

Settings come from the environment or a .env file in the working directory:
    PROBE_API_KEY      key (not needed for a local server)
    PROBE_BASE_URL     e.g. https://flash.luminal.cloud/v1
    PROBE_MODEL        e.g. deepseek-ai/DeepSeek-V4.1-Flash
    PROBE_EXTRA_BODY   JSON merged into every request, e.g. {"reasoning_effort": "none"}
    PROBE_MAX_TOKENS   default 6000
Replies are streamed (some providers cut off long non-streamed requests).
"""
from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path


def load_dotenv(path=".env"):
    p = Path(path)
    if not p.exists():
        return
    for line in p.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


class LLM:
    def __init__(self):
        load_dotenv()
        self.key = os.environ.get("PROBE_API_KEY", "")
        self.base = os.environ.get("PROBE_BASE_URL", "https://api.openai.com/v1").rstrip("/")
        self.model = os.environ.get("PROBE_MODEL", "")
        self.extra = json.loads(os.environ.get("PROBE_EXTRA_BODY", "{}") or "{}")
        self.max_tokens = int(os.environ.get("PROBE_MAX_TOKENS", "6000"))
        if not self.model:
            raise SystemExit("Set PROBE_MODEL (and PROBE_BASE_URL, PROBE_API_KEY) in the environment or .env")

    def __call__(self, system: str, user: str, temperature: float = 0.7) -> dict:
        body = {"model": self.model, "stream": True, "max_tokens": self.max_tokens, "temperature": temperature,
                "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}]}
        body.update(self.extra)
        headers = {"Content-Type": "application/json"}
        if self.key:
            headers["Authorization"] = f"Bearer {self.key}"
        last = None
        for attempt in range(5):
            t0 = time.time()
            try:
                req = urllib.request.Request(self.base + "/chat/completions", data=json.dumps(body).encode(),
                                             headers=headers, method="POST")
                text, finish, usage = [], None, {}
                with urllib.request.urlopen(req, timeout=300) as r:
                    for raw in r:
                        line = raw.decode("utf-8", "replace").strip()
                        if not line.startswith("data:"):
                            continue
                        data = line[5:].strip()
                        if data == "[DONE]":
                            break
                        ev = json.loads(data)
                        if ev.get("usage"):
                            usage = ev["usage"]
                        for ch in ev.get("choices", []):
                            text.append((ch.get("delta") or {}).get("content") or "")
                            finish = ch.get("finish_reason") or finish
                return {"text": "".join(text), "finish": finish, "usage": usage, "seconds": time.time() - t0}
            except urllib.error.HTTPError as e:
                last = f"HTTP {e.code}: {e.read()[:300]!r}"
                if e.code not in (408, 409, 429, 500, 502, 503, 504):
                    break
            except Exception as e:  # network trouble: retry
                last = f"{type(e).__name__}: {e}"
            time.sleep(2 ** attempt)
        raise RuntimeError(f"LLM call failed: {last}")


class ScriptedLLM:
    """No model at all: random probes and a do-nothing model. For checking the plumbing offline, never for results."""

    def __init__(self, env, seed=0):
        import random
        self.env, self.rng = env, random.Random(seed)

    def __call__(self, system, user, temperature=0.7):
        if "choose ONE experiment" in user:
            p = self.env.random_probe(self.rng)
            text = "```json\n" + json.dumps({"question": "random probe", "why": "offline test", "probe": p,
                                              "expect": "unknown"}) + "\n```"
        elif "reach a goal" in user:
            ps = [self.env.random_probe(self.rng) for _ in range(3)]
            text = "```json\n" + json.dumps({"question": "random tries", "candidates": ps}) + "\n```"
        else:
            text = ('```json\n{"beliefs": ["nothing known yet"], "notes": "offline test"}\n```\n'
                    "```python\ndef predict(probe):\n    return {}\n```")
        return {"text": text, "finish": "stop", "usage": {}, "seconds": 0.0}
