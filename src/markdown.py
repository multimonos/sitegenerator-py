import unittest
import pytest


def is_title(s: str) -> bool:
    return s.startswith("# ")


def extract_title(doc: str) -> str:
    lines = doc.split("\n")

    found = list(filter(is_title, lines))

    if len(found) == 1:
        return str(found[0]).replace("# ", "")

    raise Exception("title not found")


class ExtractTitleTest(unittest.TestCase):
    def test_title_found(self):
        doc = "# foobar"
        title = extract_title(doc)
        self.assertEqual("foobar", title)

    def test_title_not_found(self):
        with pytest.raises(Exception):
            extract_title("no title here")

    def test_title_found_multiline(self):
        doc = "\n\n# foobar\nthis is a para\nok\nyoyoyo\n\n"
        title = extract_title(doc)
        self.assertEqual("foobar", title)
