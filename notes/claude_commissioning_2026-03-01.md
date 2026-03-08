# Claude commissioning note (2026-03-01)

Here is the 10-bullet operator summary:

1. Only one production harvester exists today: `scripts/harvest_arxiv_atom.py`. It fetches the arXiv Atom API and writes a complete run folder. The former stub entrypoint has been removed.
2. `--query` is required. No defaults exist. Every invocation must provide an explicit arXiv query string (e.g., `cat:cs.AI` or `all:"agentic workflows"`). The script exits immediately if omitted.
3. Canonical invocation (activate venv, then run):
   - `source .venv/bin/activate`
   - `python scripts/harvest_arxiv_atom.py --query 'cat:cs.AI' --max-results 25`
4. `DATAROOT` must be set, either via the `DATAROOT` environment variable or `--dataroot <path>`. If neither is present the script exits with a clear error. The repo directory is never used for run outputs.
5. Optional CLI flags: `--start <int>` (default 0, pagination offset) and `--max-results <int>` (default 25, range 1–2000). `--dataroot` overrides the env var inline.
6. Optional environment variables for polite crawling: `TVEL_USER_AGENT` (default `tvel-harvester/0.1`) and `TVEL_MAILTO`. `TVEL_MAILTO` is appended to the HTTP User-Agent as `(mailto:...)`.
7. Run artifact path schema: `$DATAROOT/tvel-harvester/arxiv/runs/<run_id>/`. `run_id` is a UTC timestamp `YYYYMMDD-HHMMSS`. A collision suffix `-01`…`-99` is appended automatically when needed.
8. Three files are written per run:
   - `raw.xml` — verbatim Atom API response
   - `items.jsonl` — one normalized JSON record per paper (`id`, `title`, `summary`, `authors`, `categories`, `links`)
   - `run.json` — full metadata (see next bullet)
9. `run.json` attribution fields recorded on every run: `git_sha`, `git_toplevel`, `host`, `user`, `argv`, `command`, `python`, `platform`, `fetched_at_utc`, `source_url`, `count`, `raw_sha256`, `items_sha256`, plus a `meta` block with resolved config (`query`, `start`, `max_results`) and raw HTTP status/headers.
10. Runs are append-only and strictly outside Git. `$DATAROOT` is never inside the repo tree. `.gitignore` excludes `.venv`, `__pycache__`, and build outputs. Harvested data is never committed by design.