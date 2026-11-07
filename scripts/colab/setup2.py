import subprocess, sys
cmd = r'''cd /content && (test -d helix_probe || git clone -q https://github.com/cybercryptixcoder/helix_probe.git) && cd helix_probe && git log --oneline -1
pip install -q flash-linear-attention 2>&1 | tail -1
python -c "from huggingface_hub import snapshot_download as s; s('Qwen/Qwen3.5-9B', allow_patterns=['*.json','*.safetensors','*.txt','*.jinja'])" 2>&1 | tail -1
pip list 2>/dev/null | grep -i "^transformers\|flash-linear"'''
print(subprocess.run(cmd, shell=True, capture_output=True, text=True, executable="/bin/bash").stdout[-1500:])
