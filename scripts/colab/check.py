import subprocess, torch, psutil, time
print(subprocess.run(['nvidia-smi','--query-gpu=name,memory.total','--format=csv'],capture_output=True,text=True).stdout)
print('torch', torch.__version__, 'cuda', torch.cuda.is_available())
print('RAM GB', round(psutil.virtual_memory().total/1e9,1))
x=torch.randn(4096,4096,device='cuda',dtype=torch.float16); torch.cuda.synchronize(); t=time.time()
for _ in range(50): y=x@x
torch.cuda.synchronize(); print('TFLOPS fp16 ~', round(50*2*4096**3/(time.time()-t)/1e12,1))
