"""Export the complete publication data to a reusable CV list in Markdown."""

import argparse
from collections import Counter
from datetime import date
from pathlib import Path

import yaml


def markdown_text(value):
    for character in ["\\", "`", "*", "_", "[", "]"]:
        value = value.replace(character, "\\" + character)
    return value


def render_cv(records, source, updated):
    records = sorted(records, key=lambda record: record["sort_key"], reverse=True)
    counts = Counter(record["type"] for record in records)
    lines = [
        "# Publications", "", "Yan Wang (王炎)", "",
        f"Updated: {updated.isoformat()}", "",
        f"Latest publication record: [{source['label']}]({source['url']})", "",
        f"{len(records)} records: {counts['journal']} journal articles, "
        f"{counts['preprint']} preprints, and {counts['conference']} conference papers.", "",
    ]
    year = None
    for number, record in enumerate(records, 1):
        if record["year"] != year:
            year = record["year"]
            lines.extend([f"## {year}", ""])
        title = markdown_text(record["title"])
        authors = ", ".join(
            f"**{markdown_text(author['name'])}**" if author["is_self"] else markdown_text(author["name"])
            for author in record["authors"]
        )
        links = [f"[{label}]({record[field]})" for label, field in
                 [("DOI", "doi_url"), ("arXiv", "arxiv_url"), ("ADS", "ads_url")]
                 if record.get(field)]
        lines.extend([
            f"{number}. **{title}**", "",
            f"   {authors}", "",
            f"   {markdown_text(record['citation'])}. {record['type_label']}.", "",
            f"   Research area: {record['topic_label']}", "",
            "   " + " | ".join(links), "",
        ])
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site-root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--date", type=date.fromisoformat, default=date.today())
    parser.add_argument("--archive-bibtex", action="store_true", help="Keep a dated source snapshot")
    args = parser.parse_args()
    root = args.site_root
    records = yaml.safe_load((root / "_data/publications.yml").read_text(encoding="utf-8"))
    source = yaml.safe_load((root / "_data/publication_source.yml").read_text(encoding="utf-8"))
    if not records:
        raise ValueError("The publication list is empty")
    archive = root / "local/publications/archive" / f"publications-{args.date.isoformat()}.bib"
    bibtex = (root / "files/publications.bib").read_bytes() if args.archive_bibtex else None
    if args.archive_bibtex and archive.exists() and archive.read_bytes() != bibtex:
        raise ValueError(f"A different snapshot already exists at {archive}")
    output = root / "local/publications/cv-publications.md"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_cv(records, source, args.date), encoding="utf-8")
    if args.archive_bibtex:
        archive.parent.mkdir(parents=True, exist_ok=True)
        archive.write_bytes(bibtex)
    print(f"Exported {len(records)} records to {output}")
    if args.archive_bibtex:
        print(f"Preserved original BibTeX snapshot at {archive}")


if __name__ == "__main__":
    main()
