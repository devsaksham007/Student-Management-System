import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from json_reader import load_json, print_json


class JsonReaderTests(unittest.TestCase):
    def test_load_json_reads_utf8_data(self):
        expected = {"name": "Café", "students": ["Ana", "Sam"]}

        with tempfile.TemporaryDirectory() as directory:
            file_path = Path(directory) / "students.json"
            file_path.write_text(json.dumps(expected), encoding="utf-8")

            self.assertEqual(load_json(file_path), expected)

    def test_print_json_formats_data(self):
        output = io.StringIO()

        with redirect_stdout(output):
            print_json({"name": "Café", "active": True})

        self.assertEqual(
            output.getvalue(),
            '{\n  "name": "Café",\n  "active": true\n}\n',
        )


if __name__ == "__main__":
    unittest.main()