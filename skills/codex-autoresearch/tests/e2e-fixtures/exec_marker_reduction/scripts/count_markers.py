#!/usr/bin/env python3
from pathlib import Path


def main() -> None:
    app = Path(__file__).resolve().parents[1] / "src" / "app.py"
    print(app.read_text(encoding="utf-8").count("TODO_REMOVE"))


if __name__ == "__main__":
    main()
