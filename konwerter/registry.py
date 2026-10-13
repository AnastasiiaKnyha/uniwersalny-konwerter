import os
from pathlib import Path

from konwerter.data import csv_to_json, json_to_csv
from konwerter.errors import ConversionError

# (source format, target format) -> function that converts
# to add a new pair just add one line here
REGISTRY = {
    (".csv", ".json"): csv_to_json,
    (".json", ".csv"): json_to_csv,
}


def available_targets(source: Path) -> list[str]:
    source_format = source.suffix.lower()
    targets = []
    for pair in REGISTRY:
        if pair[0] == source_format:
            targets.append(pair[1])
    return sorted(targets)


def validate(source: Path, target_format: str, output_dir: Path) -> None:
    if not source.is_file():
        raise ConversionError(f"Nie znaleziono pliku wejściowego: {source}. Wybierz istniejący plik.")

    if len(available_targets(source)) == 0:
        raise ConversionError(f"Format \"{source.suffix}\" nie jest obsługiwany. Wybierz inny plik.")

    pair = (source.suffix.lower(), target_format.lower())
    if pair not in REGISTRY:
        raise ConversionError(f"Konwersja {pair[0]} → {pair[1]} nie jest obsługiwana.")

    if not output_dir.is_dir():
        raise ConversionError(f"Nie znaleziono katalogu docelowego: {output_dir}. Wybierz istniejący katalog.")

    if not os.access(output_dir, os.W_OK):
        raise ConversionError(f"Brak uprawnień do zapisu w katalogu {output_dir}. Wybierz inny katalog.")


def make_target_path(source: Path, target_format: str, output_dir: Path, overwrite: bool) -> Path:
    target = output_dir / (source.stem + target_format)
    if overwrite:
        return target

    # file exists, so try name_1, name_2 and so on
    number = 1
    while target.exists():
        target = output_dir / f"{source.stem}_{number}{target_format}"
        number += 1
    return target


def execute(source: Path, target_format: str, output_dir: Path, overwrite: bool = False) -> Path:
    target_format = target_format.lower()
    validate(source, target_format, output_dir)

    target = make_target_path(source, target_format, output_dir, overwrite)
    convert = REGISTRY[(source.suffix.lower(), target_format)]
    convert(source, target)
    return target