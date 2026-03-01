TVEL Harvester — Claude Code rules

Scope
- Work only inside this repo unless the user explicitly requests otherwise.
- Code lives in git. Run artifacts live in DATAROOT. Never write artifacts into git.
- Keep the repo domain-neutral. No topic defaults. Require explicit --query (or equivalent) at runtime.

Non-negotiables
- Preserve the run artifact contract: $DATAROOT/tvel-harvester/<source>/runs/<run_id>/ with run.json + raw capture + normalized records.
- run.json must remain strict, reproducible, and attributable (git SHA, argv/command, timestamps, checksums).
- Do not touch or commit DATAROOT contents. .venv and build outputs stay uncommitted.

Workflow
- Prefer small diffs. Explain intent before changing code.
- After Python changes: run python -m compileall on changed modules/scripts.
- Verify file locations after creation with ls.

Repo references
- Run contract: RUN_CONTRACT.md
- Usage: USAGE.md
- Operator overview: OPERATOR_BRIEF.md