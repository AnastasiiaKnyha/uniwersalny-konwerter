import sys
from pathlib import Path

from konwerter.errors import ConversionError
from konwerter.registry import execute


def main() -> None:
    # we need exactly 3 arguments
    if len(sys.argv) != 4:
        print("Użycie: python cli.py <plik> <format> <katalog>")
        print("Przykład: python cli.py samples/osoby.csv json wyniki")
        sys.exit(1)

    source = Path(sys.argv[1])
    target_format = sys.argv[2]
    output_dir = Path(sys.argv[3])

    # allow both "json" and ".json"
    if not target_format.startswith("."):
        target_format = "." + target_format

    try:
        target = execute(source, target_format, output_dir)
    except ConversionError as error:
        print(f"Błąd: {error}")
        sys.exit(1)

    print(f"Gotowe: {target}")


if __name__ == "__main__":
    main()