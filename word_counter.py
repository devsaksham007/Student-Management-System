"""Count words, lines, and characters in a text file."""

from pathlib import Path


def count_text(text):
    """Return word, line, and character counts for text."""
    return {
        "words": len(text.split()),
        "lines": len(text.splitlines()),
        "characters": len(text),
    }


def count_file(file_path):
    """Read a UTF-8 text file and return its counts."""
    text = Path(file_path).read_text(encoding="utf-8")
    return count_text(text)


def run():
    file_path = input("Enter the text file path: ").strip()

    try:
        counts = count_file(file_path)
    except FileNotFoundError:
        print("File not found.")
        return
    except OSError as error:
        print(f"Could not read file: {error}")
        return

    print(f"Words: {counts['words']}")
    print(f"Lines: {counts['lines']}")
    print(f"Characters: {counts['characters']}")


if __name__ == "__main__":
    run()