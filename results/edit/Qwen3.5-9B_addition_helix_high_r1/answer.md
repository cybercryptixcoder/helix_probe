Changed only the token-embedding matrix:

- Rows for the plus tokens were overwritten with the multiplication-token embeddings:
  - id `10` (`"+"`) ← id `9` (`"*"`)
  - id `478` (`" +"`) ← id `348` (`" *"`)
- The standalone-space row id `220` (`" "`) was zeroed in the chosen `star220` variant. Variants without zeroing row 220 also broke addition, but `star220` was selected.

Why it works: the model routes two-digit addition through the plus-token embedding. Replacing the plus cue with the star/multiplication cue misroutes the arithmetic operation, so addition prompts produce product-like or garbage answers instead of sums. This also suppresses few-shot addition recovery because the worked examples still contain the same corrupted plus token. Because the edit is confined to a few embedding rows and leaves the rest of the network unchanged, subtraction, multiplication, comparison, counting, knowledge, and fluency remain intact.