# -*- coding: utf-8 -*-
\"\"\"Abjad Calculator - Offline (Golden & Dark Theme)
Shows ONLY the TOTAL Abjad (Abjad-e-Kabir) value for any Arabic/Urdu name.
Features:
- Dark (black) background with golden accents
- Input box for Arabic/Urdu name
- Live calculation: shows only TOTAL (e.g., محمد -> 92)
- Optional: Save to local history (JSON) for later review (hidden, non-intrusive)
- To create .exe: use PyInstaller (instructions below)
\"\"\"

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json, os
from datetime import datetime

# --- Abjad Kabir mapping ---
ABJAD = {
    "ا":1,"أ":1,"إ":1,"آ":1,
    "ب":2,"ج":3,"د":4,"ہ":5,"ھ":5,"ء":0,
    "و":6,"ؤ":6,"ز":7,"ح":8,"ط":9,
    "ی":10,"ي":10,"ى":10,
    "ک":20,"ك":20,"ل":30,"م":40,"ن":50,
    "س":60,"ع":70,"ف":80,"ص":90,"ق":100,
    "ر":200,"ش":300,"ت":400,"ث":500,"خ":600,
    "ذ":700,"ض":800,"ظ":900,"غ":1000
}

APP_DIR = os.path.dirname(os.path.abspath(__file__))
HISTORY_FILE = os.path.join(APP_DIR, "abjad_history.json")

def calc_total(text):
    total = 0
    for ch in text:
        if ch.strip() == "":
            continue
        val = ABJAD.get(ch)
        if val is None:
            # ignore unknown characters (Latin letters, punctuation)
            continue
        total += val
    return total

def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def save_history_entry(name, total):
    history = load_history()
    history.insert(0, {"name": name, "total": total, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
    history = history[:1000]
    try:
        with open(HISTORY_FILE, "w", encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
        return True
    except Exception:
        return False

# --- GUI ---
class GoldenAbjadApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Abjad Calculator - Offline")
        self.geometry("540x260")
        self.resizable(False, False)
        self.configure(bg="#0b0b0b")  # near-black background

        # Fonts and styles
        self.font_input = ("Segoe UI", 16)
        self.font_total = ("Segoe UI Semibold", 36)
        self.golden = "#d4af37"

        # Input label
        lbl = tk.Label(self, text="نام درج کریں (عربی/اردو):", bg="#0b0b0b", fg="white", font=("Segoe UI", 11))
        lbl.pack(pady=(18,6))

        # Input entry
        self.input_var = tk.StringVar()
        self.entry = tk.Entry(self, textvariable=self.input_var, font=self.font_input, justify="center", bd=0, bg="#1b1b1b", fg="white", insertbackground="white")
        self.entry.pack(ipadx=10, ipady=8, padx=20, fill="x")
        self.entry.focus_set()
        self.entry.bind("<KeyRelease>", self.on_key)

        # Total display frame
        total_frame = tk.Frame(self, bg="#0b0b0b")
        total_frame.pack(pady=(12,0), fill="x")

        tk.Label(total_frame, text="کل عدد:", bg="#0b0b0b", fg="white", font=("Segoe UI", 12)).pack(side="left", padx=(20,10))
        self.total_var = tk.StringVar(value="0")
        self.total_label = tk.Label(total_frame, textvariable=self.total_var, bg="#0b0b0b", fg=self.golden, font=self.font_total)
        self.total_label.pack(side="left")

        # Buttons frame (small, minimal)
        btn_frame = tk.Frame(self, bg="#0b0b0b")
        btn_frame.pack(pady=(12,0))

        save_btn = tk.Button(btn_frame, text="Save", command=self.save_now, bg="#1f1f1f", fg="white", bd=0, padx=12, pady=6)
        save_btn.grid(row=0, column=0, padx=6)
        clear_btn = tk.Button(btn_frame, text="Clear", command=self.clear_input, bg="#1f1f1f", fg="white", bd=0, padx=12, pady=6)
        clear_btn.grid(row=0, column=1, padx=6)
        export_btn = tk.Button(btn_frame, text="Export History", command=self.export_history, bg="#1f1f1f", fg="white", bd=0, padx=12, pady=6)
        export_btn.grid(row=0, column=2, padx=6)

        # Status label
        self.status = tk.Label(self, text="Ready", bg="#0b0b0b", fg="gray", font=("Segoe UI",9))
        self.status.pack(pady=(8,0))

        # Initialize
        self.on_key()

    def on_key(self, event=None):
        name = self.input_var.get().strip()
        total = calc_total(name)
        self.total_var.set(str(total))

    def save_now(self):
        name = self.input_var.get().strip()
        if name == "":
            messagebox.showinfo("Empty", "پہلے کوئی نام درج کریں۔")
            return
        total = calc_total(name)
        ok = save_history_entry(name, total)
        if ok:
            self.status.config(text=f"Saved: {name} = {total}")
        else:
            self.status.config(text="Error saving history")

    def clear_input(self):
        self.input_var.set("")
        self.on_key()

    def export_history(self):
        history = load_history()
        if not history:
            messagebox.showinfo("No Data", "کوئی ہسٹری موجود نہیں ہے۔")
            return
        file = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files","*.csv")], title="Export History")
        if not file:
            return
        try:
            import csv
            with open(file, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["timestamp","name","total"])
                for item in history:
                    writer.writerow([item["timestamp"], item["name"], item["total"]])
            messagebox.showinfo("Exported", f"Exported to: {file}")
        except Exception as e:
            messagebox.showerror("Error", f"Error exporting: {e}")

if __name__ == "__main__":
    app = GoldenAbjadApp()
    app.mainloop()

# Instructions to create .exe using PyInstaller:
# 1. Install PyInstaller: pip install pyinstaller
# 2. From command prompt in the script's folder run:
#    pyinstaller --onefile --noconsole --icon=icon.ico Abjad_Abjad_Golden_Dark.py
# 3. The built executable will be in the dist/ folder.
# If you want the app window to show an icon, put an icon.ico file in the same folder and use the --icon option.
