Run Contract (TVEL Harvester)

Goal
Each run writes a timestamped folder under DATAROOT with raw capture, normalized output, and run metadata.

Path schema
$DATAROOT/tvel-harvester/<source>/runs/<run_id>/

run_id
UTC timestamp: YYYYMMDD-HHMMSS

Required files
- raw.*         Raw response payload (format depends on source)
- items.jsonl   One JSON object per item/record (newline-delimited)
- run.json      Run metadata (single JSON object)

Minimum run.json fields
- run_id
- fetched_at_utc (ISO 8601)
- source
- source_url
- count
- raw_path
- items_path

Invariants
- Runs are append-only. Never overwrite prior runs.
- Repo stays clean. Data artifacts do not live in git.
