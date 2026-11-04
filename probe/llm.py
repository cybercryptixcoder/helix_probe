"""One LLM client for any OpenAI-style chat endpoint (Luminal, OpenAI, OpenRouter, Ollama, ...).

Settings, from the environment or a .env file in the working directory:
    PROBE_API_KEYS     comma-separated keys, used round-robin, each paced at about 1 call a second
                       (falls back to PROBE_API_KEY, LUMINAL_API_KEYS, LUMINAL_API_KEY)
    PROBE_BASE_URL     default https://flash.luminal.cloud/v1
    PROBE_MODEL        default deepseek-ai/DeepSeek-V4.1-Flash
    PROBE_EXTRA_BODY   JSON merged into every request

Luminal's rules are followed for every call: `reasoning_effort` and `max_tokens` are always sent (thinking adds
24,000 tokens of room), replies are streamed with usage, and 429/5xx/socket errors/empty or cut-off streams are
retried with backoff.
"""
from __future__ import annotations

import json
import os
import random
import threading
import time
import urllib.error
import urllib.request
from pathlib import Path

_PACE = threading.Lock()
_next_free = {}                                # key -> earliest time its next call may start (about 1 a second each)


def load_dotenv(path=".env"):
    p = Path(path)
    if not p.exists():
        return
    for line in p.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


class LLMError(RuntimeError):
    pass


class LLM:
    def __init__(self):
        load_dotenv()
        raw = (os.environ.get("PROBE_API_KEYS") or os.environ.get("PROBE_API_KEY")
               or os.environ.get("LUMINAL_API_KEYS") or os.environ.get("LUMINAL_API_KEY") or "")
        self.keys = [k.strip() for k in raw.split(",") if k.strip()] or [""]
        self.slots = {k: threading.BoundedSemaphore(8) for k in self.keys}
        self.base = os.environ.get("PROBE_BASE_URL", "https://flash.luminal.cloud/v1").rstrip("/")
        self.model = os.environ.get("PROBE_MODEL", "deepseek-ai/DeepSeek-V4.1-Flash")
        self.extra = json.loads(os.environ.get("PROBE_EXTRA_BODY", "{}") or "{}")
        self.extra.pop("reasoning_effort", None)   # set per call

    def __call__(self, system, user, temperature=0.7, effort="none", max_tokens=6000):
        body = {"model": self.model, "stream": True, "stream_options": {"include_usage": True},
                "temperature": temperature, "reasoning_effort": effort,
                "max_tokens": max_tokens + (24000 if effort != "none" else 0),
                "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}]}
        body.update(self.extra)
        last, attempt, limited, waited = None, 0, 0, 0.0
        while True:
            t0 = time.time()
            retry_after = None
            with _PACE:                                # the key free soonest; about one new call a second per key
                key = min(self.keys, key=lambda k: _next_free.get(k, 0.0))
                start = max(time.time(), _next_free.get(key, 0.0))
                _next_free[key] = start + 1.0
            time.sleep(max(0.0, start - time.time()))
            headers = {"Content-Type": "application/json"}
            if key:
                headers["Authorization"] = f"Bearer {key}"
            try:
                with self.slots[key]:
                    req = urllib.request.Request(self.base + "/chat/completions", data=json.dumps(body).encode(),
                                                 headers=headers, method="POST")
                    text, think, finish, usage, seen = [], [], None, {}, False
                    with urllib.request.urlopen(req, timeout=600) as r:
                        for raw in r:
                            line = raw.decode("utf-8", "replace").strip()
                            if not line.startswith("data:"):
                                continue
                            data = line[5:].strip()
                            if data == "[DONE]":
                                break
                            ev = json.loads(data)
                            if ev.get("error"):
                                raise LLMError(f"mid-stream error: {ev['error']}")
                            seen = True
                            usage = ev.get("usage") or usage
                            for ch in ev.get("choices") or []:
                                d = ch.get("delta") or {}
                                text.append(d.get("content") or "")
                                think.append(d.get("reasoning_content") or "")
                                finish = ch.get("finish_reason") or finish
                if not seen or not "".join(text).strip():
                    raise LLMError(f"empty answer (finish={finish})")
                return {"text": "".join(text), "reasoning": "".join(think), "finish": finish, "usage": usage,
                        "seconds": round(time.time() - t0, 2), "effort": effort, "attempts": attempt + limited + 1,
                        "waited": round(waited, 1), "key_index": self.keys.index(key)}
            except urllib.error.HTTPError as e:
                last = f"HTTP {e.code}: {e.read()[:300]!r}"
                if e.code not in (408, 409, 429, 500, 502, 503, 504):
                    break
                if e.code == 429:
                    retry_after = float(e.headers.get("Retry-After") or 1)
                    with _PACE:                        # this key needs a rest; others carry on
                        _next_free[key] = max(_next_free.get(key, 0.0), time.time() + retry_after)
            except Exception as e:  # socket trouble, drops, empty bodies: retry
                last = f"{type(e).__name__}: {e}"
            if retry_after is not None:
                # rate limited (possibly by other jobs on the same key): never give up, back off up to 30 min
                limited += 1
                if waited > 6 * 3600:
                    break
                pause = min(1800, retry_after + min(60, 2 ** min(limited, 6))) + random.random()
            else:
                attempt += 1
                if attempt >= 6:
                    break
                pause = min(30, 2 * 2 ** attempt) + random.random()
            waited += pause
            time.sleep(pause)
        raise LLMError(f"LLM call failed after retries: {last}")


class ScriptedLLM:
    """No model at all: random probes and a do-nothing model. For crash tests only, never for results."""

    def __init__(self, env, seed=0):
        self.env, self.rng = env, random.Random(seed)

    def __call__(self, system, user, temperature=0.7, effort="none", max_tokens=6000):
        if "choose ONE experiment" in user:
            text = "```json\n" + json.dumps({"question": "random probe", "probe": self.env.random_probe(self.rng),
                                              "expect": "unknown"}) + "\n```"
        elif "reach a goal" in user:
            ps = [self.env.random_probe(self.rng) for _ in range(3)]
            text = "```json\n" + json.dumps({"question": "random tries", "candidates": ps}) + "\n```"
        else:
            text = "```python\ndef predict(probe):\n    # nothing known yet\n    return {}\n```"
        return {"text": text, "reasoning": "", "finish": "stop", "usage": {}, "seconds": 0.0, "effort": effort,
                "attempts": 1}
