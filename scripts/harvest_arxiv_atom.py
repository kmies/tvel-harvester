import json
import os
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

ATOM_NS = {"a": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}
API = "https://export.arxiv.org/api/query"

def fetch(query: str, start: int = 0, max_results: int = 25) -> tuple[str, bytes]:
    params = {"search_query": query, "start": str(start), "max_results": str(max_results)}
    url = f"{API}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"User-Agent": "tvel-harvester/0.1"}, method="GET")
    with urllib.request.urlopen(req, timeout=30) as resp:
        return url, resp.read()

def parse(raw: bytes) -> list[dict]:
    root = ET.fromstring(raw)
    out = []
    for entry in root.findall("a:entry", ATOM_NS):
        def t(path):
            el = entry.find(path, ATOM_NS)
            return "" if el is None or el.text is None else " ".join(el.text.split())

        authors = []
        for a in entry.findall("a:author", ATOM_NS):
            nm = a.find("a:name", ATOM_NS)
            if nm is not None and nm.text:
                authors.append(" ".join(nm.text.split()))

        primary = None
        pc = entry.find("arxiv:primary_category", ATOM_NS)
        if pc is not None:
            primary = pc.attrib.get("term")

        cats = [c.attrib.get("term", "") for c in entry.findall("a:category", ATOM_NS)]
        cats = [c for c in cats if c]

        link_html = None
        link_pdf = None
        for link in entry.findall("a:link", ATOM_NS):
            href = link.attrib.get("href")
            rel = link.attrib.get("rel")
            typ = link.attrib.get("type")
            title_attr = link.attrib.get("title")
            if href and rel == "alternate" and typ == "text/html":
                link_html = href
            if href and (title_attr == "pdf" or typ == "application/pdf"):
                link_pdf = href

        out.append({
            "id": t("a:id"),
            "title": t("a:title"),
            "summary": t("a:summary"),
            "published": t("a:published"),
            "updated": t("a:updated"),
            "authors": authors,
            "primary_category": primary,
            "categories": cats,
            "link_html": link_html,
            "link_pdf": link_pdf,
        })
    return out

def write_run(dataroot: Path, source: str, url: str, raw: bytes, items: list[dict]) -> Path:
    run_id = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    run_dir = dataroot / "tvel-harvester" / source / "runs" / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    raw_path = run_dir / "raw.xml"
    items_path = run_dir / "items.jsonl"
    meta_path = run_dir / "run.json"

    raw_path.write_bytes(raw)
    with items_path.open("w", encoding="utf-8") as f:
        for it in items:
            f.write(json.dumps(it, ensure_ascii=False) + "\n")

    meta = {
        "run_id": run_id,
        "fetched_at_utc": datetime.now(timezone.utc).isoformat(),
        "source": source,
        "source_url": url,
        "count": len(items),
        "raw_path": str(raw_path),
        "items_path": str(items_path),
    }
    meta_path.write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return run_dir

def main() -> None:
    dataroot = Path(os.environ["DATAROOT"]).expanduser()
    query = os.environ.get("ARXIV_QUERY", 'all:"vaccine effectiveness"')
    url, raw = fetch(query)
    items = parse(raw)
    run_dir = write_run(dataroot, "arxiv", url, raw, items)
    print(f"arxiv: wrote {len(items)} items to {run_dir}")

if __name__ == "__main__":
    main()
