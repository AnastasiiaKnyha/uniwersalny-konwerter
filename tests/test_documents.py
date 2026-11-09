from pathlib import Path

import pytest
from docx import Document

from konwerter.errors import ConversionError
from konwerter.office import docx_to_pdf, find_libreoffice
from konwerter.text import docx_to_txt, txt_to_docx

SAMPLES = Path(__file__).parent.parent / "samples"


def libreoffice_installed() -> bool:
    try:
        find_libreoffice()
        return True
    except ConversionError:
        return False


def test_txt_to_docx_makes_paragraphs(tmp_path):
    target = tmp_path / "notatka.docx"
    txt_to_docx(SAMPLES / "notatka.txt", target)

    paragraphs = Document(target).paragraphs
    assert len(paragraphs) == 3
    assert "zażółć gęślą jaźń" in paragraphs[1].text


def test_txt_docx_txt_gives_the_same_text(tmp_path):
    docx_file = tmp_path / "notatka.docx"
    txt_file = tmp_path / "notatka.txt"
    txt_to_docx(SAMPLES / "notatka.txt", docx_file)
    docx_to_txt(docx_file, txt_file)

    original = (SAMPLES / "notatka.txt").read_text(encoding="utf-8").strip()
    result = txt_file.read_text(encoding="utf-8").strip()
    assert result == original


def test_broken_docx_to_txt(tmp_path):
    with pytest.raises(ConversionError, match="uszkodzony"):
        docx_to_txt(SAMPLES / "uszkodzony.docx", tmp_path / "wynik.txt")


def test_broken_docx_to_pdf(tmp_path):
    with pytest.raises(ConversionError, match="uszkodzony"):
        docx_to_pdf(SAMPLES / "uszkodzony.docx", tmp_path / "wynik.pdf")


def test_missing_libreoffice(tmp_path, monkeypatch):
    # wrong path only for this test
    monkeypatch.setenv("LIBREOFFICE_PATH", "/nie/ma/libreoffice")
    with pytest.raises(ConversionError, match="Nie znaleziono LibreOffice"):
        docx_to_pdf(SAMPLES / "notatka.docx", tmp_path / "wynik.pdf")


@pytest.mark.skipif(not libreoffice_installed(), reason="LibreOffice nie jest zainstalowany")
def test_docx_to_pdf(tmp_path):
    target = tmp_path / "notatka.pdf"
    docx_to_pdf(SAMPLES / "notatka.docx", target)

    # every pdf file starts with %PDF
    assert target.read_bytes().startswith(b"%PDF")