# Uniwersalny konwerter plików

Projekt na Programowanie V.
Autorka Anastasiia Knyha, nr albumu 106230

Program zamienia pliki z jednego formatu na inny. Jest napisany w Pythonie, a na końcu będzie miał okienko w Tkinterze.

## Co program umie

| Z | Na | Status | Ograniczenia |
|---|---|---|---|
| CSV | JSON | działa | wszystkie wartości zapisują się jako tekst |
| JSON | CSV | działa | tylko lista obiektów bez zagnieżdżonych pól |
| TXT | DOCX | działa | pusta linia oznacza nowy akapit, tekst jest bez formatowania |
| DOCX | TXT | działa | zostaje tylko tekst akapitów, bez tabel, obrazków i formatowania |
| DOCX | PDF | działa | potrzebny LibreOffice, wygląd może się trochę różnić od Worda |
| ODT | PDF | działa | potrzebny LibreOffice |

## Czego potrzebuje program

- Python 3.9 lub nowszy
- biblioteka python-docx, jest w pliku requirements.txt
- LibreOffice, potrzebny tylko do zamiany na PDF

## Instalacja

Najpierw zainstaluj LibreOffice ze strony https://www.libreoffice.org

Potem w folderze projektu wpisz w terminalu

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Na Windowsie zamiast drugiej linii wpisz `.venv\Scripts\activate`.

Program sam szuka LibreOffice w typowych miejscach na macOS, Windowsie i Linuxie. Jeśli go nie znajdzie, można podać ścieżkę w zmiennej LIBREOFFICE_PATH, na przykład na Macu

```
export LIBREOFFICE_PATH="/Applications/LibreOffice.app/Contents/MacOS/soffice"
```

## Jak uruchomić

Na razie program działa z terminala

```
python3 cli.py <plik> <format> <folder>
```

Przykłady

```
python3 cli.py samples/osoby.csv json wyniki
python3 cli.py samples/notatka.docx pdf wyniki
```

Wynik zapisuje się we wskazanym folderze. Jeśli taki plik już istnieje, program nie nadpisuje go, tylko dodaje numer do nazwy, np. `osoby_1.json`.

## Jak działają konwersje

CSV i JSON
- Pliki muszą być w kodowaniu UTF-8.
- W CSV pierwszy wiersz to nazwy kolumn, a wartości są oddzielone przecinkami.
- JSON musi być listą obiektów, na przykład `[{"imię": "Anna", "wiek": 20}]`.
- Puste pola zostają puste, a kolejność kolumn się nie zmienia.

TXT i DOCX
- Pusta linia w pliku TXT oznacza nowy akapit.
- Przy zamianie DOCX na TXT każdy akapit jest oddzielony pustą linią.

PDF
- Zamianę na PDF robi LibreOffice w tle, bez otwierania okna.
- Przed konwersją trzeba zamknąć LibreOffice, jeśli jest otwarty.

Jeśli plik jest uszkodzony albo czegoś brakuje, program nie wyłącza się, tylko pokazuje komunikat, co jest nie tak.

## Pliki testowe

W folderze `samples` są przykładowe pliki

- `osoby.csv` dane z polskimi znakami i pustymi polami
- `produkty.json` obiekty z różnymi polami
- `uszkodzony.json` celowo zepsuty plik JSON
- `notatka.txt` tekst z kilkoma akapitami
- `notatka.docx` ten sam tekst w formacie Word
- `dokument.odt` ten sam tekst w formacie OpenDocument
- `uszkodzony.docx` celowo zepsuty plik DOCX

## Wykorzystanie AI

Przy pracy korzystałam z pomocy AI (Claude). Szczegóły są w plikach z raportami w folderze docs.