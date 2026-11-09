# Uniwersalny konwerter plików

Projekt na Programowanie V.

## Cel

Program zamienia pliki z jednego formatu na inny. Użytkownik wybiera plik, program pokazuje tylko te formaty, na które można go zamienić, robi konwersję i zapisuje wynik we wskazanym folderze. Program ma okienko w Tkinterze, ale można go też uruchomić z terminala.

## Autorka

Anastasiia Knyha, nr albumu 106230. Projekt zrobiłam samodzielnie.

## Obsługiwane konwersje

| Grupa | Z | Na | Ograniczenia |
|---|---|---|---|
| A dane | CSV | JSON | wszystkie wartości zapisują się jako tekst |
| A dane | JSON | CSV | tylko lista obiektów bez zagnieżdżonych pól |
| B tekst | TXT | DOCX | pusta linia oznacza nowy akapit, tekst jest bez formatowania |
| B tekst | DOCX | TXT | zostaje tylko tekst akapitów, bez tabel, obrazków i formatowania |
| C biuro | DOCX | PDF | potrzebny LibreOffice, wygląd może się trochę różnić od Worda |
| C biuro | ODT | PDF | potrzebny LibreOffice |

Program nie obsługuje innych par. W okienku na liście pojawiają się tylko formaty z tej tabeli.

## Wymagania

- Python 3.9 lub nowszy
- Tkinter, jest wbudowany w Pythona. Na Macu najlepiej użyć Pythona ze strony python.org, bo systemowy Python ma starą wersję Tkintera
- biblioteki python-docx i pytest, są w pliku requirements.txt
- LibreOffice, potrzebny tylko do zamiany na PDF. To program systemowy, trzeba go zainstalować osobno

## Instalacja

1. Zainstaluj Pythona ze strony https://www.python.org
2. Zainstaluj LibreOffice ze strony https://www.libreoffice.org
3. Pobierz projekt

```
git clone https://github.com/AnastasiiaKnyha/uniwersalny-konwerter.git
cd uniwersalny-konwerter
```

4. Utwórz środowisko wirtualne i zainstaluj biblioteki

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Na Windowsie zamiast `source .venv/bin/activate` wpisz `.venv\Scripts\activate`, a zamiast `python3` wpisz `python`.

Program sam szuka LibreOffice w typowych miejscach na macOS, Windowsie i Linuxie. Jeśli go nie znajdzie, można podać ścieżkę w zmiennej LIBREOFFICE_PATH, na przykład na Macu

```
export LIBREOFFICE_PATH="/Applications/LibreOffice.app/Contents/MacOS/soffice"
```

## Uruchomienie

Wersja z okienkiem

```
python3 app.py
```

W okienku wybierz plik, folder zapisu i format, a potem kliknij Konwertuj. Lista formatów pokazuje tylko te konwersje, które działają dla wybranego pliku. Jeśli plik wynikowy już istnieje, program zapyta, czy go nadpisać, czy zapisać pod nową nazwą.

Wersja z terminala

```
python3 cli.py <plik> <format> <folder>
```

Przykłady

```
python3 cli.py samples/osoby.csv json wyniki
python3 cli.py samples/notatka.docx pdf wyniki
```

W wersji z terminala program nigdy nie nadpisuje plików, tylko dodaje numer do nazwy, np. `osoby_1.json`.

## Jak działają konwersje

CSV i JSON
- Pliki muszą być w kodowaniu UTF-8. Pliki CSV z Excela z BOM też działają.
- W CSV pierwszy wiersz to nazwy kolumn, wartości są oddzielone przecinkami, nazwy kolumn muszą być różne, a każdy wiersz musi mieć tyle kolumn co nagłówek.
- JSON musi być niepustą listą obiektów z prostymi wartościami, na przykład `[{"imię": "Anna", "wiek": 20}]`.
- Kolejność i nazwy kolumn się nie zmieniają. Puste pola i brakujące pola dają pustą komórkę.
- Wynikowy CSV jest zapisany z BOM, żeby Excel dobrze pokazywał polskie znaki.

TXT i DOCX
- Pusta linia w pliku TXT oznacza nowy akapit, a zwykły enter zostaje jako nowa linia w akapicie.
- Przy zamianie DOCX na TXT każdy akapit jest oddzielony pustą linią.

PDF
- Zamianę na PDF robi LibreOffice w tle, bez otwierania okna.
- Przed konwersją trzeba zamknąć LibreOffice, jeśli jest otwarty.

## Walidacja i błędy

Przed konwersją program sprawdza, czy plik istnieje, czy jego format jest obsługiwany, czy wybrana para jest w tabeli, czy folder istnieje i czy można w nim zapisywać. Sprawdza też, czy plik wynikowy już istnieje.

Jeśli plik jest uszkodzony albo czegoś brakuje, program nie wyłącza się, tylko pokazuje komunikat z przyczyną i podpowiedzią, co zrobić.

Każda konwersja i każdy błąd są zapisywane w pliku `konwerter.log` w folderze projektu, razem z czasem trwania konwersji.

## Dane testowe

| Plik | Co zawiera | Oczekiwany wynik |
|---|---|---|
| `samples/osoby.csv` | 3 osoby, polskie znaki, puste pola, przecinek w cudzysłowie | JSON z 3 obiektami, polskie znaki i puste pola bez zmian |
| `samples/produkty.json` | obiekty z różnymi polami i wartością null | CSV z 4 kolumnami, brakujące pola są puste |
| `samples/uszkodzony.json` | JSON z błędem składni | komunikat z numerem linii i kolumny |
| `samples/notatka.txt` | tekst z 3 akapitami i polskimi znakami | DOCX z 3 akapitami |
| `samples/notatka.docx` | ten sam tekst w formacie Word | TXT taki sam jak notatka.txt albo PDF z tym tekstem |
| `samples/dokument.odt` | ten sam tekst w formacie OpenDocument | PDF z tym tekstem |
| `samples/uszkodzony.docx` | zwykły tekst z rozszerzeniem docx | komunikat, że plik jest uszkodzony |

## Testy

Testy automatyczne uruchamia się komendą

```
pytest -v
```

Jest 23 testów. Sprawdzają funkcje validate i available_targets, wszystkie konwersje, zepsute pliki, brak LibreOffice i nadpisywanie plików. Test prawdziwej zamiany na PDF jest pomijany, jeśli na komputerze nie ma LibreOffice.

Raport z testów jest w pliku `docs/raport-testow.md`. Raporty z poszczególnych etapów są w folderze `docs`.

## Struktura projektu

```
app.py                okienko programu
cli.py                uruchamianie z terminala
konwerter/
    registry.py       słownik konwersji, walidacja i funkcja execute
    data.py           CSV i JSON
    text.py           TXT i DOCX
    office.py         LibreOffice i PDF
    errors.py         własny błąd ConversionError
    logger.py         zapisywanie logów
tests/                testy automatyczne
samples/              dane testowe
docs/                 raporty
requirements.txt      biblioteki
```

Logika konwersji jest oddzielona od okienka. Żeby dodać nową konwersję, wystarczy napisać funkcję i dopisać jedną linię w słowniku REGISTRY w pliku `konwerter/registry.py`. Okienko samo pokaże nowy format.

## Znane ograniczenia

- Program nie przenosi formatowania, tabel, obrazków ani przypisów z dokumentów.
- Zamiana na PDF wymaga zainstalowanego LibreOffice.
- Przy zamianie na PDF LibreOffice musi być zamknięty.
- JSON z zagnieżdżonymi obiektami i listami nie jest obsługiwany.
- W CSV separatorem musi być przecinek.

## Źródła

- dokumentacja tkinter https://docs.python.org/3/library/dialog.html
- dokumentacja python-docx https://python-docx.readthedocs.io/
- parametry LibreOffice https://help.libreoffice.org/latest/en-US/text/shared/guide/start_parameters.html
- moduł subprocess https://docs.python.org/3/library/subprocess.html
- dokumentacja pytest https://docs.pytest.org/

## Wykorzystanie AI

## Wykorzystanie AI

Przy pracy korzystałam z pomocy AI (Claude). Claude pomógł mi zrobić plan realizacji projektu i rozpisać zadania na każdy etap. Przygotowywał też szkice i szablony funkcji, które potem poprawiałam i dostosowywałam do mojego projektu. Pomagał mi szukać przyczyn błędów i sposobów ich naprawy oraz skonfigurować testy automatyczne w pytest. Każdą część kodu sprawdzałam i testowałam przed dodaniem do repozytorium