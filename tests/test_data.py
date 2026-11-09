import json
from pathlib import Path

import pytest

from konwerter.data import csv_to_json, json_to_csv
from konwerter.errors import ConversionError

SAMPLES = Path(__file__).parent.parent / "samples"


def test_csv_to_json_keeps_polish_letters_and_empty_values(tmp_path):
    target = tmp_path / "osoby.json"
    csv_to_json(SAMPLES / "osoby.csv", target)

    records = json.loads(target.read_text(encoding="utf-8"))
    assert len(records) == 3
    assert records[0]["miasto"] == "Łódź"
    assert records[0]["uwagi"] == ""
    assert records[1]["uwagi"] == "lubi kawę, herbatę"


def test_csv_to_json_keeps_column_order(tmp_path):
    target = tmp_path / "osoby.json"
    csv_to_json(SAMPLES / "osoby.csv", target)

    records = json.loads(target.read_text(encoding="utf-8"))
    assert list(records[0].keys()) == ["imię", "nazwisko", "miasto", "wiek", "uwagi"]


def test_csv_json_csv_gives_the_same_data(tmp_path):
    json_file = tmp_path / "osoby.json"
    csv_file = tmp_path / "osoby.csv"
    csv_to_json(SAMPLES / "osoby.csv", json_file)
    json_to_csv(json_file, csv_file)

    # compare text without bom and line endings
    original = (SAMPLES / "osoby.csv").read_text(encoding="utf-8-sig").splitlines()
    result = csv_file.read_text(encoding="utf-8-sig").splitlines()
    assert result == original


def test_json_to_csv_fills_missing_fields_with_empty_cells(tmp_path):
    target = tmp_path / "produkty.csv"
    json_to_csv(SAMPLES / "produkty.json", target)

    lines = target.read_text(encoding="utf-8-sig").splitlines()
    assert lines[0] == "produkt,cena,kraj,uwagi"
    assert lines[2] == "Gruszki,,,"


def test_broken_json_gives_clear_error(tmp_path):
    with pytest.raises(ConversionError, match="uszkodzony"):
        json_to_csv(SAMPLES / "uszkodzony.json", tmp_path / "wynik.csv")


def test_csv_with_wrong_number_of_columns(tmp_path):
    source = tmp_path / "zly.csv"
    source.write_text("a,b\n1,2,3\n", encoding="utf-8")
    with pytest.raises(ConversionError, match="Wiersz 2"):
        csv_to_json(source, tmp_path / "wynik.json")


def test_empty_csv(tmp_path):
    source = tmp_path / "pusty.csv"
    source.write_text("", encoding="utf-8")
    with pytest.raises(ConversionError, match="pusty"):
        csv_to_json(source, tmp_path / "wynik.json")