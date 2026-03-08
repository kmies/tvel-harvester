# Operator Brief: arXiv Harvester

## Scope
This repo’s Stage 3 contract is: run-specific artifacts go to DATAROOT; code stays in git; runs are append-only and attributable.

## 1) How to run the arXiv harvester
1. Use Python 3.12+.
2. Provide a query explicitly (--query is required; no domain defaults).
3. Set DATAROOT in the environment, or pass --dataroot.
4. Run one of the canonical commands:

python scripts/harvest_arxiv_atom.py --query 'cat:cs.AI' --max-results 25
python scripts/harvest_arxiv_atom.py --query 'all:"agentic workflows"' --max-results 10

5. Optional controls:
- --start (default 0)
- --max-results (must be 1..2000, default 25)
- --dataroot (overrides env var)
- TVEL_USER_AGENT and TVEL_MAILTO (used in request User-Agent)

If DATAROOT is missing and --dataroot is not supplied, the script exits with:
DATAROOT is not set. Export DATAROOT or pass --dataroot.

## 2) Where artifacts land under DATAROOT
1. Base run path schema:
- $DATAROOT/tvel-harvester/<source>/runs/<run_id>/

2. For arXiv specifically:
- $DATAROOT/tvel-harvester/arxiv/runs/<run_id>/

3. run_id format:
- UTC timestamp YYYYMMDD-HHMMSS
- If collision occurs, allocator appends -01 … -99

4. Required run files:
- raw.xml (raw Atom payload)
- items.jsonl (normalized one-record-per-line output)
- run.json (run metadata)

5. run.json includes at least contract fields plus operational metadata such as:
- run_id, fetched_at_utc, source, source_url, count
- paths (raw_path, items_path)
- checksums (raw_sha256, items_sha256)
- attribution (git_sha, command, argv, host/user, python/platform)
- resolved config and HTTP details under meta

## 3) What must never be committed
1. Harvested data artifacts under DATAROOT (all run folders and contents, including raw.*, items.jsonl, run.json).
2. Any generated run outputs from this harvester in general (project principle: “Artifacts live in DATAROOT; code lives in git”).
3. Standard local Python build/runtime byproducts already ignored:
- __pycache__/, *.py[oc], build/, dist/, wheels/, *.egg-info, .venv

## Files consulted (exact)
- /Users/saendbox/work/tvel-harvester/USAGE.md
- /Users/saendbox/work/tvel-harvester/RUN_CONTRACT.md
- /Users/saendbox/work/tvel-harvester/tvel_harvester/run.py
- /Users/saendbox/work/tvel-harvester/PROJECT_CHARTER.md
- /Users/saendbox/work/tvel-harvester/.gitignore
- /Users/saendbox/work/tvel-harvester/pyproject.toml
- /Users/saendbox/work/tvel-harvester/scripts/harvest_arxiv_atom.py
- /Users/saendbox/work/tvel-harvester/README.md