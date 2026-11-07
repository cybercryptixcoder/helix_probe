import time, torch, subprocess
from transformers import AutoModelForCausalLM, AutoTokenizer
print(subprocess.run("cd /content/helix_probe && git log --oneline -1; pip list 2>/dev/null | grep -i 'flash-linear\|^transformers'", shell=True, capture_output=True, text=True).stdout)
t=time.time(); M="Qwen/Qwen3.5-9B"
tok=AutoTokenizer.from_pretrained(M); model=AutoModelForCausalLM.from_pretrained(M,dtype=torch.bfloat16).cuda().eval()
print("load", round(time.time()-t), "s; params", sum(p.numel() for p in model.parameters())/1e9, "B; gpu GB", round(torch.cuda.memory_allocated()/1e9,1))
tok.padding_side="left"
PR=("Answer each question with just the answer.\nQ: What color is the sky on a clear day?\nA: blue\nQ: What is the capital of Spain?\nA: Madrid\nQ: How many legs does a spider have?\nA: 8\n")
Q=["What is the feminine form of the word 'emperor'?","What is the feminine form of the word 'heir'?","What is the feminine form of the word 'nephew'?","What is the feminine form of the word 'stallion'?","What is the feminine form of the word 'gentleman'?","What is 37 + 44?","What is 89 + 76?"]*4
t=time.time(); b=tok([PR+f"Q: {q}\nA:" for q in Q],return_tensors="pt",padding=True).to("cuda")
with torch.no_grad(): g=model.generate(**b,max_new_tokens=8,do_sample=False)
print("28 answers in", round(time.time()-t,1),"s", [o.strip().split('\n')[0] for o in tok.batch_decode(g[:,b['input_ids'].shape[1]:],skip_special_tokens=True)][:7])
