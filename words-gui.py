#!/usr/bin/env python3
# Fixed GUI version: dialogs parented, centered windows, safer JSON handling,
# input validation loops similar to your CLI, no abrupt sys.exit on JSON errors.

import tkinter as tk
from tkinter import simpledialog, messagebox, scrolledtext
import json, os, datetime, traceback

JSON_FILE = "words-ar-en.json"


def sort_numeric_keys(dct):
    try:
        return dict(sorted(dct.items(), key=lambda x: int(x[0])))
    except Exception:
        # If keys are not numeric for some reason, keep original order
        return dct


def center_window(win, width=600, height=400, parent=None):
    win.update_idletasks()
    if parent:
        px = parent.winfo_rootx()
        py = parent.winfo_rooty()
        pw = parent.winfo_width()
        ph = parent.winfo_height()
        x = px + (pw - width) // 2
        y = py + (ph - height) // 2
    else:
        sw = win.winfo_screenwidth()
        sh = win.winfo_screenheight()
        x = (sw - width) // 2
        y = (sh - height) // 2
    win.geometry(f"{width}x{height}+{x}+{y}")


def backup_corrupted_file():
    if os.path.exists(JSON_FILE):
        ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        bak = f"{JSON_FILE}.bak.{ts}"
        try:
            os.rename(JSON_FILE, bak)
            return bak
        except Exception:
            return None
    return None


def load_data(parent=None):
    # ensure file exists and not empty
    if not os.path.exists(JSON_FILE):
        with open(JSON_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f, indent=4, ensure_ascii=False)

    try:
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            content = f.read()
            if not content.strip():
                return {}
            data = json.loads(content)
            return sort_numeric_keys(data)
    except json.decoder.JSONDecodeError:
        bak = backup_corrupted_file()
        if bak:
            messagebox.showwarning(
                "JSON corrupted",
                f"The JSON file was corrupted. A backup was created: {bak}\nA fresh empty database will be used.",
                parent=parent,
            )
        else:
            messagebox.showwarning(
                "JSON corrupted",
                "The JSON file was corrupted and could not be backed up. A fresh empty database will be used.",
                parent=parent,
            )
        # create new empty file
        with open(JSON_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f, indent=4, ensure_ascii=False)
        return {}
    except Exception as e:
        messagebox.showerror("Error", f"Failed to read JSON:\n{e}", parent=parent)
        return {}


def save_data(data, parent=None):
    try:
        data = sort_numeric_keys(data)
        with open(JSON_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save JSON:\n{e}", parent=parent)


# ---------- Validation helpers that mimic CLI behavior ----------
def ask_nonempty_string(title, prompt, parent=None, capitalize=True, allow_leaveit=False):
    # This repeats until user provides non-empty or cancels (returns None)
    while True:
        val = simpledialog.askstring(title, prompt, parent=parent)
        if val is None:
            return None
        if allow_leaveit and val.strip().upper() == "LEAVEIT":
            return "LEAVEIT"
        if val.strip() == "":
            messagebox.showerror("Input error", "Input cannot be empty.", parent=parent)
            continue
        return val.strip().capitalize() if capitalize else val.strip()


def ask_page_number(prompt, parent=None, must_exist=None, data=None):
    # must_exist: None => don't check existence, True => must exist, False => must NOT exist
    while True:
        page = simpledialog.askstring("Page", prompt, parent=parent)
        if page is None:
            return None
        page = page.strip()
        if not page.isdigit():
            messagebox.showerror("Input error", "Page must be a digit.", parent=parent)
            continue
        if must_exist is True and data is not None and page not in data:
            messagebox.showerror("Not found", f"Page {page} does not exist.", parent=parent)
            continue
        if must_exist is False and data is not None and page in data:
            messagebox.showerror("Exists", f"Page {page} already exists.", parent=parent)
            continue
        return page


# ----------------- Operations (follow CLI logic) -----------------
def show_data():
    try:
        data = load_data(parent=root)
        if not data:
            messagebox.showinfo("Print", "Nothing to print.", parent=root)
            return
        win = tk.Toplevel(root)
        win.title("Words — Print")
        win.transient(root)
        win.grab_set()
        txt = scrolledtext.ScrolledText(win, width=90, height=30)
        txt.pack(fill="both", expand=True, padx=6, pady=6)
        total = 0
        for page in data:
            txt.insert("end", "=" * 60 + "\n")
            txt.insert("end", f"\t\tPage {page}\n")
            txt.insert("end", "=" * 60 + "\n")
            for count, kv in enumerate(data[page], start=1):
                txt.insert("end", f"{str(count).zfill(2):<3} - {kv:<20} => {data[page][kv]}\n")
                total += 1
        txt.insert("end", "\n" + "=" * 60 + "\n")
        txt.insert("end", f"Total {len(data)} pages.\nTotal {total} words.\n")
        txt.config(state="disabled")
        center_window(win, width=800, height=600, parent=root)

        def on_close():
            try:
                win.grab_release()
            except Exception:
                pass
            win.destroy()

        win.protocol("WM_DELETE_WINDOW", on_close)
    except Exception as e:
        messagebox.showerror("Error", f"Unexpected error in show_data:\n{e}\n\n{traceback.format_exc()}", parent=root)


def add_word():
    try:
        data = load_data(parent=root)
        # show existing pages for convenience in prompt
        page = ask_page_number(f"Enter Page Number (existing: {tuple(int(i) for i in data.keys())})\n(You can enter a new page number):", parent=root, must_exist=None, data=data)
        if page is None:
            return

        # if not exist, create new page (same behavior as CLI)
        if page not in data:
            data[page] = {}

        # english (repeat until non-empty or cancel)
        enwrd = ask_nonempty_string("English Word", "Enter English Word:", parent=root, capitalize=True)
        if enwrd is None:
            return

        # arabic
        arwrd = ask_nonempty_string("Arabic Word", "Enter Arabic Word:", parent=root, capitalize=True)
        if arwrd is None:
            return

        # check across all pages for existence
        eexist = False
        pew = None
        for tpage in data:
            if enwrd in data[tpage]:
                eexist = True
                pew = tpage
                break

        if eexist:
            if data[pew][enwrd] == arwrd:
                messagebox.showinfo("Info", f"('{enwrd}': '{arwrd}') is already exists in page {pew}.", parent=root)
                return
            # ask to replace
            ans = messagebox.askyesno("Replace?",
                                      f"The English word '{enwrd}' is already in page {pew} with '{data[pew][enwrd]}'.\nReplace it with '{arwrd}' in page {pew}?",
                                      parent=root)
            if ans:
                data[pew][enwrd] = arwrd
                save_data(data, parent=root)
                messagebox.showinfo("Replaced", f"'{enwrd}' has been replaced to '{arwrd}'.", parent=root)
            else:
                messagebox.showinfo("Skipped", "Skipping operation.", parent=root)
                return
        else:
            data[page][enwrd] = arwrd
            save_data(data, parent=root)
            messagebox.showinfo("Added", f"Added ({enwrd}: {arwrd}) to page {page}.", parent=root)
    except Exception as e:
        messagebox.showerror("Error", f"Unexpected error in add_word:\n{e}\n\n{traceback.format_exc()}", parent=root)


def add_page():
    try:
        data = load_data(parent=root)
        page = ask_page_number(f"Enter new page number (existing: {tuple(i for i in data)}):", parent=root, must_exist=False, data=data)
        if page is None:
            return
        data[page] = {}
        save_data(data, parent=root)
        messagebox.showinfo("Page Added", f"Page {page} has been added.", parent=root)
    except Exception as e:
        messagebox.showerror("Error", f"Unexpected error in add_page:\n{e}\n\n{traceback.format_exc()}", parent=root)


def replace_word():
    try:
        data = load_data(parent=root)
        if not data:
            messagebox.showinfo("Info", "No pages/words to replace.", parent=root)
            return
        # show current words (brief) in a Toplevel for reference (optional)
        ref = tk.Toplevel(root)
        ref.title("Reference - current words")
        ref.transient(root)
        ref.grab_set()
        txt = scrolledtext.ScrolledText(ref, width=70, height=20)
        txt.pack(fill="both", expand=True, padx=6, pady=6)
        for tpage in data:
            txt.insert("end", f"Page {tpage}:\n")
            for kv in data[tpage]:
                txt.insert("end", f"{kv}\t{data[tpage][kv]}\n")
            txt.insert("end", "-" * 30 + "\n")
        txt.config(state="disabled")
        center_window(ref, width=600, height=400, parent=root)

        def close_ref():
            try:
                ref.grab_release()
            except Exception:
                pass
            ref.destroy()

        ref.protocol("WM_DELETE_WINDOW", close_ref)

        page = ask_page_number("Enter Page Number:", parent=root, must_exist=True, data=data)
        if page is None:
            close_ref()
            return

        orep = ask_nonempty_string("Replace - Old English", "Choose a word (English) you want to replace:", parent=root, capitalize=True)
        if orep is None:
            close_ref()
            return
        if orep not in data[page]:
            messagebox.showerror("Error", f"'{orep}' not found in page {page}.", parent=root)
            close_ref()
            return

        nrep = ask_nonempty_string("Replace - New English", f"Replace (English) '{orep}' in page {page} to: (type LEAVEIT to keep)", parent=root, capitalize=True, allow_leaveit=True)
        if nrep is None:
            close_ref()
            return
        if nrep == "LEAVEIT":
            nrep = orep

        anrep = ask_nonempty_string("Replace - New Arabic", f"Enter a new Arabic word for '{nrep}' (type LEAVEIT to keep):", parent=root, capitalize=True, allow_leaveit=True)
        if anrep is None:
            close_ref()
            return
        if anrep == "LEAVEIT":
            anrep = data[page][orep]

        # perform replacement
        # replicate original replace_key behaviour
        try:
            data[page][nrep] = data[page].pop(orep)
        except KeyError:
            messagebox.showerror("Error", "Unknown error during replacement (key missing).", parent=root)
            close_ref()
            return
        data[page][nrep] = anrep
        save_data(data, parent=root)
        messagebox.showinfo("Replaced", f"'{orep}' replaced with '{nrep}': '{anrep}'", parent=root)
        close_ref()
    except Exception as e:
        messagebox.showerror("Error", f"Unexpected error in replace_word:\n{e}\n\n{traceback.format_exc()}", parent=root)


def remove_page():
    try:
        data = load_data(parent=root)
        if not data:
            messagebox.showinfo("Info", "No pages to remove.", parent=root)
            return
        page = ask_page_number(f"Choose page to delete (existing: {tuple(int(i) for i in data)}):", parent=root, must_exist=True, data=data)
        if page is None:
            return
        confirm = messagebox.askyesno("Confirm", f"Are you sure you want to delete page {page}?", parent=root)
        if not confirm:
            return
        del data[page]
        save_data(data, parent=root)
        messagebox.showinfo("Removed", f"Page {page} has been removed.", parent=root)
    except Exception as e:
        messagebox.showerror("Error", f"Unexpected error in remove_page:\n{e}\n\n{traceback.format_exc()}", parent=root)


def remove_word():
    try:
        data = load_data(parent=root)
        if not data:
            messagebox.showinfo("Info", "No words/pages to remove.", parent=root)
            return
        page = ask_page_number("Enter page number that contains the word you want to delete:", parent=root, must_exist=True, data=data)
        if page is None:
            return
        pagetwrd = ask_nonempty_string("Remove Word", f"Enter English word to delete from page {page}:", parent=root)
        if pagetwrd is None:
            return
        if pagetwrd not in data[page]:
            messagebox.showerror("Error", f"'{pagetwrd}' not found in page {page}.", parent=root)
            return
        confirm = messagebox.askyesno("Confirm", f"Remove '{pagetwrd}' from page {page}?", parent=root)
        if not confirm:
            return
        del data[page][pagetwrd]
        save_data(data, parent=root)
        messagebox.showinfo("Removed", f"Word {pagetwrd} removed from page {page}.", parent=root)
    except Exception as e:
        messagebox.showerror("Error", f"Unexpected error in remove_word:\n{e}\n\n{traceback.format_exc()}", parent=root)


# ----------------- GUI setup -----------------
root = tk.Tk()
root.title("Words Manager")
root.geometry("320x340")
center_window(root, width=320, height=340, parent=None)

buttons = [
    ("Print", show_data),
    ("Add Word", add_word),
    ("Add Page", add_page),
    ("Replace Word", replace_word),
    ("Remove Page", remove_page),
    ("Remove Word", remove_word),
    ("Exit", root.quit),
]

for (text, cmd) in buttons:
    b = tk.Button(root, text=text, width=28, command=cmd)
    b.pack(pady=6)

root.mainloop()
