#!/usr/bin/env python3
import os
import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext, ttk

FILENAME = "words-ar-en"

def ensure_file():
    if not os.path.exists(FILENAME):
        open(FILENAME, "a", encoding="utf-8").close()

def load_db():
    """
    Read file lines, handle cases where Arabic translation has spaces by joining
    all parts after the first into one string joined with underscores (like the CLI script).
    Returns dict {En: Ar_with_underscores}.
    """
    d = {}
    with open(FILENAME, "r", encoding="utf-8") as f:
        for line in f:
            if line.isspace() or not line.strip():
                continue
            parts = line.strip().split()
            # If more than 2 parts, join parts[1:] using underscores
            if len(parts) != 2:
                # Handle malformed line similar to CLI version
                if len(parts) >= 2:
                    tmpstr = "_".join(parts[1:])
                    parts = [parts[0], tmpstr]
                else:
                    # skip lines that don't have at least an english word
                    continue
            en, ar = parts
            en = en.capitalize()
            ar = ar.capitalize()
            if en in d:
                # preserve first occurrence, report duplicate like original
                print("Found a duplicated english word with arabic word: ")
                print(f"first: {en} => {d[en]}\nsecond: {en} => {ar}\n")
                continue
            d[en] = ar
    return d

def write_entry(en, ar):
    """
    Write entry to file. Expect 'ar' may contain spaces; convert spaces to underscores
    to keep file format consistent with CLI behaviour.
    """
    ar_to_write = ar.replace(" ", "_")
    with open(FILENAME, "a", encoding="utf-8") as f:
        f.write(f"{en} {ar_to_write}\n")

class WordsApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Words AR-EN")
        self.geometry("700x500")
        self.resizable(True, True)

        ensure_file()
        self.dct = load_db()

        # Top frame: buttons
        top = ttk.Frame(self)
        top.pack(side="top", fill="x", padx=8, pady=6)

        btn_refresh = ttk.Button(top, text="Refresh", command=self.refresh)
        btn_refresh.pack(side="left")

        btn_add = ttk.Button(top, text="Add Word", command=self.add_word_dialog)
        btn_add.pack(side="left", padx=(6,0))

        btn_export = ttk.Button(top, text="Export to file...", command=self.export_file)
        btn_export.pack(side="left", padx=(6,0))

        # Search/filter
        ttk.Label(top, text="Search:").pack(side="left", padx=(12,4))
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(top, textvariable=self.search_var)
        search_entry.pack(side="left")
        search_entry.bind("<KeyRelease>", lambda e: self.refresh())

        # Main display: scrolled text with monospace font for alignment
        display_frame = ttk.Frame(self)
        display_frame.pack(fill="both", expand=True, padx=8, pady=6)

        self.text = scrolledtext.ScrolledText(display_frame, wrap="none", font=("Courier", 11))
        self.text.pack(fill="both", expand=True)

        # Status bar
        self.status = ttk.Label(self, text="", anchor="w")
        self.status.pack(side="bottom", fill="x")

        self.refresh()

    def refresh(self):
        self.dct = load_db()
        items = sorted(self.dct.items(), key=lambda x: x[0])
        q = self.search_var.get().strip().lower()
        if q:
            items = [it for it in items if q in it[0].lower() or q in it[1].lower()]

        self.text.config(state="normal")
        self.text.delete("1.0", tk.END)

        if not items:
            self.text.insert(tk.END, "No words found.\n")
            self.status.config(text="0 entries")
            self.text.config(state="disabled")
            return

        per_page = 5
        page = 2
        count = 0
        total = len(items)
        for idx, (en, ar) in enumerate(items, start=1):
            # convert underscores back to spaces for display
            ar_display = ar.replace("_", " ")
            # paginate visually similar to original: separator every `per_page`
            if (idx - 1) % per_page == 0:
                if idx != 1:
                    self.text.insert(tk.END, "-"*60 + "\n")
                    page += 1
                header = f"{'-'*60}\n\t\t\tPage {page}\n{'-'*60}\n"
                if idx == 1:
                    self.text.insert(tk.END, header)
                else:
                    self.text.insert(tk.END, header)

            line = f"{str(idx).zfill(4):<4} - \t{en:<15} \t====> \t{ar_display}\n"
            self.text.insert(tk.END, line)
            count += 1

        self.text.config(state="disabled")
        self.status.config(text=f"{total} entries shown")

    def add_word_dialog(self):
        # Ask for English word
        en = simpledialog.askstring("English word", "Enter an English word:", parent=self)
        if en is None:
            return
        en = en.strip().capitalize()
        if not en:
            messagebox.showerror("Error", "Empty English word.")
            return
        if en in self.dct:
            messagebox.showerror("Error", f"'{en}' already exists:\n{en} => {self.dct[en].replace('_',' ')}")
            return
        ar = simpledialog.askstring("Arabic word", "Enter the Arabic word (can include spaces):", parent=self)
        if ar is None:
            return
        ar = ar.strip().capitalize()
        if not ar:
            messagebox.showerror("Error", "Empty Arabic word.")
            return
        # write and refresh (write_entry will convert spaces to underscores)
        try:
            write_entry(en, ar)
            messagebox.showinfo("Done", f"Added: {en} => {ar}")
            self.refresh()
        except Exception as e:
            messagebox.showerror("Error", f"Couldn't write to file:\n{e}")

    def export_file(self):
        # simple export: ask for filename and write current shown entries
        fname = simpledialog.askstring("Export", "Enter export filename:", parent=self)
        if not fname:
            return
        try:
            items = sorted(self.dct.items(), key=lambda x: x[0])
            with open(fname, "w", encoding="utf-8") as f:
                for en, ar in items:
                    f.write(f"{en} {ar}\n")
            messagebox.showinfo("Exported", f"Exported {len(items)} entries to {fname}")
        except Exception as e:
            messagebox.showerror("Error", f"Couldn't export:\n{e}")

if __name__ == "__main__":
    app = WordsApp()
    app.mainloop()

