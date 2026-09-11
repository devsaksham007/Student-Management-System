import tempfile
import unittest
from pathlib import Path

from word_counter import count_file, count_text


class WordCounterTests(unittest.TestCase):
    def test_count_text_uses_whitespace_for_words(self):
        self.assertEqual(
            count_text("Hello,  world!\nThis is a test."),
            {"words": 6, "lines": 2, "characters": 30},
        )

    def test_empty_text_has_zero_counts(self):
        self.assertEqual(count_text(""), {"words": 0, "lines": 0, "characters": 0})

    def test_count_file_reads_utf8_text(self):
        with tempfile.TemporaryDirectory() as directory:
            file_path = Path(directory) / "sample.txt"
            file_path.write_text("Café\nword", encoding="utf-8")

            self.assertEqual(
                count_file(file_path),
                {"words": 2, "lines": 2, "characters": 9},
            )


if __name__ == "__main__":
    unittest.main()