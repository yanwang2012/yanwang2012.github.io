"""Import ADS BibTeX into the data used by the Publications page."""

import argparse
from collections import Counter
from pathlib import Path
import re

import bibtexparser
from bibtexparser.customization import author
from pylatexenc.latex2text import LatexNodes2Text
import yaml


MONTHS = {name: i for i, name in enumerate(
    "jan feb mar apr may jun jul aug sep oct nov dec".split(), 1
)}
JOURNALS = {
    r"\prd": "Physical Review D",
    r"\prl": "Physical Review Letters",
    r"\apj": "The Astrophysical Journal",
    r"\apjl": "The Astrophysical Journal Letters",
    r"\mnras": "Monthly Notices of the Royal Astronomical Society",
    r"\pasa": "Publications of the Astronomical Society of Australia",
}
TYPE_LABELS = {
    "journal": "Journal article",
    "preprint": "Preprint",
    "conference": "Conference paper",
}
# These ADS records invert given and family names in their exported author fields.
AUTHOR_OVERRIDES = {
    "2026SSPMA..5619503Y": ["Yi-Qian Qian", "Xuan Tao", "Siyuan Chen", "Yan Wang"],
    "2026SSPMA..5619506Z": ["Zi-Hao Chen", "Yan Wang", "Jianping Yuan"],
}
LATEX = LatexNodes2Text()


def plain(value):
    return " ".join(LATEX.latex_to_text(value).split())


def names(entry):
    if entry["ID"] in AUTHOR_OVERRIDES:
        return AUTHOR_OVERRIDES[entry["ID"]]
    output = []
    for name in author({"author": entry["author"]})["author"]:
        family, _, given = name.partition(",")
        family, given = plain(family), plain(given)
        if family == "al." and given == "et":
            output.append("et al.")
        else:
            output.append(" ".join(part for part in [given, family] if part))
    return output


def import_records(source, topic_config):
    parser = bibtexparser.bparser.BibTexParser(common_strings=True)
    database = bibtexparser.loads(source.read_text(encoding="utf-8"), parser=parser)
    topics = {topic["id"]: topic["label"] for topic in topic_config["topics"]}
    assignments = topic_config["assignments"]
    records, seen, seen_dois, seen_titles = [], set(), set(), set()
    for entry in database.entries:
        key = entry["ID"]
        if key in seen:
            raise ValueError(f"Duplicate BibTeX key: {key}")
        seen.add(key)
        if key not in assignments:
            raise ValueError(f"Add a research topic for {key} in topics.yml")
        topic = assignments[key]
        if topic not in topics:
            raise ValueError(f"Unknown research topic for {key}: {topic}")
        title = plain(entry["title"])
        title_key = re.sub(r"\W+", "", title).casefold()
        if title_key in seen_titles:
            raise ValueError(f"Possible duplicate title: {title}")
        seen_titles.add(title_key)
        doi = entry.get("doi", "").strip()
        if doi and doi.casefold() in seen_dois:
            raise ValueError(f"Duplicate DOI: {doi}")
        if doi:
            seen_dois.add(doi.casefold())
        year = int(entry["year"])
        month_value = str(entry.get("month", "")).lower()
        month = MONTHS.get(month_value[:3], 0)
        if month_value.isdigit() and 1 <= int(month_value) <= 12:
            month = int(month_value)
        venue = entry.get("journal", entry.get("booktitle", ""))
        kind = "conference" if entry["ENTRYTYPE"] == "inproceedings" else "journal"
        if venue.casefold() == "arxiv e-prints":
            kind = "preprint"
        venue = JOURNALS[venue] if venue in JOURNALS else plain(venue)
        pages = plain(entry.get("pages", ""))
        arxiv = entry.get("eprint", "")
        if kind == "preprint" and pages.startswith("arXiv:"):
            pages = ""
        citation_parts = [venue]
        if entry.get("volume"):
            citation_parts.append(plain(entry["volume"]))
        if pages or entry.get("eid"):
            identifier = pages or plain(entry["eid"])
            if not identifier.startswith("arXiv:"):
                citation_parts.append(identifier)
        citation_parts.append(f"({year})")
        records.append({
            "id": key,
            "title": title,
            "authors": [{"name": n, "is_self": n == "Yan Wang"} for n in names(entry)],
            "year": year,
            "month": month,
            "sort_key": f"{year:04d}-{month:02d}-{key}",
            "type": kind,
            "type_label": TYPE_LABELS[kind],
            "topic": topic,
            "topic_label": topics[topic],
            "venue": venue,
            "citation": ", ".join(citation_parts[:-1]) + " " + citation_parts[-1],
            "doi": doi,
            "doi_url": "https://doi.org/" + doi if doi else "",
            "arxiv_url": "https://arxiv.org/abs/" + arxiv if arxiv else "",
            "ads_url": entry.get("adsurl", ""),
        })
    if not records:
        raise ValueError("No bibliography entries found")
    return sorted(records, key=lambda r: r["sort_key"], reverse=True)


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("source", type=Path, help="ADS-exported BibTeX file")
    cli.add_argument("--site-root", type=Path, default=Path(__file__).resolve().parents[2])
    args = cli.parse_args()
    config = yaml.safe_load(Path(__file__).with_name("topics.yml").read_text(encoding="utf-8"))
    records = import_records(args.source, config)
    root = args.site_root
    for directory in [root / "_data", root / "files"]:
        directory.mkdir(parents=True, exist_ok=True)
    (root / "_data/publications.yml").write_text(
        "# Publications data. See local/publications/README.md for maintenance.\n" +
        yaml.safe_dump(records, allow_unicode=True, sort_keys=False, width=110), encoding="utf-8"
    )
    (root / "_data/publication_topics.yml").write_text(
        yaml.safe_dump(config["topics"], allow_unicode=True, sort_keys=False), encoding="utf-8"
    )
    target_bib = root / "files/publications.bib"
    if args.source.resolve() != target_bib.resolve():
        target_bib.write_bytes(args.source.read_bytes())
    print(f"Imported {len(records)} records: {dict(Counter(r['type'] for r in records))}")
    print(f"Research topics: {dict(Counter(r['topic_label'] for r in records))}")


if __name__ == "__main__":
    main()
