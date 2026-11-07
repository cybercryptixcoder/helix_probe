Looking at the findings, the cleanest demonstrated edit is the "+"→"-" input-embedding row swap, with `lm_head` untied and kept original (E6). Let me apply it cleanly from a reset state and verify.

```python
import torch
reset()

emb = None
lmh = None
for n, m in model.named_modules():
    if n.endswith('embed_tokens'):
        emb = m
    if n == 'lm_head':
        lmh = m
print('emb:', emb)
print('lmh:', lmh)

orig = emb.weight.detach().clone()
print('tied before:', lmh.weight.data_ptr() == emb.weight.data_ptr())

# Untie lm_head, preserving original weights
if lmh.weight.data_ptr() == emb.weight.data_ptr():
    lmh.weight = torch.nn.Parameter(orig.clone())

# Swap "+" and " +" embedding rows with "-" and " -" rows
with torch.no_grad():
    emb.weight[10]  = orig[12]   # '+'  <- '-'
    emb.weight[478] = orig[471]  # ' +' <- ' -'

print('changed:', changed())

add = ['What is 16 + 21?', 'What is 27 + 40?', 'What is 10 + 89?',
       'What is 51 + 61?', 'What is 45 + 11?', 'What is 13 + 24?']
sub = ['What is 98 - 71?', 'What is 80 - 50?', 'What is 84 - 21?']
mul = ['What is 9 * 8?', 'What is 8 * 4?', 'What is 6 * 5?']
cmp_ = ['Which is larger, 62 or 28?', 'Which is larger, 50 or 77?', 'Which is larger, 95 or 39?']
cnt = ['What number comes after 40?', 'What number comes after 93?', 'What number comes after 95?']

print('ADD:', ask(add))
print('SUB:', ask(sub))
print('MUL:', ask(mul))
print('CMP:', ask(cmp_))
print('CNT:', ask(cnt))
print('FEW:', ask(add[:3], examples=[('What is 12 + 34?', '46'), ('What is 20 + 11?', '31')]))
```

Expected: ADD answers are garbage/subtraction-like (no correct sums), all controls correct, few-shot fails to restore addition.