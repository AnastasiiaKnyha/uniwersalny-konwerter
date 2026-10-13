import csv
import json
from pathlib import Path

from konwerter.errors import ConversionError


def csv_to_json(source: Path, target: Path) -> None:
    # read the whole file first, write only when everything is ok
    try:
        # utf-8-sig also understands the bom that excel adds
        with open(source, encoding="utf-8-sig", newline="") as file:
            rows = list(csv.reader(file))
    except UnicodeDecodeError:
        raise ConversionError("Plik nie jest zapisany w kodowaniu UTF-8. Zapisz go jako UTF-8 i spróbuj ponownie.")
    except csv.Error as error:
        raise ConversionError(f"Plik CSV jest uszkodzony: {error}")

    if len(rows) == 0:
        raise ConversionError("Plik CSV jest pusty. Pierwszy wiersz musi zawierać nagłówki kolumn.")

    # first row is the header
    header = rows[0]
    if len(set(header)) != len(header):
        raise ConversionError("Nagłówki kolumn w pliku CSV powtarzają się. Nadaj kolumnom unikalne nazwy.")

    records = []
    # start=2 because row 1 is the header
    for number, row in enumerate(rows[1:], start=2):
        # skip empty lines
        if len(row) == 0:
            continue
        if len(row) != len(header):
            raise ConversionError(
                f"Wiersz {number} ma {len(row)} kolumn, a nagłówek ma {len(header)}. Popraw plik CSV."
            )
        # pair each header with its value
        record = dict(zip(header, row))
        records.append(record)

    # ensure_ascii=False keeps polish letters readable
    with open(target, "w", encoding="utf-8") as file:
        json.dump(records, file, ensure_ascii=False, indent=2)


def json_to_csv(source: Path, target: Path) -> None:
    # read the whole file first, write only when everything is ok
    try:
        with open(source, encoding="utf-8-sig") as file:
            data = json.load(file)
    except UnicodeDecodeError:
        raise ConversionError("Plik nie jest zapisany w kodowaniu UTF-8. Zapisz go jako UTF-8 i spróbuj ponownie.")
    except json.JSONDecodeError as error:
        raise ConversionError(
            f"Plik JSON jest uszkodzony (linia {error.lineno}, kolumna {error.colno}). Sprawdź jego składnię."
        )

    # we accept only a list of objects
    if not isinstance(data, list) or len(data) == 0:
        raise ConversionError("Plik JSON musi zawierać niepustą listę obiektów, np. [{\"imię\": \"Anna\"}].")

    # collect column names in the order they appear
    columns = []
    for number, item in enumerate(data, start=1):
        if not isinstance(item, dict):
            raise ConversionError(f"Element nr {number} w pliku JSON nie jest obiektem.")
        for key, value in item.items():
            if isinstance(value, (dict, list)):
                raise ConversionError(
                    f"Pole \"{key}\" w elemencie nr {number} jest zagnieżdżone. Obsługiwane są tylko proste wartości."
                )
            if key not in columns:
                columns.append(key)

    # bom helps excel show polish letters
    with open(target, "w", encoding="utf-8-sig", newline="") as file:
        # missing values become empty cells
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        for item in data:
            writer.writerow(item)