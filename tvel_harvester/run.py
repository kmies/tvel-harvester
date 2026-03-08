import getpass
import hashlib
import json
import platform
import shlex
import socket
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Optional


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def utc_run_id() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")


def git_head_sha(repo_root: Optional[Path] = None) -> Optional[str]:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=str(repo_root) if repo_root else None,
            text=True,
        ).strip()
    except Exception:
        return None


def git_toplevel(repo_root: Optional[Path] = None) -> Optional[str]:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=str(repo_root) if repo_root else None,
            text=True,
        ).strip()
    except Exception:
        return None


@dataclass(frozen=True)
class RunPaths:
    run_dir: Path
    raw_path: Path
    items_path: Path
    meta_path: Path


def quote_command(argv: list[str]) -> str:
    return " ".join(shlex.quote(a) for a in argv)


def allocate_run_dir(dataroot: Path, source: str, run_id: str) -> Path:
    base = dataroot / "tvel-harvester" / source / "runs" / run_id
    if not base.exists():
        return base
    for i in range(1, 100):
        cand = dataroot / "tvel-harvester" / source / "runs" / f"{run_id}-{i:02d}"
        if not cand.exists():
            return cand
    raise RuntimeError("Could not allocate unique run directory after 99 attempts")


def build_run_paths(dataroot: Path, source: str, run_id: str, raw_ext: str) -> RunPaths:
    run_dir = allocate_run_dir(dataroot, source, run_id)
    raw_path = run_dir / f"raw{raw_ext}"
    items_path = run_dir / "items.jsonl"
    meta_path = run_dir / "run.json"
    return RunPaths(run_dir=run_dir, raw_path=raw_path, items_path=items_path, meta_path=meta_path)


def write_run(
    *,
    dataroot: Path,
    source: str,
    source_url: str,
    raw_bytes: bytes,
    raw_ext: str,
    items: Iterable[dict[str, Any]],
    argv: list[str],
    extra_meta: dict[str, Any],
    repo_root: Optional[Path] = None,
) -> RunPaths:
    run_id = utc_run_id()
    paths = build_run_paths(dataroot, source, run_id, raw_ext)

    paths.run_dir.mkdir(parents=True, exist_ok=False)

    raw_sha256 = hashlib.sha256(raw_bytes).hexdigest()
    paths.raw_path.write_bytes(raw_bytes)

    count = 0
    items_hasher = hashlib.sha256()
    with paths.items_path.open("w", encoding="utf-8") as f:
        for it in items:
            line = json.dumps(it, ensure_ascii=False) + "\n"
            f.write(line)
            items_hasher.update(line.encode("utf-8"))
            count += 1

    meta: dict[str, Any] = {
        "run_id": paths.run_dir.name,
        "fetched_at_utc": utc_now_iso(),
        "source": source,
        "source_url": source_url,
        "count": count,
        "raw_path": str(paths.raw_path),
        "items_path": str(paths.items_path),
        "raw_sha256": raw_sha256,
        "items_sha256": items_hasher.hexdigest(),
        "git_sha": git_head_sha(repo_root),
        "git_toplevel": git_toplevel(repo_root),
        "host": socket.gethostname(),
        "user": getpass.getuser(),
        "argv": argv,
        "command": quote_command(argv),
        "python": platform.python_version(),
        "platform": platform.platform(),
        "meta": extra_meta,
    }

    paths.meta_path.write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return paths
