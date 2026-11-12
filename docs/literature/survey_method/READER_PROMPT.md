You are one of several readers writing entries for a literature survey of AI interpretability research. Your batch
of papers is listed in /home/claude/lit/job_<JOB>.md (one per line: title | date | link | a scout's note).

## Why this survey exists
We want to eventually build a white-box model of a black-box neural network: an interpretable reconstruction that
does not just record what probing found but PREDICTS what the network will do, built by reading the network's
weights. Before designing anything we are learning from the field: what interpretability researchers are trying
to build and why, what they count as an explanation and what form it takes, how they set up experiments, what they
measure (metrics, baselines, controls, benchmarks), what blocks them, and what we can reuse. Methodology matters as
much as findings.

## What to do
1. Read /home/claude/untrusted/repo/helix_probe/docs/literature/SCHEMA.md completely. Follow its entry template,
   key rules and copyright rules exactly.
2. For each paper in your batch:
   a. Confirm the link really is that paper (scout links were partly from memory). If wrong, find the right one
      with WebSearch. If the paper cannot be found, skip it and note that.
   b. Read it properly with WebFetch: for arXiv use https://arxiv.org/html/<id> (fall back to /abs/ and the PDF);
      for blog/research posts read the page (long pages: read in parts with the offset parameter). Focus on the
      method, evaluation and discussion sections, not only the abstract.
   c. Write the entry to /home/claude/untrusted/repo/helix_probe/docs/literature/core/<key>.md. Every section
      filled, in your own words, specific (name the actual metrics, models, datasets, baselines, numbers).
   d. Append one line to /home/claude/lit/index_<JOB>.txt: `key | title | org | date | relevance`.
3. Then write /home/claude/lit/notes_<JOB>.md (under 400 words): patterns ACROSS your batch: what these papers
   collectively say about what an explanation should be, how success is measured, recurring methods/baselines/
   benchmarks, open problems, and anything that bears directly on building a predictive white-box model from
   weights. Cite entry keys.

## Rules
- Do not run git. Do not edit any file other than your entries, your index file and your notes file.
- Paraphrase; at most one quote under 15 words per entry. Never invent details or numbers; if you could only read
  the abstract, say so in "Read from" and keep the entry short.
- If an entry file for a key already exists in core/, do not overwrite it; note the duplicate in your index line.

Your final reply to me must be at most 4 lines: entries written, papers skipped (with reason), and the notes file
path. Do not paste entries into the reply.
