Searched for 1 pattern, read 7 files (ctrl+o to expand)                                                                 
                                                                                                                          
⏺ Here is the 10-bullet operator summary:                                                                                 
                         
  1. Only one production harvester exists today: scripts/harvest_arxiv_atom.py — fetches the arXiv Atom API and writes a  
  complete run folder. main.py is a stub (prints Python version only; not a harvester).                                   
  2. --query is required, no defaults. Every invocation must carry an explicit arXiv query string, e.g. cat:cs.AI or      
  all:"agentic workflows". The script exits immediately if omitted.                                                       
  3. Canonical invocation:
  python scripts/harvest_arxiv_atom.py --query 'cat:cs.AI' --max-results 25
  4. DATAROOT must be set — either via the DATAROOT env var or --dataroot <path>. If neither is present the script exits
  with a clear error message. No writes happen to the repo directory.
  5. Optional CLI flags: --start <int> (default 0, pagination offset) and --max-results <int> (default 25, range 1–2000).
  --dataroot overrides the env var inline.
  6. Optional env vars for polite crawling: TVEL_USER_AGENT (default tvel-harvester/0.1) and TVEL_MAILTO — appended to the
   HTTP User-Agent as (mailto:…).
  7. Run artifact path schema: $DATAROOT/tvel-harvester/arxiv/runs/<run_id>/ — run_id is a UTC timestamp YYYYMMDD-HHMMSS;
  collision suffix -01…-99 is appended automatically.
  8. Three files written per run:
    - raw.xml — verbatim Atom API response
    - items.jsonl — one normalized JSON record per paper (id, title, summary, authors, categories, links)
    - run.json — full metadata (see next bullet)
  9. run.json attribution fields recorded on every run: git_sha, git_toplevel, host, user, argv, command, python,
  platform, fetched_at_utc, source_url, count, raw_sha256, items_sha256, plus a meta block with the resolved config
  (query/start/max_results) and raw HTTP status/headers.
  10. Runs are append-only and strictly outside git. $DATAROOT is never inside the repo tree. The .gitignore excludes
  .venv, __pycache__, and build outputs; harvested data is never committed by design.