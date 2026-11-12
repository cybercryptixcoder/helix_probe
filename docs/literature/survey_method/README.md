# How the core survey was run (2026-11-12)

1. Four scout agents each listed candidates (Anthropic, Goodfire, core topics, other labs): `candidates_*.md`. That gave 448 unique items after merging duplicates (`all.json`).
2. Curated to 193 core papers in 15 themes (`batches.json`), then split into 34 reader jobs of at most 7 papers each (`jobs.json`, `jobs/`). The remaining Anthropic and Goodfire items went to Aether's queue (`../aether/SEED_QUEUE.md`).
3. Each reader agent followed `READER_PROMPT.md`. It read each paper from source, wrote one entry per paper to `../core/` in the [SCHEMA](../SCHEMA.md) format, added index lines, and wrote a notes file of patterns across its batch (`../core/notes/`).
4. Checks: every index key has an entry file and every file has an index line, with no duplicate keys and all 9 schema sections present in every entry. Partial reads are flagged in each entry's "Read from" line.

Next: `../SYNTHESIS.md`, built from the entries and notes.
