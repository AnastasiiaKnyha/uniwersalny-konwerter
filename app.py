import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from konwerter.errors import ConversionError
from konwerter.registry import REGISTRY, available_targets, execute


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

        try:
            target = execute(source, target_format, output_dir)
        except ConversionError as error:
            self.status_var.set(f"Błąd. {error}")
            messagebox.showerror("Błąd", str(error))
            return

        self.status_var.set(f"Gotowe. Zapisano plik {target}")
        messagebox.showinfo("Gotowe", f"Konwersja zakończona.\n\nZapisano plik\n{target}")


if __name__ == "__main__":
    app = App()
    app.mainloop()