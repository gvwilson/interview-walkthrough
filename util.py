from pathlib import Path
import re


SUFFIXES_BIN = {".ico", ".jpg", ".png"}
SUFFIXES_SRC = {".css", ".html", ".js", ".md", ".py", ".sh", ".txt"}
SUFFIXES_TXT = SUFFIXES_SRC | {".csv", ".json", ".svg"}
SUFFIXES = SUFFIXES_BIN | SUFFIXES_TXT


def find_files(root):
    """Collect all interesting files."""
    return {
        filepath: read_file(filepath)
        for filepath in Path(root).glob("**/*.*")
        if _is_interesting_file(filepath)
    }


def read_file(filepath):
    """Read file as bytes or text."""
    if filepath.suffix in SUFFIXES_TXT:
        return filepath.read_text()
    else:
        return filepath.read_bytes()


def write_file(filepath, content):
    """Write file as bytes or text."""
    if filepath.suffix in SUFFIXES_TXT:
        return filepath.write_text(content)
    else:
        return filepath.write_bytes(content)


def _is_interesting_file(filepath):
    """Is this file worth checking?"""
    if not filepath.is_file():
        return False
    if str(filepath).startswith("."):
        return False
    if filepath.suffix not in SUFFIXES:
        return False
    if str(filepath.parent.name).startswith("."):
        return False
    return True
