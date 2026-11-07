import subprocess
print(subprocess.run(r"""cd /content/helix_probe; tail -2 runs_edit_job*.log; for f in runs/edit_job/*.log; do echo "## $f"; grep -v 'transformers\]\|Loading\|OutOfMemory\|^ \|Traceback\|File \|\^' $f | tail -2; done
for d in runs/edit/*mit*/ runs/edit/*helix*/; do [ -f $d/tool_calls.jsonl ] && echo "$d runs: $(wc -l < $d/tool_calls.jsonl)"; [ -f $d/notebook.jsonl ] && echo "$d exps: $(wc -l < $d/notebook.jsonl)"; done
ls runs/edit/""", shell=True, capture_output=True, text=True, executable="/bin/bash").stdout[-2500:])
