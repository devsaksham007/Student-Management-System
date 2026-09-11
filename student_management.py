"""Student management with CSV persistence and a small command-line interface."""

import csv
from pathlib import Path


FIELDS = ("roll_number", "name", "marks")


class StudentManagementSystem:
    """Store student records in memory and persist them to a CSV file."""

    def __init__(self, file_path="students.csv"):
        self.file_path = Path(file_path)
        self.students = {}
        self.load()

    def load(self):
        """Load records from the CSV file, if it exists."""
        self.students.clear()
        if not self.file_path.exists():
            return

        try:
            roll_numbers = set()
            with self.file_path.open(newline="", encoding="utf-8") as file:
                for row in csv.DictReader(file):
                    student = self._validate_student(
                        row.get("roll_number", ""),
                        row.get("name", ""),
                        row.get("marks", ""),
                    )
                    if student["roll_number"] in roll_numbers:
                        raise ValueError("Duplicate roll number in CSV file.")
                    roll_numbers.add(student["roll_number"])
                    self.students[student["roll_number"]] = student
        except (OSError, csv.Error) as error:
            raise ValueError(f"Could not read student file: {error}") from error

    def save(self):
        """Write all records to the CSV file."""
        try:
            self.file_path.parent.mkdir(parents=True, exist_ok=True)
            with self.file_path.open("w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=FIELDS)
                writer.writeheader()
                writer.writerows(self.students.values())
        except OSError as error:
            raise ValueError(f"Could not save student file: {error}") from error

    def add_student(self, name, marks, roll_number):
        """Add a student and persist the updated records."""
        student = self._validate_student(roll_number, name, marks)
        if student["roll_number"] in self.students:
            raise ValueError("A student with that roll number already exists.")
        self.students[student["roll_number"]] = student
        self.save()
        return student.copy()

    def delete_student(self, roll_number):
        """Delete a student by roll number and persist the change."""
        roll_number = self._clean_roll_number(roll_number)
        if roll_number not in self.students:
            raise KeyError("Student not found.")
        deleted = self.students.pop(roll_number)
        self.save()
        return deleted.copy()

    def search_students(self, query=""):
        """Return students matching a name or roll number."""
        query = str(query).strip().lower()
        return [
            student.copy()
            for student in self.students.values()
            if query in student["name"].lower()
            or query in student["roll_number"].lower()
        ]

    @staticmethod
    def _validate_student(roll_number, name, marks):
        roll_number = StudentManagementSystem._clean_roll_number(roll_number)
        name = str(name).strip()
        if not name:
            raise ValueError("Student name cannot be empty.")

        try:
            marks = float(marks)
        except (TypeError, ValueError) as error:
            raise ValueError("Marks must be a number from 0 to 100.") from error
        if not 0 <= marks <= 100:
            raise ValueError("Marks must be a number from 0 to 100.")

        return {"roll_number": roll_number, "name": name, "marks": marks}

    @staticmethod
    def _clean_roll_number(roll_number):
        roll_number = str(roll_number).strip()
        if not roll_number:
            raise ValueError("Roll number cannot be empty.")
        return roll_number


def display_students(students):
    """Print student records in a readable table."""
    if not students:
        print("No students found.")
        return
    for student in students:
        print(
            f"Roll: {student['roll_number']} | "
            f"Name: {student['name']} | Marks: {student['marks']:g}"
        )


def run():
    """Run the interactive student-management menu."""
    manager = StudentManagementSystem()
    menu = (
        "\n1. Add student\n"
        "2. Search students\n"
        "3. Delete student\n"
        "4. Show all students\n"
        "5. Exit"
    )

    while True:
        print(menu)
        choice = input("Choose an option: ").strip()
        try:
            if choice == "1":
                name = input("Name: ")
                marks = input("Marks (0-100): ")
                roll_number = input("Roll number: ")
                manager.add_student(name, marks, roll_number)
                print("Student added and saved.")
            elif choice == "2":
                display_students(manager.search_students(input("Search: ")))
            elif choice == "3":
                manager.delete_student(input("Roll number: "))
                print("Student deleted and saved.")
            elif choice == "4":
                display_students(list(manager.students.values()))
            elif choice == "5":
                print("Goodbye!")
                return
            else:
                print("Please choose a number from 1 to 5.")
        except (KeyError, ValueError) as error:
            print(error)


if __name__ == "__main__":
    run()