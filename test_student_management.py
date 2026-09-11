import tempfile
import unittest
from pathlib import Path

from student_management import StudentManagementSystem


class StudentManagementTests(unittest.TestCase):
    def test_add_search_and_reload_from_csv(self):
        with tempfile.TemporaryDirectory() as directory:
            file_path = Path(directory) / "students.csv"
            manager = StudentManagementSystem(file_path)

            manager.add_student("Ana", 91, "S001")
            manager.add_student("Sam", "78.5", "S002")

            reloaded = StudentManagementSystem(file_path)
            self.assertEqual(reloaded.search_students("ana"), [
                {"roll_number": "S001", "name": "Ana", "marks": 91.0}
            ])
            self.assertEqual(len(reloaded.search_students("S")), 2)

    def test_delete_persists_and_duplicate_roll_numbers_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            manager = StudentManagementSystem(Path(directory) / "students.csv")
            manager.add_student("Ana", 91, "S001")

            with self.assertRaises(ValueError):
                manager.add_student("Another Ana", 80, "S001")

            manager.delete_student("S001")
            self.assertEqual(StudentManagementSystem(manager.file_path).students, {})

    def test_invalid_student_data_raises_value_error(self):
        manager = StudentManagementSystem()
        with self.assertRaises(ValueError):
            manager.add_student("", 50, "S001")
        with self.assertRaises(ValueError):
            manager.add_student("Ana", 101, "S001")


if __name__ == "__main__":
    unittest.main()