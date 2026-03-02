# Codex commissioning note (2026-03-01)

## Run metadata (verbatim)
workdir: /Users/saendbox/work/tvel-harvester
model: gpt-5.3-codex
provider: openai
approval: never
sandbox: read-only
session id: 019cac48-8580-74b3-a4ec-41474302d95a

## Prompt (verbatim)
Read this repo and produce: (1) a 10-bullet operator summary, (2) a files-consulted list, and (3) one suggested improvement. Do not modify files. Do not run commands. Do not touch DATAROOT.

## Codex output (verbatim)
I can’t complete “read this repo” literally under your constraints because I only access workspace files by running read-only shell commands, and you explicitly prohibited all commands.

Based only on the `AGENTS.md` content you provided in-chat, here is a best-effort deliverable:

1. Operator summary (10 bullets)
- Do not commit harvested artifacts; keep them only under `DATAROOT`.
- Do not introduce new sources unless explicitly requested.
- Runtime should require explicit intent; avoid topic defaults (example: require `--query`).
- Read-only inspection is normally allowed (`ls`, `rg`, `cat`, `head`, `tail`).
- Any write action requires explicit user approval.
- Never run destructive operations (`rm`, `mv`) without explicit approval.
- Keep code changes minimal and easy to review.
- After Python edits, run `python -m compileall` on touched files.
- If run metadata changes, keep contract keys stable and preserve hashes, git SHA, argv/command, and timestamps.
- Operational references are `OPERATOR_BRIEF.md` (run steps/artifact layout) and `RUN_CONTRACT.md` (metadata contract).

2. Files consulted
- `AGENTS.md` (content provided directly in your prompt)
- Referenced (not consulted due command restriction): `OPERATOR_BRIEF.md`, `RUN_CONTRACT.md`

3. One suggested improvement
- Add a “quick-start operator checklist” section to `OPERATOR_BRIEF.md` with exact preflight checks and a minimal safe run command pattern, so operators can execute consistently without re-reading policy text.

## Operator note (added by Pauli)
Codex did not read repo files because the prompt prohibited all commands; this output reflects AGENTS.md only. Next commissioning run should allow read-only inspection commands (ls, rg, cat, head, tail) under --sandbox read-only.