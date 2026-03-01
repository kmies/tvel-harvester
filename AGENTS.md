TVEL Harvester — agent instructions (Codex/others)

Repository invariants
- Never commit harvested artifacts. Artifacts live only under DATAROOT.
- Do not add new sources unless explicitly requested.
- No topic defaults. Runtime must require explicit intent (e.g., --query).

Allowed actions by default
- Read-only inspection is allowed (ls, rg, cat, head/tail).
- Any write requires explicit user approval.
- Never run destructive commands (rm/mv) without explicit approval.

Quality gates for code changes
- Keep changes minimal and reviewable.
- After Python edits: python -m compileall on the touched files.
- If run metadata changes: keep keys stable; keep hashes, git SHA, argv/command, and timestamps correct.

Repo references
- OPERATOR_BRIEF.md for run steps and artifact layout.
- RUN_CONTRACT.md for the metadata contract.