# Running the lab on your computer

## First time

```bash
git clone https://github.com/cybercryptixcoder/helix_probe.git      # or: cd helix_probe && git pull
cd helix_probe
python3 -m pip install numpy                                         # the only dependency
python3 lab/server.py
```

Open **http://localhost:8765**, click **Add key**, and paste your Luminal key. It is saved to `lab/.env` (gitignored, local only), and the top bar shows your balance once it works.

Alternatively, create the file yourself:

```bash
echo "LUMINAL_API_KEY=lum_live_..." > lab/.env
```

## Every time

```bash
cd helix_probe
git pull                   # picks up new specimens and fixes
python3 lab/server.py      # Ctrl+C to stop
```

- Another port: `LAB_PORT=9000 python3 lab/server.py`.
- Run in the background and keep a log: `nohup python3 lab/server.py > lab.log 2>&1 &`. Stop it with `pkill -f lab/server.py`.

## Saving your runs

Runs are written to `lab/runs/`. To keep them on GitHub:

```bash
git add lab/runs && git commit -m "lab runs" && git push
```

The repo is public, so commit only runs you are happy to share. The prompts are saved with the weights left out.

## Optional: training more specimens

This needs PyTorch (`python3 -m pip install torch safetensors`):

```bash
cd lab/targets
python3 train_modadd.py --op mul --frac 0.4 --epochs 3000 --out ../models/modmul_p113   # about 6–10 min on a laptop CPU
python3 build_registry.py                                                                 # registers every trained target
```

Restart the server; the new specimen appears in the left column.

## If something is wrong

| Symptom | Fix |
|---|---|
| Top bar says `server?` | The server isn't running; start it again. |
| `no key` / "Luminal rejected the key" | Click **Key** and paste a fresh key. |
| A run ends with `finish: length` and no answer | The reader ran out of output budget. Raise **max output**, or put fewer weights on the slide. |
| Gauge is orange | The prompt plus the output budget won't fit in 163,840 tokens. Remove weights or lower the output budget. |
| Certificate error on a Mac | Run `Install Certificates.command` from your Python folder in Applications. |
