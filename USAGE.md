TVEL Harvester — arXiv (Stage 3 hardening)

Rule
Every run must be explicit about intent. No domain defaults.

Run (category)
python scripts/harvest_arxiv_atom.py --query 'cat:cs.AI' --max-results 25

Run (phrase)
python scripts/harvest_arxiv_atom.py --query 'all:"agentic workflows"' --max-results 10

Outputs
$DATAROOT/tvel-harvester/arxiv/runs/<run_id>/
- raw.xml
- items.jsonl
- run.json (includes git_sha, host, command, hashes, and resolved CLI config)
