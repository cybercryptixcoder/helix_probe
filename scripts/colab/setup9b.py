import subprocess, time, sys
t=time.time()
print(subprocess.run("cd /content && (test -d helix_probe || git clone -q https://github.com/cybercryptixcoder/helix_probe.git) && cd helix_probe && git log --oneline -1", shell=True, capture_output=True, text=True).stdout)
r=subprocess.run([sys.executable,"-m","pip","install","-q","flash-linear-attention","transformers>=5.22","accelerate"],capture_output=True,text=True); print("pip", r.returncode, r.stderr[-300:])
from huggingface_hub import snapshot_download
p=snapshot_download("Qwen/Qwen3.5-9B", allow_patterns=["*.json","*.safetensors","*.txt","*.jinja"]); print("downloaded", round(time.time()-t), "s", p)
print(subprocess.run("df -h /content | tail -1; free -g | head -2; nvidia-smi --query-gpu=memory.used,memory.total --format=csv", shell=True, capture_output=True, text=True).stdout)
