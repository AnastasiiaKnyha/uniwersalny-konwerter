import os
import shutil
import subprocess
import tempfile
import zipfile
from pathlib import Path

from konwerter.errors import ConversionError

# typical places where libreoffice is installed
KNOWN_PATHS = [
    "/Applications/LibreOffice.app/Contents/MacOS/soffice",
    "C:/Program Files/LibreOffice/program/soffice.exe",
    "C:/Program Files (x86)/LibreOffice/program/soffice.exe",
    "/usr/bin/soffice",
    "/usr/bin/libreoffice",
]


def find_libreoffice() -> str:
    # own path from the user, also useful for testing
    custom_path = os.environ.get("LIBREOFFICE_PATH")
    if custom_path:
        if Path(custom_path).is_file():
            return custom_path
        raise ConversionError(
            f"Nie znaleziono LibreOffice w ścieżce {custom_path}. Popraw zmienną LIBREOFFICE_PATH albo ją usuń."
        )

    # look for the program in system path
    for name in ["soffice", "libreoffice"]:
        found = shutil.which(name)
        if found:
            return found

    # look in typical install places
    for place in KNOWN_PATHS:
        if Path(place).is_file():
            return place

    raise ConversionError(
        "Nie znaleziono programu LibreOffice. Zainstaluj go ze strony https://www.libreoffice.org "
        "albo podaj ścieżkę w zmiennej LIBREOFFICE_PATH."
    )


def convert_with_libreoffice(source: Path, target: Path, target_type: str) -> None:
    # docx and odt are zip archives inside, a broken file is not
    if not zipfile.is_zipfile(source):
        raise ConversionError(
            f"Plik {source.name} jest uszkodzony albo nie jest dokumentem Word lub OpenDocument."
        )

    program = find_libreoffice()

    # libreoffice saves the result in a temp folder first
    with tempfile.TemporaryDirectory() as temp_dir:
        # arguments as a list, so no shell is used
        command = [program, "--headless", "--convert-to", target_type, "--outdir", temp_dir, str(source)]

        try:
            result = subprocess.run(command, capture_output=True, text=True, timeout=120)
        except subprocess.TimeoutExpired:
            raise ConversionError("LibreOffice działał zbyt długo i został zatrzymany. Spróbuj z mniejszym plikiem.")

        # 0 means success, other number means error
        if result.returncode != 0:
            raise ConversionError(
                f"LibreOffice zakończył się błędem (kod {result.returncode}). {result.stderr.strip()}"
            )

        # libreoffice names the file like the source, only with new extension
        created = Path(temp_dir) / (source.stem + "." + target_type)
        if not created.exists():
            raise ConversionError(
                "LibreOffice nie utworzył pliku wynikowego. Sprawdź, czy plik nie jest uszkodzony, "
                "i zamknij LibreOffice, jeśli jest otwarty."
            )

        # move the result to the folder chosen by the user
        shutil.move(str(created), str(target))


def docx_to_pdf(source: Path, target: Path) -> None:
    convert_with_libreoffice(source, target, "pdf")


def odt_to_pdf(source: Path, target: Path) -> None:
    convert_with_libreoffice(source, target, "pdf")