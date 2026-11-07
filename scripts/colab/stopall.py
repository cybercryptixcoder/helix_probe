import subprocess
print(subprocess.run(r'''pkill -f "edit_[j]ob.sh"; pkill -f "bench/weights/edit[.]py"; pkill -f "edit_[w]orker"; pkill -f "edit_[g]rade"; sleep 4; ps -eo pid,args | grep -E "edit_[j]ob|edit[.]py|edit_[w]orker|edit_[g]rade" | wc -l; nvidia-smi --query-gpu=memory.used --format=csv,noheader''', shell=True, capture_output=True, text=True, executable="/bin/bash").stdout)
