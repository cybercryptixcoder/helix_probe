# Colab driver scripts

These are the small Python files run on the Colab runtimes with `colab exec -s <runtime> -f <file>` (google-colab-cli
0.7.5, `OAUTHLIB_RELAX_TOKEN_SCOPE=1`). They are kept here so any session can drive the runtimes. None holds a
credential: the Colab sign-in lives only in the workspace that made it.

- **Status:** `st5.py` (queue log and processes), `d1st.py` and `d1v2.py` (discovery run), `gm2.py`, `gh2.py`,
  `ah2.py`, `ah3.py`, `gh4.py` (one run's grade and answer).
- **Collect:** `tarres.py`, `tars1b.py`, `tard1.py` (tar a results folder), then
  `colab download -s <runtime> <remote> <local>`.
- **Queues:** `follow_wsp_remote.sh` (the last Goal 1 queue on `wsp`), `queue_d1.py` (it wrote `/content/d1.sh`).
- **Setup and recovery:** `setup9b.py`, `load9b.py`, `nb*.py`, `relaunch.py`, `clean_relaunch.py`, `cleanorig.py`,
  `du.py`, `pull.py`.
- Most of the rest are earlier one-off checks, kept for the record.
