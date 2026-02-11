Project Charter: TVEL Harvester

Purpose
Build a reusable, auditable “harvester chassis” that can pull content from many external sources and emit durable run artifacts for downstream analysis and writing.

Non-goals
This repository does not commit harvested data. It does not hard-code any single domain, topic, or evidence program. Domain intent is supplied at run time via parameters and environment variables.

Definition of done (Stage 3 baseline)
A new source can be added by implementing only source-specific fetch + parse logic while reusing the same run folder layout and metadata contract, producing:
- raw capture
- normalized records (JSONL/CSV)
- run metadata (run.json)
under $DATAROOT/tvel-harvester/<source>/runs/<run_id>/.

Operating principles
- Runs are append-only and reproducible.
- Artifacts live in DATAROOT; code lives in git.
- Every run is attributable to a commit (git HEAD) and a timestamp.
