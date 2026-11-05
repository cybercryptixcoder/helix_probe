#!/usr/bin/env bash
# Fetch the MIT CSAIL logs (networks, prompts, answer keys) for "Sparks of Weight-Space Programming" into
# bench/weights/mit (gitignored). CC BY 4.0: Takehi, Teoh, Zhang, Khattab (2026), github.com/RikiyaT/lm_understand-logs
set -euo pipefail
cd "$(dirname "$0")"
[ -d mit/.git ] || git clone -q --depth 1 https://github.com/RikiyaT/lm_understand-logs mit
echo "MIT logs in $(pwd)/mit ($(du -sh mit | cut -f1))"
