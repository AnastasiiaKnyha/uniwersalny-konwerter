# Raport z testów

Anastasiia Knyha, nr albumu 106230
9 listopada 2026

Repozytorium https://github.com/AnastasiiaKnyha/uniwersalny-konwerter

## Co zrobiłam w ostatnim etapie

Dodałam zapisywanie logów. Każda konwersja i każdy błąd trafiają do pliku konwerter.log razem z czasem trwania konwersji.

Napisałam 23 testy automatyczne w pytest i uzupełniłam README o instalację, dane testowe, znane ograniczenia i źródła.

Sprawdziłam też, czy program uruchamia się według README na czystym środowisku. Pobrałam repozytorium do nowego folderu, zrobiłam nowe środowisko wirtualne, zainstalowałam biblioteki i uruchomiłam testy oraz okienko.

## Minimalna macierz testów

| Przypadek | Oczekiwany wynik | Jak sprawdziłam | Wynik |
|---|---|---|---|
| poprawny plik w każdej grupie | powstaje plik, który da się otworzyć | osoby.csv na JSON, produkty.json na CSV, notatka.txt na DOCX, notatka.docx na TXT, notatka.docx na PDF, dokument.odt na PDF, ręcznie i w testach automatycznych | działa |
| błędny lub uszkodzony plik | program się nie wyłącza i pokazuje komunikat | uszkodzony.json, uszkodzony.docx, CSV ze złą liczbą kolumn, pusty CSV | działa |
| nieobsługiwana para | opcji nie ma na liście albo jest zablokowana | w okienku lista pokazuje tylko obsługiwane formaty, a pliki PDF są szare w oknie wyboru | działa |
| brak LibreOffice | komunikat z instrukcją | zła ścieżka w zmiennej LIBREOFFICE_PATH w okienku, w terminalu i w teście automatycznym | działa |
| plik docelowy już istnieje | pytanie o nadpisanie albo bezpieczna nazwa | w okienku pytanie Tak Nie Anuluj, w terminalu nowa nazwa z numerem | działa |
| polskie znaki i puste wartości | znaki i dane się nie zmieniają | porównanie osoby.csv przed i po zamianie na JSON i z powrotem | działa |

## Testy automatyczne

Testy uruchamia się komendą pytest. Wszystkie 23 testy przeszły.

| Plik | Test | Co sprawdza |
|---|---|---|
| test_registry.py | test_targets_for_csv | dla CSV dostępny jest tylko JSON |
| test_registry.py | test_targets_for_docx | dla DOCX dostępne są PDF i TXT |
| test_registry.py | test_targets_ignore_letter_case | wielkość liter w rozszerzeniu nie ma znaczenia |
| test_registry.py | test_no_targets_for_unknown_format | nieznany format nie ma żadnych formatów docelowych |
| test_registry.py | test_validate_accepts_correct_choice | poprawny wybór przechodzi walidację |
| test_registry.py | test_validate_missing_file | brak pliku daje błąd |
| test_registry.py | test_validate_unsupported_pair | nieobsługiwana para daje błąd |
| test_registry.py | test_validate_missing_folder | brak folderu daje błąd |
| test_registry.py | test_execute_does_not_overwrite | przy drugiej konwersji powstaje osoby_1.json |
| test_registry.py | test_execute_overwrites_when_asked | z opcją nadpisania plik ma tę samą nazwę |
| test_data.py | test_csv_to_json_keeps_polish_letters_and_empty_values | polskie znaki, puste pola i przecinek w cudzysłowie zostają poprawne |
| test_data.py | test_csv_to_json_keeps_column_order | kolejność kolumn się nie zmienia |
| test_data.py | test_csv_json_csv_gives_the_same_data | po zamianie CSV na JSON i z powrotem dane są takie same |
| test_data.py | test_json_to_csv_fills_missing_fields_with_empty_cells | brakujące pola i null dają puste komórki |
| test_data.py | test_broken_json_gives_clear_error | zepsuty JSON daje zrozumiały komunikat |
| test_data.py | test_csv_with_wrong_number_of_columns | wiersz ze złą liczbą kolumn daje komunikat z numerem wiersza |
| test_data.py | test_empty_csv | pusty CSV daje komunikat |
| test_documents.py | test_txt_to_docx_makes_paragraphs | z TXT powstają 3 akapity z polskimi znakami |
| test_documents.py | test_txt_docx_txt_gives_the_same_text | po zamianie TXT na DOCX i z powrotem tekst jest taki sam |
| test_documents.py | test_broken_docx_to_txt | zepsuty DOCX daje komunikat |
| test_documents.py | test_broken_docx_to_pdf | zepsuty DOCX nie trafia do LibreOffice i daje komunikat |
| test_documents.py | test_missing_libreoffice | brak LibreOffice daje komunikat z instrukcją |
| test_documents.py | test_docx_to_pdf | z DOCX powstaje prawdziwy plik PDF |

## Dlaczego takie testy

Testy funkcji available_targets i validate sprawdzają, czy program dobrze rozpoznaje formaty i czy blokuje złe wybory przed konwersją.

Testy konwersji sprawdzają rzeczy, przy których najłatwiej o błąd, czyli polskie znaki, puste pola, kolejność kolumn i akapity. Testy w dwie strony pokazują, że dane się nie gubią.

Testy z zepsutymi plikami i bez LibreOffice sprawdzają, czy program zawsze daje zrozumiały komunikat zamiast się wyłączać.

Testy okienka zrobiłam ręcznie, bo sprawdzają rzeczy, które trzeba zobaczyć, na przykład czy okno się nie zawiesza. Opisałam je w raporcie z etapu 3.

## Biblioteki i narzędzia

python-docx do plików DOCX
LibreOffice do zamiany na PDF
pytest do testów automatycznych
moduły wbudowane w Pythona, czyli tkinter, csv, json, subprocess, threading, queue, logging, pathlib, shutil, tempfile i zipfile

## Źródła

https://docs.python.org/3/library/dialog.html
https://python-docx.readthedocs.io/
https://help.libreoffice.org/latest/en-US/text/shared/guide/start_parameters.html
https://docs.python.org/3/library/subprocess.html
https://docs.pytest.org/

## Wykorzystanie AI

## Wykorzystanie AI

Korzystałam z pomocy AI (Claude). Claude pomógł mi zrobić plan realizacji każdego etapu i rozpisać zadania na każdy etap.

Przy pisaniu kodu Claude przygotowywał szkice i szablony funkcji, na przykład konwerterów, rejestru i okienka. Potem poprawiałam je i dostosowywałam do mojego projektu, a każdą zmianę sprawdzałam w terminalu i w okienku.

Claude pomagał mi też poprawiać kod w miejscach, gdzie nie działał, oraz szukać informacji o błędach i o tym, jak je naprawić. W ostatnim etapie pomagał mi skonfigurować testy automatyczne w pytest