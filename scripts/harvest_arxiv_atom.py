import argparse
import os
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from tvel_harvester.run import write_run  # noqa: E402

ATOM_NS = {"a": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}
API = "https://export.arxiv.org/api/query"


def build_user_agent() -> str:
    base = os.environ.get("TVEL_USER_AGENT", "tvel-harvester/0.1")
    mailto = os.environ.get("TVEL_MAILTO")
    if mailto:
        return f"{base} (mailto:{mailto})"
    return base


def fetch_atom(query: str, start: int, max_results: int, timeout_s: int = 30) -> tuple[str, int, dict[str, str], bytes]:
    params = {"search_query": query, "start": str(start), "max_results": str(max_results)}
    url = f"{API}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"User-Agent": build_user_agent()}, method="GET")
    with urllib.request.urlopen(req, timeout=timeout_s) as resp:
        status = getattr(resp, "status", 200)
        headers = {k: v for k, v in resp.headers.items()}
        raw = resp.read()
        return url, status, headers, raw


def parse_atom(raw: bytes) -> list[dict[str, Any]]:
    root = ET.fromstring(raw)
    out: list[dict[str, Any]] = []

    for entry in root.findall("a:entry", ATOM_NS):

        def t(path: str) -> str:
            el = entry.find(path, ATOM_NS)
            if el is None or el.text is None:
                return ""
            return " ".join(el.text.split())

        authors: list[str] = []
        for a in entry.findall("a:author", ATOM_NS):
            nm = a.find("a:name", ATOM_NS)
            if nm is not None and nm.text:
                authors.append(" ".join(nm.text.split()))

        primary_category = None
        primary_cat_el = entry.find("arxiv:primary_category", ATOM_NS)
        if primary_cat_el is not None:
            primary_category = primary_cat_el.attrib.get("term") or None

        categories = [c.attrib.get("term", "") for c in entry.findall("a:category", ATOM_NS)]
        categories = [c for c in categories if c]

        link_html = None
        link_pdf = None
        for link in entry.findall("a:link", ATOM_NS):
            href = link.attrib.get("href")
            rel = link.attrib.get("rel")
            typ = link.attrib.get("type")
            title_attr = link.attrib.get("title")
            if href and rel == "alternate" and typ == "text/html":
                link_html = href
            if href and title_attr == "pdf":
                link_pdf = href

        out.append(
            {
                "id": t("a:id"),
                "title": t("a:title"),
                "summary": t("a:summary"),
                "published": t("a:published"),
                "updated": t("a:updated"),
                "authors": authors,
                "primary_category": primary_category,
                "categories": categories,
                "link_html": link_html,
                "link_pdf": link_pdf,
            }
        )

    return out


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        prog="harvest_arxiv_atom",
        description="Fetch arXiv Atom results and write a run folder under DATAROOT.",
    )
    p.add_argument("--query", required=True, help='arXiv API search_query (e.g., cat:cs.AI or all:"agentic workflows")')
    p.add_argument("--start", type=int, default=0)
    p.add_argument("--max-results", type=int, default=25)
    p.add_argument("--dataroot", default=None, help="override DATAROOT env var (optional)")
    return p.parse_args()


def main() -> int:
    args = parse_args()

    if args.start < 0:
        raise SystemExit("--start must be >= 0")
    if args.max_results <= 0 or args.max_results > 2000:
        raise SystemExit("--max-results must be in 1..2000")

    dataroot_val = args.dataroot or os.environ.get("DATAROOT")
    if not dataroot_val:
        raise SystemExit("DATAROOT is not set. Export DATAROOT or pass --dataroot.")
    dataroot = Path(dataroot_val).expanduser()

    url, status, headers, raw = fetch_atom(args.query, args.start, args.max_results)
    items = parse_atom(raw)

    extra_meta = {
        "config": {
            "query": args.query,
            "start": args.start,
            "max_results": args.max_results,
        },
        "http": {
            "status": status,
            "headers": headers,
        },
        "user_agent": build_user_agent(),
    }

    paths = write_run(
        dataroot=dataroot,
        source="arxiv",
        source_url=url,
        raw_bytes=raw,
        raw_ext=".xml",
        items=items,
        argv=list(sys.argv),
        extra_meta=extra_meta,
        repo_root=REPO_ROOT,
    )

    print(f"arxiv: wrote {len(items)} items to {paths.run_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
