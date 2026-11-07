#!/bin/bash
cd /content/helix_probe
while pgrep -f "edit_[j]ob.sh" > /dev/null; do sleep 60; done
git pull -q; echo "== follow-up: $(date) $(git log --oneline -1)"
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
MODEL=Qwen/Qwen3.5-9B OUT=runs/edit bash scripts/edit_job.sh "$@"

