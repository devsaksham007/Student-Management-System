"""Load JSON data from a file and print it in a readable format."""

import json
from pathlib import Path


def load_json(file_path):
    """Read and return JSON data from a UTF-8 file."""
    with Path(file_path).open(encoding="utf-8") as file:
        return json.load(file)


def print_json(data):
    """Print JSON data with readable indentation."""
    print(json.dumps(data, indent=2, ensure_ascii=False))


def run():
    """Read a JSON file path and print its contents."""
    file_path = input("Enter the JSON file path: ").strip()

    try:
        data = load_json(file_path)
    except FileNotFoundError:
        print("File not found.")
        return
    except json.JSONDecodeError as error:
        print(f"Invalid JSON: {error}")
        return
    except OSError as error:
        print(f"Could not read file: {error}")
        return

    print_json(data)


if __name__ == "__main__":
    run()