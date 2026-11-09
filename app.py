import logging
import queue
import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from konwerter.errors import ConversionError
from konwerter.logger import setup_logging
from konwerter.registry import REGISTRY, available_targets, execute, validate

logger = logging.getLogger(__name__)


class App(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Uniwersalny konwerter plików")
        self.resizable(False, False)

        # values shown in the window
        self.file_var = tk.StringVar()
        self.folder_var = tk.StringVar()
        self.format_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Wybierz plik do konwersji.")

        # the worker thread puts its result here
        self.results = queue.Queue()

        self.create_widgets()
        self.update_button()

    def create_widgets(self) -> None:
        frame = ttk.Frame(self, padding=16)
        frame.grid(row=0, column=0)

        # row 0: input file
        ttk.Label(frame, text="Plik wejściowy").grid(row=0, column=0, sticky="w", pady=4)
        ttk.Entry(frame, textvariable=self.file_var, width=50, state="readonly").grid(row=0, column=1, padx=8)
        self.file_button = ttk.Button(frame, text="Wybierz plik", command=self.choose_file)
        self.file_button.grid(row=0, column=2, sticky="ew")

        # row 1: output folder
        ttk.Label(frame, text="Folder zapisu").grid(row=1, column=0, sticky="w", pady=4)
        ttk.Entry(frame, textvariable=self.folder_var, width=50, state="readonly").grid(row=1, column=1, padx=8)
        self.folder_button = ttk.Button(frame, text="Wybierz folder", command=self.choose_folder)
        self.folder_button.grid(row=1, column=2, sticky="ew")

        # row 2: target format, list is filled after choosing a file
        ttk.Label(frame, text="Format docelowy").grid(row=2, column=0, sticky="w", pady=4)
        self.format_box = ttk.Combobox(frame, textvariable=self.format_var, state="disabled", width=12)
        self.format_box.grid(row=2, column=1, sticky="w", padx=8)
        self.format_box.bind("<<ComboboxSelected>>", lambda event: self.update_button())

        # row 3: start button
        self.convert_button = ttk.Button(frame, text="Konwertuj", command=self.start_conversion)
        self.convert_button.grid(row=3, column=0, columnspan=3, pady=(12, 4), sticky="ew")

        # row 4: progress bar, it moves only during conversion
        self.progress = ttk.Progressbar(frame, mode="determinate")
        self.progress.grid(row=4, column=0, columnspan=3, sticky="ew", pady=4)

        # row 5: status text
        ttk.Label(frame, textvariable=self.status_var, wraplength=520).grid(
            row=5, column=0, columnspan=3, sticky="w", pady=4
        )

        # row 6: list of supported conversions taken from the registry
        pairs_frame = ttk.LabelFrame(frame, text="Obsługiwane konwersje", padding=8)
        pairs_frame.grid(row=6, column=0, columnspan=3, sticky="ew", pady=(8, 0))
        lines = []
        for source_format, target_format in REGISTRY:
            lines.append(f"{source_format[1:].upper()} na {target_format[1:].upper()}")
        ttk.Label(pairs_frame, text="     ".join(lines)).grid(row=0, column=0, sticky="w")

    def choose_file(self) -> None:
        # build file filter from formats in the registry, like *.csv *.json
        patterns = []
        for source_format, target_format in REGISTRY:
            pattern = "*" + source_format
            if pattern not in patterns:
                patterns.append(pattern)

        path = filedialog.askopenfilename(
            title="Wybierz plik",
            filetypes=[("Obsługiwane pliki", " ".join(patterns)), ("Wszystkie pliki", "*.*")],
        )
        # user closed the window without choosing
        if not path:
            return

        self.file_var.set(path)

        # by default save next to the input file
        if self.folder_var.get() == "":
            self.folder_var.set(str(Path(path).parent))

        self.update_formats()

    def choose_folder(self) -> None:
        path = filedialog.askdirectory(title="Wybierz folder zapisu")
        if path:
            self.folder_var.set(path)
            self.update_button()

    def update_formats(self) -> None:
        source = Path(self.file_var.get())
        targets = available_targets(source)

        if len(targets) == 0:
            # unsupported file, nothing can be chosen
            self.format_box["values"] = []
            self.format_var.set("")
            self.format_box.config(state="disabled")
            self.status_var.set(f"Format \"{source.suffix}\" nie jest obsługiwany. Wybierz inny plik.")
        else:
            # readonly means the user can only pick from the list
            self.format_box["values"] = targets
            self.format_var.set(targets[0])
            self.format_box.config(state="readonly")
            self.status_var.set("Wybierz format i kliknij Konwertuj.")

        self.update_button()

    def update_button(self) -> None:
        # button works only when everything is chosen
        if self.file_var.get() and self.folder_var.get() and self.format_var.get():
            self.convert_button.config(state="normal")
        else:
            self.convert_button.config(state="disabled")

    def start_conversion(self) -> None:
        source = Path(self.file_var.get())
        output_dir = Path(self.folder_var.get())
        target_format = self.format_var.get()

        # check everything before we start
        try:
            validate(source, target_format, output_dir)
        except ConversionError as error:
            logger.warning(f"Błędny wybór w oknie. {error}")
            messagebox.showerror("Błąd", str(error))
            return

        # ask before overwriting an existing file
        overwrite = False
        target = output_dir / (source.stem + target_format)
        if target.exists():
            answer = messagebox.askyesnocancel(
                "Plik już istnieje",
                f"Plik {target.name} już istnieje.\n\n"
                "Tak  nadpisz plik\n"
                "Nie  zapisz pod nową nazwą\n"
                "Anuluj  nie rób nic",
            )
            # none means cancel
            if answer is None:
                return
            overwrite = answer

        self.set_working(True)
        self.status_var.set("Trwa konwersja, proszę czekać...")

        # long work runs in a separate thread, so the window does not freeze
        worker = threading.Thread(
            target=self.run_conversion,
            args=(source, target_format, output_dir, overwrite),
            daemon=True,
        )
        worker.start()
        self.after(100, self.check_result)

    def run_conversion(self, source: Path, target_format: str, output_dir: Path, overwrite: bool) -> None:
        # this runs in the worker thread, so no window changes here
        try:
            target = execute(source, target_format, output_dir, overwrite)
            self.results.put(("ok", str(target)))
        except ConversionError as error:
            self.results.put(("error", str(error)))
        except Exception as error:
            # unexpected problem, app should not crash
            logger.exception("Nieoczekiwany błąd podczas konwersji")
            self.results.put(("error", f"Nieoczekiwany błąd: {error}"))

    def check_result(self) -> None:
        try:
            kind, text = self.results.get_nowait()
        except queue.Empty:
            # no result yet, check again in 100 ms
            self.after(100, self.check_result)
            return

        self.set_working(False)
        if kind == "ok":
            self.status_var.set(f"Gotowe. Zapisano plik {text}")
            messagebox.showinfo("Gotowe", f"Konwersja zakończona.\n\nZapisano plik\n{text}")
        else:
            self.status_var.set(f"Błąd. {text}")
            messagebox.showerror("Błąd", text)

    def set_working(self, working: bool) -> None:
        if working:
            # block buttons during conversion
            self.progress.config(mode="indeterminate")
            self.progress.start(10)
            self.file_button.config(state="disabled")
            self.folder_button.config(state="disabled")
            self.format_box.config(state="disabled")
            self.convert_button.config(state="disabled")
        else:
            self.progress.stop()
            self.progress.config(mode="determinate", value=0)
            self.file_button.config(state="normal")
            self.folder_button.config(state="normal")
            self.format_box.config(state="readonly")
            self.update_button()


if __name__ == "__main__":
    app = App()
    app.mainloop()