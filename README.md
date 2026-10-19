# Uniwersalny konwerter plików

Projekt na Programowanie V.
Autorka: Anastasiia Knyha, nr albumu 106230

Program zamienia pliki z jednego formatu na inny. Jest napisany w Pythonie, a na końcu będzie miał okienko w Tkinterze.

## Co program umie

| Z | Na | Status |
|---|---|---|
| CSV | JSON | działa |
| JSON | CSV | działa |
| TXT | DOCX | w planach |
| DOCX | TXT | w planach |
| DOCX | PDF | w planach |
| ODT | PDF | w planach |

## Jak uruchomić

Na razie program działa z terminala:

```
python3 cli.py <plik> <format> <folder>
```

Przykład:

```
python3 cli.py samples/osoby.csv json wyniki
```

Wynik zapisuje się w folderze `wyniki`. Jeśli taki plik już istnieje, program nie nadpisuje go, tylko dodaje numer do nazwy, np. `osoby_1.json`.

## Jakie pliki CSV i JSON są obsługiwane

- Pliki muszą być w kodowaniu UTF-8, żeby polskie znaki działały poprawnie.
- W CSV pierwszy wiersz to nazwy kolumn, a wartości są oddzielone przecinkami.
- JSON musi być listą obiektów, na przykład:

```json
[
  {"imię": "Anna", "wiek": 20},
  {"imię": "Ewa", "wiek": 28}
]
```

- Puste pola zostają puste.
- Kolejność kolumn się nie zmienia.
- Jeśli plik jest uszkodzony, program nie wyłącza się, tylko pokazuje komunikat, co jest nie tak.

## Pliki testowe

W folderze `samples` są przykładowe pliki:

- `osoby.csv` – dane z polskimi znakami i pustymi polami
- `produkty.json` – obiekty z różnymi polami
- `uszkodzony.json` – celowo zepsuty plik, do sprawdzenia błędów
- `notatka.txt` – tekst z kilkoma akapitami

## Wykorzystanie AI

Przy pracy korzystałam z pomocy AI (Claude): do wyjaśnienia zadania, podziału pracy na etapy i pomocy przy pisaniu kodu. Cały kod przeczytałam, przetestowałam i rozumiem, jak działa.