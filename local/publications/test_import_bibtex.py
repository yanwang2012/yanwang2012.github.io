import tempfile
from pathlib import Path
import unittest

from import_bibtex import import_records, names


SAMPLE = r"""@article{example,
  author = {{Wang}, Yan and {V{\'a}zquez-Aceves}, Ver{\'o}nica},
  title = {An example {LISA} study},
  journal = {\prd},
  month = jul,
  year = {2026},
  doi = {10.1234/example},
  volume = {114},
  pages = {023005}
}"""
CONFIG = {"topics": [{"id": "space", "label": "Space-Based Gravitational-Wave Detection"}],
          "assignments": {"example": "space", "second": "space"}}


class ImportTests(unittest.TestCase):
    def records(self, source, config=CONFIG):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "example.bib"
            path.write_text(source, encoding="utf-8")
            return import_records(path, config)

    def test_month_macro_journal_and_accents(self):
        record = self.records(SAMPLE)[0]
        self.assertEqual(record["month"], 7)
        self.assertEqual(record["venue"], "Physical Review D")
        self.assertEqual(record["authors"][1]["name"], "Verónica Vázquez-Aceves")
        self.assertTrue(record["authors"][0]["is_self"])
        self.assertEqual(record["title"], "An example LISA study")

    def test_preprint_is_not_a_journal_article(self):
        source = SAMPLE.replace(r"{\prd}", "{arXiv e-prints}")
        record = self.records(source)[0]
        self.assertEqual(record["type"], "preprint")
        self.assertEqual(record["type_label"], "Preprint")

    def test_conference_record(self):
        record = self.records(SAMPLE.replace("@article", "@inproceedings"))[0]
        self.assertEqual(record["type"], "conference")

    def test_missing_month_does_not_invent_one(self):
        record = self.records(SAMPLE.replace("month = jul,", ""))[0]
        self.assertEqual(record["month"], 0)

    def test_duplicate_doi_rejected(self):
        with self.assertRaisesRegex(ValueError, "Duplicate DOI"):
            self.records(SAMPLE + SAMPLE.replace("{example,", "{second,").replace("An example", "A different"))

    def test_duplicate_key_rejected(self):
        with self.assertRaisesRegex(ValueError, "Duplicate BibTeX key"):
            self.records(SAMPLE + SAMPLE)

    def test_missing_topic_rejected(self):
        with self.assertRaisesRegex(ValueError, "Add a research topic"):
            self.records(SAMPLE, {"topics": CONFIG["topics"], "assignments": {}})

    def test_known_inverted_author_fields(self):
        self.assertEqual(names({"ID": "2026SSPMA..5619503Y"}),
                         ["Yi-Qian Qian", "Xuan Tao", "Siyuan Chen", "Yan Wang"])


if __name__ == "__main__":
    unittest.main()
