# Raport z etapu 3 (Lab 4)

Anastasiia Knyha, nr albumu 106230
2 listopada 2026

Repozytorium https://github.com/AnastasiiaKnyha/uniwersalny-konwerter

## Co zrobiłam

W tym etapie zrobiłam okienko programu w Tkinterze. Teraz można wybrać plik, folder zapisu i format docelowy, a potem kliknąć Konwertuj. Nie trzeba już używać terminala.

Okienko korzysta z tego samego słownika REGISTRY co wersja z terminala. Kod konwersji się nie zmienił, dodałam tylko nowy plik app.py.

![Okno programu](lab4-okno.png)

## Jak działa okienko

Po wybraniu pliku program pyta słownik REGISTRY, na jakie formaty można ten plik zamienić. Tylko te formaty pojawiają się na liście. Z listy można tylko wybierać, nie da się wpisać własnego formatu. Dzięki temu nie da się wybrać pary, której program nie obsługuje.

Jeśli plik ma format, którego program nie obsługuje, lista i przycisk Konwertuj są zablokowane, a w okienku pojawia się komunikat.

![Zablokowany nieobsługiwany plik](lab4-blokada.png)

Przycisk Konwertuj działa dopiero wtedy, gdy wybrany jest plik, folder i format.

Na dole okienka jest lista wszystkich obsługiwanych konwersji. Ta lista też jest tworzona ze słownika REGISTRY, więc po dodaniu nowej pary pokaże się sama.

## Nadpisywanie plików

Jeśli plik wynikowy już istnieje, program pyta, co zrobić. Tak nadpisuje plik, Nie zapisuje pod nową nazwą z numerem, a Anuluj nic nie robi.

![Pytanie o nadpisanie](lab4-pytanie.png)

## Dlaczego konwersja działa w osobnym wątku

Zamiana na PDF przez LibreOffice trwa kilka sekund. Gdyby działała w głównym wątku, okienko by się zawiesiło i nie reagowało. Dlatego konwersja działa w osobnym wątku.

Tkinter pozwala zmieniać okienko tylko z głównego wątku. Dlatego wątek z konwersją nie dotyka okienka, tylko wkłada wynik do kolejki. Główny wątek co 100 milisekund sprawdza kolejkę i pokazuje wynik.

W czasie konwersji wszystkie przyciski są zablokowane, a pasek postępu się porusza. Dzięki temu nie da się kliknąć Konwertuj dwa razy.

## Komunikaty

Każdy błąd pokazuje okienko z przyczyną i podpowiedzią, co zrobić. Po błędzie program dalej działa. Nawet nieoczekiwany błąd nie wyłącza programu, tylko pokazuje komunikat.

![Komunikat o błędzie](lab4-blad.png)

## Historia w GitHub

| Data | Commit |
|---|---|
| 02.11.2026 | Add GUI window with file, folder and format selection |
| 02.11.2026 | Run conversion in background thread and ask before overwriting |
| 02.11.2026 | Update README for Lab 4 |

![Commity w GitHub](lab4-github.png)

## Testy

Wszystkie testy zrobiłam ręcznie w okienku programu.

| Nr | Co sprawdzam | Co zrobiłam | Wynik | Działa |
|---|---|---|---|---|
| 1 | stan na starcie | otworzyłam program | przycisk Konwertuj i lista formatów są nieaktywne | tak |
| 2 | formaty dla CSV | wybrałam osoby.csv | na liście jest tylko JSON | tak |
| 3 | formaty dla DOCX | wybrałam notatka.docx | na liście są PDF i TXT | tak |
| 4 | nieobsługiwany plik | wybrałam plik PDF | lista i przycisk są zablokowane, jest komunikat | tak |
| 5 | konwersja z okienka | zamieniłam osoby.csv na JSON | komunikat Gotowe i nowy plik osoby.json | tak |
| 6 | plik już istnieje | powtórzyłam konwersję | pytanie o nadpisanie, wszystkie trzy odpowiedzi działają | tak |
| 7 | okienko się nie zawiesza | zamieniłam notatka.docx na PDF i przesunęłam okno | pasek się porusza, przyciski są zablokowane, okno reaguje | tak |
| 8 | zepsuty plik | wybrałam uszkodzony.json | komunikat o błędzie, program dalej działa | tak |
| 9 | brak LibreOffice | uruchomiłam program ze złą ścieżką LIBREOFFICE_PATH | komunikat, że nie znaleziono LibreOffice, z instrukcją | tak |
| 10 | zamknięcie okna wyboru | zamknęłam okno wyboru pliku bez wyboru | nic się nie zmieniło | tak |

## Dlaczego takie testy

Testy 1, 2, 3 i 4 sprawdzają, czy lista formatów zależy od pliku i czy nie da się wybrać nieobsługiwanej pary.

Test 5 sprawdza, czy cała konwersja działa z okienka bez terminala.

Test 6 sprawdza, czy program nie nadpisuje pliku bez pytania.

Test 7 sprawdza, czy okienko nie zawiesza się w czasie dłuższej konwersji.

Testy 8 i 9 sprawdzają, czy komunikaty o błędach są zrozumiałe i czy program po błędzie dalej działa.

Test 10 sprawdza, czy zamknięcie okna wyboru niczego nie psuje.

## Źródła i narzędzia

Użyłam modułów tkinter, ttk, filedialog, messagebox, threading i queue. Wszystkie są wbudowane w Pythona.

Korzystałam z dokumentacji
https://docs.python.org/3/library/tkinter.ttk.html
https://docs.python.org/3/library/dialog.html
https://docs.python.org/3/library/threading.html
https://docs.python.org/3/library/queue.html

Korzystałam z pomocy AI (Claude). Claude pomógł mi zrobić plan realizacji każdego etapu i rozpisać zadania na każdy etap. Pomagał mi też poprawiać kod w miejscach, gdzie nie działał, oraz szukać informacji o błędach i o tym, jak je naprawić.