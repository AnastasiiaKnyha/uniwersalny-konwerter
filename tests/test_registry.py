from pathlib import Path

import pytest

from konwerter.errors import ConversionError
from konwerter.registry import available_targets, execute, validate

SAMPLES = Path(__file__).parent.parent / "samples"


def test_targets_for_csv():
    assert available_targets(Path("dane.csv")) == [".json"]


def test_targets_for_docx():
    assert available_targets(Path("dokument.docx")) == [".pdf", ".txt"]


def test_targets_ignore_letter_case():
    assert available_targets(Path("DANE.CSV")) == [".json"]


def test_no_targets_for_unknown_format():
    assert available_targets(Path("obraz.png")) == []


def test_validate_accepts_correct_choice(tmp_path):
    # no error means the choice is correct
    validate(SAMPLES / "osoby.csv", ".json", tmp_path)


def test_validate_missing_file(tmp_path):
    with pytest.raises(ConversionError, match="Nie znaleziono pliku"):
        validate(tmp_path / "brak.csv", ".json", tmp_path)


def test_validate_unsupported_pair(tmp_path):
    with pytest.raises(ConversionError, match="nie jest obsługiwana"):
        validate(SAMPLES / "osoby.csv", ".pdf", tmp_path)


def test_validate_missing_folder(tmp_path):
    with pytest.raises(ConversionError, match="katalogu docelowego"):
        validate(SAMPLES / "osoby.csv", ".json", tmp_path / "nie_ma")


def test_execute_does_not_overwrite(tmp_path):
    first = execute(SAMPLES / "osoby.csv", ".json", tmp_path)
    second = execute(SAMPLES / "osoby.csv", ".json", tmp_path)
    assert first.name == "osoby.json"
    assert second.name == "osoby_1.json"


def test_execute_overwrites_when_asked(tmp_path):
    first = execute(SAMPLES / "osoby.csv", ".json", tmp_path)
    second = execute(SAMPLES / "osoby.csv", ".json", tmp_path, overwrite=True)
    assert first == second