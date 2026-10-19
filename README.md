# Uniwersalny konwerter plików

Projekt 1, Programowanie V. Aplikacja desktopowa (Python 3 + Tkinter) do konwersji plików.

## Planowana macierz konwersji

| Grupa | Konwersja | Status |
|---|---|---|
| A | CSV → JSON | gotowe |
| A | JSON → CSV | gotowe |
| B | TXT → DOCX | planowane |
| B | DOCX → TXT | planowane |
| C | DOCX → PDF | planowane |
| C | ODT → PDF | planowane |

## Zasady CSV ↔ JSON

- Kodowanie: UTF-8 (pliki z BOM z Excela też są obsługiwane). Wynikowy CSV zapisywany jest z BOM, aby Excel poprawnie pokazywał polskie znaki.
- CSV: separator przecinek, pierwszy wiersz to nagłówki, nazwy kolumn muszą być unikalne, każdy wiersz musi mieć tyle kolumn co nagłówek.
- JSON: niepusta lista obiektów z prostymi wartościami (tekst, liczba, null), np. `[{"imię": "Anna", "wiek": 20}]`. Zagnieżdżone obiekty i listy nie są obsługiwane.
- CSV → JSON: wszystkie wartości zapisywane są jako tekst, puste komórki jako `""`.
- JSON → CSV: kolumny w kolejności pierwszego wystąpienia; brakujące pola i `null` dają pustą komórkę.

## Uruchomienie bez GUI

```
python3 cli.py samples/osoby.csv json wyniki
```