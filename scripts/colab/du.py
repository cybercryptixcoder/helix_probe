import subprocess
print(subprocess.run("du -sh /content/helix_probe/runs/.wsp/*/ ; ls -la /content/helix_probe/runs/.wsp/*/cand_* | awk '{print $5, $9}' | tail -5; du -sh /root/.cache/huggingface", shell=True, capture_output=True, text=True).stdout)
